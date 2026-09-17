#!/usr/bin/env python3
"""
Universal Data Analyst V2 - 通用数据分析专家（优化版）

优化内容：
1. LLM 步骤解耦：支持 autonomous 模式，无需外部 LLM 响应
2. 多文件/多表关联：支持多文件输入和自动关联检测
3. 质量驱动策略：根据数据质量自动调整分析策略

工作流程：
1. 加载数据 (data_loader) - 支持多文件
2. 数据本体识别 (ontology profiling) - 支持 autonomous 模式
3. 数据质量校验 (data_validator) - 质量驱动的策略调整
4. 多表关联分析 (multi_table_join) - 自动检测关联可行性
5. 分析方案规划 (analysis planning) - 支持 autonomous 模式
6. 生成并执行分析脚本
7. 输出分析报告
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Union
from dataclasses import dataclass, asdict, field
from datetime import datetime
import warnings

import pandas as pd
import numpy as np

# Add skill layers to path
SKILL_ROOT = Path(__file__).parent
sys.path.insert(0, str(SKILL_ROOT))
sys.path.insert(0, str(SKILL_ROOT / 'layers'))

from layers.data_loader import DataLoader, DataLoadResult, DataFormat
from layers.data_validator import DataValidator, ValidationReport


@dataclass
class DataOntology:
    """数据本体识别结果"""
    entity_type: str = "特征/属性型"
    entity_type_reason: str = "默认：每行是一个实体的属性描述"
    generation_mechanism: str = "观测型"
    mechanism_reason: str = "默认：被动记录的数据"
    core_dimensions: List[Dict[str, str]] = field(default_factory=list)
    quality_assessment: str = "未评估"
    is_economic: bool = False
    economic_type: Optional[str] = None
    domain_type: str = "通用"
    keywords: List[str] = field(default_factory=lambda: ["数据", "分析"])
    recommended_questions: List[str] = field(default_factory=lambda: ["描述性统计"])
    limitations: List[str] = field(default_factory=lambda: ["无已知局限"])
    confidence: str = "低"  # 自主识别的置信度


@dataclass
class AnalysisPlan:
    """分析方案"""
    question_type: str = "描述型"
    question_type_reason: str = "默认：用户诉求未明确因果推断"
    frameworks: List[Dict[str, str]] = field(default_factory=list)
    analysis_steps: List[Dict[str, Any]] = field(default_factory=list)
    scripts: List[Dict[str, str]] = field(default_factory=list)
    expected_outputs: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    quality_adjustments: List[str] = field(default_factory=list)  # 质量驱动的调整


@dataclass
class MultiTableProfile:
    """多表关联分析结果"""
    can_join: bool = False
    join_type: str = "left"  # left, inner, outer
    left_table: str = ""
    right_table: str = ""
    left_key: str = ""
    right_key: str = ""
    left_cardinality: int = 0
    right_cardinality: int = 0
    coverage: float = 0.0  # 关联覆盖率
    type_conflicts: List[Dict[str, str]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class UniversalDataAnalystV2:
    """通用数据分析主类（V2优化版）"""

    def __init__(self, autonomous: bool = False):
        self.loader = DataLoader()
        self.validator = DataValidator()
        self.autonomous = autonomous  # 自主模式开关

        # 多文件支持
        self.data_dict: Dict[str, pd.DataFrame] = {}  # 存储多个数据表
        self.load_results: Dict[str, DataLoadResult] = {}
        self.primary_table: Optional[str] = None

        # 分析状态
        self.validation_report: Optional[ValidationReport] = None
        self.ontology: Optional[DataOntology] = None
        self.analysis_plan: Optional[AnalysisPlan] = None
        self.multi_table_profile: Optional[MultiTableProfile] = None
        self.quality_strategy: Dict[str, Any] = {}  # 质量驱动的策略

    # ========== 多文件加载支持 ==========

    def load_multiple_files(self, file_paths: List[str], **kwargs) -> Dict[str, DataLoadResult]:
        """
        加载多个数据文件

        Args:
            file_paths: 文件路径列表
            **kwargs: 传递给 loader 的参数

        Returns:
            各文件的加载结果字典
        """
        print(f"📂 正在加载 {len(file_paths)} 个数据文件...")

        results = {}
        for i, file_path in enumerate(file_paths, 1):
            print(f"\n  [{i}/{len(file_paths)}] 加载: {file_path}")
            result = self.loader.execute({'file_path': file_path, **kwargs})

            if result.success:
                # 使用文件名（不含扩展名）作为表名
                table_name = Path(file_path).stem
                self.data_dict[table_name] = result.data
                self.load_results[table_name] = result
                results[table_name] = result
                print(f"      ✓ 成功: {result.rows:,} 行 × {result.columns} 列")
            else:
                print(f"      ✗ 失败: {result.errors}")
                results[Path(file_path).stem] = result

        # 设置主表（第一个成功加载的表）
        if self.data_dict:
            self.primary_table = list(self.data_dict.keys())[0]
            print(f"\n✅ 主表设置: {self.primary_table}")
            print(f"   共加载 {len(self.data_dict)} 个数据表")

        return results

    # ========== V1 API 兼容层 ==========

    def load_data(self, file_path: str, **kwargs) -> DataLoadResult:
        """V1 API 兼容：加载单个文件"""
        results = self.load_multiple_files([file_path], **kwargs)
        table_name = Path(file_path).stem
        if table_name in results:
            return results[table_name]
        return DataLoadResult(success=False, errors=[f"加载失败: {file_path}"])

    @property
    def data(self):
        """V1 API 兼容：获取主表 DataFrame"""
        if self.primary_table and self.primary_table in self.data_dict:
            return self.data_dict[self.primary_table]
        return None

    @property
    def load_result(self):
        """V1 API 兼容：获取主表加载结果"""
        if self.primary_table and self.primary_table in self.load_results:
            return self.load_results[self.primary_table]
        return None

    def analyze_join_feasibility(self, left_table: str = None, right_table: str = None,
                                  left_key: str = None, right_key: str = None) -> MultiTableProfile:
        """
        分析多表关联可行性

        自动检测关联键、基数、覆盖率等
        """
        if len(self.data_dict) < 2:
            return MultiTableProfile(can_join=False, recommendations=["至少需要2个表才能关联"])

        # 如果没有指定表，使用第一个和第二个
        if left_table is None:
            left_table = list(self.data_dict.keys())[0]
        if right_table is None:
            right_table = list(self.data_dict.keys())[1]

        left_df = self.data_dict[left_table]
        right_df = self.data_dict[right_table]

        profile = MultiTableProfile()
        profile.left_table = left_table
        profile.right_table = right_table

        # 自动检测关联键
        if left_key is None or right_key is None:
            left_key, right_key = self._detect_join_keys(left_df, right_df)

        if left_key is None:
            profile.recommendations.append("无法自动检测关联键，请手动指定")
            return profile

        profile.left_key = left_key
        profile.right_key = right_key

        # 分析基数
        left_unique = left_df[left_key].nunique()
        right_unique = right_df[right_key].nunique()
        profile.left_cardinality = left_unique
        profile.right_cardinality = right_unique

        # 检查类型冲突
        left_dtype = left_df[left_key].dtype
        right_dtype = right_df[right_key].dtype

        if left_dtype != right_dtype:
            profile.type_conflicts.append({
                'left': f"{left_key} ({left_dtype})",
                'right': f"{right_key} ({right_dtype})",
                'suggestion': f"建议统一为 {left_dtype}"
            })

        # 计算覆盖率
        left_values = set(left_df[left_key].dropna().astype(str))
        right_values = set(right_df[right_key].dropna().astype(str))

        if len(left_values) > 0:
            coverage = len(left_values & right_values) / len(left_values)
            profile.coverage = coverage

            if coverage >= 0.95:
                profile.join_type = "inner"
                profile.can_join = True
                profile.recommendations.append(f"覆盖率 {coverage*100:.1f}%，建议使用 INNER JOIN")
            elif coverage >= 0.8:
                profile.join_type = "left"
                profile.can_join = True
                profile.recommendations.append(f"覆盖率 {coverage*100:.1f}%，建议使用 LEFT JOIN（可能丢失部分右表数据）")
            elif coverage >= 0.5:
                profile.join_type = "outer"
                profile.can_join = True
                profile.recommendations.append(f"覆盖率 {coverage*100:.1f}%，建议使用 OUTER JOIN（两侧都有大量未匹配数据）")
            else:
                profile.can_join = False
                profile.recommendations.append(f"⚠️ 覆盖率仅 {coverage*100:.1f}%，关联意义有限")

        # 检测重复键（一对多关系）
        left_duplicates = left_df[left_key].duplicated().sum()
        right_duplicates = right_df[right_key].duplicated().sum()

        if left_duplicates > 0 and right_duplicates > 0:
            profile.recommendations.append(f"注意：两侧关联键都有重复（多对多关系），可能导致笛卡尔积膨胀")
        elif left_duplicates > 0:
            profile.recommendations.append(f"注意：左表关联键有 {left_duplicates} 个重复值（一对多关系）")
        elif right_duplicates > 0:
            profile.recommendations.append(f"注意：右表关联键有 {right_duplicates} 个重复值（多对一关系）")

        self.multi_table_profile = profile
        return profile

    def _detect_join_keys(self, left_df: pd.DataFrame, right_df: pd.DataFrame) -> Tuple[Optional[str], Optional[str]]:
        """自动检测关联键"""
        # 候选键名称
        candidate_names = ['id', 'key', 'code', 'no', 'num', 'user_id', 'product_id', 'order_id']

        left_candidates = []
        right_candidates = []

        for col in left_df.columns:
            col_lower = col.lower()
            if any(cand in col_lower for cand in candidate_names):
                # 优先选择高基数列
                uniqueness = left_df[col].nunique() / len(left_df)
                left_candidates.append((col, uniqueness))

        for col in right_df.columns:
            col_lower = col.lower()
            if any(cand in col_lower for cand in candidate_names):
                uniqueness = right_df[col].nunique() / len(right_df)
                right_candidates.append((col, uniqueness))

        # 按名称匹配度排序
        if left_candidates and right_candidates:
            # 寻找同名列
            left_names = {c[0].lower() for c in left_candidates}
            right_names = {c[0].lower() for c in right_candidates}
            common = left_names & right_names

            if common:
                # 返回第一个匹配的同名列
                match = list(common)[0]
                left_key = next(c[0] for c in left_candidates if c[0].lower() == match)
                right_key = next(c[0] for c in right_candidates if c[0].lower() == match)
                return left_key, right_key

            # 如果没有同名列，返回各自最高基数的候选
            left_key = max(left_candidates, key=lambda x: x[1])[0]
            right_key = max(right_candidates, key=lambda x: x[1])[0]
            return left_key, right_key

        return None, None

    def join_tables(self, left_table: str = None, right_table: str = None,
                    left_key: str = None, right_key: str = None,
                    join_type: str = None) -> pd.DataFrame:
        """
        执行多表关联

        Returns:
            关联后的 DataFrame
        """
        if self.multi_table_profile is None:
            self.analyze_join_feasibility(left_table, right_table, left_key, right_key)

        profile = self.multi_table_profile

        if not profile.can_join:
            raise ValueError(f"无法关联: {profile.recommendations}")

        left_df = self.data_dict[profile.left_table]
        right_df = self.data_dict[profile.right_table]

        join_type = join_type or profile.join_type

        # 处理类型冲突
        if profile.type_conflicts:
            # 统一为左表类型
            right_df = right_df.copy()
            right_df[profile.right_key] = right_df[profile.right_key].astype(
                left_df[profile.left_key].dtype
            )

        # 执行关联
        merged = left_df.merge(
            right_df,
            left_on=profile.left_key,
            right_on=profile.right_key,
            how=join_type,
            suffixes=('', f'_{profile.right_table}')
        )

        # 更新主表
        self.data_dict['merged'] = merged
        self.primary_table = 'merged'

        print(f"\n🔗 关联完成:")
        print(f"   左表: {profile.left_table} ({len(left_df):,} 行)")
        print(f"   右表: {profile.right_table} ({len(right_df):,} 行)")
        print(f"   结果: {len(merged):,} 行")
        print(f"   方式: {join_type.upper()} JOIN on {profile.left_key}={profile.right_key}")

        return merged

    # ========== Autonomous 模式支持 ==========

    def profile_data_ontology(self, autonomous: bool = None) -> Union[str, DataOntology]:
        """
        步骤2: 数据本体识别

        Args:
            autonomous: 是否使用自主模式（无需LLM）

        Returns:
            autonomous=True 时返回 DataOntology 对象
            autonomous=False 时返回提示词字符串（需外部调用LLM）
        """
        autonomous = autonomous if autonomous is not None else self.autonomous

        if not self.data_dict:
            raise ValueError("请先加载数据")

        # 使用主表进行本体识别
        primary_df = self.data_dict[self.primary_table]

        print("\n🔍 正在进行数据本体识别...")

        if autonomous:
            # 自主模式：基于规则自动推断
            self.ontology = self._autonomous_ontology_inference(primary_df)
            print(f"   ✓ 自主识别完成（置信度: {self.ontology.confidence}）")
            return self.ontology
        else:
            # 交互模式：生成提示词供外部LLM使用
            data_profile = self._generate_data_profile(primary_df)
            prompt = self._build_ontology_prompt(data_profile)
            return prompt

    def _autonomous_ontology_inference(self, df: pd.DataFrame) -> DataOntology:
        """基于规则自动推断数据本体"""
        ontology = DataOntology()

        # 检测实体类型
        col_names = [c.lower() for c in df.columns]

        # 时序检测
        time_indicators = ['time', 'date', 'timestamp', 'created', 'updated', 'day', 'month', 'year']
        time_cols = [c for c in col_names if any(t in c for t in time_indicators)]

        if time_cols and len(df) > 1000:
            ontology.entity_type = "时序/轨迹型"
            ontology.entity_type_reason = f"检测到时间列: {time_cols[:3]}，且数据量大({len(df):,})，可能包含时间序列模式"
            ontology.core_dimensions.append({"维度": "时间", "说明": f"列: {', '.join(time_cols[:3])}"})

        # 交易/经济检测
        money_indicators = ['price', 'cost', 'amount', 'revenue', 'profit', 'salary', 'income', 'pay']
        money_cols = [c for c in col_names if any(m in c for m in money_indicators)]

        if money_cols:
            ontology.is_economic = True
            ontology.economic_type = "交易数据"
            ontology.entity_type = "交易/事件型"
            ontology.entity_type_reason = f"检测到货币列: {money_cols[:3]}"
            ontology.core_dimensions.append({"维度": "经济", "说明": f"货币列: {', '.join(money_cols[:3])}"})

        # ID/关系检测
        id_indicators = ['id', 'user', 'customer', 'product', 'order', 'item']
        id_cols = [c for c in col_names if any(i in c for i in id_indicators)]

        if len(id_cols) >= 2:
            if ontology.entity_type == "特征/属性型":
                ontology.entity_type = "关系/网络型"
                ontology.entity_type_reason = f"检测到多个实体ID: {id_cols[:3]}，可能存在关联关系"
            ontology.core_dimensions.append({"维度": "实体", "说明": f"ID列: {', '.join(id_cols[:3])}"})

        # 地理检测
        geo_indicators = ['city', 'country', 'region', 'location', 'lat', 'lng', 'address']
        geo_cols = [c for c in col_names if any(g in c for g in geo_indicators)]

        if geo_cols:
            ontology.core_dimensions.append({"维度": "地理", "说明": f"地理列: {', '.join(geo_cols[:3])}"})

        # 生成关键词
        ontology.keywords = list(set(
            [ontology.entity_type.split('/')[0]] +
            [ontology.economic_type] if ontology.economic_type else [] +
            time_cols[:1] + money_cols[:1] + id_cols[:1]
        ))[:5]

        # 推荐问题
        if ontology.is_economic:
            ontology.recommended_questions = ["收入/支出分布", "趋势变化", "异常检测", "预测"]
        elif "时序" in ontology.entity_type:
            ontology.recommended_questions = ["时间趋势", "周期性", "异常检测", "预测"]
        elif "关系" in ontology.entity_type:
            ontology.recommended_questions = ["关联分析", "网络结构", "群体发现"]
        else:
            ontology.recommended_questions = ["描述性统计", "分布特征", "异常检测"]

        # 局限性
        ontology.limitations = []
        if len(df) < 100:
            ontology.limitations.append("样本量小，统计推断能力有限")
        if df.isnull().sum().sum() / (len(df) * len(df.columns)) > 0.1:
            ontology.limitations.append("缺失率较高，需注意缺失值影响")

        # 置信度
        if len(ontology.core_dimensions) >= 2 and ontology.entity_type != "特征/属性型":
            ontology.confidence = "高"
        elif len(ontology.core_dimensions) >= 1:
            ontology.confidence = "中"
        else:
            ontology.confidence = "低"

        return ontology

    # ========== 质量驱动的策略调整 ==========

    def validate_data(self, table_name: str = None) -> ValidationReport:
        """
        步骤3: 数据质量校验（含质量驱动的策略调整）
        """
        if not self.data_dict:
            raise ValueError("请先加载数据")

        table_name = table_name or self.primary_table
        df = self.data_dict[table_name]

        print(f"\n🔎 正在对 '{table_name}' 进行数据质量校验...")
        self.validation_report = self.validator.execute(df)

        print(f"   质量评分: {self.validation_report.overall_score:.1f}/100")
        print(f"   发现问题: {len(self.validation_report.issues)} 个")

        # 生成质量驱动的策略调整
        self.quality_strategy = self._generate_quality_strategy()

        if self.quality_strategy.get('adjustments'):
            print(f"\n   📋 基于质量的策略调整:")
            for adj in self.quality_strategy['adjustments']:
                print(f"      • {adj}")

        return self.validation_report

    def _generate_quality_strategy(self) -> Dict[str, Any]:
        """基于数据质量生成分析策略调整"""
        strategy = {
            'score': self.validation_report.overall_score,
            'adjustments': [],
            'recommended_methods': [],
            'avoid_methods': [],
            'confidence_level': 'normal'
        }

        if not self.validation_report:
            return strategy

        # 根据质量评分调整策略
        score = self.validation_report.overall_score

        if score >= 90:
            strategy['confidence_level'] = 'high'
            strategy['adjustments'].append("数据质量优秀，可进行复杂推断分析")
        elif score >= 70:
            strategy['confidence_level'] = 'normal'
            strategy['adjustments'].append("数据质量良好，标准分析流程适用")
        elif score >= 50:
            strategy['confidence_level'] = 'low'
            strategy['adjustments'].append("数据质量一般，建议优先进行数据清洗")
            strategy['avoid_methods'].append("复杂的因果推断（内生性问题可能被放大）")
        else:
            strategy['confidence_level'] = 'critical'
            strategy['adjustments'].append("⚠️ 数据质量差，分析结论可信度低")
            strategy['avoid_methods'].extend(["预测模型", "因果推断", "统计假设检验"])
            strategy['recommended_methods'].append("探索性数据分析（EDA）")
            strategy['recommended_methods'].append("数据质量问题诊断")

        # 检查具体问题并调整
        from layers.data_validator import IssueSeverity
        critical_issues = [i for i in self.validation_report.issues if i.severity == IssueSeverity.CRITICAL]
        high_missing = [i for i in self.validation_report.issues if '缺失' in str(i) and getattr(i, 'percentage', 0) > 20]

        if critical_issues:
            strategy['adjustments'].append(f"发现 {len(critical_issues)} 个严重问题，需优先处理")

        if high_missing:
            strategy['adjustments'].append("部分字段缺失率>20%，建议使用完整案例分析或插值")
            strategy['avoid_methods'].append("直接使用含缺失的字段进行回归分析")

        # 时序相关检查
        if self.data_dict:
            df = list(self.data_dict.values())[0]
            time_cols = [c for c in df.columns if any(t in c.lower() for t in ['time', 'date', 'timestamp'])]

            if time_cols:
                for col in time_cols:
                    missing_pct = df[col].isnull().sum() / len(df) * 100
                    if missing_pct > 5:
                        strategy['adjustments'].append(f"时间列 '{col}' 缺失率 {missing_pct:.1f}%，时序分析需谨慎")
                        strategy['avoid_methods'].append(f"基于 '{col}' 的精确时序分析")

        return strategy

    # ========== 分析方案规划（含质量调整） ==========

    def plan_analysis(self, user_intent: str, autonomous: bool = None) -> Union[str, AnalysisPlan]:
        """
        步骤4: 分析方案规划

        结合质量策略调整分析方案
        """
        autonomous = autonomous if autonomous is not None else self.autonomous

        if not self.data_dict:
            raise ValueError("请先加载数据")

        print(f"\n📋 正在规划分析方案...")
        print(f"   用户诉求: {user_intent}")

        if self.quality_strategy.get('adjustments'):
            print(f"   质量调整: 已应用 {len(self.quality_strategy['adjustments'])} 项策略")

        if autonomous:
            self.analysis_plan = self._autonomous_plan_generation(user_intent)
            print(f"   ✓ 自主规划完成")
            return self.analysis_plan
        else:
            primary_df = self.data_dict[self.primary_table]
            prompt = self._build_planning_prompt(user_intent, primary_df)
            return prompt

    def _autonomous_plan_generation(self, user_intent: str) -> AnalysisPlan:
        """基于规则自动生成分析方案"""
        plan = AnalysisPlan()

        # 问题类型判定
        intent_lower = user_intent.lower()

        if any(w in intent_lower for w in ['为什么', '原因', '因素']):
            plan.question_type = "诊断型"
            plan.question_type_reason = "用户询问原因"
        elif any(w in intent_lower for w in ['预测', '未来', '将会']):
            plan.question_type = "预测型"
            plan.question_type_reason = "用户要求预测"
        elif any(w in intent_lower for w in ['验证', '因果', '影响']):
            plan.question_type = "因果型"
            plan.question_type_reason = "用户要求验证因果关系"
        else:
            plan.question_type = "描述型"
            plan.question_type_reason = "默认：描述性分析"

        # 应用质量调整
        if self.quality_strategy:
            plan.quality_adjustments = self.quality_strategy.get('adjustments', [])

            # 如果质量低，降低分析复杂度
            if self.quality_strategy.get('confidence_level') == 'critical':
                plan.question_type = "描述型"
                plan.question_type_reason += "（因数据质量问题降级）"
                plan.risks.append("数据质量差，所有推断结论可信度低")

        # 推荐框架
        if self.ontology:
            if "时序" in self.ontology.entity_type:
                plan.frameworks.append({"框架": "时序分析", "理由": "数据包含时间维度"})
            if self.ontology.is_economic:
                plan.frameworks.append({"框架": "经济计量", "理由": "经济数据特征"})
            if "关系" in self.ontology.entity_type:
                plan.frameworks.append({"框架": "网络分析", "理由": "多实体关联"})

        # 基础框架
        plan.frameworks.append({"框架": "描述统计", "理由": "所有分析的基础"})

        # 分析步骤
        steps = [
            {"步骤": 1, "名称": "数据概览", "内容": "基础统计、分布分析"},
            {"步骤": 2, "名称": "质量检查", "内容": "缺失值、异常值处理"},
        ]

        if plan.question_type in ["诊断型", "因果型"]:
            steps.append({"步骤": 3, "名称": "相关性分析", "内容": "探索变量关系"})
            steps.append({"步骤": 4, "名称": "诊断验证", "内容": "回归分析、分组对比"})

        if plan.question_type == "预测型":
            steps.append({"步骤": 3, "名称": "特征工程", "内容": "构建预测特征"})
            steps.append({"步骤": 4, "名称": "模型训练", "内容": "时序预测或机器学习"})

        plan.analysis_steps = steps
        plan.expected_outputs = ["HTML报告", "可视化图表", "分析摘要"]

        return plan

    # ========== 辅助方法（保持不变） ==========

    def _generate_data_profile(self, df: pd.DataFrame) -> Dict[str, Any]:
        """生成数据画像"""
        profile = {
            'shape': df.shape,
            'memory_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'columns': []
        }

        for col in df.columns:
            col_info = {
                'name': col,
                'dtype': str(df[col].dtype),
                'null_count': df[col].isnull().sum(),
                'null_pct': df[col].isnull().sum() / len(df) * 100,
                'unique_count': df[col].nunique(),
            }

            if pd.api.types.is_numeric_dtype(df[col]):
                col_info.update({
                    'type': 'numeric',
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'mean': df[col].mean() if df[col].notna().any() else None,
                })
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                col_info.update({
                    'type': 'datetime',
                    'min': str(df[col].min()),
                    'max': str(df[col].max()),
                })
            else:
                col_info.update({
                    'type': 'categorical' if df[col].nunique() < 100 else 'text',
                    'sample_values': df[col].dropna().head(5).tolist(),
                })

            profile['columns'].append(col_info)

        profile['potential_time_cols'] = [
            col for col in df.columns
            if any(keyword in col.lower() for keyword in ['time', 'date', 'timestamp', 'created', 'updated'])
        ]

        profile['potential_price_cols'] = [
            col for col in df.columns
            if any(keyword in col.lower() for keyword in ['price', 'cost', 'amount', 'revenue', 'profit'])
            and pd.api.types.is_numeric_dtype(df[col])
        ]

        return profile

    def _build_ontology_prompt(self, data_profile: Dict[str, Any]) -> str:
        """构建数据本体识别提示词"""
        prompt = f"""你是一位数据本体论专家。请分析以下数据的基本特征。

数据概况：
- 行数: {data_profile['shape'][0]:,}
- 列数: {data_profile['shape'][1]}
- 内存: {data_profile['memory_mb']:.2f} MB

字段详情：
"""
        for col in data_profile['columns'][:10]:
            prompt += f"\n- {col['name']} ({col['type']}, {col['dtype']})"
            if col.get('unique_count'):
                prompt += f", 唯一值: {col['unique_count']: ,}"
            if col.get('null_pct') > 0:
                prompt += f", 缺失率: {col['null_pct']:.1f}%"

        if data_profile.get('potential_time_cols'):
            prompt += f"\n\n潜在时间列: {data_profile['potential_time_cols']}"
        if data_profile.get('potential_price_cols'):
            prompt += f"\n潜在价格/货币列: {data_profile['potential_price_cols']}"

        prompt += """

请回答：
1. 实体类型：交易/事件型、状态/存量型、关系/网络型、特征/属性型、时序/轨迹型？
2. 数据生成机制：观测/实验/模拟/测量/报告？
3. 核心维度：时间？地理？分类？网络关系？
4. 是否经济型数据？如果是，初步判断类型？
5. 3-5个关键词标签
6. 最适合回答什么问题？
7. 明显局限性？
"""
        return prompt

    def _build_planning_prompt(self, user_intent: str, df: pd.DataFrame) -> str:
        """构建分析规划提示词"""
        sample = df.head(10).to_string()

        column_details = []
        for col in df.columns:
            dtype = df[col].dtype
            unique = df[col].nunique()
            null_pct = df[col].isnull().sum() / len(df) * 100

            detail = f"{col}: {dtype}, 唯一值{unique:,}, 缺失{null_pct:.1f}%"
            if pd.api.types.is_numeric_dtype(df[col]):
                detail += f", 范围[{df[col].min():.2f}, {df[col].max():.2f}]"
            column_details.append(detail)

        # 添加质量策略信息
        quality_info = ""
        if self.quality_strategy:
            quality_info = f"""
数据质量信息：
- 质量评分: {self.quality_strategy.get('score', 'N/A')}/100
- 置信级别: {self.quality_strategy.get('confidence_level', 'unknown')}
- 建议避免的方法: {', '.join(self.quality_strategy.get('avoid_methods', []))}
- 建议采用的方法: {', '.join(self.quality_strategy.get('recommended_methods', []))}
"""

        prompt = f"""你是一位跨领域数据分析专家。请规划完整的分析方案。

用户诉求: {user_intent}

{quality_info}

数据样本（前10行）:
{sample}

字段详情:
{chr(10).join(column_details)}

请完成：
1. 问题类型判定（描述/诊断/预测/规范/因果）
2. 推荐分析框架及理由
3. 分步骤分析路径（具体到代码逻辑）
4. 脚本文件清单
5. 预期输出
"""
        return prompt

    def save_session(self, output_dir: str = "./analysis_output") -> str:
        """保存分析会话"""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_file = os.path.join(output_dir, f"session_v2_{timestamp}.json")

        session_data = {
            'timestamp': timestamp,
            'version': '2.0',
            'autonomous': self.autonomous,
            'tables': list(self.data_dict.keys()),
            'primary_table': self.primary_table,
            'validation': self.validation_report.to_dict() if self.validation_report else None,
            'ontology': asdict(self.ontology) if self.ontology else None,
            'quality_strategy': self.quality_strategy,
            'multi_table_profile': asdict(self.multi_table_profile) if self.multi_table_profile else None,
        }

        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2, default=str)

        return session_file


# ========== 命令行入口 ==========

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='通用数据分析工具 V2（优化版）')
    parser.add_argument('files', nargs='+', help='数据文件路径（支持多个）')
    parser.add_argument('--intent', '-i', help='用户分析诉求', default='探索性数据分析')
    parser.add_argument('--validate', '-v', action='store_true', help='执行数据质量校验')
    parser.add_argument('--output', '-o', default='./analysis_output', help='输出目录')
    parser.add_argument('--autonomous', '-a', action='store_true',
                        help='自主模式：不依赖外部LLM，自动完成所有判断')
    parser.add_argument('--join', '-j', action='store_true',
                        help='自动分析并执行多表关联')

    args = parser.parse_args()

    # 初始化分析器
    analyst = UniversalDataAnalystV2(autonomous=args.autonomous)

    print("="*70)
    print("Universal Data Analyst V2 (优化版)")
    print(f"模式: {'自主模式' if args.autonomous else '交互模式'}")
    print("="*70)

    # 步骤1: 加载多个数据文件
    results = analyst.load_multiple_files(args.files)

    if not analyst.data_dict:
        print("❌ 没有成功加载任何数据文件")
        sys.exit(1)

    # 多表关联（如果需要）
    if args.join and len(analyst.data_dict) >= 2:
        print("\n" + "="*70)
        print("【多表关联分析】")
        print("="*70)

        profile = analyst.analyze_join_feasibility()

        print(f"\n关联可行性分析:")
        print(f"  左表: {profile.left_table}")
        print(f"  右表: {profile.right_table}")
        print(f"  关联键: {profile.left_key} = {profile.right_key}")
        print(f"  覆盖率: {profile.coverage*100:.1f}%")
        print(f"  建议: {profile.recommendations[0] if profile.recommendations else 'N/A'}")

        if profile.can_join:
            merged = analyst.join_tables()
            print(f"\n✅ 关联完成，主表已更新为 'merged'")
        else:
            print(f"\n⚠️ 不建议关联: {profile.recommendations}")

    # 步骤2: 数据本体识别
    print("\n" + "="*70)
    print("【步骤2】数据本体识别")
    print("="*70)

    ontology_result = analyst.profile_data_ontology()

    if args.autonomous:
        onto = ontology_result
        print(f"\n✓ 自主识别结果:")
        print(f"  实体类型: {onto.entity_type}")
        print(f"  生成机制: {onto.generation_mechanism}")
        print(f"  核心维度: {', '.join([d.get('维度', '') for d in onto.core_dimensions])}")
        print(f"  关键词: {', '.join(onto.keywords)}")
        print(f"  置信度: {onto.confidence}")
    else:
        print("\n提示词（需调用大模型）:")
        print(ontology_result[:500] + "...")

    # 步骤3: 数据质量校验
    if args.validate:
        print("\n" + "="*70)
        print("【步骤3】数据质量校验")
        print("="*70)

        analyst.validate_data()

    # 步骤4: 分析方案规划
    print("\n" + "="*70)
    print("【步骤4】分析方案规划")
    print("="*70)

    plan_result = analyst.plan_analysis(args.intent)

    if args.autonomous:
        plan = plan_result
        print(f"\n✓ 自主规划结果:")
        print(f"  问题类型: {plan.question_type}")
        print(f"  分析框架: {', '.join([f.get('框架', '') for f in plan.frameworks])}")
        print(f"  分析步骤: {len(plan.analysis_steps)} 步")
        if plan.quality_adjustments:
            print(f"  质量调整: {len(plan.quality_adjustments)} 项")
    else:
        print("\n提示词（需调用大模型）:")
        print(plan_result[:500] + "...")

    # 保存会话
    session_file = analyst.save_session(args.output)
    print(f"\n💾 会话已保存: {session_file}")

    print("\n" + "="*70)
    print("分析准备完成")
    print("="*70)


if __name__ == '__main__':
    main()

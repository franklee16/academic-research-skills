#!/usr/bin/env python3
"""
Orchestrator V2 - 增强版流程编排器

改进点：
1. 集成流程健康监控 - 每个步骤都有状态追踪
2. 明确的错误提示 - 步骤失败时给用户清晰的报错和建议
3. 流程中断检测 - 关键步骤失败时阻止后续步骤执行
4. 最终健康报告 - 输出完整的流程执行状态
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime

# Setup paths
SKILL_ROOT = Path(__file__).parent
sys.path.insert(0, str(SKILL_ROOT))
sys.path.insert(0, str(SKILL_ROOT / 'layers'))

from main import UniversalDataAnalystV2 as UniversalDataAnalyst, DataOntology, AnalysisPlan
from llm_analyzer import LLMAnalyzer, OntologyResult, AnalysisPlan as LLMAnalysisPlan
from report_generator import ReportGenerator
from flow_health_monitor import FlowHealthMonitor, StepStatus, StepImportance


class DataAnalysisOrchestratorV2:
    """
    增强版数据分析流程编排器（带健康监控）
    """

    def __init__(self, output_dir: str = "./analysis_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # 初始化组件
        self.analyst = UniversalDataAnalyst()
        self.llm_analyzer = LLMAnalyzer()
        self.report_generator = None

        # 初始化流程健康监控器
        self.health_monitor = FlowHealthMonitor()

        # 会话状态
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = self.output_dir / f"session_{self.session_id}"
        self.session_dir.mkdir(exist_ok=True)

        # 初始化报告生成器
        self.report_generator = ReportGenerator(str(self.session_dir))

        # 缓存结果
        self.ontology_result: Optional[OntologyResult] = None
        self.analysis_plan: Optional[LLMAnalysisPlan] = None
        self.validation_report_dict: Optional[Dict] = None
        self.data_info: Optional[Dict] = None

    def step1_load_data(self, file_path: str, **kwargs) -> Tuple[bool, str]:
        """步骤1: 加载数据（带健康监控）"""
        print("\n" + "="*80)
        print("【步骤1/7】数据加载")
        print("="*80)

        # 检查是否可以执行
        if not self.health_monitor.record_step_start("load"):
            return False, "步骤被阻塞，无法执行"

        try:
            result = self.analyst.load_data(file_path, **kwargs)

            if result.success:
                msg = f"✅ 加载成功: {result.rows:,} 行 × {result.columns} 列"
                print(msg)

                # 检查编码回退警告
                if result.warnings:
                    print(f"\n⚠️ 警告:")
                    for warning in result.warnings:
                        print(f"   - {warning}")

                # 保存数据基本信息
                self.data_info = {
                    "file_path": file_path,
                    "file_name": Path(file_path).name,
                    "rows": result.rows,
                    "columns": result.columns,
                    "memory_mb": result.memory_usage_mb,
                    "column_names": list(self.analyst.data.columns),
                    "encoding": result.encoding,
                    "report_title": f"{Path(file_path).stem} 数据分析报告"
                }
                self._save_json("step1_data_info.json", self.data_info)

                # 记录成功
                self.health_monitor.record_step_success(
                    "load",
                    message=msg,
                    details={
                        "rows": result.rows,
                        "columns": result.columns,
                        "encoding": result.encoding
                    }
                )
                return True, msg
            else:
                msg = f"❌ 加载失败: {result.errors}"
                print(msg)

                # 分析错误类型，给出建议
                suggestions = []
                for error in result.errors:
                    if "encoding" in error.lower() or "codec" in error.lower():
                        suggestions.extend([
                            "文件编码可能不是UTF-8，尝试手动指定encoding参数",
                            "常见中文编码: gbk, gb2312, gb18030",
                            "可使用文本编辑器查看或转换文件编码"
                        ])
                    elif "parser" in error.lower() or "tokeniz" in error.lower():
                        suggestions.extend([
                            "文件格式可能损坏，检查CSV分隔符是否正确",
                            "尝试用文本编辑器打开文件检查内容",
                            "如果是Excel文件，请先另存为CSV格式"
                        ])
                    elif "permission" in error.lower():
                        suggestions.extend([
                            "检查文件读取权限",
                            "尝试将文件复制到其他目录"
                        ])
                    else:
                        suggestions.extend([
                            "检查文件路径是否正确",
                            "确认文件未被其他程序占用"
                        ])

                # 记录失败
                self.health_monitor.record_step_failure(
                    "load",
                    error="; ".join(result.errors),
                    suggestions=suggestions,
                    is_critical=True
                )
                return False, msg

        except Exception as e:
            error_msg = f"❌ 加载异常: {str(e)}"
            print(error_msg)
            self.health_monitor.record_step_failure(
                "load",
                error=str(e),
                suggestions=[
                    "检查文件路径是否正确",
                    "确认文件格式是否为支持的格式(CSV/Excel/Parquet/JSON)",
                    "检查系统内存是否充足"
                ],
                is_critical=True
            )
            return False, error_msg

    def step2_identify_ontology(self) -> Tuple[bool, str, str]:
        """步骤2: 识别数据本体（带健康监控）"""
        print("\n" + "="*80)
        print("【步骤2/7】数据本体识别")
        print("="*80)

        # 检查依赖
        if not self.health_monitor.record_step_start("ontology"):
            blocked_result = self.health_monitor.step_results.get("ontology")
            msg = f"⛔ 步骤被阻塞: {blocked_result.message if blocked_result else '未知原因'}"
            print(msg)
            return False, "", ""

        try:
            # 生成数据画像
            data_profile = self.analyst._generate_data_profile(self.analyst.data)

            # 生成提示词
            prompt = self.llm_analyzer.identify_ontology(data_profile)

            # 保存提示词
            prompt_file = self.session_dir / "step2_ontology_prompt.txt"
            prompt_file.write_text(prompt, encoding='utf-8')

            print("💾 提示词已生成")
            print("\n📋 提示词预览（前500字符）:")
            print("-" * 80)
            print(prompt[:500])
            print("...")

            # 记录成功（但提醒用户需要手动调用LLM）
            self.health_monitor.record_step_success(
                "ontology",
                message="提示词已生成，需要调用LLM完成本体识别",
                details={"prompt_file": str(prompt_file)}
            )

            # 显示重要提醒
            print("\n" + "⚠️" * 40)
            print("【重要提醒】")
            print("⚠️  本体识别需要调用大模型完成！")
            print(f"⚠️  提示词已保存到: {prompt_file}")
            print("⚠️  请使用此提示词调用 Claude 或其他LLM，")
            print("⚠️  然后将结果保存为: ontology_result.json")
            print("⚠️" * 40)

            return True, str(prompt), str(prompt_file)

        except Exception as e:
            error_msg = f"生成提示词失败: {str(e)}"
            print(f"❌ {error_msg}")
            self.health_monitor.record_step_failure(
                "ontology",
                error=error_msg,
                suggestions=[
                    "检查数据是否正确加载",
                    "确认 llm_analyzer 模块正常工作",
                    "可以尝试使用 autonomous 模式跳过此步骤"
                ]
            )
            return False, "", ""

    def step3_validate_data(self) -> Optional[Dict[str, Any]]:
        """步骤3: 数据质量校验（带健康监控）"""
        print("\n" + "="*80)
        print("【步骤3/7】数据质量校验")
        print("="*80)

        # 检查依赖
        if not self.health_monitor.record_step_start("validation"):
            blocked_result = self.health_monitor.step_results.get("validation")
            print(f"⛔ 步骤被阻塞: {blocked_result.message if blocked_result else '未知原因'}")
            return None

        try:
            report = self.analyst.validate_data()

            # 转换为字典
            self.validation_report_dict = report.to_dict()

            # 保存校验结果
            self._save_json("step3_validation_report.json", self.validation_report_dict)

            # 生成清洗报告
            cleaning_report = report.generate_cleaning_report()
            cleaning_file = self.session_dir / "step3_cleaning_report.txt"
            cleaning_file.write_text(cleaning_report, encoding='utf-8')

            # 显示关键信息
            print(f"\n📊 质量评分: {report.overall_score:.1f}/100")

            if report.issues:
                critical_count = sum(1 for i in report.issues if str(i.severity) == 'IssueSeverity.CRITICAL')
                warning_count = sum(1 for i in report.issues if str(i.severity) == 'IssueSeverity.WARNING')

                print(f"📋 发现问题: {len(report.issues)} 个")
                print(f"   - Critical: {critical_count} 个")
                print(f"   - Warning: {warning_count} 个")

                # 如果有严重问题，给出警告
                if critical_count > 0:
                    print("\n" + "⚠️" * 20)
                    print("⚠️  发现严重数据质量问题！")
                    print("⚠️  建议在继续分析前处理这些问题")
                    print("⚠️  查看 step3_cleaning_report.txt 了解详情")
                    print("⚠️" * 20)
            else:
                print("✅ 未发现数据质量问题")

            summary = report.get_cleaning_summary()
            if summary.get('recommended_deletions', 0) > 0:
                print(f"🗑️  建议删除: {summary['recommended_deletions']:,} 行")
            if summary.get('recommended_fills', 0) > 0:
                print(f"📝 建议填充: {summary['recommended_fills']:,} 个缺失值")

            # 记录成功
            self.health_monitor.record_step_success(
                "validation",
                message=f"质量评分 {report.overall_score:.1f}/100",
                details={
                    "score": report.overall_score,
                    "issues_count": len(report.issues)
                }
            )

            return self.validation_report_dict

        except Exception as e:
            error_msg = f"数据校验失败: {str(e)}"
            print(f"❌ {error_msg}")
            self.health_monitor.record_step_failure(
                "validation",
                error=error_msg,
                suggestions=[
                    "检查数据是否正确加载",
                    "确认 data_validator 模块正常工作"
                ]
            )
            return None

    def step4_plan_analysis(self, user_intent: str) -> Tuple[bool, str, str]:
        """步骤4: 规划分析方案（带健康监控）"""
        print("\n" + "="*80)
        print("【步骤4/7】分析方案规划")
        print("="*80)
        print(f"📝 用户诉求: {user_intent}")

        # 检查依赖
        if not self.health_monitor.record_step_start("planning"):
            blocked_result = self.health_monitor.step_results.get("planning")
            msg = f"⛔ 步骤被阻塞: {blocked_result.message if blocked_result else '未知原因'}"
            print(msg)
            return False, "", ""

        try:
            # 需要先有本体结果，如果没有，使用占位
            if self.ontology_result is None:
                print("⚠️ 警告: 尚未进行本体识别，使用数据画像替代")
                data_profile = self.analyst._generate_data_profile(self.analyst.data)
                ontology = self._create_placeholder_ontology(data_profile)
            else:
                ontology = self.ontology_result

            # 获取数据样本和字段详情
            df = self.analyst.data
            data_sample = df.head(10).to_string()

            column_details = []
            for col in df.columns:
                dtype = df[col].dtype
                unique = df[col].nunique()
                null_pct = df[col].isnull().sum() / len(df) * 100
                detail = f"{col}: {dtype}, 唯一值{unique:,}, 缺失{null_pct:.1f}%"
                if hasattr(df[col], 'min') and pd.api.types.is_numeric_dtype(df[col]):
                    detail += f", 范围[{df[col].min():.2f}, {df[col].max():.2f}]"
                column_details.append(detail)

            # 生成提示词
            prompt = self.llm_analyzer.plan_analysis(
                ontology=ontology,
                user_intent=user_intent,
                data_sample=data_sample,
                column_details=column_details
            )

            # 保存提示词
            prompt_file = self.session_dir / "step4_planning_prompt.txt"
            prompt_file.write_text(prompt, encoding='utf-8')

            print("💾 分析方案提示词已生成")

            # 记录成功
            self.health_monitor.record_step_success(
                "planning",
                message="提示词已生成，需要调用LLM完成方案规划",
                details={"prompt_file": str(prompt_file)}
            )

            # 显示提醒
            print("\n⚠️ 分析方案规划需要调用大模型完成！")
            print(f"⚠️ 提示词已保存到: {prompt_file}")
            print("⚠️ 请将结果保存为: analysis_plan.json")

            return True, str(prompt), str(prompt_file)

        except Exception as e:
            error_msg = f"方案规划失败: {str(e)}"
            print(f"❌ {error_msg}")
            self.health_monitor.record_step_failure(
                "planning",
                error=error_msg,
                suggestions=[
                    "检查数据是否正确加载",
                    "确认 llm_analyzer 模块正常工作"
                ]
            )
            return False, "", ""

    def step5_generate_script(self) -> Tuple[bool, str, str]:
        """步骤5: 生成分析脚本（带健康监控）"""
        print("\n" + "="*80)
        print("【步骤5/7】生成分析脚本")
        print("="*80)

        # 检查依赖
        if not self.health_monitor.record_step_start("script_generation"):
            blocked_result = self.health_monitor.step_results.get("script_generation")
            msg = f"⛔ 步骤被阻塞: {blocked_result.message if blocked_result else '未知原因'}"
            print(msg)
            return False, "", ""

        try:
            # 需要有分析计划
            if self.analysis_plan is None:
                error_msg = "尚未进行分析方案规划，无法生成脚本"
                print(f"❌ {error_msg}")
                self.health_monitor.record_step_failure(
                    "script_generation",
                    error=error_msg,
                    suggestions=[
                        "先完成步骤4（分析方案规划）",
                        "将LLM的规划结果保存为 analysis_plan.json"
                    ]
                )
                return False, "", ""

            # 使用已识别的本体（或占位）
            ontology = self.ontology_result or self._create_placeholder_ontology(
                self.analyst._generate_data_profile(self.analyst.data)
            )

            file_path = self.analyst.load_result.file_path if self.analyst.load_result else "data.csv"

            # 生成提示词
            prompt = self.llm_analyzer.generate_script(
                analysis_plan=self.analysis_plan,
                ontology=ontology,
                file_path=file_path
            )

            # 保存提示词
            prompt_file = self.session_dir / "step5_script_prompt.txt"
            prompt_file.write_text(prompt, encoding='utf-8')

            print("💾 脚本生成提示词已保存")

            # 记录成功
            self.health_monitor.record_step_success(
                "script_generation",
                message="提示词已生成，需要调用LLM生成脚本",
                details={"prompt_file": str(prompt_file)}
            )

            print("\n⚠️ 脚本生成需要调用大模型完成！")
            print(f"⚠️ 提示词已保存到: {prompt_file}")
            print("⚠️ 请将生成的脚本保存为: analysis_script.py")

            return True, str(prompt), str(prompt_file)

        except Exception as e:
            error_msg = f"脚本生成失败: {str(e)}"
            print(f"❌ {error_msg}")
            self.health_monitor.record_step_failure(
                "script_generation",
                error=error_msg,
                suggestions=[
                    "检查分析方案规划是否完成",
                    "确认 llm_analyzer 模块正常工作"
                ]
            )
            return False, "", ""

    def step6_execute_analysis(self, script_path: Optional[str] = None) -> Dict[str, Any]:
        """步骤6: 执行分析脚本（带健康监控）"""
        print("\n" + "="*80)
        print("【步骤6/7】执行分析")
        print("="*80)

        # 检查依赖
        if not self.health_monitor.record_step_start("execution"):
            blocked_result = self.health_monitor.step_results.get("execution")
            print(f"⛔ 步骤被阻塞: {blocked_result.message if blocked_result else '未知原因'}")
            return {"status": "被阻塞", "executed": False}

        results = {
            "status": "未执行",
            "executed": False,
            "script_output": ""
        }

        if script_path and os.path.exists(script_path):
            print(f"🚀 执行分析脚本: {script_path}")
            try:
                result = subprocess.run(
                    [sys.executable, script_path],
                    capture_output=True,
                    text=True,
                    cwd=str(self.session_dir)
                )
                print(result.stdout)
                if result.stderr:
                    print("⚠️ 警告:", result.stderr)

                results["status"] = "执行成功"
                results["executed"] = True
                results["script_output"] = result.stdout

                # 记录成功
                self.health_monitor.record_step_success(
                    "execution",
                    message="分析脚本执行完成"
                )

            except Exception as e:
                error_msg = f"执行失败: {e}"
                print(f"❌ {error_msg}")
                results["status"] = f"执行失败: {e}"
                self.health_monitor.record_step_failure(
                    "execution",
                    error=str(e),
                    suggestions=[
                        "检查脚本是否存在语法错误",
                        "确认脚本所需的依赖包已安装",
                        "检查数据文件路径是否正确"
                    ]
                )
        else:
            msg = "未提供脚本路径或脚本不存在，跳过执行"
            print(f"ℹ️ {msg}")
            results["status"] = "未提供脚本"
            self.health_monitor.record_step_failure(
                "execution",
                error=msg,
                suggestions=[
                    "完成步骤5（脚本生成）",
                    "将LLM生成的脚本保存为 analysis_script.py",
                    f"或将脚本路径传入 step6_execute_analysis(script_path='...')"
                ]
            )

        # 尝试读取分析结果
        results_file = self.session_dir / "analysis_results.json"
        if results_file.exists():
            try:
                with open(results_file, 'r', encoding='utf-8') as f:
                    analysis_data = json.load(f)
                    results["data"] = analysis_data
                    print(f"📊 分析结果已读取: {results_file}")
            except Exception as e:
                print(f"⚠️ 读取分析结果失败: {e}")

        return results

    def step7_generate_comprehensive_report(self, **kwargs) -> Dict[str, str]:
        """步骤7: 生成综合报告（带健康监控）"""
        print("\n" + "="*80)
        print("【步骤7/7】生成综合报告")
        print("="*80)

        # 检查依赖
        if not self.health_monitor.record_step_start("report"):
            blocked_result = self.health_monitor.step_results.get("report")
            print(f"⛔ 步骤被阻塞: {blocked_result.message if blocked_result else '未知原因'}")
            return {}

        try:
            # 准备数据（使用占位数据如果实际数据不存在）
            data_info = self.data_info or {
                "file_name": "Unknown",
                "rows": 0,
                "columns": 0,
                "report_title": "数据分析报告"
            }

            validation_report = self.validation_report_dict or {
                "overall_score": 0,
                "issues": [],
                "cleaning_summary": {}
            }

            # 生成报告
            report_paths = self.report_generator.generate_all_reports(
                data_info=data_info,
                validation_report=validation_report,
                ontology=kwargs.get('ontology_result', {}),
                analysis_plan=kwargs.get('analysis_plan_result', {}),
                analysis_results=kwargs.get('analysis_results', {}),
                chart_files=[]
            )

            print("\n📄 报告已生成:")
            print(f"  📘 HTML报告: {report_paths['html_report']}")
            print(f"  📄 Markdown报告: {report_paths['markdown_report']}")

            # 记录成功
            self.health_monitor.record_step_success(
                "report",
                message="综合报告已生成",
                details=report_paths
            )

            return report_paths

        except Exception as e:
            error_msg = f"报告生成失败: {str(e)}"
            print(f"❌ {error_msg}")
            self.health_monitor.record_step_failure(
                "report",
                error=error_msg,
                suggestions=[
                    "检查报告生成器是否正常工作",
                    "确认输出目录有写入权限"
                ]
            )
            return {}

    def run_full_analysis(self, file_path: str, user_intent: str) -> Dict[str, Any]:
        """运行完整分析流程（带健康监控）"""
        print("\n" + "="*80)
        print("🚀 启动通用数据分析流程（增强版）")
        print(f"📁 数据文件: {file_path}")
        print(f"🎯 分析目标: {user_intent}")
        print("="*80)

        # 检查流程是否可以开始
        if not self.health_monitor.can_proceed("load"):
            print("\n❌ 流程无法开始，检查失败")
            return {"error": "流程初始化失败"}

        # 步骤1: 加载数据
        success, msg = self.step1_load_data(file_path)
        if not success:
            self._finalize_flow()
            return {"error": msg, "session_dir": str(self.session_dir)}

        # 步骤2: 本体识别
        success, _, _ = self.step2_identify_ontology()
        # 本体识别失败不终止流程，继续执行

        # 步骤3: 数据校验
        validation_report = self.step3_validate_data()

        # 步骤4: 方案规划
        success, _, _ = self.step4_plan_analysis(user_intent)

        # 步骤5: 脚本生成
        success, _, _ = self.step5_generate_script()

        # 步骤6: 执行分析
        analysis_results = self.step6_execute_analysis()

        # 步骤7: 生成报告
        report_paths = self.step7_generate_comprehensive_report()

        # 最终化流程
        return self._finalize_flow()

    def _finalize_flow(self) -> Dict[str, Any]:
        """结束流程，生成最终报告"""
        # 打印流程状态
        self.health_monitor.print_flow_status(full_report=True)

        # 保存健康报告
        health_report = self.health_monitor.get_final_report()
        self._save_json("FLOW_HEALTH_REPORT.json", health_report)

        # 生成最终摘要
        summary = {
            "session_dir": str(self.session_dir),
            "flow_completed": not self.health_monitor.flow_interrupted,
            "health_score": self.health_monitor.health_score,
            "health_report_file": str(self.session_dir / "FLOW_HEALTH_REPORT.json")
        }

        print("\n" + "="*80)
        if self.health_monitor.flow_interrupted:
            print("🔴 流程执行失败，请查看上述错误信息并修复问题")
        elif self.health_monitor.health_score == 100:
            print("✅ 流程执行成功！所有步骤已完成")
        else:
            print("🟡 流程部分完成，部分步骤存在问题")
        print("="*80)
        print(f"\n📂 所有文件保存在: {self.session_dir}")
        print(f"📊 流程健康报告: {summary['health_report_file']}")

        return summary

    def _save_json(self, filename: str, data: Dict):
        """保存JSON文件"""
        filepath = self.session_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    def _create_placeholder_ontology(self, data_profile: Dict) -> OntologyResult:
        """创建占位本体结果"""
        return OntologyResult(
            entity_type="待识别",
            entity_type_reason="尚未调用大模型进行本体识别",
            generation_mechanism="待识别",
            mechanism_reason="尚未调用大模型进行本体识别",
            core_dimensions=[],
            is_economic=False,
            economic_type=None,
            domain_type="待识别",
            keywords=["待识别"],
            recommended_questions=["待识别"],
            limitations=["尚未进行本体识别"],
            confidence="低"
        )


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Universal Data Analyst V2 - 增强版流程编排器（带健康监控）'
    )
    parser.add_argument('file', help='数据文件路径')
    parser.add_argument(
        '--intent', '-i',
        default='探索性数据分析，了解数据特征和潜在模式',
        help='用户分析诉求'
    )
    parser.add_argument(
        '--output', '-o',
        default='./analysis_output',
        help='输出目录'
    )

    args = parser.parse_args()

    # 运行完整分析
    orchestrator = DataAnalysisOrchestratorV2(output_dir=args.output)
    results = orchestrator.run_full_analysis(
        file_path=args.file,
        user_intent=args.intent
    )

    # 根据健康分数决定退出码
    if results.get('flow_completed'):
        print("\n✅ 分析流程成功完成")
        sys.exit(0)
    else:
        print("\n❌ 分析流程执行失败")
        sys.exit(1)


if __name__ == '__main__':
    import pandas as pd
    main()

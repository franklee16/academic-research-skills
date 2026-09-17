"""
数据验证器

验证数据质量，检测常见问题：
- 缺失值
- 异常值
- 重复记录
- 数据类型不一致
- 业务规则违反
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IssueSeverity(Enum):
    """问题严重程度"""
    CRITICAL = "critical"    # 必须修复
    WARNING = "warning"      # 建议修复
    INFO = "info"            # 仅供参考


class CleaningActionType(Enum):
    """清洗操作类型"""
    DELETE_ROWS = "delete_rows"       # 删除行
    DELETE_COLUMN = "delete_column"   # 删除列
    FILL_NA = "fill_na"               # 填充缺失值
    CLIP = "clip"                     # 截断异常值
    CONVERT_TYPE = "convert_type"     # 类型转换
    KEEP = "keep"                     # 保留但标记
    REVIEW = "review"                 # 人工审核


@dataclass
class CleaningAction:
    """清洗操作建议"""
    action_type: CleaningActionType
    target: str                       # 操作目标（列名或整表）
    affected_rows: int               # 影响行数
    description: str                 # 操作描述
    reason: str                      # 操作原因
    recommended: bool = True         # 是否建议执行


@dataclass
class ValidationIssue:
    """验证问题"""
    severity: IssueSeverity
    category: str                    # missing/duplicate/outlier/type/business
    column: Optional[str]           # 相关列
    description: str
    affected_rows: int
    affected_percent: float
    suggestion: str
    cleaning_action: Optional[CleaningAction] = None  # 建议的清洗操作


@dataclass
class ValidationReport:
    """验证报告"""
    total_rows: int
    total_columns: int
    overall_score: float   # 0-100
    issues: List[ValidationIssue] = field(default_factory=list)
    passed_checks: List[str] = field(default_factory=list)

    def has_critical_issues(self) -> bool:
        return any(i.severity == IssueSeverity.CRITICAL for i in self.issues)

    def get_issues_by_severity(self, severity: IssueSeverity) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == severity]

    def get_cleaning_summary(self) -> Dict[str, Any]:
        """获取清洗操作汇总"""
        summary = {
            'total_issues': len(self.issues),
            'recommended_deletions': 0,
            'recommended_fills': 0,
            'recommended_conversions': 0,
            'recommended_reviews': 0,
            'columns_to_delete': [],
            'rows_to_delete_estimate': 0,
            'actions_by_type': {}
        }

        for issue in self.issues:
            if issue.cleaning_action:
                action = issue.cleaning_action
                action_type = action.action_type.value

                # 统计各类操作
                if action_type not in summary['actions_by_type']:
                    summary['actions_by_type'][action_type] = []
                summary['actions_by_type'][action_type].append({
                    'target': action.target,
                    'rows': action.affected_rows,
                    'description': action.description
                })

                # 统计建议删除的行数
                if action.action_type == CleaningActionType.DELETE_ROWS:
                    summary['recommended_deletions'] += action.affected_rows
                    summary['rows_to_delete_estimate'] += action.affected_rows
                elif action.action_type == CleaningActionType.DELETE_COLUMN:
                    summary['columns_to_delete'].append(action.target)
                elif action.action_type == CleaningActionType.FILL_NA:
                    summary['recommended_fills'] += action.affected_rows
                elif action.action_type == CleaningActionType.CONVERT_TYPE:
                    summary['recommended_conversions'] += action.affected_rows
                elif action.action_type == CleaningActionType.REVIEW:
                    summary['recommended_reviews'] += action.affected_rows

        return summary

    def generate_cleaning_report(self) -> str:
        """生成清洗报告文本"""
        summary = self.get_cleaning_summary()
        lines = ["\n=== 数据清洗建议报告 ===\n"]

        # 总体统计
        lines.append(f"原始数据: {self.total_rows:,} 行 × {self.total_columns} 列")
        lines.append(f"发现问题: {summary['total_issues']} 个")
        lines.append("")

        # 建议删除的行
        if summary['recommended_deletions'] > 0:
            lines.append(f"【建议删除行】共 {summary['recommended_deletions']:,} 行")
            if 'delete_rows' in summary['actions_by_type']:
                for action in summary['actions_by_type']['delete_rows']:
                    lines.append(f"  - {action['target']}: {action['rows']:,} 行 - {action['description']}")
            lines.append("")
        else:
            lines.append("【建议删除行】无")
            lines.append("  策略: 保留所有行，不直接删除数据")
            lines.append("")

        # 建议删除的列
        if summary['columns_to_delete']:
            lines.append(f"【建议删除列】共 {len(summary['columns_to_delete'])} 列")
            for col in summary['columns_to_delete']:
                lines.append(f"  - {col}")
            lines.append("")

        # 缺失值字段分析说明（核心修改）
        missing_issues = [i for i in self.issues if i.category == 'missing' and i.affected_rows > 0]
        if missing_issues:
            lines.append("【缺失值字段处理说明】")
            lines.append(f"  共有 {len(missing_issues)} 个字段存在缺失值，保留所有原始行，分析时按需处理：")
            lines.append("")
            for issue in missing_issues:
                col = issue.column
                missing_count = issue.affected_rows
                missing_pct = issue.affected_percent
                valid_rows = self.total_rows - missing_count
                lines.append(f"  ▶ 字段 '{col}':")
                lines.append(f"    - 缺失值: {missing_count:,} 个 ({missing_pct:.2f}%)")
                lines.append(f"    - 有效数据: {valid_rows:,} 行")
                lines.append(f"    - 处理方式: 分析该字段时，使用 {valid_rows:,} 条有效数据，备注说明数据来源")
                if issue.cleaning_action:
                    lines.append(f"    - 建议: {issue.cleaning_action.description}")
                lines.append("")

        # 建议类型转换
        if summary['recommended_conversions'] > 0:
            lines.append(f"【建议类型转换】")
            if 'convert_type' in summary['actions_by_type']:
                for action in summary['actions_by_type']['convert_type']:
                    lines.append(f"  - {action['target']}: {action['description']}")
            lines.append("")

        # 建议人工审核
        if summary['recommended_reviews'] > 0:
            lines.append(f"【建议人工审核】共 {summary['recommended_reviews']:,} 行")
            if 'review' in summary['actions_by_type']:
                for action in summary['actions_by_type']['review']:
                    lines.append(f"  - {action['target']}: {action['rows']:,} 行 - {action['description']}")
            lines.append("")

        # 异常但保留
        if 'keep' in summary['actions_by_type']:
            keep_actions = summary['actions_by_type']['keep']
            # 筛选出非缺失值的保留项
            outlier_keep = [a for a in keep_actions if '缺失' not in a['description']]
            if outlier_keep:
                lines.append("【异常值但保留】")
                for action in outlier_keep:
                    lines.append(f"  - {action['target']}: {action['description']}")
                lines.append("")

        # 预计结果
        remaining_rows = self.total_rows - summary['rows_to_delete_estimate']
        lines.append(f"【预计清洗结果】")
        lines.append(f"  - 原始数据: {self.total_rows:,} 行")
        lines.append(f"  - 删除行数: {summary['rows_to_delete_estimate']:,}")
        lines.append(f"  - 保留行数: {remaining_rows:,} (100%)")
        lines.append(f"  - 说明: 保留所有原始数据，各字段分析时根据有效数据量独立处理")

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_rows': self.total_rows,
            'total_columns': self.total_columns,
            'overall_score': round(self.overall_score, 1),
            'issue_count': len(self.issues),
            'critical_count': len(self.get_issues_by_severity(IssueSeverity.CRITICAL)),
            'warning_count': len(self.get_issues_by_severity(IssueSeverity.WARNING)),
            'passed_checks': self.passed_checks,
            'cleaning_summary': self.get_cleaning_summary(),
        }


class DataValidator:
    """
    数据验证器

    自动检测数据质量问题
    """

    tool_name = "data_validator"
    tool_description = "验证数据质量，检测缺失值、异常值、重复等问题"

    # 阈值配置（可从配置文件读取）
    DEFAULT_THRESHOLDS = {
        'missing_critical': 0.5,    # 缺失率超过50%为严重问题
        'missing_warning': 0.1,     # 缺失率超过10%为警告
        'duplicate_critical': 0.1,  # 重复率超过10%为严重问题
        'duplicate_warning': 0.01,  # 重复率超过1%为警告
        'outlier_zscore': 3,        # Z-score超过3为异常
        'outlier_iqr': 1.5,         # IQR倍数
        'cardinality_ratio': 0.9,   # 高基数比例（唯一值/总行数）
    }

    def __init__(self, thresholds: Optional[Dict] = None):
        self.thresholds = thresholds or self.DEFAULT_THRESHOLDS

    def execute(self, data: pd.DataFrame,
                params: Optional[Dict] = None) -> ValidationReport:
        """
        执行数据验证

        Args:
            params: {
                'business_rules': [...],  # 业务规则
                'custom_thresholds': {...},  # 自定义阈值
            }
        """
        issues = []
        passed = []

        params = params or {}
        custom_rules = params.get('business_rules', [])
        custom_thresholds = params.get('custom_thresholds', {})
        thresholds = {**self.thresholds, **custom_thresholds}

        # 1. 检查缺失值
        missing_issues = self._check_missing_values(data, thresholds)
        issues.extend(missing_issues)
        if not missing_issues:
            passed.append("缺失值检查")

        # 2. 检查重复值
        duplicate_issues = self._check_duplicates(data, thresholds)
        issues.extend(duplicate_issues)
        if not duplicate_issues:
            passed.append("重复值检查")

        # 3. 检查异常值
        outlier_issues = self._check_outliers(data, thresholds)
        issues.extend(outlier_issues)
        if not outlier_issues:
            passed.append("异常值检查")

        # 4. 检查数据类型
        type_issues = self._check_data_types(data)
        issues.extend(type_issues)
        if not type_issues:
            passed.append("数据类型检查")

        # 5. 检查业务规则
        if custom_rules:
            rule_issues = self._check_business_rules(data, custom_rules)
            issues.extend(rule_issues)

        # 计算总分
        score = self._calculate_score(data, issues)

        report = ValidationReport(
            total_rows=len(data),
            total_columns=len(data.columns),
            overall_score=score,
            issues=issues,
            passed_checks=passed
        )

        # 生成并打印清洗报告
        cleaning_report = report.generate_cleaning_report()
        logger.info(cleaning_report)

        logger.info(f"数据验证完成: 得分 {score:.1f}/100, "
                   f"发现 {len(issues)} 个问题")

        return report

    def interpret_results(self, results: Dict[str, Any]) -> str:
        """解释验证结果"""
        report = ValidationReport(**results)

        if report.overall_score >= 90:
            return f"数据质量优秀 ({report.overall_score:.0f}/100)，可直接用于分析"
        elif report.overall_score >= 70:
            return f"数据质量良好 ({report.overall_score:.0f}/100)，建议处理警告项"
        elif report.overall_score >= 50:
            return f"数据质量一般 ({report.overall_score:.0f}/100)，需要清洗"
        else:
            return f"数据质量较差 ({report.overall_score:.0f}/100)，建议先修复严重问题"

    def _check_missing_values(self, data: pd.DataFrame,
                              thresholds: Dict) -> List[ValidationIssue]:
        """检查缺失值"""
        issues = []
        total_rows = len(data)

        for col in data.columns:
            missing_count = data[col].isnull().sum()
            missing_pct = missing_count / total_rows

            if missing_pct > thresholds['missing_critical']:
                # 严重缺失：建议删除列（但不删除行）
                cleaning_action = CleaningAction(
                    action_type=CleaningActionType.DELETE_COLUMN,
                    target=col,
                    affected_rows=0,  # 不删除行
                    description=f"删除列 '{col}'（缺失率 {missing_pct:.1%} 过高）",
                    reason=f"缺失率 {missing_pct:.1%} 超过临界阈值 {thresholds['missing_critical']:.1%}，建议删除该列而非删除行"
                )
                issues.append(ValidationIssue(
                    severity=IssueSeverity.CRITICAL,
                    category='missing',
                    column=col,
                    description=f"列 '{col}' 缺失率 {missing_pct:.1%}，共 {missing_count:,} 个缺失值",
                    affected_rows=missing_count,
                    affected_percent=missing_pct * 100,
                    suggestion=f"该列缺失严重，建议删除此列；如需分析该字段，可临时删除 {missing_count:,} 个缺失行进行分析",
                    cleaning_action=cleaning_action
                ))
            elif missing_pct > thresholds['missing_warning']:
                # 警告级别缺失：保留所有行，分析时按需处理
                cleaning_action = CleaningAction(
                    action_type=CleaningActionType.KEEP,
                    target=col,
                    affected_rows=0,  # 不删除行
                    description=f"保留所有行，列 '{col}' 的 {missing_count:,} 个缺失值在分析该字段时再处理",
                    reason=f"缺失率 {missing_pct:.1%}，建议保留全部数据；分析 '{col}' 字段时需删除 {missing_count:,} 个缺失行"
                )
                issues.append(ValidationIssue(
                    severity=IssueSeverity.WARNING,
                    category='missing',
                    column=col,
                    description=f"列 '{col}' 缺失率 {missing_pct:.1%}，共 {missing_count:,} 个缺失值",
                    affected_rows=missing_count,
                    affected_percent=missing_pct * 100,
                    suggestion=f"保留所有行；如需分析 '{col}' 字段，临时删除该列缺失的 {missing_count:,} 行并备注说明",
                    cleaning_action=cleaning_action
                ))

        return issues

    def _check_duplicates(self, data: pd.DataFrame,
                         thresholds: Dict) -> List[ValidationIssue]:
        """检查重复值"""
        issues = []
        total_rows = len(data)

        # 完全重复
        dup_count = data.duplicated().sum()
        dup_pct = dup_count / total_rows

        if dup_pct > thresholds['duplicate_critical']:
            cleaning_action = CleaningAction(
                action_type=CleaningActionType.DELETE_ROWS,
                target="整表",
                affected_rows=dup_count,
                description=f"删除 {dup_count:,} 行完全重复的记录",
                reason=f"重复率 {dup_pct:.1%} 超过临界阈值，必须删除"
            )
            issues.append(ValidationIssue(
                severity=IssueSeverity.CRITICAL,
                category='duplicate',
                column=None,
                description=f"发现 {dup_count} 行完全重复记录 ({dup_pct:.1%})",
                affected_rows=dup_count,
                affected_percent=dup_pct * 100,
                suggestion="删除重复记录，检查数据采集流程",
                cleaning_action=cleaning_action
            ))
        elif dup_pct > thresholds['duplicate_warning']:
            cleaning_action = CleaningAction(
                action_type=CleaningActionType.DELETE_ROWS,
                target="整表",
                affected_rows=dup_count,
                description=f"删除 {dup_count:,} 行完全重复的记录",
                reason=f"重复率 {dup_pct:.1%} 超过警告阈值，建议删除"
            )
            issues.append(ValidationIssue(
                severity=IssueSeverity.WARNING,
                category='duplicate',
                column=None,
                description=f"发现 {dup_count} 行完全重复记录 ({dup_pct:.1%})",
                affected_rows=dup_count,
                affected_percent=dup_pct * 100,
                suggestion="检查并删除重复记录",
                cleaning_action=cleaning_action
            ))

        return issues

    def _check_outliers(self, data: pd.DataFrame,
                       thresholds: Dict) -> List[ValidationIssue]:
        """检查异常值"""
        issues = []

        # 排除 boolean 列（bool 是 np.number 的子类，但无法做减法运算）
        numeric_cols = data.select_dtypes(include=[np.number], exclude=['bool']).columns

        for col in numeric_cols:
            series = data[col].dropna()
            if len(series) < 10:
                continue

            # IQR 方法
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - thresholds['outlier_iqr'] * IQR
            upper_bound = Q3 + thresholds['outlier_iqr'] * IQR

            outliers = series[(series < lower_bound) | (series > upper_bound)]
            outlier_pct = len(outliers) / len(series)

            if outlier_pct > 0.05:  # 超过5%的异常值
                # 根据异常值比例决定清洗策略
                if outlier_pct > 0.2:  # 超过20%建议保留但截断
                    cleaning_action = CleaningAction(
                        action_type=CleaningActionType.CLIP,
                        target=col,
                        affected_rows=len(outliers),
                        description=f"对列 '{col}' 的异常值进行截断处理（下限:{lower_bound:.2f}, 上限:{upper_bound:.2f}）",
                        reason=f"异常值比例 {outlier_pct:.1%} 较高，建议截断而非删除"
                    )
                elif outlier_pct > 0.1:  # 10%-20%建议人工审核
                    cleaning_action = CleaningAction(
                        action_type=CleaningActionType.REVIEW,
                        target=col,
                        affected_rows=len(outliers),
                        description=f"人工审核列 '{col}' 的 {len(outliers):,} 个异常值",
                        reason=f"异常值比例 {outlier_pct:.1%}，建议人工判断是否删除"
                    )
                else:  # 低于10%建议删除行
                    cleaning_action = CleaningAction(
                        action_type=CleaningActionType.DELETE_ROWS,
                        target=col,
                        affected_rows=len(outliers),
                        description=f"删除列 '{col}' 中 {len(outliers):,} 个异常值所在行",
                        reason=f"异常值比例 {outlier_pct:.1%}，建议删除异常行"
                    )

                issues.append(ValidationIssue(
                    severity=IssueSeverity.WARNING,
                    category='outlier',
                    column=col,
                    description=f"列 '{col}' 发现 {len(outliers)} 个异常值 ({outlier_pct:.1%})",
                    affected_rows=len(outliers),
                    affected_percent=outlier_pct * 100,
                    suggestion="检查是否为数据错误，或使用稳健统计方法",
                    cleaning_action=cleaning_action
                ))

        return issues

    def _check_data_types(self, data: pd.DataFrame) -> List[ValidationIssue]:
        """检查数据类型问题"""
        issues = []

        # 检查可能是日期的字符串列
        for col in data.select_dtypes(include=['object']).columns:
            sample = data[col].dropna().head(100)
            if len(sample) == 0:
                continue

            # 简单判断是否为日期格式
            date_patterns = [
                r'^\d{4}-\d{2}-\d{2}',
                r'^\d{4}/\d{2}/\d{2}',
                r'^\d{2}/\d{2}/\d{4}',
            ]

            date_like_count = 0
            for val in sample:
                for pattern in date_patterns:
                    if re.match(pattern, str(val)):
                        date_like_count += 1
                        break

            if date_like_count / len(sample) > 0.8:
                cleaning_action = CleaningAction(
                    action_type=CleaningActionType.CONVERT_TYPE,
                    target=col,
                    affected_rows=data[col].notna().sum(),
                    description=f"将列 '{col}' 从字符串转换为 datetime 类型",
                    reason="该列内容符合日期格式特征，转换为日期类型便于时间序列分析"
                )
                issues.append(ValidationIssue(
                    severity=IssueSeverity.INFO,
                    category='type',
                    column=col,
                    description=f"列 '{col}' 看起来像是日期，但当前为字符串类型",
                    affected_rows=len(sample),
                    affected_percent=100.0,
                    suggestion="考虑转换为 datetime 类型以便时间序列分析",
                    cleaning_action=cleaning_action
                ))

        return issues

    def _check_business_rules(self, data: pd.DataFrame,
                             rules: List[Dict]) -> List[ValidationIssue]:
        """检查业务规则"""
        issues = []

        for rule in rules:
            name = rule.get('name', '未命名规则')
            condition = rule.get('condition')  # lambda或列名
            threshold = rule.get('threshold', 0)
            action = rule.get('action', 'review')  # delete/review/keep

            if callable(condition):
                violated = data.apply(condition, axis=1).sum()
            elif isinstance(condition, str) and condition in data.columns:
                violated = data[condition].sum() if data[condition].dtype == bool else 0
            else:
                continue

            violation_pct = violated / len(data)

            if violation_pct > threshold:
                # 根据规则配置决定清洗动作
                if action == 'delete':
                    cleaning_action = CleaningAction(
                        action_type=CleaningActionType.DELETE_ROWS,
                        target=name,
                        affected_rows=violated,
                        description=f"删除违反业务规则 '{name}' 的 {violated:,} 行",
                        reason=f"违反业务规则，建议删除"
                    )
                elif action == 'keep':
                    cleaning_action = CleaningAction(
                        action_type=CleaningActionType.KEEP,
                        target=name,
                        affected_rows=violated,
                        description=f"保留但标记违反业务规则 '{name}' 的 {violated:,} 行",
                        reason="业务规则违反但数据可保留分析"
                    )
                else:  # default review
                    cleaning_action = CleaningAction(
                        action_type=CleaningActionType.REVIEW,
                        target=name,
                        affected_rows=violated,
                        description=f"人工审核违反业务规则 '{name}' 的 {violated:,} 行",
                        reason="需要人工判断是否删除"
                    )

                issues.append(ValidationIssue(
                    severity=IssueSeverity.WARNING,
                    category='business',
                    column=None,
                    description=f"业务规则 '{name}' 违反 {violated} 次 ({violation_pct:.1%})",
                    affected_rows=violated,
                    affected_percent=violation_pct * 100,
                    suggestion=rule.get('suggestion', '检查业务规则'),
                    cleaning_action=cleaning_action
                ))

        return issues

    def _calculate_score(self, data: pd.DataFrame,
                        issues: List[ValidationIssue]) -> float:
        """计算数据质量得分"""
        score = 100.0

        for issue in issues:
            if issue.severity == IssueSeverity.CRITICAL:
                score -= 20 * (issue.affected_percent / 100)
            elif issue.severity == IssueSeverity.WARNING:
                score -= 10 * (issue.affected_percent / 100)
            elif issue.severity == IssueSeverity.INFO:
                score -= 2 * (issue.affected_percent / 100)

        return max(0, min(100, score))


# 全局实例
validator = DataValidator()

# 便捷函数
def validate(data: pd.DataFrame, **kwargs) -> ValidationReport:
    """便捷验证函数"""
    return validator.execute(data, kwargs)

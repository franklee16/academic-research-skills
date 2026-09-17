#!/usr/bin/env python3
"""
流程健康监控器 - Flow Health Monitor

用于监控 Universal Data Analyst Skill 的执行流程，
在步骤失败时给用户明确的报错和提示。
"""

import sys
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime


class StepStatus(Enum):
    """步骤状态"""
    PENDING = "待执行"
    RUNNING = "执行中"
    SUCCESS = "成功"
    FAILED = "失败"
    SKIPPED = "跳过"
    BLOCKED = "被阻塞"  # 前置步骤失败导致无法执行


class StepImportance(Enum):
    """步骤重要性"""
    CRITICAL = "关键"    # 失败则整个流程终止
    REQUIRED = "必需"    # 失败会阻塞后续步骤
    OPTIONAL = "可选"    # 失败不影响后续步骤


@dataclass
class StepResult:
    """步骤执行结果"""
    step_name: str
    step_number: int
    status: StepStatus
    importance: StepImportance
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    suggestions: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class FlowHealthMonitor:
    """
    流程健康监控器

    追踪每个步骤的执行状态，在失败时提供清晰的错误提示
    """

    # 步骤定义（名称、编号、重要性、前置步骤）
    STEPS_CONFIG = {
        "load": {
            "number": 1,
            "name": "数据加载",
            "importance": StepImportance.CRITICAL,
            "dependencies": [],
            "description": "从文件加载数据到内存"
        },
        "ontology": {
            "number": 2,
            "name": "数据本体识别",
            "importance": StepImportance.REQUIRED,
            "dependencies": ["load"],
            "description": "识别数据的实体类型和生成机制"
        },
        "validation": {
            "number": 3,
            "name": "数据质量校验",
            "importance": StepImportance.REQUIRED,
            "dependencies": ["load"],
            "description": "检查数据质量问题并生成报告"
        },
        "planning": {
            "number": 4,
            "name": "分析方案规划",
            "importance": StepImportance.REQUIRED,
            "dependencies": ["ontology", "validation"],
            "description": "根据用户诉求规划分析框架和步骤"
        },
        "script_generation": {
            "number": 5,
            "name": "脚本生成",
            "importance": StepImportance.REQUIRED,
            "dependencies": ["planning"],
            "description": "生成可执行的分析脚本"
        },
        "execution": {
            "number": 6,
            "name": "执行分析",
            "importance": StepImportance.REQUIRED,
            "dependencies": ["script_generation"],
            "description": "运行分析脚本生成结果"
        },
        "report": {
            "number": 7,
            "name": "报告生成",
            "importance": StepImportance.OPTIONAL,
            "dependencies": ["execution"],
            "description": "生成HTML和Markdown格式的综合报告"
        }
    }

    def __init__(self):
        self.step_results: Dict[str, StepResult] = {}
        self.flow_interrupted = False
        self.interrupt_reason = None
        self.health_score = 100  # 流程健康分数

    def record_step_start(self, step_id: str) -> bool:
        """
        记录步骤开始执行

        返回: 是否应该执行该步骤（检查前置依赖）
        """
        if step_id not in self.STEPS_CONFIG:
            return False

        config = self.STEPS_CONFIG[step_id]

        # 检查前置依赖
        for dep in config["dependencies"]:
            dep_result = self.step_results.get(dep)
            if not dep_result:
                # 前置步骤尚未执行
                self._record_blocked(step_id, f"前置步骤 '{dep}' 尚未执行")
                return False
            if dep_result.status == StepStatus.FAILED:
                # 前置步骤失败
                self._record_blocked(
                    step_id,
                    f"前置步骤 '{dep}' 执行失败",
                    suggestions=[
                        f"请检查步骤 '{dep}' 的错误信息并修复问题",
                        "修复后重新运行完整流程"
                    ]
                )
                return False
            if dep_result.status == StepStatus.BLOCKED:
                # 前置步骤被阻塞
                self._record_blocked(
                    step_id,
                    f"前置步骤 '{dep}' 被阻塞，可能是更前置的步骤失败",
                    suggestions=["从流程开始处检查错误并修复"]
                )
                return False

        # 可以执行
        self.step_results[step_id] = StepResult(
            step_name=config["name"],
            step_number=config["number"],
            status=StepStatus.RUNNING,
            importance=config["importance"]
        )
        return True

    def record_step_success(self, step_id: str, message: str = "", details: Dict = None):
        """记录步骤成功完成"""
        if step_id in self.step_results:
            self.step_results[step_id].status = StepStatus.SUCCESS
            self.step_results[step_id].message = message
            if details:
                self.step_results[step_id].details = details

    def record_step_failure(
        self,
        step_id: str,
        error: str,
        suggestions: List[str] = None,
        is_critical: bool = False
    ):
        """
        记录步骤失败

        Args:
            step_id: 步骤ID
            error: 错误信息
            suggestions: 修复建议列表
            is_critical: 是否为关键错误（会终止整个流程）
        """
        if step_id not in self.STEPS_CONFIG:
            return

        config = self.STEPS_CONFIG[step_id]

        self.step_results[step_id].status = StepStatus.FAILED
        self.step_results[step_id].error = error
        self.step_results[step_id].suggestions = suggestions or []

        # 更新健康分数
        if config["importance"] == StepImportance.CRITICAL:
            self.health_score -= 50
        elif config["importance"] == StepImportance.REQUIRED:
            self.health_score -= 30
        else:
            self.health_score -= 10

        # 关键步骤失败，标记流程中断
        if is_critical or config["importance"] == StepImportance.CRITICAL:
            self.flow_interrupted = True
            self.interrupt_reason = f"关键步骤 '{config['name']}' 失败: {error}"

    def _record_blocked(self, step_id: str, reason: str, suggestions: List[str] = None):
        """记录步骤被阻塞"""
        if step_id not in self.STEPS_CONFIG:
            return

        config = self.STEPS_CONFIG[step_id]

        self.step_results[step_id] = StepResult(
            step_name=config["name"],
            step_number=config["number"],
            status=StepStatus.BLOCKED,
            importance=config["importance"],
            message=reason,
            suggestions=suggestions or []
        )

        self.health_score -= 10

    def can_proceed(self, step_id: str) -> bool:
        """检查是否可以执行指定步骤"""
        if step_id not in self.STEPS_CONFIG:
            return False

        config = self.STEPS_CONFIG[step_id]

        # 检查前置依赖
        for dep in config["dependencies"]:
            dep_result = self.step_results.get(dep)
            if not dep_result or dep_result.status != StepStatus.SUCCESS:
                return False

        return not self.flow_interrupted

    def print_flow_status(self, full_report: bool = True):
        """打印流程状态报告"""
        print("\n" + "="*80)
        print("📊 流程健康监控报告")
        print("="*80)

        # 执行摘要
        total_steps = len(self.STEPS_CONFIG)
        success_steps = sum(1 for r in self.step_results.values() if r.status == StepStatus.SUCCESS)
        failed_steps = sum(1 for r in self.step_results.values() if r.status == StepStatus.FAILED)
        blocked_steps = sum(1 for r in self.step_results.values() if r.status == StepStatus.BLOCKED)

        print(f"\n执行摘要:")
        print(f"  总步骤: {total_steps}")
        print(f"  成功: {success_steps} ✅")
        print(f"  失败: {failed_steps} ❌")
        print(f"  被阻塞: {blocked_steps} ⛔")
        print(f"  健康分数: {max(0, self.health_score)}/100")

        if self.flow_interrupted:
            print(f"\n⚠️  流程已中断!")
            print(f"   原因: {self.interrupt_reason}")

        # 详细步骤状态
        if full_report:
            print(f"\n步骤详情:")
            for step_id, config in sorted(self.STEPS_CONFIG.items(), key=lambda x: x[1]["number"]):
                result = self.step_results.get(step_id)

                if not result:
                    icon = "⏳"
                    status_text = "待执行"
                    color = ""
                elif result.status == StepStatus.SUCCESS:
                    icon = "✅"
                    status_text = "成功"
                elif result.status == StepStatus.FAILED:
                    icon = "❌"
                    status_text = "失败"
                elif result.status == StepStatus.BLOCKED:
                    icon = "⛔"
                    status_text = "被阻塞"
                elif result.status == StepStatus.RUNNING:
                    icon = "🔄"
                    status_text = "执行中"
                else:
                    icon = "⏳"
                    status_text = "待执行"

                importance_icon = "🔴" if config["importance"] == StepImportance.CRITICAL else (
                    "🟡" if config["importance"] == StepImportance.REQUIRED else "⚪"
                )

                print(f"\n  {icon} 步骤{config['number']}: {config['name']}")
                print(f"     重要性: {importance_icon} {config['importance'].value}")
                print(f"     状态: {status_text}")

                if result:
                    if result.message:
                        print(f"     信息: {result.message}")
                    if result.error:
                        print(f"     错误: {result.error}")
                    if result.suggestions:
                        print(f"     建议:")
                        for i, suggestion in enumerate(result.suggestions, 1):
                            print(f"       {i}. {suggestion}")

        # 最终建议
        print("\n" + "="*80)
        if self.flow_interrupted:
            print("🔴 流程执行失败")
            print("="*80)
            print("\n问题汇总:")
            for step_id, result in self.step_results.items():
                if result.status == StepStatus.FAILED:
                    print(f"  - {result.step_name}: {result.error}")

            print("\n修复建议:")
            suggestions_shown = set()
            for step_id, result in self.step_results.items():
                if result.status == StepStatus.FAILED:
                    for suggestion in result.suggestions:
                        if suggestion not in suggestions_shown:
                            print(f"  • {suggestion}")
                            suggestions_shown.add(suggestion)

        elif success_steps == total_steps:
            print("✅ 流程执行成功")
            print("="*80)

        else:
            print("🟡 流程部分完成")
            print("="*80)
            print(f"已完成 {success_steps}/{total_steps} 个步骤")

        print()

    def get_final_report(self) -> Dict[str, Any]:
        """获取最终报告（用于保存到JSON）"""
        return {
            "health_score": max(0, self.health_score),
            "flow_completed": not self.flow_interrupted,
            "flow_interrupted": self.flow_interrupted,
            "interrupt_reason": self.interrupt_reason,
            "steps_summary": {
                step_id: {
                    "name": result.step_name,
                    "number": result.step_number,
                    "status": result.status.value,
                    "importance": result.importance.value,
                    "message": result.message,
                    "error": result.error,
                    "suggestions": result.suggestions
                }
                for step_id, result in self.step_results.items()
            }
        }


# 便捷函数
def create_monitor() -> FlowHealthMonitor:
    """创建流程监控器实例"""
    return FlowHealthMonitor()

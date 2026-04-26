#!/usr/bin/env python3
"""
战略分析报告质量门禁
在最终输出前进行专业性检查
"""

from typing import List, Tuple


class ReportQualityGate:
    """报告质量门禁 - 确保专业性"""

    # 核心分析框架（至少要有3个）
    REQUIRED_FRAMEWORKS = [
        "波特五力模型",
        "市场规模测算",
        "竞争格局分析",
        "PESTEL趋势分析",
        "价值链分析",
        "关键成功因素",
    ]

    # 必须包含的章节
    REQUIRED_SECTIONS = [
        "执行摘要",
        "数据溯源与可信度说明",
        "行业概览",
        "行业结构分析",
        "市场规模与增长",
        "竞争格局",
        "战略启示",
    ]

    # 禁用词（非专业表达）
    FORBIDDEN_WORDS = [
        "我觉得",
        "可能吧",
        "大概",
        "应该",
        "也许",
        "差不多",
        "说白了",
        "其实吧",
    ]

    # 专业术语列表
    PROFESSIONAL_TERMS = [
        "波特五力",
        "TAM",
        "SAM",
        "SOM",
        "PESTEL",
        "价值链",
        "战略群组",
        "关键成功因素",
        "CSF",
        "进入壁垒",
        "规模效应",
        "转换成本",
        "议价能力",
        "市场集中度",
        "CR4",
        "HHI",
    ]

    # 标准章节顺序（必须严格遵循）
    STANDARD_SECTION_ORDER = [
        "执行摘要",
        "数据溯源与可信度说明",
        "行业概览",
        "行业结构分析",
        "市场规模与增长",
        "竞争格局",
        "价值链分析",
        "关键趋势",
        "关键成功因素",
        "战略启示",
        "附录",
    ]

    # 标准表格格式检查
    STANDARD_TABLE_PATTERNS = [
        ("关键数据表", r"\| 指标 \| 数值 \| 来源 \| 可信度 \|"),
        ("五力评估表", r"\| 力量 \| 强度\(1-5\) \| 趋势 \| 关键因素 \|"),
        ("市场规模表", r"\| 层级 \| 规模 \| 测算方法 \| 关键假设 \|"),
        ("竞争格局表", r"\| 群组 \| 价格带 \| 代表企业 \| 核心策略 \|"),
        ("趋势影响表", r"\| 趋势 \| 紧迫性 \| 影响程度 \| 确定性 \| 优先级 \|"),
        ("数据溯源表", r"\| 数据项 \| 数值 \| 来源 \| 发布时间 \| 可信度 \| 提取方式 \|"),
    ]

    def __init__(self, report_content: str):
        self.content = report_content
        self.issues: List[Tuple[str, str]] = []  # (问题类型, 具体描述)

    def check_structure(self) -> bool:
        """检查报告结构完整性"""
        passed = True
        for section in self.REQUIRED_SECTIONS:
            if section not in self.content:
                self.issues.append(("结构缺失", f"缺少必要章节：{section}"))
                passed = False
        return passed

    def check_frameworks(self) -> Tuple[bool, int]:
        """检查核心框架应用数量"""
        count = 0
        found_frameworks = []

        for framework in self.REQUIRED_FRAMEWORKS:
            if framework.replace("模型", "").replace("分析", "").replace("测算", "") in self.content.replace("模型", "").replace("分析", "").replace("测算", ""):
                count += 1
                found_frameworks.append(framework)

        if count < 3:
            self.issues.append(
                ("框架不足", f"只应用了{count}个核心框架（至少需3个），已找到：{found_frameworks}")
            )
            return False, count

        return True, count

    def check_language(self) -> bool:
        """检查语言专业性"""
        passed = True
        found_words = []

        for word in self.FORBIDDEN_WORDS:
            if word in self.content:
                found_words.append(word)

        if found_words:
            self.issues.append(
                ("语言不专业", f"发现非专业表达：{found_words}，请改为基于数据/框架的客观陈述")
            )
            passed = False

        return passed

    def check_professional_terms(self) -> Tuple[bool, int]:
        """检查专业术语使用"""
        count = 0
        found_terms = []

        for term in self.PROFESSIONAL_TERMS:
            if term in self.content:
                count += 1
                found_terms.append(term)

        if count < 3:
            self.issues.append(
                ("术语不足", f"专业术语使用较少（{count}个），建议增加战略分析术语")
            )
            return False, count

        return True, count

    def check_section_order(self) -> bool:
        """检查章节顺序是否符合标准"""
        passed = True
        found_sections = []

        for section in self.STANDARD_SECTION_ORDER:
            if section in self.content:
                found_sections.append(section)

        # 检查章节顺序
        last_index = -1
        for section in found_sections:
            current_index = self.content.find(section)
            if current_index < last_index:
                self.issues.append(
                    ("章节顺序错误", f"章节'{section}'位置不符合标准顺序")
                )
                passed = False
            last_index = current_index

        # 检查关键章节是否缺失
        critical_sections = ["执行摘要", "行业结构分析", "市场规模与增长", "竞争格局"]
        for section in critical_sections:
            if section not in found_sections:
                self.issues.append(("关键章节缺失", f"缺少必要章节：{section}"))
                passed = False

        return passed

    def check_table_consistency(self) -> bool:
        """检查表格格式一致性"""
        passed = True

        # 检查是否有表格
        if "|" not in self.content:
            self.issues.append(("表格缺失", "报告中缺少数据表格"))
            return False

        # 检查关键数据表格式
        if "市场规模" in self.content and "TAM" in self.content:
            if "| 层级 | 规模 | 测算方法 | 关键假设 |" not in self.content:
                self.issues.append(
                    ("表格格式不规范", "市场规模表格式不符合标准（应为：层级|规模|测算方法|关键假设）")
                )
                passed = False

        return passed

    def check_rating_consistency(self) -> bool:
        """检查评级标准一致性"""
        passed = True

        # 检查是否使用星级和P1/P2/P3
        has_stars = "★" in self.content
        has_priority = "P1" in self.content or "P2" in self.content or "P3" in self.content

        if not has_stars:
            self.issues.append(("评级标准", "缺少可信度星级标注（★★★★★）"))
            passed = False

        if not has_priority:
            self.issues.append(("评级标准", "缺少优先级标注（P1/P2/P3）"))
            passed = False

        return passed

    def check_data_transparency(self) -> bool:
        """检查数据透明度"""
        passed = True

        # 检查是否有可信度星级
        if "★" not in self.content:
            self.issues.append(("数据透明度", "缺少数据可信度星级标注（★★★★★）"))
            passed = False

        # 检查是否有来源标注
        if "来源" not in self.content and "数据溯源" not in self.content:
            self.issues.append(("数据透明度", "缺少数据来源说明"))
            passed = False

        # 检查是否有推算说明
        if "估算" in self.content and "推算方法" not in self.content and "置信区间" not in self.content:
            self.issues.append(("数据透明度", "有估算数据但未说明推算方法和置信区间"))
            passed = False

        return passed

    def check_actionable(self) -> bool:
        """检查建议是否可执行"""
        passed = True

        if "建议行动" not in self.content and "战略建议" not in self.content:
            self.issues.append(("缺少建议", "报告缺少战略建议或行动清单章节"))
            passed = False

        # 检查是否有具体行动项
        if "[ ]" not in self.content and "- [ ]" not in self.content:
            self.issues.append(("建议不具体", "建议缺少具体的行动检查清单"))
            passed = False

        return passed

    def run_all_checks(self) -> Tuple[bool, List]:
        """运行所有检查"""
        checks = [
            ("结构完整性", self.check_structure()),
            ("章节顺序", self.check_section_order()),
            ("框架应用", self.check_frameworks()[0]),
            ("语言专业性", self.check_language()),
            ("术语使用", self.check_professional_terms()[0]),
            ("表格一致性", self.check_table_consistency()),
            ("评级标准一致性", self.check_rating_consistency()),
            ("数据透明度", self.check_data_transparency()),
            ("可执行性", self.check_actionable()),
        ]

        all_passed = all(passed for _, passed in checks)

        return all_passed, self.issues

    def generate_report(self) -> str:
        """生成质量检查报告"""
        all_passed, issues = self.run_all_checks()

        lines = ["## 报告质量门禁检查结果\n"]

        if all_passed:
            lines.append("✅ **所有检查通过，报告符合专业标准**\n")
        else:
            lines.append("⚠️ **发现以下问题，请修正后再提交：**\n")

        if issues:
            lines.append("\n### 待修正问题\n")
            for i, (issue_type, description) in enumerate(issues, 1):
                lines.append(f"{i}. **{issue_type}**：{description}")

        lines.append("\n### 检查项详情\n")

        # 框架统计
        _, framework_count = self.check_frameworks()
        lines.append(f"- 核心框架应用：{framework_count}/6 {'✅' if framework_count >= 3 else '⚠️'}")

        # 术语统计
        _, term_count = self.check_professional_terms()
        lines.append(f"- 专业术语使用：{term_count}+ {'✅' if term_count >= 3 else '⚠️'}")

        # 结构一致性统计
        section_ok = self.check_section_order()
        lines.append(f"- 章节顺序规范：{'✅ 符合标准' if section_ok else '⚠️ 存在问题'}")

        # 表格一致性
        table_ok = self.check_table_consistency()
        lines.append(f"- 表格格式规范：{'✅ 符合标准' if table_ok else '⚠️ 存在问题'}")

        # 评级一致性
        rating_ok = self.check_rating_consistency()
        lines.append(f"- 评级标准规范：{'✅ 符合标准' if rating_ok else '⚠️ 存在问题'}")

        lines.append("")
        return "\n".join(lines)


def quick_check(report_content: str) -> bool:
    """快速检查（便捷函数）"""
    gate = ReportQualityGate(report_content)
    passed, issues = gate.run_all_checks()

    if not passed:
        print(gate.generate_report())

    return passed



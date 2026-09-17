#!/usr/bin/env python3
"""
报告生成器 - 生成统一格式的综合分析报告

风格规范 (v2.0):
================
1. 公式格式:
   - 使用 <div class="process-flow"> 包裹
   - 公式整体单行展示
   - 变量说明在"其中:"后单独成行
   - 乘号使用 × (U+00D7)，不使用 ·
   - 下标使用 <sub> 标签，如 Diversity<sub>it</sub>
   - 公式示例:
     PlayDuration<sub>it</sub> = β₀ + β<sub>1</sub> × Diversity<sub>it</sub> + α<sub>i</sub> + ε<sub>it</sub>

2. p值显示:
   - 使用粗体数字: <strong>0.0001</strong>
   - 不使用"显著/不显著"等文字标签
   - p < 0.0001 时显示: <strong>&lt; 0.0001</strong>

3. 结论框:
   - 使用 <div class="conclusion-box">
   - 标题统一为"结论": <div class="conclusion-title">结论</div>
   - 不使用"✅ 显著"等前缀
   - 内容使用 <ul class="conclusion-list"> 列表

4. 表格:
   - 使用 <table class="financial-table">
   - 数字列使用 <td class="num">
   - 表头使用 <thead> 包裹

5. 层级结构:
   - 一级: <div class="section">
   - 二级: <div class="dimension-block">
   - 三级: <div class="insight-item">

输出:
- HTML报告（整合所有内容，内嵌图表）
- Markdown报告（文字部分）
- 图表目录（单独保存的图表）
"""

import os
import json
import base64
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import re


class ReportGenerator:
    """统一报告生成器"""

    def __init__(self, session_dir: str):
        self.session_dir = Path(session_dir)
        self.output_dir = self.session_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.charts_dir = self.output_dir / "charts"
        self.charts_dir.mkdir(exist_ok=True)

    def generate_all_reports(self,
                            data_info: Dict,
                            validation_report: Dict,
                            ontology: Dict,
                            analysis_plan: Dict,
                            analysis_results: Dict,
                            chart_files: List[str] = None) -> Dict[str, str]:
        """
        生成所有报告格式

        Returns:
            {
                'html_report': html文件路径,
                'markdown_report': md文件路径,
                'charts_dir': 图表目录
            }
        """
        # 生成HTML报告
        html_content = self._generate_html_report(
            data_info, validation_report, ontology,
            analysis_plan, analysis_results, chart_files or []
        )
        html_path = self.output_dir / "analysis_report.html"
        html_path.write_text(html_content, encoding='utf-8')

        # 生成Markdown报告
        md_content = self._generate_markdown_report(
            data_info, validation_report, ontology,
            analysis_plan, analysis_results
        )
        md_path = self.output_dir / "analysis_report.md"
        md_path.write_text(md_content, encoding='utf-8')

        return {
            'html_report': str(html_path),
            'markdown_report': str(md_path),
            'charts_dir': str(self.charts_dir)
        }

    def _generate_html_report(self,
                             data_info: Dict,
                             validation_report: Dict,
                             ontology: Dict,
                             analysis_plan: Dict,
                             analysis_results: Dict,
                             chart_files: List[str]) -> str:
        """生成HTML报告"""

        # 加载图表并转为base64
        charts_html = self._embed_charts(chart_files)

        # 提取关键数字
        key_numbers = self._extract_key_numbers(analysis_results, data_info)

        # 生成报告
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据分析报告 - {data_info.get('file_name', 'Unknown')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Helvetica Neue', Helvetica, Arial, 'Microsoft YaHei', sans-serif;
            line-height: 1.5;
            color: #1a1a1a;
            background: #fff;
            font-size: 12px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 30px 40px;
        }}

        /* 头部 */
        .header {{
            border-bottom: 2px solid #1a1a1a;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }}

        .header h1 {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 5px;
        }}

        .header .meta {{
            font-size: 11px;
            color: #666;
        }}

        /* 关键数字卡片 */
        .key-metrics {{
            display: flex;
            gap: 15px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}

        .metric-card {{
            flex: 1;
            min-width: 140px;
            padding: 12px 15px;
            background: #f8f9fa;
            border-left: 3px solid #333;
        }}

        .metric-card.warning {{
            border-left-color: #c00;
        }}

        .metric-card.success {{
            border-left-color: #27ae60;
        }}

        .metric-value {{
            font-size: 18px;
            font-weight: 600;
            color: #1a1a1a;
        }}

        .metric-label {{
            font-size: 10px;
            color: #666;
            margin-top: 3px;
        }}

        /* 一级章节 */
        .section {{
            margin-bottom: 25px;
        }}

        .section-title {{
            font-size: 14px;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 12px;
            padding-bottom: 6px;
            border-bottom: 1px solid #ddd;
        }}

        .section-note {{
            font-size: 10px;
            color: #999;
            margin: -8px 0 12px 0;
            font-style: italic;
        }}

        /* 二级：分析维度 */
        .dimension-block {{
            margin-left: 15px;
            margin-bottom: 18px;
        }}

        .dimension-title {{
            font-size: 12px;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
        }}

        /* 三级：洞察项 */
        .insight-item {{
            margin-left: 30px;
            margin-bottom: 15px;
            padding-left: 12px;
            border-left: 2px solid #ddd;
        }}

        .insight-item.high {{ border-left-color: #c00; }}
        .insight-item.medium {{ border-left-color: #666; }}
        .insight-item.low {{ border-left-color: #bbb; }}

        .insight-header {{
            display: flex;
            align-items: baseline;
            gap: 8px;
            margin-bottom: 6px;
        }}

        .insight-title {{
            font-size: 12px;
            font-weight: 600;
        }}

        .significance-tag {{
            font-size: 10px;
            font-weight: 600;
        }}

        .tag-high {{ color: #c00; }}
        .tag-medium {{ color: #666; }}
        .tag-low {{ color: #999; }}

        .insight-line {{
            margin-left: 0;
            margin-bottom: 4px;
            font-size: 11px;
            line-height: 1.6;
        }}

        .insight-line .label {{
            color: #666;
            font-size: 10px;
        }}

        .highlight-red {{
            color: #c00;
            font-weight: 600;
        }}

        .highlight-green {{
            color: #27ae60;
            font-weight: 600;
        }}

        /* 字段信息 */
        .field-summary {{
            margin-left: 15px;
            margin-bottom: 10px;
            font-size: 11px;
        }}

        .field-item {{
            display: inline-block;
            margin-right: 25px;
            margin-bottom: 5px;
        }}

        .field-label {{
            color: #666;
        }}

        .field-value {{
            font-weight: 600;
        }}

        /* 财报风格表格 */
        .financial-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 11px;
            margin: 8px 0 15px 15px;
            max-width: 600px;
        }}

        .financial-table thead {{
            border-top: 1px solid #1a1a1a;
            border-bottom: 1px solid #1a1a1a;
        }}

        .financial-table th {{
            padding: 6px 8px;
            text-align: left;
            font-weight: 600;
            background: #fafafa;
            font-size: 10px;
        }}

        .financial-table td {{
            padding: 5px 8px;
            border-bottom: 1px solid #eee;
        }}

        .financial-table .num {{
            text-align: right;
            font-family: 'Helvetica Neue', monospace;
        }}

        /* 公式/流程展示 */
        .process-flow {{
            margin-left: 15px;
            padding: 10px 15px;
            background: #f8f9fa;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 11px;
            line-height: 1.8;
            border-left: 3px solid #666;
            margin-bottom: 12px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}

        /* 结论框 */
        .conclusion-box {{
            margin-left: 15px;
            padding: 12px 15px;
            background: #f0f9f4;
            border-left: 3px solid #27ae60;
            margin-top: 10px;
        }}

        .conclusion-box.warning {{
            background: #fffbf0;
            border-left-color: #f39c12;
        }}

        .conclusion-box.critical {{
            background: #fff5f5;
            border-left-color: #c00;
        }}

        .conclusion-title {{
            font-size: 12px;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 8px;
        }}

        .conclusion-list {{
            margin: 0;
            padding-left: 18px;
            font-size: 11px;
            line-height: 1.6;
        }}

        .conclusion-list li {{
            margin-bottom: 4px;
        }}

        /* 假设状态 */
        .hypothesis-status {{
            font-weight: 600;
            padding: 2px 6px;
            border-radius: 2px;
            font-size: 10px;
        }}

        .hypothesis-status.status-supported {{
            color: #27ae60;
            background: #f0f9f4;
        }}

        .hypothesis-status.status-weak {{
            color: #f39c12;
            background: #fffbf0;
        }}

        .hypothesis-status.status-rejected {{
            color: #c00;
            background: #fff5f5;
        }}

        /* 数据质量问题列表 */
        .issue-list {{
            margin-left: 15px;
            margin-bottom: 12px;
        }}

        .issue-item {{
            margin-bottom: 8px;
            padding: 8px 10px;
            background: #f8f9fa;
            border-left: 2px solid #ddd;
            font-size: 11px;
        }}

        .issue-item.critical {{
            border-left-color: #c00;
            background: #fff5f5;
        }}

        .issue-item.warning {{
            border-left-color: #f39c12;
            background: #fffbf0;
        }}

        .issue-field {{
            font-weight: 600;
            color: #1a1a1a;
        }}

        .issue-count {{
            color: #c00;
            font-weight: 600;
        }}

        /* 图表容器 */
        .chart-container {{
            margin: 10px 0 15px 30px;
            text-align: center;
        }}

        .chart-container img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #eee;
        }}

        .chart-caption {{
            font-size: 10px;
            color: #666;
            margin-top: 5px;
            font-style: italic;
        }}

        /* 行动建议 */
        .action-list {{
            margin-left: 15px;
            list-style: none;
            counter-reset: action-counter;
        }}

        .action-item {{
            margin-left: 0;
            margin-bottom: 6px;
            padding-left: 20px;
            text-indent: -15px;
            font-size: 11px;
            line-height: 1.5;
        }}

        .action-item::before {{
            counter-increment: action-counter;
            content: counter(action-counter) ". ";
            color: #999;
        }}

        .priority-mark {{
            font-size: 10px;
            font-weight: 600;
            margin-right: 6px;
        }}

        .priority-high {{ color: #c00; }}

        /* 页脚 */
        .footer {{
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
            font-size: 10px;
            color: #999;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{data_info.get('report_title', '数据分析报告')}</h1>
            <div class="meta">
                生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} |
                数据源：{data_info.get('file_name', 'Unknown')} |
                AI 辅助数据分析
            </div>
        </div>

        <!-- 关键指标卡片 -->
        <div class="key-metrics">
            {key_numbers}
        </div>

        <!-- 1. 数据质量诊断 -->
        <div class="section">
            <h2 class="section-title">1. 数据质量诊断</h2>
            <div class="section-note">基于 data_validator 自动检测的数据质量问题</div>

            {self._generate_quality_section(validation_report)}
        </div>

        <!-- 2. 数据特征描述 -->
        <div class="section">
            <h2 class="section-title">2. 数据特征描述</h2>
            <div class="section-note">数据本体识别结果：实体类型、生成机制、核心维度</div>

            {self._generate_ontology_section(ontology)}
        </div>

        <!-- 3. 分析方法规划 -->
        <div class="section">
            <h2 class="section-title">3. 分析方法规划</h2>
            <div class="section-note">问题类型判定、领域框架匹配、分析路径设计</div>

            {self._generate_planning_section(analysis_plan)}
        </div>

        <!-- 4. 分析结果 -->
        <div class="section">
            <h2 class="section-title">4. 分析结果</h2>
            <div class="section-note">基于执行脚本的分析发现与数据洞察</div>

            {self._generate_results_section(analysis_results)}

            <!-- 图表展示 -->
            {charts_html}
        </div>

        <!-- 5. 结论与建议 -->
        <div class="section">
            <h2 class="section-title">5. 结论与建议</h2>
            {self._generate_conclusions_section(analysis_results)}
        </div>

        <!-- 页脚 -->
        <div class="footer">
            本报告由 Universal Data Analyst 自动生成 |
            数据局限性说明见各章节标注
        </div>
    </div>
</body>
</html>"""
        return html

    def _generate_markdown_report(self,
                                 data_info: Dict,
                                 validation_report: Dict,
                                 ontology: Dict,
                                 analysis_plan: Dict,
                                 analysis_results: Dict) -> str:
        """生成Markdown报告（仅文字部分）"""

        md = f"""# {data_info.get('report_title', '数据分析报告')}

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 数据源：{data_info.get('file_name', 'Unknown')}
> AI 辅助数据分析

---

## 1. 数据质量诊断

### 1.1 数据规模
- **原始数据**：{data_info.get('rows', 0):,} 行 × {data_info.get('columns', 0)} 列
- **质量评分**：{validation_report.get('overall_score', 0):.1f}/100

### 1.2 发现的问题

"""

        # 添加数据质量问题
        issues = validation_report.get('issues', [])
        if issues:
            for issue in issues[:10]:  # 最多显示10个问题
                severity = issue.get('severity', 'info')
                col = issue.get('column', '整表')
                desc = issue.get('description', '')
                affected = issue.get('affected_rows', 0)
                pct = issue.get('affected_percent', 0)

                md += f"- **[{severity.upper()}]** `{col}`: {desc}\n"
                md += f"  - 影响：{affected:,} 行 ({pct:.1f}%)\n"

                # 添加清洗操作说明
                action = issue.get('cleaning_action', {})
                if action:
                    md += f"  - 处理：{action.get('description', '需人工审核')}\n"
                md += "\n"
        else:
            md += "✅ 未检测到明显的数据质量问题\n\n"

        # 数据特征描述
        md += """---

## 2. 数据特征描述

### 2.1 实体类型
"""
        md += f"- **判定**：{ontology.get('entity_type', '待识别')}\n"
        md += f"- **依据**：{ontology.get('entity_type_reason', '')}\n\n"

        md += "### 2.2 数据生成机制\n"
        md += f"- **判定**：{ontology.get('generation_mechanism', '待识别')}\n"
        md += f"- **依据**：{ontology.get('mechanism_reason', '')}\n\n"

        md += "### 2.3 核心维度\n"
        for dim in ontology.get('core_dimensions', []):
            md += f"- **{dim.get('dimension', '')}**：{dim.get('description', '')}\n"

        md += f"\n### 2.4 经济类型判定\n"
        if ontology.get('is_economic'):
            md += f"- **类型**：{ontology.get('economic_type', '未知')}\n"
        else:
            md += f"- **领域**：{ontology.get('domain_type', '待识别')}\n"

        md += f"\n### 2.5 数据局限性\n"
        for lim in ontology.get('limitations', []):
            md += f"- {lim}\n"

        # 分析方法规划
        md += """\n---

## 3. 分析方法规划

"""
        md += f"### 3.1 问题类型判定\n"
        md += f"- **判定**：{analysis_plan.get('question_type', '待规划')}\n"
        md += f"- **依据**：{analysis_plan.get('question_type_reason', '')}\n\n"

        md += "### 3.2 推荐分析框架\n"
        for fw in analysis_plan.get('frameworks', []):
            md += f"- **{fw.get('name', '')}**：{fw.get('reason', '')}\n"
            md += f"  - 应用场景：{fw.get('application', '')}\n"

        md += "\n### 3.3 分析步骤\n"
        for step in analysis_plan.get('analysis_steps', []):
            md += f"\n**步骤 {step.get('step_number', '?')}：{step.get('name', '')}**\n"
            md += f"- 目的：{step.get('purpose', '')}\n"
            md += f"- 方法：{step.get('method', '')}\n"
            md += f"- 输出：{step.get('output', '')}\n"

        # 分析结果
        md += """\n---

## 4. 分析结果

"""
        # 执行摘要
        md += "### 4.1 执行摘要\n"
        exec_summary = analysis_results.get('executive_summary', [])
        if exec_summary:
            for item in exec_summary:
                md += f"- {item}\n"
        else:
            # 从结果中提取关键发现
            findings = analysis_results.get('findings', [])
            for finding in findings[:5]:
                md += f"- {finding}\n"

        # 详细发现
        md += "\n### 4.2 详细发现\n"
        detailed = analysis_results.get('detailed_findings', {})
        for section, content in detailed.items():
            md += f"\n#### {section}\n"
            if isinstance(content, list):
                for item in content:
                    md += f"- {item}\n"
            elif isinstance(content, dict):
                for key, value in content.items():
                    md += f"- **{key}**：{value}\n"
            else:
                md += f"{content}\n"

        # 结论与建议
        md += """\n---

## 5. 结论与建议

"""
        md += "### 5.1 主要结论\n"
        conclusions = analysis_results.get('conclusions', [])
        for conclusion in conclusions:
            md += f"- {conclusion}\n"

        md += "\n### 5.2 行动建议\n"
        recommendations = analysis_results.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            md += f"{i}. {rec}\n"

        md += "\n### 5.3 数据局限性说明\n"
        limitations = analysis_results.get('limitations', [])
        if limitations:
            for lim in limitations:
                md += f"- {lim}\n"
        else:
            md += "- 分析基于当前数据快照，可能存在幸存者偏差\n"
            md += "- 时间维度有限，难以分析长期趋势\n"

        md += """\n---

> **附注**：
> - 本报告图表保存在 `output/charts/` 目录下
> - 详细数据结果保存在 `analysis_results.json` 中
> - 如需重新分析，请保留原始数据文件
"""

        return md

    def _embed_charts(self, chart_files: List[str]) -> str:
        """将图表嵌入HTML（base64编码）"""
        if not chart_files:
            return ""

        html = '<div class="dimension-block">\n'
        html += '<div class="dimension-title">可视化图表</div>\n'

        for chart_path in chart_files:
            chart_file = Path(chart_path)
            if not chart_file.exists():
                continue

            try:
                with open(chart_file, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode('utf-8')

                # 根据文件扩展名确定MIME类型
                ext = chart_file.suffix.lower()
                mime = 'image/png' if ext == '.png' else 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/svg+xml'

                caption = chart_file.stem.replace('_', ' ').replace('-', ' ').title()

                html += f'''
                <div class="chart-container">
                    <img src="data:{mime};base64,{img_data}" alt="{caption}" />
                    <div class="chart-caption">{caption}</div>
                </div>
                '''
            except Exception as e:
                html += f'<div class="chart-container">图表加载失败: {e}</div>\n'

        html += '</div>\n'
        return html

    def _extract_key_numbers(self, analysis_results: Dict, data_info: Dict) -> str:
        """提取关键数字生成卡片"""
        cards = []

        # 数据规模
        cards.append({
            'value': f"{data_info.get('rows', 0):,}",
            'label': '数据行数',
            'class': ''
        })

        # 从分析结果中提取关键指标
        key_metrics = analysis_results.get('key_metrics', {})
        for name, value in list(key_metrics.items())[:3]:
            cards.append({
                'value': str(value),
                'label': name,
                'class': 'warning' if '流失' in name or '风险' in name else 'success'
            })

        # 如果没有关键指标，显示默认信息
        if len(cards) < 2:
            cards.append({
                'value': f"{data_info.get('columns', 0)}",
                'label': '字段数',
                'class': ''
            })

        html = ''
        for card in cards:
            html += f'''
            <div class="metric-card {card['class']}">
                <div class="metric-value">{card['value']}</div>
                <div class="metric-label">{card['label']}</div>
            </div>
            '''

        return html

    def _format_p_value(self, p_value: float) -> str:
        """格式化p值为粗体数字，不使用文字标签"""
        if p_value < 0.0001:
            return "<strong>&lt; 0.0001</strong>"
        return f"<strong>{p_value:.4f}</strong>"

    def _generate_formula_html(self, title: str, formula_lines: List[str], variables: List[tuple]) -> str:
        """
        生成标准格式的公式HTML

        Args:
            title: 公式标题（如"基础模型"）
            formula_lines: 公式行列表，每行一个公式
            variables: 变量说明列表，每个元素为(name, description)元组
        """
        html = '<div class="process-flow">\n'
        html += f'{title}:\n'
        for line in formula_lines:
            html += f'  {line}\n'
        html += '\n其中:\n'
        for name, desc in variables:
            html += f'  {name} = {desc}\n'
        html += '</div>'
        return html

    def _generate_conclusion_box(self, title: str = "结论", items: List[str] = None, box_type: str = "") -> str:
        """生成结论框HTML"""
        box_class = f"conclusion-box {box_type}".strip()
        html = f'<div class="{box_class}">'
        html += f'<div class="conclusion-title">{title}</div>'
        html += '<ul class="conclusion-list">'
        for item in items or []:
            html += f'<li>{item}</li>'
        html += '</ul></div>'
        return html

    def _generate_quality_section(self, validation_report: Dict) -> str:
        """生成数据质量章节HTML"""
        html = ''

        # 质量评分
        score = validation_report.get('overall_score', 0)
        score_class = 'highlight-red' if score < 60 else 'highlight-green' if score >= 80 else ''

        html += f'''
        <div class="dimension-block">
            <div class="dimension-title">质量评分：<span class="{score_class}">{score:.1f}/100</span></div>
        </div>
        '''

        # 问题列表
        issues = validation_report.get('issues', [])
        if issues:
            html += '<div class="dimension-block">\n'
            html += '<div class="dimension-title">发现的问题</div>\n'
            html += '<div class="issue-list">\n'

            for issue in issues[:15]:  # 最多显示15个问题
                severity = issue.get('severity', 'info')
                col = issue.get('column', '整表')
                desc = issue.get('description', '')
                affected = issue.get('affected_rows', 0)
                pct = issue.get('affected_percent', 0)

                css_class = 'critical' if severity == 'critical' else 'warning' if severity == 'warning' else ''

                html += f'''
                <div class="issue-item {css_class}">
                    <span class="issue-field">{col}</span>：
                    {desc}<br/>
                    <span style="color:#666;font-size:10px;">
                        影响：<span class="issue-count">{affected:,}</span> 行 ({pct:.1f}%) |
                        严重程度：{severity.upper()}
                    </span>
                </div>
                '''

            html += '</div>\n</div>\n'

        # 清洗操作建议
        cleaning = validation_report.get('cleaning_summary', {})
        if cleaning:
            html += '<div class="dimension-block">\n'
            html += '<div class="dimension-title">清洗操作建议</div>\n'

            deletions = cleaning.get('recommended_deletions', 0)
            fills = cleaning.get('recommended_fills', 0)
            reviews = cleaning.get('recommended_reviews', 0)

            if deletions > 0:
                html += f'<div class="insight-line"><span class="label">建议删除行：</span>{deletions:,} 行</div>\n'
            if fills > 0:
                html += f'<div class="insight-line"><span class="label">建议填充：</span>{fills:,} 个缺失值</div>\n'
            if reviews > 0:
                html += f'<div class="insight-line"><span class="label">建议人工审核：</span>{reviews:,} 行</div>\n'

            html += '</div>\n'

        return html

    def _generate_ontology_section(self, ontology: Dict) -> str:
        """生成数据特征描述章节HTML"""
        html = ''

        # 实体类型
        html += '<div class="dimension-block">\n'
        html += '<div class="dimension-title">实体类型识别</div>\n'
        html += f'<div class="insight-item medium">\n'
        html += f'<div class="insight-title">{ontology.get("entity_type", "待识别")}</div>\n'
        html += f'<div class="insight-line">{ontology.get("entity_type_reason", "")}</div>\n'
        html += '</div>\n</div>\n'

        # 生成机制
        html += '<div class="dimension-block">\n'
        html += '<div class="dimension-title">数据生成机制</div>\n'
        html += f'<div class="insight-item medium">\n'
        html += f'<div class="insight-title">{ontology.get("generation_mechanism", "待识别")}</div>\n'
        html += f'<div class="insight-line">{ontology.get("mechanism_reason", "")}</div>\n'
        html += '</div>\n</div>\n'

        # 核心维度
        html += '<div class="dimension-block">\n'
        html += '<div class="dimension-title">核心维度</div>\n'
        html += '<table class="financial-table">\n'
        html += '<thead><tr><th>维度</th><th>说明</th></tr></thead>\n<tbody>\n'
        for dim in ontology.get('core_dimensions', []):
            html += f'<tr><td>{dim.get("dimension", "")}</td><td>{dim.get("description", "")}</td></tr>\n'
        html += '</tbody></table>\n</div>\n'

        # 经济类型
        html += '<div class="dimension-block">\n'
        html += '<div class="dimension-title">经济类型判定</div>\n'
        if ontology.get('is_economic'):
            html += f'<div class="insight-item high">\n'
            html += f'<div class="insight-title">{ontology.get("economic_type", "未知")}</div>\n'
        else:
            html += f'<div class="insight-item low">\n'
            html += f'<div class="insight-title">{ontology.get("domain_type", "待识别")}</div>\n'
        html += '</div>\n</div>\n'

        # 关键词
        html += '<div class="dimension-block">\n'
        html += '<div class="dimension-title">关键词标签</div>\n'
        html += '<div class="field-summary">\n'
        for kw in ontology.get('keywords', []):
            html += f'<span class="field-item"><span class="field-value">{kw}</span></span>\n'
        html += '</div>\n</div>\n'

        return html

    def _generate_planning_section(self, analysis_plan: Dict) -> str:
        """生成分析方法规划章节HTML"""
        html = ''

        # 问题类型
        html += '<div class="dimension-block">\n'
        html += '<div class="dimension-title">问题类型判定</div>\n'
        html += f'<div class="insight-item high">\n'
        html += f'<div class="insight-title">{analysis_plan.get("question_type", "待规划")}</div>\n'
        html += f'<div class="insight-line">{analysis_plan.get("question_type_reason", "")}</div>\n'
        html += '</div>\n</div>\n'

        # 推荐框架
        html += '<div class="dimension-block">\n'
        html += '<div class="dimension-title">推荐分析框架</div>\n'
        for fw in analysis_plan.get('frameworks', []):
            html += f'<div class="insight-item medium">\n'
            html += f'<div class="insight-title">{fw.get("name", "")}</div>\n'
            html += f'<div class="insight-line">{fw.get("reason", "")}</div>\n'
            html += f'<div class="insight-line"><span class="label">应用场景：</span>{fw.get("application", "")}</div>\n'
            html += '</div>\n'
        html += '</div>\n'

        # 分析步骤
        html += '<div class="dimension-block">\n'
        html += '<div class="dimension-title">分析步骤</div>\n'
        html += '<table class="financial-table">\n'
        html += '<thead><tr><th>步骤</th><th>名称</th><th>方法</th><th>输出</th></tr></thead>\n<tbody>\n'
        for step in analysis_plan.get('analysis_steps', []):
            html += f'<tr>\n'
            html += f'<td>{step.get("step_number", "?")}</td>\n'
            html += f'<td>{step.get("name", "")}</td>\n'
            html += f'<td>{step.get("method", "")}</td>\n'
            html += f'<td>{step.get("output", "")}</td>\n'
            html += '</tr>\n'
        html += '</tbody></table>\n</div>\n'

        # 前置条件
        if analysis_plan.get('prerequisites'):
            html += '<div class="dimension-block">\n'
            html += '<div class="dimension-title">前置条件</div>\n'
            html += '<ul class="action-list">\n'
            for pre in analysis_plan.get('prerequisites', []):
                html += f'<li class="action-item">{pre}</li>\n'
            html += '</ul>\n</div>\n'

        return html

    def _generate_results_section(self, analysis_results: Dict) -> str:
        """生成分析结果章节HTML"""
        html = ''

        # 执行摘要
        html += '<div class="dimension-block">\n'
        html += '<div class="dimension-title">执行摘要</div>\n'

        exec_summary = analysis_results.get('executive_summary', [])
        if exec_summary:
            for item in exec_summary:
                html += f'<div class="insight-item high">\n'
                html += f'<div class="insight-line">{item}</div>\n'
                html += '</div>\n'
        else:
            findings = analysis_results.get('findings', [])
            for finding in findings[:5]:
                html += f'<div class="insight-item medium">\n'
                html += f'<div class="insight-line">{finding}</div>\n'
                html += '</div>\n'

        html += '</div>\n'

        # 详细发现
        detailed = analysis_results.get('detailed_findings', {})
        if detailed:
            html += '<div class="dimension-block">\n'
            html += '<div class="dimension-title">详细发现</div>\n'

            for section, content in detailed.items():
                html += f'<div class="insight-item medium">\n'
                html += f'<div class="insight-title">{section}</div>\n'

                if isinstance(content, list):
                    for item in content:
                        html += f'<div class="insight-line">• {item}</div>\n'
                elif isinstance(content, dict):
                    html += '<table class="financial-table">\n<tbody>\n'
                    for key, value in content.items():
                        html += f'<tr><td>{key}</td><td class="num">{value}</td></tr>\n'
                    html += '</tbody></table>\n'
                else:
                    html += f'<div class="insight-line">{content}</div>\n'

                html += '</div>\n'

            html += '</div>\n'

        return html

    def _generate_conclusions_section(self, analysis_results: Dict) -> str:
        """生成结论与建议章节HTML"""
        html = ''

        # 主要结论
        html += '<div class="dimension-block">\n'
        html += '<div class="dimension-title">主要结论</div>\n'

        conclusions = analysis_results.get('conclusions', [])
        if conclusions:
            for conclusion in conclusions:
                html += f'<div class="insight-item high">\n'
                html += f'<div class="insight-line">{conclusion}</div>\n'
                html += '</div>\n'
        else:
            html += '<div class="insight-line">基于数据分析得出上述发现，具体结论请结合实际业务场景进一步判断。</div>\n'

        html += '</div>\n'

        # 行动建议
        html += '<div class="dimension-block">\n'
        html += '<div class="dimension-title">行动建议</div>\n'
        html += '<ol class="action-list">\n'

        recommendations = analysis_results.get('recommendations', [])
        for rec in recommendations:
            priority = 'high' if '优先' in rec or '紧急' in rec else 'medium'
            html += f'<li class="action-item"><span class="priority-mark priority-{priority}">●</span>{rec}</li>\n'

        html += '</ol>\n</div>\n'

        # 局限性
        html += '<div class="dimension-block">\n'
        html += '<div class="dimension-title">数据局限性</div>\n'

        limitations = analysis_results.get('limitations', [])
        if limitations:
            for lim in limitations:
                html += f'<div class="insight-item low">\n'
                html += f'<div class="insight-line">{lim}</div>\n'
                html += '</div>\n'
        else:
            html += '<div class="insight-item low">\n'
            html += '<div class="insight-line">分析基于当前数据快照，可能存在幸存者偏差；时间维度有限，难以分析长期趋势。</div>\n'
            html += '</div>\n'

        html += '</div>\n'

        return html


def main():
    """测试入口"""
    import tempfile

    # 创建测试数据
    test_session_dir = tempfile.mkdtemp()
    generator = ReportGenerator(test_session_dir)

    # 模拟数据
    data_info = {
        'file_name': 'test_data.csv',
        'rows': 10000,
        'columns': 20,
        'report_title': '测试分析报告'
    }

    validation_report = {
        'overall_score': 85.5,
        'issues': [
            {
                'severity': 'warning',
                'column': 'price',
                'description': '存在异常值',
                'affected_rows': 50,
                'affected_percent': 0.5,
                'cleaning_action': {'description': '建议人工审核'}
            }
        ],
        'cleaning_summary': {
            'recommended_deletions': 0,
            'recommended_fills': 100,
            'recommended_reviews': 50
        }
    }

    ontology = {
        'entity_type': '交易/事件型',
        'entity_type_reason': '每行是一个独立的交易事件',
        'generation_mechanism': '观测型',
        'mechanism_reason': '系统被动记录',
        'core_dimensions': [
            {'dimension': '时间', 'description': '交易时间戳'},
            {'dimension': '用户', 'description': '购买者ID'}
        ],
        'is_economic': True,
        'economic_type': '零售经济',
        'domain_type': '商业',
        'keywords': ['电商', '交易', '零售'],
        'limitations': ['缺乏退货数据']
    }

    analysis_plan = {
        'question_type': '诊断型',
        'question_type_reason': '用户询问为什么',
        'frameworks': [{'name': 'RFM', 'reason': '适合客户分层', 'application': '识别高价值客户'}],
        'analysis_steps': [
            {'step_number': 1, 'name': '数据清洗', 'method': '缺失值处理', 'output': '清洗后数据'}
        ],
        'prerequisites': ['数据完整']
    }

    analysis_results = {
        'executive_summary': ['核心发现1', '核心发现2'],
        'findings': ['发现1', '发现2', '发现3'],
        'conclusions': ['结论1', '结论2'],
        'recommendations': ['建议1', '建议2'],
        'limitations': ['局限性1'],
        'key_metrics': {'流失率': '26.5%', 'CLTV': '$5,400'}
    }

    result = generator.generate_all_reports(
        data_info, validation_report, ontology,
        analysis_plan, analysis_results, []
    )

    print(f"HTML报告: {result['html_report']}")
    print(f"MD报告: {result['markdown_report']}")


if __name__ == '__main__':
    main()

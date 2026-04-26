#!/usr/bin/env python3
"""
战略分析报告生成器
支持Markdown和HTML双格式输出
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ReportSection:
    """报告章节"""
    title: str
    level: int  # 1-4
    content: str


class HTMLReportGenerator:
    """HTML报告生成器 - 专业严谨风格(黑/红/灰)"""

    # 专业配色方案 - 黑红灰
    COLORS = {
        'primary': '#000000',      # 黑色 - 主色
        'secondary': '#333333',    # 深灰 - 次要
        'accent': '#cc0000',       # 红色 - 强调
        'success': '#555555',      # 中灰
        'warning': '#cc0000',      # 红色
        'danger': '#990000',       # 深红
        'text': '#222222',         # 正文黑
        'text_light': '#666666',   # 浅灰
        'bg': '#ffffff',           # 白色背景
        'bg_alt': '#f5f5f5',       # 交替背景
        'border': '#cccccc',       # 边框 - 浅灰
    }

    # 可信度星级颜色
    RELIABILITY_COLORS = {
        5: '#000000',  # 黑
        4: '#555555',  # 中灰
        3: '#888888',  # 浅灰
        2: '#cc3333',  # 红
        1: '#990000',  # 深红
    }

    # 优先级样式
    PRIORITY_STYLES = {
        'P1': {'bg': '#fee2e2', 'color': '#7f1d1d', 'border': '#dc2626'},
        'P2': {'bg': '#f3f4f6', 'color': '#374151', 'border': '#9ca3af'},
        'P3': {'bg': '#fafafa', 'color': '#525252', 'border': '#a3a3a3'},
    }

    def __init__(self, title: str, subtitle: str = ""):
        self.title = title
        self.subtitle = subtitle
        self.sections: List[ReportSection] = []
        self.metadata = {
            'generated_at': datetime.now().isoformat(),
            'version': '1.2',
        }

    def add_section(self, title: str, level: int, content: str):
        """添加章节"""
        self.sections.append(ReportSection(title, level, content))

    def _parse_markdown_tables(self, content: str) -> str:
        """解析Markdown表格为HTML表格"""
        # 匹配Markdown表格
        table_pattern = r'\|([^\n]+)\|\n\|[-:\s|]+\|\n((?:\|[^\n]+\|\n?)+)'

        def convert_table(match):
            header_line = match.group(1).strip()
            body_lines = match.group(2).strip()

            # 解析表头
            headers = [h.strip() for h in header_line.split('|') if h.strip()]

            # 解析行
            rows = []
            for line in body_lines.split('\n'):
                if line.strip():
                    cells = [c.strip() for c in line.split('|') if c.strip()]
                    if cells:
                        rows.append(cells)

            # 生成HTML表格（含下载按钮）
            html = ['<div class="table-wrapper">']
            html.append('<div class="table-actions">')
            html.append('<button class="table-download-btn" onclick="downloadTableAsPng(this)" title="下载PNG">PNG</button>')
            html.append('<button class="table-download-btn" onclick="downloadTableAsSvg(this)" title="下载SVG">SVG</button>')
            html.append('</div>')
            html.append('<table class="data-table">')

            # 表头
            html.append('<thead><tr>')
            for header in headers:
                html.append(f'<th>{self._format_cell_content(header)}</th>')
            html.append('</tr></thead>')

            # 表体
            html.append('<tbody>')
            for row in rows:
                html.append('<tr>')
                for i, cell in enumerate(row):
                    if i < len(headers):
                        html.append(f'<td>{self._format_cell_content(cell)}</td>')
                html.append('</tr>')
            html.append('</tbody>')

            html.append('</table></div>')
            return '\n'.join(html)

        return re.sub(table_pattern, convert_table, content)

    def _format_cell_content(self, content: str) -> str:
        """格式化单元格内容 - 处理星级、优先级等特殊标记"""
        # 可信度星级
        star_match = re.search(r'(★+)(☆*)', content)
        if star_match:
            filled = len(star_match.group(1))
            color = self.RELIABILITY_COLORS.get(filled, self.COLORS['text'])
            stars_html = f'<span class="reliability-stars" style="color: {color};">{star_match.group(0)}</span>'
            content = content.replace(star_match.group(0), stars_html)

        # 优先级P1/P2/P3
        for p, style in self.PRIORITY_STYLES.items():
            if p in content:
                badge = f'<span class="priority-badge priority-{p.lower()}" style="background: {style["bg"]}; color: {style["color"]}; border: 1px solid {style["border"]};">{p}</span>'
                content = content.replace(p, badge)

        # 趋势箭头
        content = content.replace('↑', '<span class="trend-arrow trend-up">↑</span>')
        content = content.replace('↓', '<span class="trend-arrow trend-down">↓</span>')
        content = content.replace('→', '<span class="trend-arrow trend-stable">→</span>')

        return content

    def _parse_markdown_content(self, content: str) -> str:
        """解析Markdown内容为HTML"""
        # 先处理表格
        content = self._parse_markdown_tables(content)

        # 处理水平分割线（Markdown 章节分隔符）
        content = re.sub(r'\n*-{3,}\n*', '\n\n<hr/>\n\n', content)

        # 处理任务清单
        content = re.sub(r'^- \[x\] (.+)$', r'<div class="check-item checked">\1</div>', content, flags=re.MULTILINE)
        content = re.sub(r'^- \[ \] (.+)$', r'<div class="check-item">\1</div>', content, flags=re.MULTILINE)
        content = re.sub(r'^- (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)

        # 包裹连续的 li（仅吞掉列表项之间的换行，保留列表后的空行）
        li_pattern = r'(?:<li>.*?</li>(?:\n(?=<li>))?)+'
        def wrap_ul(match):
            inner = match.group(0)
            return f'<ul class="bullet-list">{inner}</ul>'
        content = re.sub(li_pattern, wrap_ul, content, flags=re.DOTALL)

        # 处理有序列表：确保每项独立成行
        content = re.sub(r'^(\d+)\.\s+(.+)$', r'<li value="\1">\2</li>', content, flags=re.MULTILINE)
        ol_pattern = r'(?:<li value="\d+">.*?</li>(?:\n(?=<li value="))?)+'
        def wrap_ol(match):
            inner = match.group(0)
            return f'<ol class="numbered-list">{inner}</ol>'
        content = re.sub(ol_pattern, wrap_ol, content, flags=re.DOTALL)

        # 防止 ul/ol 被包裹进 p 标签
        content = re.sub(r'<(/?(?:ul|ol)[^>]*)>', r'\n<\1>\n', content)

        # 处理 Markdown 链接（必须在强调之前，避免冲突）
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)

        # 处理强调
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
        content = re.sub(r'`(.+?)`', r'<code>\1</code>', content)

        # 处理引用块
        content = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', content, flags=re.MULTILINE)

        # 处理段落 - 将空行分隔的文本包裹为段落
        segments = re.split(r'\n\s*\n', content)
        formatted = []
        inline_tags = {'strong', 'em', 'code', 'span', 'a', 'b', 'i', 'u', 's', 'del', 'ins', 'sub', 'sup', 'mark', 'small', 'label', 'img', 'br', 'wbr'}
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue

            # 判断 segment 是否以块级 HTML 元素开头
            first_tag = re.match(r'<([a-zA-Z][a-zA-Z0-9]*)', seg)
            is_block = False
            if first_tag:
                tag_name = first_tag.group(1).lower()
                if tag_name not in inline_tags:
                    is_block = True

            if is_block:
                formatted.append(seg)
            else:
                formatted.append(f'<p>{seg}</p>')

        return '\n'.join(formatted)

    def _generate_css(self) -> str:
        """生成CSS样式 - 专业黑红灰风格，紧凑排版，金融研报式表格"""
        return f"""
        <style>
            :root {{
                --primary: {self.COLORS['primary']};
                --secondary: {self.COLORS['secondary']};
                --accent: {self.COLORS['accent']};
                --text: {self.COLORS['text']};
                --text-light: {self.COLORS['text_light']};
                --bg-alt: {self.COLORS['bg_alt']};
                --border: {self.COLORS['border']};
            }}

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                font-size: 13px;
                line-height: 1.65;
                color: var(--text);
                background: #ffffff;
                padding: 20px;
            }}

            .report-container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
            }}

            /* 封面 - 极简扁平 */
            .cover {{
                background: #fff;
                color: var(--primary);
                padding: 30px 0 15px 0;
                text-align: left;
                border-bottom: 2px solid var(--primary);
                margin-bottom: 25px;
            }}

            .cover h1 {{
                font-size: 1.6em;
                font-weight: 600;
                margin-bottom: 6px;
                letter-spacing: 0.5px;
            }}

            .cover .subtitle {{
                font-size: 1em;
                color: var(--secondary);
                font-weight: 400;
                margin-bottom: 10px;
            }}

            .cover .meta {{
                font-size: 0.8em;
                color: var(--text-light);
            }}

            /* 内容区 */
            .content {{
                padding: 0;
            }}

            /* 章节标题 */
            h1.section-title {{
                color: var(--primary);
                font-size: 1.25em;
                font-weight: 600;
                margin: 28px 0 12px 0;
                padding-bottom: 4px;
                border-bottom: 1px solid var(--border);
            }}

            h2.section-title {{
                color: var(--secondary);
                font-size: 1.05em;
                font-weight: 600;
                margin: 18px 0 8px 0;
            }}

            h3.section-title {{
                color: var(--text);
                font-size: 0.95em;
                font-weight: 600;
                margin: 14px 0 6px 0;
            }}

            /* 内容区 Flex 布局 */
            .section-content {{
                display: flex;
                flex-wrap: wrap;
                gap: 16px;
                align-items: flex-start;
            }}

            .section-content > *:not(.table-wrapper) {{
                flex: 1 1 100%;
                width: 100%;
            }}

            .section-content > .table-wrapper {{
                flex: 1 1 calc(50% - 10px);
                min-width: 280px;
            }}

            /* 数据表格 - 金融研报风格 */
            .table-wrapper {{
                position: relative;
                overflow-x: auto;
                margin: 8px 0;
            }}

            .table-actions {{
                position: absolute;
                top: 4px;
                right: 4px;
                display: none;
                gap: 4px;
                z-index: 10;
            }}

            .table-wrapper:hover .table-actions {{
                display: flex;
            }}

            .table-download-btn {{
                font-size: 11px;
                padding: 2px 6px;
                border: 1px solid var(--border);
                background: #fff;
                color: var(--primary);
                cursor: pointer;
                line-height: 1.2;
            }}

            .table-download-btn:hover {{
                background: var(--bg-alt);
                border-color: var(--primary);
            }}

            table.data-table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 0.85em;
                border: none;
                background: #fff;
            }}

            table.data-table thead {{
                background: #fff;
                color: var(--primary);
            }}

            table.data-table th {{
                padding: 6px 8px;
                text-align: left;
                font-weight: 600;
                border: none;
                border-bottom: 2px solid var(--primary);
                font-size: 0.85em;
                letter-spacing: 0.3px;
            }}

            table.data-table td {{
                padding: 5px 8px;
                border: none;
                border-bottom: 1px solid var(--border);
            }}

            table.data-table tbody tr:last-child td {{
                border-bottom: 1px solid #999;
            }}

            /* 可信度星级 */
            .reliability-stars {{
                font-size: 1em;
                letter-spacing: 1px;
            }}

            /* 优先级徽章 */
            .priority-badge {{
                display: inline-block;
                padding: 1px 6px;
                border-radius: 2px;
                font-size: 0.8em;
                font-weight: 600;
            }}

            /* 趋势箭头 */
            .trend-arrow {{
                font-weight: bold;
                font-size: 1.1em;
                margin: 0 2px;
            }}

            .trend-up {{ color: #cc0000; }}
            .trend-down {{ color: #990000; }}
            .trend-stable {{ color: var(--text-light); }}

            /* 列表 */
            ul.bullet-list, ol.numbered-list {{
                margin: 8px 0 8px 20px;
                padding-left: 0;
            }}

            ul.bullet-list li, ol.numbered-list li {{
                margin-bottom: 5px;
                line-height: 1.6;
            }}

            /* 引用块 */
            blockquote {{
                border-left: 2px solid var(--accent);
                padding: 6px 10px;
                margin: 10px 0;
                color: var(--text-light);
                font-size: 0.95em;
            }}

            /* 代码 */
            code {{
                background: #f5f5f5;
                padding: 1px 4px;
                border-radius: 2px;
                font-family: "SF Mono", Monaco, "Cascadia Code", monospace;
                font-size: 0.85em;
                color: var(--danger);
            }}

            /* 强调框 */
            .highlight-box {{
                background: #fafafa;
                border-left: 2px solid var(--accent);
                padding: 10px;
                margin: 10px 0;
                font-size: 0.95em;
            }}

            /* 执行摘要 - 扁平化 */
            .executive-summary {{
                background: none;
                padding: 0;
                margin-bottom: 20px;
                border: none;
            }}

            .key-metrics {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 10px;
                margin: 10px 0;
            }}

            .metric-card {{
                background: white;
                padding: 10px;
                border: 1px solid var(--border);
                text-align: center;
            }}

            .metric-value {{
                font-size: 1.4em;
                font-weight: 600;
                color: var(--primary);
                margin-bottom: 2px;
            }}

            .metric-label {{
                color: var(--text-light);
                font-size: 0.8em;
            }}

            /* 章节内容 */
            .section-content p {{
                margin-bottom: 8px;
                text-align: justify;
            }}

            /* 分隔线 */
            hr {{
                border: none;
                border-top: 1px solid var(--border);
                margin: 16px 0;
                flex-basis: 100%;
            }}

            /* 页脚 */
            .footer {{
                background: none;
                padding: 20px 0 10px 0;
                text-align: left;
                color: var(--text-light);
                font-size: 0.8em;
                border-top: 1px solid var(--border);
                margin-top: 30px;
            }}

            /* 打印样式 */
            @media print {{
                body {{
                    background: white;
                    padding: 0;
                }}
                .report-container {{
                    border: none;
                }}
                .content {{
                    padding: 0;
                }}
            }}

            /* 响应式 */
            @media (max-width: 768px) {{
                body {{
                    padding: 12px;
                }}
                .cover h1 {{
                    font-size: 1.3em;
                }}
                .section-content > .table-wrapper {{
                    flex: 1 1 100%;
                }}
                table.data-table {{
                    font-size: 0.8em;
                }}
                table.data-table th,
                table.data-table td {{
                    padding: 4px 6px;
                }}
            }}
        </style>
        """

    def _generate_js(self) -> str:
        """生成表格下载脚本 - 零依赖纯JS实现，PNG使用Canvas2D跨浏览器渲染"""
        return """
        <script>
        (function() {
            function getTable(btn) {
                var wrapper = btn.closest('.table-wrapper');
                return wrapper ? wrapper.querySelector('table.data-table') : null;
            }

            function cloneWithStyles(node) {
                var clone = node.cloneNode(true);
                var orig = node.querySelectorAll('*');
                var cln = clone.querySelectorAll('*');
                for (var i = 0; i < orig.length; i++) {
                    var style = window.getComputedStyle(orig[i]);
                    var el = cln[i];
                    el.style.cssText = '';
                    for (var j = 0; j < style.length; j++) {
                        var prop = style[j];
                        el.style.setProperty(prop, style.getPropertyValue(prop), style.getPropertyPriority(prop));
                    }
                }
                var rootStyle = window.getComputedStyle(node);
                clone.style.cssText = '';
                for (var k = 0; k < rootStyle.length; k++) {
                    var p = rootStyle[k];
                    clone.style.setProperty(p, rootStyle.getPropertyValue(p), rootStyle.getPropertyPriority(p));
                }
                return clone;
            }

            function tableToSvg(table) {
                var clone = cloneWithStyles(table);
                clone.setAttribute('xmlns', 'http://www.w3.org/1999/xhtml');
                var w = table.offsetWidth;
                var h = table.offsetHeight;
                var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                svg.setAttribute('width', w);
                svg.setAttribute('height', h);
                svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
                var fo = document.createElementNS('http://www.w3.org/2000/svg', 'foreignObject');
                fo.setAttribute('width', '100%');
                fo.setAttribute('height', '100%');
                fo.appendChild(clone);
                svg.appendChild(fo);
                return new XMLSerializer().serializeToString(svg);
            }

            function renderTableToCanvas(table, scale) {
                scale = scale || 2;
                var rows = Array.from(table.rows);
                var tempCanvas = document.createElement('canvas');
                var tctx = tempCanvas.getContext('2d');
                var colCount = 0;
                rows.forEach(function(row) { colCount = Math.max(colCount, row.cells.length); });
                var colWidths = new Array(colCount).fill(0);
                var rowHeights = [];
                rows.forEach(function(row) {
                    var maxH = 0;
                    Array.from(row.cells).forEach(function(cell, c) {
                        var style = window.getComputedStyle(cell);
                        var px = parseFloat(style.paddingLeft) + parseFloat(style.paddingRight);
                        var py = parseFloat(style.paddingTop) + parseFloat(style.paddingBottom);
                        tctx.font = style.font || '13px sans-serif';
                        var text = cell.textContent || '';
                        var lines = text.split(/\n/);
                        var maxTextWidth = 0;
                        lines.forEach(function(line) {
                            maxTextWidth = Math.max(maxTextWidth, tctx.measureText(line).width);
                        });
                        colWidths[c] = Math.max(colWidths[c], maxTextWidth + px + 8);
                        var fontSize = parseFloat(style.fontSize) || 13;
                        var lineHeight = parseFloat(style.lineHeight) || fontSize * 1.45;
                        maxH = Math.max(maxH, lineHeight * lines.length + py + 8);
                    });
                    rowHeights.push(Math.max(maxH, 26));
                });
                var width = colWidths.reduce(function(a, b) { return a + b; }, 0) + 2;
                var height = rowHeights.reduce(function(a, b) { return a + b; }, 0) + 2;
                var canvas = document.createElement('canvas');
                canvas.width = Math.floor(width * scale);
                canvas.height = Math.floor(height * scale);
                var ctx = canvas.getContext('2d');
                ctx.scale(scale, scale);
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, width, height);
                var y = 1;
                rows.forEach(function(row, r) {
                    var x = 1;
                    var h = rowHeights[r];
                    var isLastRow = r === rows.length - 1;
                    Array.from(row.cells).forEach(function(cell, c) {
                        var w = colWidths[c];
                        var style = window.getComputedStyle(cell);
                        ctx.fillStyle = (style.backgroundColor && style.backgroundColor !== 'rgba(0, 0, 0, 0)') ? style.backgroundColor : '#ffffff';
                        ctx.fillRect(x, y, w, h);
                        ctx.fillStyle = style.color || '#000000';
                        ctx.font = style.font || '13px sans-serif';
                        ctx.textBaseline = 'middle';
                        var padL = parseFloat(style.paddingLeft) || 8;
                        var fontSize = parseFloat(style.fontSize) || 13;
                        var lineHeight = parseFloat(style.lineHeight) || fontSize * 1.45;
                        var text = cell.textContent || '';
                        var lines = text.split(/\n/);
                        var textY = y + h / 2 - (lines.length - 1) * lineHeight / 2 + 1;
                        lines.forEach(function(line, i) {
                            ctx.fillText(line, x + padL, textY + i * lineHeight);
                        });
                        ctx.strokeStyle = isLastRow ? '#999999' : '#cccccc';
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(x, y + h);
                        ctx.lineTo(x + w, y + h);
                        ctx.stroke();
                        x += w;
                    });
                    y += h;
                });
                if (rows.length > 0 && table.tHead && table.tHead.rows.length > 0) {
                    var headerH = 0;
                    for (var i = 0; i < table.tHead.rows.length; i++) {
                        headerH += rowHeights[i];
                    }
                    ctx.strokeStyle = '#000000';
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(1, 1 + headerH);
                    ctx.lineTo(width - 1, 1 + headerH);
                    ctx.stroke();
                }
                return canvas;
            }

            window.downloadTableAsSvg = function(btn) {
                var table = getTable(btn);
                if (!table) return;
                var svgStr = tableToSvg(table);
                var blob = new Blob([svgStr], {type: 'image/svg+xml;charset=utf-8'});
                var url = URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = 'table.svg';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            };

            window.downloadTableAsPng = function(btn) {
                var table = getTable(btn);
                if (!table) return;
                var canvas = renderTableToCanvas(table, 2);
                canvas.toBlob(function(blob) {
                    if (!blob) return;
                    var url = URL.createObjectURL(blob);
                    var a = document.createElement('a');
                    a.href = url;
                    a.download = 'table.png';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                });
            };
        })();
        </script>
        """

    def generate_html(self) -> str:
        """生成完整HTML报告"""
        html_parts = [
            '<!DOCTYPE html>',
            '<html lang="zh-CN">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'    <title>{self.title}</title>',
            self._generate_css(),
            self._generate_js(),
            '</head>',
            '<body>',
            '    <div class="report-container">',
        ]

        # 封面
        html_parts.append(f"""
        <div class="cover">
            <h1>{self.title}</h1>
            <div class="subtitle">{self.subtitle}</div>
            <div class="meta">
                生成时间: {datetime.now().strftime('%Y年%m月%d日')}
            </div>
        </div>
        """)

        # 内容区
        html_parts.append('<div class="content">')

        for section in self.sections:
            tag = f'h{section.level}'
            html_parts.append(f'<{tag} class="section-title">{section.title}</{tag}>')
            content_html = self._parse_markdown_content(section.content)
            html_parts.append(f'<div class="section-content">{content_html}</div>')

        html_parts.append('</div>')  # 结束内容区

        # 页脚
        html_parts.append(f"""
        <div class="footer">
            本报告由战略分析系统自动生成 | 数据截止日期: {datetime.now().strftime('%Y-%m-%d')}
        </div>
        """)

        html_parts.extend([
            '    </div>',  # 结束report-container
            '</body>',
            '</html>',
        ])

        return '\n'.join(html_parts)

    def save(self, filepath: str):
        """保存HTML文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate_html())


class ReportConverter:
    """Markdown报告转HTML转换器"""

    @staticmethod
    def from_markdown(md_content: str, title: str = "战略分析报告", subtitle: str = "") -> HTMLReportGenerator:
        """从Markdown内容创建HTML报告"""
        generator = HTMLReportGenerator(title, subtitle)

        # 解析Markdown章节 - 匹配 ## 标题和内容
        section_pattern = r'^(##+)\s+(.+?)\n(.*?)(?=^##+|\Z)'
        matches = re.finditer(section_pattern, md_content, re.MULTILINE | re.DOTALL)

        for match in matches:
            hashes = match.group(1)
            title_text = match.group(2).strip()
            content = match.group(3).strip()

            # 确定标题级别
            level = len(hashes)

            generator.add_section(title_text, level, content)

        # 如果没有解析到章节，把整个内容作为一章
        if not generator.sections:
            generator.add_section("报告正文", 2, md_content)

        return generator

    @staticmethod
    def convert_file(md_filepath: str, html_filepath: str):
        """转换Markdown文件为HTML文件"""
        with open(md_filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # 从文件内容提取标题
        title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
        title = title_match.group(1) if title_match else "战略分析报告"

        generator = ReportConverter.from_markdown(md_content, title)
        generator.save(html_filepath)
        return html_filepath


class ReportGenerator:
    """Markdown报告生成器 - 原始功能保留"""

    def __init__(self, industry: str, user_type: str = "full"):
        self.industry = industry
        self.user_type = user_type
        self.sections = []
        self.data = {}

    def set_data(self, data: Dict):
        """设置分析数据"""
        self.data = data

    def generate_executive_summary(self) -> str:
        """生成执行摘要"""
        return f"""## 执行摘要

2024年中国云计算市场在AI智算需求的推动下继续保持高速增长，整体规模突破八千亿大关。头部阵营中，阿里云稳居首位，华为云增速领先，而运营商云依托政策与网络优势持续蚕食政企市场份额。本报告基于中国信通院、IDC、Canalys及上市公司财报等权威数据，系统梳理市场规模、竞争格局、行业结构与关键趋势，并为相关方提供战略参考。

### 核心结论
1. **市场规模突破八千亿元**：2024年中国云计算市场规模达 **¥8,288亿元**，同比增长 **34.4%**，增速显著高于全球平均水平。
2. **AI成为核心增长引擎**：2024年中国AI公有云服务市场规模达 **¥195.9亿元**，同比大增 **55.3%**；公有云SaaS增速反弹至 **68.2%**。
3. **头部格局稳定但分化明显**：阿里云以 **26.1%**（IDC IaaS）/ **36%**（Canalys 整体）稳居第一；华为云 **13.2%** 位居第二，增速领先；天翼云、移动云、腾讯云分列三至五位。
4. **政策红利持续释放**：数字中国2025目标算力规模超 **300 EFLOPS**，东数西算深化推进，绿色算力（PUE≤1.3）成为硬性门槛。

### 关键数据
| 指标 | 数值 | 来源 | 可信度 | 提取方式 | 来源链接 |
|-----|------|-----|-------|---------|---------|
| 市场规模(TAM) | {self.data.get('market_size', '¥8,288亿')} | 中国信通院 | ★★★★★ | WebSearch | [链接](https://www.caict.ac.cn) |
| 年增长率 | {self.data.get('growth_rate', '34.4%')} | 中国信通院 | ★★★★★ | WebSearch | [链接](https://www.caict.ac.cn) |
| 市场集中度(CR5 IaaS) | {self.data.get('cr5', '69.8%')} | IDC 2024 H2 | ★★★★★ | WebSearch | [链接](https://www.idc.com) |
"""

    def generate_industry_structure(self) -> str:
        """生成行业结构分析"""
        return f"""## 行业结构分析（波特五力模型）

### 1. 现有竞争者竞争强度
市场整体增速保持在 **34.4%** 的高位，但基础 IaaS 层增速已回落至 **13.8%**，意味着增量红利逐渐收窄，竞争焦点从规模扩张转向 AI 智算能力与政企解决方案的比拼。IDC 数据显示，CR5 集中度同比下降 1.0 个百分点，说明中腰部厂商在细分领域仍有一定突围空间，但价格战与贴身竞争依然激烈。综合判断，现有竞争者竞争强度较高。

**评分：** ★★★★☆（高强度）

### 2. 新进入者威胁
云计算属于典型的资本与技术密集型行业。超大规模数据中心建设、智算中心投资均需百亿级资金；同时，大模型训练/推理框架、软硬一体化优化、全栈安全合规能力构成了深厚的技术壁垒。此外，政企客户对云厂商资质与案例积累的要求极高，新进入者难以在短期内建立信任。综合判断，新进入者威胁处于中等偏低水平。

**评分：** ★★★☆☆（中等）

### 3. 替代品威胁
当前主要替代方案包括私有云/混合云部署以及 Serverless 无服务器架构。对于金融、政务等强监管行业，混合云确实是主流选择，但公有云凭借弹性扩展、持续迭代和成本优势，仍占据市场 **75%** 的份额。随着国产化适配与安全合规体系完善，公有云对核心业务的渗透仍在加深。替代品威胁相对有限。

**评分：** ★★☆☆☆（较低）

### 4. 买方议价能力
头部互联网客户集中且迁移成本敏感，议价能力较强；但另一方面，随着 PaaS 与 SaaS 服务深度绑定，客户的整体切换成本在上升。政企客户虽然分散，但更看重解决方案能力与长期服务稳定性，对价格的敏感度低于互联网客户。整体来看，买方议价能力处于中等水平，且随着服务层级上移呈下降趋势。

**评分：** ★★★☆☆（中等）

### 5. 供应商议价能力
AI 训练与推理所需的高端芯片供应高度集中，国际出口管制与国产芯片产能爬坡使得算力资源成为稀缺资产。部分头部云厂商已通过自研芯片（如华为昇腾）或大规模锁单缓解供应压力，但行业整体的供应商议价能力依然偏高。

**评分：** ★★★★☆（较高）

### 综合评估
行业整体吸引力评定为 **中高**。云计算市场具备显著的规模效应与增长潜力，但 IaaS 层的激烈竞争和 AI 芯片供应压力意味着企业必须通过差异化（AI 智算、行业解决方案、生态绑定）来获取可持续的竞争优势。
"""

    def generate_market_sizing(self) -> str:
        """生成市场规模分析"""
        return f"""## 市场规模与增长

### TAM-SAM-SOM 测算

| 层级 | 规模 | 测算方法 | 关键假设 | 来源链接 |
|-----|------|---------|---------|---------|
| TAM (总潜在市场) | {self.data.get('tam', '¥8,288亿')} | 中国信通院宏观统计 | 含公有云、私有云、出海 | [中国信通院](https://www.caict.ac.cn) |
| SAM (可服务市场) | {self.data.get('sam', '¥6,216亿')} | 公有云市场规模 | 公有云占比75% | [中国信通院](https://www.caict.ac.cn) |
| SOM (可获得市场) | {self.data.get('som', '¥2,400亿')} | Top5公有云IaaS占比估算 | 头部厂商可获取的IaaS+PaaS份额 | [IDC](https://www.idc.com) |

### 增长驱动因素
需求端来看，大模型创业公司与传统企业对智算算力的爆发式需求是首要拉动力；与此同时，传统企业数字化转型加速，SaaS 渗透率持续提升，以及中国企业全球化带来的出海云服务需求，共同构成了多元增长引擎。供给端方面，东数西算工程与地方算力补贴有效降低了算力成本，而国产 AI 芯片的快速迭代与算力基础设施的持续扩容，则为市场增长提供了坚实支撑。

### 增长预测
| 年份 | 规模 | 增长率 | 驱动因素 | 来源链接 |
|-----|------|-------|---------|---------|
| 2023 | ¥6,165亿 | 35.5% | 企业数字化、AI需求初现 | [中国信通院](https://www.caict.ac.cn) |
| 2024 | ¥8,288亿 | 34.4% | AI智算爆发、公有云加速 | [中国信通院](https://www.caict.ac.cn) |
| 2025 | ~¥9,500亿 | ~15% | 大模型算力需求 | [Canalys](https://www.canalys.com) |
| 2027 | >¥21,000亿 | - | AI原生技术革新、大模型规模化落地 | [IDC](https://www.idc.com) |
| 2030 | >¥30,000亿 | - | "十五五"期间保持20%以上增长 | [中国信通院](https://www.caict.ac.cn) |
"""

    def generate_competitive_landscape(self) -> str:
        """生成竞争格局分析"""
        return f"""## 竞争格局分析

### 市场集中度与格局类型
从 IDC 2024 下半年数据来看，中国公有云 IaaS 市场 CR5 为 **69.8%**，同比下降 1.0 个百分点，市场仍属于寡头竞争格局，但集中度略有分散。格局类型上，呈现「互联网云龙头 + 全栈 ICT 巨头 + 运营商云」三足鼎立的态势，AI 垂直能力厂商则在细分赛道寻找突破口。

### 战略群组
| 群组 | 代表企业 | 定位特点 | 核心策略 |
|-----|---------|---------|---------|
| 互联网云龙头 | 阿里云、腾讯云 | 互联网基因、生态丰富 | 公有云+AI大模型+平台生态 |
| 全栈ICT巨头 | 华为云 | 政企/制造/金融强、软硬一体 | CloudMatrix AI算力+行业解决方案 |
| 运营商云 | 天翼云、移动云 | 央企/政务/5G边缘 | 国家项目+安全合规+算力网络 |
| AI垂直领军 | 百度智能云 | AI能力深厚 | 大模型即服务（MaaS）+AI公有云 |

### 主要竞争者画像

**阿里云**以 **26.1%** 的公有云 IaaS 份额（IDC）和 **36%** 的整体云基础设施份额（Canalys）稳居中国市场首位。其核心优势在于深厚的电商与互联网基因、通义大模型系列的快速迭代，以及公共云业务持续盈利的能力（Q4 EBITA 利润率约 10%）。近期，阿里巴巴宣布未来三年在云与 AI 基础设施上的投入将超过过去十年的总和，AI 相关产品收入已连续六个季度保持三位数增长。相对短板在于政企市场的客情关系与传统行业交付能力，仍弱于华为与运营商云。

**华为云**在 2024 年全年实现收入 **688.1 亿元**（含内部交易），同比增长 **24.4%**，海外市场增速更超 **50%**。凭借 CloudMatrix AI 算力架构与在制造、金融、政务等行业的深耕，华为云在 IDC 2024 H2 公有云 IaaS 市场中以 **13.2%** 位列第二，Canalys 整体口径份额达 **20%**。其主要挑战在于整体业务目前尚未盈利，2025 年正通过组织调整向 AI 战略聚焦，以实现盈利目标。

**腾讯云**未单独披露云业务收入，其云计算板块纳入「金融科技与企业服务」板块（Q1 收入 **523 亿元**，同比 +7%）。2024 年全年，腾讯在该领域的资本开支高达 **721 亿元**，较 2023 年的 227 亿元大幅跃升，主要用于 GPU 及 AI 基础设施采购。腾讯云在社交、游戏、音视频与 PaaS/SaaS 整合方面具备天然优势，但在 IaaS 基础设施层的份额受到互联网红利见顶与运营商云崛起的双重挤压，IDC 2024 H2 IaaS 排名位列第五。

### 竞争态势演变
当前市场正处于由 **红海增长期向红海存量期过渡** 的阶段，AI 大模型与智算服务成为核心新增量。竞争焦点已从单纯的价格与规模比拼，转向 **AI 智算能力、政企行业解决方案深度、生态绑定强度** 的立体竞争。未来 2–3 年，头部厂商将持续加码 AI 基础设施投资，而运营商云依托政策、网络与央企身份，有望在政务与关键行业市场进一步扩大存在感。
"""

    def generate_trend_analysis(self) -> str:
        """生成趋势分析 - PESTEL以表格整合"""
        return f"""## 关键趋势分析（PESTEL）

宏观环境层面，数字中国战略的深入推进使算力成为国家级基础设施，东数西算工程从布局走向全国一体化调度，直接利好具备政企项目承接能力的头部云厂商与运营商。经济上，数字经济核心产业占 GDP 比重目标突破 10%，企业数字化支出保持刚性增长。社会与技术层面，远程办公常态化叠加 AI 应用（智能体、Copilot）的快速普及，推动 SaaS 与 PaaS 服务消费持续升级；大模型训推需求爆发、国产芯片替代加速，使得技术领先者在竞争中获得结构性优势。环境层面，数据中心 PUE 要求趋严（新建不高于 1.3），西部地区凭借绿电与气候优势成为智算中心建设热土。法律层面，数据安全法、个人信息保护法及生成式 AI 管理办法已全面落地，跨境数据流动与算法备案监管日趋严格，合规能力成为云服务商的必修课。

### PESTEL 综合评估表

| 维度 | 现状 | 趋势 | 影响 |
|-----|------|------|------|
| 政治环境 (Political) | 数字中国战略深入推进，算力成为国家基础设施 | 东数西算深化，算力一体化调度 | 有利于头部云厂商与运营商承接国家级项目 |
| 经济环境 (Economic) | 数字经济核心产业占GDP比重目标>10% | 企业数字化支出持续增加 | 云服务作为数字化底座需求刚性增长 |
| 社会环境 (Social) | 远程办公、在线教育常态化 | AI应用（智能体、Copilot）快速普及 | 推动SaaS与PaaS层服务消费升级 |
| 技术环境 (Technological) | 大模型训练推理需求爆发，国产芯片替代加速 | AI原生云计算、Serverless、边缘计算演进 | 技术领先者（阿里、华为）获得结构性优势 |
| 环境因素 (Environmental) | 数据中心PUE要求趋严（≤1.3） | 绿电占比要求提升（枢纽节点≥80%） | 西部绿色算力中心价值凸显，成本结构变化 |
| 法律环境 (Legal) | 数据安全法、个人信息保护法、生成式AI管理办法已落地 | 跨境数据流动监管收紧，IDC客户数据保护新规出台 | 合规成本上升，国内厂商相对外资云优势扩大 |

### 关键趋势总结
| 趋势 | 紧迫性 | 影响程度 | 确定性 | 应对优先级 |
|-----|-------|---------|-------|-----------|
| AI智算需求爆发 | 高 | 极高 | 高 | P1 |
| 东数西算与绿色算力 | 中 | 高 | 高 | P1 |
| 数据安全与合规趋严 | 高 | 高 | 高 | P1 |
| 出海云服务增长 | 中 | 中 | 中 | P2 |
| 国产芯片替代 | 中 | 高 | 中 | P2 |
"""

    def generate_key_success_factors(self) -> str:
        """生成关键成功因素分析"""
        return f"""## 关键成功因素分析

### 行业CSF识别

在当前阶段，云计算行业的竞争已从基础设施的规模扩张升级为 **AI 智算能力、政企行业解决方案深度、以及生态绑定强度** 的立体竞争。以下三项因素被认为是最关键的成功要素：

**1. AI 智算能力**
大模型训练与推理平台、GPU/自研芯片供应保障、以及 MaaS（模型即服务）的产品化成熟度，直接决定了云厂商能否抓住当前最大增量市场。该能力需要百亿级 AI 基建投资、2–3 年的模型与平台打磨周期，以及分布式训练框架、推理优化与异构算力调度等高技术壁垒。

**2. 政企/行业解决方案**
政务、金融、制造等传统行业的上云进程已进入核心系统迁移阶段，客户不仅需要稳定的基础设施，更需要贴合业务场景的行业 Know-How、混合云架构设计与私有化部署能力。该能力的建立需要 3–5 年的行业案例积累与信任建立，壁垒较高但客户粘性与利润率同样可观。

**3. 生态与渠道绑定**
ISV（独立软件开发商）生态、开发者社区活跃度、以及 SaaS 应用市场的丰富度，决定了云平台能否形成网络效应并提升客户切换成本。生态培育周期通常在 5 年以上，但一旦成型，将成为竞争对手难以复制的护城河。

### CSF优先级排序
| 排序 | CSF | 重要性 | 壁垒 | 紧迫性 |
|-----|-----|-------|-----|-------|
| 1 | AI智算能力 | 极高 | 高 | 高 |
| 2 | 政企/行业解决方案 | 极高 | 高 | 高 |
| 3 | 生态与渠道绑定 | 高 | 中高 | 中 |

### 能力建设建议
**短期（0-6个月）**：评估现有 AI 算力资源与缺口，明确是否具备大模型训练/推理服务能力；梳理重点行业客户清单，聚焦 1–2 个高景气行业深化解决方案。

**中期（6-18个月）**：与头部 AI 芯片厂商（如华为昇腾、寒武纪）建立战略合作，确保算力供应稳定；构建垂直行业 MaaS 平台，将通用大模型能力转化为可落地的行业专用模型。

**长期（18个月+）**：建立自主可控的混合云 + 边缘云全栈技术体系；培育 ISV 与开发者生态，逐步形成平台级网络效应与客户高切换成本。
"""

    def generate_strategic_implications(self) -> str:
        """生成战略启示（已移除建议行动清单）"""
        return f"""## 战略启示

### 机会识别
| 机会 | 描述 | 吸引力 | 可行性 | 时间窗口 | 优先级 |
|-----|------|-------|-------|---------|-------|
| 企业级AI智算服务 | 为大模型创业公司与传统企业提供训练/推理算力与平台 | ★★★★★ | ★★★★☆ | 2024-2027 | P1 |
| 政务/央企云迁移 | 数字政府、央国企信创替代带来的IaaS+PaaS增量 | ★★★★★ | ★★★★☆ | 持续 | P1 |
| 中企出海云服务 | 伴随中国企业全球化，提供跨境云与合规服务 | ★★★★☆ | ★★★☆☆ | 2025-2030 | P2 |

### 风险提示
| 风险 | 描述 | 概率 | 影响 | 紧迫性 | 应对建议 |
|-----|------|-----|------|-------|---------|
| AI芯片供应受限 | 高端GPU出口管制持续，国产芯片产能爬坡不及预期 | 中 | 大 | 高 | 多元化供应商布局，预锁定算力资源 |
| 价格战侵蚀利润 | IaaS同质化竞争下，头部厂商持续降价抢份额 | 高 | 中 | 高 | 提升PaaS/SaaS高毛利业务占比 |
| 合规政策突变 | 数据跨境、生成式AI监管政策进一步收紧 | 中 | 中 | 中 | 建立专职合规团队，提前进行安全评估与算法备案 |

### 战略建议
**定位建议**：若企业具备算力与 AI 平台技术优势，建议聚焦「AI 智算服务商」定位，以大模型训推与 MaaS 为核心切入点；若具备深厚政企关系与行业交付经验，则更适合「行业云解决方案商」定位，通过混合云与私有化部署赚取高毛利。

**竞争策略**：避免在通用 IaaS 层面与阿里云等龙头进行纯价格竞争，应通过深耕垂直行业或特定技术栈（如 AI 推理优化、边缘云、音视频处理）建立差异化壁垒。同时，积极拓展 ISV 合作与 SaaS marketplace，放大服务能力并提升客户切换成本。

**能力建设重点**：短期优先确保 AI 算力层的资源供给与平台产品化；中期着力构建行业大模型微调平台与 Agent 开发环境，降低企业客户的 AI 应用门槛；长期则需完善政企级安全合规体系与贴身交付服务能力，实现从基础设施提供商到数字化转型伙伴的跃迁。
"""

    def generate_full_report(self) -> str:
        """生成完整报告"""
        sections = [
            f"# {self.industry} 战略分析报告",
            f"\n> 报告生成时间: {datetime.now().strftime('%Y年%m月%d日')}",
            f"> 分析框架: 麦肯锡战略分析方法论\n",
            self.generate_executive_summary(),
            "## 数据溯源与可信度说明\n\n| 数据项 | 数值 | 来源 | 发布时间 | 可信度 | 提取方式 | 来源链接 |\n|-------|------|-----|---------|-------|---------|---------|\n| 中国云计算市场规模 | ¥8,288亿 | 中国信通院 | 2025-07 | ★★★★★ | WebSearch | [链接](https://www.caict.ac.cn) |\n| 公有云IaaS市场份额 | CR5=69.8% | IDC | 2025-04 | ★★★★★ | WebSearch | [链接](https://www.idc.com) |\n| 云基础设施市场份额 | 阿里36%/华为20%/腾讯15% | Canalys | 2025-01 | ★★★★★ | WebSearch | [链接](https://www.canalys.com) |\n| AI公有云市场规模 | ¥195.9亿 | IDC | 2025-08 | ★★★★★ | WebSearch | [链接](https://www.idc.com) |\n| 阿里云Q4营收 | ¥317.42亿 | 阿里巴巴财报 | 2025-02 | ★★★★★ | WebSearch | [链接](https://www.alibabagroup.com) |\n| 华为云全年收入 | ¥688.1亿 | 华为2024年报 | 2025-03 | ★★★★★ | WebSearch | [链接](https://www.huawei.com) |",
            self.generate_industry_structure(),
            self.generate_market_sizing(),
            self.generate_competitive_landscape(),
            self.generate_trend_analysis(),
            self.generate_key_success_factors(),
            self.generate_strategic_implications(),
            "## 附录\n\n### 数据来源\n\n1. 中国信息通信研究院《云计算蓝皮书（2025年）》\n2. IDC《中国公有云服务市场（2024下半年）跟踪》\n3. IDC《中国AI公有云服务市场份额，2024》\n4. Canalys 中国云基础设施市场季度报告（2024 Q4）\n5. 阿里巴巴集团2025财年第三季度财报\n6. 华为《2024年年度报告》\n7. 腾讯控股2024年第一季度财报\n8. 国家数据局、中国政府网政策文件\n\n### 分析方法说明\n\n- **波特五力模型**：评估行业竞争结构与盈利潜力。\n- **TAM-SAM-SOM**：测算市场层级与可触达空间。\n- **PESTEL**：系统分析宏观环境对行业的影响。\n- **CSF分析**：识别行业关键成功因素并评估能力差距。\n\n### 免责声明\n\n> 本报告基于公开数据分析生成，仅供参考。数据存在时效性和完整性局限，\n> 不同机构统计口径可能存在差异。重大决策请咨询专业顾问。",
        ]

        return "\n\n---\n\n".join(sections)

    def save_report(self, filepath: str):
        """保存Markdown报告到文件"""
        report = self.generate_full_report()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Markdown报告已保存至: {filepath}")

    def generate_html_report(self, html_filepath: str = None) -> str:
        """生成并保存HTML格式的报告"""
        if html_filepath is None:
            html_filepath = f"{self.industry}_report.html"

        md_content = self.generate_full_report()
        html_generator = ReportConverter.from_markdown(
            md_content,
            title=f"{self.industry} 战略分析报告",
            subtitle="基于2024-2025年权威数据的竞争格局与战略研判"
        )
        html_generator.save(html_filepath)
        print(f"HTML报告已保存至: {html_filepath}")
        return html_filepath


def quick_generate(industry: str, output_path: Optional[str] = None,
                   html_output: Optional[str] = None) -> Dict[str, str]:
    """快速生成报告模板（支持双格式输出）"""
    generator = ReportGenerator(industry)

    result = {}

    # Markdown报告
    report = generator.generate_full_report()
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Markdown报告模板已生成: {output_path}")
        result['markdown'] = output_path

    # HTML报告
    if html_output:
        html_path = generator.generate_html_report(html_output)
        result['html'] = html_path

    return result


def generate_html_report(md_content: str, title: str = "战略分析报告",
                        subtitle: str = "", output_path: str = None) -> str:
    """从Markdown内容生成HTML报告"""
    generator = ReportConverter.from_markdown(md_content, title, subtitle)

    if output_path:
        generator.save(output_path)
        return output_path

    return generator.generate_html()


def convert_report(md_filepath: str, html_filepath: str = None) -> str:
    """转换Markdown报告为HTML"""
    if html_filepath is None:
        html_filepath = md_filepath.replace('.md', '.html')

    ReportConverter.convert_file(md_filepath, html_filepath)
    return html_filepath


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        industry = sys.argv[1]
        md_output = sys.argv[2] if len(sys.argv) > 2 else f"{industry}_report.md"
        html_output = sys.argv[3] if len(sys.argv) > 3 else md_output.replace('.md', '.html')

        quick_generate(industry, md_output, html_output)
    else:
        print("用法: python report_generator.py '行业名称' [md输出文件] [html输出文件]")
        print("示例: python report_generator.py '新能源汽车' report.md report.html")

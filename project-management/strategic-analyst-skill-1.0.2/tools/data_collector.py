#!/usr/bin/env python3
"""
战略分析数据收集工具
用于系统化收集和整理行业分析数据
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class DataPoint:
    """单个数据点"""
    item: str           # 数据项名称
    value: str          # 数值
    source: str         # 来源
    date: str           # 发布时间
    reliability: int    # 可信度 1-5
    extract_method: str = "直接引用"  # 提取方式：直接引用/PDF提取/网页抓取/OCR识别
    notes: str = ""     # 备注
    source_url: str = ""  # 来源链接

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_markdown_row(self) -> str:
        stars = "★" * self.reliability + "☆" * (5 - self.reliability)
        source_display = f"[{self.source}]({self.source_url})" if self.source_url else self.source
        return f"| {self.item} | {self.value} | {source_display} | {self.date} | {stars} | {self.extract_method} | {self.notes} |"


class IndustryDataCollector:
    """行业数据收集器"""

    def __init__(self, industry_name: str):
        self.industry = industry_name
        self.data = {
            "market_size": [],      # 市场规模
            "growth": [],           # 增长率
            "competition": [],      # 竞争格局
            "policy": [],           # 政策法规
            "financing": [],        # 投融资
            "trends": [],           # 趋势数据
            "players": [],          # 主要玩家
        }
        self.collection_log = []
        self.search_results: List[Dict[str, Any]] = []  # 原始搜索记录

    def add_market_size(self, value: str, source: str, date: str,
                        reliability: int, extract_method: str = "直接引用", notes: str = "", source_url: str = ""):
        """添加市场规模数据

        Args:
            extract_method: 提取方式（直接引用/PDF提取/网页抓取/OCR识别）
            source_url: 来源链接
        """
        dp = DataPoint("市场规模", value, source, date, reliability, extract_method, notes, source_url)
        self.data["market_size"].append(dp)
        self._log(f"添加市场规模: {value} from {source} ({extract_method})")

    def add_growth_rate(self, value: str, source: str, date: str,
                        reliability: int, extract_method: str = "直接引用", notes: str = "", source_url: str = ""):
        """添加增长率数据

        Args:
            extract_method: 提取方式（直接引用/PDF提取/网页抓取/OCR识别）
            source_url: 来源链接
        """
        dp = DataPoint("增长率", value, source, date, reliability, extract_method, notes, source_url)
        self.data["growth"].append(dp)
        self._log(f"添加增长率: {value} from {source} ({extract_method})")

    def add_competition_data(self, item: str, value: str, source: str,
                             date: str, reliability: int, extract_method: str = "直接引用", notes: str = "", source_url: str = ""):
        """添加竞争格局数据

        Args:
            extract_method: 提取方式（直接引用/PDF提取/网页抓取/OCR识别）
            source_url: 来源链接
        """
        dp = DataPoint(item, value, source, date, reliability, extract_method, notes, source_url)
        self.data["competition"].append(dp)
        self._log(f"添加竞争数据: {item}={value} ({extract_method})")

    def add_player(self, name: str, description: str, source: str,
                   date: str, reliability: int, extract_method: str = "直接引用", source_url: str = ""):
        """添加主要玩家信息

        Args:
            extract_method: 提取方式（直接引用/PDF提取/网页抓取/OCR识别）
            source_url: 来源链接
        """
        dp = DataPoint(name, description, source, date, reliability, extract_method, source_url=source_url)
        self.data["players"].append(dp)
        self._log(f"添加玩家: {name} ({extract_method})")

    def add_policy(self, policy_name: str, content: str, source: str,
                   date: str, reliability: int, extract_method: str = "直接引用", impact: str = "", source_url: str = ""):
        """添加政策法规

        Args:
            extract_method: 提取方式（直接引用/PDF提取/网页抓取/OCR识别）
            source_url: 来源链接
        """
        notes = f"影响: {impact}" if impact else ""
        dp = DataPoint(policy_name, content, source, date, reliability, extract_method, notes, source_url)
        self.data["policy"].append(dp)
        self._log(f"添加政策: {policy_name} ({extract_method})")

    def add_financing(self, company: str, amount: str, round_type: str,
                      source: str, date: str, reliability: int, extract_method: str = "直接引用", source_url: str = ""):
        """添加融资事件

        Args:
            extract_method: 提取方式（直接引用/PDF提取/网页抓取/OCR识别）
            source_url: 来源链接
        """
        value = f"{amount} ({round_type})"
        dp = DataPoint(company, value, source, date, reliability, extract_method, source_url=source_url)
        self.data["financing"].append(dp)
        self._log(f"添加融资: {company} {amount} ({extract_method})")

    def generate_summary_table(self) -> str:
        """生成汇总表格"""
        lines = [f"## {self.industry} 数据收集汇总\n"]
        lines.append(f"> 收集时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

        for category, datapoints in self.data.items():
            if not datapoints:
                continue

            category_names = {
                "market_size": "市场规模",
                "growth": "增长数据",
                "competition": "竞争格局",
                "policy": "政策法规",
                "financing": "投融资",
                "trends": "趋势数据",
                "players": "主要玩家",
            }

            lines.append(f"\n### {category_names.get(category, category)}\n")
            lines.append("| 数据项 | 数值 | 来源 | 发布时间 | 可信度 | 提取方式 | 备注 |")
            lines.append("|-------|------|-----|---------|-------|---------|-----|")

            for dp in datapoints:
                lines.append(dp.to_markdown_row())

            lines.append("")

        return "\n".join(lines)

    def add_search_result(self, query: str, source: str, url: str,
                          snippet: str, tool_used: str = "WebSearch"):
        """添加原始搜索记录"""
        record = {
            "query": query,
            "source": source,
            "url": url,
            "snippet": snippet,
            "tool_used": tool_used,
            "timestamp": datetime.now().isoformat(),
        }
        self.search_results.append(record)
        self._log(f"记录搜索: [{tool_used}] {query} -> {source}")

    def generate_data_collection_md(self) -> str:
        """生成数据收集原始记录 Markdown"""
        lines = [
            f"# {self.industry} 数据收集原始记录",
            "",
            f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 1. 搜索记录",
            "",
        ]

        if self.search_results:
            lines.append("| 搜索关键词 | 工具 | 来源 | URL | 原始摘要 | 记录时间 |")
            lines.append("|-----------|-----|------|-----|---------|---------|")
            for r in self.search_results:
                snippet = r['snippet'].replace('|', '\\|').replace('\n', ' ')
                url = r['url'].replace('|', '\\|')
                query = r['query'].replace('|', '\\|')
                source = r['source'].replace('|', '\\|')
                tool = r['tool_used'].replace('|', '\\|')
                ts = r['timestamp'][:19]
                lines.append(f"| {query} | {tool} | {source} | [{url}]({url}) | {snippet[:80]}{'...' if len(snippet) > 80 else ''} | {ts} |")
        else:
            lines.append("> 暂无搜索记录")

        lines.extend([
            "",
            "---",
            "",
            "## 2. 整理后数据",
            "",
        ])
        lines.append(self.generate_summary_table())

        lines.extend([
            "",
            "---",
            "",
            "## 3. 未验证 / 待确认数据",
            "",
        ])

        pending = []
        for category, datapoints in self.data.items():
            for dp in datapoints:
                if dp.reliability <= 2 or not dp.source_url:
                    pending.append(dp)

        if pending:
            lines.append("| 数据项 | 数值 | 来源 | 可信度 | 缺失/待确认项 |")
            lines.append("|-------|------|-----|-------|--------------|")
            for dp in pending:
                stars = "★" * dp.reliability + "☆" * (5 - dp.reliability)
                issue = "来源链接缺失" if not dp.source_url else "可信度较低，建议复核"
                lines.append(f"| {dp.item} | {dp.value} | {dp.source} | {stars} | {issue} |")
        else:
            lines.append("> 所有关键数据均已标注来源链接并通过可信度校验。")

        lines.append("")
        return "\n".join(lines)

    def save_data_collection_md(self, filepath: str = "data_collection.md"):
        """保存数据收集原始记录到文件"""
        md_content = self.generate_data_collection_md()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"数据收集原始记录已保存至: {filepath}")

    def export_json(self, filepath: str):
        """导出为JSON"""
        export_data = {
            "industry": self.industry,
            "export_time": datetime.now().isoformat(),
            "data": {
                k: [dp.to_dict() for dp in v]
                for k, v in self.data.items()
            },
            "log": self.collection_log
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

    def _log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.collection_log.append(f"[{timestamp}] {message}")


class SearchQueryGenerator:
    """搜索关键词生成器"""

    def __init__(self, industry: str):
        self.industry = industry

    def generate_queries(self) -> Dict[str, List[str]]:
        """生成各维度的搜索关键词"""
        return {
            "市场规模": [
                f"{self.industry} 市场规模 2024",
                f"{self.industry} 市场容量 TAM",
                f"{self.industry} 行业报告 艾瑞/易观",
            ],
            "竞争格局": [
                f"{self.industry} 竞争格局 CR5",
                f"{self.industry} 市场份额 排名",
                f"{self.industry} 主要企业",
            ],
            "发展趋势": [
                f"{self.industry} 发展趋势 2024",
                f"{self.industry} 前景预测",
                f"{self.industry} 投资热度",
            ],
            "政策法规": [
                f"{self.industry} 政策 2024",
                f"{self.industry} 监管",
                f"{self.industry} 国家标准",
            ],
            "融资动态": [
                f"{self.industry} 融资 2024",
                f"{self.industry} 投资事件",
                f"{self.industry} 独角兽",
            ],
        }

    def print_search_plan(self):
        """打印搜索计划"""
        queries = self.generate_queries()
        print(f"\n=== {self.industry} 行业数据收集搜索计划 ===\n")
        for category, query_list in queries.items():
            print(f"\n【{category}】")
            for i, q in enumerate(query_list, 1):
                print(f"  {i}. {q}")
        print("\n" + "="*50)


def create_collector(industry: str) -> IndustryDataCollector:
    """创建数据收集器（便捷函数）"""
    return IndustryDataCollector(industry)


def generate_search_plan(industry: str):
    """生成搜索计划（便捷函数）"""
    generator = SearchQueryGenerator(industry)
    generator.print_search_plan()


if __name__ == "__main__":
    # 示例用法
    import sys

    if len(sys.argv) > 1:
        industry = sys.argv[1]
        generate_search_plan(industry)
    else:
        print("用法: python data_collector.py '行业名称'")
        print("示例: python data_collector.py '新能源汽车'")

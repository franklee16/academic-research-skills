"""
PPT Agent 文本解析器 - 终版
修复：1) 图注释行不再作为文字渲染  2) 编号统一  3) 空白页保护
新增：scene 参数支持推免/文献汇报两种场景的关键词表
"""

import re
from typing import Dict, List, Optional, Tuple
from ..models import (
    ParsedData,
    CoverData,
    TOCItem,
    SectionData,
    ContentListData,
    ContentDetailData,
    TimelineData,
    TimelineEvent,
    HeaderInfo,
    FooterInfo,
    ListItem,
    Page,
    FigurePlaceholder,
    PAGE_TYPE_SECTION,
    PAGE_TYPE_CONTENT_LIST,
    PAGE_TYPE_CONTENT_DETAIL,
    PAGE_TYPE_TIMELINE,
)

# 图注释正则（匹配 <!-- 图: xxx | path=yyy | position=zzz -->）
FIG_RE = re.compile(
    r"<!--\s*图[：:]?\s*([^|]+)\|\s*path=([^|]*)\|\s*position=(\w+)\s*-->"
)

# 推免答辩场景关键词
_RESUME_CONTENT_TYPES = {
    "教育": "content-list",
    "科研": "content-detail",
    "获奖": "content-list",
    "学生工作": "content-list",
    "优势": "content-list",
    "计划": "timeline",
    "未来": "timeline",
    "规划": "timeline",
}

# 文献汇报场景关键词
_ACADEMIC_CONTENT_TYPES = {
    "背景": "content-detail",
    "动机": "content-detail",
    "引言": "content-detail",
    "方法": "content-detail",
    "实验": "content-detail",
    "材料": "content-detail",
    "合成": "content-detail",
    "表征": "content-detail",
    "性能": "content-detail",
    "结果": "content-list",
    "讨论": "content-detail",
    "分析": "content-detail",
    "应用": "content-list",
    "总结": "content-list",
    "展望": "timeline",
    "摘要": "content-list",
    # 也兼容推免关键词
    "教育": "content-list",
    "科研": "content-detail",
    "获奖": "content-list",
    "学生工作": "content-list",
    "优势": "content-list",
    "计划": "timeline",
    "未来": "timeline",
    "规划": "timeline",
}


class TextParser:
    SUPPORTED_CONTENT_TYPES = _RESUME_CONTENT_TYPES  # 保持向后兼容

    def __init__(self, config=None, scene: str = "推免"):
        """
        Args:
            config: 配置对象
            scene: 场景类型，"推免" 或 "文献汇报"。
                   "文献汇报" 会启用更多学术关键词（背景/方法/结果/讨论等）。
        """
        self.config = config
        self.parsed_data = ParsedData()
        self.warnings: List[str] = []
        # 根据场景选择关键词表
        if scene == "文献汇报":
            self.content_types = _ACADEMIC_CONTENT_TYPES
        else:
            self.content_types = _RESUME_CONTENT_TYPES

    def parse(self, text: str) -> ParsedData:
        text = self._preprocess(text)
        lines = text.strip().split("\n")
        self._parse_meta(lines)
        self._parse_sections(lines)
        return self.parsed_data

    def _preprocess(self, text: str) -> str:
        if text.strip().startswith("{"):
            try:
                import json

                return self._convert_json_to_text(json.loads(text))
            except Exception:
                pass
        if text.strip().startswith("---"):
            try:
                import yaml

                data = yaml.safe_load(text)
                if data:
                    return self._convert_json_to_text(data)
            except Exception:
                pass
        return text

    def _convert_json_to_text(self, data: Dict) -> str:
        lines = []
        if "meta" in data:
            for key, value in data["meta"].items():
                if value:
                    lines.append(f"{key}: {value}")
        if "sections" in data:
            for i, section in enumerate(data["sections"], 1):
                lines.append(f"{i}. {section.get('title', '')}")
                for item in section.get("content", []):
                    lines.append(f"- {item}")
        return "\n".join(lines)

    def validate(self, data: ParsedData) -> List[str]:
        warnings = []
        if not data.meta.title:
            warnings.append("缺少标题")
        if not data.meta.author:
            warnings.append("缺少申请人")
        if len(data.sections) == 0:
            warnings.append("未检测到任何章节内容")
        self.warnings = warnings
        return warnings

    def _parse_meta(self, lines: List[str]):
        meta = CoverData()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ":" in line or "：" in line:
                sep = ":" if ":" in line else "："
                key, value = line.split(sep, 1)
                key = key.strip().lower()
                value = value.strip()
                if "主题" in key or "标题" in key:
                    meta.title = value
                elif (
                    "申请人" in key
                    or "汇报人" in key
                    or "姓名" in key
                    or "author" in key
                ):
                    meta.author = value
                elif "导师" in key or "指导" in key:
                    meta.advisor = value
                elif "方向" in key:
                    meta.direction = value
                elif "时间" in key or "日期" in key:
                    meta.date = value
        self.parsed_data.meta = meta

    def _parse_sections(self, lines: List[str]):
        current_section = None
        current_content = []
        section_index = 0

        for line in lines:
            line_s = line.strip()
            if not line_s:
                continue
            if self._is_meta_line(line_s):
                continue
            if self._is_section_header(line_s):
                if current_section is not None:
                    section_index += 1
                    self._add_section(current_section, current_content, section_index)
                current_section = self._parse_section_header(line_s)
                current_content = []
            elif current_section is not None:
                current_content.append(line_s)

        if current_section is not None:
            section_index += 1
            self._add_section(current_section, current_content, section_index)

    def _is_meta_line(self, line: str) -> bool:
        meta_keywords = [
            "主题",
            "标题",
            "申请人",
            "汇报人",
            "姓名",
            "导师",
            "指导",
            "方向",
            "时间",
            "日期",
        ]
        for kw in meta_keywords:
            if (
                line.startswith(kw)
                and len(line) > len(kw)
                and line[len(kw)] in (":", "：")
            ):
                return True
        return False

    def _is_section_header(self, line: str) -> bool:
        patterns = [
            r"^Part\s*\d+",
            r"^\d+\.\s*\S+",
            r"^第[一二三四五六七八九十\d]+部分",
        ]
        return any(re.match(p, line) for p in patterns)

    def _parse_section_header(self, line: str) -> SectionData:
        section = SectionData()
        m = re.match(r"^(\d+)\.\s*(.+)", line)
        if m:
            section.part_num = m.group(1)
            section.part_title = m.group(2).strip()
        m2 = re.match(r"Part\s*(\d+)\s*[:\：]?\s*(.*)", line, re.IGNORECASE)
        if m2:
            section.part_num = m2.group(1)
            section.part_title = m2.group(2).strip()
        m3 = re.match(r"第([一二三四五六七八九十\d]+)部分[:\：]?\s*(.*)", line)
        if m3:
            section.part_title = m3.group(2).strip()
        if not section.part_title:
            section.part_title = line.strip()
        return section

    def _add_section(self, section: SectionData, content: List[str], index: int):
        section.part_num = str(index)  # 统一编号

        # 分离图注释行 vs 正文行
        text_lines = []
        figures = []
        for line in content:
            m = FIG_RE.match(line.strip())
            if m:
                figures.append(
                    FigurePlaceholder(
                        label=m.group(1).strip(),
                        path=m.group(2).strip(),
                        position=m.group(3).strip(),
                        caption=m.group(1).strip(),
                        fig_type="figure",
                    )
                )
            else:
                text_lines.append(line)

        # 判断页面类型
        section_title = section.part_title.lower()
        page_type = "content-list"
        for keyword, type_name in self.content_types.items():
            if keyword in section_title:
                page_type = type_name
                break

        if text_lines:
            if self._is_timeline_content(text_lines):
                page_type = "timeline"
            elif self._is_detail_content(text_lines):
                page_type = "content-detail"

        # 构建 data
        if page_type == "content-detail":
            data = self._parse_detail_content(section.part_title, text_lines)
            if isinstance(data, ContentListData):
                page_type = "content-list"
        elif page_type == "timeline":
            data = self._parse_plan_content(section.part_title, text_lines)
            if isinstance(data, ContentListData):
                page_type = "content-list"
        else:
            data = self._parse_list_content(section.part_title, text_lines)

        # 注入 part_num + figures
        try:
            data.part_num = str(index)
        except AttributeError:
            pass
        try:
            data.figures = figures
        except AttributeError:
            pass

        self.parsed_data.sections.append(
            Page(
                page_type="section",
                data=SectionData(part_num=str(index), part_title=section.part_title),
            )
        )
        self.parsed_data.sections.append(Page(page_type=page_type, data=data))

    def _is_timeline_content(self, content: List[str]) -> bool:
        for line in content:
            if re.search(r"20\d{2}[年\-/]", line):
                return True
            if re.search(r"第[一二三四五]年|研[一二三]|博[一二三四]", line):
                return True
        return False

    def _is_detail_content(self, content: List[str]) -> bool:
        detail_keywords = [
            "研究",
            "项目",
            "成果",
            "背景",
            "要点",
            "发表",
            "论文",
            "专利",
        ]
        for line in content:
            for kw in detail_keywords:
                if kw in line:
                    return True
        return False

    def _parse_list_content(self, title: str, content: List[str]) -> ContentListData:
        data = ContentListData()
        data.title = title
        data.subtitle = self.parsed_data.meta.author
        for line in content:
            line = re.sub(r"^[\*\-\◆\●\■\➢]+\s*", "", line.strip())
            if line and not FIG_RE.match(line):
                data.items.append(ListItem(text=line))
        return data

    def _parse_detail_content(
        self, title: str, content: List[str]
    ) -> ContentDetailData:
        data = ContentDetailData()
        data.title = title
        for line in content:
            line = re.sub(r"^[\*\-\◆\●\■\➢]+\s*", "", line.strip())
            if not line or FIG_RE.match(line):
                continue
            if any(
                kw in line for kw in ["结论", "发现", "成效", "验证", "成功率", "证明"]
            ):
                data.results.append(line)
            else:
                data.points.append(line)
        if not data.points and not data.results:
            fallback = ContentListData()
            fallback.title = title
            fallback.subtitle = self.parsed_data.meta.author
            return fallback
        return data

    def _parse_plan_content(self, title: str, content: List[str]) -> TimelineData:
        data = TimelineData()
        data.title = title
        for line in content:
            line = re.sub(r"^[\*\-\◆\●\■\➢]+\s*", "", line.strip())
            if not line or FIG_RE.match(line):
                continue
            m = re.match(r"(20\d{2}[年\-/]?\d*[年月]?)\s*[:\：\-–—]?\s*(.+)", line)
            if m:
                data.events.append(
                    TimelineEvent(
                        date=m.group(1).strip(),
                        title=m.group(2).split("，")[0][:20],
                        description=m.group(2).strip(),
                    )
                )
                continue
            m2 = re.match(
                r"(第[一二三四五]年|研[一二三]|博[一二三四])\s*[:\：]?\s*(.+)", line
            )
            if m2:
                data.events.append(
                    TimelineEvent(
                        date=m2.group(1),
                        title=m2.group(2)[:20],
                        description=m2.group(2).strip(),
                    )
                )
                continue
            data.events.append(
                TimelineEvent(date="", title=line[:20], description=line)
            )
        if not data.events:
            fallback = ContentListData()
            fallback.title = title
            return fallback
        return data


def parse_user_input(text: str, config=None, scene: str = "推免") -> ParsedData:
    return TextParser(config, scene=scene).parse(text)

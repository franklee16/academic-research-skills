#!/usr/bin/env python3
"""Render a stable LaTeX paper report from metadata and analysis JSON."""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
MAX_GRAPHIC_WIDTH_FRACTION = 0.92
REFERENCE_GRAPHIC_PIXEL_WIDTH = 800
MIN_GRAPHIC_WIDTH_FRACTION = 0.05
UNSAFE_MATH_RE = re.compile(
    r"\\(?:input|include|write|openout|read|catcode|usepackage|documentclass|newcommand|renewcommand|def|gdef|edef|directlua|csname|immediate)\b",
    re.IGNORECASE,
)
META_EVIDENCE_LANGUAGE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"应该.{0,8}放[在到进]"), "不要讨论图表公式应该放在哪里，要直接解释它本身承载的论文内容。"),
    (re.compile(r"而不是.{0,20}(独立|单独|图表|公式|章节|部分)"), "不要写版式安排对比，要把证据自然接入当前论证。"),
    (re.compile(r"(独立|单独).{0,8}(图表|公式|证据).{0,8}(章节|部分|模块)"), "不要提独立证据章节或模块。"),
    (re.compile(r"正好对应"), "不要用“正好对应”解释插入原因，要说明图表公式中的具体元素如何推进论证。"),
    (re.compile(r"讲到.{0,16}(展示|插入|放入|给出)"), "不要写“讲到这里展示”，要把图表公式中的内容写进论述。"),
    (re.compile(r"(这里|此处|下面|接下来|随后).{0,12}(展示|插入|放入|给出)"), "不要写舞台提示式的证据插入语。"),
    (re.compile(r"看完(这|该)?(张|个)?(图|表|公式)"), "不要写报告操作步骤，要直接承接图表公式中的内容继续解释。"),
    (re.compile(r"(如图所示|如下图所示|如下表所示|可以看到)"), "不要把理解任务丢给读者，要直接说出图表中的结构、数字或公式含义。"),
    (re.compile(r"读这(张图|个表|个公式|一公式)"), "不要指导读者读图表公式，要直接解释可观察到的结构、数字或推导作用。"),
    (re.compile(r"作为.{0,8}(证据块|图表块|公式块)"), "不要暴露报告结构或证据块概念。"),
)
GENERIC_EVIDENCE_LANGUAGE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(
            r"^(图|表|公式)\s*[A-Za-z0-9一二三四五六七八九十.\-]*\s*"
            r"(展示|显示|说明|呈现|给出)了?"
            r"(论文|方法|模型|实验|结果|流程|结构|效果|性能|趋势|核心|机制|主要内容)?[。.]?$"
        ),
        "不要只写图表公式在展示什么类别，要写出其中具体的结构、数字、变量、步骤或推理作用。",
    ),
    (
        re.compile(
            r"^(这张图|该图|这个表|该表|这个公式|该公式)"
            r"(展示|显示|说明|呈现|给出)了?"
            r"(论文|方法|模型|实验|结果|流程|结构|效果|性能|趋势|核心|机制|主要内容)?[。.]?$"
        ),
        "不要只写泛化解说句，要把证据中的可观察细节讲出来。",
    ),
)
ABRUPT_EVIDENCE_OPENING_RE = re.compile(
    r"^\s*(图|表|公式)\s*[A-Za-z0-9一二三四五六七八九十.\-]*\s*"
    r"(把|将|是|为|展示|显示|说明|呈现|给出|比较|汇总|列出|报告)"
)
MIN_PRE_EVIDENCE_CONTEXT_CJK_CHARS = 18
MIN_POST_EVIDENCE_CONTEXT_CJK_CHARS = 18
EVIDENCE_BLOCK_TYPES = {"evidence", "figure", "table", "equation", "formula", "proof", "theory"}
PARAGRAPH_BLOCK_TYPES = {"paragraph", "text", "story"}
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))
TEMPLATE_PATH = SCRIPT_DIR.parent / "assets" / "report-template.tex"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} does not contain a JSON object")
    return payload


def first_value(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", []):
            return value
    return None


def contains_cjk(value: str) -> bool:
    return bool(CJK_RE.search(value))


def cjk_char_count(value: str) -> int:
    return len(CJK_RE.findall(value))


def escape_latex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def strip_math_delimiters(expression: str) -> str:
    text = expression.strip()
    delimiter_pairs = ((r"\[", r"\]"), ("$$", "$$"), ("$", "$"))
    changed = True
    while changed:
        changed = False
        for left, right in delimiter_pairs:
            if text.startswith(left) and text.endswith(right) and len(text) > len(left) + len(right):
                text = text[len(left) : -len(right)].strip()
                changed = True
    return text


def braces_are_balanced(expression: str) -> bool:
    depth = 0
    escaped = False
    for char in expression:
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def is_safe_math_expression(expression: str) -> bool:
    if not expression or len(expression) > 1200:
        return False
    if "%" in expression or UNSAFE_MATH_RE.search(expression):
        return False
    return braces_are_balanced(expression)


def raw_to_latex_expression(raw_expression: Any) -> str | None:
    if raw_expression in (None, ""):
        return None
    text = strip_math_delimiters(str(raw_expression))
    if not text:
        return None

    replacements = {
        "≤": r"\le ",
        "≥": r"\ge ",
        "≠": r"\ne ",
        "∑": r"\sum ",
        "∏": r"\prod ",
        "√": r"\sqrt{}",
        "×": r"\times ",
        "÷": r"\div ",
        "±": r"\pm ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"(?<!\\)\bsum(?=\s*[_^{])", r"\\sum", text)
    text = re.sub(r"(?<!\\)\bsum\b", r"\\sum", text)
    text = re.sub(r"(?<!\\)\bprod(?=\s*[_^{])", r"\\prod", text)
    text = re.sub(r"(?<!\\)\bprod\b", r"\\prod", text)
    text = re.sub(r"\barg\s*max\b", r"\\operatorname*{arg\,max}", text, flags=re.IGNORECASE)
    text = re.sub(r"\barg\s*min\b", r"\\operatorname*{arg\,min}", text, flags=re.IGNORECASE)
    text = re.sub(r"\bSmoothL1\b", r"\\operatorname{SmoothL1}", text)
    text = re.sub(r"\bCrossEntropy\b", r"\\operatorname{CrossEntropy}", text)
    text = re.sub(r"\bSSC\b", r"\\operatorname{SSC}", text)
    text = re.sub(r"\bScore\b", r"\\operatorname{Score}", text)
    text = re.sub(r"(?<!\\)_theta\b", r"_\\theta", text)
    text = re.sub(r"(?<!\\)_lambda\b", r"_\\lambda", text)
    text = re.sub(r"(?<!\\)_gamma\b", r"_\\gamma", text)
    text = re.sub(r"(?<!\\)_tau\b", r"_\\tau", text)
    text = re.sub(r"([A-Za-z])_([A-Za-z]{2,})\b", r"\1_{\\mathrm{\2}}", text)
    for greek in ("alpha", "beta", "gamma", "lambda", "theta", "tau", "omega", "mu", "eta"):
        text = re.sub(rf"(?<!\\)\b{greek}\b", rf"\\{greek}", text)

    return text if is_safe_math_expression(text) else None


def latex_math_block(item: dict[str, Any]) -> str:
    expression = item.get("latex_expression")
    latex_expression = strip_math_delimiters(str(expression)) if expression not in (None, "") else None
    if not latex_expression:
        latex_expression = raw_to_latex_expression(item.get("raw_expression"))
    if latex_expression and is_safe_math_expression(latex_expression):
        return "\n".join([r"\begin{equation*}", latex_expression, r"\end{equation*}"])
    raw_expression = str(item.get("raw_expression") or "暂无公式。")
    return "\n".join([r"\begin{quote}", latex_text_block(raw_expression), r"\end{quote}"])


def latex_text_block(text: str) -> str:
    paragraphs = [segment.strip() for segment in text.splitlines() if segment.strip()]
    if not paragraphs:
        return escape_latex("暂无信息。")
    return "\n\n".join(escape_latex(paragraph) for paragraph in paragraphs)


def latex_itemize(items: list[str]) -> str:
    if not items:
        return latex_text_block("暂无信息。")
    lines = [r"\begin{itemize}[leftmargin=*]"]
    for item in items:
        lines.append(rf"\item {escape_latex(item)}")
    lines.append(r"\end{itemize}")
    return "\n".join(lines)


def render_block(value: Any) -> str:
    if value in (None, "", []):
        return latex_text_block("暂无信息。")
    if isinstance(value, str):
        return latex_text_block(value.strip() or "暂无信息。")
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, str):
                text = item.strip()
            else:
                text = json.dumps(item, ensure_ascii=False, sort_keys=True)
            if text:
                lines.append(text)
        return latex_itemize(lines)
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if item in (None, "", []):
                continue
            lines.append(f"{key}: {item}")
        return latex_itemize(lines)
    return latex_text_block(str(value))


def render_chinese_block(value: Any, *, placeholder: str = "暂无信息。") -> str:
    if value in (None, "", []):
        return latex_text_block(placeholder)
    if isinstance(value, str):
        text = value.strip()
        return latex_text_block(text if text and contains_cjk(text) else placeholder)
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, str):
                text = item.strip()
                if text and contains_cjk(text):
                    lines.append(text)
            elif isinstance(item, dict):
                text = json.dumps(item, ensure_ascii=False, sort_keys=True)
                if contains_cjk(text):
                    lines.append(text)
        return latex_itemize(lines) if lines else latex_text_block(placeholder)
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if item in (None, "", []):
                continue
            item_text = str(item)
            if contains_cjk(item_text):
                lines.append(f"{key}: {item_text}")
        return latex_itemize(lines) if lines else latex_text_block(placeholder)
    return latex_text_block(placeholder)


def read_jpeg_dimensions(path: Path) -> tuple[int, int] | None:
    sof_markers = {
        0xC0,
        0xC1,
        0xC2,
        0xC3,
        0xC5,
        0xC6,
        0xC7,
        0xC9,
        0xCA,
        0xCB,
        0xCD,
        0xCE,
        0xCF,
    }
    standalone_markers = set(range(0xD0, 0xD9)) | {0x01}
    try:
        with path.open("rb") as handle:
            if handle.read(2) != b"\xff\xd8":
                return None
            while True:
                prefix = handle.read(1)
                while prefix and prefix != b"\xff":
                    prefix = handle.read(1)
                if not prefix:
                    return None
                marker_byte = handle.read(1)
                while marker_byte == b"\xff":
                    marker_byte = handle.read(1)
                if not marker_byte:
                    return None
                marker = marker_byte[0]
                if marker == 0xD9:
                    return None
                if marker in standalone_markers:
                    continue
                length_bytes = handle.read(2)
                if len(length_bytes) != 2:
                    return None
                segment_length = struct.unpack(">H", length_bytes)[0]
                if segment_length < 2:
                    return None
                payload_length = segment_length - 2
                if marker in sof_markers:
                    payload = handle.read(payload_length)
                    if len(payload) < 5:
                        return None
                    height, width = struct.unpack(">HH", payload[1:5])
                    return (width, height) if width > 0 and height > 0 else None
                handle.seek(payload_length, 1)
    except OSError:
        return None


def read_image_dimensions(asset_path: str | Path) -> tuple[int, int] | None:
    path = Path(asset_path)
    try:
        header = path.read_bytes()[:32]
    except OSError:
        return None

    if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) >= 24 and header[12:16] == b"IHDR":
        width, height = struct.unpack(">II", header[16:24])
        return (width, height) if width > 0 and height > 0 else None
    if header.startswith((b"GIF87a", b"GIF89a")) and len(header) >= 10:
        width, height = struct.unpack("<HH", header[6:10])
        return (width, height) if width > 0 and height > 0 else None
    if header.startswith(b"\xff\xd8"):
        return read_jpeg_dimensions(path)
    return None


def graphics_width_fraction(asset_path: str | Path) -> float:
    dimensions = read_image_dimensions(asset_path)
    if not dimensions:
        return MAX_GRAPHIC_WIDTH_FRACTION
    width_px, _height_px = dimensions
    scaled_fraction = MAX_GRAPHIC_WIDTH_FRACTION * width_px / REFERENCE_GRAPHIC_PIXEL_WIDTH
    return min(MAX_GRAPHIC_WIDTH_FRACTION, max(MIN_GRAPHIC_WIDTH_FRACTION, scaled_fraction))


def latex_graphics_options(asset_path: str | Path) -> str:
    width_fraction = graphics_width_fraction(asset_path)
    return f"width={width_fraction:.2f}\\linewidth,keepaspectratio"


def latex_include_graphics(asset_path: str, caption: str, *, floating: bool = True) -> str:
    path = Path(asset_path).resolve().as_posix()
    options = latex_graphics_options(asset_path)
    if not floating:
        return "\n".join(
            [
                r"\begin{center}",
                rf"\includegraphics[{options}]{{\detokenize{{{path}}}}}",
                rf"\par\small {escape_latex(caption)}",
                r"\end{center}",
            ]
        )
    return "\n".join(
        [
            r"\begin{figure}[H]",
            r"\centering",
            rf"\includegraphics[{options}]{{\detokenize{{{path}}}}}",
            rf"\caption*{{{escape_latex(caption)}}}",
            r"\end{figure}",
        ]
    )


def pick_chinese_text(item: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = item.get(key)
        if isinstance(value, str):
            text = value.strip()
            if text and contains_cjk(text):
                return text
    return None


def latex_subsection(title: str, body: str) -> str:
    return "\n".join([rf"\subsection{{{escape_latex(title)}}}", body]).strip()


def latex_section(title: str, body: str) -> str:
    return "\n".join([rf"\section{{{escape_latex(title)}}}", body]).strip()


def latex_evidence_box(title: str, body: str) -> str:
    return "\n".join(
        [
            rf"\begin{{tcolorbox}}[title={{{escape_latex(title)}}}]",
            body,
            r"\end{tcolorbox}",
        ]
    )


def evidence_title(item: dict[str, Any], default: str = "证据") -> str:
    label = str(item.get("label_zh") or item.get("label") or item.get("label_original") or default)
    caption = pick_chinese_text(item, "caption_zh", "caption")
    if caption and len(caption) <= 48:
        return f"{label}：{caption}"
    return label


def format_visual_evidence(item: dict[str, Any]) -> str:
    title = str(item.get("label_zh") or item.get("label") or item.get("label_original") or "图表证据")
    caption = pick_chinese_text(item, "caption_zh", "caption")
    lines = []
    if item.get("asset_path"):
        lines.append(latex_include_graphics(str(item["asset_path"]), caption or title, floating=False))
    elif caption:
        lines.append(latex_text_block(caption))
    else:
        lines.append(latex_text_block("暂无可展示图表。"))
    return latex_evidence_box(title, "\n\n".join(lines))


def format_equation_evidence(item: dict[str, Any]) -> str:
    title = evidence_title(item, "公式证据")
    parts = [latex_math_block(item)]
    details = []
    role = pick_chinese_text(item, "method_role_zh", "method_role")
    if role:
        details.append(f"作用: {role}")
    derivation = pick_chinese_text(item, "derivation_summary_zh", "derivation_summary")
    if derivation:
        details.append(f"推理/推导说明: {derivation}")
    symbols = item.get("symbol_explanations")
    if isinstance(symbols, dict):
        symbol_lines = [
            f"{key}={value}"
            for key, value in symbols.items()
            if isinstance(value, str) and value.strip()
        ]
        if symbol_lines:
            details.append("符号说明: " + "；".join(symbol_lines))
    if item.get("page") not in (None, ""):
        details.append(f"页码: {item['page']}")
    parts.append(latex_itemize(details or ["暂无信息。"]))
    return latex_evidence_box(title, "\n\n".join(parts))


def format_theory_evidence(item: dict[str, Any]) -> str:
    title = evidence_title(item, "理论证据")
    details = []
    for prefix, keys in (
        ("命题/证明线索", ("statement_summary_zh", "statement_summary", "statement_original")),
        ("证明主线", ("proof_summary_zh", "proof_summary")),
        ("意义", ("importance_zh", "importance")),
    ):
        text = pick_chinese_text(item, *keys)
        if text:
            details.append(f"{prefix}: {text}")
    assumptions = item.get("assumptions")
    if isinstance(assumptions, list):
        zh_assumptions = [
            str(value).strip()
            for value in assumptions
            if str(value).strip() and contains_cjk(str(value))
        ]
        if zh_assumptions:
            details.append("关键假设: " + "；".join(zh_assumptions))
    if item.get("page") not in (None, ""):
        details.append(f"页码: {item['page']}")
    return latex_evidence_box(title, latex_itemize(details or ["暂无信息。"]))


def format_generic_evidence(item: dict[str, Any]) -> str:
    title = evidence_title(item, "证据")
    body = render_chinese_block(
        first_value(
            item.get("body_zh"),
            item.get("summary_zh"),
            item.get("evidence_summary_zh"),
            item.get("body"),
            item.get("summary"),
            item.get("text"),
        )
    )
    return latex_evidence_box(title, body)


def format_evidence_block(item: dict[str, Any]) -> str:
    item_type = str(
        first_value(item.get("type"), item.get("visual_type"), item.get("kind"), "")
    ).lower()
    if item_type in {"figure", "table"} or item.get("asset_path"):
        return format_visual_evidence(item)
    if item_type in {"equation", "formula"} or item.get("latex_expression") or item.get("raw_expression"):
        return format_equation_evidence(item)
    if item_type in {"proof", "theory", "theorem", "lemma", "proposition"} or item.get("proof_summary_zh"):
        return format_theory_evidence(item)
    return format_generic_evidence(item)


def proof_explanations_from_metadata(metadata: dict[str, Any]) -> list[str]:
    items = metadata.get("theoretical_items")
    if not isinstance(items, list):
        return []
    explanations = []
    for item in items:
        if not isinstance(item, dict):
            continue
        text = pick_chinese_text(item, "proof_summary_zh", "statement_summary_zh", "importance_zh")
        if text:
            explanations.append(text)
    return explanations


def flatten_chinese_lines(value: Any) -> list[str]:
    lines = []
    if value in (None, "", []):
        return lines
    if isinstance(value, str):
        text = value.strip()
        if text and contains_cjk(text):
            lines.append(text)
        return lines
    if isinstance(value, list):
        for item in value:
            lines.extend(flatten_chinese_lines(item))
        return lines
    if isinstance(value, dict):
        for key, item in value.items():
            if item in (None, "", []):
                continue
            if isinstance(item, (list, dict)):
                nested = flatten_chinese_lines(item)
                lines.extend(f"{key}: {line}" for line in nested)
                continue
            text = str(item).strip()
            if text and contains_cjk(text):
                lines.append(f"{key}: {text}")
        return lines
    text = str(value).strip()
    if text and contains_cjk(text):
        lines.append(text)
    return lines


def render_chinese_paragraphs(value: Any, *, placeholder: str = "暂无信息。") -> str:
    lines = flatten_chinese_lines(value)
    if not lines:
        return latex_text_block(placeholder)
    return "\n\n".join(latex_text_block(line) for line in lines)


def iter_narrative_text_fields(analysis: dict[str, Any]) -> list[tuple[str, str]]:
    sections = analysis.get("narrative_sections")
    if not isinstance(sections, list):
        return []
    text_fields: list[tuple[str, str]] = []
    for section_index, section in enumerate(sections, start=1):
        if not isinstance(section, dict):
            continue
        blocks = first_value(section.get("blocks"), section.get("content_blocks"))
        if not isinstance(blocks, list):
            continue
        for block_index, block in enumerate(blocks, start=1):
            location = f"narrative_sections[{section_index}].blocks[{block_index}]"
            if isinstance(block, str):
                text_fields.append((location, block))
                continue
            if not isinstance(block, dict):
                continue
            for key in (
                "text_zh",
                "body_zh",
                "summary_zh",
            ):
                value = block.get(key)
                if isinstance(value, str) and value.strip():
                    text_fields.append((f"{location}.{key}", value.strip()))
    return text_fields


def validate_integrated_narrative_language(analysis: dict[str, Any]) -> None:
    findings: list[str] = []
    for location, text in iter_narrative_text_fields(analysis):
        for pattern, guidance in META_EVIDENCE_LANGUAGE_PATTERNS:
            match = pattern.search(text)
            if not match:
                continue
            fragment = match.group(0)
            findings.append(f"{location}: `{fragment}`。{guidance}")
            break
    if not findings:
        return
    message = (
        "analysis.narrative_sections contains meta evidence-placement language. "
        "Rewrite the narrative so figures, tables, and formulas are part of the argument itself.\n"
        + "\n".join(f"- {item}" for item in findings[:10])
    )
    raise ValueError(message)


def block_type(block: Any) -> str:
    if isinstance(block, str):
        return "paragraph"
    if not isinstance(block, dict):
        return ""
    return str(first_value(block.get("type"), block.get("kind"), "paragraph")).lower()


def paragraph_text_from_block(block: Any) -> str | None:
    if isinstance(block, str):
        return block.strip() or None
    if not isinstance(block, dict) or block_type(block) not in PARAGRAPH_BLOCK_TYPES:
        return None
    value = first_value(block.get("text_zh"), block.get("body_zh"), block.get("text"), block.get("body"))
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def iter_narrative_evidence_contexts(analysis: dict[str, Any]) -> list[tuple[str, dict[str, Any], str | None, str | None]]:
    sections = analysis.get("narrative_sections")
    if not isinstance(sections, list):
        return []
    evidence_blocks: list[tuple[str, dict[str, Any], str | None, str | None]] = []
    for section_index, section in enumerate(sections, start=1):
        if not isinstance(section, dict):
            continue
        blocks = first_value(section.get("blocks"), section.get("content_blocks"))
        if not isinstance(blocks, list):
            continue
        for block_index, block in enumerate(blocks, start=1):
            if not isinstance(block, dict):
                continue
            if block_type(block) in EVIDENCE_BLOCK_TYPES:
                location = f"narrative_sections[{section_index}].blocks[{block_index}]"
                before_text = paragraph_text_from_block(blocks[block_index - 2]) if block_index >= 2 else None
                after_text = paragraph_text_from_block(blocks[block_index]) if block_index < len(blocks) else None
                evidence_blocks.append((location, block, before_text, after_text))
    return evidence_blocks


def validate_context_paragraph_specificity(location: str, field_name: str, value: Any, min_cjk_chars: int) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return [
            f"{location}.{field_name}: 缺少相邻的中文整合段落。"
            "`lead_in_zh`/`takeaway_zh` 只作为放置提示，不会直接渲染进报告。"
        ]
    text = value.strip()
    findings: list[str] = []
    if cjk_char_count(text) < min_cjk_chars:
        findings.append(
            f"{location}.{field_name}: `{text}` 过短。请把图、表、公式或证明和上下文写成完整整合段落。"
        )
    for pattern, guidance in GENERIC_EVIDENCE_LANGUAGE_PATTERNS:
        if pattern.search(text):
            findings.append(f"{location}.{field_name}: `{text}`。{guidance}")
            break
    if field_name == "previous_paragraph" and ABRUPT_EVIDENCE_OPENING_RE.search(text):
        findings.append(
            f"{location}.{field_name}: `{text[:80]}` 以图表公式编号开头，读者会感觉证据突然插入。"
            "请先解释必要概念、对比对象、数据集/指标、变量或推导上下文，再插入证据。"
        )
    return findings


def validate_narrative_evidence_depth(analysis: dict[str, Any]) -> None:
    findings: list[str] = []
    for location, _block, before_text, after_text in iter_narrative_evidence_contexts(analysis):
        findings.extend(
            validate_context_paragraph_specificity(
                location,
                "previous_paragraph",
                before_text,
                MIN_PRE_EVIDENCE_CONTEXT_CJK_CHARS,
            )
        )
        findings.extend(
            validate_context_paragraph_specificity(
                location,
                "next_paragraph",
                after_text,
                MIN_POST_EVIDENCE_CONTEXT_CJK_CHARS,
            )
        )
    if not findings:
        return
    message = (
        "analysis.narrative_sections contains evidence blocks that are not integrated into the narrative. "
        "Keep placement hints in lead_in_zh or narrative_plan if useful, but write final report prose as paragraph -> evidence -> paragraph. "
        "The renderer inserts the evidence asset only; it does not render lead_in_zh or takeaway_zh as body text.\n"
        + "\n".join(f"- {item}" for item in findings[:12])
    )
    raise ValueError(message)


def normalize_section_title(section: dict[str, Any], index: int) -> str:
    title = first_value(section.get("title_zh"), section.get("heading_zh"), section.get("title"))
    if isinstance(title, str) and title.strip() and contains_cjk(title):
        return title.strip()
    return f"主线 {index}"


def evidence_identity_keys(item: dict[str, Any]) -> set[str]:
    keys = set()
    for key in ("id", "evidence_id", "label", "label_zh", "label_original"):
        value = item.get(key)
        if value not in (None, ""):
            text = str(value).strip().lower()
            keys.add(text)
            keys.add(re.sub(r"\s+", "", text))
    item_type = first_value(item.get("type"), item.get("visual_type"), item.get("kind"))
    if item_type:
        for key in list(keys):
            keys.add(f"{item_type}:{key}")
    return keys


def collect_evidence_blocks(metadata: dict[str, Any], analysis: dict[str, Any]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []

    def add_many(items: Any, default_type: str) -> None:
        if not isinstance(items, list):
            return
        for item in items:
            if not isinstance(item, dict):
                continue
            block = dict(item)
            block.setdefault("type", default_type)
            blocks.append(block)

    add_many(analysis.get("evidence_blocks"), "evidence")
    add_many(metadata.get("evidence_blocks"), "evidence")
    add_many(first_value(analysis.get("key_figures"), metadata.get("figures")), "figure")
    add_many(first_value(analysis.get("key_tables"), metadata.get("tables")), "table")
    add_many(first_value(analysis.get("key_equations"), metadata.get("equations")), "equation")
    add_many(first_value(analysis.get("proof_items"), metadata.get("theoretical_items")), "proof")
    add_many(metadata.get("theoretical_items"), "proof")

    seen = set()
    unique: list[dict[str, Any]] = []
    for block in blocks:
        identity = tuple(sorted(evidence_identity_keys(block))) or (json.dumps(block, sort_keys=True, ensure_ascii=False),)
        if identity in seen:
            continue
        seen.add(identity)
        unique.append(block)
    return unique


def resolve_evidence_blocks(
    evidence_ids: Any,
    direct_blocks: Any,
    evidence_pool: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    if isinstance(direct_blocks, list):
        resolved.extend(item for item in direct_blocks if isinstance(item, dict))
    elif isinstance(direct_blocks, dict):
        resolved.append(direct_blocks)

    if isinstance(evidence_ids, str):
        requested = [evidence_ids]
    elif isinstance(evidence_ids, list):
        requested = [str(item) for item in evidence_ids if item not in (None, "")]
    else:
        requested = []

    requested_keys = {value.strip().lower() for value in requested}
    requested_keys |= {re.sub(r"\s+", "", value) for value in list(requested_keys)}
    for item in evidence_pool:
        if evidence_identity_keys(item) & requested_keys:
            resolved.append(item)

    seen = set()
    unique: list[dict[str, Any]] = []
    for item in resolved:
        identity = tuple(sorted(evidence_identity_keys(item))) or (json.dumps(item, sort_keys=True, ensure_ascii=False),)
        if identity in seen:
            continue
        seen.add(identity)
        unique.append(item)
    return unique


def render_narrative_content_blocks(
    section: dict[str, Any],
    evidence_pool: list[dict[str, Any]],
) -> str | None:
    content_blocks = first_value(section.get("blocks"), section.get("content_blocks"))
    if not isinstance(content_blocks, list) or not content_blocks:
        return None

    rendered: list[str] = []
    for block in content_blocks:
        if isinstance(block, str):
            if contains_cjk(block):
                rendered.append(latex_text_block(block))
            continue
        if not isinstance(block, dict):
            continue
        current_block_type = block_type(block)

        if current_block_type in PARAGRAPH_BLOCK_TYPES:
            text = first_value(block.get("text_zh"), block.get("body_zh"), block.get("text"), block.get("body"))
            if text:
                rendered.append(render_chinese_paragraphs(text))
            continue

        if current_block_type in EVIDENCE_BLOCK_TYPES:
            evidence = resolve_evidence_blocks(
                first_value(block.get("evidence_id"), block.get("evidence_ids"), block.get("evidence_ref")),
                first_value(block.get("evidence_block"), block.get("evidence_blocks"), block.get("evidence")),
                evidence_pool,
            )
            if not evidence:
                direct = dict(block)
                direct.setdefault("type", current_block_type)
                evidence = [direct]
            rendered.extend(format_evidence_block(item) for item in evidence[:3])
            continue

        text = first_value(block.get("text_zh"), block.get("body_zh"), block.get("summary_zh"))
        if text:
            rendered.append(render_chinese_paragraphs(text))

    return "\n\n".join(rendered) if rendered else None


def render_narrative_sections(metadata: dict[str, Any], analysis: dict[str, Any]) -> str | None:
    sections = analysis.get("narrative_sections")
    if not isinstance(sections, list) or not sections:
        return None
    evidence_pool = collect_evidence_blocks(metadata, analysis)
    rendered = []
    for index, section in enumerate(sections, 1):
        if not isinstance(section, dict):
            continue
        title = normalize_section_title(section, index)
        interleaved_body = render_narrative_content_blocks(section, evidence_pool)
        if interleaved_body is None:
            body = render_chinese_paragraphs(
                first_value(section.get("body_zh"), section.get("body"), section.get("summary_zh"), section.get("summary")),
            )
            evidence = resolve_evidence_blocks(
                first_value(section.get("evidence_ids"), section.get("evidence_refs")),
                first_value(section.get("evidence_blocks"), section.get("evidence")),
                evidence_pool,
            )
            evidence_latex = "\n\n".join(format_evidence_block(item) for item in evidence[:6])
            interleaved_body = "\n\n".join(part for part in (body, evidence_latex) if part)
        rendered.append(latex_section(title, interleaved_body))
    return "\n\n".join(rendered) if rendered else None


def render_missing_narrative_notice() -> str:
    body = latex_text_block(
        "尚未由 Codex 完成叙事型报告正文。请先通读 Docling 导出的正文、图表、公式和证明线索，"
        "确定论文的核心叙事主线，然后在 analysis.json 中写入 narrative_sections。"
        "不要依赖脚本把 method_flow、key_figures、key_tables 和 key_equations 自动拼成报告。"
    )
    return latex_section("论文主线（待 Codex 撰写）", body)


def format_author_analysis(metadata: dict[str, Any], analysis: dict[str, Any]) -> str:
    explicit = first_value(analysis.get("author_analysis"), metadata.get("author_influence_summary"))
    explicit_lines = flatten_chinese_lines(explicit)

    lines = []
    first_author = metadata.get("first_author")
    if isinstance(first_author, dict):
        parts = [str(first_author.get("name") or "未知一作")]
        if first_author.get("affiliation"):
            parts.append(str(first_author["affiliation"]))
        if first_author.get("citation_count") not in (None, ""):
            parts.append(f"引用 {first_author['citation_count']}")
        lines.append("一作: " + " | ".join(parts))
    elif isinstance(first_author, str) and first_author.strip():
        lines.append(f"一作: {first_author.strip()}")

    corresponding = metadata.get("corresponding_authors")
    if isinstance(corresponding, list) and corresponding:
        names = []
        for author in corresponding:
            if isinstance(author, dict):
                names.append(str(author.get("name") or "未知通讯作者"))
            elif isinstance(author, str):
                names.append(author)
        if names:
            lines.append("通讯作者: " + "，".join(names))
    elif metadata.get("corresponding_author_status"):
        lines.append(f"通讯作者: {metadata['corresponding_author_status']}")

    authors = metadata.get("authors")
    if isinstance(authors, list):
        for author in authors:
            if not isinstance(author, dict):
                continue
            name = author.get("name") or "未知作者"
            parts = []
            if author.get("affiliation"):
                parts.append(str(author["affiliation"]))
            if author.get("citation_count") not in (None, ""):
                parts.append(f"引用: {author['citation_count']}")
            if author.get("h_index") not in (None, ""):
                parts.append(f"h-index: {author['h_index']}")
            if author.get("is_high_impact"):
                source = author.get("evidence_source") or "未知来源"
                parts.append(f"高影响力作者 ({source})")
            if parts:
                lines.append(f"{name} | " + " | ".join(parts))

    lines.extend(explicit_lines)
    highlights = flatten_chinese_lines(analysis.get("collaboration_highlights"))
    lines.extend(highlights)
    return latex_itemize(lines) if lines else latex_text_block("暂无信息。")


def build_snapshot(metadata: dict[str, Any]) -> list[str]:
    sources = metadata.get("metadata_sources")
    source_summary = "暂无信息。"
    if isinstance(sources, list) and sources:
        formatted = []
        for source in sources:
            if not isinstance(source, dict):
                continue
            name = source.get("source_name") or "未知来源"
            marker = "官方" if source.get("is_official") else "回退来源"
            formatted.append(f"{name} ({marker})")
        if formatted:
            source_summary = ", ".join(formatted)

    return [
        f"论文 ID: {first_value(metadata.get('paper_id'), '暂无信息。')}",
        f"发表时间: {first_value(metadata.get('published_at'), '暂无信息。')}",
        f"会议或期刊: {first_value(metadata.get('venue'), '暂无信息。')}",
        f"DOI: {first_value(metadata.get('doi'), '暂无信息。')}",
        f"arXiv ID: {first_value(metadata.get('arxiv_id'), '暂无信息。')}",
        f"引用次数: {first_value(metadata.get('citation_count'), '暂无信息。')}",
        f"PDF 路径: {first_value(metadata.get('pdf_path'), '暂无信息。')}",
        f"PDF 解析状态: {first_value(metadata.get('pdf_parse_status', {}).get('state') if isinstance(metadata.get('pdf_parse_status'), dict) else None, '暂无信息。')}",
        f"详情页: {first_value(metadata.get('landing_page'), '暂无信息。')}",
        f"元数据补全状态: {metadata_enrichment_summary(metadata)}",
        f"来源: {source_summary}",
    ]


def metadata_enrichment_summary(metadata: dict[str, Any]) -> str:
    status = metadata.get("metadata_enrichment_status")
    if not isinstance(status, dict):
        return "暂无信息。"
    field_status = status.get("field_status")
    if isinstance(field_status, dict):
        missing = [key for key, value in field_status.items() if value != "found"]
        if missing:
            return "仍缺失 " + "、".join(missing)
        return "关键字段已补全"
    checked = status.get("sources_checked")
    if isinstance(checked, list) and checked:
        return "已检查 " + "、".join(str(item) for item in checked)
    return "暂无信息。"


def render_value_limitations(analysis: dict[str, Any]) -> str:
    blocks = [
        latex_subsection("论文价值", render_chinese_block(analysis.get("value"))),
        latex_subsection(
            "局限",
            render_chinese_block(first_value(analysis.get("limitation_evidence"), analysis.get("limitations"))),
        ),
        latex_subsection("可以怎么优化", render_chinese_block(analysis.get("improvements"))),
    ]
    return "\n\n".join(blocks)


def build_document_body(metadata: dict[str, Any], analysis: dict[str, Any]) -> str:
    validate_integrated_narrative_language(analysis)
    validate_narrative_evidence_depth(analysis)
    narrative_body = render_narrative_sections(metadata, analysis) or render_missing_narrative_notice()
    sections = [
        latex_section("论文概览与元数据", latex_itemize(build_snapshot(metadata))),
        latex_section("作者与影响力", format_author_analysis(metadata, analysis)),
        latex_section("英文摘要原文", render_block(metadata.get("abstract_en"))),
        latex_section(
            "中文摘要",
            render_chinese_block(
                first_value(analysis.get("abstract_zh"), metadata.get("abstract_zh")),
                placeholder="暂无忠实直译摘要。",
            ),
        ),
        latex_section("一句话概括", render_chinese_block(analysis.get("summary_one_liner"))),
        narrative_body,
        latex_section("价值、局限与可优化方向", render_value_limitations(analysis)),
    ]
    return "\n\n".join(sections)


def render_report(metadata: dict[str, Any], analysis: dict[str, Any], output_path: Path | None = None) -> str:
    del output_path
    title = first_value(analysis.get("title_zh"), metadata.get("title_zh"), metadata.get("title"), "未命名论文")
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    body = build_document_body(metadata, analysis)
    return (
        template.replace("__REPORT_TITLE__", escape_latex(str(title)))
        .replace("__REPORT_DATE__", r"\today")
        .replace("__REPORT_BODY__", body)
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a LaTeX paper report.")
    parser.add_argument("--metadata-file", required=True)
    parser.add_argument("--analysis-file")
    parser.add_argument("--output", required=True)
    parser.add_argument("--pdf-output")
    return parser.parse_args()


def refresh_library_index(metadata_file: Path, metadata: dict[str, Any]) -> dict[str, Any] | None:
    bundle_dir_value = metadata.get("bundle_dir")
    bundle_dir = Path(str(bundle_dir_value)) if bundle_dir_value else metadata_file.parent
    metadata_path = bundle_dir / "metadata.json"
    if not metadata_path.exists():
        return None

    from scripts import paper_store

    library_dir = bundle_dir.parent
    try:
        library_dir = paper_store.validate_library_dir(library_dir)
    except ValueError:
        return None
    return paper_store.refresh_html_index(library_dir)


def main() -> int:
    args = parse_args()
    metadata_file = Path(args.metadata_file)
    metadata = load_json(metadata_file)
    analysis = load_json(Path(args.analysis_file)) if args.analysis_file else {}
    output_path = Path(args.output)
    report = render_report(metadata, analysis, output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    if args.pdf_output:
        from scripts import render_report_pdf

        render_report_pdf.render_tex_file_to_pdf(output_path, Path(args.pdf_output))
    refresh_library_index(metadata_file, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

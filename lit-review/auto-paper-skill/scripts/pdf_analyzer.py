#!/usr/bin/env python3
"""Extract structured PDF evidence for AutoPaperSkill using Docling only."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
MATH_SIGNAL_RE = re.compile(
    r"(=|≤|≥|∑|∏|√|±|×|÷|∫|\\sum|\\frac|\\argmax|\\argmin|\bE\[|\blog\b|\bexp\b|\bp\(|\bScore\()"
)
CAPTION_RE = re.compile(
    r"^(Figure|Fig\.?|Table|图|表)\s*([A-Za-z0-9.\-一二三四五六七八九十]+)?[:.\s-]*(.*)$",
    re.IGNORECASE,
)
THEORY_RE = re.compile(r"\b(theorem|lemma|proposition|corollary|proof)\b", re.IGNORECASE)
UNSAFE_MATH_RE = re.compile(
    r"\\(?:input|include|write|openout|read|catcode|usepackage|documentclass|newcommand|renewcommand|def|gdef|edef|directlua|csname|immediate)\b",
    re.IGNORECASE,
)
DEFAULT_IMAGE_SCALE = 3.0


def contains_cjk(text: str) -> bool:
    return bool(CJK_RE.search(text))


def detect_caption(line: str) -> tuple[str, str, str, str] | None:
    match = CAPTION_RE.match(line)
    if not match:
        return None
    kind = match.group(1)
    number = (match.group(2) or "").strip()
    original_label = f"{kind} {number}".strip()
    if kind.lower().startswith("table") or kind == "表":
        label = f"表 {number}".strip() or "表"
        visual_type = "table"
    else:
        label = f"图 {number}".strip() or "图"
        visual_type = "figure"
    caption = (match.group(3) or "").strip() or line.strip()
    return label, original_label, caption, visual_type


def is_equation_like(line: str) -> bool:
    text = " ".join(line.split())
    if len(text) < 6 or not MATH_SIGNAL_RE.search(text):
        return False
    word_count = len(re.findall(r"[A-Za-z]{3,}", text))
    if len(text) > 180 and word_count > 20:
        return False
    if text.count(".") >= 2 and word_count > 10:
        return False
    math_chars = len(re.findall(r"[=+\-*/≤≥∑∏√±×÷∫(){}[\]_^|]", text))
    density = math_chars / max(len(text), 1)
    return density >= 0.06 or bool(re.search(r"\b[a-zA-Z]\s*=\s*[^,.;]+", text))


def summarize_equation(line: str) -> dict[str, str]:
    symbol_explanations: dict[str, str] = {}
    lowered = line.lower()
    if "lambda" in lowered:
        symbol_explanations["lambda"] = "正则化权重或权衡系数"
    if "theta" in lowered:
        symbol_explanations["theta"] = "模型参数"
    if "w" in line:
        symbol_explanations["W"] = "权重或参数矩阵"
    if "b" in line:
        symbol_explanations["b"] = "偏置项"
    return symbol_explanations


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


def raw_to_latex_expression(raw_expression: str) -> str | None:
    text = strip_math_delimiters(raw_expression)
    if not text or len(text) > 1200 or "%" in text or UNSAFE_MATH_RE.search(text):
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
    return text if braces_are_balanced(text) else None


def equation_importance_score(item: dict[str, Any]) -> int:
    text = str(item.get("raw_expression") or "")
    lowered = text.lower()
    if any(token in lowered for token in ("years old", "the answer is", "alex is", "amy is", "jake is")):
        return -10

    score = 0
    for token in ("ssc", "arg max", "argmax", "smoothl1", "crossentropy", "score", "soft", "confidence"):
        if token in lowered:
            score += 4
    for token in ("∑", "\\sum", "sum", "τ", "gamma", "lambda", "p(", "max", "min"):
        if token in lowered:
            score += 2
    score += min(len(re.findall(r"[=≤≥∑∏{}()_^]", text)), 8)
    if 25 <= len(text) <= 220:
        score += 2
    if len(text) > 320:
        score -= 3
    return score


def select_key_equations(equations: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    ranked = [
        (equation_importance_score(item), index, item)
        for index, item in enumerate(equations)
        if equation_importance_score(item) > 0
    ]
    ranked.sort(key=lambda row: (-row[0], row[1]))
    return [item for _, _, item in ranked[:limit]]


def normalize_docling_label(label: Any) -> str:
    if label is None:
        return ""
    value = getattr(label, "value", label)
    return str(value).strip().lower()


def extract_page_no(item: Any) -> int | None:
    prov = getattr(item, "prov", None) or []
    if not prov:
        return None
    return getattr(prov[0], "page_no", None)


def item_text(item: Any) -> str:
    for attr in ("text", "orig"):
        value = getattr(item, attr, None)
        if value:
            return str(value).strip()
    return ""


def item_caption_text(item: Any, document: Any) -> str:
    caption_method = getattr(item, "caption_text", None)
    if callable(caption_method):
        try:
            value = caption_method(doc=document)
        except TypeError:
            value = caption_method(document)
        return str(value or "").strip()
    for attr in ("caption", "text", "orig"):
        value = getattr(item, attr, None)
        if value:
            return str(value).strip()
    return ""


def save_docling_image(image: Any, output_path: Path) -> str | None:
    if image is None:
        return None
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        image.save(output_path, format="PNG")
    except TypeError:
        with output_path.open("wb") as handle:
            image.save(handle, format="PNG")
    return str(output_path.resolve())


def normalize_visual_identity(caption: str, visual_type: str, index: int) -> tuple[str, str]:
    detected = detect_caption(caption)
    if detected:
        label_zh, original_label, _, _ = detected
        return label_zh, original_label
    if visual_type == "table":
        return f"表 {index}", f"Table {index}"
    return f"图 {index}", f"Figure {index}"


def try_import_docling() -> tuple[Any, Any, Any, Any, Any]:
    try:
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling_core.types.doc import PictureItem, TableItem
    except ImportError as exc:
        raise ModuleNotFoundError(
            "Docling is not installed. Install the standard `docling` package to use the primary PDF parser."
        ) from exc
    return DocumentConverter, InputFormat, PdfFormatOption, PdfPipelineOptions, (PictureItem, TableItem)


def configure_standard_docling_pipeline_options(
    pipeline_options: Any,
    image_scale: float = DEFAULT_IMAGE_SCALE,
) -> Any:
    """Configure Docling to use only the standard local PDF pipeline."""
    if hasattr(pipeline_options, "images_scale"):
        pipeline_options.images_scale = image_scale
    if hasattr(pipeline_options, "generate_page_images"):
        pipeline_options.generate_page_images = True
    if hasattr(pipeline_options, "generate_picture_images"):
        pipeline_options.generate_picture_images = True
    if hasattr(pipeline_options, "generate_table_images"):
        pipeline_options.generate_table_images = True
    if hasattr(pipeline_options, "do_table_structure"):
        pipeline_options.do_table_structure = True
    if hasattr(pipeline_options, "document_timeout"):
        pipeline_options.document_timeout = 120.0
    if hasattr(pipeline_options, "enable_remote_services"):
        pipeline_options.enable_remote_services = False
    if hasattr(pipeline_options, "do_picture_description"):
        pipeline_options.do_picture_description = False
    if hasattr(pipeline_options, "do_picture_classification"):
        pipeline_options.do_picture_classification = False
    if hasattr(pipeline_options, "do_formula_enrichment"):
        pipeline_options.do_formula_enrichment = False
    if hasattr(pipeline_options, "do_code_enrichment"):
        pipeline_options.do_code_enrichment = False
    return pipeline_options


def build_docling_converter(image_scale: float = DEFAULT_IMAGE_SCALE) -> tuple[Any, type[Any], type[Any]]:
    DocumentConverter, InputFormat, PdfFormatOption, PdfPipelineOptions, classes = try_import_docling()
    picture_cls, table_cls = classes

    pipeline_options = PdfPipelineOptions()
    configure_standard_docling_pipeline_options(pipeline_options, image_scale=image_scale)

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
        }
    )
    return converter, picture_cls, table_cls


def convert_with_docling(
    pdf_path: Path,
    image_scale: float = DEFAULT_IMAGE_SCALE,
) -> tuple[Any, type[Any], type[Any]]:
    converter, picture_cls, table_cls = build_docling_converter(image_scale=image_scale)
    conversion = converter.convert(pdf_path)
    return conversion, picture_cls, table_cls


def extract_docling_visuals(
    document: Any,
    picture_cls: type[Any],
    table_cls: type[Any],
    images_dir: Path,
    image_scale: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    figures: list[dict[str, Any]] = []
    tables: list[dict[str, Any]] = []

    for element, _level in document.iterate_items():
        if isinstance(element, picture_cls):
            index = len(figures) + 1
            caption = item_caption_text(element, document)
            label_zh, original_label = normalize_visual_identity(caption, "figure", index)
            asset_path = save_docling_image(
                element.get_image(document),
                images_dir / f"figure-{index:03d}.png",
            )
            status = "已由 Docling 直接导出" if asset_path else "Docling 识别到图对象，但未返回可导出图像"
            figures.append(
                {
                    "label": label_zh,
                    "label_zh": label_zh,
                    "label_original": original_label,
                    "caption": caption,
                    "caption_zh": caption if contains_cjk(caption) else None,
                    "page": extract_page_no(element),
                    "asset_path": asset_path,
                    "image_scale": image_scale,
                    "visual_type": "figure",
                    "crop_status": status,
                    "crop_status_zh": status,
                    "evidence_summary": "Docling 直接解析出了图对象和对应标题，可据此分析方法流程或关键视觉证据。",
                    "evidence_summary_zh": "Docling 直接解析出了图对象和对应标题，可据此分析方法流程或关键视觉证据。",
                    "linked_sections": ["method_flow"],
                }
            )
        elif isinstance(element, table_cls):
            index = len(tables) + 1
            caption = item_caption_text(element, document)
            label_zh, original_label = normalize_visual_identity(caption, "table", index)
            asset_path = save_docling_image(
                element.get_image(document),
                images_dir / f"table-{index:03d}.png",
            )
            status = "已由 Docling 直接导出" if asset_path else "Docling 识别到表对象，但未返回可导出图像"
            tables.append(
                {
                    "label": label_zh,
                    "label_zh": label_zh,
                    "label_original": original_label,
                    "caption": caption,
                    "caption_zh": caption if contains_cjk(caption) else None,
                    "page": extract_page_no(element),
                    "asset_path": asset_path,
                    "image_scale": image_scale,
                    "visual_type": "table",
                    "crop_status": status,
                    "crop_status_zh": status,
                    "evidence_summary": "Docling 直接解析出了表对象和对应标题，可据此核对主结果、消融或实验设置。",
                    "evidence_summary_zh": "Docling 直接解析出了表对象和对应标题，可据此核对主结果、消融或实验设置。",
                    "linked_sections": ["results"],
                }
            )
    return figures, tables


def extract_docling_textual_evidence(document: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    equations: list[dict[str, Any]] = []
    theory_items: list[dict[str, Any]] = []

    for text_item in getattr(document, "texts", []):
        text = item_text(text_item)
        if not text:
            continue
        page_no = extract_page_no(text_item)
        label_text = normalize_docling_label(getattr(text_item, "label", None))

        if "formula" in label_text or is_equation_like(text):
            latex_expression = raw_to_latex_expression(text)
            equations.append(
                {
                    "label": f"公式 {len(equations) + 1}",
                    "label_zh": f"公式 {len(equations) + 1}",
                    "raw_expression": text,
                    "latex_expression": latex_expression,
                    "page": page_no,
                    "context": "从 Docling 结构化文本中提取",
                    "symbol_explanations": summarize_equation(text),
                    "method_role": "从 Docling 结构化结果中识别到的公式型表达。",
                    "method_role_zh": "从 Docling 结构化结果中识别到的公式型表达。",
                    "derivation_summary": "需要结合论文上下文进一步解释各项如何作用于训练、推理或理论分析。",
                    "derivation_summary_zh": "需要结合论文上下文进一步解释各项如何作用于训练、推理或理论分析。",
                }
            )

        if THEORY_RE.search(text):
            theory_items.append(
                {
                    "label": "证明相关段落",
                    "label_zh": "证明相关段落",
                    "kind": "proof" if "proof" in text.lower() else "theory",
                    "page": page_no,
                    "statement_original": text,
                    "statement_summary": "Docling 识别到理论或证明相关文本段落。",
                    "statement_summary_zh": "Docling 识别到理论或证明相关文本段落。",
                    "assumptions": [],
                    "proof_summary": "需要结合正文继续解释证明主线、关键假设和结论意义。",
                    "proof_summary_zh": "需要结合正文继续解释证明主线、关键假设和结论意义。",
                    "importance": "可作为理论贡献或证明过程的结构化证据入口。",
                    "importance_zh": "可作为理论贡献或证明过程的结构化证据入口。",
                }
            )
    return equations, theory_items


def export_document_markdown(document: Any) -> str:
    export_method = getattr(document, "export_to_markdown", None)
    if not callable(export_method):
        return ""
    try:
        return str(export_method() or "").strip()
    except Exception:
        return ""


def export_document_text(document: Any) -> str:
    export_method = getattr(document, "export_to_text", None)
    if callable(export_method):
        try:
            text = str(export_method() or "").strip()
            if text:
                return text
        except Exception:
            pass
    return "\n\n".join(item_text(item) for item in getattr(document, "texts", []) if item_text(item))


def extract_markdown_sections(markdown: str, *, max_chars_per_section: int = 2400) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    current_title = "正文"
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines
        body = "\n".join(current_lines).strip()
        if body:
            sections.append({"title": current_title, "text": body[:max_chars_per_section]})
        current_lines = []

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            flush()
            current_title = heading.group(2).strip()
            continue
        if line:
            current_lines.append(line)
    flush()
    return sections


def analyze_pdf_with_docling(
    pdf_path: Path,
    images_dir: Path,
    image_scale: float = DEFAULT_IMAGE_SCALE,
) -> dict[str, Any]:
    conversion, picture_cls, table_cls = convert_with_docling(pdf_path, image_scale=image_scale)
    document = conversion.document

    figures, tables = extract_docling_visuals(document, picture_cls, table_cls, images_dir, image_scale=image_scale)
    equations, theory_items = extract_docling_textual_evidence(document)
    key_equations = select_key_equations(equations)
    document_markdown = export_document_markdown(document)
    document_text = export_document_text(document)
    text_sections = extract_markdown_sections(document_markdown)

    notes = [
        "解析器: Docling 标准 PDF pipeline",
        "图和表优先由 Docling 直接解析为文档对象，再导出对应图像资产。",
        f"Docling 图表导出倍率: {image_scale:g}x。",
        "公式和证明线索优先来自 Docling 的结构化文本结果。",
        "当前未启用 Docling VLM、图片描述或远程模型服务。",
    ]
    if not figures:
        notes.append("Docling 未识别到可用图对象，请结合正文进一步核对。")
    if not tables:
        notes.append("Docling 未识别到可用表对象，请结合正文进一步核对。")

    pages = getattr(document, "pages", {})
    page_count = len(pages)

    return {
        "pdf_path": str(pdf_path.resolve()),
        "pdf_parse_status": {
            "state": "已解析",
            "parser": "docling",
            "page_count": page_count,
            "image_scale": image_scale,
            "notes": notes,
        },
        "figures": figures,
        "tables": tables,
        "equations": equations,
        "theoretical_items": theory_items,
        "document_text": document_text[:60000],
        "document_markdown": document_markdown[:60000],
        "text_sections": text_sections,
        "method_evidence": [f"{item['label']}: {item['evidence_summary_zh']}" for item in figures[:3]]
        + [f"{item['label']}: {item['raw_expression']}" for item in key_equations[:2]],
        "result_evidence": [f"{item['label']}: {item['evidence_summary_zh']}" for item in tables[:3]],
        "proof_explanations": [item["proof_summary_zh"] for item in theory_items[:3]],
        "key_figures": figures[:5],
        "key_tables": tables[:5],
        "key_equations": key_equations,
        "derivation_explanations": [item["derivation_summary_zh"] for item in key_equations[:3]],
    }

def analyze_pdf(
    pdf_path: Path,
    images_dir: Path,
    image_scale: float = DEFAULT_IMAGE_SCALE,
) -> dict[str, Any]:
    try:
        return analyze_pdf_with_docling(pdf_path, images_dir, image_scale=image_scale)
    except Exception as exc:
        raise RuntimeError(f"Docling 解析失败，无法继续生成分析结果: {exc}") from exc


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract structured PDF evidence for AutoPaperSkill.")
    parser.add_argument("--pdf", required=True, help="Path to the local PDF file.")
    parser.add_argument("--output-json", required=True, help="Path to write the structured JSON output.")
    parser.add_argument("--images-dir", required=True, help="Directory for extracted images.")
    parser.add_argument(
        "--image-scale",
        type=positive_float,
        default=DEFAULT_IMAGE_SCALE,
        help=(
            "Docling image export scale. Higher values produce sharper figure/table assets "
            f"at the cost of larger files and slower parsing. Default: {DEFAULT_IMAGE_SCALE:g}."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = analyze_pdf(Path(args.pdf), Path(args.images_dir), image_scale=args.image_scale)
    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

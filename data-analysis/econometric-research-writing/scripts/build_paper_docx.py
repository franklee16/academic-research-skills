import argparse
import json
from pathlib import Path
import re

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

from omml_math import append_display_equation, append_inline_equation, GREEK


DEFAULT_SECTIONS = [
    ("1. Introduction", ["State the research question, setting, empirical strategy, and main finding."]),
    ("2. Data", ["Describe sample construction, variables, transformations, and summary statistics."]),
    ("3. Empirical Strategy", ["Present the baseline equation, estimator, assumptions, and inference approach."]),
    ("4. Results", ["Interpret estimates with economic magnitude and uncertainty."]),
    ("5. Robustness", ["Group robustness checks by threat: measurement, sample, specification, inference, and identification."]),
    ("6. Conclusion", ["Summarize what the evidence shows and what remains uncertain."]),
]


def set_run_style(run, bold=False, italic=False, superscript=False, subscript=False, size=12):
    run.bold = bool(bold)
    run.italic = bool(italic)
    run.font.superscript = bool(superscript)
    run.font.subscript = bool(subscript)
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)


def add_styled_run(paragraph, text, bold=False, italic=False, superscript=False, subscript=False, size=12):
    run = paragraph.add_run(str(text))
    set_run_style(run, bold=bold, italic=italic, superscript=superscript, subscript=subscript, size=size)
    return run


def add_runs(paragraph, runs, default_size=12):
    for item in runs:
        if isinstance(item, str):
            add_styled_run(paragraph, item, size=default_size)
            continue
        add_styled_run(
            paragraph,
            item.get("text", ""),
            bold=item.get("bold", False),
            italic=item.get("italic", False),
            superscript=item.get("superscript", False),
            subscript=item.get("subscript", False),
            size=item.get("size", default_size),
        )


def should_render_as_math(text):
    if not isinstance(text, str):
        return False
    if "_" in text or "^" in text:
        return True
    words = re.findall(r"[a-zA-Z]+", text)
    if any(w in GREEK for w in words):
        return True
    return False


def set_cell_text(cell, text, bold=False):
    cell.text = ""
    p = cell.paragraphs[0]
    if should_render_as_math(text):
        append_inline_equation(p, text)
    else:
        add_styled_run(p, text, bold=bold, size=10)


def set_cell_border(cell, **kwargs):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)

    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        if edge not in kwargs:
            continue
        tag = "w:{}".format(edge)
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        for key, value in kwargs[edge].items():
            element.set(qn("w:{}".format(key)), str(value))


def force_style_color(style, color="000000"):
    r_pr = style.element.get_or_add_rPr()
    color_el = r_pr.find(qn("w:color"))
    if color_el is None:
        color_el = OxmlElement("w:color")
        r_pr.append(color_el)
    color_el.set(qn("w:val"), color)


def apply_three_line_table(table):
    line = {"val": "single", "sz": "8", "space": "0", "color": "000000"}
    no_line = {"val": "nil"}
    row_count = len(table.rows)
    if row_count == 0:
        return

    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    for row in table.rows:
        for cell in row.cells:
            set_cell_border(
                cell,
                top=no_line,
                left=no_line,
                bottom=no_line,
                right=no_line,
                insideH=no_line,
                insideV=no_line,
            )

    for cell in table.rows[0].cells:
        set_cell_border(cell, top=line, bottom=line, left=no_line, right=no_line)
    for cell in table.rows[-1].cells:
        set_cell_border(cell, bottom=line, left=no_line, right=no_line)


def style_document(doc):
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(6)

    for name, size in [("Title", 16), ("Heading 1", 13), ("Heading 2", 12), ("Heading 3", 12)]:
        if name not in styles:
            continue
        style = styles[name]
        style.font.name = "Times New Roman"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
        force_style_color(style)

    for style in styles:
        if style.name.startswith("Heading"):
            style.font.color.rgb = RGBColor(0, 0, 0)
            force_style_color(style)


def add_title_block(doc, spec):
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_styled_run(title, spec.get("title", "Econometric Research Paper"), bold=True, size=16)

    for key in ["author", "affiliation", "date"]:
        if spec.get(key):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_styled_run(p, spec[key], size=12)

    if spec.get("abstract"):
        doc.add_paragraph("Abstract", style="Heading 1")
        doc.add_paragraph(spec["abstract"])

    if spec.get("keywords"):
        p = doc.add_paragraph()
        add_styled_run(p, "Keywords: ", bold=True)
        add_styled_run(p, ", ".join(spec["keywords"]) if isinstance(spec["keywords"], list) else str(spec["keywords"]))


def add_small_note(doc, label, value):
    if not value:
        return
    text = " ".join(str(item) for item in value) if isinstance(value, list) else str(value)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    add_styled_run(p, f"{label}: ", bold=True, size=9)
    add_styled_run(p, text, size=9)


def add_table(doc, table_spec):
    rows = table_spec.get("rows", [])
    if not rows:
        return
    caption = table_spec.get("caption")
    if caption:
        p = doc.add_paragraph()
        add_styled_run(p, caption, bold=True, size=10)
    col_count = max(len(row) for row in rows)
    table = doc.add_table(rows=len(rows), cols=col_count)
    for i, row in enumerate(rows):
        for j in range(col_count):
            value = row[j] if j < len(row) else ""
            set_cell_text(table.cell(i, j), str(value), bold=(i == 0))
    apply_table_merges(table, table_spec.get("merges", []) + table_spec.get("header_merges", []))
    if table_spec.get("style", "three-line") == "grid":
        table.style = "Table Grid"
    else:
        apply_three_line_table(table)
    add_small_note(doc, "Notes", table_spec.get("notes"))
    add_small_note(doc, "Source", table_spec.get("source"))


def apply_table_merges(table, merges):
    for merge in merges:
        if isinstance(merge, dict):
            if "col" in merge:
                col = int(merge["col"])
                start_row = int(merge.get("start_row", merge.get("start", 0)))
                end_row = int(merge.get("end_row", merge.get("end", start_row)))
                max_row = len(table.rows) - 1
                start_row = max(0, min(start_row, max_row))
                end_row = max(0, min(end_row, max_row))
                if end_row > start_row:
                    table.cell(start_row, col).merge(table.cell(end_row, col))
            else:
                row = int(merge.get("row", 0))
                start_col = int(merge.get("start_col", merge.get("start", 0)))
                end_col = int(merge.get("end_col", merge.get("end", start_col)))
                max_col = len(table.columns) - 1
                start_col = max(0, min(start_col, max_col))
                end_col = max(0, min(end_col, max_col))
                if end_col > start_col:
                    table.cell(row, start_col).merge(table.cell(row, end_col))
        else:
            if len(merge) >= 4 and str(merge[3]).lower() == "vertical":
                col, start_row, end_row = [int(v) for v in merge[:3]]
                max_row = len(table.rows) - 1
                start_row = max(0, min(start_row, max_row))
                end_row = max(0, min(end_row, max_row))
                if end_row > start_row:
                    table.cell(start_row, col).merge(table.cell(end_row, col))
            else:
                row, start_col, end_col = [int(value) for value in merge[:3]]
                max_col = len(table.columns) - 1
                start_col = max(0, min(start_col, max_col))
                end_col = max(0, min(end_col, max_col))
                if end_col > start_col:
                    table.cell(row, start_col).merge(table.cell(row, end_col))


def add_figure(doc, figure_spec):
    path = Path(figure_spec.get("path", ""))
    if not path.exists():
        raise FileNotFoundError(f"Figure file not found: {path}")

    width = Inches(float(figure_spec.get("width_inches", 5.8)))
    caption = figure_spec.get("caption")
    if caption and figure_spec.get("caption_position") == "above":
        p = doc.add_paragraph()
        add_styled_run(p, caption, bold=True, size=10)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(str(path), width=width)

    if caption and figure_spec.get("caption_position", "below") != "above":
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_styled_run(p, caption, bold=True, size=10)

    add_small_note(doc, "Notes", figure_spec.get("notes"))
    add_small_note(doc, "Source", figure_spec.get("source"))


def add_paragraph_item(doc, item):
    p = doc.add_paragraph()
    if item.get("runs"):
        add_runs(p, item["runs"], default_size=item.get("size", 12))
    else:
        add_styled_run(p, item.get("text", ""), size=item.get("size", 12))
    return p


def add_section(doc, section):
    doc.add_paragraph(section.get("heading", "Section"), style=section.get("style", "Heading 1"))
    for item in section.get("content", []):
        if isinstance(item, str):
            doc.add_paragraph(item)
        elif item.get("type") == "paragraph":
            add_paragraph_item(doc, item)
        elif item.get("type") == "equation":
            append_display_equation(doc, item.get("text", ""))
        elif item.get("type") == "table":
            add_table(doc, item)
        elif item.get("type") == "figure":
            add_figure(doc, item)


def build_docx(spec, out_path, template=None, apply_default_style=None):
    doc = Document(template) if template else Document()
    if apply_default_style is None:
        apply_default_style = not bool(template)
    if apply_default_style:
        style_document(doc)
    add_title_block(doc, spec)

    sections = spec.get("sections")
    if not sections:
        sections = [{"heading": h, "content": [{"type": "paragraph", "text": p} for p in ps]} for h, ps in DEFAULT_SECTIONS]
    for section in sections:
        add_section(doc, section)

    if spec.get("references"):
        doc.add_paragraph("References", style="Heading 1")
        for ref in spec["references"]:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.first_line_indent = Inches(-0.25)
            if isinstance(ref, dict) and ref.get("runs"):
                add_runs(p, ref["runs"], default_size=12)
            else:
                add_styled_run(p, ref.get("text", "") if isinstance(ref, dict) else ref)

    doc.save(out_path)


def build_style_template(out_path):
    doc = Document()
    style_document(doc)
    doc.save(out_path)


def main():
    parser = argparse.ArgumentParser(description="Build a standard economics/management paper DOCX from JSON.")
    parser.add_argument("input_json")
    parser.add_argument("output_docx")
    parser.add_argument("--template")
    parser.add_argument("--apply-default-style", action="store_true", help="Apply the built-in Times New Roman layout even when a template is supplied.")
    parser.add_argument("--make-template", action="store_true", help="Ignore input content and create a reusable style template.")
    args = parser.parse_args()

    if args.make_template:
        build_style_template(args.output_docx)
        return
    else:
        spec = json.loads(Path(args.input_json).read_text(encoding="utf-8"))

    apply_default_style = True if args.apply_default_style else None
    build_docx(spec, args.output_docx, template=args.template, apply_default_style=apply_default_style)


if __name__ == "__main__":
    main()

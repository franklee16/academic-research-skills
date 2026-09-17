#!/usr/bin/env python3
"""
assemble_docx.py — Convert assembled markdown grant text to formatted DOCX.

Usage:
    python assemble_docx.py <input.md> <output.docx>

Features:
    - Parses markdown bold (**) and italic (*) markers
    - Applies heading hierarchy (14pt / 13pt / 12pt bold)
    - Times New Roman 12pt body text, 1-inch margins, single spacing
    - Auto-installs python-docx if missing
"""

import sys
import subprocess

try:
    from docx import Document
    from docx.shared import Pt, Inches
except ImportError:
    print("python-docx not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document
    from docx.shared import Pt, Inches


def apply_heading_style(doc, text, level=1):
    """Add a heading paragraph with appropriate size and bold."""
    sizes = {1: Pt(14), 2: Pt(13), 3: Pt(12)}
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = sizes.get(level, Pt(12))
    run.font.name = "Times New Roman"
    return p


def add_body_paragraph(doc, text):
    """Add a body paragraph, parsing inline bold and italic markers."""
    p = doc.add_paragraph()
    # Split by ** to handle bold first, then * for italic within segments
    parts = text.split("**")
    for i, part in enumerate(parts):
        if not part:
            continue
        if i % 2 == 1:
            # Bold segment
            run = p.add_run(part)
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
        else:
            # Normal/italic segment — split by * for italic
            italic_parts = part.split("*")
            for j, seg in enumerate(italic_parts):
                if not seg:
                    continue
                run = p.add_run(seg)
                run.font.name = "Times New Roman"
                run.font.size = Pt(12)
                if j % 2 == 1:
                    run.italic = True
    return p


def classify_header(line):
    """
    Classify a header line and return (is_header, level, clean_text).
    Level 1: main sections (1. Research Context, 2. Research Questions, etc.)
    Level 2: subsections (1.1, 3.1, 3.2, etc.)
    Level 3: sub-subsections (3.1.1, 3.3.1, etc.)
    """
    stripped = line.strip()
    # Remove surrounding ** if present
    if stripped.startswith("**") and stripped.endswith("**"):
        stripped = stripped.strip("*").strip()

    # Level 3: x.x.x pattern
    if any(stripped.startswith(p) for p in [
        "1.1.", "1.2.", "3.1.1", "3.1.2", "3.2.1", "3.2.2",
        "3.3.1", "3.3.2", "3.3.3", "3.3.4", "3.3.5"
    ]):
        return True, 3, stripped

    # Level 2: x.x pattern or specific keywords
    if any(stripped.startswith(p) for p in [
        "1.1 ", "1.2 ", "3.1 ", "3.2 ", "3.3 ", "3.4 "
    ]) or stripped in ["Short run", "Medium and long run"]:
        return True, 2, stripped

    # Level 1: x. or specific headers
    if any(stripped.startswith(p) for p in [
        "1. ", "2. ", "3. Research", "References"
    ]):
        return True, 1, stripped

    return False, 0, stripped


def main(input_path, output_path):
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Set default style
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.line_spacing = 1.15

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    for line in content.split("\n"):
        line = line.rstrip()
        if not line.strip():
            continue

        is_header, level, text = classify_header(line)
        if is_header:
            p = apply_heading_style(doc, text, level)
            p.paragraph_format.space_before = Pt(12 if level == 1 else 8)
            p.paragraph_format.space_after = Pt(6 if level == 1 else 4)
        else:
            add_body_paragraph(doc, line)

    doc.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python assemble_docx.py <input.md> <output.docx>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])

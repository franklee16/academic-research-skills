import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


def read_xml(zf, name):
    try:
        return zf.read(name)
    except KeyError:
        return b""


def inspect_docx(path):
    path = Path(path)
    with zipfile.ZipFile(path) as zf:
        document_xml = read_xml(zf, "word/document.xml")
        styles_xml = read_xml(zf, "word/styles.xml")
        root = ET.fromstring(document_xml)
        styles = ET.fromstring(styles_xml) if styles_xml else None
        media = [n for n in zf.namelist() if n.startswith("word/media/")]

    headings = []
    for p in root.findall(".//w:p", NS):
        pstyle = p.find("./w:pPr/w:pStyle", NS)
        if pstyle is not None:
            val = pstyle.attrib.get(f"{{{NS['w']}}}val", "")
            if val.lower().startswith("heading"):
                text = "".join(t.text or "" for t in p.findall(".//w:t", NS))
                headings.append({"style": val, "text": text[:120]})

    grid_table_count = 0
    for tbl in root.findall(".//w:tbl", NS):
        tbl_style = tbl.find("./w:tblPr/w:tblStyle", NS)
        if tbl_style is None:
            continue
        val = tbl_style.attrib.get(f"{{{NS['w']}}}val", "")
        if val.lower() in {"tablegrid", "gridtable"}:
            grid_table_count += 1

    superscript_run_count = 0
    for run in root.findall(".//w:r", NS):
        vert_align = run.find("./w:rPr/w:vertAlign", NS)
        if vert_align is None:
            continue
        if vert_align.attrib.get(f"{{{NS['w']}}}val", "").lower() == "superscript":
            superscript_run_count += 1

    plain_numeric_citation_markers = []
    table_caption_count = 0
    figure_caption_count = 0
    source_note_count = 0
    for p in root.findall(".//w:p", NS):
        chars = []
        superscript_flags = []
        for run in p.findall("./w:r", NS):
            vert_align = run.find("./w:rPr/w:vertAlign", NS)
            is_superscript = (
                vert_align is not None
                and vert_align.attrib.get(f"{{{NS['w']}}}val", "").lower() == "superscript"
            )
            run_text = "".join(t.text or "" for t in run.findall(".//w:t", NS))
            chars.append(run_text)
            superscript_flags.extend([is_superscript] * len(run_text))
        text = "".join(chars).strip()
        if not text:
            continue
        leading_space = len("".join(chars)) - len("".join(chars).lstrip())
        for match in re.finditer(r"\[\d{1,3}\]", text):
            start = leading_space + match.start()
            end = leading_space + match.end()
            if not superscript_flags[start:end] or not all(superscript_flags[start:end]):
                plain_numeric_citation_markers.append(text[:160])
                break
        if text.lower().startswith("table "):
            table_caption_count += 1
        if text.lower().startswith("figure "):
            figure_caption_count += 1
        if text.lower().startswith("source:"):
            source_note_count += 1

    blue_heading_styles = []
    if styles is not None:
        for style in styles.findall(".//w:style", NS):
            style_id = style.attrib.get(f"{{{NS['w']}}}styleId", "")
            if style_id.lower().startswith("heading"):
                color = style.find(".//w:color", NS)
                if color is not None:
                    val = color.attrib.get(f"{{{NS['w']}}}val", "")
                    if val and val.upper() not in {"000000", "AUTO"}:
                        blue_heading_styles.append({"style": style_id, "color": val})

    return {
        "path": str(path),
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else 0,
        "omml_count": len(root.findall(".//m:oMath", NS)),
        "table_count": len(root.findall(".//w:tbl", NS)),
        "grid_table_style_count": grid_table_count,
        "media_count": len(media),
        "table_caption_count": table_caption_count,
        "figure_caption_count": figure_caption_count,
        "source_note_count": source_note_count,
        "superscript_run_count": superscript_run_count,
        "plain_numeric_citation_markers_preview": plain_numeric_citation_markers[:12],
        "heading_count": len(headings),
        "headings_preview": headings[:12],
        "nonblack_heading_styles": blue_heading_styles,
    }


def main():
    parser = argparse.ArgumentParser(description="Inspect DOCX formulas, tables, media, and heading styles.")
    parser.add_argument("docx")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = inspect_docx(args.docx)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for key, value in report.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()

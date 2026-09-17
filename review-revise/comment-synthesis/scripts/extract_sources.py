#!/usr/bin/env python
"""
Extract plain text from a folder of comment files (PDF, PPTX, DOCX, TXT, MD).

Usage:
    python extract_sources.py <input-folder> <output-folder>

Writes one .txt per source file into <output-folder>. Tries markitdown first
(broad format coverage), then falls back to per-format libraries.

Reads files relative to the input folder; never writes into the input folder.
"""
import os
import sys
from pathlib import Path


def _try_markitdown(path: Path) -> str | None:
    try:
        from markitdown import MarkItDown
    except Exception:
        return None
    try:
        md = MarkItDown()
        result = md.convert(str(path))
        return result.text_content
    except Exception:
        return None


def _extract_pdf(path: Path) -> str:
    for mod in ("pdfplumber", "pypdf"):
        try:
            if mod == "pdfplumber":
                import pdfplumber
                with pdfplumber.open(path) as pdf:
                    return "\n\n".join((p.extract_text() or "") for p in pdf.pages)
            else:
                from pypdf import PdfReader
                reader = PdfReader(str(path))
                return "\n\n".join((page.extract_text() or "") for page in reader.pages)
        except Exception:
            continue
    return ""


def _extract_pptx(path: Path) -> str:
    try:
        from pptx import Presentation
    except Exception:
        return ""
    prs = Presentation(str(path))
    chunks = []
    for i, slide in enumerate(prs.slides, 1):
        texts = []
        for shape in slide.shapes:
            if getattr(shape, "has_text_frame", False):
                texts.append(shape.text_frame.text)
            if getattr(shape, "has_table", False):
                for row in shape.table.rows:
                    texts.append(" | ".join(cell.text for cell in row.cells))
        if texts:
            chunks.append(f"--- Slide {i} ---\n" + "\n".join(texts))
    return "\n\n".join(chunks)


def _extract_docx(path: Path) -> str:
    try:
        from docx import Document
    except Exception:
        return ""
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs)


def extract(path: Path) -> str:
    suffix = path.suffix.lower()
    text = _try_markitdown(path)
    if text:
        return text
    if suffix == ".pdf":
        return _extract_pdf(path)
    if suffix == ".pptx":
        return _extract_pptx(path)
    if suffix == ".docx":
        return _extract_docx(path)
    if suffix in (".txt", ".md"):
        return path.read_text(encoding="utf-8", errors="replace")
    return ""


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    in_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    if not in_dir.is_dir():
        print(f"Input folder not found: {in_dir}")
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)

    exts = {".pdf", ".pptx", ".docx", ".txt", ".md"}
    files = [p for p in sorted(in_dir.iterdir()) if p.suffix.lower() in exts]
    if not files:
        print(f"No comment files found in {in_dir}")
        return 1

    for f in files:
        try:
            text = extract(f)
        except Exception as e:
            print(f"FAILED  {f.name}: {e}")
            continue
        out = out_dir / (f.stem + ".txt")
        out.write_text(text or "(extraction returned no text)", encoding="utf-8")
        n = len(text or "")
        print(f"OK      {f.name}  ->  {out.name}  ({n} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

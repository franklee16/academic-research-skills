#!/usr/bin/env python3
"""Extract readable PDF text into a Markdown handoff file for the skill."""

from __future__ import annotations

import argparse
import importlib
import os
from pathlib import Path
import subprocess
import sys


DEPENDENCIES = {
    "pypdf": "pypdf>=4.0",
    "pdfplumber": "pdfplumber>=0.11",
}


def ensure_package(module_name: str) -> None:
    if importlib.util.find_spec(module_name) is not None:
        return
    if os.environ.get("PAPER_EVIDENCE_DISTILLER_NO_INSTALL"):
        raise RuntimeError(
            f"Missing Python package '{module_name}'. Install dependencies with: "
            "python -m pip install -r requirements.txt"
        )
    requirement = DEPENDENCIES[module_name]
    subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])


def extract_with_pypdf(pdf_path: Path) -> list[tuple[int, str]]:
    ensure_package("pypdf")
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    pages: list[tuple[int, str]] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append((index, text.strip()))
    return pages


def extract_with_pdfplumber(pdf_path: Path) -> list[tuple[int, str]]:
    ensure_package("pdfplumber")
    import pdfplumber

    pages: list[tuple[int, str]] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pages.append((index, text.strip()))
    return pages


def extract_pages(pdf_path: Path) -> list[tuple[int, str]]:
    try:
        return extract_with_pypdf(pdf_path)
    except Exception:
        return extract_with_pdfplumber(pdf_path)


def write_markdown(pdf_path: Path, output_path: Path) -> None:
    pages = extract_pages(pdf_path)
    lines = [
        f"# Extracted text: {pdf_path.name}",
        "",
        f"- Source PDF: `{pdf_path}`",
        "- Extraction note: generated for paper-evidence-distiller; verify claims against page anchors in this file.",
        "",
    ]
    for page_number, text in pages:
        lines.extend([f"## Page {page_number}", "", text or ""])
        lines.append("")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract a PDF to Markdown for paper evidence distillation.")
    parser.add_argument("pdf", type=Path, help="Input academic paper PDF")
    parser.add_argument("-o", "--output", type=Path, help="Output Markdown path")
    args = parser.parse_args()

    pdf_path = args.pdf.resolve()
    if not pdf_path.exists():
        parser.error(f"PDF not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        parser.error(f"Input must be a .pdf file: {pdf_path}")

    output_path = args.output or pdf_path.with_suffix(".extracted.md")
    write_markdown(pdf_path, output_path.resolve())
    print(output_path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

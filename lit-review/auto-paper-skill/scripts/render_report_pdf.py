#!/usr/bin/env python3
"""Compile a LaTeX paper report into PDF with XeLaTeX."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


def run_xelatex(workdir: Path, tex_path: Path) -> None:
    subprocess.run(
        [
            "xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-output-directory",
            str(workdir),
            str(tex_path),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def render_tex_file_to_pdf(tex_file: Path, output_pdf: Path) -> Path:
    tex_file = tex_file.resolve()
    output_pdf = output_pdf.resolve()
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="autopaper-report-", dir=str(output_pdf.parent)) as tmpdir:
        workdir = Path(tmpdir)
        tex_copy = workdir / "report.tex"
        tex_copy.write_text(tex_file.read_text(encoding="utf-8"), encoding="utf-8")

        run_xelatex(workdir, tex_copy)
        run_xelatex(workdir, tex_copy)

        pdf_path = workdir / "report.pdf"
        shutil.copy2(pdf_path, output_pdf)
    return output_pdf


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile a LaTeX paper report into PDF.")
    parser.add_argument("--tex-file", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    render_tex_file_to_pdf(Path(args.tex_file), Path(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Inspect a PDF page's raster/vector composition without modifying the PDF.

This is a routing aid for THU Digitizer.  It does not extract chart values or
claim that every drawing path is a data mark.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import fitz


def colour_hex(colour: tuple[float, float, float] | None) -> str | None:
    """Convert PyMuPDF's normalized RGB tuple to a stable hexadecimal string."""
    if colour is None:
        return None
    return "#" + "".join(f"{round(channel * 255):02x}" for channel in colour)


def rect_dict(rect: fitz.Rect) -> dict[str, float]:
    return {
        "x0_pt": round(rect.x0, 6),
        "y0_pt": round(rect.y0, 6),
        "x1_pt": round(rect.x1, 6),
        "y1_pt": round(rect.y1, 6),
    }


def counter_rows(counter: Counter[str]) -> list[dict[str, int | str]]:
    return [
        {"value": value, "count": count}
        for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ]


def inspect_page(document: fitz.Document, page_index: int) -> dict[str, Any]:
    page = document[page_index]
    drawings = page.get_drawings()
    operation_counts: Counter[str] = Counter()
    fill_colours: Counter[str] = Counter()
    stroke_colours: Counter[str] = Counter()
    filled_bezier_paths = 0
    nonempty_drawing_bounds = 0

    for drawing in drawings:
        operations = [item[0] for item in drawing["items"]]
        operation_counts.update(operations)
        if drawing["rect"].is_empty is False:
            nonempty_drawing_bounds += 1

        fill = colour_hex(drawing.get("fill"))
        stroke = colour_hex(drawing.get("color"))
        if fill is not None:
            fill_colours[fill] += 1
        if stroke is not None:
            stroke_colours[stroke] += 1
        if fill is not None and "c" in operations:
            filled_bezier_paths += 1

    text_span_count = sum(
        len(line["spans"])
        for block in page.get_text("dict")["blocks"]
        if "lines" in block
        for line in block["lines"]
    )
    images = []
    for image in page.get_images(full=True):
        xref, _, width, height, bits_per_component, colourspace, *_ = image
        images.append(
            {
                "xref": xref,
                "width_px": width,
                "height_px": height,
                "bits_per_component": bits_per_component,
                "colourspace": colourspace,
            }
        )

    if drawings and images:
        status = "mixed_vector_and_raster"
        next_step = (
            "Inspect the requested panel: axes, labels, markers, and fitted curves may be "
            "vector paths even when heatmaps or gradients are raster images."
        )
    elif drawings:
        status = "vector_paths_detected"
        next_step = (
            "Inspect drawing bounds and path geometry before attempting direct mark recovery; "
            "legend symbols and decorations can use the same vector primitives as data marks."
        )
    elif images:
        status = "raster_images_only"
        next_step = "Use the calibrated raster workflow; preserve the raster dimensions and crop evidence."
    else:
        status = "no_vector_or_embedded_raster_detected"
        next_step = "Render visually and inspect the PDF structure manually before choosing an extraction route."

    return {
        "page_number_1_based": page_index + 1,
        "page_rect_pt": rect_dict(page.rect),
        "text_span_count": text_span_count,
        "embedded_image_count": len(images),
        "embedded_images": images,
        "drawing_path_count": len(drawings),
        "drawing_paths_with_nonempty_bounds": nonempty_drawing_bounds,
        "filled_bezier_path_count": filled_bezier_paths,
        "path_operation_counts": counter_rows(operation_counts),
        "fill_colour_counts": counter_rows(fill_colours),
        "stroke_colour_counts": counter_rows(stroke_colours),
        "composition_status": status,
        "suggested_next_step": next_step,
        "limitations": [
            "A vector drawing path is not necessarily a plotted datum.",
            "This report does not identify panel bounds, axis transforms, legends, or source-data parameters.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Input PDF path")
    parser.add_argument(
        "--page",
        required=True,
        type=int,
        help="One-based page number to inspect",
    )
    parser.add_argument(
        "--output-report",
        required=True,
        type=Path,
        help="JSON report path; parent directory must already exist",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        raise FileNotFoundError(f"Input PDF not found: {args.input}")
    with fitz.open(args.input) as document:
        if not 1 <= args.page <= len(document):
            raise ValueError(f"--page must be between 1 and {len(document)}, got {args.page}")
        page_report = inspect_page(document, args.page - 1)

    report = {
        "input_file": str(args.input.resolve()),
        "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "tool": "thu-digitizer/scripts/inspect_pdf_vectors.py",
        "tool_scope": "composition routing only; not a chart-data extractor",
        **page_report,
    }
    args.output_report.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

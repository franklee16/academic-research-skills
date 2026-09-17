"""Build the Nature Communications Fig. 2b grouped-bar gallery case.

The primary CSV is always raster-derived.  Optional PDF vector geometry is
retained as a separate validation reference and never replaces raster values.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

import fitz
import matplotlib
import numpy as np
from PIL import Image

from candidate_digitize_bar_chart import extract_bar_chart, write_overlay
from inspect_pdf_vectors import inspect_page


matplotlib.use("Agg")
import matplotlib.pyplot as plt


CASE_ID = "nature-oatman-grouped-bar"
ARTICLE_URL = "https://www.nature.com/articles/s41467-026-68864-9"
FIGURE_URL = f"{ARTICLE_URL}/figures/2"
IMAGE_URL = (
    "https://media.springernature.com/full/springer-static/image/"
    "art%3A10.1038%2Fs41467-026-68864-9/MediaObjects/"
    "41467_2026_68864_Fig2_HTML.png"
)
PDF_SOURCE_URL = (
    "https://ora.ox.ac.uk/objects/"
    "uuid%3Aea675125-e2a0-409a-8288-31c37c1fe9cf/files/r9593tx374"
)

PANEL_CROP = (1080, 0, 2002, 665)
PLOT_BOUNDS = (87, 20, 890, 485)
# The lower pixel row of each two-pixel major grid line is exactly spaced:
# 0, 10000, 20000, 30000 -> y = 485, 351, 217, 83.
VALUE_AXIS = (485.0, 0.0, 83.0, 30000.0)
EXCLUDE_REGIONS = [(110, 75, 155, 160)]
SERIES_COLORS = {"CER": "#8968CD", "TCX": "#00C5CD"}
CATEGORIES = [
    ("Active TSS", 116.75),
    ("Flanking TSS", 166.25),
    ("Transcription at 5' and 3'", 216.0),
    ("Strong Transcription", 265.75),
    ("Weak Transcription", 315.5),
    ("Genic enhancers", 365.0),
    ("Enhancers", 415.0),
    ("ZNF genes & repeats", 464.5),
    ("Heterochromatin", 514.0),
    ("Bivalent/poised TSS", 563.75),
    ("Flanking bivalent TSS/Enh", 613.5),
    ("Bivalent enhancer", 663.0),
    ("Repressed Polycomb", 712.75),
    ("Weak repressed Polycomb", 762.5),
    ("Quiescent/low", 812.0),
    ("Not Defined", 861.75),
]

PDF_PAGE = 4
PDF_PANEL_BOUNDS = (330.0, 45.0, 540.0, 180.0)
PDF_VALUE_AXIS = (165.113, 0.0, 68.742, 30000.0)
PDF_FILL_COLORS = {
    "CER": (0.53725, 0.40784, 0.80392),
    "TCX": (0.0, 0.77255, 0.80392),
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pixel_to_value(pixel: float, axis: tuple[float, float, float, float]) -> float:
    pixel_0, value_0, pixel_1, value_1 = axis
    return float(value_0 + (pixel - pixel_0) * (value_1 - value_0) / (pixel_1 - pixel_0))


def build_vector_reference(pdf_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    with fitz.open(pdf_path) as document:
        page = document[PDF_PAGE - 1]
        inspection = {
            "input_file": str(pdf_path.resolve()),
            "input_sha256": file_sha256(pdf_path),
            "tool": "thu-digitizer/scripts/inspect_pdf_vectors.py",
            "tool_scope": "composition routing only; not a chart-data extractor",
            **inspect_page(document, PDF_PAGE - 1),
        }
        drawings = page.get_drawings()

    bars: list[dict[str, Any]] = []
    for series, target_fill in PDF_FILL_COLORS.items():
        candidates: list[tuple[int, Any]] = []
        for drawing_index, drawing in enumerate(drawings):
            fill = drawing.get("fill")
            rect = drawing["rect"]
            if fill is None or max(abs(fill[index] - target_fill[index]) for index in range(3)) >= 0.002:
                continue
            if not (PDF_PANEL_BOUNDS[0] < rect.x0 < PDF_PANEL_BOUNDS[2]):
                continue
            if not (PDF_PANEL_BOUNDS[1] < rect.y0 < PDF_PANEL_BOUNDS[3]):
                continue
            if not 4.5 < rect.width < 6.2:
                continue
            if abs(rect.y1 - PDF_VALUE_AXIS[0]) >= 0.02:
                continue
            candidates.append((drawing_index, rect))
        candidates.sort(key=lambda item: item[1].x0)
        if len(candidates) != len(CATEGORIES):
            raise RuntimeError(
                f"expected {len(CATEGORIES)} PDF vector bars for {series}, got {len(candidates)}"
            )
        for (category, _), (drawing_index, rect) in zip(CATEGORIES, candidates):
            bars.append(
                {
                    "category": category,
                    "series": series,
                    "drawing_index": drawing_index,
                    "rect_pt": {
                        "x0": float(rect.x0),
                        "y0": float(rect.y0),
                        "x1": float(rect.x1),
                        "y1": float(rect.y1),
                    },
                    "value": pixel_to_value(float(rect.y0), PDF_VALUE_AXIS),
                    "status": "vector_rectangle_extracted",
                }
            )
    bars.sort(key=lambda row: ([name for name, _ in CATEGORIES].index(row["category"]), row["series"]))
    reference = {
        "schema_version": 1,
        "role": "independent vector-geometry validation; not raster extraction truth replacement",
        "source_url": PDF_SOURCE_URL,
        "source_sha256": file_sha256(pdf_path),
        "page_number_1_based": PDF_PAGE,
        "panel": "Fig. 2b",
        "panel_bounds_pt": list(PDF_PANEL_BOUNDS),
        "value_axis": list(PDF_VALUE_AXIS),
        "axis_anchors": [
            {"pixel_y_pt": PDF_VALUE_AXIS[0], "value": PDF_VALUE_AXIS[1], "label": "0"},
            {"pixel_y_pt": PDF_VALUE_AXIS[2], "value": PDF_VALUE_AXIS[3], "label": "30000"},
        ],
        "legend_exclusion_rule": "accept only 4.5-6.2 pt rectangles meeting the 0 baseline at y=165.113 pt",
        "bars": bars,
    }
    return reference, inspection


def write_raster_csv(path: Path, extraction: dict[str, Any]) -> None:
    fields = [
        "category",
        "series",
        "status",
        "value",
        "unit",
        "confidence",
        "category_center_pixel",
        "bar_left_pixel",
        "bar_top_pixel",
        "bar_right_pixel",
        "bar_bottom_pixel",
        "baseline_pixel",
        "end_pixel",
    ]
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for mark in extraction["marks"]:
            component = mark.get("component", {})
            writer.writerow(
                {
                    "category": mark["category"],
                    "series": mark["series"],
                    "status": mark["status"],
                    "value": mark.get("value", ""),
                    "unit": "visible rCpGm count",
                    "confidence": mark.get("confidence", ""),
                    "category_center_pixel": mark.get("component_category_pixel", ""),
                    "bar_left_pixel": component.get("left_pixel", ""),
                    "bar_top_pixel": component.get("top_pixel", ""),
                    "bar_right_pixel": component.get("right_pixel", ""),
                    "bar_bottom_pixel": component.get("bottom_pixel", ""),
                    "baseline_pixel": mark.get("baseline_pixel", ""),
                    "end_pixel": mark.get("end_pixel", ""),
                }
            )


def validate_against_vector(
    extraction: dict[str, Any], vector_reference: dict[str, Any], output_csv: Path
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    raster = {
        (mark["category"], mark["series"]): mark
        for mark in extraction["marks"]
        if mark["status"] == "extracted"
    }
    vector = {
        (bar["category"], bar["series"]): bar for bar in vector_reference["bars"]
    }
    rows: list[dict[str, Any]] = []
    for key in sorted(vector, key=lambda item: ([name for name, _ in CATEGORIES].index(item[0]), item[1])):
        raster_mark = raster.get(key)
        vector_bar = vector[key]
        matched = raster_mark is not None
        raster_value = float(raster_mark["value"]) if matched else None
        vector_value = float(vector_bar["value"])
        error = raster_value - vector_value if matched else None
        rows.append(
            {
                "category": key[0],
                "series": key[1],
                "raster_value": raster_value,
                "vector_value": vector_value,
                "signed_error": error,
                "absolute_error": abs(error) if error is not None else None,
                "matched": matched,
                "raster_status": raster_mark["status"] if raster_mark else "not_extracted",
                "vector_status": vector_bar["status"],
                "vector_drawing_index": vector_bar["drawing_index"],
            }
        )
    with output_csv.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    errors = np.asarray([row["signed_error"] for row in rows if row["matched"]], dtype=float)
    absolute = np.abs(errors)
    summary = {
        "status": "validated_real_vector_geometry" if len(errors) == len(rows) else "partial_validated",
        "visible_raster_bars": len(extraction["marks"]),
        "vector_bars": len(vector_reference["bars"]),
        "matched_bars": int(len(errors)),
        "mae": float(np.mean(absolute)),
        "rmse": float(np.sqrt(np.mean(np.square(errors)))),
        "median_absolute_error": float(np.median(absolute)),
        "p95_absolute_error": float(np.percentile(absolute, 95)),
        "max_absolute_error": float(np.max(absolute)),
        "mean_signed_error": float(np.mean(errors)),
        "normalized_mae_of_30000_tick_span": float(np.mean(absolute) / 30000.0),
        "raster_value_per_pixel": abs(
            (extraction["value_axis"][3] - extraction["value_axis"][1])
            / (extraction["value_axis"][2] - extraction["value_axis"][0])
        ),
        "reference_file": "vector-reference.json",
        "comparison_file": "vector-validation.csv",
    }
    return summary, rows


def write_recreation(extraction: dict[str, Any], output_path: Path) -> None:
    category_names = [name for name, _ in CATEGORIES]
    positions = np.arange(len(category_names), dtype=float)
    values = {
        (mark["category"], mark["series"]): float(mark["value"])
        for mark in extraction["marks"]
        if mark["status"] == "extracted"
    }
    figure, axis = plt.subplots(figsize=(14, 6.4), dpi=180)
    width = 0.42
    for index, (series, color) in enumerate(SERIES_COLORS.items()):
        offset = (index - 0.5) * width
        axis.bar(
            positions + offset,
            [values[(category, series)] for category in category_names],
            width=width,
            color=color,
            label=series,
        )
    axis.set_ylabel("rCpGm Count")
    axis.set_xlabel("Chromatin State")
    axis.set_xticks(positions, category_names, rotation=31, ha="right", rotation_mode="anchor")
    axis.grid(axis="y", color="#e9e9e9", linewidth=0.8)
    axis.set_axisbelow(True)
    axis.legend(title="tissue", frameon=False, ncol=2, loc="upper left")
    axis.spines[["top", "right"]].set_visible(False)
    axis.set_ylim(0, 34200)
    figure.subplots_adjust(left=0.07, right=0.995, top=0.96, bottom=0.32)
    figure.savefig(output_path, facecolor="white")
    plt.close(figure)


def write_validation_plot(rows: list[dict[str, Any]], output_path: Path) -> None:
    figure, axis = plt.subplots(figsize=(6.4, 6.0), dpi=180)
    for series, color in SERIES_COLORS.items():
        subset = [row for row in rows if row["series"] == series and row["matched"]]
        axis.scatter(
            [row["vector_value"] for row in subset],
            [row["raster_value"] for row in subset],
            s=34,
            color=color,
            label=series,
        )
    limit = 34200
    axis.plot([0, limit], [0, limit], color="#202020", linewidth=1.0, linestyle="--")
    axis.set(xlim=(0, limit), ylim=(0, limit), xlabel="PDF vector value", ylabel="Raster-extracted value")
    axis.set_aspect("equal", adjustable="box")
    axis.grid(color="#eeeeee", linewidth=0.7)
    axis.legend(frameon=False)
    figure.tight_layout()
    figure.savefig(output_path, facecolor="white")
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Official full Fig. 2 PNG")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--pdf", type=Path, help="Published PDF used to build vector reference")
    parser.add_argument("--vector-reference", type=Path, help="Previously retained vector-reference.json")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(args.input) as source:
        source_rgb = source.convert("RGB")
        if source_rgb.size != (2002, 1493):
            raise ValueError(f"expected official Fig. 2 raster size 2002x1493, got {source_rgb.size}")
        source_rgb.crop(PANEL_CROP).save(args.output_dir / "original.png")
    source_figure = args.output_dir / "source-figure.png"
    if args.input.resolve() != source_figure.resolve():
        shutil.copy2(args.input, source_figure)

    extraction = extract_bar_chart(
        args.output_dir / "original.png",
        plot_bounds=PLOT_BOUNDS,
        value_axis=VALUE_AXIS,
        orientation="vertical",
        layout="grouped",
        series_colors=SERIES_COLORS,
        categories=CATEGORIES,
        exclude_regions=EXCLUDE_REGIONS,
        tolerance=2.0,
    )
    if extraction["status"] != "candidate" or extraction["summary"]["extracted_mark_count"] != 32:
        raise RuntimeError(f"real grouped-bar extraction failed: {extraction['summary']}")
    write_raster_csv(args.output_dir / "data.csv", extraction)
    write_overlay(args.output_dir / "original.png", extraction, args.output_dir / "overlay.png")
    write_recreation(extraction, args.output_dir / "recreated.png")

    if args.pdf is not None:
        vector_reference, inspection = build_vector_reference(args.pdf)
        (args.output_dir / "vector-reference.json").write_text(
            json.dumps(vector_reference, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (args.output_dir / "vector-inspection.json").write_text(
            json.dumps(inspection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    else:
        reference_path = args.vector_reference or (args.output_dir / "vector-reference.json")
        vector_reference = json.loads(reference_path.read_text(encoding="utf-8"))
        inspection = None

    validation, validation_rows = validate_against_vector(
        extraction, vector_reference, args.output_dir / "vector-validation.csv"
    )
    write_validation_plot(validation_rows, args.output_dir / "vector-validation.png")

    report = {
        "schema_version": 1,
        "case_id": CASE_ID,
        "status": "candidate",
        "family": "grouped_bar",
        "article": {
            "title": "Integrative epigenomic landscape of Alzheimer’s Disease brains reveals oligodendrocyte molecular perturbations associated with tau",
            "journal": "Nature Communications",
            "year": 2026,
            "doi": "10.1038/s41467-026-68864-9",
            "figure": "Fig. 2b",
            "article_url": ARTICLE_URL,
            "figure_url": FIGURE_URL,
            "image_url": IMAGE_URL,
            "license": "CC BY-NC-ND 4.0",
            "license_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
            "redistribution_note": "Adapted overlays require separate permission for public redistribution.",
        },
        "input": {
            "source_figure": "source-figure.png",
            "source_figure_sha256": file_sha256(source_figure),
            "source_dimensions": {"width": 2002, "height": 1493},
            "panel_crop_source_pixels": list(PANEL_CROP),
            "panel_file": "original.png",
            "panel_sha256": file_sha256(args.output_dir / "original.png"),
        },
        "recoverable_representation": "32 visible CER/TCX grouped-bar endpoints on a calibrated linear count axis",
        "non_recoverable": [
            "the underlying CpG records represented by each count",
            "unplotted categories or sample-level observations",
            "values more precise than the raster pixel quantization without independent vector/source evidence",
        ],
        "candidate_extraction": extraction,
        "vector_validation": validation,
        "vector_reference": {
            "source_url": vector_reference["source_url"],
            "source_sha256": vector_reference["source_sha256"],
            "page_number_1_based": vector_reference["page_number_1_based"],
            "bar_count": len(vector_reference["bars"]),
            "composition_status": inspection["composition_status"] if inspection else "retained_reference",
        },
        "webplotdigitizer_comparison": {
            "status": "not_compared",
            "reason": "No same-input, same-calibration, same-intervention comparison has been run.",
        },
        "outputs": {
            "original": "original.png",
            "overlay": "overlay.png",
            "recreated": "recreated.png",
            "data": "data.csv",
            "vector_reference": "vector-reference.json",
            "vector_validation": "vector-validation.csv",
            "vector_validation_plot": "vector-validation.png",
        },
        "limitations": [
            "The raster values remain the primary extraction and are not overwritten by PDF vector values.",
            "The in-plot legend is removed only through a visually verified exclusion region recorded in the report.",
            "The route remains candidate pending additional held-out real figures and fair WebPlotDigitizer comparison.",
            "The source article is CC BY-NC-ND 4.0; public redistribution of adapted overlay imagery requires separate permission.",
        ],
    }
    (args.output_dir / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"STATUS={report['status']}")
    print(f"BARS={validation['matched_bars']}/{validation['visible_raster_bars']}")
    print(f"VECTOR_MAE={validation['mae']:.6f}")


if __name__ == "__main__":
    main()

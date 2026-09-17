"""Publish the Fig. 5a PDF-vector spatial-point-map case to the gallery.

The source inputs are the evidence-led extraction artifacts in
``thu_digitizer_natcom_fig5a``.  This publisher deliberately does not read
the paper's raw spatial-transcriptomics data: its public CSV contains only
the visibly rendered PDF-vector point geometry, colours, and colourbar-derived
display estimates already present in those artifacts.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "thu_digitizer_natcom_fig5a"
DEFAULT_OUTPUT = REPO_ROOT / "gallery" / "assets" / "cases" / "nature-51329-fig5a"
CASE_ID = "nature-51329-fig5a"
CANVAS = {"width": 1834, "height": 550}
PDF_CROP_PT = {"x": 80.0, "y": 48.0}
PT_TO_PX = 300.0 / 72.0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(value: str) -> float:
    return float(value)


def pixel_coordinate(pdf_x_pt: str, pdf_y_pt: str) -> tuple[float, float]:
    """Map PDF point centres to the 300 DPI crop without inventing map axes."""

    return (
        (as_float(pdf_x_pt) - PDF_CROP_PT["x"]) * PT_TO_PX,
        (as_float(pdf_y_pt) - PDF_CROP_PT["y"]) * PT_TO_PX,
    )


def public_row(source: dict[str, str], *, kind: str) -> dict[str, str]:
    pixel_x, pixel_y = pixel_coordinate(source["pdf_x_pt"], source["pdf_y_pt"])
    width_px = as_float(source["marker_width_pt"]) * PT_TO_PX
    height_px = as_float(source["marker_height_pt"]) * PT_TO_PX
    row = {
        "kind": "point",
        "set": "region_map" if kind == "region" else source["map_id"],
        "series": "categorical_region_spot" if kind == "region" else "colour_mapped_spot",
        "category": source["region"] if kind == "region" else source["cell_type"],
        "spot_id": source["spot_id"],
        "pdf_x_pt": source["pdf_x_pt"],
        "pdf_y_pt": source["pdf_y_pt"],
        "panel_x_norm": source["panel_x_norm"],
        "panel_y_norm": source["panel_y_norm"],
        "pixel_x": f"{pixel_x:.6f}",
        "pixel_y": f"{pixel_y:.6f}",
        "radius": f"{max(width_px, height_px) / 2.0:.6f}",
        "fill": source["fill_hex"],
        "fill_r": source["fill_r"],
        "fill_g": source["fill_g"],
        "fill_b": source["fill_b"],
        "marker_width_pt": source["marker_width_pt"],
        "marker_height_pt": source["marker_height_pt"],
        "value": "" if kind == "region" else source["displayed_colour_value_approx"],
        "value_status": (
            "categorical_visible_marker_no_numeric_value"
            if kind == "region"
            else source["value_status"]
        ),
        "colourbar_y_px": "" if kind == "region" else source["colourbar_y_px"],
        "colourbar_lab_distance": "" if kind == "region" else source["colourbar_lab_distance"],
        "drawing_index": source["drawing_index"],
        "visible_status": source["visible_status"],
        "numeric_use_allowed": "false",
        "coordinate_space": "pdf_vector_point_and_source_crop_pixel",
    }
    return row


CSV_FIELDS = [
    "kind",
    "set",
    "series",
    "category",
    "spot_id",
    "pdf_x_pt",
    "pdf_y_pt",
    "panel_x_norm",
    "panel_y_norm",
    "pixel_x",
    "pixel_y",
    "radius",
    "fill",
    "fill_r",
    "fill_g",
    "fill_b",
    "marker_width_pt",
    "marker_height_pt",
    "value",
    "value_status",
    "colourbar_y_px",
    "colourbar_lab_distance",
    "drawing_index",
    "visible_status",
    "numeric_use_allowed",
    "coordinate_space",
]


def source_report(source_dir: Path) -> dict[str, Any]:
    with (source_dir / "figure5a_extraction_report.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build(source_dir: Path, output_dir: Path) -> None:
    required = [
        "region_spots_visible.csv",
        "probability_spots_visible.csv",
        "figure5a_source.png",
        "figure5a_vector_spot_overlay.png",
        "figure5a_visible_vector_recreation.png",
        "figure5a_extraction_report.json",
        "preflight_report.json",
        "figure5a_spec.json",
    ]
    missing = [name for name in required if not (source_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing required Fig. 5a extraction artifacts: {', '.join(missing)}")

    regions = read_csv(source_dir / "region_spots_visible.csv")
    probabilities = read_csv(source_dir / "probability_spots_visible.csv")
    if len(regions) != 426 or len(probabilities) != 3424:
        raise ValueError(
            f"Unexpected visible-vector coverage: regions={len(regions)}, probabilities={len(probabilities)}"
        )
    if any(row["visible_status"] != "vector_marker_extracted" for row in [*regions, *probabilities]):
        raise ValueError("Only direct PDF-vector marks may be published in the gallery primary CSV.")

    output_dir.mkdir(parents=True, exist_ok=True)
    copied = {
        "figure5a_source.png": "original.png",
        "figure5a_vector_spot_overlay.png": "overlay.png",
        "figure5a_visible_vector_recreation.png": "recreated.png",
        "region_spots_visible.csv": "region-spots-visible.csv",
        "probability_spots_visible.csv": "probability-spots-visible.csv",
        "preflight_report.json": "preflight-report.json",
        "figure5a_spec.json": "figure-spec.json",
    }
    for original, published in copied.items():
        shutil.copy2(source_dir / original, output_dir / published)

    rows = [*(public_row(row, kind="region") for row in regions), *(public_row(row, kind="probability") for row in probabilities)]
    with (output_dir / "data.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    extraction = source_report(source_dir)
    region_counts = dict(sorted(Counter(row["region"] for row in regions).items()))
    map_counts = dict(sorted(Counter(row["map_id"] for row in probabilities).items()))
    report = {
        "schema_version": 1,
        "case_contract_version": 1,
        "case_id": CASE_ID,
        "status": "partial_visible",
        "extraction_status": "candidate_partial_visible",
        "claim": "direct_pdf_vector_visible_spatial_point_recovery",
        "registered_route": "unknown_refuse",
        "registered_route_status": "not_automated",
        "numeric_output_authorized_by_registered_route": False,
        "extraction_strategy": "case_specific_direct_pdf_vector_spot_recovery",
        "source_data_role": "independent_validation_only",
        "source_contract": {
            "article_url": extraction["source"]["article_url"],
            "figure_url": extraction["source"]["figure_url"],
            "article_pdf_sha256": extraction["source"]["input_sha256"],
            "pdf_page_1_based": extraction["source"]["pdf_page_1_based"],
            "panel_crop_pdf_pt": extraction["source"]["panel_crop_pdf_pt"],
            "measurement_space": "PDF-vector point centres; source-crop pixels for gallery hit-testing",
            "source_canvas_px": [CANVAS["width"], CANVAS["height"]],
        },
        "preflight": extraction["preflight"],
        "visible_grammar": {
            "chart_type": "spatial_point_map",
            "left_panel": "categorical region spots",
            "right_panels": "eight colour-mapped spot maps",
            "coordinate_model": "relative map coordinates only; no physical axes are printed",
            "mark_origin": "direct PDF vector-drawn circle marks",
        },
        "recoverable_representation": {
            "left_map": "426 categorical spot centres, fills, and relative positions",
            "right_maps": "3424 spot centres and rendered fills across eight displayed cell-type maps",
            "colour_values": "nearest-CIELAB matches to the printed colourbar, retained only as visible display approximations",
        },
        "counts": {
            "region_spots_total": len(regions),
            "region_spots_by_category": region_counts,
            "colour_mapped_spots_total": len(probabilities),
            "colour_mapped_spots_by_map": map_counts,
            "primary_csv_rows": len(rows),
        },
        "colourbar_display_calibration": extraction["colourbar_calibration"],
        "outputs": {
            "primary_csv": "data.csv",
            "region_spots_csv": "region-spots-visible.csv",
            "probability_spots_csv": "probability-spots-visible.csv",
            "original": "original.png",
            "overlay": "overlay.png",
            "recreated": "recreated.png",
            "preflight_report": "preflight-report.json",
            "figure_spec": "figure-spec.json",
        },
        "limitations": extraction["not_recovered"],
        "review_required": extraction["review_required"],
    }
    write_json(output_dir / "report.json", report)
    write_json(
        output_dir / "manifest.json",
        {
            "schema_version": 1,
            "case_id": CASE_ID,
            "chart_type": "spatial_point_map",
            "status": "partial_visible",
            "assets": report["outputs"],
            "counts": report["counts"],
        },
    )
    (output_dir / "README.md").write_text(
        "# Nature Communications Fig. 5a — spatial point map\n\n"
        "This gallery case is a candidate, case-specific recovery of visible PDF-vector point marks. "
        "`data.csv` contains the 426 categorical-region spots and 3,424 colour-mapped spots that are directly visible in the figure. "
        "The right-map `value` field is an approximation from the printed colourbar and is never author raw data. "
        "No physical spatial coordinates, cell IDs, or unrendered probabilistic values are claimed.\n",
        encoding="utf-8",
    )
    (output_dir / "SOURCES.md").write_text(
        "# Sources\n\n"
        "- Article: https://www.nature.com/articles/s41467-024-51329-2\n"
        "- Figure: https://www.nature.com/articles/s41467-024-51329-2/figures/5\n"
        "- Published panel: Figure 5a, PDF page 10.\n\n"
        "Only visible figure/PDF-vector evidence is used for the public extraction CSV.\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build(args.source.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()

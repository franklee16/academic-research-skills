"""Build a reproducible visible-evidence bundle for the Gakedaban ΔT map.

The public figure is a raster-only filled contour/isogram map.  This builder
uses the candidate contour-map extractor only for visibly rendered colour
classes and ink.  It does not claim the survey observations, gridded ΔT values,
interpolation procedure, or a numerical ΔT value at an arbitrary location.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASE_ROOT = REPO_ROOT / "outputs" / "china-mining-gakedaban-dt-300m"
DEFAULT_EXTRACTOR = Path(r"C:\Users\Liang\.agents\skills\thu-digitizer\scripts\candidate_digitize_contour_map.py")
DEFAULT_OUTPUT_NAME = "visible-contour-extraction-v2-full-legend"

SOURCE_PAGE_URL = "http://www.chinaminingmagazine.com/en/supplement/d54a6c83-9a62-493c-a673-b34c60773e73"
SOURCE_IMAGE_URL = "http://www.chinaminingmagazine.com/fileZGKY/journal/article/zgky/2024/S1/20240624-11.jpg"
ARTICLE_URL = "http://www.chinaminingmagazine.com/en/article/doi/10.12075/j.issn.1004-4051.20240624"

# Vertices were reviewed on the original raster and refined with a saturated-
# fill connected component only to follow the irregular outer survey boundary.
MAP_POLYGON = [
    (143, 80), (141, 874), (181, 976), (342, 990), (1257, 981),
    (1269, 565), (1312, 555), (1309, 318), (707, 313), (692, 79),
]

# The legend has 25 equally tall visible swatches.  Centres are listed bottom
# to top, so class index 1 begins at the printed 20 nT end of the legend.
LEGEND_SWATCH_CENTRES = [(1438, 1048 - 31 * index) for index in range(25)]
LEGEND_SWATCH_VALUE_NT = [20 + 20 * index for index in range(25)]

# Visible graticule anchors.  Degree components are retained separately rather
# than claiming an unprinted datum/CRS.
COORDINATE_ANCHORS = [
    {"axis": "longitude", "pixel_coordinate": 98.0, "degree_component": 163, "arcminute": 54, "label_visible": "163°54′"},
    {"axis": "longitude", "pixel_coordinate": 343.0, "degree_component": 163, "arcminute": 55, "label_visible": "163°55′"},
    {"axis": "longitude", "pixel_coordinate": 588.0, "degree_component": 163, "arcminute": 56, "label_visible": "163°56′"},
    {"axis": "longitude", "pixel_coordinate": 833.0, "degree_component": 163, "arcminute": 57, "label_visible": "163°57′"},
    {"axis": "longitude", "pixel_coordinate": 1078.0, "degree_component": 163, "arcminute": 58, "label_visible": "163°58′"},
    {"axis": "longitude", "pixel_coordinate": 1323.0, "degree_component": 163, "arcminute": 59, "label_visible": "163°59′"},
    {"axis": "latitude", "pixel_coordinate": 241.0, "degree_component": 40, "arcminute": 47, "label_visible": "40°47′"},
    {"axis": "latitude", "pixel_coordinate": 486.0, "degree_component": 40, "arcminute": 46, "label_visible": "40°46′"},
    {"axis": "latitude", "pixel_coordinate": 730.0, "degree_component": 40, "arcminute": 45, "label_visible": "40°45′"},
    {"axis": "latitude", "pixel_coordinate": 976.0, "degree_component": 40, "arcminute": 44, "label_visible": "40°44′"},
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def affine_fit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    xs = [float(row["pixel_coordinate"]) for row in rows]
    ys = [float(row["arcminute"]) for row in rows]
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    denominator = sum((value - mean_x) ** 2 for value in xs)
    slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / denominator
    intercept = mean_y - slope * mean_x
    residuals = [y - (slope * x + intercept) for x, y in zip(xs, ys)]
    return {
        "formula": "arcminute = slope * pixel_coordinate + intercept",
        "slope": slope,
        "intercept": intercept,
        "anchor_residual_arcminute": residuals,
        "max_abs_anchor_residual_arcminute": max(abs(value) for value in residuals),
    }


def run_candidate(source: Path, output: Path, extractor: Path) -> None:
    command = [
        sys.executable,
        str(extractor),
        "--input", str(source),
        "--output-dir", str(output),
        "--map-polygon", ";".join(f"{x},{y}" for x, y in MAP_POLYGON),
    ]
    for x, y in LEGEND_SWATCH_CENTRES:
        command.extend(["--legend-swatch-center", f"{x},{y}"])
    # These are class indices only.  They deliberately avoid inventing colour-
    # band boundaries from labels that are printed at every second swatch.
    command.extend([
        "--legend-break-values", ",".join(str(index) for index in range(26)),
        "--palette-tolerance-lab", "48",
        "--no-measurement-point-detection",
    ])
    subprocess.run(command, check=True)


def build_full_canvas_recreation(source: Path, output: Path) -> None:
    """Keep the recovered map distinct while retaining visible figure furniture.

    The contour candidate writes a source-sized canvas but intentionally leaves
    everything outside the map polygon blank.  That is useful for inspecting
    the recovered map alone, but a publication-style recreation also needs the
    visible legend, graticule labels, frame, and scale bar.  Preserve that
    non-map annotation layer directly from the raster rather than pretending it
    was numerically re-extracted.
    """
    map_only_path = output / "map_only_recreation.png"
    candidate_recreation_path = output / "map_recreation.png"
    candidate_recreation_path.replace(map_only_path)

    with Image.open(source) as original, Image.open(map_only_path) as map_only:
        if original.size != map_only.size:
            raise ValueError("Map-only reconstruction canvas differs from the source canvas")
        map_mask = Image.new("L", original.size, 0)
        ImageDraw.Draw(map_mask).polygon(MAP_POLYGON, fill=255)
        full_canvas = original.convert("RGB")
        full_canvas.paste(map_only.convert("RGB"), mask=map_mask)
        full_canvas.save(candidate_recreation_path)


def build(case_root: Path, output: Path, extractor: Path) -> None:
    source = case_root / "source.jpg"
    if not source.is_file():
        raise FileNotFoundError(source)
    if not extractor.is_file():
        raise FileNotFoundError(extractor)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Refusing to overwrite non-empty evidence directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    run_candidate(source, output, extractor)
    build_full_canvas_recreation(source, output)

    candidate = read_json(output / "extraction_report.json")
    with (output / "contour_bands.csv").open(encoding="utf-8-sig", newline="") as handle:
        candidate_bands = list(csv.DictReader(handle))
    if len(candidate_bands) != len(LEGEND_SWATCH_CENTRES):
        raise ValueError("Candidate output does not preserve the 25 visible legend swatches")

    visible_bands = []
    for index, candidate_band in enumerate(candidate_bands):
        displayed_value = LEGEND_SWATCH_VALUE_NT[index]
        direct_label = displayed_value % 40 == 20
        visible_bands.append({
            "band_id": candidate_band["band_id"],
            "legend_swatch_index_bottom_to_top": index + 1,
            "legend_swatch_x_px": LEGEND_SWATCH_CENTRES[index][0],
            "legend_swatch_y_px": LEGEND_SWATCH_CENTRES[index][1],
            "printed_legend_value_nT": displayed_value if direct_label else "",
            "derived_regular_step_value_nT": displayed_value,
            "value_status": "printed_legend_label" if direct_label else "derived_between_adjacent_printed_legend_labels",
            "palette_hex": candidate_band["palette_bgr"],
            "pixel_count": candidate_band["pixel_count"],
            "area_fraction_of_map": candidate_band["area_fraction_of_map"],
            "band_semantics": "visible_colour_swatch_class_only_not_a_point_value_or_source_grid",
        })
    write_csv(output / "visible_contour_bands.csv", visible_bands)
    write_csv(output / "coordinate_grid_anchors.csv", COORDINATE_ANCHORS)

    coordinate_calibration = {
        "coordinate_space": "degree_and_arcminute_labels_visible_on_graticule",
        "longitude": affine_fit([row for row in COORDINATE_ANCHORS if row["axis"] == "longitude"]),
        "latitude": affine_fit([row for row in COORDINATE_ANCHORS if row["axis"] == "latitude"]),
        "limitations": [
            "The figure does not print a datum, projection, or coordinate-reference-system identifier.",
            "The calibration is retained as a pixel-to-degree/arcminute display mapping; it is not a surveyed georeferencing claim.",
        ],
    }
    write_json(output / "coordinate_calibration.json", coordinate_calibration)

    summary = {
        "schema_version": 1,
        "case_id": "china-mining-gakedaban-dt-300m-isogram",
        "status": "candidate_partial_visible",
        "source": {
            "supplement_page_url": SOURCE_PAGE_URL,
            "image_url": SOURCE_IMAGE_URL,
            "article_url": ARTICLE_URL,
            "article_title": "Study on the anomaly characteristics of high-precision magnetic survey in the Gakedaban Area of the western section of East Kunlun",
            "article_doi": "10.12075/j.issn.1004-4051.20240624",
            "figure_title": "Isogram plan of extending 300 m above ΔT polarization",
            "input_sha256": candidate["source"]["sha256"],
            "input_image_size_px": candidate["image_size_px"],
        },
        "visible_grammar": {
            "chart_type": "filled_contour_or_isogram_map",
            "map_boundary": "irregular L-shaped visible filled region",
            "filled_colour_classes": 25,
            "full_canvas_recreation": "recovered map pixels inside the map polygon plus retained source-raster legend, graticule labels, frame, and scale bar",
            "contour_ink": "retained as a raster ink layer; it still contains graticule and label ink because no per-label annotation was introduced",
            "measurement_points": "none accepted; point detection was disabled because no dedicated point-mark grammar is visible",
        },
        "map_polygon_px": candidate["map_polygon_px"],
        "legend": {
            "displayed_unit": "ΔT / nT",
            "directly_printed_values_nT": [20 + 40 * index for index in range(13)],
            "regular_swatch_step_nT": 20,
            "value_rule": "Only every second swatch has a printed label. Intermediate 20 nT values are separately flagged as derived from the visibly uniform two-swatch spacing, not as author source data.",
            "candidate_class_index_is_not_physical_value": True,
        },
        "coordinate_calibration": coordinate_calibration,
        "candidate_quality": {
            "low_support_fraction_of_map": candidate["low_support_fraction_of_map"],
            "palette_tolerance_lab": candidate["parameters"]["palette_tolerance_lab"],
            "visual_review_required": True,
        },
        "files": {
            "source_image": "../source.jpg",
            "preflight_report": "../preflight-report.json",
            "figure_spec": "../figure-spec.json",
            "visible_band_summary": "visible_contour_bands.csv",
            "coordinate_grid_anchors": "coordinate_grid_anchors.csv",
            "coordinate_calibration": "coordinate_calibration.json",
            "candidate_grid": "contour_band_grid.npz",
            "candidate_band_csv": "contour_bands.csv",
            "map_only_recreation": "map_only_recreation.png",
            "map_recreation": "map_recreation.png",
            "semantic_overlay": "semantic_overlay.png",
            "candidate_report": "extraction_report.json",
        },
        "not_recovered": [
            "Raw magnetic-survey observations, station locations, and original gridded ΔT values.",
            "Interpolation, continuation, smoothing, contouring, or kriging settings.",
            "An exact ΔT value at an arbitrary map location inside a rendered colour class.",
            "A declared geodetic datum, projection, or CRS.",
        ],
    }
    write_json(output / "extraction_summary.json", summary)
    (output / "README.md").write_text(
        "# Visible extraction: Gakedaban ΔT isogram map\n\n"
        "This evidence bundle recovers the displayed colour-class grid, visible neutral ink, legend swatches, and printed graticule anchors. "
        "`map_recreation.png` is a full canvas: the recovered map appears inside its polygon while the visible legend, graticule labels, frame, and scale bar are retained as source-raster annotations; `map_only_recreation.png` isolates the recovered map. "
        "It is a candidate raster extraction, not the original magnetic-survey or interpolation dataset. "
        "Use `visible_contour_bands.csv` for the 25 visible legend swatches and `contour_band_grid.npz` for the per-pixel class grid.\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-root", type=Path, default=DEFAULT_CASE_ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--extractor", type=Path, default=DEFAULT_EXTRACTOR)
    args = parser.parse_args()
    case_root = args.case_root.resolve()
    output = (args.output or case_root / DEFAULT_OUTPUT_NAME).resolve()
    build(case_root, output, args.extractor.resolve())


if __name__ == "__main__":
    main()

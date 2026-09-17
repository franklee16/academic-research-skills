"""Publish the Gakedaban \u0394T filled-contour map as a gallery evidence case.

The public gallery bundle is deliberately limited to features visible in the
supplement raster: colour-band classes, printed legend labels, visible ink,
and graticule anchors.  It does not publish or imply source survey stations,
gridded magnetic values, interpolation parameters, or an unobserved CRS.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE = (
    REPO_ROOT
    / "outputs"
    / "china-mining-gakedaban-dt-300m"
    / "visible-contour-extraction-v2-full-legend"
)
DEFAULT_OUTPUT = REPO_ROOT / "gallery" / "assets" / "cases" / "china-mining-gakedaban-dt-300m"
DEFAULT_BASICS = REPO_ROOT / "gallery" / "data" / "basics.json"
CASE_ID = "china-mining-gakedaban-dt-300m"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def compose_full_canvas_overlay(source: Path, map_overlay: Path, destination: Path, polygon: list[list[float]]) -> None:
    """Place the map-only semantic evidence back on its original full canvas."""
    with Image.open(source) as original, Image.open(map_overlay) as overlay:
        if original.size != overlay.size:
            raise ValueError("Semantic overlay canvas differs from source canvas")
        mask = Image.new("L", original.size, 0)
        ImageDraw.Draw(mask).polygon([tuple(vertex) for vertex in polygon], fill=255)
        full_canvas = original.convert("RGB")
        full_canvas.paste(overlay.convert("RGB"), mask=mask)
        full_canvas.save(destination)


def gallery_sample() -> dict[str, Any]:
    """Return the homepage metadata; its fields match the visible-only contract."""
    root = f"assets/cases/{CASE_ID}"
    return {
        "id": CASE_ID,
        "title": "填色等值线地图",
        "subtitle": "高精度磁测 ΔT 上延 300 m",
        "status": "partial_visible",
        "statusLabel": "候选 · 可见色带与等值线",
        "description": "从《中国矿业》补图的栅格图像恢复不规则 L 形图域、25 个可见色带、图中等值线/文字墨线层，以及 10 个经纬度分格锚点。右侧图例每隔一个色带印有数值；未印刷的中间 20 nT 级别在表中单列为规则色带推导值，不冒充原始磁测数据。",
        "metrics": [
            {"label": "可见色带", "value": "25"},
            {"label": "直接图例值", "value": "13"},
            {"label": "格网锚点", "value": "10"},
        ],
        "metricNote": "下载 CSV 是可见图例色带的摘要；完整逐像素分类网格以 NPZ 证据资产保留。图像不能恢复原始磁测站点、作者栅格、插值/上延参数、任意位置 ΔT 值或坐标基准。",
        "articleUrl": "http://www.chinaminingmagazine.com/en/article/doi/10.12075/j.issn.1004-4051.20240624",
        "journal": "China Mining Magazine",
        "articleTitle": "Study on the anomaly characteristics of high-precision magnetic survey in the Gakedaban Area of the western section of East Kunlun",
        "figure": "Supplement — Isogram plan of extending 300 m above ΔT polarization",
        "figureUrl": "http://www.chinaminingmagazine.com/en/supplement/d54a6c83-9a62-493c-a673-b34c60773e73",
        "assets": {
            "original": f"{root}/original.jpg",
            "overlay": f"{root}/overlay.png",
            "recreated": f"{root}/recreated.png",
            "data": f"{root}/data.csv",
            "report": f"{root}/report.json",
        },
    }


def register_sample(basics_path: Path, sample: dict[str, Any]) -> None:
    """Replace this one generated card without disturbing unrelated cases."""
    basics = read_json(basics_path)
    samples = basics.get("samples", [])
    existing_index = next((index for index, item in enumerate(samples) if item.get("id") == CASE_ID), None)
    if existing_index is None:
        samples.append(sample)
    else:
        samples[existing_index] = sample
    basics["samples"] = samples
    write_json(basics_path, basics)


def build(evidence_dir: Path, output_dir: Path) -> dict[str, Any]:
    source_dir = evidence_dir.parent
    required = {
        source_dir / "source.jpg",
        evidence_dir / "visible_contour_bands.csv",
        evidence_dir / "contour_band_grid.npz",
        evidence_dir / "semantic_overlay.png",
        evidence_dir / "map_recreation.png",
        evidence_dir / "map_only_recreation.png",
        evidence_dir / "coordinate_grid_anchors.csv",
        evidence_dir / "coordinate_calibration.json",
        evidence_dir / "extraction_summary.json",
    }
    missing = sorted(str(path) for path in required if not path.is_file())
    if missing:
        raise FileNotFoundError("Missing contour-map evidence: " + ", ".join(missing))

    evidence_summary = read_json(evidence_dir / "extraction_summary.json")
    bands = read_csv(evidence_dir / "visible_contour_bands.csv")
    if len(bands) != 25:
        raise ValueError(f"Expected 25 visible legend bands, found {len(bands)}")
    printed_labels = [row for row in bands if row["value_status"] == "printed_legend_label"]
    derived_labels = [row for row in bands if row["value_status"] == "derived_between_adjacent_printed_legend_labels"]
    if len(printed_labels) != 13 or len(derived_labels) != 12:
        raise ValueError("Legend-label provenance no longer matches the reviewed 13/12 split")

    output_dir.mkdir(parents=True, exist_ok=True)
    copied = {
        source_dir / "source.jpg": "original.jpg",
        evidence_dir / "semantic_overlay.png": "map-only-semantic-overlay.png",
        evidence_dir / "map_recreation.png": "recreated.png",
        evidence_dir / "map_only_recreation.png": "map-only-recreation.png",
        evidence_dir / "visible_contour_bands.csv": "data.csv",
        evidence_dir / "contour_band_grid.npz": "visible-contour-band-grid.npz",
        evidence_dir / "coordinate_grid_anchors.csv": "coordinate-grid-anchors.csv",
        evidence_dir / "coordinate_calibration.json": "coordinate-calibration.json",
        evidence_dir / "extraction_summary.json": "evidence-summary.json",
    }
    for source, name in copied.items():
        copy(source, output_dir / name)
    compose_full_canvas_overlay(
        source_dir / "source.jpg",
        evidence_dir / "semantic_overlay.png",
        output_dir / "overlay.png",
        evidence_summary["map_polygon_px"],
    )

    source = evidence_summary["source"]
    report = {
        "schema_version": 1,
        "case_contract_version": 1,
        "case_id": CASE_ID,
        "status": "partial_visible",
        "extraction_status": "candidate_partial_visible",
        "claim": "visible_raster_filled_contour_colour_class_and_ink_recovery",
        "registered_route": "raster_contour_map_candidate",
        "registered_route_status": "candidate_only",
        "numeric_output_authorized_by_registered_route": False,
        "source_data_role": "not_provided_or_used",
        "source": {
            "supplement_page_url": source["supplement_page_url"],
            "image_url": source["image_url"],
            "article_url": source["article_url"],
            "article_title": source["article_title"],
            "article_doi": source["article_doi"],
            "figure_title": source["figure_title"],
            "sha256": source["input_sha256"],
            "image_size_px": source["input_image_size_px"],
            "license_status": "not_stated_on_the_source_page; retain as a local gallery evidence asset and obtain permission before any public redistribution",
        },
        "visible_grammar": evidence_summary["visible_grammar"],
        "recoverable_representation": {
            "map_polygon_source_pixels": evidence_summary["map_polygon_px"],
            "colour_classes": "one visible discrete legend class per accepted map pixel",
            "legend": "25 sampled swatches; 13 directly printed values and 12 explicitly derived intermediate regular steps",
            "ink": "neutral raster ink retained in the overlay; contour, graticule, and text remain a review layer rather than a clean vector contour set",
            "coordinate_mapping": "pixel to printed degree/arcminute graticule mapping only",
        },
        "legend": evidence_summary["legend"],
        "coordinate_calibration": evidence_summary["coordinate_calibration"],
        "candidate_quality": evidence_summary["candidate_quality"],
        "counts": {
            "visible_colour_classes": len(bands),
            "directly_printed_legend_labels": len(printed_labels),
            "derived_regular_step_labels": len(derived_labels),
            "accepted_measurement_points": 0,
            "graticule_anchors": 10,
        },
        "outputs": {
            "primary_csv": "data.csv",
            "visible_band_grid": "visible-contour-band-grid.npz",
            "coordinate_grid_anchors": "coordinate-grid-anchors.csv",
            "coordinate_calibration": "coordinate-calibration.json",
            "original": "original.jpg",
            "overlay": "overlay.png",
            "map_only_semantic_overlay": "map-only-semantic-overlay.png",
            "recreated": "recreated.png",
            "map_only_recreation": "map-only-recreation.png",
            "evidence_summary": "evidence-summary.json",
        },
        "full_canvas_recreation": "The map polygon is replaced with the visible-class reconstruction; legend, graticule labels, frame, and scale bar remain as source-raster annotation layers.",
        "limitations": evidence_summary["not_recovered"],
        "review_required": True,
    }
    write_json(output_dir / "report.json", report)
    write_json(
        output_dir / "manifest.json",
        {
            "schema_version": 1,
            "case_id": CASE_ID,
            "chart_type": "filled_contour_or_isogram_map",
            "status": "partial_visible",
            "assets": report["outputs"],
            "counts": report["counts"],
        },
    )
    (output_dir / "README.md").write_text(
        "# China Mining Magazine — Gakedaban ΔT isogram\n\n"
        "This gallery case publishes only visible raster evidence. `data.csv` summarises the 25 legend colour classes; `visible-contour-band-grid.npz` retains the per-pixel class grid used by the static recreation. "
        "The full recreation preserves the source-raster legend and other figure furniture outside the recovered map polygon. It does not represent original survey points, an author grid, or interpolation parameters.\n",
        encoding="utf-8",
    )
    (output_dir / "SOURCES.md").write_text(
        "# Sources and reuse notice\n\n"
        "- Article: http://www.chinaminingmagazine.com/en/article/doi/10.12075/j.issn.1004-4051.20240624\n"
        "- Supplement figure: http://www.chinaminingmagazine.com/en/supplement/d54a6c83-9a62-493c-a673-b34c60773e73\n"
        "- Direct raster: http://www.chinaminingmagazine.com/fileZGKY/journal/article/zgky/2024/S1/20240624-11.jpg\n\n"
        "The source page did not state a reuse licence during extraction. These assets are retained for local evidence and demonstration; confirm the publisher's permission before public redistribution.\n",
        encoding="utf-8",
    )
    return gallery_sample()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--register-basics", action="store_true")
    parser.add_argument("--basics", type=Path, default=DEFAULT_BASICS)
    args = parser.parse_args()
    sample = build(args.evidence.resolve(), args.output.resolve())
    if args.register_basics:
        register_sample(args.basics.resolve(), sample)
    print(json.dumps({"case_id": sample["id"], "output": str(args.output.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()

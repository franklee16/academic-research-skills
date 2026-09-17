"""Rebuild every retained UpSet gallery case from visible original pixels.

Official source files are used only for a separate validation table.  Primary
CSV rows, static recreations, interaction hit geometry, and reports come from
the registered lattice-composite candidate plus visibly verified labels.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

import numpy as np
import openpyxl
from PIL import Image, ImageDraw, ImageFont

try:
    from candidate_digitize_lattice_composite import extract_lattice_composite, write_outputs
    from figure_spec import write_figure_spec
    from source_coordinate_contract import file_sha256, raster_identity
    from thu_digitizer import build_preflight
except ImportError:  # pragma: no cover - package-style invocation
    from .candidate_digitize_lattice_composite import extract_lattice_composite, write_outputs
    from .figure_spec import write_figure_spec
    from .source_coordinate_contract import file_sha256, raster_identity
    from .thu_digitizer import build_preflight


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "gallery" / "assets" / "cases"
MANIFEST = ROOT / "gallery" / "data" / "basics.json"
FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")


def _font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT), size)


def _text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    value: Any,
    size: int,
    *,
    fill: str | tuple[int, int, int] = "#222222",
    anchor: str | None = None,
    bold: bool = False,
) -> None:
    draw.text(xy, str(value), font=_font(size, bold=bold), fill=fill, anchor=anchor)


def _vertical_text(
    canvas: Image.Image,
    xy: tuple[float, float],
    value: str,
    size: int,
    *,
    fill: str = "#222222",
) -> None:
    face = _font(size)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bounds = probe.textbbox((0, 0), value, font=face)
    label = Image.new("RGBA", (bounds[2] - bounds[0] + 8, bounds[3] - bounds[1] + 8), (255, 255, 255, 0))
    ImageDraw.Draw(label).text((4 - bounds[0], 4 - bounds[1]), value, font=face, fill=fill)
    label = label.rotate(90, expand=True)
    canvas.paste(label, (round(xy[0] - label.width / 2), round(xy[1] - label.height / 2)), label)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def config_19006(original: Path) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "source": raster_identity(original).as_dict(),
        "layers": {
            "column_bars": {
                "role": "column_bar",
                "roi": [185, 70, 1080, 501],
                "color": [59, 59, 59],
                "color_verification": "verified",
                "tolerance": 0,
                "width_range": [30, 40],
            },
            "row_bars": {
                "role": "membership_guides",
                "roi": [190, 503, 1080, 607],
                "colors": [[229, 229, 229], [232, 232, 232]],
                "color_verification": "verified",
                "tolerance": 0,
                "height_range": [7, 15],
                "min_area": 100,
                "min_row_pixels": 20,
            },
            "membership": {
                "color": [59, 59, 59],
                "color_verification": "verified",
                "tolerance": 2,
                "patch_radius": 7,
                "active_fraction_min": 0.25,
                "inactive_fraction_max": 0.18,
            },
        },
        "semantics": {
            "verification": "verified",
            "column_ids": [f"I{index:02d}" for index in range(1, 16)],
            "column_values": [1857, 709, 565, 495, 458, 444, 355, 308, 298, 273, 249, 207, 178, 158, 121],
            "row_ids": ["FunC-2", "FunC-4", "FunC-3", "FunC-1"],
            "row_types": [],
        },
        "validation": {
            "max_spacing_cv": 0.02,
            "row_value_axis": [],
            "row_bar_edge_offset_px": 0,
            "row_total_max_abs_error": None,
            "top_value_max_abs_error": 8,
        },
    }


def config_28348(original: Path) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "source": raster_identity(original).as_dict(),
        "layers": {
            "column_bars": {
                "role": "membership_guides",
                "roi": [275, 350, 995, 380],
                "color": [217, 95, 2],
                "color_verification": "verified",
                "tolerance": 0,
                "width_range": [20, 30],
            },
            "row_bars": {
                "role": "row_bar",
                "roi": [60, 327, 276, 638],
                "colors": [[190, 99, 29], [101, 149, 47], [207, 65, 137], [124, 120, 171], [29, 170, 175]],
                "color_verification": "verified",
                "tolerance": 0,
                "height_range": [35, 55],
                "min_area": 1000,
                "min_row_pixels": 30,
            },
            "membership": {
                "colors": [[217, 95, 2], [102, 166, 30], [231, 41, 138], [117, 112, 179], [4, 193, 200]],
                "color_verification": "verified",
                "tolerance": 0,
                "patch_radius": 13,
                "active_fraction_min": 0.3,
                "inactive_fraction_max": 0.02,
            },
        },
        "semantics": {
            "verification": "verified",
            "column_ids": [f"I{index:02d}" for index in range(1, 13)],
            "column_values": [3219, 1929, 1347, 878, 818, 249, 206, 121, 14, 3, 1, 1],
            "row_ids": ["Direct Match", "Non-Synon", "Position-Specific", "Diagnosis Match", "AMP Tier I"],
            "row_types": [],
        },
        "validation": {
            "max_spacing_cv": 0.02,
            "row_value_axis": [],
            "row_bar_edge_offset_px": 0,
            "row_total_max_abs_error": None,
            "top_value_max_abs_error": None,
        },
    }


def _top_geometry(case_id: str, bar: dict[str, Any]) -> tuple[float, float, float, float]:
    if case_id == "nature-19006-fig2b":
        return float(bar["left_px"]), float(bar["top_px"]), float(bar["right_px"]), float(bar["bottom_px"])
    values = np.asarray([0, 500, 1000, 1500, 2000, 2500, 3000], dtype=float)
    pixels = np.asarray([326, 281, 235, 190, 144, 98, 53], dtype=float)
    slope, intercept = np.polyfit(values, pixels, 1)
    top = float(slope * float(bar["value"]) + intercept)
    return float(bar["pixel_x"]) - 22.5, top, float(bar["pixel_x"]) + 22.5, 326.0


def _primary_rows(case_id: str, report: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    inset_y = {"FunC-4": 92, "FunC-3": 141, "FunC-2": 191, "FunC-1": 240}
    for row_bar in report["row_bars"]:
        row_id = str(row_bar["row_id"])
        if case_id == "nature-19006-fig2b":
            hit_y = inset_y[row_id] - 20
            hit_x = 836
            hit_width = float(row_bar["derived_total"]) * 257 / 4300
            hit_height = 40
        else:
            hit_x = float(row_bar["left_px"])
            hit_y = float(row_bar["top_px"])
            hit_width = float(row_bar["right_px"] - row_bar["left_px"])
            hit_height = float(row_bar["bottom_px"] - row_bar["top_px"])
        rows.append({
            "record_id": len(rows) + 1,
            "kind": "set_total",
            "shape": "rect",
            "set": row_id,
            "value": int(round(float(row_bar["derived_total"]))),
            "value_status": "derived_from_visible_intersections_and_memberships",
            "guide_role": row_bar["guide_role"],
            "pixel_x": hit_x + hit_width / 2,
            "pixel_y": hit_y + hit_height / 2,
            "guide_left_px": int(row_bar["left_px"]),
            "guide_right_px": int(row_bar["right_px"]),
            "left_bar_left_px": int(row_bar["left_px"]) if row_bar["guide_role"] == "row_bar" else "",
            "left_bar_right_px": int(row_bar["right_px"]) if row_bar["guide_role"] == "row_bar" else "",
            "hit_x": hit_x,
            "hit_y": hit_y,
            "width": hit_width,
            "height": hit_height,
        })
    for bar in report["column_bars"]:
        left, top, right, bottom = _top_geometry(case_id, bar)
        members = ";".join(str(item) for item in bar["members"])
        rows.append({
            "record_id": len(rows) + 1,
            "kind": "intersection",
            "shape": "rect",
            "intersection": int(bar["column_index"]),
            "column_id": bar["column_id"],
            "members": members,
            "combination": "+".join(str(item) for item in bar["members"]),
            "count": int(bar["value"]),
            "member_count": int(bar["member_count"]),
            "value_status": "visible_printed_value_and_original_pixel_membership",
            "guide_role": bar["guide_role"],
            "bar_geometry_status": (
                "original_pixel_detected"
                if bar["guide_role"] == "column_bar"
                else "calibrated_from_visible_value_axis_for_interaction"
            ),
            "pixel_x": float(bar["pixel_x"]),
            "pixel_y": (top + bottom) / 2,
            "bar_left_x_px": left,
            "bar_top_y_px": top,
            "bar_right_x_px": right,
            "bar_bottom_y_px": bottom,
            "hit_x": left,
            "hit_y": top,
            "width": right - left,
            "height": max(8.0, bottom - top),
        })
    for cell in report["cells"]:
        if cell["status"] != "active":
            continue
        rows.append({
            "record_id": len(rows) + 1,
            "kind": "membership_cell",
            "shape": "circle",
            "intersection": int(cell["column_index"]),
            "column_id": cell["column_id"],
            "set": cell["row_id"],
            "present": "yes",
            "cell_status": cell["status"],
            "foreground_fraction": round(float(cell["foreground_fraction"]), 6),
            "value_status": "original_pixel_active_membership",
            "pixel_x": float(cell["pixel_x"]),
            "pixel_y": float(cell["pixel_y"]),
            "radius": 13 if case_id == "nature-28348-fig7" else 8,
        })
    return rows


def _render_19006(original: Image.Image, report: dict[str, Any]) -> Image.Image:
    canvas = Image.new("RGB", original.size, "white")
    draw = ImageDraw.Draw(canvas)
    dark = "#3b3b3b"
    _text(draw, (31, 18), "b", 28, bold=True)
    draw.line((157, 24, 157, 609), fill="#222222", width=2)
    draw.line((157, 498, 1105, 498), fill="#222222", width=2)
    draw.line((157, 609, 1105, 609), fill="#222222", width=2)
    y_value = lambda value: 498 - value * (498 - 56) / 2000
    for tick in (0, 500, 1000, 1500, 2000):
        y = y_value(tick)
        draw.line((151, y, 157, y), fill="#222222", width=2)
        _text(draw, (142, y), tick, 21, anchor="rm")
    _vertical_text(canvas, (78, 280), "Intersection Size", 24)
    row_map = {str(row["row_id"]): row for row in report["row_bars"]}
    for index, row_id in enumerate(["FunC-2", "FunC-4", "FunC-3", "FunC-1"]):
        y = float(row_map[row_id]["pixel_y"])
        if index % 2:
            draw.rectangle((157, round(y - 13), 1105, round(y + 13)), fill="#f8f8f8")
        _text(draw, (143, y), row_id, 20, anchor="rm")
    cells = {(cell["column_index"], cell["row_id"]): cell for cell in report["cells"]}
    for bar in report["column_bars"]:
        draw.rectangle((bar["left_px"], bar["top_px"], bar["right_px"] - 1, bar["bottom_px"] - 1), fill=dark)
        _text(draw, (bar["pixel_x"], bar["top_px"] - 11), bar["value"], 17, anchor="ms", fill="#444444")
        active_y = [float(row_map[name]["pixel_y"]) for name in bar["members"]]
        if len(active_y) > 1:
            draw.line((bar["pixel_x"], min(active_y), bar["pixel_x"], max(active_y)), fill=dark, width=3)
        for row_id, row in row_map.items():
            y = float(row["pixel_y"])
            active = cells[(bar["column_index"], row_id)]["status"] == "active"
            radius = 6 if active else 5
            colour = dark if active else "#e8e8e8"
            draw.ellipse((bar["pixel_x"] - radius, y - radius, bar["pixel_x"] + radius, y + radius), fill=colour)

    inset_colours = {"FunC-4": "#984ea3", "FunC-3": "#4daf4a", "FunC-2": "#377eb8", "FunC-1": "#e41a1c"}
    inset_y = {"FunC-4": 92, "FunC-3": 141, "FunC-2": 191, "FunC-1": 240}
    draw.line((836, 68, 836, 264), fill="#222222", width=2)
    draw.line((836, 264, 1093, 264), fill="#222222", width=2)
    for row_id in ["FunC-4", "FunC-3", "FunC-2", "FunC-1"]:
        y = inset_y[row_id]
        total = float(row_map[row_id]["derived_total"])
        right = 836 + total * 257 / 4300
        draw.rectangle((836, y - 22, right, y + 22), fill=inset_colours[row_id])
        _text(draw, (821, y), row_id, 20, anchor="rm")
    for tick in (0, 1000, 2000, 3000, 4000):
        x = 836 + tick * 257 / 4300
        draw.line((x, 264, x, 270), fill="#222222", width=2)
        _text(draw, (x, 277), tick, 18, anchor="ma")
    _text(draw, (965, 313), "Sum of unique KO annotations", 21, anchor="mm")
    return canvas


def _render_28348(original: Image.Image, report: dict[str, Any]) -> Image.Image:
    canvas = Image.new("RGB", original.size, "white")
    draw = ImageDraw.Draw(canvas)
    dark = "#414141"
    value_ticks = [0, 500, 1000, 1500, 2000, 2500, 3000]
    tick_pixels = [326, 281, 235, 190, 144, 98, 53]
    slope, intercept = np.polyfit(np.asarray(value_ticks, dtype=float), np.asarray(tick_pixels, dtype=float), 1)
    for tick, y in zip(value_ticks, tick_pixels):
        draw.line((275, y, 999, y), fill="#cccccc", width=3)
        _text(draw, (266, y), tick, 22, anchor="rm")
    draw.line((275, 19, 275, 326), fill="#cccccc", width=3)
    _vertical_text(canvas, (145, 183), "Intersection Size\n(Samples)", 26)
    for bar in report["column_bars"]:
        top = float(slope * float(bar["value"]) + intercept)
        x = float(bar["pixel_x"])
        visible_top = min(324, round(top))
        draw.rectangle((round(x - 22.5), visible_top, round(x + 22.5), 325), fill=dark)
        _text(draw, (x, min(top, 324) - 10), bar["value"], 24, anchor="ms")

    draw.rectangle((35, 327, 275, 638), fill="#cacaca")
    draw.line((64, 327, 64, 638), fill="#666666", width=2)
    row_colours = {
        "Direct Match": "#be631d", "Non-Synon": "#65952f", "Position-Specific": "#cf4189",
        "Diagnosis Match": "#7c78ab", "AMP Tier I": "#1daaae",
    }
    node_colours = {
        "Direct Match": "#d95f02", "Non-Synon": "#66a61e", "Position-Specific": "#e7298a",
        "Diagnosis Match": "#7570b3", "AMP Tier I": "#04c1c8",
    }
    row_map = {str(row["row_id"]): row for row in report["row_bars"]}
    for row_id, row in row_map.items():
        draw.rectangle((row["left_px"], row["top_px"], row["right_px"] - 1, row["bottom_px"] - 1), fill=row_colours[row_id], outline="#111111", width=2)
        _text(draw, (row["left_px"] - 8, row["pixel_y"]), int(row["derived_total"]), 22, anchor="rm")
        draw.line((275, row["pixel_y"], 999, row["pixel_y"]), fill="#cccccc", width=3)
    _text(draw, (37, 283), "Union\n8786", 24, anchor="mm")
    _text(draw, (38, 695), "Total\n9961", 24, anchor="mm")
    _text(draw, (143, 736), "Samples", 27, anchor="mm")

    for bar in report["column_bars"]:
        x = float(bar["pixel_x"])
        draw.line((x, 327, x, 638), fill="#cccccc", width=3)
        active_y = [float(row_map[name]["pixel_y"]) for name in bar["members"]]
        if len(active_y) > 1:
            draw.line((x, min(active_y), x, max(active_y)), fill="#111111", width=5)
        for row_id in bar["members"]:
            y = float(row_map[row_id]["pixel_y"])
            draw.ellipse((x - 14, y - 14, x + 14, y + 14), fill=node_colours[row_id], outline="#111111", width=2)

    legend = ["Direct Match", "Non-Synon", "Position-Specific", "Diagnosis Match", "AMP Tier I"]
    positions = [(240, 716), (240, 750), (493, 716), (493, 750), (794, 716)]
    for row_id, (x, y) in zip(legend, positions):
        draw.rectangle((x, y - 12, x + 50, y + 7), fill=node_colours[row_id], outline="#111111")
        _text(draw, (x + 67, y - 2), row_id, 21, anchor="lm")
    return canvas


def _source_validation_19006(
    report: dict[str, Any], root: Path
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source = root / "source-reference.csv"
    if not source.is_file():
        return [], {"status": "source_not_available_locally", "path": str(source)}
    counts: dict[tuple[int, int, int, int], int] = {}
    with source.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            mask = tuple(int(row[f"FunC_{index}"]) for index in range(1, 5))
            counts[mask] = int(row["count"])
    source_rows = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    order = ["FunC-1", "FunC-2", "FunC-3", "FunC-4"]
    rows = []
    for bar, (mask, count) in zip(report["column_bars"], source_rows):
        source_members = {name for name, active in zip(order, mask) if active}
        extracted_members = set(bar["members"])
        rows.append({
            "intersection": bar["column_index"],
            "visible_count": bar["value"],
            "source_count": count,
            "count_error": int(bar["value"]) - count,
            "visible_members": ";".join(bar["members"]),
            "source_members": ";".join(name for name in order if name in source_members),
            "membership_match": extracted_members == source_members,
            "validation_status": "validated" if int(bar["value"]) == count and extracted_members == source_members else "mismatch",
        })
    return rows, {
        "status": "validated",
        "path": str(source.relative_to(ROOT)),
        "sha256": file_sha256(source),
        "role": "committed_summary_derived_from_official_fig2b_tsv",
        "upstream_file": "Source Data/fig2b.tsv",
        "upstream_sha256": "b8e56cf1e3276837ef40524ebe6e189a235ff0ecadd35cc032094729cbaf636f",
    }


def _source_validation_28348(report: dict[str, Any], source: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not source.is_file():
        return [], {"status": "source_not_available_locally", "path": str(source)}
    values = list(openpyxl.load_workbook(source, read_only=True, data_only=True)["Figure 7"].values)
    header_index = next(index for index, row in enumerate(values) if row and row[0] == "AMP Tier I" and len(row) > 5)
    header = list(values[header_index][:5])
    source_rows = []
    for row in values[header_index + 1:]:
        if row and isinstance(row[5], (int, float)):
            source_rows.append(({str(header[index]) for index, value in enumerate(row[:5]) if value}, int(row[5])))
    source_rows.sort(key=lambda item: item[1], reverse=True)
    rows = []
    for bar, (members, count) in zip(report["column_bars"], source_rows):
        extracted_members = set(bar["members"])
        rows.append({
            "intersection": bar["column_index"],
            "visible_count": bar["value"],
            "source_count": count,
            "count_error": int(bar["value"]) - count,
            "visible_members": ";".join(bar["members"]),
            "source_members": ";".join(str(item) for item in header if str(item) in members),
            "membership_match": extracted_members == members,
            "validation_status": "validated" if int(bar["value"]) == count and extracted_members == members else "mismatch",
        })
    return rows, {"status": "validated", "path": "source-data.xlsx", "sha256": file_sha256(source)}


def _build(case_id: str) -> dict[str, Any]:
    root = CASES / case_id
    original_path = root / "original.png"
    if not original_path.is_file():
        raise FileNotFoundError(original_path)
    config = config_19006(original_path) if case_id == "nature-19006-fig2b" else config_28348(original_path)
    report = extract_lattice_composite(original_path, config)
    if not report["numeric_output_authorized"]:
        raise RuntimeError(f"{case_id}: {report['reason']}")
    (root / "lattice-config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "lattice-candidate-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix=f"{case_id}-") as directory:
        evidence = Path(directory)
        write_outputs(original_path, report, evidence)
        shutil.copy2(evidence / "geometry.csv", root / "lattice-geometry.csv")
        shutil.copy2(evidence / "overlay.png", root / "overlay.png")

    rows = _primary_rows(case_id, report)
    _write_csv(root / "data.csv", rows)
    _write_csv(root / "data-image-extracted.csv", rows)
    with Image.open(original_path) as source_image:
        original = source_image.convert("RGB")
    recreated = _render_19006(original, report) if case_id == "nature-19006-fig2b" else _render_28348(original, report)
    if recreated.size != original.size:
        raise ValueError(f"{case_id}: recreation canvas mismatch")
    recreated.save(root / "recreated.png")

    if case_id == "nature-19006-fig2b":
        validation_rows, source_info = _source_validation_19006(report, root)
        article_url = "https://www.nature.com/articles/s41467-020-19006-2"
        figure = "Fig. 2b"
    else:
        validation_rows, source_info = _source_validation_28348(report, root / "source-data.xlsx")
        article_url = "https://www.nature.com/articles/s41467-022-28348-y"
        figure = "Fig. 7"
    _write_csv(root / "source-validation.csv", validation_rows or [{"validation_status": source_info["status"]}])

    preflight, figure_spec = build_preflight(original_path, chart_type="upset")
    (root / "preflight-report.json").write_text(json.dumps(preflight, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_figure_spec(root / "figure-spec.json", figure_spec)
    mismatches = sum(row.get("validation_status") != "validated" for row in validation_rows)
    public_report = {
        "schema_version": 1,
        "case_id": case_id,
        "status": "visible_geometry_candidate",
        "article_url": article_url,
        "figure": figure,
        "input": raster_identity(original_path).as_dict(),
        "visible_extraction": {
            "extractor": report["extractor"],
            "algorithm_version": report["algorithm_version"],
            "deterministic_run_id": report["deterministic_run_id"],
            "numeric_output_authorized": report["numeric_output_authorized"],
            "column_guide_role": report["geometry"]["column_guide_role"],
            "row_guide_role": report["geometry"]["row_guide_role"],
        },
        "coverage": {
            "intersections": report["geometry"]["column_count"],
            "set_rows": report["geometry"]["row_count"],
            "membership_grid_cells": report["geometry"]["cell_count"],
            "active_membership_nodes": report["geometry"]["active_cell_count"],
            "ambiguous_membership_nodes": report["geometry"]["ambiguous_cell_count"],
        },
        "validation": {
            "candidate_spacing_status": report["validation"]["spacing_status"],
            "top_bars_vs_values": report["validation"]["top_bars_vs_values"],
            "official_source": source_info,
            "source_mismatch_count": mismatches,
        },
        "source_data_role": "independent_validation_only",
        "limitations": [
            "Intersection values and row labels are visibly transcribed; geometry and memberships are original-pixel detections.",
            "The retained official-source reference validates the immutable image-derived table but never replaces it.",
            "The candidate recovers visible plotted summaries, not hidden observations or connector semantics.",
        ],
    }
    (root / "report.json").write_text(json.dumps(public_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return public_report


def build_case_19006() -> dict[str, Any]:
    return _build("nature-19006-fig2b")


def build_case_28348() -> dict[str, Any]:
    return _build("nature-28348-fig7")


def _manifest_entry(case_id: str, report: dict[str, Any]) -> dict[str, Any]:
    if case_id == "nature-19006-fig2b":
        title, subtitle = "UpSet 复合图", "Functional intersections across four FunC sets"
        article_title = "Integration of time-series meta-omics data reveals how microbial ecosystems respond to disturbance"
        article_url = report["article_url"]
        figure, figure_url = "Fig. 2b", f"{article_url}/figures/2"
        description = "从原图恢复 15 个交集柱、4×15 成员格阵和 32 个激活节点；独立 inset 仅用于显示由可见交集推导的集合总量。"
    else:
        title, subtitle = "UpSet 复合图", "Therapeutic-match intersections across samples"
        article_title = "A platform for oncogenomic reporting and interpretation"
        article_url = report["article_url"]
        figure, figure_url = "Fig. 7", f"{article_url}/figures/7"
        description = "从原图恢复 12 个交集、5×12 成员格阵和 40 个多色激活节点；工作簿只作为独立验证。"
    root = f"assets/cases/{case_id}"
    return {
        "id": case_id,
        "title": title,
        "subtitle": subtitle,
        "status": "visible_geometry_candidate",
        "statusLabel": "真实图 · 原像素候选",
        "description": description,
        "metrics": [
            {"label": "visible intersections", "value": str(report["coverage"]["intersections"])},
            {"label": "active membership nodes", "value": str(report["coverage"]["active_membership_nodes"])},
        ],
        "journal": "Nature Communications",
        "articleTitle": article_title,
        "articleUrl": article_url,
        "figure": figure,
        "figureUrl": figure_url,
        "assets": {
            "original": f"{root}/original.png",
            "overlay": f"{root}/overlay.png",
            "recreated": f"{root}/recreated.png",
            "data": f"{root}/data-image-extracted.csv",
            "report": f"{root}/report.json",
        },
        "styleSpec": {
            "renderer": "paper-visible-upset",
            "rasterEvidenceInteractive": True,
            "fidelity": "visible_geometry_candidate",
            "label": "Original-pixel lattice recreation",
            "note": "交互层复用同尺寸复现底图；命中区域直接来自原图像素 CSV。",
            "canvas": {"width": report["input"]["width"], "height": report["input"]["height"]},
            "fontFamily": "Arial, Helvetica, sans-serif",
        },
    }


def update_manifest(reports: dict[str, dict[str, Any]]) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    case_ids = list(reports)
    samples = [sample for sample in manifest["samples"] if sample["id"] not in case_ids]
    insertion = next((index for index, sample in enumerate(samples) if sample["id"] == "nature-27341-fig1"), len(samples))
    entries = [_manifest_entry(case_id, reports[case_id]) for case_id in case_ids]
    manifest["samples"] = samples[:insertion] + entries + samples[insertion:]
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=["19006", "28348", "all"], default="all")
    args = parser.parse_args()
    reports: dict[str, dict[str, Any]] = {}
    if args.case in {"19006", "all"}:
        reports["nature-19006-fig2b"] = build_case_19006()
    if args.case in {"28348", "all"}:
        reports["nature-28348-fig7"] = build_case_28348()
    update_manifest(reports)
    print(json.dumps({case_id: report["coverage"] for case_id, report in reports.items()}, ensure_ascii=False))


if __name__ == "__main__":
    main()

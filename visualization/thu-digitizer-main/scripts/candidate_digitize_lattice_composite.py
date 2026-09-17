"""Extract aligned bars and a categorical membership lattice from a raster.

The implementation is deliberately configuration-driven.  It detects repeated
row/column geometry from the original raster and classifies every lattice cell
as active, inactive, or ambiguous.  Semantic labels and printed values may be
supplied only as separately verified configuration; they never alter detected
geometry.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np
from PIL import Image, ImageDraw

try:
    from raster_digitizer_core import AxisCalibration
    from source_coordinate_contract import (
        ORIGINAL_RASTER_SPACE,
        assert_original_raster,
        raster_identity,
    )
except ImportError:  # pragma: no cover - package-style import
    from .raster_digitizer_core import AxisCalibration
    from .source_coordinate_contract import (
        ORIGINAL_RASTER_SPACE,
        assert_original_raster,
        raster_identity,
    )


ALGORITHM_VERSION = "lattice-composite-original-pixel-v2"


def _runs(indices: Iterable[int]) -> list[tuple[int, int]]:
    values = [int(value) for value in indices]
    if not values:
        return []
    result: list[tuple[int, int]] = []
    start = previous = values[0]
    for value in values[1:]:
        if value > previous + 1:
            result.append((start, previous + 1))
            start = value
        previous = value
    result.append((start, previous + 1))
    return result


def _rgb(value: Sequence[int] | str | None, *, path: str) -> tuple[int, int, int]:
    if value is None:
        raise ValueError(f"{path} must be verified before extraction")
    if isinstance(value, str):
        text = value.strip().lstrip("#")
        if len(text) != 6:
            raise ValueError(f"{path} must be #RRGGBB or three RGB channels")
        try:
            channels = tuple(int(text[index:index + 2], 16) for index in (0, 2, 4))
        except ValueError as exc:
            raise ValueError(f"{path} must be #RRGGBB or three RGB channels") from exc
    else:
        channels = tuple(int(channel) for channel in value)
    if len(channels) != 3 or any(channel < 0 or channel > 255 for channel in channels):
        raise ValueError(f"{path} must contain three channels in 0..255")
    return channels  # type: ignore[return-value]


def _mask(rgb: np.ndarray, target: tuple[int, int, int], tolerance: float) -> np.ndarray:
    difference = rgb.astype(np.int32) - np.asarray(target, dtype=np.int32)
    return np.square(difference).sum(axis=2) <= float(tolerance) ** 2


def _colours(layer: dict[str, Any], *, path: str) -> list[tuple[int, int, int]]:
    raw = layer.get("colors")
    if raw in (None, []):
        raw = [layer.get("color")]
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"{path}.color or {path}.colors must be verified before extraction")
    return [_rgb(value, path=f"{path}.colors[{index}]") for index, value in enumerate(raw)]


def _layer_mask(rgb: np.ndarray, layer: dict[str, Any], *, path: str) -> np.ndarray:
    tolerance = float(layer.get("tolerance", 12))
    combined = np.zeros(rgb.shape[:2], dtype=bool)
    for colour in _colours(layer, path=path):
        combined |= _mask(rgb, colour, tolerance)
    return combined


def _bounds(layer: dict[str, Any], width: int, height: int, *, path: str) -> tuple[int, int, int, int]:
    if "roi" in layer:
        values = layer["roi"]
        if not isinstance(values, list) or len(values) != 4:
            raise ValueError(f"{path}.roi must contain left,top,right,bottom")
        left, top, right, bottom = (int(round(float(value))) for value in values)
    else:
        values = layer.get("roi_fraction")
        if not isinstance(values, list) or len(values) != 4:
            raise ValueError(f"{path} needs roi or roi_fraction")
        fractions = [float(value) for value in values]
        if any(value < 0 or value > 1 for value in fractions):
            raise ValueError(f"{path}.roi_fraction values must stay in 0..1")
        left, top, right, bottom = (
            int(round(fractions[0] * width)),
            int(round(fractions[1] * height)),
            int(round(fractions[2] * width)),
            int(round(fractions[3] * height)),
        )
    if not (0 <= left < right <= width and 0 <= top < bottom <= height):
        raise ValueError(f"{path} bounds must stay inside the original raster")
    return left, top, right, bottom


def _range(value: Any, *, path: str, default: tuple[int, int]) -> tuple[int, int]:
    if value is None:
        return default
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{path} must contain minimum and maximum")
    low, high = (int(item) for item in value)
    if low <= 0 or low > high:
        raise ValueError(f"{path} must satisfy 0 < minimum <= maximum")
    return low, high


def _spacing_diagnostics(centres: list[float]) -> dict[str, float | None]:
    if len(centres) < 2:
        return {"median": None, "coefficient_of_variation": None, "max_relative_deviation": None}
    gaps = np.diff(np.asarray(centres, dtype=float))
    median = float(np.median(gaps))
    return {
        "median": median,
        "coefficient_of_variation": float(np.std(gaps) / max(abs(np.mean(gaps)), 1e-12)),
        "max_relative_deviation": float(np.max(np.abs(gaps - median)) / max(abs(median), 1e-12)),
    }


def _detect_column_bars(
    mask: np.ndarray,
    *,
    roi: tuple[int, int, int, int],
    width_range: tuple[int, int],
    max_vertical_gap_px: int = 0,
    min_vertical_row_fraction: float = 0.6,
) -> tuple[list[dict[str, Any]], int]:
    if max_vertical_gap_px < 0:
        raise ValueError("max_vertical_gap_px must be non-negative")
    if not 0 < min_vertical_row_fraction <= 1:
        raise ValueError("min_vertical_row_fraction must stay in (0, 1]")
    left, top, right, bottom = roi
    candidates: list[tuple[int, int, list[tuple[int, int]]]] = []
    for y in range(top, bottom):
        local_runs = _runs(np.flatnonzero(mask[y, left:right]))
        bars = [
            (start + left, stop + left)
            for start, stop in local_runs
            if width_range[0] <= stop - start <= width_range[1]
        ]
        candidates.append((len(bars), y, bars))
    count, baseline_row, runs = max(candidates, key=lambda item: (item[0], item[1]))
    if count == 0:
        return [], baseline_row
    bars = []
    for start, stop in runs:
        center_x = (start + stop - 1) / 2
        width = stop - start
        required_pixels = max(1, int(np.ceil(width * min_vertical_row_fraction)))
        row_support = mask[top:baseline_row + 1, start:stop].sum(axis=1) >= required_pixels
        top_index = len(row_support) - 1
        gap = 0
        for index in range(len(row_support) - 1, -1, -1):
            if row_support[index]:
                top_index = index
                gap = 0
            else:
                gap += 1
                if gap > max_vertical_gap_px:
                    break
        bars.append({
            "pixel_x": center_x,
            "left_px": start,
            "right_px": stop,
            "top_px": top + top_index,
            "bottom_px": baseline_row + 1,
            "width_px": width,
            "max_vertical_gap_px": max_vertical_gap_px,
        })
    return bars, baseline_row


def _detect_row_bars(
    mask: np.ndarray,
    *,
    roi: tuple[int, int, int, int],
    height_range: tuple[int, int],
    min_area: int,
    min_row_pixels: int,
) -> list[dict[str, Any]]:
    left, top, right, bottom = roi
    local = mask[top:bottom, left:right]
    active_rows = np.flatnonzero(local.sum(axis=1) >= min_row_pixels)
    bars = []
    for local_top, local_bottom in _runs(active_rows):
        run_height = local_bottom - local_top
        if not height_range[0] <= run_height <= height_range[1]:
            continue
        ys, xs = np.where(local[local_top:local_bottom])
        if xs.size < min_area:
            continue
        absolute_top, absolute_bottom = top + local_top, top + local_bottom
        bars.append({
            "pixel_y": (absolute_top + absolute_bottom - 1) / 2,
            "top_px": absolute_top,
            "bottom_px": absolute_bottom,
            "left_px": int(xs.min()) + left,
            "right_px": int(xs.max()) + left + 1,
            "height_px": run_height,
            "area_px": int(xs.size),
        })
    return bars


def init_config(input_path: Path) -> dict[str, Any]:
    """Create a source-locked template; colours and semantics remain missing."""

    identity = raster_identity(input_path)
    return {
        "schema_version": 1,
        "source": identity.as_dict(),
        "layers": {
            "column_bars": {
                "role": "column_bar",
                "roi_fraction": [0.20, 0.02, 0.95, 0.72],
                "color": None,
                "color_verification": "missing",
                "tolerance": 12,
                "width_range": [3, max(6, round(identity.width * 0.03))],
                "max_vertical_gap_px": 0,
                "min_vertical_row_fraction": 1.0,
            },
            "row_bars": {
                "role": "row_bar",
                "roi_fraction": [0.0, 0.60, 0.30, 0.98],
                "color": None,
                "color_verification": "missing",
                "tolerance": 12,
                "height_range": [3, max(6, round(identity.height * 0.03))],
                "min_area": 20,
                "min_row_pixels": 3,
            },
            "membership": {
                "color": None,
                "color_verification": "missing",
                "tolerance": 12,
                "patch_radius": 7,
                "active_fraction_min": 0.35,
                "inactive_fraction_max": 0.05,
            },
        },
        "semantics": {
            "verification": "missing",
            "column_ids": [],
            "column_values": [],
            "row_ids": [],
            "row_types": [],
        },
        "validation": {
            "max_spacing_cv": 0.08,
            "row_value_axis": [],
            "row_bar_edge_offset_px": 0,
            "row_total_max_abs_error": None,
            "top_value_max_abs_error": None,
        },
    }


def _semantic_values(values: Any, count: int, *, name: str, required: bool = False) -> list[Any]:
    if values in (None, []):
        if required:
            raise ValueError(f"semantics.{name} must contain {count} verified entries")
        return []
    if not isinstance(values, list) or len(values) != count:
        raise ValueError(f"semantics.{name} must contain exactly {count} entries")
    return values


def extract_lattice_composite(input_path: Path, config: dict[str, Any]) -> dict[str, Any]:
    if config.get("schema_version") != 1:
        raise ValueError("config schema_version must equal 1")
    source = config.get("source")
    if not isinstance(source, dict):
        raise ValueError("config.source must be an original-raster identity object")
    identity = assert_original_raster(input_path, source)
    with Image.open(input_path) as image:
        rgb = np.asarray(image.convert("RGB"), dtype=np.uint8)
    height, width = rgb.shape[:2]

    layers = config.get("layers")
    if not isinstance(layers, dict):
        raise ValueError("config.layers must be an object")
    column_config = layers.get("column_bars")
    row_config = layers.get("row_bars")
    membership_config = layers.get("membership")
    if not all(isinstance(item, dict) for item in (column_config, row_config, membership_config)):
        raise ValueError("column_bars, row_bars, and membership layer configs are required")
    assert isinstance(column_config, dict) and isinstance(row_config, dict) and isinstance(membership_config, dict)
    for name, layer in (("column_bars", column_config), ("row_bars", row_config), ("membership", membership_config)):
        if layer.get("color_verification") != "verified":
            raise ValueError(f"layers.{name}.color_verification must equal 'verified'")

    column_mask = _layer_mask(rgb, column_config, path="layers.column_bars")
    row_mask = _layer_mask(rgb, row_config, path="layers.row_bars")
    node_mask = _layer_mask(rgb, membership_config, path="layers.membership")

    column_roi = _bounds(column_config, width, height, path="layers.column_bars")
    row_roi = _bounds(row_config, width, height, path="layers.row_bars")
    column_bars, baseline_row = _detect_column_bars(
        column_mask,
        roi=column_roi,
        width_range=_range(column_config.get("width_range"), path="layers.column_bars.width_range", default=(3, 60)),
        max_vertical_gap_px=int(column_config.get("max_vertical_gap_px", 0)),
        min_vertical_row_fraction=float(column_config.get("min_vertical_row_fraction", 0.6)),
    )
    row_bars = _detect_row_bars(
        row_mask,
        roi=row_roi,
        height_range=_range(row_config.get("height_range"), path="layers.row_bars.height_range", default=(3, 50)),
        min_area=int(row_config.get("min_area", 20)),
        min_row_pixels=int(row_config.get("min_row_pixels", 3)),
    )
    if not column_bars or not row_bars:
        raise ValueError(
            f"repeated geometry not found: {len(column_bars)} column bars and {len(row_bars)} row bars"
        )
    column_guide_role = str(column_config.get("role", "column_bar"))
    if column_guide_role not in {"column_bar", "membership_guides"}:
        raise ValueError("layers.column_bars.role must be column_bar or membership_guides")
    for column_bar in column_bars:
        column_bar["guide_role"] = column_guide_role
    row_guide_role = str(row_config.get("role", "row_bar"))
    if row_guide_role not in {"row_bar", "membership_guides"}:
        raise ValueError("layers.row_bars.role must be row_bar or membership_guides")
    for row_bar in row_bars:
        row_bar["guide_role"] = row_guide_role

    semantics = config.get("semantics", {})
    if not isinstance(semantics, dict):
        raise ValueError("config.semantics must be an object")
    column_ids = _semantic_values(semantics.get("column_ids"), len(column_bars), name="column_ids")
    row_ids = _semantic_values(semantics.get("row_ids"), len(row_bars), name="row_ids")
    column_values = _semantic_values(semantics.get("column_values"), len(column_bars), name="column_values")
    row_types = _semantic_values(semantics.get("row_types"), len(row_bars), name="row_types")
    if not column_ids:
        column_ids = [f"column-{index:02d}" for index in range(1, len(column_bars) + 1)]
    if not row_ids:
        row_ids = [f"row-{index:02d}" for index in range(1, len(row_bars) + 1)]

    patch_radius = int(membership_config.get("patch_radius", 7))
    if patch_radius < 1:
        raise ValueError("layers.membership.patch_radius must be positive")
    active_min = float(membership_config.get("active_fraction_min", 0.35))
    inactive_max = float(membership_config.get("inactive_fraction_max", 0.05))
    if not 0 <= inactive_max < active_min <= 1:
        raise ValueError("membership fractions must satisfy 0 <= inactive < active <= 1")

    cells = []
    members_by_column: list[list[str]] = []
    for column_index, (column_id, bar) in enumerate(zip(column_ids, column_bars), 1):
        members = []
        x = int(round(float(bar["pixel_x"])))
        for row_index, (row_id, row_bar) in enumerate(zip(row_ids, row_bars), 1):
            y = int(round(float(row_bar["pixel_y"])))
            patch = node_mask[
                max(0, y - patch_radius):min(height, y + patch_radius + 1),
                max(0, x - patch_radius):min(width, x + patch_radius + 1),
            ]
            fraction = float(np.mean(patch)) if patch.size else 0.0
            if fraction >= active_min:
                status = "active"
                members.append(str(row_id))
            elif fraction <= inactive_max:
                status = "inactive"
            else:
                status = "ambiguous"
            cells.append({
                "column_index": column_index,
                "column_id": column_id,
                "row_index": row_index,
                "row_id": row_id,
                "pixel_x": float(bar["pixel_x"]),
                "pixel_y": float(row_bar["pixel_y"]),
                "status": status,
                "foreground_fraction": fraction,
            })
        members_by_column.append(members)

    for index, (column_id, bar, members) in enumerate(zip(column_ids, column_bars, members_by_column), 1):
        bar.update({
            "column_index": index,
            "column_id": column_id,
            "value": column_values[index - 1] if column_values else None,
            "member_count": len(members),
            "members": members,
        })

    row_totals: dict[str, float] = {}
    if column_values:
        numeric_values = [float(value) for value in column_values]
        row_totals = {
            str(row_id): sum(value for value, members in zip(numeric_values, members_by_column) if str(row_id) in members)
            for row_id in row_ids
        }
    for index, (row_id, row_bar) in enumerate(zip(row_ids, row_bars), 1):
        row_bar.update({
            "row_index": index,
            "row_id": row_id,
            "row_type": row_types[index - 1] if row_types else None,
            "derived_total": row_totals.get(str(row_id)),
        })

    validation_config = config.get("validation", {})
    if not isinstance(validation_config, dict):
        raise ValueError("config.validation must be an object")
    column_spacing = _spacing_diagnostics([float(bar["pixel_x"]) for bar in column_bars])
    row_spacing = _spacing_diagnostics([float(bar["pixel_y"]) for bar in row_bars])
    max_spacing_cv = float(validation_config.get("max_spacing_cv", 0.08))
    spacing_ok = all(
        item["coefficient_of_variation"] is not None
        and float(item["coefficient_of_variation"]) <= max_spacing_cv
        for item in (column_spacing, row_spacing)
    )

    top_validation: dict[str, Any] = {"status": "not_applicable"}
    if column_values and column_guide_role == "column_bar":
        values = np.asarray([float(value) for value in column_values], dtype=float)
        tops = np.asarray([float(bar["top_px"]) for bar in column_bars], dtype=float)
        fit = np.polyfit(tops, values, 1)
        predictions = np.polyval(fit, tops)
        errors = predictions - values
        top_validation = {
            "status": "validated_against_verified_visible_values",
            "rmse": float(np.sqrt(np.mean(np.square(errors)))),
            "max_abs_error": float(np.max(np.abs(errors))),
        }
    elif column_values:
        top_validation = {
            "status": "not_applicable_membership_derived_column_guides",
            "reason": "column centres come from repeated membership glyphs, not value-bar edges",
        }

    row_validation: dict[str, Any] = {"status": "not_applicable", "rows": []}
    anchors = validation_config.get("row_value_axis", [])
    if anchors:
        if row_guide_role != "row_bar":
            raise ValueError("row_value_axis validation requires row_bar guides")
        if not row_totals:
            raise ValueError("row_value_axis validation requires verified column_values")
        if not isinstance(anchors, list):
            raise ValueError("validation.row_value_axis must be a list")
        calibration = AxisCalibration.fit(
            [(float(anchor["pixel"]), float(anchor["value"])) for anchor in anchors]
        )
        row_errors = []
        row_records = []
        edge_offset = float(validation_config.get("row_bar_edge_offset_px", 0))
        for row_bar in row_bars:
            estimate = calibration.value_at_pixel(float(row_bar["left_px"]) + edge_offset)
            error = estimate - float(row_bar["derived_total"])
            row_errors.append(error)
            row_records.append({
                "row_id": row_bar["row_id"],
                "derived_total": row_bar["derived_total"],
                "pixel_estimate": estimate,
                "pixel_minus_total": error,
                "edge_offset_px": edge_offset,
            })
            row_bar["pixel_total_estimate"] = estimate
            row_bar["pixel_total_error"] = error
        row_validation = {
            "status": "validated_against_independent_row_bar_geometry",
            "calibration": calibration.report(),
            "mae": float(np.mean(np.abs(row_errors))),
            "max_abs_error": float(np.max(np.abs(row_errors))),
            "rows": row_records,
        }

    ambiguous_count = sum(cell["status"] == "ambiguous" for cell in cells)
    reasons = []
    if ambiguous_count:
        reasons.append(f"{ambiguous_count} lattice cells are ambiguous")
    if not spacing_ok:
        reasons.append("row or column spacing exceeds the configured regularity gate")
    top_limit = validation_config.get("top_value_max_abs_error")
    if top_limit is not None and column_guide_role != "column_bar":
        reasons.append("top_value_max_abs_error requires column_bar guides")
    if top_limit is not None and top_validation.get("max_abs_error", 0) > float(top_limit):
        reasons.append("top-bar geometry disagrees with verified visible column values")
    row_limit = validation_config.get("row_total_max_abs_error")
    if row_limit is not None and row_validation.get("max_abs_error", 0) > float(row_limit):
        reasons.append("derived row totals disagree with independent row-bar geometry")
    semantics_verified = semantics.get("verification") == "verified"
    if column_values and not semantics_verified:
        reasons.append("visible semantic values are not marked verified")

    geometry_authorized = not ambiguous_count and spacing_ok
    numeric_authorized = geometry_authorized and bool(column_values) and semantics_verified and not reasons
    status = "candidate" if numeric_authorized else "partial_visible" if geometry_authorized else "low_confidence"
    run_configuration = {
        "algorithm_version": ALGORITHM_VERSION,
        "input_sha256": identity.sha256,
        "config": config,
    }
    run_id = hashlib.sha256(
        json.dumps(run_configuration, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    return {
        "schema_version": 1,
        "extractor": "candidate_lattice_composite",
        "algorithm_version": ALGORITHM_VERSION,
        "deterministic_run_id": run_id,
        "status": status,
        "geometry_output_authorized": geometry_authorized,
        "numeric_output_authorized": numeric_authorized,
        "reason": "; ".join(reasons) if reasons else "all configured candidate gates passed",
        "input": {"file": str(input_path), **identity.as_dict()},
        "coordinate_provenance": {
            "measurement_space": ORIGINAL_RASTER_SPACE,
            "resampling_applied": False,
            "x_origin": "left",
            "y_origin": "top",
        },
        "configuration": config,
        "geometry": {
            "column_bar_roi": list(column_roi),
            "column_guide_role": column_guide_role,
            "row_bar_roi": list(row_roi),
            "row_guide_role": row_guide_role,
            "common_column_baseline_row": baseline_row,
            "column_count": len(column_bars),
            "row_count": len(row_bars),
            "cell_count": len(cells),
            "active_cell_count": sum(cell["status"] == "active" for cell in cells),
            "inactive_cell_count": sum(cell["status"] == "inactive" for cell in cells),
            "ambiguous_cell_count": ambiguous_count,
            "column_spacing": column_spacing,
            "row_spacing": row_spacing,
        },
        "column_bars": column_bars,
        "row_bars": row_bars,
        "cells": cells,
        "validation": {
            "spacing_status": "passed" if spacing_ok else "failed",
            "top_bars_vs_values": top_validation,
            "row_totals_vs_bars": row_validation,
        },
        "required_review": [
            "Open the overlay at original resolution and verify every bar box and active-cell ring.",
            "Review every ambiguous cell; do not convert it to active or inactive from an expected count.",
            "Verify semantic labels and printed values independently of detected geometry.",
        ],
        "limitations": [
            "This candidate supports repeated aligned column bars or membership-derived column guides, row bars or membership-derived row guides, and compact filled membership nodes.",
            "A layer may combine multiple verified fill colours; colour lists do not supply semantic row identities.",
            "It does not recover hidden records, occluded nodes, connector semantics, or unverified text.",
            "Semantic labels and printed values are external verified inputs and never tune the geometry detector.",
        ],
    }


def _flat_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in report["column_bars"]:
        kind = "column_bar" if item.get("guide_role") == "column_bar" else "column_guide"
        rows.append({"kind": kind, **item, "members": ";".join(item["members"])})
    for item in report["row_bars"]:
        kind = "row_bar" if item.get("guide_role") == "row_bar" else "row_guide"
        rows.append({"kind": kind, **item})
    for item in report["cells"]:
        rows.append({"kind": "membership_cell", **item})
    return rows


def write_outputs(input_path: Path, report: dict[str, Any], output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"refusing to overwrite non-empty evidence directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    flat = _flat_rows(report)
    fields = list(dict.fromkeys(key for row in flat for key in row))
    with (output_dir / "geometry.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(flat)
    (output_dir / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    with Image.open(input_path) as source:
        overlay = source.convert("RGB")
    draw = ImageDraw.Draw(overlay)
    for bar in report["column_bars"]:
        if bar.get("guide_role") == "membership_guides":
            draw.line(
                (bar["pixel_x"], bar["top_px"] - 5, bar["pixel_x"], bar["bottom_px"] + 5),
                fill="#ff7f00",
                width=2,
            )
        else:
            draw.rectangle(
                (bar["left_px"] - 2, bar["top_px"] - 2, bar["right_px"] + 1, bar["bottom_px"] + 1),
                outline="#ff7f00",
                width=2,
            )
    for row in report["row_bars"]:
        if row.get("guide_role") == "membership_guides":
            draw.line(
                (row["left_px"] - 5, row["pixel_y"], row["right_px"] + 5, row["pixel_y"]),
                fill="#d200b4",
                width=2,
            )
        else:
            draw.line(
                (row["left_px"] + 1, row["top_px"] - 2, row["left_px"] + 1, row["bottom_px"] + 2),
                fill="#d200b4",
                width=3,
            )
    for cell in report["cells"]:
        if cell["status"] == "inactive":
            continue
        colour = "#e60000" if cell["status"] == "active" else "#ffbf00"
        radius = 11
        draw.ellipse(
            (
                cell["pixel_x"] - radius,
                cell["pixel_y"] - radius,
                cell["pixel_x"] + radius,
                cell["pixel_y"] + radius,
            ),
            outline=colour,
            width=3,
        )
    overlay.save(output_dir / "overlay.png")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    initialize = subparsers.add_parser("init-config", help="Lock a config template to the original raster")
    initialize.add_argument("--input", required=True, type=Path)
    initialize.add_argument("--output", required=True, type=Path)
    extract = subparsers.add_parser("extract", help="Run the configured original-pixel candidate")
    extract.add_argument("--input", required=True, type=Path)
    extract.add_argument("--config", required=True, type=Path)
    extract.add_argument("--output-dir", required=True, type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "init-config":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(init_config(args.input), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps({"status": "template_created", "config": str(args.output)}, ensure_ascii=False))
        return
    config = json.loads(args.config.read_text(encoding="utf-8"))
    report = extract_lattice_composite(args.input, config)
    write_outputs(args.input, report, args.output_dir)
    print(json.dumps({
        "status": report["status"],
        "geometry_output_authorized": report["geometry_output_authorized"],
        "numeric_output_authorized": report["numeric_output_authorized"],
        "columns": report["geometry"]["column_count"],
        "rows": report["geometry"]["row_count"],
        "active_cells": report["geometry"]["active_cell_count"],
        "output_dir": str(args.output_dir),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

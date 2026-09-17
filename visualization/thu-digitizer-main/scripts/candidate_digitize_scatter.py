"""Extract compact visible scatter-marker centres from a calibrated raster panel.

This deterministic candidate separates touching filled markers with distance-
transform peaks.  It treats axes, curves, text, and confidence bands as
competing raster evidence rather than asking a vision model to count points.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Sequence

import cv2
import numpy as np
from PIL import Image, ImageDraw

try:
    from raster_digitizer_core import AxisCalibration
except ImportError:  # pragma: no cover - package import
    from .raster_digitizer_core import AxisCalibration


Bounds = tuple[int, int, int, int]
Anchor = tuple[float, float]
ALGORITHM_VERSION = "compact-scatter-distance-peaks-v2-residual-audit"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parse_bounds(value: str) -> Bounds:
    try:
        parts = tuple(int(item.strip()) for item in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("bounds must be left,top,right,bottom integers") from exc
    if len(parts) != 4 or parts[0] >= parts[2] or parts[1] >= parts[3]:
        raise argparse.ArgumentTypeError("bounds must satisfy left<right and top<bottom")
    return parts  # type: ignore[return-value]


def _parse_anchor(value: str) -> Anchor:
    try:
        pixel, numeric = (float(item.strip()) for item in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("anchors must be pixel,value") from exc
    return pixel, numeric


def _parse_rgb(value: str | Sequence[int]) -> tuple[int, int, int]:
    if isinstance(value, str):
        text = value.strip().lstrip("#")
        if "," in text:
            channels = tuple(int(item.strip()) for item in text.split(","))
        else:
            if len(text) != 6:
                raise ValueError("marker colour must be #RRGGBB or R,G,B")
            channels = tuple(int(text[index : index + 2], 16) for index in (0, 2, 4))
    else:
        channels = tuple(int(item) for item in value)
    if len(channels) != 3 or any(channel < 0 or channel > 255 for channel in channels):
        raise ValueError("marker colour needs three channels in 0..255")
    return channels  # type: ignore[return-value]


def _validate_bounds(bounds: Bounds, width: int, height: int, *, name: str) -> None:
    left, top, right, bottom = bounds
    if not (0 <= left < right < width and 0 <= top < bottom < height):
        raise ValueError(f"{name} {bounds} must fit image dimensions {width}x{height}")


def _marker_mask(
    rgb: np.ndarray,
    *,
    marker_mode: str,
    marker_color: str | Sequence[int] | None,
    color_tolerance: float,
    dark_threshold: int,
    light_threshold: int,
) -> np.ndarray:
    if marker_mode == "color":
        if marker_color is None:
            raise ValueError("marker_color is required when marker_mode='color'")
        target = np.asarray(_parse_rgb(marker_color), dtype=np.int32)
        difference = rgb.astype(np.int32) - target
        return np.square(difference).sum(axis=2) <= float(color_tolerance) ** 2
    # Fixed luminance coefficients make the mode independent of OpenCV channel order.
    luminance = (
        0.2126 * rgb[:, :, 0].astype(np.float32)
        + 0.7152 * rgb[:, :, 1].astype(np.float32)
        + 0.0722 * rgb[:, :, 2].astype(np.float32)
    )
    if marker_mode == "dark":
        return luminance <= dark_threshold
    if marker_mode == "light":
        return luminance >= light_threshold
    raise ValueError("marker_mode must be dark, light, or color")


def _disc_fraction(mask: np.ndarray, x: float, y: float, radius: float) -> float:
    if radius <= 0:
        return 0.0
    left = max(0, int(math.floor(x - radius)))
    right = min(mask.shape[1] - 1, int(math.ceil(x + radius)))
    top = max(0, int(math.floor(y - radius)))
    bottom = min(mask.shape[0] - 1, int(math.ceil(y + radius)))
    yy, xx = np.mgrid[top : bottom + 1, left : right + 1]
    selector = np.square(xx - x) + np.square(yy - y) <= radius * radius
    if not np.any(selector):
        return 0.0
    return float(np.mean(mask[top : bottom + 1, left : right + 1][selector]))


def _peak_candidates(
    mask: np.ndarray,
    *,
    min_radius: float,
    max_radius: float,
    peak_window: int,
) -> tuple[np.ndarray, list[dict[str, float]]]:
    binary = mask.astype(np.uint8)
    distance = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    kernel = np.ones((peak_window, peak_window), dtype=np.uint8)
    dilated = cv2.dilate(distance, kernel)
    maxima = (distance >= dilated - 1e-6) & (distance >= min_radius) & (distance <= max_radius)
    maxima_count, maxima_labels = cv2.connectedComponents(maxima.astype(np.uint8))
    candidates: list[dict[str, float]] = []
    for label in range(1, maxima_count):
        yy, xx = np.where(maxima_labels == label)
        weights = distance[yy, xx].astype(float)
        if not len(weights) or float(weights.sum()) <= 0:
            continue
        candidates.append(
            {
                "x": float(np.average(xx, weights=weights)),
                "y": float(np.average(yy, weights=weights)),
                "radius": float(weights.max()),
                "plateau_pixels": float(len(weights)),
            }
        )
    return distance, candidates


def _non_maximum_suppression(candidates: list[dict[str, float]]) -> tuple[list[dict[str, float]], list[dict[str, Any]]]:
    accepted: list[dict[str, float]] = []
    suppressed: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda item: (-item["radius"], item["y"], item["x"])):
        conflict = None
        for selected in accepted:
            separation = math.hypot(candidate["x"] - selected["x"], candidate["y"] - selected["y"])
            minimum = max(2.0, 0.42 * (candidate["radius"] + selected["radius"]))
            if separation < minimum:
                conflict = (selected, separation, minimum)
                break
        if conflict is None:
            accepted.append(candidate)
        else:
            selected, separation, minimum = conflict
            suppressed.append(
                {
                    **candidate,
                    "reason": "peak_too_close_to_stronger_peak",
                    "selected_peak": {"x": selected["x"], "y": selected["y"]},
                    "separation_pixels": separation,
                    "required_separation_pixels": minimum,
                }
            )
    return sorted(accepted, key=lambda item: (item["x"], item["y"])), suppressed


def _restrict_to_verified_region(
    mask: np.ndarray,
    *,
    plot_bounds: Bounds,
    edge_margin: int,
    exclude_regions: Sequence[Bounds],
) -> np.ndarray:
    """Apply the same verified spatial contract to every detector pass."""

    result = mask.copy()
    outside = np.ones_like(result, dtype=bool)
    left, top, right, bottom = plot_bounds
    outside[top : bottom + 1, left : right + 1] = False
    result[outside] = False
    if edge_margin:
        result[top : min(bottom + 1, top + edge_margin), left : right + 1] = False
        result[max(top, bottom - edge_margin + 1) : bottom + 1, left : right + 1] = False
        result[top : bottom + 1, left : min(right + 1, left + edge_margin)] = False
        result[top : bottom + 1, max(left, right - edge_margin + 1) : right + 1] = False
    for region_left, region_top, region_right, region_bottom in exclude_regions:
        result[region_top : region_bottom + 1, region_left : region_right + 1] = False
    return result


def _residual_marker_candidates(
    rgb: np.ndarray,
    *,
    accepted: list[dict[str, float]],
    radius_reference: float | None,
    plot_bounds: Bounds,
    edge_margin: int,
    exclude_regions: Sequence[Bounds],
    marker_mode: str,
    marker_color: str | Sequence[int] | None,
    color_tolerance: float,
    dark_threshold: int,
    light_threshold: int,
    min_radius: float,
    max_radius: float,
    peak_window: int,
    threshold_delta: int,
    color_tolerance_ratio: float,
    radius_ratio_min: float,
    radius_ratio_max: float,
    core_fraction_min: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Run a relaxed negative-space pass without adding points.

    The pass can only block authorization.  It never promotes a residual peak
    into the primary table.  A caller must refine verified exclusions or the
    marker configuration and rerun the primary detector.
    """

    relaxed_mask = _marker_mask(
        rgb,
        marker_mode=marker_mode,
        marker_color=marker_color,
        color_tolerance=color_tolerance * color_tolerance_ratio,
        dark_threshold=min(255, dark_threshold + threshold_delta),
        light_threshold=max(0, light_threshold - threshold_delta),
    )
    relaxed_mask = _restrict_to_verified_region(
        relaxed_mask,
        plot_bounds=plot_bounds,
        edge_margin=edge_margin,
        exclude_regions=exclude_regions,
    )
    _, relaxed_peaks = _peak_candidates(
        relaxed_mask,
        min_radius=min_radius,
        max_radius=max_radius,
        peak_window=peak_window,
    )
    reference = radius_reference
    if reference is None and relaxed_peaks:
        reference = float(
            np.percentile([candidate["radius"] for candidate in relaxed_peaks], 75)
        )
    residuals: list[dict[str, Any]] = []
    if reference is not None:
        minimum = max(min_radius, reference * radius_ratio_min)
        maximum = min(max_radius, reference * radius_ratio_max)
        for candidate in relaxed_peaks:
            radius = float(candidate["radius"])
            if not minimum <= radius <= maximum:
                continue
            if any(
                math.hypot(candidate["x"] - point["x"], candidate["y"] - point["y"])
                < max(2.0, 0.55 * (radius + float(point["radius"])))
                for point in accepted
            ):
                continue
            core_fraction = _disc_fraction(
                relaxed_mask,
                float(candidate["x"]),
                float(candidate["y"]),
                max(1.0, radius * 0.82),
            )
            if core_fraction < core_fraction_min:
                continue
            residuals.append(
                {
                    "pixel_x": round(float(candidate["x"]), 4),
                    "pixel_y": round(float(candidate["y"]), 4),
                    "marker_radius_evidence_pixels": round(radius, 4),
                    "core_foreground_fraction_relaxed": round(core_fraction, 4),
                    "reason_code": "detector_residual",
                    "status": "review_required_not_promoted",
                }
            )
    return residuals, {
        "strategy": "relaxed_negative_space_peak_pass",
        "role": "authorization_gate_only_never_adds_points",
        "threshold_delta": threshold_delta,
        "color_tolerance_ratio": color_tolerance_ratio,
        "radius_ratio_range": [radius_ratio_min, radius_ratio_max],
        "core_fraction_min": core_fraction_min,
        "relaxed_raw_peak_count": len(relaxed_peaks),
        "residual_candidate_count": len(residuals),
        "status": "clear" if not residuals else "review_required",
        "candidates": residuals,
    }


def extract_scatter_points(
    input_path: Path,
    *,
    plot_bounds: Bounds,
    x_anchors: Sequence[Anchor],
    y_anchors: Sequence[Anchor],
    x_scale: str = "linear",
    y_scale: str = "linear",
    marker_mode: str = "dark",
    marker_color: str | Sequence[int] | None = None,
    color_tolerance: float = 36.0,
    dark_threshold: int = 120,
    light_threshold: int = 225,
    min_radius: float = 2.8,
    max_radius: float = 18.0,
    radius_consistency_ratio: float = 0.72,
    peak_window: int = 5,
    edge_margin: int = 3,
    exclude_regions: Sequence[Bounds] = (),
    annotated_pearson_r: float | None = None,
    pearson_tolerance: float = 0.03,
    residual_threshold_delta: int = 24,
    residual_color_tolerance_ratio: float = 1.35,
    residual_radius_ratio_min: float = 0.72,
    residual_radius_ratio_max: float = 1.45,
    residual_core_fraction_min: float = 0.70,
) -> dict[str, Any]:
    """Return calibrated centres supported by compact visible raster peaks."""
    if len(x_anchors) < 2 or len(y_anchors) < 2:
        raise ValueError("at least two anchors are required for each axis")
    if not (0 <= dark_threshold <= 255 and 0 <= light_threshold <= 255):
        raise ValueError("dark/light thresholds must be in 0..255")
    if color_tolerance <= 0 or min_radius <= 0 or max_radius <= min_radius:
        raise ValueError("colour tolerance and radii must be positive with max_radius>min_radius")
    if not (0 < radius_consistency_ratio <= 1):
        raise ValueError("radius_consistency_ratio must be in (0, 1]")
    if peak_window < 3 or peak_window % 2 == 0:
        raise ValueError("peak_window must be an odd integer of at least 3")
    if edge_margin < 0:
        raise ValueError("edge_margin must be non-negative")
    if pearson_tolerance <= 0:
        raise ValueError("pearson_tolerance must be positive")
    if residual_threshold_delta < 0:
        raise ValueError("residual_threshold_delta must be non-negative")
    if residual_color_tolerance_ratio < 1:
        raise ValueError("residual_color_tolerance_ratio must be at least 1")
    if not 0 < residual_radius_ratio_min <= residual_radius_ratio_max:
        raise ValueError("residual radius ratios must be positive and ordered")
    if not 0 < residual_core_fraction_min <= 1:
        raise ValueError("residual_core_fraction_min must be in (0, 1]")

    input_path = Path(input_path)
    with Image.open(input_path) as source:
        image = source.convert("RGB")
    rgb = np.asarray(image)
    height, width = rgb.shape[:2]
    _validate_bounds(plot_bounds, width, height, name="plot_bounds")
    for region in exclude_regions:
        _validate_bounds(region, width, height, name="exclude_region")

    x_axis = AxisCalibration.fit(x_anchors, scale=x_scale)
    y_axis = AxisCalibration.fit(y_anchors, scale=y_scale)
    mask = _marker_mask(
        rgb,
        marker_mode=marker_mode,
        marker_color=marker_color,
        color_tolerance=color_tolerance,
        dark_threshold=dark_threshold,
        light_threshold=light_threshold,
    )
    mask = _restrict_to_verified_region(
        mask,
        plot_bounds=plot_bounds,
        edge_margin=edge_margin,
        exclude_regions=exclude_regions,
    )

    distance, candidates = _peak_candidates(
        mask,
        min_radius=min_radius,
        max_radius=max_radius,
        peak_window=peak_window,
    )
    radius_reference = (
        float(np.percentile([candidate["radius"] for candidate in candidates], 75))
        if candidates
        else None
    )
    radius_cutoff = (
        max(min_radius, radius_reference * radius_consistency_ratio)
        if radius_reference is not None
        else min_radius
    )
    radius_rejected = [
        {
            **candidate,
            "reason": "peak_radius_inconsistent_with_compact_marker_mode",
            "minimum_consistent_radius": radius_cutoff,
        }
        for candidate in candidates
        if candidate["radius"] < radius_cutoff
    ]
    consistent_candidates = [
        candidate for candidate in candidates if candidate["radius"] >= radius_cutoff
    ]
    accepted, proximity_suppressed = _non_maximum_suppression(consistent_candidates)
    suppressed = [*radius_rejected, *proximity_suppressed]
    residual_candidates, residual_audit = _residual_marker_candidates(
        rgb,
        accepted=accepted,
        radius_reference=radius_reference,
        plot_bounds=plot_bounds,
        edge_margin=edge_margin,
        exclude_regions=exclude_regions,
        marker_mode=marker_mode,
        marker_color=marker_color,
        color_tolerance=color_tolerance,
        dark_threshold=dark_threshold,
        light_threshold=light_threshold,
        min_radius=min_radius,
        max_radius=max_radius,
        peak_window=peak_window,
        threshold_delta=residual_threshold_delta,
        color_tolerance_ratio=residual_color_tolerance_ratio,
        radius_ratio_min=residual_radius_ratio_min,
        radius_ratio_max=residual_radius_ratio_max,
        core_fraction_min=residual_core_fraction_min,
    )
    component_count, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)

    points: list[dict[str, Any]] = []
    component_peaks: dict[int, int] = {}
    for point_index, candidate in enumerate(accepted, start=1):
        x = float(candidate["x"])
        y = float(candidate["y"])
        ix = min(width - 1, max(0, int(round(x))))
        iy = min(height - 1, max(0, int(round(y))))
        component_label = int(labels[iy, ix])
        component_peaks[component_label] = component_peaks.get(component_label, 0) + 1
        radius = float(candidate["radius"])
        core_fraction = _disc_fraction(mask, x, y, max(1.0, radius * 0.82))
        radius_score = min(1.0, max(0.0, (radius - min_radius) / max(1.0, min_radius)))
        confidence = min(1.0, 0.55 + 0.25 * core_fraction + 0.20 * radius_score)
        pixel_sigma = max(0.45, 0.9 / math.sqrt(max(radius, 1e-6)))
        points.append(
            {
                "point_id": point_index,
                "pixel_x": round(x, 4),
                "pixel_y": round(y, 4),
                "x": round(x_axis.value_at_pixel(x), 8),
                "y": round(y_axis.value_at_pixel(y), 8),
                "x_uncertainty": round(x_axis.uncertainty_at_pixel(x, pixel_sigma=pixel_sigma), 8),
                "y_uncertainty": round(y_axis.uncertainty_at_pixel(y, pixel_sigma=pixel_sigma), 8),
                "marker_radius_evidence_pixels": round(radius, 4),
                "core_foreground_fraction": round(core_fraction, 4),
                "confidence": round(confidence, 4),
                "component_id": component_label,
                "status": "visible_marker_candidate",
            }
        )

    components = []
    for label in sorted(component_peaks):
        x = int(stats[label, cv2.CC_STAT_LEFT])
        y = int(stats[label, cv2.CC_STAT_TOP])
        component_width = int(stats[label, cv2.CC_STAT_WIDTH])
        component_height = int(stats[label, cv2.CC_STAT_HEIGHT])
        components.append(
            {
                "component_id": label,
                "bounds": [x, y, x + component_width - 1, y + component_height - 1],
                "area_pixels": int(stats[label, cv2.CC_STAT_AREA]),
                "peak_count": component_peaks[label],
                "split_status": (
                    "distance_transform_split" if component_peaks[label] > 1 else "single_peak"
                ),
            }
        )
    for point in points:
        point["component_peak_count"] = component_peaks.get(point["component_id"], 0)

    validation: dict[str, Any] = {
        "role": "validation only; the annotation is never used to add, remove, or move points",
        "annotated_pearson_r": annotated_pearson_r,
        "pearson_tolerance": pearson_tolerance,
        "recomputed_pearson_r": None,
        "absolute_difference": None,
        "status": "not_available",
    }
    if len(points) >= 3:
        x_values = np.asarray([point["x"] for point in points], dtype=float)
        y_values = np.asarray([point["y"] for point in points], dtype=float)
        if float(np.std(x_values)) > 0 and float(np.std(y_values)) > 0:
            recomputed = float(np.corrcoef(x_values, y_values)[0, 1])
            validation["recomputed_pearson_r"] = recomputed
            if annotated_pearson_r is None:
                validation["status"] = "computed_without_annotation"
            else:
                difference = abs(recomputed - annotated_pearson_r)
                validation["absolute_difference"] = difference
                validation["status"] = "matched" if difference <= pearson_tolerance else "mismatch"

    reasons: list[str] = []
    if not points:
        reasons.append("no compact marker peaks met the visible-evidence thresholds")
    if annotated_pearson_r is not None and validation["status"] != "matched":
        reasons.append("recomputed Pearson correlation does not match the supplied annotation")
    if residual_candidates:
        reasons.append(
            "relaxed negative-space audit found unresolved marker-like residuals"
        )
    status = "candidate" if not reasons else "low_confidence"
    authorized = status == "candidate"
    for point in points:
        point["value_status"] = (
            "visible_marker_candidate" if authorized else "candidate_not_authorized"
        )

    input_sha256 = _sha256(input_path)
    run_configuration = {
        "input_sha256": input_sha256,
        "plot_bounds": list(plot_bounds),
        "x_anchors": [list(anchor) for anchor in x_anchors],
        "y_anchors": [list(anchor) for anchor in y_anchors],
        "x_scale": x_scale,
        "y_scale": y_scale,
        "marker_mode": marker_mode,
        "marker_color": list(_parse_rgb(marker_color)) if marker_color is not None else None,
        "color_tolerance": color_tolerance,
        "dark_threshold": dark_threshold,
        "light_threshold": light_threshold,
        "min_radius": min_radius,
        "max_radius": max_radius,
        "radius_consistency_ratio": radius_consistency_ratio,
        "peak_window": peak_window,
        "edge_margin": edge_margin,
        "exclude_regions": [list(region) for region in exclude_regions],
        "annotated_pearson_r": annotated_pearson_r,
        "pearson_tolerance": pearson_tolerance,
        "residual_threshold_delta": residual_threshold_delta,
        "residual_color_tolerance_ratio": residual_color_tolerance_ratio,
        "residual_radius_ratio_min": residual_radius_ratio_min,
        "residual_radius_ratio_max": residual_radius_ratio_max,
        "residual_core_fraction_min": residual_core_fraction_min,
    }
    run_id = hashlib.sha256(
        json.dumps(run_configuration, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    return {
        "schema_version": 1,
        "extractor": "candidate_compact_scatter_distance_peaks",
        "algorithm_version": ALGORITHM_VERSION,
        "deterministic_run_id": run_id,
        "software": {"opencv": cv2.__version__, "numpy": np.__version__},
        "status": status,
        "numeric_output_authorized": authorized,
        "reason": "; ".join(reasons) if reasons else "all configured candidate gates passed",
        "input": {
            "file": str(input_path),
            "sha256": input_sha256,
            "dimensions": [width, height],
        },
        "plot_bounds": list(plot_bounds),
        "calibration": {"x": x_axis.report(), "y": y_axis.report()},
        "detection": {
            "marker_mode": marker_mode,
            "marker_color": list(_parse_rgb(marker_color)) if marker_color is not None else None,
            "color_tolerance": color_tolerance,
            "dark_threshold": dark_threshold,
            "light_threshold": light_threshold,
            "min_radius": min_radius,
            "max_radius": max_radius,
            "radius_consistency_ratio": radius_consistency_ratio,
            "radius_reference_pixels": radius_reference,
            "radius_cutoff_pixels": radius_cutoff,
            "peak_window": peak_window,
            "edge_margin": edge_margin,
            "exclude_regions": [list(region) for region in exclude_regions],
            "foreground_pixels": int(np.count_nonzero(mask)),
            "raw_peak_count": len(candidates),
            "accepted_peak_count": len(points),
            "suppressed_peak_count": len(suppressed),
        },
        "points": points,
        "components": components,
        "suppressed_peaks": suppressed,
        "residual_audit": residual_audit,
        "validation": validation,
        "required_review": [
            "Open the overlay at original resolution and verify every accepted ring is centred on a visible marker.",
            "Review every multi-peak component and every suppressed peak before publishing numeric output.",
            "The residual audit must be clear; residual candidates must be resolved by verified exclusions or configuration, never promoted by eye.",
        ],
        "limitations": [
            "This candidate recovers compact filled visible marker centres only.",
            "Perfectly coincident, fully occluded, hollow, or non-compact markers are not recovered by this route.",
            "A supplied correlation annotation validates the result but never changes detected geometry.",
            "Axes, curves, text, and legends that are as thick and compact as markers may require a verified exclusion region.",
        ],
    }


def write_csv(report: dict[str, Any], output_path: Path) -> None:
    fields = [
        "point_id",
        "x",
        "y",
        "pixel_x",
        "pixel_y",
        "x_uncertainty",
        "y_uncertainty",
        "marker_radius_evidence_pixels",
        "core_foreground_fraction",
        "confidence",
        "component_id",
        "component_peak_count",
        "status",
        "value_status",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(report["points"])


def write_overlay(input_path: Path, report: dict[str, Any], output_path: Path) -> None:
    with Image.open(input_path) as source:
        overlay = source.convert("RGB")
    draw = ImageDraw.Draw(overlay)
    colour = "#00a65a" if report["numeric_output_authorized"] else "#ff8c00"
    left, top, right, bottom = report["plot_bounds"]
    draw.rectangle((left, top, right, bottom), outline="#00a6ff", width=1)
    for point in report["points"]:
        x = float(point["pixel_x"])
        y = float(point["pixel_y"])
        radius = max(4.0, float(point["marker_radius_evidence_pixels"]) + 2.0)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=colour, width=2)
        draw.line((x - 2, y, x + 2, y), fill=colour, width=1)
        draw.line((x, y - 2, x, y + 2), fill=colour, width=1)
    for candidate in report.get("residual_audit", {}).get("candidates", []):
        x = float(candidate["pixel_x"])
        y = float(candidate["pixel_y"])
        radius = max(4.0, float(candidate["marker_radius_evidence_pixels"]) + 2.0)
        draw.rectangle((x - radius, y - radius, x + radius, y + radius), outline="#d000d0", width=2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    overlay.save(output_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--overlay", required=True, type=Path)
    parser.add_argument("--plot-bounds", required=True, type=_parse_bounds)
    parser.add_argument("--x-anchor", required=True, action="append", type=_parse_anchor)
    parser.add_argument("--y-anchor", required=True, action="append", type=_parse_anchor)
    parser.add_argument("--x-scale", choices=("linear", "log10", "displayed_log10"), default="linear")
    parser.add_argument("--y-scale", choices=("linear", "log10", "displayed_log10"), default="linear")
    parser.add_argument("--marker-mode", choices=("dark", "light", "color"), default="dark")
    parser.add_argument("--marker-color")
    parser.add_argument("--color-tolerance", type=float, default=36.0)
    parser.add_argument("--dark-threshold", type=int, default=120)
    parser.add_argument("--light-threshold", type=int, default=225)
    parser.add_argument("--min-radius", type=float, default=2.8)
    parser.add_argument("--max-radius", type=float, default=18.0)
    parser.add_argument("--radius-consistency-ratio", type=float, default=0.72)
    parser.add_argument("--peak-window", type=int, default=5)
    parser.add_argument("--edge-margin", type=int, default=3)
    parser.add_argument("--exclude-region", action="append", type=_parse_bounds)
    parser.add_argument("--annotated-pearson-r", type=float)
    parser.add_argument("--pearson-tolerance", type=float, default=0.03)
    parser.add_argument("--residual-threshold-delta", type=int, default=24)
    parser.add_argument("--residual-color-tolerance-ratio", type=float, default=1.35)
    parser.add_argument("--residual-radius-ratio-min", type=float, default=0.72)
    parser.add_argument("--residual-radius-ratio-max", type=float, default=1.45)
    parser.add_argument("--residual-core-fraction-min", type=float, default=0.70)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    report = extract_scatter_points(
        args.input,
        plot_bounds=args.plot_bounds,
        x_anchors=args.x_anchor,
        y_anchors=args.y_anchor,
        x_scale=args.x_scale,
        y_scale=args.y_scale,
        marker_mode=args.marker_mode,
        marker_color=args.marker_color,
        color_tolerance=args.color_tolerance,
        dark_threshold=args.dark_threshold,
        light_threshold=args.light_threshold,
        min_radius=args.min_radius,
        max_radius=args.max_radius,
        radius_consistency_ratio=args.radius_consistency_ratio,
        peak_window=args.peak_window,
        edge_margin=args.edge_margin,
        exclude_regions=args.exclude_region or (),
        annotated_pearson_r=args.annotated_pearson_r,
        pearson_tolerance=args.pearson_tolerance,
        residual_threshold_delta=args.residual_threshold_delta,
        residual_color_tolerance_ratio=args.residual_color_tolerance_ratio,
        residual_radius_ratio_min=args.residual_radius_ratio_min,
        residual_radius_ratio_max=args.residual_radius_ratio_max,
        residual_core_fraction_min=args.residual_core_fraction_min,
    )
    write_csv(report, args.output_csv)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_overlay(args.input, report, args.overlay)
    print(
        json.dumps(
            {
                "status": report["status"],
                "numeric_output_authorized": report["numeric_output_authorized"],
                "point_count": len(report["points"]),
                "csv": str(args.output_csv),
                "report": str(args.report),
                "overlay": str(args.overlay),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

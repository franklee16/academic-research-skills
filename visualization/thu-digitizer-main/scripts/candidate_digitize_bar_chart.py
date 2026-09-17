"""Candidate extractor for calibrated, colour-distinct bar charts.

The route is deliberately assisted: callers provide the plot bounds, a verified
linear value-axis calibration, category-centre pixels, and one colour per
series.  It supports vertical or horizontal grouped/simple bars, stacked bars,
100%-stacked bars, negative values, and separately coloured error bars.

This module is a candidate, not a promoted stable extractor.  It returns only
visible rectangle/interval geometry and refuses ambiguous series/category
assignments instead of inventing values.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import deque
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from PIL import Image, ImageDraw

try:
    from extraction_contract import build_coverage_ledger
except ImportError:  # pragma: no cover - package-style invocation
    from .extraction_contract import build_coverage_ledger


VALID_ORIENTATIONS = {"vertical", "horizontal"}
VALID_LAYOUTS = {"grouped", "stacked", "percent_stacked"}


def _rgb_from_hex(value: str) -> tuple[int, int, int]:
    if not isinstance(value, str) or len(value) != 7 or not value.startswith("#"):
        raise ValueError("colours must use #RRGGBB")
    try:
        return tuple(int(value[index : index + 2], 16) for index in (1, 3, 5))
    except ValueError as error:
        raise ValueError("colours must use #RRGGBB") from error


def _color_mask(image: np.ndarray, color: str, tolerance: float) -> np.ndarray:
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    target = np.asarray(_rgb_from_hex(color), dtype=np.int32)
    difference = image.astype(np.int32) - target
    return np.square(difference).sum(axis=2) <= tolerance * tolerance


def _pixel_to_data(pixel: float, axis: tuple[float, float, float, float]) -> float:
    pixel_start, data_start, pixel_end, data_end = axis
    if pixel_start == pixel_end:
        raise ValueError("value-axis calibration pixels must differ")
    return float(
        data_start
        + (pixel - pixel_start) * (data_end - data_start) / (pixel_end - pixel_start)
    )


def _data_to_pixel(value: float, axis: tuple[float, float, float, float]) -> float:
    pixel_start, data_start, pixel_end, data_end = axis
    if data_start == data_end:
        raise ValueError("value-axis calibration values must differ")
    return float(
        pixel_start
        + (value - data_start) * (pixel_end - pixel_start) / (data_end - data_start)
    )


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_bounds(
    plot_bounds: tuple[int, int, int, int], image_shape: tuple[int, int, int]
) -> None:
    left, top, right, bottom = plot_bounds
    rows, columns = image_shape[:2]
    if not (0 <= left < right < columns and 0 <= top < bottom < rows):
        raise ValueError(
            f"plot_bounds must be inclusive bounds inside a {columns}x{rows} image"
        )


def _validate_exclude_regions(
    regions: list[tuple[int, int, int, int]], image_shape: tuple[int, int, int]
) -> None:
    rows, columns = image_shape[:2]
    for index, (left, top, right, bottom) in enumerate(regions):
        if not (0 <= left <= right < columns and 0 <= top <= bottom < rows):
            raise ValueError(
                "exclude_regions must contain inclusive bounds inside "
                f"a {columns}x{rows} image; region {index} is invalid"
            )


def _component_overlaps_region(
    component: dict[str, float], region: tuple[int, int, int, int]
) -> bool:
    left, top, right, bottom = region
    component_right = component["right_pixel"] - 1
    component_bottom = component["bottom_pixel"] - 1
    return not (
        component_right < left
        or component["left_pixel"] > right
        or component_bottom < top
        or component["top_pixel"] > bottom
    )


def _connected_components(
    mask: np.ndarray,
    *,
    orientation: str,
    bridge_gap: int,
    verified_occluder_mask: np.ndarray | None = None,
    verified_occluder_bridge_gap: int = 0,
    verified_occluder_min_fraction: float = 0.60,
    bridge_stats: dict[str, float] | None = None,
) -> list[np.ndarray]:
    """Return original true pixels, bridging thin cross-axis overlay gaps.

    An error-bar spine can replace a one-pixel strip through a filled bar.  The
    cross-axis jump connects the two remaining fill regions without changing
    the measured outer rectangle.
    """
    if bridge_gap < 0 or verified_occluder_bridge_gap < 0:
        raise ValueError("bridge gaps must be non-negative")
    if not 0 < verified_occluder_min_fraction <= 1:
        raise ValueError("verified_occluder_min_fraction must be in (0, 1]")
    if verified_occluder_mask is not None and verified_occluder_mask.shape != mask.shape:
        raise ValueError("verified occluder mask must match the bar mask shape")
    rows, columns = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    result: list[np.ndarray] = []
    regular_cross_jump = bridge_gap + 1
    verified_cross_jump = verified_occluder_bridge_gap + 1
    cross_jump = max(regular_cross_jump, verified_cross_jump)

    def verified_extended_jump(
        row: int,
        column: int,
        row_offset: int,
        column_offset: int,
    ) -> tuple[bool, int, float]:
        if verified_occluder_mask is None:
            return False, 0, 0.0
        if orientation == "vertical":
            if row_offset != 0 or abs(column_offset) <= regular_cross_jump:
                return False, 0, 0.0
            start, end = sorted((column, column + column_offset))
            support = verified_occluder_mask[row, start + 1 : end]
            intermediate_fill = mask[row, start + 1 : end]
        else:
            if column_offset != 0 or abs(row_offset) <= regular_cross_jump:
                return False, 0, 0.0
            start, end = sorted((row, row + row_offset))
            support = verified_occluder_mask[start + 1 : end, column]
            intermediate_fill = mask[start + 1 : end, column]
        gap = int(len(support))
        if not gap or gap > verified_occluder_bridge_gap or np.any(intermediate_fill):
            return False, gap, 0.0
        fraction = float(np.mean(support))
        return fraction >= verified_occluder_min_fraction, gap, fraction

    for start_row, start_column in zip(*np.where(mask)):
        if visited[start_row, start_column]:
            continue
        queue = deque([(int(start_row), int(start_column))])
        visited[start_row, start_column] = True
        pixels: list[tuple[int, int]] = []
        while queue:
            row, column = queue.popleft()
            pixels.append((row, column))
            row_offsets: Iterable[int]
            column_offsets: Iterable[int]
            if orientation == "vertical":
                row_offsets = range(-1, 2)
                column_offsets = range(-cross_jump, cross_jump + 1)
            else:
                row_offsets = range(-cross_jump, cross_jump + 1)
                column_offsets = range(-1, 2)
            for row_offset in row_offsets:
                for column_offset in column_offsets:
                    if row_offset == 0 and column_offset == 0:
                        continue
                    neighbor_row = row + row_offset
                    neighbor_column = column + column_offset
                    if (
                        0 <= neighbor_row < rows
                        and 0 <= neighbor_column < columns
                        and mask[neighbor_row, neighbor_column]
                        and not visited[neighbor_row, neighbor_column]
                    ):
                        cross_offset = (
                            abs(column_offset)
                            if orientation == "vertical"
                            else abs(row_offset)
                        )
                        if cross_offset > regular_cross_jump:
                            allowed, gap, fraction = verified_extended_jump(
                                row, column, row_offset, column_offset
                            )
                            if not allowed:
                                continue
                            if bridge_stats is not None:
                                bridge_stats["verified_bridge_edge_count"] = (
                                    bridge_stats.get("verified_bridge_edge_count", 0.0) + 1.0
                                )
                                bridge_stats["maximum_verified_gap_pixels"] = max(
                                    bridge_stats.get("maximum_verified_gap_pixels", 0.0),
                                    float(gap),
                                )
                                bridge_stats["minimum_occluder_support_fraction"] = min(
                                    bridge_stats.get("minimum_occluder_support_fraction", 1.0),
                                    fraction,
                                )
                        visited[neighbor_row, neighbor_column] = True
                        queue.append((neighbor_row, neighbor_column))
        result.append(np.asarray(pixels, dtype=float))
    return result


def _bridge_value_gaps(mask: np.ndarray, *, orientation: str, max_gap: int) -> np.ndarray:
    """Close thin raster/gridline gaps along the value axis only.

    Publication bars are often crossed by a one-pixel horizontal gridline or
    anti-aliased boundary.  The old component pass interpreted every such gap
    as a second bar.  Bridging is restricted to a run with true evidence on
    both sides, so it cannot create a bar from an isolated colour speck.
    """

    if max_gap < 0:
        raise ValueError("value_gap must be non-negative")
    if max_gap == 0:
        return mask
    result = mask.copy()
    if orientation == "vertical":
        for x in range(mask.shape[1]):
            column = mask[:, x]
            true_rows = np.flatnonzero(column)
            if len(true_rows) < 2:
                continue
            for start, end in zip(true_rows[:-1], true_rows[1:]):
                if 1 < end - start <= max_gap + 1:
                    result[start : end + 1, x] = True
    else:
        for y in range(mask.shape[0]):
            row = mask[y, :]
            true_columns = np.flatnonzero(row)
            if len(true_columns) < 2:
                continue
            for start, end in zip(true_columns[:-1], true_columns[1:]):
                if 1 < end - start <= max_gap + 1:
                    result[y, start : end + 1] = True
    return result


def _dilate_cross_axis(
    mask: np.ndarray, *, orientation: str, radius: int
) -> np.ndarray:
    """Expand a verified thin occluder only across bar thickness.

    Anti-alias pixels around a dark interval line may no longer match the
    sampled interval colour.  Dilation is restricted to the cross axis and is
    used only as topology evidence between visible fill on both sides.
    """

    if radius < 0:
        raise ValueError("cross-axis dilation radius must be non-negative")
    if radius == 0:
        return mask.copy()
    result = mask.copy()
    if orientation == "vertical":
        for offset in range(1, radius + 1):
            result[:, offset:] |= mask[:, :-offset]
            result[:, :-offset] |= mask[:, offset:]
    else:
        for offset in range(1, radius + 1):
            result[offset:, :] |= mask[:-offset, :]
            result[:-offset, :] |= mask[offset:, :]
    return result


def _component_record(
    pixels: np.ndarray,
    *,
    left: int,
    top: int,
    orientation: str,
) -> dict[str, float]:
    rows = pixels[:, 0] + top
    columns = pixels[:, 1] + left
    min_row = int(rows.min())
    max_row = int(rows.max())
    min_column = int(columns.min())
    max_column = int(columns.max())
    width = max_column - min_column + 1
    height = max_row - min_row + 1
    cross_extent = width if orientation == "vertical" else height
    value_extent = height if orientation == "vertical" else width
    return {
        "area": float(len(pixels)),
        "left_pixel": float(min_column),
        "right_pixel": float(max_column + 1),
        "top_pixel": float(min_row),
        "bottom_pixel": float(max_row + 1),
        "width_pixels": float(width),
        "height_pixels": float(height),
        "cross_extent_pixels": float(cross_extent),
        "value_extent_pixels": float(value_extent),
        "fill_ratio": float(len(pixels) / (width * height)),
        "category_pixel": float(
            (min_column + max_column + 1) / 2
            if orientation == "vertical"
            else (min_row + max_row + 1) / 2
        ),
    }


def _category_tolerance(
    category_pixels: list[float],
    plot_bounds: tuple[int, int, int, int],
    orientation: str,
) -> float:
    if len(category_pixels) > 1:
        spacings = np.diff(sorted(category_pixels))
        if np.any(spacings <= 0):
            raise ValueError("category pixels must be unique")
        return float(np.min(spacings) * 0.48)
    left, top, right, bottom = plot_bounds
    return float((right - left if orientation == "vertical" else bottom - top) / 2)


def _measure_component(
    component: dict[str, float],
    *,
    layout: str,
    orientation: str,
    value_axis: tuple[float, float, float, float],
    baseline_value: float,
    baseline_tolerance_px: float,
    allow_occluded_baseline: bool = False,
) -> tuple[dict[str, float] | None, str | None]:
    if orientation == "vertical":
        first_pixel = component["top_pixel"]
        second_pixel = component["bottom_pixel"]
    else:
        first_pixel = component["left_pixel"]
        second_pixel = component["right_pixel"]

    baseline_pixel = _data_to_pixel(baseline_value, value_axis)
    first_value = _pixel_to_data(first_pixel, value_axis)
    second_value = _pixel_to_data(second_pixel, value_axis)
    data_per_pixel = abs(
        (value_axis[3] - value_axis[1]) / (value_axis[2] - value_axis[0])
    )
    data_tolerance = baseline_tolerance_px * data_per_pixel

    if layout == "grouped":
        if abs(first_pixel - baseline_pixel) <= abs(second_pixel - baseline_pixel):
            start_pixel, end_pixel = first_pixel, second_pixel
        else:
            start_pixel, end_pixel = second_pixel, first_pixel
        if abs(start_pixel - baseline_pixel) > baseline_tolerance_px:
            if allow_occluded_baseline:
                # A legend or annotation can cover the lower bar segment.  If
                # the visible component is otherwise a full-width bar, the
                # calibrated baseline remains the correct geometric origin;
                # retain the occlusion flag instead of discarding its endpoint.
                nearest_endpoint = first_pixel if abs(first_pixel - baseline_pixel) < abs(second_pixel - baseline_pixel) else second_pixel
                end_pixel = second_pixel if nearest_endpoint == first_pixel else first_pixel
                end_value = _pixel_to_data(end_pixel, value_axis)
                return {
                    "baseline_pixel": baseline_pixel,
                    "start_pixel": float(baseline_pixel),
                    "end_pixel": float(end_pixel),
                    "start_value": float(baseline_value),
                    "end_value": float(end_value),
                    "value": float(end_value - baseline_value),
                    "baseline_status": "occluded_by_overlay",
                }, None
            return None, (
                "rectangle does not meet the calibrated baseline within "
                f"{baseline_tolerance_px:g}px"
            )
        end_value = _pixel_to_data(end_pixel, value_axis)
        return {
            "baseline_pixel": baseline_pixel,
            "start_pixel": float(start_pixel),
            "end_pixel": float(end_pixel),
            "start_value": float(baseline_value),
            "end_value": float(end_value),
            "value": float(end_value - baseline_value),
        }, None

    low_value = min(first_value, second_value)
    high_value = max(first_value, second_value)
    if low_value < baseline_value - data_tolerance and high_value > baseline_value + data_tolerance:
        return None, "stack segment straddles the calibrated baseline"

    if (low_value + high_value) / 2 >= baseline_value:
        start_value, end_value = low_value, high_value
    else:
        start_value, end_value = high_value, low_value
    start_pixel = first_pixel if abs(first_value - start_value) <= abs(second_value - start_value) else second_pixel
    end_pixel = second_pixel if start_pixel == first_pixel else first_pixel
    return {
        "baseline_pixel": baseline_pixel,
        "start_pixel": float(start_pixel),
        "end_pixel": float(end_pixel),
        "start_value": float(start_value),
        "end_value": float(end_value),
        "value": float(end_value - start_value),
    }, None


def _extract_error_interval(
    error_mask: np.ndarray,
    mark: dict[str, Any],
    *,
    plot_bounds: tuple[int, int, int, int],
    orientation: str,
    value_axis: tuple[float, float, float, float],
    radius: int,
    min_span: int,
) -> dict[str, Any]:
    left, top, right, bottom = plot_bounds
    center = int(round(mark["component_category_pixel"]))
    if orientation == "vertical":
        cross_start, cross_end = max(left, center - radius), min(right, center + radius)
        value_positions, _ = np.where(error_mask[top : bottom + 1, cross_start : cross_end + 1])
        value_positions = value_positions + top
    else:
        cross_start, cross_end = max(top, center - radius), min(bottom, center + radius)
        _, value_positions = np.where(error_mask[cross_start : cross_end + 1, left : right + 1])
        value_positions = value_positions + left
    if not len(value_positions):
        return {"status": "not_extracted", "reason": "no distinct error-colour evidence"}
    unique_positions = np.unique(np.sort(value_positions))
    clusters = np.split(unique_positions, np.where(np.diff(unique_positions) > 3)[0] + 1)
    supported_clusters = [cluster for cluster in clusters if int(cluster[-1] - cluster[0]) >= min_span]
    if not supported_clusters:
        return {
            "status": "not_extracted",
            "reason": f"no error-colour cluster spans at least {min_span}px",
        }
    endpoint = float(mark["end_pixel"])

    def distance_to_endpoint(cluster: np.ndarray) -> float:
        if cluster[0] <= endpoint <= cluster[-1]:
            return 0.0
        return float(min(abs(endpoint - cluster[0]), abs(endpoint - cluster[-1])))

    ranked = sorted(supported_clusters, key=distance_to_endpoint)
    if len(ranked) > 1 and abs(distance_to_endpoint(ranked[0]) - distance_to_endpoint(ranked[1])) <= 1.0:
        return {
            "status": "not_extracted",
            "reason": "multiple error-colour intervals are equally close to the bar endpoint",
        }
    selected = ranked[0]
    first_pixel = int(selected.min())
    second_pixel = int(selected.max())
    span = second_pixel - first_pixel
    if endpoint - first_pixel < 2 or second_pixel - endpoint < 2:
        return {
            "status": "not_extracted",
            "reason": "visible interval does not bracket the bar endpoint on both sides",
        }
    first_value = _pixel_to_data(first_pixel, value_axis)
    second_value = _pixel_to_data(second_pixel, value_axis)
    if first_value <= second_value:
        lower_pixel, lower_value = first_pixel, first_value
        upper_pixel, upper_value = second_pixel, second_value
    else:
        lower_pixel, lower_value = second_pixel, second_value
        upper_pixel, upper_value = first_pixel, first_value
    coverage = len(selected) / (span + 1)
    return {
        "status": "extracted",
        "lower_pixel": float(lower_pixel),
        "upper_pixel": float(upper_pixel),
        "lower_value": float(lower_value),
        "upper_value": float(upper_value),
        "span_pixels": float(span),
        "confidence": round(float(min(1.0, 0.5 + 0.5 * coverage)), 3),
        "semantic_type": "visible_interval_only",
    }


def _stack_diagnostics(
    marks: list[dict[str, Any]],
    *,
    categories: list[tuple[str, float]],
    baseline_value: float,
    stack_gap_tolerance_px: float,
    expected_stack_total: float | None,
    stack_total_tolerance: float,
) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    for category_name, _ in categories:
        visible = [
            mark
            for mark in marks
            if mark["category"] == category_name and mark["status"] == "extracted"
        ]
        gap_value_by_sign: dict[str, float] = {}
        gap_pixels_by_sign: dict[str, float] = {}
        for sign, sign_marks in (
            ("positive", [mark for mark in visible if mark["value"] > 0]),
            ("negative", [mark for mark in visible if mark["value"] < 0]),
        ):
            ordered = sorted(
                sign_marks,
                key=lambda mark: abs(mark["start_value"] - baseline_value),
            )
            previous_end_pixel: float | None = None
            previous_end_value: float | None = None
            visible_gap_value = 0.0
            visible_gap_pixels = 0.0
            for index, mark in enumerate(ordered):
                expected_start_pixel = mark["baseline_pixel"] if index == 0 else previous_end_pixel
                expected_start_value = baseline_value if index == 0 else previous_end_value
                gap = abs(mark["start_pixel"] - expected_start_pixel)
                gap_value = abs(mark["start_value"] - expected_start_value)
                visible_gap_pixels += float(gap)
                visible_gap_value += float(gap_value)
                if gap > stack_gap_tolerance_px:
                    diagnostics.append(
                        {
                            "kind": "stack_gap",
                            "category": category_name,
                            "sign": sign,
                            "series": mark["series"],
                            "gap_pixels": float(gap),
                        }
                    )
                previous_end_pixel = mark["end_pixel"]
                previous_end_value = mark["end_value"]
            gap_value_by_sign[sign] = visible_gap_value
            gap_pixels_by_sign[sign] = visible_gap_pixels
        if expected_stack_total is not None:
            positive_total = sum(mark["value"] for mark in visible if mark["value"] > 0)
            difference = positive_total - expected_stack_total
            positive_gap_value = gap_value_by_sign.get("positive", 0.0)
            positive_gap_pixels = gap_pixels_by_sign.get("positive", 0.0)
            separator_consistent = bool(
                difference < 0
                and positive_gap_value > 0
                and abs(abs(difference) - positive_gap_value) <= stack_total_tolerance
                and not any(
                    diagnostic["kind"] == "stack_gap"
                    and diagnostic["category"] == category_name
                    and diagnostic["sign"] == "positive"
                    for diagnostic in diagnostics
                )
            )
            within_tolerance = abs(difference) <= stack_total_tolerance
            diagnostics.append(
                {
                    "kind": "stack_total",
                    "category": category_name,
                    "expected": float(expected_stack_total),
                    "observed_positive_total": float(positive_total),
                    "difference": float(difference),
                    "within_tolerance": within_tolerance,
                    "visible_internal_gap_value_total": float(positive_gap_value),
                    "visible_internal_gap_pixels_total": float(positive_gap_pixels),
                    "separator_consistent": separator_consistent,
                    "validation_status": (
                        "within_numeric_tolerance"
                        if within_tolerance
                        else "visible_separator_shortfall"
                        if separator_consistent
                        else "unresolved_stack_total_mismatch"
                    ),
                    "values_normalized_or_completed": False,
                }
            )
    return diagnostics


def extract_bar_chart(
    image_path: Path,
    *,
    plot_bounds: tuple[int, int, int, int],
    value_axis: tuple[float, float, float, float],
    orientation: str,
    layout: str,
    series_colors: dict[str, str],
    categories: list[tuple[str, float]],
    exclude_regions: list[tuple[int, int, int, int]] | None = None,
    baseline_value: float = 0.0,
    tolerance: float = 32.0,
    min_area: int = 20,
    min_bar_thickness: int = 3,
    min_bar_length: int = 2,
    min_fill_ratio: float = 0.55,
    bridge_gap: int = 1,
    verified_occluder_bridge_gap: int = 6,
    verified_occluder_min_fraction: float = 0.60,
    value_gap: int = 2,
    category_tolerance_px: float | None = None,
    baseline_tolerance_px: float = 3.0,
    stack_gap_tolerance_px: float = 3.0,
    expected_stack_total: float | None = None,
    stack_total_tolerance: float = 0.75,
    error_color: str | None = None,
    error_tolerance: float = 18.0,
    error_search_radius: int = 2,
    error_min_span: int = 5,
    prefer_baseline_connected: bool = True,
) -> dict[str, Any]:
    """Extract visible calibrated bar rectangles and optional error intervals."""
    if orientation not in VALID_ORIENTATIONS:
        raise ValueError(f"orientation must be one of {sorted(VALID_ORIENTATIONS)}")
    if layout not in VALID_LAYOUTS:
        raise ValueError(f"layout must be one of {sorted(VALID_LAYOUTS)}")
    if not series_colors:
        raise ValueError("at least one named series colour is required")
    if not categories:
        raise ValueError("at least one category centre is required")
    if len(set(series_colors)) != len(series_colors):
        raise ValueError("series names must be unique")
    category_names = [name for name, _ in categories]
    category_pixels = [float(pixel) for _, pixel in categories]
    if len(set(category_names)) != len(category_names):
        raise ValueError("category names must be unique")
    if len(set(category_pixels)) != len(category_pixels):
        raise ValueError("category pixels must be unique")
    if min_area < 1 or min_bar_thickness < 1 or min_bar_length < 1:
        raise ValueError("minimum geometry thresholds must be positive")
    if not 0 < min_fill_ratio <= 1:
        raise ValueError("min_fill_ratio must be in (0, 1]")
    if layout == "percent_stacked" and expected_stack_total is None:
        expected_stack_total = 100.0

    image_path = Path(image_path)
    with Image.open(image_path) as source:
        rgb_image = source.convert("RGB")
        image = np.asarray(rgb_image)
        width, height = rgb_image.size
    _validate_bounds(plot_bounds, image.shape)
    verified_exclude_regions = list(exclude_regions or [])
    _validate_exclude_regions(verified_exclude_regions, image.shape)
    left, top, right, bottom = plot_bounds
    value_low = min(left, right) if orientation == "horizontal" else min(top, bottom)
    value_high = max(left, right) if orientation == "horizontal" else max(top, bottom)
    baseline_pixel = _data_to_pixel(baseline_value, value_axis)
    if baseline_pixel < value_low - baseline_tolerance_px or baseline_pixel > value_high + baseline_tolerance_px:
        raise ValueError("the calibrated baseline must fall inside the plot bounds")
    for name, color in series_colors.items():
        try:
            _rgb_from_hex(color)
        except ValueError as error:
            raise ValueError(f"invalid colour for series {name!r}: {error}") from error
    if error_color is not None:
        try:
            _rgb_from_hex(error_color)
        except ValueError as error:
            raise ValueError(f"invalid error colour: {error}") from error

    assignment_tolerance = (
        float(category_tolerance_px)
        if category_tolerance_px is not None
        else _category_tolerance(category_pixels, plot_bounds, orientation)
    )
    assignments: dict[tuple[str, str], list[dict[str, float]]] = {
        (category_name, series_name): []
        for category_name, _ in categories
        for series_name in series_colors
    }
    rejected_components: list[dict[str, Any]] = []
    excluded_components: list[dict[str, Any]] = []
    verified_bridge_stats: dict[str, float] = {
        "verified_bridge_edge_count": 0.0,
        "maximum_verified_gap_pixels": 0.0,
        "minimum_occluder_support_fraction": 1.0,
    }
    error_mask = (
        _color_mask(image, error_color, error_tolerance)
        if error_color is not None
        else None
    )
    raw_error_view = (
        error_mask[top : bottom + 1, left : right + 1]
        if error_mask is not None
        else None
    )
    error_view = (
        _dilate_cross_axis(
            raw_error_view,
            orientation=orientation,
            radius=verified_occluder_bridge_gap,
        )
        if raw_error_view is not None
        else None
    )

    for series_name, color in series_colors.items():
        full_mask = _color_mask(image, color, tolerance)
        view = full_mask[top : bottom + 1, left : right + 1]
        view = _bridge_value_gaps(view, orientation=orientation, max_gap=value_gap)
        for pixels in _connected_components(
            view,
            orientation=orientation,
            bridge_gap=bridge_gap,
            verified_occluder_mask=error_view,
            verified_occluder_bridge_gap=(
                verified_occluder_bridge_gap if error_view is not None else 0
            ),
            verified_occluder_min_fraction=verified_occluder_min_fraction,
            bridge_stats=verified_bridge_stats,
        ):
            component = _component_record(
                pixels, left=left, top=top, orientation=orientation
            )
            matching_exclusions = [
                list(region)
                for region in verified_exclude_regions
                if _component_overlaps_region(component, region)
            ]
            if matching_exclusions:
                excluded_components.append(
                    {
                        "series": series_name,
                        "reason": "overlaps_verified_exclusion_region",
                        "exclude_regions": matching_exclusions,
                        **component,
                    }
                )
                continue
            reasons = []
            if component["area"] < min_area:
                reasons.append("area_below_minimum")
            if component["cross_extent_pixels"] < min_bar_thickness:
                reasons.append("bar_thickness_below_minimum")
            if component["value_extent_pixels"] < min_bar_length:
                reasons.append("bar_length_below_minimum")
            if component["fill_ratio"] < min_fill_ratio:
                reasons.append("fill_ratio_below_minimum")
            nearest_index = int(
                np.argmin(
                    [abs(component["category_pixel"] - pixel) for pixel in category_pixels]
                )
            )
            category_name, category_pixel = categories[nearest_index]
            category_distance = abs(component["category_pixel"] - category_pixel)
            if category_distance > assignment_tolerance:
                reasons.append("outside_category_tolerance")
            component["category_distance_pixels"] = float(category_distance)
            if reasons:
                rejected_components.append(
                    {
                        "series": series_name,
                        "nearest_category": category_name,
                        "reasons": reasons,
                        **component,
                    }
                )
                continue
            assignments[(category_name, series_name)].append(component)

    marks: list[dict[str, Any]] = []
    ambiguity_count = 0
    for category_name, requested_category_pixel in categories:
        for series_name, color in series_colors.items():
            candidates = assignments[(category_name, series_name)]
            base: dict[str, Any] = {
                "category": category_name,
                "requested_category_pixel": float(requested_category_pixel),
                "series": series_name,
                "color": color,
            }
            if not candidates:
                marks.append(
                    {
                        **base,
                        "status": "not_extracted",
                        "reason_code": "no_supported_geometry",
                        "reason": "no supported rectangle for this series/category",
                    }
                )
                continue
            if prefer_baseline_connected and len(candidates) > 1:
                # Legends and in-plot colour swatches often share the same
                # series colour.  A real grouped/stacked bar must touch the
                # calibrated baseline; use that geometric fact to discard
                # swatches, but retain ambiguity when multiple rectangles all
                # satisfy it (for example two fused bars in one category).
                baseline_pixel = _data_to_pixel(baseline_value, value_axis)
                connected = []
                for candidate in candidates:
                    endpoints = (
                        (candidate["top_pixel"], candidate["bottom_pixel"])
                        if orientation == "vertical"
                        else (candidate["left_pixel"], candidate["right_pixel"])
                    )
                    if min(abs(float(endpoint) - baseline_pixel) for endpoint in endpoints) <= baseline_tolerance_px:
                        connected.append(candidate)
                if len(connected) == 1:
                    candidates = connected
                elif not connected:
                    largest = max(candidates, key=lambda item: item["area"])
                    other_area = max(item["area"] for item in candidates if item is not largest)
                    if largest["area"] >= max(4.0 * other_area, float(min_area) * 4.0):
                        candidates = [largest]
            if len(candidates) != 1:
                ambiguity_count += 1
                marks.append(
                    {
                        **base,
                        "status": "low_confidence",
                        "reason_code": "ambiguous_geometry",
                        "reason": "multiple supported rectangles map to this series/category",
                        "candidate_count": len(candidates),
                        "candidates": candidates,
                    }
                )
                continue
            component = candidates[0]
            measurement, reason = _measure_component(
                component,
                layout="grouped" if layout == "grouped" else "stacked",
                orientation=orientation,
                value_axis=value_axis,
                baseline_value=baseline_value,
                baseline_tolerance_px=baseline_tolerance_px,
                allow_occluded_baseline=bool(
                    prefer_baseline_connected
                    and min(
                        abs(component["top_pixel"] - _data_to_pixel(baseline_value, value_axis)),
                        abs(component["bottom_pixel"] - _data_to_pixel(baseline_value, value_axis)),
                    ) > baseline_tolerance_px
                ),
            )
            if measurement is None:
                ambiguity_count += 1
                marks.append(
                    {
                        **base,
                        "status": "low_confidence",
                        "reason_code": "calibration_geometry_conflict",
                        "reason": reason,
                        "component": component,
                    }
                )
                continue
            confidence = min(
                1.0,
                0.45 * component["fill_ratio"]
                + 0.35 * min(1.0, component["cross_extent_pixels"] / max(3.0, min_bar_thickness * 2))
                + 0.20 * (1 - min(1.0, component["category_distance_pixels"] / max(1.0, assignment_tolerance))),
            )
            marks.append(
                {
                    **base,
                    "status": "extracted",
                    "reason_code": "visible_geometry_supported",
                    "confidence": round(float(confidence), 3),
                    "component_category_pixel": component["category_pixel"],
                    "component": component,
                    **measurement,
                }
            )

    stack_diagnostics: list[dict[str, Any]] = []
    if layout in {"stacked", "percent_stacked"}:
        stack_diagnostics = _stack_diagnostics(
            marks,
            categories=categories,
            baseline_value=baseline_value,
            stack_gap_tolerance_px=stack_gap_tolerance_px,
            expected_stack_total=expected_stack_total,
            stack_total_tolerance=stack_total_tolerance,
        )
        ambiguity_count += sum(
            diagnostic["kind"] == "stack_gap"
            or (
                diagnostic["kind"] == "stack_total"
                and not diagnostic["within_tolerance"]
                and not diagnostic["separator_consistent"]
            )
            for diagnostic in stack_diagnostics
        )

    if error_color is not None:
        assert error_mask is not None
        for mark in marks:
            if mark["status"] == "extracted":
                mark["error_bar"] = _extract_error_interval(
                    error_mask,
                    mark,
                    plot_bounds=plot_bounds,
                    orientation=orientation,
                    value_axis=value_axis,
                    radius=error_search_radius,
                    min_span=error_min_span,
                )

    extracted_count = sum(mark["status"] == "extracted" for mark in marks)
    missing_count = sum(mark["status"] == "not_extracted" for mark in marks)
    error_missing_count = sum(
        mark.get("error_bar", {}).get("status") == "not_extracted" for mark in marks
    )
    if extracted_count == 0:
        status = "low_confidence" if ambiguity_count else "not_extracted"
    elif ambiguity_count:
        status = "partial_visible" if layout == "grouped" else "low_confidence"
    elif missing_count or rejected_components or error_missing_count:
        status = "partial_visible"
    else:
        status = "candidate"

    globally_authorized = status != "low_confidence" and extracted_count > 0
    invalid_stack_categories = {
        diagnostic["category"]
        for diagnostic in stack_diagnostics
        if diagnostic["kind"] == "stack_gap"
        or (
            diagnostic["kind"] == "stack_total"
            and not diagnostic["within_tolerance"]
            and not diagnostic["separator_consistent"]
        )
    }
    for mark in marks:
        mark["numeric_output_authorized"] = bool(
            mark["status"] == "extracted"
            and (
                globally_authorized
                or (
                    layout == "grouped"
                    and mark["reason_code"] == "visible_geometry_supported"
                )
            )
            and mark["category"] not in invalid_stack_categories
        )
    coverage_ledger = build_coverage_ledger(
        marks,
        slot_fields=("category", "series"),
    )

    return {
        "schema_version": 1,
        "extractor_status": "candidate",
        "status": status,
        "numeric_output_authorized": bool(
            coverage_ledger["authorized_slot_count"] > 0
        ),
        "numeric_authorization_scope": (
            "all_declared_slots"
            if coverage_ledger["authorized_slot_count"] == len(marks)
            else "authorized_records_only"
            if coverage_ledger["authorized_slot_count"]
            else "none"
        ),
        "input_file": image_path.name,
        "input_sha256": _file_sha256(image_path),
        "image_size": {"width": width, "height": height},
        "orientation": orientation,
        "layout": layout,
        "plot_bounds": list(plot_bounds),
        "exclude_regions": [list(region) for region in verified_exclude_regions],
        "value_axis": list(value_axis),
        "axis_assumption": "verified linear value axis",
        "baseline_value": float(baseline_value),
        "baseline_pixel": float(baseline_pixel),
        "categories": [
            {"name": name, "center_pixel": float(pixel)} for name, pixel in categories
        ],
        "series": [
            {"name": name, "color": color} for name, color in series_colors.items()
        ],
        "parameters": {
            "tolerance": float(tolerance),
            "min_area": int(min_area),
            "min_bar_thickness": int(min_bar_thickness),
            "min_bar_length": int(min_bar_length),
            "min_fill_ratio": float(min_fill_ratio),
            "bridge_gap": int(bridge_gap),
            "value_gap": int(value_gap),
            "verified_occluder_bridge_gap": int(verified_occluder_bridge_gap),
            "verified_occluder_min_fraction": float(
                verified_occluder_min_fraction
            ),
            "category_tolerance_px": float(assignment_tolerance),
            "baseline_tolerance_px": float(baseline_tolerance_px),
            "stack_gap_tolerance_px": float(stack_gap_tolerance_px),
            "expected_stack_total": expected_stack_total,
            "stack_total_tolerance": float(stack_total_tolerance),
            "error_color": error_color,
            "error_tolerance": float(error_tolerance),
            "error_search_radius": int(error_search_radius),
            "error_min_span": int(error_min_span),
        },
        "marks": marks,
        "rejected_components": rejected_components,
        "excluded_components": excluded_components,
        "stack_diagnostics": stack_diagnostics,
        "verified_occluder_bridging": {
            **verified_bridge_stats,
            "enabled": error_view is not None and verified_occluder_bridge_gap > 0,
            "occluder_role": "topology_only_not_numeric_fill",
            "mask_preparation": "verified_error_colour_cross_axis_dilation",
        },
        "coverage_ledger": coverage_ledger,
        "summary": {
            "expected_mark_count": len(categories) * len(series_colors),
            "extracted_mark_count": extracted_count,
            "missing_mark_count": missing_count,
            "ambiguous_mark_count": sum(
                mark["status"] == "low_confidence" for mark in marks
            ),
            "rejected_component_count": len(rejected_components),
            "excluded_component_count": len(excluded_components),
            "error_bar_missing_count": error_missing_count,
            "mean_confidence": round(
                float(
                    np.mean(
                        [
                            mark["confidence"]
                            for mark in marks
                            if mark["status"] == "extracted"
                        ]
                    )
                ),
                3,
            )
            if extracted_count
            else 0.0,
        },
        "limitations": [
            "Only visible colour-distinct rectangles are measured; source observations are not recovered.",
            "Category centres, the plot region, orientation, layout, and linear calibration must be verified.",
            "A missing segment is not converted to a zero value.",
            "Error intervals describe visible endpoints only; SD, SEM, or confidence-interval semantics are unknown.",
            "Facets, insets, photos, 3D projections, gradients, hatching, and overlapping same-colour marks require separate routing.",
            "Every exclusion region must be visually verified as legend or decorative geometry before extraction.",
            "Verified occluder bridging changes component topology only; values remain calibrated from the outer visible fill endpoints.",
            "Separator-consistent stack gaps are reported and never normalized or filled.",
        ],
    }


def write_overlay(image_path: Path, report: dict[str, Any], output_path: Path) -> None:
    with Image.open(image_path) as source:
        overlay = source.convert("RGB")
    draw = ImageDraw.Draw(overlay)
    for region in report.get("exclude_regions", []):
        draw.rectangle(tuple(region), outline=(255, 170, 0), width=2)
    for category in report["categories"]:
        pixel = int(round(category["center_pixel"]))
        left, top, right, bottom = report["plot_bounds"]
        if report["orientation"] == "vertical":
            draw.line((pixel, top, pixel, bottom), fill=(255, 170, 0), width=1)
        else:
            draw.line((left, pixel, right, pixel), fill=(255, 170, 0), width=1)
    for mark in report["marks"]:
        if mark["status"] != "extracted":
            continue
        component = mark["component"]
        rectangle = (
            int(round(component["left_pixel"])),
            int(round(component["top_pixel"])),
            int(round(component["right_pixel"] - 1)),
            int(round(component["bottom_pixel"] - 1)),
        )
        draw.rectangle(rectangle, outline=(255, 0, 255), width=2)
        error_bar = mark.get("error_bar")
        if error_bar and error_bar["status"] == "extracted":
            center = int(round(mark["component_category_pixel"]))
            first = int(round(error_bar["lower_pixel"]))
            second = int(round(error_bar["upper_pixel"]))
            if report["orientation"] == "vertical":
                draw.ellipse((center - 3, first - 3, center + 3, first + 3), outline=(0, 180, 255), width=2)
                draw.ellipse((center - 3, second - 3, center + 3, second + 3), outline=(0, 180, 255), width=2)
            else:
                draw.ellipse((first - 3, center - 3, first + 3, center + 3), outline=(0, 180, 255), width=2)
                draw.ellipse((second - 3, center - 3, second + 3, center + 3), outline=(0, 180, 255), width=2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    overlay.save(output_path)


def write_recreation(
    report: dict[str, Any], output_path: Path, *, title: str | None = None
) -> None:
    """Render an audit plot from extracted visible bar geometry.

    The recreation intentionally uses a plain style.  It reproduces accepted
    numeric geometry, not the source figure's typography or hidden source data.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    categories = [item["name"] for item in report["categories"]]
    series = [item["name"] for item in report["series"]]
    colors = {item["name"]: item["color"] for item in report["series"]}
    marks = {
        (mark["category"], mark["series"]): mark for mark in report["marks"]
    }
    positions = np.arange(len(categories), dtype=float)
    baseline = float(report["baseline_value"])
    orientation = report["orientation"]
    layout = report["layout"]
    figure, axis = plt.subplots(figsize=(7.2, 4.8), dpi=120)
    axis.set_axisbelow(True)
    axis.grid(axis="y" if orientation == "vertical" else "x", color="#dddddd", linewidth=0.8)

    if layout == "grouped":
        width = 0.78 / max(1, len(series))
        for series_index, series_name in enumerate(series):
            offset = (series_index - (len(series) - 1) / 2) * width
            values = []
            bottoms = []
            accepted = []
            for category in categories:
                mark = marks[(category, series_name)]
                accepted.append(mark["status"] == "extracted")
                values.append(float(mark["value"]) if mark["status"] == "extracted" else 0.0)
                bottoms.append(baseline)
            bar_positions = positions + offset
            if orientation == "vertical":
                axis.bar(
                    bar_positions,
                    values,
                    width=width * 0.9,
                    bottom=bottoms,
                    color=colors[series_name],
                    label=series_name,
                )
            else:
                axis.barh(
                    bar_positions,
                    values,
                    height=width * 0.9,
                    left=bottoms,
                    color=colors[series_name],
                    label=series_name,
                )
            for category_index, category in enumerate(categories):
                mark = marks[(category, series_name)]
                if mark["status"] != "extracted":
                    if orientation == "vertical":
                        axis.scatter(bar_positions[category_index], baseline, marker="x", color="#c00000", zorder=5)
                    else:
                        axis.scatter(baseline, bar_positions[category_index], marker="x", color="#c00000", zorder=5)
                    continue
                error_bar = mark.get("error_bar", {})
                if error_bar.get("status") != "extracted":
                    continue
                end_value = float(mark["end_value"])
                lower_error = max(0.0, end_value - float(error_bar["lower_value"]))
                upper_error = max(0.0, float(error_bar["upper_value"]) - end_value)
                if orientation == "vertical":
                    axis.errorbar(
                        bar_positions[category_index],
                        end_value,
                        yerr=np.asarray([[lower_error], [upper_error]]),
                        fmt="none",
                        ecolor="#333333",
                        elinewidth=1.2,
                        capsize=3,
                    )
                else:
                    axis.errorbar(
                        end_value,
                        bar_positions[category_index],
                        xerr=np.asarray([[lower_error], [upper_error]]),
                        fmt="none",
                        ecolor="#333333",
                        elinewidth=1.2,
                        capsize=3,
                    )
    else:
        for series_name in series:
            values = []
            starts = []
            for category in categories:
                mark = marks[(category, series_name)]
                if mark["status"] == "extracted":
                    values.append(float(mark["value"]))
                    starts.append(float(mark["start_value"]))
                else:
                    values.append(0.0)
                    starts.append(baseline)
            if orientation == "vertical":
                axis.bar(
                    positions,
                    values,
                    width=0.64,
                    bottom=starts,
                    color=colors[series_name],
                    edgecolor="white",
                    linewidth=0.8,
                    label=series_name,
                )
            else:
                axis.barh(
                    positions,
                    values,
                    height=0.64,
                    left=starts,
                    color=colors[series_name],
                    edgecolor="white",
                    linewidth=0.8,
                    label=series_name,
                )

    if orientation == "vertical":
        axis.set_xticks(positions, categories)
        axis.axhline(baseline, color="#555555", linewidth=0.9)
        axis.set_ylabel("Extracted value")
    else:
        axis.set_yticks(positions, categories)
        axis.axvline(baseline, color="#555555", linewidth=0.9)
        axis.set_xlabel("Extracted value")
    axis.legend(frameon=False, title="Extracted series")
    axis.set_title(title or "Candidate recreation from extracted visible geometry")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, facecolor="white")
    plt.close(figure)


def _parse_bounds(value: str) -> tuple[int, int, int, int]:
    try:
        parsed = tuple(int(part.strip()) for part in value.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("bounds must be four comma-separated integers") from error
    if len(parsed) != 4:
        raise argparse.ArgumentTypeError("bounds must be left,top,right,bottom")
    return parsed  # type: ignore[return-value]


def _parse_axis(value: str) -> tuple[float, float, float, float]:
    try:
        parsed = tuple(float(part.strip()) for part in value.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("axis must be pixel0,value0,pixel1,value1") from error
    if len(parsed) != 4:
        raise argparse.ArgumentTypeError("axis must be pixel0,value0,pixel1,value1")
    return parsed  # type: ignore[return-value]


def _parse_named_color(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("series must use NAME=#RRGGBB")
    name, color = (part.strip() for part in value.split("=", 1))
    if not name:
        raise argparse.ArgumentTypeError("series name must not be empty")
    try:
        _rgb_from_hex(color)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    return name, color


def _parse_category(value: str) -> tuple[str, float]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("category must use LABEL=PIXEL")
    name, pixel = (part.strip() for part in value.split("=", 1))
    if not name:
        raise argparse.ArgumentTypeError("category label must not be empty")
    try:
        return name, float(pixel)
    except ValueError as error:
        raise argparse.ArgumentTypeError("category pixel must be numeric") from error


def _write_csv(path: Path, report: dict[str, Any]) -> None:
    fields = [
        "category",
        "series",
        "status",
        "reason_code",
        "reason",
        "numeric_output_authorized",
        "value",
        "start_value",
        "end_value",
        "start_pixel",
        "end_pixel",
        "confidence",
        "error_status",
        "error_lower_value",
        "error_upper_value",
        "error_lower_pixel",
        "error_upper_pixel",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for mark in report["marks"]:
            error_bar = mark.get("error_bar", {})
            writer.writerow(
                {
                    "category": mark["category"],
                    "series": mark["series"],
                    "status": mark["status"],
                    "reason_code": mark.get("reason_code", ""),
                    "reason": mark.get("reason", ""),
                    "numeric_output_authorized": mark.get(
                        "numeric_output_authorized", False
                    ),
                    "value": mark.get("value", ""),
                    "start_value": mark.get("start_value", ""),
                    "end_value": mark.get("end_value", ""),
                    "start_pixel": mark.get("start_pixel", ""),
                    "end_pixel": mark.get("end_pixel", ""),
                    "confidence": mark.get("confidence", ""),
                    "error_status": error_bar.get("status", ""),
                    "error_lower_value": error_bar.get("lower_value", ""),
                    "error_upper_value": error_bar.get("upper_value", ""),
                    "error_lower_pixel": error_bar.get("lower_pixel", ""),
                    "error_upper_pixel": error_bar.get("upper_pixel", ""),
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--overlay", type=Path)
    parser.add_argument("--recreation", type=Path)
    parser.add_argument("--plot-bounds", required=True, type=_parse_bounds)
    parser.add_argument("--value-axis", required=True, type=_parse_axis)
    parser.add_argument("--orientation", choices=sorted(VALID_ORIENTATIONS), required=True)
    parser.add_argument("--layout", choices=sorted(VALID_LAYOUTS), required=True)
    parser.add_argument("--series", action="append", required=True, type=_parse_named_color)
    parser.add_argument("--category", action="append", required=True, type=_parse_category)
    parser.add_argument("--exclude-region", action="append", type=_parse_bounds, default=[])
    parser.add_argument("--baseline-value", type=float, default=0.0)
    parser.add_argument("--color-tolerance", type=float, default=32.0)
    parser.add_argument("--min-area", type=int, default=20)
    parser.add_argument("--min-bar-thickness", type=int, default=3)
    parser.add_argument("--min-bar-length", type=int, default=2)
    parser.add_argument("--bridge-gap", type=int, default=1)
    parser.add_argument("--value-gap", type=int, default=2)
    parser.add_argument("--verified-occluder-bridge-gap", type=int, default=6)
    parser.add_argument(
        "--verified-occluder-min-fraction", type=float, default=0.60
    )
    parser.add_argument("--expected-stack-total", type=float)
    parser.add_argument("--error-color")
    parser.add_argument("--error-tolerance", type=float, default=18.0)
    parser.add_argument("--error-search-radius", type=int, default=2)
    parser.add_argument("--error-min-span", type=int, default=5)
    args = parser.parse_args()
    series_colors = dict(args.series)
    if len(series_colors) != len(args.series):
        raise SystemExit("series names must be unique")
    report = extract_bar_chart(
        args.input,
        plot_bounds=args.plot_bounds,
        value_axis=args.value_axis,
        orientation=args.orientation,
        layout=args.layout,
        series_colors=series_colors,
        categories=args.category,
        exclude_regions=args.exclude_region,
        baseline_value=args.baseline_value,
        tolerance=args.color_tolerance,
        min_area=args.min_area,
        min_bar_thickness=args.min_bar_thickness,
        min_bar_length=args.min_bar_length,
        bridge_gap=args.bridge_gap,
        value_gap=args.value_gap,
        verified_occluder_bridge_gap=args.verified_occluder_bridge_gap,
        verified_occluder_min_fraction=args.verified_occluder_min_fraction,
        expected_stack_total=args.expected_stack_total,
        error_color=args.error_color,
        error_tolerance=args.error_tolerance,
        error_search_radius=args.error_search_radius,
        error_min_span=args.error_min_span,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_csv(args.output_csv, report)
    if args.overlay is not None:
        write_overlay(args.input, report, args.overlay)
    if args.recreation is not None:
        write_recreation(report, args.recreation)
    print(f"STATUS={report['status']}")
    print(f"CSV={args.output_csv}")
    print(f"REPORT={args.report}")


if __name__ == "__main__":
    main()

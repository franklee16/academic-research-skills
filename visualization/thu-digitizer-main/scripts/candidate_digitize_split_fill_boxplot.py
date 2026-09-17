"""Candidate boxplot route for a coloured fill split by a dark median line.

This module does not alter the input raster. It merges only vertically adjacent
fill components that have strongly overlapping horizontal spans, then reuses
the stable boxplot geometry checks for median and whisker evidence. The route
remains candidate-only because unfilled/background-coloured boxes and
same-colour outliers are not recovered.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from digitize_boxplot import (
    _category_band,
    _colour_mask,
    _component_centre,
    _components,
    _extract_groups,
    _horizontal_runs,
    _inclusive_bounds,
    _pixel_to_value,
)


Component = tuple[int, int, int, int, int, int, int]


def _width(component: Component) -> int:
    return component[2] - component[0] + 1


def _vertical_gap(first: Component, second: Component) -> int:
    upper, lower = sorted((first, second), key=lambda item: item[1])
    return lower[1] - upper[3] - 1


def _horizontal_overlap_ratio(first: Component, second: Component) -> float:
    overlap = max(0, min(first[2], second[2]) - max(first[0], second[0]) + 1)
    return overlap / max(1, min(_width(first), _width(second)))


def _merge_pair(first: Component, second: Component) -> Component:
    return (
        min(first[0], second[0]),
        min(first[1], second[1]),
        max(first[2], second[2]),
        max(first[3], second[3]),
        first[4] + second[4],
        first[5] + second[5],
        first[6] + second[6],
    )


def _to_builtin(value):
    """Make private-helper output safe to write as JSON evidence."""
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: _to_builtin(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_builtin(item) for item in value]
    return value


def _horizontal_clusters(
    line_mask: np.ndarray,
    *,
    centre: float,
    box_width: int,
    category_band: tuple[int, int],
    plot_bounds: tuple[int, int, int, int],
) -> list[dict]:
    """Find horizontal structural strokes crossing a box's centre line."""
    centre_pixel = int(round(centre))
    half_window = max(8, int(round(box_width * 0.85)))
    x_start = max(category_band[0], centre_pixel - half_window)
    x_end = min(category_band[1], centre_pixel + half_window)
    minimum_run = max(8, int(round(box_width * 0.45)))
    rows = []
    for y in range(plot_bounds[1], plot_bounds[3] + 1):
        candidates = []
        for run_left, run_right in _horizontal_runs(line_mask, y, x_start, x_end):
            if run_right < centre_pixel - 2 or run_left > centre_pixel + 2:
                continue
            length = run_right - run_left + 1
            if length >= minimum_run:
                candidates.append((length, run_left, run_right))
        if candidates:
            length, run_left, run_right = max(candidates)
            rows.append((y, run_left, run_right, length))

    clusters = []
    for row in rows:
        if not clusters or row[0] > clusters[-1]["row_end"] + 1:
            clusters.append(
                {
                    "row_start": row[0],
                    "row_end": row[0],
                    "run_left": row[1],
                    "run_right": row[2],
                    "maximum_run": row[3],
                }
            )
            continue
        cluster = clusters[-1]
        cluster["row_end"] = row[0]
        cluster["run_left"] = min(cluster["run_left"], row[1])
        cluster["run_right"] = max(cluster["run_right"], row[2])
        cluster["maximum_run"] = max(cluster["maximum_run"], row[3])
    for cluster in clusters:
        cluster["row_center"] = (cluster["row_start"] + cluster["row_end"]) / 2
    return clusters


def _spine_connectivity(
    line_mask: np.ndarray,
    *,
    centre: float,
    first_row: float,
    second_row: float,
) -> dict:
    """Measure tolerant centre-spine evidence between two horizontal strokes."""
    centre_pixel = int(round(centre))
    start = int(round(min(first_row, second_row)))
    end = int(round(max(first_row, second_row)))
    if end <= start:
        return {"connected": True, "coverage": 1.0, "maximum_gap": 0}
    present = [
        bool(line_mask[y, max(0, centre_pixel - 2) : centre_pixel + 3].any())
        for y in range(start, end + 1)
    ]
    maximum_gap = current_gap = 0
    for item in present:
        if item:
            current_gap = 0
        else:
            current_gap += 1
            maximum_gap = max(maximum_gap, current_gap)
    coverage = sum(present) / len(present)
    return {
        "connected": coverage >= 0.55 and maximum_gap <= 3,
        "coverage": coverage,
        "maximum_gap": maximum_gap,
    }


def _candidate_vertical_group(
    *,
    box: Component,
    line_mask: np.ndarray,
    category_band: tuple[int, int],
    plot_bounds: tuple[int, int, int, int],
    y_axis: tuple[float, float, float, float],
) -> dict:
    left, top, right, bottom, *_ = box
    centre = _component_centre(box)[0]
    box_width = right - left + 1
    clusters = _horizontal_clusters(
        line_mask,
        centre=centre,
        box_width=box_width,
        category_band=category_band,
        plot_bounds=plot_bounds,
    )

    # The filled interior starts just below the top border.  Requiring a wide
    # stroke close to that anchor avoids confusing a short whisker cap with Q3.
    q3_candidates = [
        cluster
        for cluster in clusters
        if cluster["row_center"] <= top + 1
        and top - cluster["row_center"] <= 8
        and cluster["maximum_run"] >= box_width
    ]
    q3_cluster = max(q3_candidates, key=lambda item: item["row_center"], default=None)

    median_cluster = q1_cluster = None
    if q3_cluster is not None:
        interior_end = bottom + 8
        following = [
            cluster
            for cluster in clusters
            if q3_cluster["row_center"] < cluster["row_center"] <= interior_end
        ]
        if len(following) >= 2:
            median_cluster, q1_cluster = following[:2]

    upper_cluster = lower_cluster = None
    upper_connectivity = lower_connectivity = None
    if q3_cluster is not None:
        preceding = [
            cluster for cluster in clusters if cluster["row_center"] < q3_cluster["row_center"]
        ]
        if preceding:
            candidate = preceding[-1]
            connection = _spine_connectivity(
                line_mask,
                centre=centre,
                first_row=candidate["row_center"],
                second_row=q3_cluster["row_center"],
            )
            if connection["connected"]:
                upper_cluster = candidate
            upper_connectivity = connection
    if q1_cluster is not None:
        following = [
            cluster for cluster in clusters if cluster["row_center"] > q1_cluster["row_center"]
        ]
        for candidate in following:
            # A whisker is local to the box.  This also prevents the x-axis from
            # becoming a fallback cap when the true cap overlaps Q1.
            if candidate["row_center"] - q1_cluster["row_center"] > 90:
                break
            connection = _spine_connectivity(
                line_mask,
                centre=centre,
                first_row=q1_cluster["row_center"],
                second_row=candidate["row_center"],
            )
            lower_connectivity = connection
            if connection["connected"]:
                lower_cluster = candidate
                break

    def value(cluster):
        return (
            _pixel_to_value(cluster["row_center"], y_axis)
            if cluster is not None
            else None
        )

    core_complete = all(item is not None for item in (q3_cluster, median_cluster, q1_cluster))
    missing = []
    if q3_cluster is None:
        missing.append("Q3 border not anchored to the filled interior")
    if median_cluster is None:
        missing.append("median stroke not separated from box borders")
    if q1_cluster is None:
        missing.append("Q1 border not separated from the median")
    if upper_cluster is None:
        missing.append("upper whisker cap not connected under tolerant validation")
    if lower_cluster is None:
        missing.append("lower whisker cap not connected under tolerant validation")
    return {
        "q1": value(q1_cluster),
        "median": value(median_cluster),
        "q3": value(q3_cluster),
        "lower_whisker": value(lower_cluster),
        "upper_whisker": value(upper_cluster),
        "outliers": [],
        "status": "candidate" if core_complete else "low_confidence",
        "reason": "; ".join(missing),
        "category_center_pixel": centre,
        "box_fill_bounds_pixel": [left, top, right, bottom],
        "stroke_clusters": clusters,
        "upper_spine_evidence": upper_connectivity,
        "lower_spine_evidence": lower_connectivity,
    }


def merge_split_vertical_fills(
    components: list[Component],
    *,
    maximum_gap: int = 6,
    minimum_overlap_ratio: float = 0.75,
) -> tuple[list[Component], list[dict]]:
    """Merge adjacent fill fragments separated by a horizontal median line."""
    merged = list(components)
    diagnostics: list[dict] = []
    changed = True
    while changed:
        changed = False
        for first_index, first in enumerate(merged):
            for second_index in range(first_index + 1, len(merged)):
                second = merged[second_index]
                gap = _vertical_gap(first, second)
                overlap_ratio = _horizontal_overlap_ratio(first, second)
                if 0 <= gap <= maximum_gap and overlap_ratio >= minimum_overlap_ratio:
                    combined = _merge_pair(first, second)
                    diagnostics.append(
                        {
                            "first_bounds": list(first[:4]),
                            "second_bounds": list(second[:4]),
                            "gap_pixels": gap,
                            "horizontal_overlap_ratio": overlap_ratio,
                            "merged_bounds": list(combined[:4]),
                        }
                    )
                    merged[first_index] = combined
                    merged.pop(second_index)
                    changed = True
                    break
            if changed:
                break
    return merged, diagnostics


def extract_split_fill_boxplots(
    image_path: Path,
    *,
    plot_bounds: tuple[int, int, int, int],
    x_axis: tuple[float, float, float, float],
    y_axis: tuple[float, float, float, float],
    box_color: str,
    line_color: str,
    tolerance: float = 18.0,
    min_fragment_area: int = 8,
    maximum_median_gap: int = 6,
    minimum_overlap_ratio: float = 0.75,
) -> dict:
    pixels = np.asarray(Image.open(image_path).convert("RGB"), dtype=np.int16)
    bounds = _inclusive_bounds(plot_bounds, pixels.shape[1], pixels.shape[0])
    if bounds is None:
        return {
            "schema_version": 1,
            "route": "candidate_split_fill_boxplot",
            "status": "low_confidence",
            "reason": "plot bounds do not intersect the image",
            "groups": [],
        }

    box_mask = _colour_mask(pixels, box_color, tolerance, bounds)
    line_mask = _colour_mask(pixels, line_color, tolerance, bounds)
    fragments = [
        component
        for component in _components(box_mask)
        if component[4] >= min_fragment_area and _width(component) >= 3
    ]
    boxes, merge_diagnostics = merge_split_vertical_fills(
        fragments,
        maximum_gap=maximum_median_gap,
        minimum_overlap_ratio=minimum_overlap_ratio,
    )
    groups = _extract_groups(
        orientation="vertical",
        boxes=boxes,
        bounds=bounds,
        line_mask=line_mask,
        outlier_components=[],
        x_axis=x_axis,
        y_axis=y_axis,
    )
    complete = bool(groups) and all(group["status"] == "extracted" for group in groups)
    return {
        "schema_version": 1,
        "route": "candidate_split_fill_boxplot",
        "status": "candidate" if complete else "low_confidence",
        "reason": "" if complete else "one or more merged groups lack required boxplot evidence",
        "orientation": "vertical",
        "plot_bounds": list(bounds),
        "calibration": {"x_axis": list(x_axis), "y_axis": list(y_axis)},
        "colors": {"box_fill": box_color, "line": line_color},
        "parameters": {
            "tolerance": tolerance,
            "min_fragment_area": min_fragment_area,
            "maximum_median_gap": maximum_median_gap,
            "minimum_overlap_ratio": minimum_overlap_ratio,
        },
        "fragment_count": len(fragments),
        "merged_box_count": len(boxes),
        "merge_diagnostics": merge_diagnostics,
        "groups": groups,
        "outlier_status": "not_extracted",
        "limitations": [
            "Only the colour-distinct filled series is recovered.",
            "Background-coloured unfilled boxes are not recovered by this route.",
            "Outliers sharing the line colour are not separated from axes and whiskers.",
            "The route is candidate-only and does not change the stable extractor.",
        ],
    }

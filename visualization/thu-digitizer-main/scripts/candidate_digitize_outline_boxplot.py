"""Candidate extractor for paired filled and unfilled vertical boxplots.

The stable boxplot route intentionally requires colour-distinct fills and
outliers.  Publication figures often violate both assumptions: an unfilled
series shares the white background, the coloured fill is split by its median,
and outlier rings share the structural line colour.  This candidate route uses
repeated stroke geometry instead.  It returns only visible box summaries and
visible outlier rings; it never reconstructs the underlying observations.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from digitize_boxplot import _colour_mask, _horizontal_runs, _inclusive_bounds, _pixel_to_value


def _to_builtin(value):
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: _to_builtin(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_builtin(item) for item in value]
    return value


def _coalesce_rows(rows: list[dict]) -> list[dict]:
    clusters: list[dict] = []
    for row in sorted(rows, key=lambda item: (item["y"], item["left"])):
        match = None
        for cluster in reversed(clusters):
            if row["y"] - cluster["row_end"] > 1:
                break
            row_center = (row["left"] + row["right"]) / 2
            cluster_center = (cluster["run_left"] + cluster["run_right"]) / 2
            overlap = min(row["right"], cluster["run_right"]) - max(
                row["left"], cluster["run_left"]
            ) + 1
            if abs(row_center - cluster_center) <= 3 and overlap >= 5:
                match = cluster
                break
        if match is None:
            clusters.append(
                {
                    "row_start": row["y"],
                    "row_end": row["y"],
                    "run_left": row["left"],
                    "run_right": row["right"],
                    "maximum_run": row["length"],
                }
            )
        else:
            match["row_end"] = row["y"]
            match["run_left"] = min(match["run_left"], row["left"])
            match["run_right"] = max(match["run_right"], row["right"])
            match["maximum_run"] = max(match["maximum_run"], row["length"])
    for cluster in clusters:
        cluster["row_center"] = (cluster["row_start"] + cluster["row_end"]) / 2
        cluster["run_center"] = (cluster["run_left"] + cluster["run_right"]) / 2
    return clusters


def _detect_box_centres(
    line_mask: np.ndarray,
    bounds: tuple[int, int, int, int],
    *,
    minimum_box_width: int,
    maximum_box_width: int,
) -> tuple[list[float], float, list[dict]]:
    rows = []
    for y in range(bounds[1], bounds[3] + 1):
        for left, right in _horizontal_runs(line_mask, y, bounds[0], bounds[2]):
            length = right - left + 1
            if minimum_box_width <= length <= maximum_box_width:
                rows.append({"y": y, "left": left, "right": right, "length": length})
    strokes = _coalesce_rows(rows)
    centre_groups: list[list[dict]] = []
    for stroke in sorted(strokes, key=lambda item: item["run_center"]):
        match = next(
            (
                group
                for group in centre_groups
                if abs(
                    np.mean([item["run_center"] for item in group])
                    - stroke["run_center"]
                )
                <= 4
            ),
            None,
        )
        if match is None:
            centre_groups.append([stroke])
        else:
            match.append(stroke)
    supported = [group for group in centre_groups if len(group) >= 2]
    centres = [float(np.median([item["run_center"] for item in group])) for group in supported]
    widths = [item["maximum_run"] for group in supported for item in group]
    box_width = float(np.median(widths)) if widths else 0.0
    return sorted(centres), box_width, strokes


def _local_strokes(
    line_mask: np.ndarray,
    bounds: tuple[int, int, int, int],
    *,
    centre: float,
    box_width: float,
) -> list[dict]:
    centre_pixel = int(round(centre))
    half_window = max(12, int(round(box_width * 0.72)))
    x_start = max(bounds[0], centre_pixel - half_window)
    x_end = min(bounds[2], centre_pixel + half_window)
    minimum_run = max(6, int(round(box_width * 0.30)))
    rows = []
    for y in range(bounds[1], bounds[3] + 1):
        candidates = []
        for left, right in _horizontal_runs(line_mask, y, x_start, x_end):
            if right < centre_pixel - 2 or left > centre_pixel + 2:
                continue
            length = right - left + 1
            if length >= minimum_run:
                candidates.append((length, left, right))
        if candidates:
            length, left, right = max(candidates)
            rows.append({"y": y, "left": left, "right": right, "length": length})
    return _coalesce_rows(rows)


def _line_coverage(
    mask: np.ndarray,
    *,
    x: float,
    first_row: float,
    second_row: float,
    half_width: int = 2,
) -> float:
    x_pixel = int(round(x))
    top = int(round(min(first_row, second_row)))
    bottom = int(round(max(first_row, second_row)))
    if bottom <= top:
        return 1.0
    present = [
        bool(mask[y, max(0, x_pixel - half_width) : x_pixel + half_width + 1].any())
        for y in range(top, bottom + 1)
    ]
    return sum(present) / len(present)


def _rectangle_side_score(
    mask: np.ndarray,
    *,
    centre: float,
    box_width: float,
    q3_row: float,
    q1_row: float,
) -> float:
    half = box_width / 2
    left = _line_coverage(mask, x=centre - half, first_row=q3_row, second_row=q1_row)
    right = _line_coverage(mask, x=centre + half, first_row=q3_row, second_row=q1_row)
    return (left + right) / 2


def _select_box_trio(
    line_mask: np.ndarray,
    *,
    centre: float,
    box_width: float,
    strokes: list[dict],
) -> tuple[tuple[dict, dict, dict] | None, dict]:
    box_edges = [
        stroke
        for stroke in strokes
        if stroke["maximum_run"] >= max(10, box_width * 0.74)
    ]
    scored = []
    for first_index, q3 in enumerate(box_edges):
        for q1 in box_edges[first_index + 1 :]:
            span = q1["row_center"] - q3["row_center"]
            if span < 4 or span > 120:
                continue
            side_score = _rectangle_side_score(
                line_mask,
                centre=centre,
                box_width=box_width,
                q3_row=q3["row_center"],
                q1_row=q1["row_center"],
            )
            width_scores = [
                max(0.0, 1.0 - abs(stroke["maximum_run"] - box_width) / box_width)
                for stroke in (q3, q1)
            ]
            span_preference = min(1.0, span / max(1.0, box_width * 1.5))
            total = 5.0 * side_score + sum(width_scores) + span_preference
            scored.append(
                {
                    "edges": (q3, q1),
                    "score": total,
                    "side_score": side_score,
                    "width_scores": width_scores,
                    "span_pixels": span,
                }
            )
    if not scored:
        return None, {"reason": "no plausible Q3/Q1 rectangle edges"}
    winner = max(scored, key=lambda item: item["score"])
    diagnostic = {key: value for key, value in winner.items() if key != "edges"}
    if winner["side_score"] < 0.42 or winner["score"] < 4.8:
        diagnostic["reason"] = "best Q3/Q1 pair lacks rectangle-side support"
        return None, diagnostic

    q3, q1 = winner["edges"]
    median_candidates = [
        stroke
        for stroke in strokes
        if q3["row_end"] < stroke["row_center"] < q1["row_start"]
        and stroke["maximum_run"] >= max(10, box_width * 0.74)
    ]
    if median_candidates:
        middle = (q3["row_center"] + q1["row_center"]) / 2
        median = max(
            median_candidates,
            key=lambda stroke: (
                stroke["maximum_run"],
                -abs(stroke["row_center"] - middle),
            ),
        )
        diagnostic["median_coincident_with_q1"] = False
        diagnostic["median_coincident_with_q3"] = False
        diagnostic["median_fraction"] = (
            median["row_center"] - q3["row_center"]
        ) / (q1["row_center"] - q3["row_center"])
        return (q3, median, q1), diagnostic

    # At publication raster resolution a very shallow box can collapse its
    # median onto a quartile edge.  Do not apply this exception to a tall box:
    # that would turn a genuinely missing median into an invented value.
    if winner["span_pixels"] <= 12:
        diagnostic["median_coincident_with_q1"] = True
        diagnostic["median_coincident_with_q3"] = False
        diagnostic["median_fraction"] = 1.0
        return (q3, q1, q1), diagnostic

    diagnostic["reason"] = "Q3/Q1 rectangle found but no internal median stroke"
    return None, diagnostic


def _connected_cap(
    line_mask: np.ndarray,
    *,
    centre: float,
    box_width: float,
    boundary_row: float,
    strokes: list[dict],
    direction: str,
) -> tuple[dict | None, dict]:
    candidates = [
        stroke
        for stroke in strokes
        if (
            stroke["row_center"] < boundary_row
            if direction == "upper"
            else stroke["row_center"] > boundary_row
        )
        and box_width * 0.30 <= stroke["maximum_run"] <= box_width * 0.78
    ]
    candidates.sort(key=lambda item: abs(item["row_center"] - boundary_row))
    checked = []
    for stroke in candidates:
        distance = abs(stroke["row_center"] - boundary_row)
        if distance > 90:
            continue
        coverage = _line_coverage(
            line_mask,
            x=centre,
            first_row=stroke["row_center"],
            second_row=boundary_row,
        )
        checked.append(
            {
                "row_center": stroke["row_center"],
                "distance": distance,
                "spine_coverage": coverage,
            }
        )
        if coverage >= 0.58:
            return stroke, {"checked": checked, "status": "connected"}
    return None, {"checked": checked, "status": "not_connected"}


def _ring_score(mask: np.ndarray, *, centre_x: float, centre_y: int) -> float:
    x = int(round(centre_x))
    if centre_y < 5 or centre_y + 5 >= mask.shape[0] or x < 5 or x + 5 >= mask.shape[1]:
        return 0.0
    patch = mask[centre_y - 5 : centre_y + 6, x - 5 : x + 6]
    total = int(patch.sum())
    if total < 8:
        return 0.0
    top = int(patch[:4, 2:9].sum())
    bottom = int(patch[7:, 2:9].sum())
    left = int(patch[2:9, :4].sum())
    right = int(patch[2:9, 7:].sum())
    centre = int(patch[4:7, 4:7].sum())
    if min(top, bottom, left, right) < 1 or centre > 4:
        return 0.0
    return total + 2 * min(top, bottom, left, right) - 2 * centre


def _visible_outliers(
    line_mask: np.ndarray,
    bounds: tuple[int, int, int, int],
    *,
    centre: float,
    upper_row: float,
    lower_row: float,
    y_axis: tuple[float, float, float, float],
) -> list[dict]:
    candidates = []
    for y in range(bounds[1] + 5, bounds[3] - 4):
        if upper_row - 5 <= y <= lower_row + 5:
            continue
        score = _ring_score(line_mask, centre_x=centre, centre_y=y)
        if score > 0:
            candidates.append((y, score))
    groups: list[list[tuple[int, float]]] = []
    for item in candidates:
        if not groups or item[0] - groups[-1][-1][0] > 4:
            groups.append([item])
        else:
            groups[-1].append(item)
    outliers = []
    for group in groups:
        y, score = max(group, key=lambda item: item[1])
        outliers.append(
            {
                "center_pixel": [centre, float(y)],
                "value": _pixel_to_value(y, y_axis),
                "ring_score": score,
            }
        )
    return outliers


def _fill_fraction(
    fill_mask: np.ndarray,
    *,
    centre: float,
    box_width: float,
    q3_row: float,
    q1_row: float,
) -> float:
    left = max(0, int(round(centre - box_width / 2 + 2)))
    right = min(fill_mask.shape[1] - 1, int(round(centre + box_width / 2 - 2)))
    top = max(0, int(round(q3_row + 2)))
    bottom = min(fill_mask.shape[0] - 1, int(round(q1_row - 2)))
    if left > right or top > bottom:
        return 0.0
    return float(fill_mask[top : bottom + 1, left : right + 1].mean())


def extract_outline_boxplots(
    image_path: Path,
    *,
    plot_bounds: tuple[int, int, int, int],
    y_axis: tuple[float, float, float, float],
    line_color: str,
    filled_series: dict[str, str],
    unfilled_series_label: str,
    tolerance: float = 18.0,
    minimum_box_width: int = 17,
    maximum_box_width: int = 32,
) -> dict:
    pixels = np.asarray(Image.open(image_path).convert("RGB"), dtype=np.int16)
    bounds = _inclusive_bounds(plot_bounds, pixels.shape[1], pixels.shape[0])
    if bounds is None:
        return {
            "schema_version": 1,
            "route": "candidate_outline_boxplot_geometry",
            "status": "low_confidence",
            "reason": "plot bounds do not intersect the image",
            "groups": [],
        }
    line_mask = _colour_mask(pixels, line_color, tolerance, bounds)
    fill_masks = {
        label: _colour_mask(pixels, colour, tolerance, bounds)
        for label, colour in filled_series.items()
    }
    centres, box_width, centre_strokes = _detect_box_centres(
        line_mask,
        bounds,
        minimum_box_width=minimum_box_width,
        maximum_box_width=maximum_box_width,
    )
    if not centres or box_width <= 0:
        return {
            "schema_version": 1,
            "route": "candidate_outline_boxplot_geometry",
            "status": "low_confidence",
            "reason": "repeated box-width stroke centres were not detected",
            "groups": [],
        }

    groups = []
    for centre in centres:
        strokes = _local_strokes(line_mask, bounds, centre=centre, box_width=box_width)
        trio, trio_diagnostic = _select_box_trio(
            line_mask,
            centre=centre,
            box_width=box_width,
            strokes=strokes,
        )
        if trio is None:
            groups.append(
                {
                    "category_center_pixel": centre,
                    "status": "low_confidence",
                    "reason": trio_diagnostic.get("reason", "box stroke trio unresolved"),
                    "stroke_diagnostic": trio_diagnostic,
                }
            )
            continue
        q3, median, q1 = trio
        upper, upper_evidence = _connected_cap(
            line_mask,
            centre=centre,
            box_width=box_width,
            boundary_row=q3["row_center"],
            strokes=strokes,
            direction="upper",
        )
        lower, lower_evidence = _connected_cap(
            line_mask,
            centre=centre,
            box_width=box_width,
            boundary_row=q1["row_center"],
            strokes=strokes,
            direction="lower",
        )
        upper_row = upper["row_center"] if upper is not None else q3["row_center"]
        lower_row = lower["row_center"] if lower is not None else q1["row_center"]
        fill_support = {
            label: _fill_fraction(
                mask,
                centre=centre,
                box_width=box_width,
                q3_row=q3["row_center"],
                q1_row=q1["row_center"],
            )
            for label, mask in fill_masks.items()
        }
        best_filled = max(fill_support, key=fill_support.get, default=None)
        series = (
            best_filled
            if best_filled is not None and fill_support[best_filled] >= 0.20
            else unfilled_series_label
        )
        outliers = _visible_outliers(
            line_mask,
            bounds,
            centre=centre,
            upper_row=upper_row,
            lower_row=lower_row,
            y_axis=y_axis,
        )
        group = {
            "category_center_pixel": centre,
            "series": series,
            "q1": _pixel_to_value(q1["row_center"], y_axis),
            "median": _pixel_to_value(median["row_center"], y_axis),
            "q3": _pixel_to_value(q3["row_center"], y_axis),
            "lower_whisker": _pixel_to_value(lower_row, y_axis),
            "upper_whisker": _pixel_to_value(upper_row, y_axis),
            "outliers": outliers,
            "status": "candidate",
            "reason": "",
            "box_strokes_pixel": {
                "q3": q3["row_center"],
                "median": median["row_center"],
                "q1": q1["row_center"],
            },
            "whisker_strokes_pixel": {
                "upper": upper_row,
                "lower": lower_row,
                "upper_coincident_with_q3": upper is None,
                "lower_coincident_with_q1": lower is None,
            },
            "fill_support": fill_support,
            "stroke_diagnostic": trio_diagnostic,
            "upper_cap_evidence": upper_evidence,
            "lower_cap_evidence": lower_evidence,
        }
        groups.append(group)

    complete = bool(groups) and all(group["status"] == "candidate" for group in groups)
    result = {
        "schema_version": 1,
        "route": "candidate_outline_boxplot_geometry",
        "status": "candidate" if complete else "low_confidence",
        "reason": "" if complete else "one or more repeated stroke groups were unresolved",
        "orientation": "vertical",
        "plot_bounds": list(bounds),
        "calibration": {"y_axis": list(y_axis)},
        "colors": {"line": line_color, "filled_series": filled_series},
        "parameters": {
            "tolerance": tolerance,
            "minimum_box_width": minimum_box_width,
            "maximum_box_width": maximum_box_width,
        },
        "detected_box_width_pixels": box_width,
        "detected_centres": centres,
        "centre_detection_strokes": centre_strokes,
        "groups": groups,
        "limitations": [
            "Only the visible five-number summaries and visible outlier rings are recovered.",
            "The underlying 20 repeat-level observations are not reconstructed.",
            "A raster-coincident median or whisker is reported at the visible quartile row with an explicit diagnostic flag.",
            "This route remains candidate until held-out robustness and comparative promotion gates are complete.",
        ],
    }
    return _to_builtin(result)

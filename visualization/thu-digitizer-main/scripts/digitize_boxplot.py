from collections import deque
from math import ceil, floor
from pathlib import Path

import numpy as np
from PIL import Image


def extract_boxplots(
    image_path: Path,
    *,
    plot_bounds: tuple[int, int, int, int],
    x_axis: tuple[float, float, float, float],
    y_axis: tuple[float, float, float, float],
    box_color: str,
    line_color: str,
    outlier_color: str,
    orientation: str = "auto",
    tolerance: float = 32.0,
    min_area: int = 12,
) -> dict:
    """Recover colour-distinct boxplot geometry from a calibrated image."""
    if orientation not in {"vertical", "horizontal", "auto"}:
        return {
            "orientation": "unknown",
            "groups": [],
            "status": "low_confidence",
            "reason": "unsupported orientation",
        }

    pixels = np.asarray(Image.open(image_path).convert("RGB"), dtype=np.int16)
    bounds = _inclusive_bounds(plot_bounds, pixels.shape[1], pixels.shape[0])
    if bounds is None:
        return {
            "orientation": "unknown" if orientation == "auto" else orientation,
            "groups": [],
            "status": "low_confidence",
            "reason": "plot bounds do not intersect the image",
        }

    box_mask = _colour_mask(pixels, box_color, tolerance, bounds)
    line_mask = _colour_mask(pixels, line_color, tolerance, bounds)
    outlier_mask = _colour_mask(pixels, outlier_color, tolerance, bounds)
    boxes = [component for component in _components(box_mask) if component[4] >= min_area]

    if not boxes:
        return {
            "orientation": "unknown" if orientation == "auto" else orientation,
            "groups": [],
            "status": "low_confidence",
            "reason": (
                "ambiguous_orientation: no box fill components found"
                if orientation == "auto"
                else "no box fill components found"
            ),
        }

    outliers = [component for component in _components(outlier_mask) if component[4] >= min_area]
    if orientation == "auto":
        if len(boxes) < 2:
            return {
                "orientation": "unknown",
                "groups": [],
                "status": "low_confidence",
                "reason": (
                    "ambiguous_orientation: auto orientation requires at least two "
                    "box groups with a unique valid geometric interpretation"
                ),
            }
        candidates = []
        for candidate_orientation in ("vertical", "horizontal"):
            candidate_groups = _extract_groups(
                orientation=candidate_orientation,
                boxes=boxes,
                bounds=bounds,
                line_mask=line_mask,
                outlier_components=outliers,
                x_axis=x_axis,
                y_axis=y_axis,
            )
            score = sum(group["status"] == "extracted" for group in candidate_groups)
            if score == len(boxes):
                candidates.append((candidate_orientation, candidate_groups))
        if len(candidates) != 1:
            return {
                "orientation": "unknown",
                "groups": [],
                "status": "low_confidence",
                "reason": (
                    "ambiguous_orientation: auto orientation requires exactly one "
                    "fully validated geometric interpretation"
                ),
            }
        resolved_orientation, groups = candidates[0]
    else:
        resolved_orientation = orientation
        groups = _extract_groups(
            orientation=resolved_orientation,
            boxes=boxes,
            bounds=bounds,
            line_mask=line_mask,
            outlier_components=outliers,
            x_axis=x_axis,
            y_axis=y_axis,
        )

    complete = all(group["status"] == "extracted" for group in groups)
    return {
        "orientation": resolved_orientation,
        "groups": groups,
        "status": "extracted" if complete else "low_confidence",
        "reason": "" if complete else "one or more groups lack required boxplot evidence",
    }


def _extract_vertical_group(
    *,
    box: tuple[int, int, int, int, int, int, int],
    line_mask: np.ndarray,
    outlier_components: list[tuple[int, int, int, int, int, int, int]],
    category_band: tuple[int, int],
    y_axis: tuple[float, float, float, float],
) -> dict:
    left, top, right, bottom, *_ = box
    centre = _component_centre(box)[0]
    box_width = right - left + 1
    minimum_run = max(3, box_width // 2)
    median_row = _longest_horizontal_run(
        line_mask,
        y_start=top + 1,
        y_end=bottom - 1,
        x_start=left + 1,
        x_end=right - 1,
        minimum_length=minimum_run,
    )
    upper_cap_row, upper_cap_reason = _paired_cap_row(
        line_mask,
        direction="upper",
        box_top=top,
        box_bottom=bottom,
        category_band=category_band,
        spine_center=centre,
        minimum_length=minimum_run,
    )
    lower_cap_row, lower_cap_reason = _paired_cap_row(
        line_mask,
        direction="lower",
        box_top=top,
        box_bottom=bottom,
        category_band=category_band,
        spine_center=centre,
        minimum_length=minimum_run,
    )

    q1 = _pixel_to_value(bottom, y_axis)
    q3 = _pixel_to_value(top, y_axis)
    median = _pixel_to_value(median_row, y_axis) if median_row is not None else None
    upper_whisker = _pixel_to_value(upper_cap_row, y_axis) if upper_cap_row is not None else None
    lower_whisker = _pixel_to_value(lower_cap_row, y_axis) if lower_cap_row is not None else None

    missing = []
    if q1 is None or q3 is None:
        missing.append("invalid y-axis calibration")
    if median_row is None:
        missing.append("missing median line")
    if upper_cap_reason is not None:
        missing.append(upper_cap_reason)
    if lower_cap_reason is not None:
        missing.append(lower_cap_reason)

    visible_outliers = []
    if upper_cap_row is not None and lower_cap_row is not None:
        for component in outlier_components:
            component_centre = _component_centre(component)
            if not category_band[0] <= component_centre[0] <= category_band[1]:
                continue
            if upper_cap_row < component_centre[1] < lower_cap_row:
                continue
            outlier_value = _pixel_to_value(component_centre[1], y_axis)
            if outlier_value is not None:
                visible_outliers.append(
                    {"center_pixel": component_centre, "value": outlier_value}
                )

    return {
        "q1": q1,
        "median": median,
        "q3": q3,
        "lower_whisker": lower_whisker,
        "upper_whisker": upper_whisker,
        "outliers": visible_outliers,
        "status": "low_confidence" if missing else "extracted",
        "reason": "; ".join(missing),
        "category_center_pixel": centre,
        "box_bounds_pixel": (left, top, right, bottom),
    }


def _extract_horizontal_group(
    *,
    box: tuple[int, int, int, int, int, int, int],
    line_mask: np.ndarray,
    outlier_components: list[tuple[int, int, int, int, int, int, int]],
    category_band: tuple[int, int],
    x_axis: tuple[float, float, float, float],
) -> dict:
    left, top, right, bottom, *_ = box
    centre = _component_centre(box)[1]
    box_height = bottom - top + 1
    minimum_run = max(3, box_height // 2)
    median_column = _longest_vertical_run(
        line_mask,
        x_start=left + 1,
        x_end=right - 1,
        y_start=top + 1,
        y_end=bottom - 1,
        minimum_length=minimum_run,
    )
    lower_cap_column, lower_cap_reason = _paired_cap_column(
        line_mask,
        direction="lower",
        box_left=left,
        box_right=right,
        category_band=category_band,
        spine_center=centre,
        minimum_length=minimum_run,
    )
    upper_cap_column, upper_cap_reason = _paired_cap_column(
        line_mask,
        direction="upper",
        box_left=left,
        box_right=right,
        category_band=category_band,
        spine_center=centre,
        minimum_length=minimum_run,
    )

    q1 = _pixel_to_value(left, x_axis)
    q3 = _pixel_to_value(right, x_axis)
    median = _pixel_to_value(median_column, x_axis) if median_column is not None else None
    lower_whisker = _pixel_to_value(lower_cap_column, x_axis) if lower_cap_column is not None else None
    upper_whisker = _pixel_to_value(upper_cap_column, x_axis) if upper_cap_column is not None else None

    missing = []
    if q1 is None or q3 is None:
        missing.append("invalid x-axis calibration")
    if median_column is None:
        missing.append("missing median line")
    if lower_cap_reason is not None:
        missing.append(lower_cap_reason)
    if upper_cap_reason is not None:
        missing.append(upper_cap_reason)

    visible_outliers = []
    if lower_cap_column is not None and upper_cap_column is not None:
        for component in outlier_components:
            component_centre = _component_centre(component)
            if not category_band[0] <= component_centre[1] <= category_band[1]:
                continue
            if lower_cap_column < component_centre[0] < upper_cap_column:
                continue
            outlier_value = _pixel_to_value(component_centre[0], x_axis)
            if outlier_value is not None:
                visible_outliers.append(
                    {"center_pixel": component_centre, "value": outlier_value}
                )

    return {
        "q1": q1,
        "median": median,
        "q3": q3,
        "lower_whisker": lower_whisker,
        "upper_whisker": upper_whisker,
        "outliers": visible_outliers,
        "status": "low_confidence" if missing else "extracted",
        "reason": "; ".join(missing),
        "category_center_pixel": centre,
        "box_bounds_pixel": (left, top, right, bottom),
    }


def _inclusive_bounds(
    plot_bounds: tuple[int, int, int, int], image_width: int, image_height: int):
    left, top, right, bottom = plot_bounds
    left, top = max(0, left), max(0, top)
    right, bottom = min(image_width - 1, right), min(image_height - 1, bottom)
    if left > right or top > bottom:
        return None
    return left, top, right, bottom


def _colour_mask(
    pixels: np.ndarray,
    colour: str,
    tolerance: float,
    bounds: tuple[int, int, int, int],
) -> np.ndarray:
    target = np.asarray(_parse_colour(colour), dtype=np.int16)
    distance = np.linalg.norm(pixels - target, axis=2)
    mask = np.zeros(distance.shape, dtype=bool)
    left, top, right, bottom = bounds
    mask[top : bottom + 1, left : right + 1] = (
        distance[top : bottom + 1, left : right + 1] <= tolerance
    )
    return mask


def _parse_colour(colour: str) -> tuple[int, int, int]:
    value = colour.lstrip("#")
    if len(value) != 6:
        raise ValueError("colours must be six-digit hexadecimal RGB values")
    return tuple(int(value[offset : offset + 2], 16) for offset in range(0, 6, 2))


def _components(mask: np.ndarray) -> list[tuple[int, int, int, int, int, int, int]]:
    height, width = mask.shape
    visited = np.zeros(mask.shape, dtype=bool)
    components = []
    for y, x in zip(*np.nonzero(mask)):
        if visited[y, x]:
            continue
        queue = deque([(x, y)])
        visited[y, x] = True
        left = right = x
        top = bottom = y
        size = 0
        x_total = 0
        y_total = 0
        while queue:
            current_x, current_y = queue.popleft()
            size += 1
            x_total += current_x
            y_total += current_y
            left, right = min(left, current_x), max(right, current_x)
            top, bottom = min(top, current_y), max(bottom, current_y)
            for next_x, next_y in (
                (current_x - 1, current_y),
                (current_x + 1, current_y),
                (current_x, current_y - 1),
                (current_x, current_y + 1),
            ):
                if (
                    0 <= next_x < width
                    and 0 <= next_y < height
                    and mask[next_y, next_x]
                    and not visited[next_y, next_x]
                ):
                    visited[next_y, next_x] = True
                    queue.append((next_x, next_y))
        components.append((left, top, right, bottom, size, x_total, y_total))
    return components


def _extract_groups(
    *,
    orientation: str,
    boxes: list[tuple[int, int, int, int, int, int, int]],
    bounds: tuple[int, int, int, int],
    line_mask: np.ndarray,
    outlier_components: list[tuple[int, int, int, int, int, int, int]],
    x_axis: tuple[float, float, float, float],
    y_axis: tuple[float, float, float, float],
) -> list[dict]:
    if orientation == "vertical":
        ordered_boxes = sorted(boxes, key=lambda component: (_component_centre(component)[0], component[1]))
        centres = [_component_centre(box)[0] for box in ordered_boxes]
        category_min, category_max = bounds[0], bounds[2]
    else:
        ordered_boxes = sorted(boxes, key=lambda component: (_component_centre(component)[1], component[0]))
        centres = [_component_centre(box)[1] for box in ordered_boxes]
        category_min, category_max = bounds[1], bounds[3]

    groups = []
    for index, box in enumerate(ordered_boxes):
        category_band = _category_band(index, centres, category_min, category_max)
        if orientation == "vertical":
            groups.append(
                _extract_vertical_group(
                    box=box,
                    line_mask=line_mask,
                    outlier_components=outlier_components,
                    category_band=category_band,
                    y_axis=y_axis,
                )
            )
        else:
            groups.append(
                _extract_horizontal_group(
                    box=box,
                    line_mask=line_mask,
                    outlier_components=outlier_components,
                    category_band=category_band,
                    x_axis=x_axis,
                )
            )
    return groups


def _category_band(
    index: int,
    centres: list[float],
    plot_left: int,
    plot_right: int,
) -> tuple[int, int]:
    left = plot_left if index == 0 else int((centres[index - 1] + centres[index]) // 2) + 1
    right = plot_right if index == len(centres) - 1 else int((centres[index] + centres[index + 1]) // 2)
    return left, right


def _longest_horizontal_run(
    mask: np.ndarray,
    *,
    y_start: int,
    y_end: int,
    x_start: int,
    x_end: int,
    minimum_length: int,
    prefer_nearest_to: int | None = None,
) -> int | None:
    candidates = []
    for y in range(max(0, y_start), min(mask.shape[0] - 1, y_end) + 1):
        run_length = 0
        longest = 0
        for x in range(max(0, x_start), min(mask.shape[1] - 1, x_end) + 1):
            if mask[y, x]:
                run_length += 1
                longest = max(longest, run_length)
            else:
                run_length = 0
        if longest >= minimum_length:
            candidates.append((longest, y))
    if not candidates:
        return None
    if prefer_nearest_to is None:
        return max(candidates, key=lambda item: item[0])[1]
    return max(candidates, key=lambda item: (item[0], -abs(item[1] - prefer_nearest_to)))[1]


def _longest_vertical_run(
    mask: np.ndarray,
    *,
    x_start: int,
    x_end: int,
    y_start: int,
    y_end: int,
    minimum_length: int,
) -> int | None:
    candidates = []
    for x in range(max(0, x_start), min(mask.shape[1] - 1, x_end) + 1):
        run_length = 0
        longest = 0
        for y in range(max(0, y_start), min(mask.shape[0] - 1, y_end) + 1):
            if mask[y, x]:
                run_length += 1
                longest = max(longest, run_length)
            else:
                run_length = 0
        if longest >= minimum_length:
            candidates.append((longest, x))
    if not candidates:
        return None
    return max(candidates, key=lambda item: item[0])[1]


def _paired_cap_row(
    mask: np.ndarray,
    *,
    direction: str,
    box_top: int,
    box_bottom: int,
    category_band: tuple[int, int],
    spine_center: float,
    minimum_length: int,
) -> tuple[float | None, str | None]:
    if direction == "upper":
        rows = range(0, box_top)
        boundary_row = box_top - 1
    else:
        rows = range(box_bottom + 1, mask.shape[0])
        boundary_row = box_bottom + 1

    valid_rows = []
    for y in rows:
        for run_left, run_right in _horizontal_runs(mask, y, *category_band):
            if run_right - run_left + 1 < minimum_length:
                continue
            if run_left > ceil(spine_center) + 1 or run_right < floor(spine_center) - 1:
                continue
            if _spine_connects_to_box_boundary(mask, y, boundary_row, spine_center):
                valid_rows.append(y)
                break

    label = f"{direction} whisker cap"
    cap_rows = _coalesce_contiguous_candidates(valid_rows)
    if not cap_rows:
        return None, f"missing {label} connected to the whisker spine"
    if len(cap_rows) != 1:
        return None, f"ambiguous {label} candidates connected to the whisker spine"
    return cap_rows[0], None


def _paired_cap_column(
    mask: np.ndarray,
    *,
    direction: str,
    box_left: int,
    box_right: int,
    category_band: tuple[int, int],
    spine_center: float,
    minimum_length: int,
) -> tuple[float | None, str | None]:
    if direction == "lower":
        columns = range(0, box_left)
        boundary_column = box_left - 1
    else:
        columns = range(box_right + 1, mask.shape[1])
        boundary_column = box_right + 1

    valid_columns = []
    for x in columns:
        for run_top, run_bottom in _vertical_runs(mask, x, *category_band):
            if run_bottom - run_top + 1 < minimum_length:
                continue
            if run_top > ceil(spine_center) + 1 or run_bottom < floor(spine_center) - 1:
                continue
            if _horizontal_spine_connects_to_box_boundary(
                mask, x, boundary_column, spine_center
            ):
                valid_columns.append(x)
                break

    label = f"{direction} whisker cap"
    cap_columns = _coalesce_contiguous_candidates(valid_columns)
    if not cap_columns:
        return None, f"missing {label} connected to the whisker spine"
    if len(cap_columns) != 1:
        return None, f"ambiguous {label} candidates connected to the whisker spine"
    return cap_columns[0], None


def _coalesce_contiguous_candidates(candidates: list[int]) -> list[float]:
    if not candidates:
        return []
    coalesced = []
    start = end = sorted(set(candidates))[0]
    for candidate in sorted(set(candidates))[1:]:
        if candidate == end + 1:
            end = candidate
            continue
        coalesced.append((start + end) / 2)
        start = end = candidate
    coalesced.append((start + end) / 2)
    return coalesced


def _horizontal_runs(mask: np.ndarray, y: int, x_start: int, x_end: int) -> list[tuple[int, int]]:
    runs = []
    run_start = None
    for x in range(max(0, x_start), min(mask.shape[1] - 1, x_end) + 1):
        if mask[y, x] and run_start is None:
            run_start = x
        elif not mask[y, x] and run_start is not None:
            runs.append((run_start, x - 1))
            run_start = None
    if run_start is not None:
        runs.append((run_start, min(mask.shape[1] - 1, x_end)))
    return runs


def _vertical_runs(mask: np.ndarray, x: int, y_start: int, y_end: int) -> list[tuple[int, int]]:
    runs = []
    run_start = None
    for y in range(max(0, y_start), min(mask.shape[0] - 1, y_end) + 1):
        if mask[y, x] and run_start is None:
            run_start = y
        elif not mask[y, x] and run_start is not None:
            runs.append((run_start, y - 1))
            run_start = None
    if run_start is not None:
        runs.append((run_start, min(mask.shape[0] - 1, y_end)))
    return runs


def _spine_connects_to_box_boundary(
    mask: np.ndarray,
    cap_row: int,
    boundary_row: int,
    spine_center: float,
) -> bool:
    spine_left = max(0, floor(spine_center) - 1)
    spine_right = min(mask.shape[1] - 1, ceil(spine_center) + 1)
    top, bottom = sorted((cap_row, boundary_row))
    if not any(
        mask[y, x]
        for y in range(top + 1, bottom)
        for x in range(spine_left, spine_right + 1)
    ):
        return False
    starts = [
        (x, cap_row)
        for x in range(spine_left, spine_right + 1)
        if mask[cap_row, x]
    ]
    if not starts:
        return False

    queue = deque(starts)
    visited = set(starts)
    while queue:
        x, y = queue.popleft()
        if y == boundary_row:
            return True
        for next_x, next_y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if (
                spine_left <= next_x <= spine_right
                and top <= next_y <= bottom
                and mask[next_y, next_x]
                and (next_x, next_y) not in visited
            ):
                visited.add((next_x, next_y))
                queue.append((next_x, next_y))
    return False


def _horizontal_spine_connects_to_box_boundary(
    mask: np.ndarray,
    cap_column: int,
    boundary_column: int,
    spine_center: float,
) -> bool:
    spine_top = max(0, floor(spine_center) - 1)
    spine_bottom = min(mask.shape[0] - 1, ceil(spine_center) + 1)
    left, right = sorted((cap_column, boundary_column))
    if not any(
        mask[y, x]
        for x in range(left + 1, right)
        for y in range(spine_top, spine_bottom + 1)
    ):
        return False
    starts = [
        (cap_column, y)
        for y in range(spine_top, spine_bottom + 1)
        if mask[y, cap_column]
    ]
    if not starts:
        return False

    queue = deque(starts)
    visited = set(starts)
    while queue:
        x, y = queue.popleft()
        if x == boundary_column:
            return True
        for next_x, next_y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if (
                left <= next_x <= right
                and spine_top <= next_y <= spine_bottom
                and mask[next_y, next_x]
                and (next_x, next_y) not in visited
            ):
                visited.add((next_x, next_y))
                queue.append((next_x, next_y))
    return False


def _pixel_to_value(pixel: float, axis: tuple[float, float, float, float]) -> float | None:
    pixel_start, value_start, pixel_end, value_end = axis
    if pixel_end == pixel_start:
        return None
    return value_start + (pixel - pixel_start) * (value_end - value_start) / (pixel_end - pixel_start)


def _component_centre(
    component: tuple[int, int, int, int, int, int, int],
) -> tuple[float, float]:
    _, _, _, _, size, x_total, y_total = component
    return x_total / size, y_total / size

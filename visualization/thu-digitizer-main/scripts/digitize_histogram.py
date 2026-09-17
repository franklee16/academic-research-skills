from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


def _rgb_from_hex(color):
    if not isinstance(color, str) or len(color) != 7 or not color.startswith("#"):
        raise ValueError("bar_color must be a #RRGGBB string")
    try:
        return np.array(
            [int(color[index : index + 2], 16) for index in (1, 3, 5)],
            dtype=np.int16,
        )
    except ValueError as error:
        raise ValueError("bar_color must be a #RRGGBB string") from error


def _color_mask(image, bar_color, tolerance):
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")

    difference = image.astype(np.int16) - _rgb_from_hex(bar_color)
    squared_distance = np.sum(difference.astype(np.int32) ** 2, axis=2)
    return squared_distance <= tolerance**2


def _connected_components(mask):
    rows, columns = mask.shape
    visited = np.zeros(mask.shape, dtype=bool)
    components = []

    for row in range(rows):
        for column in range(columns):
            if not mask[row, column] or visited[row, column]:
                continue

            queue = deque([(row, column)])
            visited[row, column] = True
            area = 0
            min_row = max_row = row
            min_column = max_column = column

            while queue:
                current_row, current_column = queue.popleft()
                area += 1
                min_row = min(min_row, current_row)
                max_row = max(max_row, current_row)
                min_column = min(min_column, current_column)
                max_column = max(max_column, current_column)

                for row_offset in (-1, 0, 1):
                    for column_offset in (-1, 0, 1):
                        if row_offset == 0 and column_offset == 0:
                            continue
                        neighbor_row = current_row + row_offset
                        neighbor_column = current_column + column_offset
                        if (
                            0 <= neighbor_row < rows
                            and 0 <= neighbor_column < columns
                            and mask[neighbor_row, neighbor_column]
                            and not visited[neighbor_row, neighbor_column]
                        ):
                            visited[neighbor_row, neighbor_column] = True
                            queue.append((neighbor_row, neighbor_column))

            components.append(
                (area, min_row, max_row, min_column, max_column)
            )

    return components


def _pixel_to_data(pixel, axis):
    pixel_start, data_start, pixel_end, data_end = axis
    if pixel_end == pixel_start:
        raise ValueError("axis pixel calibration points must differ")
    slope = (data_end - data_start) / (pixel_end - pixel_start)
    return float(data_start + (pixel - pixel_start) * slope)


def extract_histogram(
    image_path: Path,
    *,
    plot_bounds: tuple[int, int, int, int],
    x_axis: tuple[float, float, float, float],
    y_axis: tuple[float, float, float, float],
    bar_color: str,
    tolerance: float = 32.0,
    min_area: int = 12,
) -> list[dict[str, float]]:
    """Extract color-matched histogram bars as calibrated data bins."""
    with Image.open(image_path) as source_image:
        image = np.asarray(source_image.convert("RGB"))
    mask = _color_mask(image, bar_color, tolerance)

    left, top, right, bottom = plot_bounds
    image_rows, image_columns = mask.shape
    if not (0 <= left <= right < image_columns and 0 <= top <= bottom < image_rows):
        raise ValueError("plot_bounds must be inclusive bounds within the image")

    view = mask[top : bottom + 1, left : right + 1]
    if not view.any():
        return []

    bins = []
    for area, min_row, max_row, min_column, max_column in _connected_components(
        view
    ):
        if area < min_area:
            continue

        left_pixel = left + min_column
        right_pixel = left + max_column + 1
        top_pixel = top + min_row
        bottom_pixel = top + max_row + 1
        bins.append(
            {
                "x_left": float(_pixel_to_data(left_pixel, x_axis)),
                "x_right": float(_pixel_to_data(right_pixel, x_axis)),
                "height": float(_pixel_to_data(top_pixel, y_axis)),
                "left_pixel": float(left_pixel),
                "right_pixel": float(right_pixel),
                "top_pixel": float(top_pixel),
                "bottom_pixel": float(bottom_pixel),
                "pixel_area": float(area),
            }
        )

    return sorted(bins, key=lambda bin_: bin_["x_left"])

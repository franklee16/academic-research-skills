"""Candidate calibrated raster heatmap extractor.

The route recovers a declared row/column grid, the colour encoded value of
each visible cell, and visible white significance marks.  Values at the ends
of the colour bar are interval-censored because a clipped raster colour cannot
distinguish the endpoint from a magnitude beyond it.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def _mode_rgb(pixels: np.ndarray) -> np.ndarray:
    flat = pixels.reshape(-1, 3)
    colours, counts = np.unique(flat, axis=0, return_counts=True)
    return colours[int(np.argmax(counts))]


def _visible_white_mark(
    pixels: np.ndarray,
    *,
    fill: np.ndarray,
    center_x: float,
    center_y: float,
    cell_bounds: tuple[int, int, int, int],
) -> tuple[bool, int]:
    left, top, right, bottom = cell_bounds
    x = int(round(center_x))
    y = int(round(center_y))
    patch_left = max(left + 2, x - 7)
    patch_right = min(right - 2, x + 7)
    patch_top = max(top + 2, y - 7)
    patch_bottom = min(bottom - 2, y + 7)
    if patch_left > patch_right or patch_top > patch_bottom:
        return False, 0
    patch = pixels[patch_top : patch_bottom + 1, patch_left : patch_right + 1]
    distance = np.linalg.norm(patch.astype(float) - fill.astype(float), axis=2)
    white = (patch.mean(axis=2) > 220) & (distance > 25)
    count = int(white.sum())
    return count >= 5, count


def extract_heatmap(
    image_path: Path,
    *,
    grid_bounds: tuple[float, float, float, float],
    row_labels: list[str],
    column_labels: list[str],
    colorbar_bounds: tuple[int, int, int, int],
    colorbar_top_value: float,
    colorbar_bottom_value: float,
    cell_margin: int = 3,
    maximum_palette_distance: float = 15.0,
) -> dict:
    pixels = np.asarray(Image.open(image_path).convert("RGB"))
    height, width = pixels.shape[:2]
    left, top, right, bottom = grid_bounds
    bar_left, bar_top, bar_right, bar_bottom = colorbar_bounds
    if (
        not row_labels
        or not column_labels
        or left < 0
        or top < 0
        or right >= width
        or bottom >= height
        or left >= right
        or top >= bottom
        or bar_left < 0
        or bar_top < 0
        or bar_right >= width
        or bar_bottom >= height
        or bar_left > bar_right
        or bar_top >= bar_bottom
    ):
        return {
            "schema_version": 1,
            "route": "candidate_calibrated_heatmap",
            "status": "low_confidence",
            "reason": "invalid grid, labels, or colour-bar bounds",
            "cells": [],
        }

    x_boundaries = np.linspace(left, right, len(column_labels) + 1)
    y_boundaries = np.linspace(top, bottom, len(row_labels) + 1)
    palette = np.asarray(
        [
            _mode_rgb(pixels[y, bar_left : bar_right + 1])
            for y in range(bar_top, bar_bottom + 1)
        ],
        dtype=float,
    )
    palette_values = np.linspace(
        colorbar_top_value, colorbar_bottom_value, len(palette)
    )

    cells = []
    for row_index, row_label in enumerate(row_labels):
        for column_index, column_label in enumerate(column_labels):
            cell_left = int(np.ceil(x_boundaries[column_index]))
            cell_right = int(np.floor(x_boundaries[column_index + 1]))
            cell_top = int(np.ceil(y_boundaries[row_index]))
            cell_bottom = int(np.floor(y_boundaries[row_index + 1]))
            sample_left = cell_left + cell_margin
            sample_right = cell_right - cell_margin
            sample_top = cell_top + cell_margin
            sample_bottom = cell_bottom - cell_margin
            if sample_left > sample_right or sample_top > sample_bottom:
                cells.append(
                    {
                        "row_index": row_index,
                        "column_index": column_index,
                        "row_label": row_label,
                        "column_label": column_label,
                        "status": "low_confidence",
                        "reason": "cell interior is empty after excluding grid borders",
                    }
                )
                continue
            fill = _mode_rgb(
                pixels[
                    sample_top : sample_bottom + 1,
                    sample_left : sample_right + 1,
                ]
            ).astype(float)
            distances = np.linalg.norm(palette - fill, axis=1)
            palette_index = int(np.argmin(distances))
            palette_distance = float(distances[palette_index])
            visible_mark, white_pixel_count = _visible_white_mark(
                pixels,
                fill=fill,
                center_x=(x_boundaries[column_index] + x_boundaries[column_index + 1])
                / 2,
                center_y=(y_boundaries[row_index] + y_boundaries[row_index + 1])
                / 2,
                cell_bounds=(cell_left, cell_top, cell_right, cell_bottom),
            )
            if palette_index == 0:
                value_status = "clipped_high"
                value = colorbar_top_value
                interval = [colorbar_top_value, None]
            elif palette_index == len(palette) - 1:
                value_status = "clipped_low"
                value = colorbar_bottom_value
                interval = [None, colorbar_bottom_value]
            else:
                value_status = "numeric"
                value = float(palette_values[palette_index])
                interval = None
            cells.append(
                {
                    "row_index": row_index,
                    "column_index": column_index,
                    "row_label": row_label,
                    "column_label": column_label,
                    "value": value,
                    "value_status": value_status,
                    "value_interval": interval,
                    "significant_visible": visible_mark,
                    "white_mark_pixel_count": white_pixel_count,
                    "fill_rgb": [int(item) for item in fill],
                    "palette_index": palette_index,
                    "palette_pixel_y": bar_top + palette_index,
                    "palette_distance_rgb": palette_distance,
                    "cell_bounds_pixel": [cell_left, cell_top, cell_right, cell_bottom],
                    "cell_center_pixel": [
                        float(
                            (x_boundaries[column_index] + x_boundaries[column_index + 1])
                            / 2
                        ),
                        float(
                            (y_boundaries[row_index] + y_boundaries[row_index + 1])
                            / 2
                        ),
                    ],
                    "status": (
                        "candidate"
                        if palette_distance <= maximum_palette_distance
                        else "low_confidence"
                    ),
                    "reason": (
                        ""
                        if palette_distance <= maximum_palette_distance
                        else "cell colour is too far from the calibrated colour bar"
                    ),
                }
            )

    complete = bool(cells) and all(cell["status"] == "candidate" for cell in cells)
    return {
        "schema_version": 1,
        "route": "candidate_calibrated_heatmap",
        "status": "candidate" if complete else "low_confidence",
        "reason": "" if complete else "one or more cells failed colour-bar validation",
        "grid_bounds": [left, top, right, bottom],
        "row_labels": row_labels,
        "column_labels": column_labels,
        "x_boundaries_pixel": [float(value) for value in x_boundaries],
        "y_boundaries_pixel": [float(value) for value in y_boundaries],
        "colorbar": {
            "bounds": list(colorbar_bounds),
            "top_value": colorbar_top_value,
            "bottom_value": colorbar_bottom_value,
            "palette_rows": len(palette),
            "palette_rgb": [[int(round(channel)) for channel in row] for row in palette],
        },
        "parameters": {
            "cell_margin": cell_margin,
            "maximum_palette_distance": maximum_palette_distance,
        },
        "cell_count": len(cells),
        "cells": cells,
        "limitations": [
            "The route recovers colour-encoded cell values, not unplotted source variables.",
            "A cell matching a colour-bar endpoint is interval-censored because clipping hides any magnitude beyond that endpoint.",
            "Only visibly rendered white significance marks are returned; invisible or omitted source flags are not invented.",
            "The route is candidate-only pending held-out heatmap cases and comparative promotion gates.",
        ],
    }

"""Candidate vector-PDF extractor for dose-response plots.

The extractor recovers only geometry visibly encoded in a PDF: marker centres,
visible error-bar endpoints, and sampled fitted-curve paths.  It does not infer
raw replicates or claim that traced curves contain the authors' fit parameters.

This module is intentionally candidate quality.  Callers must supply a verified
panel ROI, a verified main-plot ROI, linear calibration anchors for the displayed
log-concentration coordinate and y axis, and the vector colours/marker shapes for
each series.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import fitz


def colour_hex(colour: tuple[float, float, float] | None) -> str | None:
    if colour is None:
        return None
    return "#" + "".join(f"{round(channel * 255):02x}" for channel in colour)


@dataclass(frozen=True)
class LinearCalibration:
    pixel_1: float
    value_1: float
    pixel_2: float
    value_2: float

    def value(self, pixel: float) -> float:
        return self.value_1 + (pixel - self.pixel_1) * (
            (self.value_2 - self.value_1) / (self.pixel_2 - self.pixel_1)
        )

    def as_dict(self) -> dict[str, float | str]:
        return {
            "transform": "linear_in_displayed_coordinate",
            "pixel_1": self.pixel_1,
            "value_1": self.value_1,
            "pixel_2": self.pixel_2,
            "value_2": self.value_2,
        }


@dataclass(frozen=True)
class SeriesSpec:
    name: str
    marker_shape: str
    marker_colour: str
    curve_colour: str


def _shape_matches(drawing: dict[str, Any], shape: str) -> bool:
    rect = drawing["rect"]
    if not (2.4 <= rect.width <= 5.2 and 2.4 <= rect.height <= 5.2):
        return False
    if not 0.65 <= rect.width / rect.height <= 1.5:
        return False
    operations = [item[0] for item in drawing["items"]]
    if shape == "square":
        return operations == ["re"]
    if shape == "triangle":
        return operations == ["l", "l", "l"]
    if shape == "circle":
        return operations == ["c", "c", "c", "c"]
    raise ValueError(f"Unsupported marker shape: {shape}")


def _centre(rect: fitz.Rect) -> tuple[float, float]:
    return ((rect.x0 + rect.x1) / 2, (rect.y0 + rect.y1) / 2)


def _rect_overlaps(rect: fitz.Rect, roi: fitz.Rect) -> bool:
    """Inclusive overlap that also accepts zero-width/height vector segments."""

    return not (
        rect.x1 < roi.x0
        or rect.x0 > roi.x1
        or rect.y1 < roi.y0
        or rect.y0 > roi.y1
    )


def _path_points(items: Iterable[tuple]) -> list[tuple[float, float]]:
    items = list(items)
    if not items:
        return []
    points = [(float(items[0][1].x), float(items[0][1].y))]
    for item in items:
        endpoint = item[-1]
        points.append((float(endpoint.x), float(endpoint.y)))
    deduplicated: list[tuple[float, float]] = []
    for point in points:
        if not deduplicated or point != deduplicated[-1]:
            deduplicated.append(point)
    return deduplicated


def _simple_coloured_segments(
    drawings: list[dict[str, Any]],
    *,
    colour: str,
    roi: fitz.Rect,
) -> list[tuple[float, float, float, float, int]]:
    segments = []
    for drawing_index, drawing in enumerate(drawings):
        if colour_hex(drawing.get("color")) != colour:
            continue
        if not _rect_overlaps(drawing["rect"], roi):
            continue
        if len(drawing["items"]) != 1 or drawing["items"][0][0] != "l":
            continue
        _, start, end = drawing["items"][0]
        segments.append((float(start.x), float(start.y), float(end.x), float(end.y), drawing_index))
    return segments


def extract_dose_response_pdf(
    pdf_path: Path,
    *,
    page_number: int,
    panel_roi: tuple[float, float, float, float],
    main_plot_roi: tuple[float, float, float, float],
    x_calibration: LinearCalibration,
    y_calibration: LinearCalibration,
    series_specs: list[SeriesSpec],
) -> dict[str, Any]:
    """Extract visible dose-response geometry from one verified PDF panel."""

    if not pdf_path.is_file():
        raise FileNotFoundError(pdf_path)
    with fitz.open(pdf_path) as document:
        if not 1 <= page_number <= len(document):
            raise ValueError(f"page_number must be within 1..{len(document)}")
        page = document[page_number - 1]
        drawings = page.get_drawings()

    panel = fitz.Rect(*panel_roi)
    main_plot = fitz.Rect(*main_plot_roi)
    points: list[dict[str, Any]] = []
    curves: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []

    for spec in series_specs:
        marker_drawings: list[tuple[int, dict[str, Any]]] = []
        for drawing_index, drawing in enumerate(drawings):
            if colour_hex(drawing.get("color")) != spec.marker_colour:
                continue
            if not drawing["rect"].intersects(panel):
                continue
            if _shape_matches(drawing, spec.marker_shape):
                marker_drawings.append((drawing_index, drawing))
        marker_drawings.sort(key=lambda item: _centre(item[1]["rect"])[0])

        segments = _simple_coloured_segments(
            drawings,
            colour=spec.marker_colour,
            roi=main_plot,
        )
        for marker_index, (drawing_index, drawing) in enumerate(marker_drawings):
            x_pt, y_pt = _centre(drawing["rect"])
            segment = "main" if main_plot.x0 <= x_pt <= main_plot.x1 else "vehicle"
            error_lower = None
            error_upper = None
            error_drawing_indices: list[int] = []
            if segment == "main":
                nearby = [
                    item
                    for item in segments
                    if abs(((item[0] + item[2]) / 2) - x_pt) <= 0.85
                    and main_plot.y0 <= min(item[1], item[3])
                    and max(item[1], item[3]) <= main_plot.y1
                ]
                if nearby:
                    endpoint_y = [coordinate for item in nearby for coordinate in (item[1], item[3])]
                    error_upper = y_calibration.value(min(endpoint_y))
                    error_lower = y_calibration.value(max(endpoint_y))
                    error_drawing_indices = sorted({item[4] for item in nearby})

            points.append(
                {
                    "series": spec.name,
                    "marker_shape": spec.marker_shape,
                    "marker_index": marker_index,
                    "segment": segment,
                    "display_x": 0.0 if segment == "vehicle" else x_calibration.value(x_pt),
                    "log10_molar": None if segment == "vehicle" else x_calibration.value(x_pt),
                    "plotted_value": y_calibration.value(y_pt),
                    "error_lower": error_lower,
                    "error_upper": error_upper,
                    "pdf_x_pt": x_pt,
                    "pdf_y_pt": y_pt,
                    "marker_drawing_index": drawing_index,
                    "error_drawing_indices": error_drawing_indices,
                    "status": "vector_marker_extracted",
                }
            )

        curve_candidates = [
            (drawing_index, drawing)
            for drawing_index, drawing in enumerate(drawings)
            if colour_hex(drawing.get("color")) == spec.curve_colour
            and drawing["rect"].intersects(main_plot)
            and len(drawing["items"]) >= 20
        ]
        if curve_candidates:
            drawing_index, drawing = max(curve_candidates, key=lambda item: len(item[1]["items"]))
            curve_points = _path_points(drawing["items"])
            curves.append(
                {
                    "series": spec.name,
                    "status": "curve_path_traced",
                    "drawing_index": drawing_index,
                    "points": [
                        {
                            "log10_molar": x_calibration.value(x_pt),
                            "plotted_value": y_calibration.value(y_pt),
                            "pdf_x_pt": x_pt,
                            "pdf_y_pt": y_pt,
                        }
                        for x_pt, y_pt in curve_points
                        if main_plot.x0 <= x_pt <= main_plot.x1
                    ],
                }
            )

        diagnostics.append(
            {
                "series": spec.name,
                "marker_count": len(marker_drawings),
                "main_marker_count": sum(
                    main_plot.x0 <= _centre(drawing["rect"])[0] <= main_plot.x1
                    for _, drawing in marker_drawings
                ),
                "simple_error_segment_count": len(segments),
                "curve_candidate_count": len(curve_candidates),
            }
        )

    return {
        "status": "candidate",
        "route": "verified_vector_pdf_geometry",
        "page_number_1_based": page_number,
        "panel_roi_pt": list(panel_roi),
        "main_plot_roi_pt": list(main_plot_roi),
        "calibration": {
            "x": {
                **x_calibration.as_dict(),
                "coordinate": "displayed log10 molar concentration",
            },
            "y": {
                **y_calibration.as_dict(),
                "coordinate": "percent of maximum cAMP response",
            },
            "vehicle_segment": {
                "display_value": 0,
                "meaning": "vehicle/control point on the left side of a broken x axis",
            },
        },
        "series": [spec.__dict__ for spec in series_specs],
        "points": points,
        "curves": curves,
        "diagnostics": diagnostics,
        "summary": {
            "visible_marker_count": len(points),
            "main_marker_count": sum(point["segment"] == "main" for point in points),
            "vehicle_marker_count": sum(point["segment"] == "vehicle" for point in points),
            "visible_error_bar_count": sum(point["error_lower"] is not None for point in points),
            "traced_curve_count": len(curves),
        },
        "limitations": [
            "Only visible marker centres, error-bar endpoints, and curve paths are recovered.",
            "The vehicle points are visible geometry but are not assigned a log-concentration value.",
            "Curve paths are traced vector geometry, not author-supplied 4PL parameters.",
            "Raw replicate observations cannot be recovered from this rendered panel.",
        ],
    }

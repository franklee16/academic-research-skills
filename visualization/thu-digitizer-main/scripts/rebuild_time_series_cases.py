"""Rebuild time-series gallery evidence without downsampling visible traces.

The gallery keeps every colour-supported raster column for the two dense black
traces.  The four-colour panel instead has one visibly marked observation per
day; it retains those 41 marks.  This replaces the earlier presentation-only
annual samples and keeps missing values as gaps.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from PIL import Image

from build_nature_six_cases import _paper_line_recreation, write_csv, write_json


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "gallery" / "assets" / "cases"
TRACE_REPORT = ROOT / "tmp" / "requested-20260720" / "fig1d-trace-report.json"


def value_at(axis: dict, pixel: float) -> float:
    value = float(axis["pixel_slope"]) * float(pixel) + float(axis["transformed_intercept"])
    return 10**value if axis.get("scale") == "log10" else value


def write_case(case_id: str, rows: list[dict], report: dict) -> None:
    root = CASES / case_id
    original = Image.open(root / "original.png").convert("RGB")
    write_csv(root / "data.csv", rows)
    write_json(root / "report.json", report)
    _paper_line_recreation(root / "recreated.png", original, case_id, report)
    recreated = Image.open(root / "recreated.png").convert("RGB")
    Image.blend(original, recreated, 0.5).save(root / "overlay.png")


def rebuild_dense_black_trace(case_id: str) -> None:
    root = CASES / case_id
    report = json.loads((root / "report.json").read_text(encoding="utf-8"))
    calibration = report["calibration"]
    rows: list[dict] = []
    for point in calibration["trace"]["path"]:
        x_pixel = point["x_pixel"]
        y_pixel = point.get("y_pixel")
        observed = y_pixel is not None and point.get("status") == "observed"
        rows.append(
            {
                "series": "Mackey-Glass" if case_id.endswith("fig3a") else "CAN/USD",
                "x": round(value_at(calibration["axis_x"], x_pixel), 8),
                "value": round(value_at(calibration["axis_y"], y_pixel), 8) if observed else "",
                "pixel_x": x_pixel,
                "pixel_y": round(y_pixel, 4) if observed else "",
                "uncertainty_value": round(abs(float(point.get("uncertainty_px") or 0.5) * calibration["axis_y"]["pixel_slope"]), 8) if observed else "",
                "confidence": round(float(point.get("peak_score") or 0), 4) if observed else "",
                "value_status": "visible_trace_observed" if observed else "not_extracted_gap",
            }
        )
    report["rows"] = len(rows)
    report["observed_rows"] = sum(row["value_status"] == "visible_trace_observed" for row in rows)
    report["pixel_extraction"] = "continuity trace retained at each colour-supported raster column"
    report["limitations"] = [
        "Values are calibrated visible-curve geometry, not the authors' underlying monthly/latent observations.",
        "Colour-unsupported columns remain explicit gaps and are never interpolated.",
    ]
    write_case(case_id, rows, report)


def rebuild_similarity_trace() -> None:
    trace_report = json.loads(TRACE_REPORT.read_text(encoding="utf-8"))
    root = CASES / "nature-02571-fig1d"
    series_colours = {
        "Bacteria (phylum)": "#8ec3e8",
        "Eukarya (phylum)": "#ed6e6f",
        "Bacteria (OTU)": "#073bb7",
        "Eukarya (OTU)": "#d81919",
    }
    x_axis = trace_report["calibration"]["x"]
    y_axis = trace_report["calibration"]["y"]
    rows: list[dict] = []
    calibration: dict[str, dict] = {}
    for name, colour in series_colours.items():
        samples = trace_report["samples"][name]
        path = []
        for index, observation in enumerate(samples):
            x_pixel = 103 + index * (591 - 103) / 40
            y_pixel = observation.get("y_pixel")
            # All four displayed curves share the visibly drawn t=0 point at 1.0.
            if index == 0:
                y_pixel = 45.0
                value = 1.0
                status = "visible_marker_observed"
            else:
                value = observation.get("value")
                status = "visible_marker_observed" if y_pixel is not None else "not_extracted_gap"
            path.append(
                {
                    "x_pixel": x_pixel,
                    "y_pixel": y_pixel,
                    "status": "observed" if status == "visible_marker_observed" else "gap",
                    "support": 1.0,
                    "peak_score": observation.get("confidence") or 0.0,
                    "uncertainty_px": observation.get("uncertainty_px"),
                }
            )
            rows.append(
                {
                    "series": name,
                    "x": index,
                    "value": round(float(value), 8) if value is not None else "",
                    "pixel_x": round(x_pixel, 4),
                    "pixel_y": round(float(y_pixel), 4) if y_pixel is not None else "",
                    "uncertainty_value": round(float(observation.get("uncertainty_value") or 0), 8) if y_pixel is not None else "",
                    "confidence": round(float(observation.get("confidence") or 0), 4) if y_pixel is not None else "",
                    "value_status": status,
                    "visible_colour": colour,
                }
            )
        calibration[name] = {"axis_x": x_axis, "axis_y": y_axis, "trace": {"path": path}}
    report = {
        "schema_version": 1,
        "status": "visible_geometry_candidate",
        "route": "calibrated_raster_candidate",
        "panel_mapping": "Fig. 1d similarity versus time lag",
        "rows": len(rows),
        "observed_rows": sum(row["value_status"] == "visible_marker_observed" for row in rows),
        "pixel_extraction": "continuity-assisted colour trace, sampled at each visibly marked day",
        "source_data": "not directly provided for this panel",
        "calibration": calibration,
        "limitations": [
            "Each value is a calibrated visible curve/marker position, not an inferred replicate summary.",
            "Error-bar geometry remains separate and is not represented as a source SD or SEM claim.",
        ],
    }
    write_case("nature-02571-fig1d", rows, report)


def main() -> None:
    rebuild_dense_black_trace("nature-00142-fig3a")
    rebuild_dense_black_trace("nature-00142-fig4a")
    rebuild_similarity_trace()


if __name__ == "__main__":
    main()

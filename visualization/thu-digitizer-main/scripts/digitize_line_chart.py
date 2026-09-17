"""Extract calibrated, color-distinct line/scatter data from a chart raster.

This script is intentionally deterministic and local.  It does not perform OCR,
download models, or send image content anywhere.  OCR should be used separately
to propose tick labels, then confirmed as numeric calibration arguments here.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw

try:
    from raster_digitizer_core import AxisCalibration, sample_traced_path, trace_colour_path
except ImportError:  # pragma: no cover - supports importing as scripts.digitize_line_chart
    from .raster_digitizer_core import AxisCalibration, sample_traced_path, trace_colour_path


def parse_color(value: str) -> tuple[int, int, int]:
    text = value.strip().lstrip("#")
    if "," in text:
        parts = [part.strip() for part in text.split(",")]
        if len(parts) != 3:
            raise argparse.ArgumentTypeError("RGB colors need three comma-separated channels")
        try:
            color = tuple(int(part) for part in parts)
        except ValueError as exc:
            raise argparse.ArgumentTypeError("RGB channels must be integers") from exc
    else:
        if len(text) != 6:
            raise argparse.ArgumentTypeError("hex colors must be #RRGGBB")
        try:
            color = tuple(int(text[index : index + 2], 16) for index in range(0, 6, 2))
        except ValueError as exc:
            raise argparse.ArgumentTypeError("invalid hex color") from exc
    if any(channel < 0 or channel > 255 for channel in color):
        raise argparse.ArgumentTypeError("RGB channels must be in 0..255")
    return color  # type: ignore[return-value]


def parse_series(value: str) -> tuple[str, tuple[int, int, int]]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("series must use NAME=#RRGGBB")
    name, color = value.split("=", 1)
    name = name.strip()
    if not name or name in {"x", "x_pixel"}:
        raise argparse.ArgumentTypeError("choose a non-empty series name other than x or x_pixel")
    return name, parse_color(color)


def parse_values(value: str) -> list[float]:
    try:
        parsed = [float(part.strip()) for part in value.split(",") if part.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("sample values must be comma-separated numbers") from exc
    if not parsed:
        raise argparse.ArgumentTypeError("at least one sample value is required")
    if len(set(parsed)) != len(parsed):
        raise argparse.ArgumentTypeError("sample values must be unique")
    return parsed


def parse_anchor(value: str) -> tuple[float, float]:
    try:
        pixel, numeric_value = (float(part.strip()) for part in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("anchors must be pixel,value") from exc
    return pixel, numeric_value


def parse_bounds(value: str) -> tuple[int, int, int, int]:
    try:
        values = tuple(int(part.strip()) for part in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("plot bounds must be x0,y0,x1,y1 integers") from exc
    if len(values) != 4 or values[0] >= values[2] or values[1] >= values[3]:
        raise argparse.ArgumentTypeError("plot bounds must satisfy x0<x1 and y0<y1")
    return values  # type: ignore[return-value]


def affine(value: float, pixel_min: float, value_min: float, pixel_max: float, value_max: float) -> float:
    if pixel_min == pixel_max:
        raise ValueError("calibration pixels must differ")
    return value_min + (value - pixel_min) * (value_max - value_min) / (pixel_max - pixel_min)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def color_mask(pixels: np.ndarray, color: tuple[int, int, int], tolerance: float) -> np.ndarray:
    # Use int32: int16 overflows when a channel difference exceeds about 181,
    # which would incorrectly classify white backgrounds as colored data.
    target = np.asarray(color, dtype=np.int32)
    distance_squared = np.square(pixels.astype(np.int32) - target).sum(axis=2)
    return distance_squared <= tolerance * tolerance


def cluster_rows(mask: np.ndarray, x_center: float, bounds: tuple[int, int, int, int], radius: int) -> list[dict[str, float]]:
    x0, y0, x1, y1 = bounds
    center = int(round(x_center))
    left = max(x0, center - radius)
    right = min(x1, center + radius)
    if left > right:
        return []
    cropped = mask[y0 : y1 + 1, left : right + 1]
    rows, _ = np.where(cropped)
    if not len(rows):
        return []
    absolute_rows = np.sort(rows + y0)
    unique_rows = np.unique(absolute_rows)
    breaks = np.where(np.diff(unique_rows) > 3)[0] + 1
    groups = np.split(unique_rows, breaks)
    result: list[dict[str, float]] = []
    for group in groups:
        row_set = set(int(row) for row in group)
        all_rows = [int(row) for row in absolute_rows if int(row) in row_set]
        result.append({"center": float(np.median(all_rows)), "pixels": float(len(all_rows))})
    return result


def choose_cluster(clusters: list[dict[str, float]], previous: float | None) -> dict[str, float] | None:
    if not clusters:
        return None
    if previous is None:
        return max(clusters, key=lambda item: item["pixels"])
    return min(
        clusters,
        key=lambda item: abs(item["center"] - previous) - 0.5 * math.log1p(item["pixels"]),
    )


def extract_series(
    mask: np.ndarray,
    sample_pixels: list[float],
    bounds: tuple[int, int, int, int],
    radius: int,
) -> tuple[list[dict[str, Any]], float]:
    previous: float | None = None
    observations: list[dict[str, Any]] = []
    confidence_values: list[float] = []
    for x_pixel in sample_pixels:
        chosen = choose_cluster(cluster_rows(mask, x_pixel, bounds, radius), previous)
        if chosen is None:
            observations.append({"y_pixel": None, "candidate_pixels": 0, "confidence": 0.0})
            continue
        previous = chosen["center"]
        confidence = min(1.0, chosen["pixels"] / max(3.0, 2.0 * radius + 1.0))
        confidence_values.append(confidence)
        observations.append(
            {
                "y_pixel": round(chosen["center"], 3),
                "candidate_pixels": int(chosen["pixels"]),
                "confidence": round(confidence, 3),
            }
        )
    return observations, (sum(confidence_values) / len(sample_pixels) if sample_pixels else 0.0)


def extract_error_bars(
    mask: np.ndarray,
    sample_pixels: list[float],
    sample_values: list[float],
    bounds: tuple[int, int, int, int],
    radius: int,
    min_span: int,
    y_calibration: tuple[float, float, float, float],
) -> list[dict[str, Any]]:
    x0, y0, x1, y1 = bounds
    y_px_min, y_value_min, y_px_max, y_value_max = y_calibration
    results: list[dict[str, Any]] = []
    for x_value, x_pixel in zip(sample_values, sample_pixels):
        center = int(round(x_pixel))
        left = max(x0, center - radius)
        right = min(x1, center + radius)
        rows, _ = np.where(mask[y0 : y1 + 1, left : right + 1])
        if not len(rows):
            results.append({"x": x_value, "status": "not_extracted", "confidence": 0.0})
            continue
        absolute_rows = rows + y0
        top = int(absolute_rows.min())
        bottom = int(absolute_rows.max())
        span = bottom - top
        if span < min_span:
            results.append(
                {
                    "x": x_value,
                    "status": "not_extracted",
                    "confidence": 0.0,
                    "reason": f"vertical evidence span {span}px is below {min_span}px",
                }
            )
            continue
        coverage = len(np.unique(absolute_rows)) / (span + 1)
        confidence = min(1.0, 0.55 * coverage + 0.45 * min(1.0, span / (min_span * 3)))
        results.append(
            {
                "x": x_value,
                "status": "extracted",
                "top_y_pixel": top,
                "bottom_y_pixel": bottom,
                "upper": round(affine(top, y_px_min, y_value_min, y_px_max, y_value_max), 6),
                "lower": round(affine(bottom, y_px_min, y_value_min, y_px_max, y_value_max), 6),
                "span_pixels": span,
                "confidence": round(confidence, 3),
            }
        )
    return results


def create_overlay(
    image: Image.Image,
    sample_pixels: list[float],
    extracted: dict[str, list[dict[str, Any]]],
    output: Path,
) -> None:
    overlay = image.convert("RGB").copy()
    draw = ImageDraw.Draw(overlay)
    colors = [(255, 170, 0), (0, 170, 80), (160, 0, 200), (0, 170, 220)]
    for index, (name, observations) in enumerate(extracted.items()):
        color = colors[index % len(colors)]
        for x_pixel, observation in zip(sample_pixels, observations):
            y_pixel = observation["y_pixel"]
            if y_pixel is not None:
                x = int(round(x_pixel))
                y = int(round(y_pixel))
                draw.ellipse((x - 2, y - 2, x + 2, y + 2), outline=color, width=1)
    overlay.save(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--overlay", type=Path)
    parser.add_argument("--x-px-min", required=True, type=float)
    parser.add_argument("--x-value-min", required=True, type=float)
    parser.add_argument("--x-px-max", required=True, type=float)
    parser.add_argument("--x-value-max", required=True, type=float)
    parser.add_argument("--y-px-min", required=True, type=float)
    parser.add_argument("--y-value-min", required=True, type=float)
    parser.add_argument("--y-px-max", required=True, type=float)
    parser.add_argument("--y-value-max", required=True, type=float)
    parser.add_argument("--plot-bounds", required=True, type=parse_bounds)
    parser.add_argument("--sample-values", required=True, type=parse_values)
    parser.add_argument("--series", required=True, action="append", type=parse_series)
    parser.add_argument("--color-tolerance", type=float, default=24.0)
    parser.add_argument("--sample-radius", type=int, default=3)
    parser.add_argument("--error-color", type=parse_color)
    parser.add_argument("--error-tolerance", type=float, default=12.0)
    parser.add_argument("--error-min-span", type=int, default=8)
    parser.add_argument(
        "--trace-mode",
        choices=("sample", "continuity"),
        default="sample",
        help="sample local rows (legacy) or trace a colour-supported path across the plot",
    )
    parser.add_argument("--x-transform", choices=("linear", "log10", "displayed_log10"), default="linear")
    parser.add_argument("--y-transform", choices=("linear", "log10", "displayed_log10"), default="linear")
    parser.add_argument("--x-anchor", action="append", type=parse_anchor, help="additional x calibration anchor pixel,value")
    parser.add_argument("--y-anchor", action="append", type=parse_anchor, help="additional y calibration anchor pixel,value")
    parser.add_argument("--trace-sigma", type=float, default=42.0)
    parser.add_argument("--trace-threshold", type=float, default=0.22)
    parser.add_argument("--trace-max-step", type=float, default=14.0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.color_tolerance <= 0 or args.error_tolerance <= 0 or args.sample_radius < 0 or args.error_min_span < 1:
        raise SystemExit("tolerances must be positive, sample radius non-negative, and min span at least one")
    if len({name for name, _ in args.series}) != len(args.series):
        raise SystemExit("series names must be unique")
    image = Image.open(args.input).convert("RGB")
    pixels = np.asarray(image)
    width, height = image.size
    x0, y0, x1, y1 = args.plot_bounds
    if not (0 <= x0 < x1 < width and 0 <= y0 < y1 < height):
        raise SystemExit(f"plot bounds must fit image size {width}x{height}")
    x_anchors = [(args.x_px_min, args.x_value_min), (args.x_px_max, args.x_value_max)]
    y_anchors = [(args.y_px_min, args.y_value_min), (args.y_px_max, args.y_value_max)]
    x_anchors.extend(args.x_anchor or [])
    y_anchors.extend(args.y_anchor or [])
    x_axis = AxisCalibration.fit(x_anchors, scale=args.x_transform)
    y_axis = AxisCalibration.fit(y_anchors, scale=args.y_transform)
    sample_pixels = [x_axis.pixel_at_value(value) for value in args.sample_values]
    if any(pixel < x0 or pixel > x1 for pixel in sample_pixels):
        raise SystemExit("every sample value must map inside plot bounds")

    series_rows: dict[str, list[dict[str, Any]]] = {}
    series_reports: list[dict[str, Any]] = []
    trace_reports: dict[str, dict[str, Any]] = {}
    for name, color in args.series:
        if args.trace_mode == "continuity":
            trace = trace_colour_path(
                pixels,
                target=color,
                plot_bounds=args.plot_bounds,
                sigma=args.trace_sigma,
                tolerance=args.color_tolerance,
                score_threshold=args.trace_threshold,
                max_step=args.trace_max_step,
            )
            observations = []
            for item in sample_traced_path(
                trace,
                x_values=args.sample_values,
                x_axis=x_axis,
                y_axis=y_axis,
                sample_radius_px=args.sample_radius,
            ):
                observations.append(
                    {
                        "y_pixel": item["y_pixel"],
                        "value": item["y"],
                        "candidate_pixels": None,
                        "uncertainty_px": item.get("uncertainty_px"),
                        "uncertainty_value": item.get("uncertainty_value"),
                        "confidence": item["confidence"],
                        "status": item["status"],
                    }
                )
            overall_confidence = float(np.mean([item["confidence"] for item in observations])) if observations else 0.0
            trace_reports[name] = trace
        else:
            observations, overall_confidence = extract_series(
                color_mask(pixels, color, args.color_tolerance), sample_pixels, args.plot_bounds, args.sample_radius
            )
            for observation in observations:
                y_pixel = observation["y_pixel"]
                observation["value"] = (
                    None
                    if y_pixel is None
                    else round(
                        affine(y_pixel, args.y_px_min, args.y_value_min, args.y_px_max, args.y_value_max),
                        6,
                    )
                )
        series_rows[name] = observations
        series_reports.append(
            {
                "name": name,
                "color_rgb": color,
                "found_samples": sum(row["y_pixel"] is not None for row in observations),
                "total_samples": len(observations),
                "mean_confidence": round(overall_confidence, 3),
            }
        )

    error_bars: list[dict[str, Any]] = []
    if args.error_color is not None:
        error_bars = extract_error_bars(
            color_mask(pixels, args.error_color, args.error_tolerance),
            sample_pixels,
            args.sample_values,
            args.plot_bounds,
            args.sample_radius,
            args.error_min_span,
            (args.y_px_min, args.y_value_min, args.y_px_max, args.y_value_max),
        )

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["x", "x_pixel", *series_rows.keys()])
        writer.writeheader()
        for index, (x_value, x_pixel) in enumerate(zip(args.sample_values, sample_pixels)):
            row: dict[str, Any] = {"x": x_value, "x_pixel": round(x_pixel, 3)}
            row.update({name: observations[index]["value"] for name, observations in series_rows.items()})
            writer.writerow(row)

    report = {
        "schema_version": 1,
        "input_file": args.input.name,
        "input_sha256": file_sha256(args.input),
        "image_size": {"width": width, "height": height},
        "plot_bounds_px": {"left": x0, "top": y0, "right": x1, "bottom": y1},
        "calibration": {
            "x": x_axis.report(),
            "y": y_axis.report(),
            "assumption": "robust affine fit in transformed value space",
        },
        "series": series_reports,
        "trace_mode": args.trace_mode,
        "traces": trace_reports,
        "samples": {name: observations for name, observations in series_rows.items()},
        "error_bars": error_bars,
        "limitations": [
            "Series values require distinct colors and a verified linear calibration.",
            "A missing observation remains missing; the script does not interpolate.",
            "Extracted error-bar geometry is not a claim about SD, SEM, or confidence intervals.",
            "Continuity mode reports only colour-supported path columns; gap columns remain missing.",
        ],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.overlay is not None:
        args.overlay.parent.mkdir(parents=True, exist_ok=True)
        create_overlay(image, sample_pixels, series_rows, args.overlay)
    print(f"CSV={args.output_csv}")
    print(f"REPORT={args.report}")
    print(f"SERIES={len(series_rows)} SAMPLES={len(args.sample_values)}")


if __name__ == "__main__":
    main()

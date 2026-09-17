"""Deterministic benchmark for compact raster scatter-marker extraction."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw

try:
    from candidate_digitize_scatter import extract_scatter_points, write_overlay
except ImportError:  # pragma: no cover - package import
    from .candidate_digitize_scatter import extract_scatter_points, write_overlay


PRIVACY = "All fixtures are deterministic and locally generated synthetic data."


@dataclass(frozen=True)
class Fixture:
    name: str
    path: Path
    plot_bounds: tuple[int, int, int, int]
    x_anchors: tuple[tuple[float, float], ...]
    y_anchors: tuple[tuple[float, float], ...]
    truth_pixels: tuple[tuple[float, float], ...]
    marker_mode: str
    marker_color: str | None
    dark_threshold: int
    light_threshold: int
    min_radius: float
    max_radius: float
    expected_status: str
    center_error_limit_pixels: float


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _scale_point(point: tuple[float, float], scale: int) -> tuple[int, int]:
    return round(point[0] * scale), round(point[1] * scale)


def _render(
    path: Path,
    *,
    name: str,
    size: tuple[int, int],
    plot_bounds: tuple[int, int, int, int],
    points: tuple[tuple[float, float], ...],
    marker_color: str,
    background: str,
    axis_color: str,
    line_color: str,
    band_color: str,
    marker_radius: float,
    antialias_scale: int = 3,
    output_format: str = "PNG",
) -> None:
    scale = antialias_scale
    image = Image.new("RGB", (size[0] * scale, size[1] * scale), background)
    draw = ImageDraw.Draw(image)
    left, top, right, bottom = (value * scale for value in plot_bounds)
    draw.line((left, top, left, bottom), fill=axis_color, width=2 * scale)
    draw.line((left, bottom, right, bottom), fill=axis_color, width=2 * scale)
    draw.polygon(
        [
            (left + 5 * scale, top + 42 * scale),
            (right - 4 * scale, top + 67 * scale),
            (right - 4 * scale, top + 102 * scale),
            (left + 5 * scale, top + 73 * scale),
        ],
        fill=band_color,
    )
    draw.line(
        (left + 5 * scale, top + 56 * scale, right - 4 * scale, top + 84 * scale),
        fill=line_color,
        width=3 * scale,
    )
    # Annotation-like strokes and ticks share the foreground polarity but are thin.
    draw.line(
        (left + 12 * scale, top + 15 * scale, left + 58 * scale, top + 15 * scale),
        fill=axis_color,
        width=2 * scale,
    )
    draw.line(
        (left + 12 * scale, top + 15 * scale, left + 12 * scale, top + 22 * scale),
        fill=axis_color,
        width=2 * scale,
    )
    for tick_x in np.linspace(left + 30 * scale, right - 25 * scale, 4):
        draw.line((tick_x, bottom - 2 * scale, tick_x, bottom + 5 * scale), fill=axis_color, width=2 * scale)
    radius = marker_radius * scale
    for point in points:
        x, y = _scale_point(point, scale)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=marker_color)
    if scale > 1:
        image = image.resize(size, Image.Resampling.LANCZOS)
    if output_format == "JPEG":
        image.save(path, format="JPEG", quality=88, subsampling=0)
    else:
        image.save(path, format=output_format)


def _fixtures(output_dir: Path) -> list[Fixture]:
    size = (320, 220)
    bounds = (38, 24, 294, 188)
    points = (
        (66.0, 62.0),
        (98.0, 91.0),
        (109.0, 91.0),
        (145.0, 51.0),
        (187.0, 118.0),
        (237.0, 151.0),
        (273.0, 82.0),
    )
    common = {
        "size": size,
        "plot_bounds": bounds,
        "points": points,
        "marker_radius": 5.5,
    }
    _render(
        output_dir / "dark_band_touching.png",
        name="dark_band_touching",
        marker_color="#282829",
        background="#ffffff",
        axis_color="#252525",
        line_color="#0058a2",
        band_color="#dbe8f3",
        **common,
    )
    _render(
        output_dir / "color_touching.png",
        name="color_touching",
        marker_color="#d62728",
        background="#ffffff",
        axis_color="#222222",
        line_color="#d62728",
        band_color="#f4dfdf",
        **common,
    )
    _render(
        output_dir / "light_on_dark.png",
        name="light_on_dark",
        marker_color="#f2f2f2",
        background="#20242b",
        axis_color="#eeeeee",
        line_color="#48bfe3",
        band_color="#394653",
        **common,
    )

    low_size = (210, 150)
    low_bounds = (25, 17, 193, 129)
    scale_x = low_size[0] / size[0]
    scale_y = low_size[1] / size[1]
    low_points = tuple((x * scale_x, y * scale_y) for x, y in points)
    _render(
        output_dir / "dark_band_touching_lowres.jpg",
        name="dark_band_touching_lowres_jpeg",
        size=low_size,
        plot_bounds=low_bounds,
        points=low_points,
        marker_color="#282829",
        background="#ffffff",
        axis_color="#252525",
        line_color="#0058a2",
        band_color="#dbe8f3",
        marker_radius=3.6,
        output_format="JPEG",
    )
    _render(
        output_dir / "line_text_only.png",
        name="line_text_only_refusal",
        marker_color="#282829",
        background="#ffffff",
        axis_color="#252525",
        line_color="#0058a2",
        band_color="#dbe8f3",
        points=(),
        size=size,
        plot_bounds=bounds,
        marker_radius=5.5,
    )
    residual_point = (278.0, 45.0)
    residual_path = output_dir / "low_contrast_residual_refusal.png"
    _render(
        residual_path,
        name="low_contrast_residual_refusal",
        marker_color="#282829",
        background="#ffffff",
        axis_color="#252525",
        line_color="#0058a2",
        band_color="#dbe8f3",
        points=points,
        size=size,
        plot_bounds=bounds,
        marker_radius=5.5,
    )
    with Image.open(residual_path) as source:
        residual_image = source.convert("RGB")
    residual_draw = ImageDraw.Draw(residual_image)
    residual_draw.ellipse(
        (
            residual_point[0] - 5.5,
            residual_point[1] - 5.5,
            residual_point[0] + 5.5,
            residual_point[1] + 5.5,
        ),
        fill="#777777",
    )
    residual_image.save(residual_path)

    def axes_for(current_bounds: tuple[int, int, int, int]):
        left, top, right, bottom = current_bounds
        return (
            ((float(left), 0.0), (float(right), 10.0)),
            ((float(top), 10.0), (float(bottom), 0.0)),
        )

    x_axes, y_axes = axes_for(bounds)
    low_x_axes, low_y_axes = axes_for(low_bounds)
    return [
        Fixture("dark_band_touching", output_dir / "dark_band_touching.png", bounds, x_axes, y_axes, points, "dark", None, 120, 225, 2.8, 12.0, "candidate", 1.5),
        Fixture("color_touching", output_dir / "color_touching.png", bounds, x_axes, y_axes, points, "color", "#d62728", 120, 225, 2.8, 12.0, "candidate", 1.5),
        Fixture("light_on_dark", output_dir / "light_on_dark.png", bounds, x_axes, y_axes, points, "light", None, 120, 220, 2.8, 12.0, "candidate", 1.5),
        Fixture("dark_band_touching_lowres_jpeg", output_dir / "dark_band_touching_lowres.jpg", low_bounds, low_x_axes, low_y_axes, low_points, "dark", None, 145, 225, 2.4, 9.0, "candidate", 2.5),
        Fixture("line_text_only_refusal", output_dir / "line_text_only.png", bounds, x_axes, y_axes, (), "dark", None, 120, 225, 2.8, 12.0, "low_confidence", 1.5),
        Fixture("low_contrast_residual_refusal", residual_path, bounds, x_axes, y_axes, points + (residual_point,), "dark", None, 105, 225, 2.8, 12.0, "low_confidence_residual", 1.5),
    ]


def _match_points(
    expected: tuple[tuple[float, float], ...],
    observed: list[dict[str, Any]],
    *,
    tolerance: float,
) -> dict[str, Any]:
    pairs = sorted(
        (
            (math.hypot(float(point["pixel_x"]) - x, float(point["pixel_y"]) - y), expected_index, observed_index)
            for expected_index, (x, y) in enumerate(expected)
            for observed_index, point in enumerate(observed)
        ),
        key=lambda item: item[0],
    )
    used_expected: set[int] = set()
    used_observed: set[int] = set()
    matches = []
    for error, expected_index, observed_index in pairs:
        if error > tolerance or expected_index in used_expected or observed_index in used_observed:
            continue
        used_expected.add(expected_index)
        used_observed.add(observed_index)
        matches.append(
            {
                "expected_index": expected_index,
                "observed_index": observed_index,
                "center_error_pixels": error,
            }
        )
    true_positive = len(matches)
    precision = true_positive / len(observed) if observed else (1.0 if not expected else 0.0)
    recall = true_positive / len(expected) if expected else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    errors = [match["center_error_pixels"] for match in matches]
    return {
        "expected_count": len(expected),
        "observed_count": len(observed),
        "matched_count": true_positive,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "mean_center_error_pixels": float(np.mean(errors)) if errors else None,
        "max_center_error_pixels": float(np.max(errors)) if errors else None,
        "matches": matches,
    }


def _annotated_r(fixture: Fixture) -> float | None:
    if len(fixture.truth_pixels) < 3:
        return None
    left, top, right, bottom = fixture.plot_bounds
    x = np.asarray([(pixel_x - left) * 10.0 / (right - left) for pixel_x, _ in fixture.truth_pixels])
    y = np.asarray([10.0 - (pixel_y - top) * 10.0 / (bottom - top) for _, pixel_y in fixture.truth_pixels])
    return float(np.corrcoef(x, y)[0, 1])


def _measure(fixture: Fixture, output_dir: Path) -> dict[str, Any]:
    annotated = _annotated_r(fixture)
    extraction = extract_scatter_points(
        fixture.path,
        plot_bounds=fixture.plot_bounds,
        x_anchors=fixture.x_anchors,
        y_anchors=fixture.y_anchors,
        marker_mode=fixture.marker_mode,
        marker_color=fixture.marker_color,
        dark_threshold=fixture.dark_threshold,
        light_threshold=fixture.light_threshold,
        min_radius=fixture.min_radius,
        max_radius=fixture.max_radius,
        annotated_pearson_r=annotated,
        pearson_tolerance=0.03,
    )
    overlay_name = f"{fixture.name}_overlay.png"
    write_overlay(fixture.path, extraction, output_dir / overlay_name)
    metrics = _match_points(
        fixture.truth_pixels,
        extraction["points"],
        tolerance=fixture.center_error_limit_pixels,
    )
    return {
        "name": fixture.name,
        "image": fixture.path.name,
        "image_sha256": _sha256(fixture.path),
        "plot_bounds": list(fixture.plot_bounds),
        "x_anchors": [list(anchor) for anchor in fixture.x_anchors],
        "y_anchors": [list(anchor) for anchor in fixture.y_anchors],
        "marker_mode": fixture.marker_mode,
        "marker_color": fixture.marker_color,
        "expected_status": fixture.expected_status,
        "center_error_limit_pixels": fixture.center_error_limit_pixels,
        "truth_pixels": [list(point) for point in fixture.truth_pixels],
        "extraction": extraction,
        "metrics": metrics,
        "overlay": overlay_name,
    }


def _failure_reason(variant: dict[str, Any]) -> str | None:
    extraction = variant["extraction"]
    expected_status = variant["expected_status"]
    if expected_status == "low_confidence":
        if extraction["status"] != "low_confidence":
            return f"{variant['name']} did not refuse the unsupported panel"
        if extraction["numeric_output_authorized"] or extraction["points"]:
            return f"{variant['name']} emitted numeric point output while refusing"
        return None
    if expected_status == "low_confidence_residual":
        if extraction["status"] != "low_confidence":
            return f"{variant['name']} did not block the unresolved residual"
        if extraction["numeric_output_authorized"]:
            return f"{variant['name']} authorized points despite a marker-like residual"
        if extraction["residual_audit"]["residual_candidate_count"] != 1:
            return f"{variant['name']} did not expose exactly one residual candidate"
        return None
    if extraction["status"] != "candidate" or not extraction["numeric_output_authorized"]:
        return f"{variant['name']} did not authorize the supported candidate"
    metrics = variant["metrics"]
    if metrics["precision"] != 1.0 or metrics["recall"] != 1.0:
        return f"{variant['name']} point precision/recall is not 1.0"
    if metrics["max_center_error_pixels"] is None or metrics["max_center_error_pixels"] > variant["center_error_limit_pixels"]:
        return f"{variant['name']} center error exceeds its limit"
    return None


def _write_csv(path: Path, variants: list[dict[str, Any]]) -> None:
    fields = [
        "variant",
        "benchmark_status",
        "image_sha256",
        "expected_status",
        "extractor_status",
        "numeric_output_authorized",
        "expected_count",
        "observed_count",
        "precision",
        "recall",
        "f1",
        "max_center_error_pixels",
        "point_id",
        "x",
        "y",
        "pixel_x",
        "pixel_y",
        "confidence",
        "value_status",
        "overlay",
    ]
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for variant in variants:
            metrics = variant["metrics"]
            base = {
                "variant": variant["name"],
                "benchmark_status": variant["status"],
                "image_sha256": variant["image_sha256"],
                "expected_status": variant["expected_status"],
                "extractor_status": variant["extraction"]["status"],
                "numeric_output_authorized": variant["extraction"]["numeric_output_authorized"],
                "expected_count": metrics["expected_count"],
                "observed_count": metrics["observed_count"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1": metrics["f1"],
                "max_center_error_pixels": metrics["max_center_error_pixels"],
                "overlay": variant["overlay"],
            }
            points = variant["extraction"]["points"] or [{}]
            for point in points:
                writer.writerow({**base, **{key: point.get(key, "") for key in ("point_id", "x", "y", "pixel_x", "pixel_y", "confidence", "value_status")}})


def run_benchmark(output_dir: Path) -> dict[str, Any]:
    output_dir = Path(output_dir)
    if output_dir.exists() and not output_dir.is_dir():
        raise FileExistsError(f"output path exists and is not a directory: {output_dir}")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"refusing to overwrite non-empty evidence directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    variants = [_measure(fixture, output_dir) for fixture in _fixtures(output_dir)]
    failures = []
    for variant in variants:
        reason = _failure_reason(variant)
        if reason is None:
            variant["status"] = (
                "rejected_as_expected"
                if variant["expected_status"].startswith("low_confidence")
                else "passed"
            )
            variant["failure_reason"] = ""
        else:
            variant["status"] = "failed"
            variant["failure_reason"] = reason
            failures.append(reason)
    report = {
        "schema_version": 1,
        "family": "compact_scatter",
        "maturity": "candidate",
        "privacy": PRIVACY,
        "status": "failed" if failures else "passed",
        "failure_reason": "; ".join(failures),
        "variants": variants,
        "claim_limit": "Synthetic evidence only; real-vector, held-out real-raster, and fair WebPlotDigitizer gates remain open.",
    }
    (output_dir / "scatter_benchmark_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_csv(output_dir / "scatter_benchmark_results.csv", variants)
    if failures:
        raise AssertionError(report["failure_reason"])
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    report = run_benchmark(args.output_dir)
    print(json.dumps({"status": report["status"], "variants": len(report["variants"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()

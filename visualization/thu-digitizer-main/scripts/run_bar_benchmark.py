"""Deterministic benchmark for the candidate assisted bar-chart extractor."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from candidate_digitize_bar_chart import extract_bar_chart, write_overlay, write_recreation


SERIES_COLORS = {
    "red": "#d62728",
    "blue": "#1f77b4",
    "green": "#2ca02c",
}
ERROR_COLOR = "#595959"
PRIVACY_STATEMENT = "All fixtures are deterministic and locally generated synthetic data."
SCI_FIGURE_HUB_REFERENCES = [
    "https://uu543493-83c1-74a94416.nma1.seetacloud.com:8448/#/panel/geography/geography/grouped_bar/10-1038-s41467-026-69560-4__fig05_a",
    "https://uu543493-83c1-74a94416.nma1.seetacloud.com:8448/#/panel/environment/environment/stacked_bar/10-1038-s41467-026-70705-8__fig02_b",
]


@dataclass(frozen=True)
class Fixture:
    name: str
    path: Path
    raster_dimensions: tuple[int, int]
    plot_bounds: tuple[int, int, int, int]
    value_axis: tuple[float, float, float, float]
    orientation: str
    layout: str
    categories: list[tuple[str, float]]
    series_colors: dict[str, str]
    truth: list[dict[str, Any]]
    expected_stack_total: float | None = None
    error_color: str | None = None
    tolerance: float = 28.0
    error_tolerance: float = 24.0
    min_area: int = 30
    min_bar_thickness: int = 3
    min_fill_ratio: float = 0.55
    bridge_gap: int = 1
    baseline_tolerance_px: float = 3.0
    stack_gap_tolerance_px: float = 3.0
    expected_status: str = "candidate"


def _plot_bounds_from_bbox(bbox, image_height: int) -> tuple[int, int, int, int]:
    return (
        math.floor(bbox.x0),
        math.floor(image_height - bbox.y1),
        math.ceil(bbox.x1) - 1,
        math.ceil(image_height - bbox.y0) - 1,
    )


def _pixel_from_value(value: float, axis: tuple[float, float, float, float]) -> float:
    pixel_start, data_start, pixel_end, data_end = axis
    return float(
        pixel_start
        + (value - data_start) * (pixel_end - pixel_start) / (data_end - data_start)
    )


def _figure_and_axis(*, dark: bool):
    background = "#111111" if dark else "white"
    foreground = "#eeeeee" if dark else "black"
    grid = "#555555" if dark else "#d9d9d9"
    figure = plt.figure(figsize=(7.0, 4.8), dpi=100, facecolor=background)
    axis = figure.add_axes([0.13, 0.16, 0.64, 0.74], facecolor=background)
    axis.tick_params(colors=foreground, labelsize=8)
    for spine in axis.spines.values():
        spine.set_color(foreground)
    axis.grid(color=grid, linewidth=0.7)
    axis.set_axisbelow(True)
    return figure, axis, background, foreground


def _save_canvas(figure, path: Path) -> tuple[int, int]:
    figure.canvas.draw()
    width, height = figure.canvas.get_width_height()
    image = Image.frombuffer(
        "RGBA",
        (width, height),
        figure.canvas.buffer_rgba(),
        "raw",
        "RGBA",
        0,
        1,
    ).convert("RGB")
    image.save(path)
    return width, height


def _finish_fixture(
    *,
    name: str,
    path: Path,
    figure,
    axis,
    orientation: str,
    layout: str,
    category_values: np.ndarray,
    category_names: list[str],
    value_limits: tuple[float, float],
    series_colors: dict[str, str],
    truth_values: dict[str, list[float]],
    truth_errors: dict[str, list[float]] | None,
    expected_stack_total: float | None = None,
    error_color: str | None = None,
) -> Fixture:
    figure.canvas.draw()
    width, height = figure.canvas.get_width_height()
    bbox = axis.get_window_extent()
    plot_bounds = _plot_bounds_from_bbox(bbox, height)
    if orientation == "vertical":
        value_axis = (
            float(height - bbox.y1),
            value_limits[1],
            float(height - bbox.y0),
            value_limits[0],
        )
        categories = [
            (name_, float(axis.transData.transform((value, 0))[0]))
            for name_, value in zip(category_names, category_values)
        ]
    else:
        value_axis = (
            float(bbox.x0),
            value_limits[0],
            float(bbox.x1),
            value_limits[1],
        )
        categories = [
            (name_, float(height - axis.transData.transform((0, value))[1]))
            for name_, value in zip(category_names, category_values)
        ]

    truth = []
    for category_index, category_name in enumerate(category_names):
        for series_name in series_colors:
            value = float(truth_values[series_name][category_index])
            record: dict[str, Any] = {
                "category": category_name,
                "series": series_name,
                "value": value,
            }
            if truth_errors is not None:
                error = float(truth_errors[series_name][category_index])
                record.update(
                    error_lower_value=value - error,
                    error_upper_value=value + error,
                    error_lower_pixel=_pixel_from_value(value - error, value_axis),
                    error_upper_pixel=_pixel_from_value(value + error, value_axis),
                )
            truth.append(record)
    raster_dimensions = _save_canvas(figure, path)
    plt.close(figure)
    return Fixture(
        name=name,
        path=path,
        raster_dimensions=raster_dimensions,
        plot_bounds=plot_bounds,
        value_axis=value_axis,
        orientation=orientation,
        layout=layout,
        categories=categories,
        series_colors=series_colors,
        truth=truth,
        expected_stack_total=expected_stack_total,
        error_color=error_color,
    )


def _render_grouped(path: Path, *, orientation: str) -> Fixture:
    figure, axis, background, foreground = _figure_and_axis(dark=False)
    category_values = np.arange(4, dtype=float)
    category_names = list("ABCD")
    values = {
        "red": [-3.0, 4.0, 7.0, 2.0],
        "blue": [5.0, -2.0, 3.0, 6.0],
    }
    errors = {
        "red": [0.7, 0.9, 0.8, 0.6],
        "blue": [0.6, 0.7, 0.5, 0.8],
    }
    offsets = {"red": -0.18, "blue": 0.18}
    width = 0.32
    value_limits = (-5.0, 10.0)
    for series_name in values:
        if orientation == "vertical":
            axis.bar(
                category_values + offsets[series_name],
                values[series_name],
                width=width,
                color=SERIES_COLORS[series_name],
                edgecolor=SERIES_COLORS[series_name],
                linewidth=0,
                yerr=errors[series_name],
                error_kw={"ecolor": ERROR_COLOR, "elinewidth": 1.5, "capsize": 3},
                label=series_name,
            )
        else:
            axis.barh(
                category_values + offsets[series_name],
                values[series_name],
                height=width,
                color=SERIES_COLORS[series_name],
                edgecolor=SERIES_COLORS[series_name],
                linewidth=0,
                xerr=errors[series_name],
                error_kw={"ecolor": ERROR_COLOR, "elinewidth": 1.5, "capsize": 3},
                label=series_name,
            )
    if orientation == "vertical":
        axis.set_xlim(-0.65, 3.65)
        axis.set_ylim(*value_limits)
        axis.set_xticks(category_values, category_names)
        axis.set_ylabel("Response", color=foreground)
    else:
        axis.set_ylim(-0.65, 3.65)
        axis.set_xlim(*value_limits)
        axis.set_yticks(category_values, category_names)
        axis.set_xlabel("Response", color=foreground)
    legend = axis.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8)
    legend.get_frame().set_facecolor(background)
    for text in legend.get_texts():
        text.set_color(foreground)
    return _finish_fixture(
        name=f"grouped_{orientation}_clean",
        path=path,
        figure=figure,
        axis=axis,
        orientation=orientation,
        layout="grouped",
        category_values=category_values,
        category_names=category_names,
        value_limits=value_limits,
        series_colors={name: SERIES_COLORS[name] for name in values},
        truth_values=values,
        truth_errors=errors,
        error_color=ERROR_COLOR,
    )


def _render_stacked(path: Path, *, orientation: str, percent: bool, dark: bool) -> Fixture:
    figure, axis, background, foreground = _figure_and_axis(dark=dark)
    category_values = np.arange(4, dtype=float)
    category_names = list("ABCD")
    values = (
        {
            "red": [20.0, 35.0, 15.0, 30.0],
            "blue": [30.0, 20.0, 45.0, 25.0],
            "green": [50.0, 45.0, 40.0, 45.0],
        }
        if percent
        else {
            "red": [18.0, 22.0, 14.0, 25.0],
            "blue": [27.0, 19.0, 31.0, 18.0],
            "green": [16.0, 23.0, 20.0, 28.0],
        }
    )
    value_limits = (0.0, 100.0 if percent else 80.0)
    cumulative = np.zeros(len(category_values), dtype=float)
    for series_name, series_values in values.items():
        if orientation == "vertical":
            axis.bar(
                category_values,
                series_values,
                width=0.58,
                bottom=cumulative,
                color=SERIES_COLORS[series_name],
                edgecolor=background,
                linewidth=0.7,
                label=series_name,
            )
        else:
            axis.barh(
                category_values,
                series_values,
                height=0.58,
                left=cumulative,
                color=SERIES_COLORS[series_name],
                edgecolor=background,
                linewidth=0.7,
                label=series_name,
            )
        cumulative += np.asarray(series_values)
    if orientation == "vertical":
        axis.set_xlim(-0.65, 3.65)
        axis.set_ylim(*value_limits)
        axis.set_xticks(category_values, category_names)
        axis.set_ylabel("Value", color=foreground)
    else:
        axis.set_ylim(-0.65, 3.65)
        axis.set_xlim(*value_limits)
        axis.set_yticks(category_values, category_names)
        axis.set_xlabel("Percent" if percent else "Value", color=foreground)
    legend = axis.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8)
    legend.get_frame().set_facecolor(background)
    for text in legend.get_texts():
        text.set_color(foreground)
    return _finish_fixture(
        name=("percent_stacked" if percent else "stacked") + f"_{orientation}_{'dark' if dark else 'clean'}",
        path=path,
        figure=figure,
        axis=axis,
        orientation=orientation,
        layout="percent_stacked" if percent else "stacked",
        category_values=category_values,
        category_names=category_names,
        value_limits=value_limits,
        series_colors={name: SERIES_COLORS[name] for name in values},
        truth_values=values,
        truth_errors=None,
        expected_stack_total=100.0 if percent else None,
    )


def _scaled_bounds(
    bounds: tuple[int, int, int, int], scale_x: float, scale_y: float
) -> tuple[int, int, int, int]:
    left, top, right, bottom = bounds
    return (
        math.floor(left * scale_x),
        math.floor(top * scale_y),
        math.ceil((right + 1) * scale_x) - 1,
        math.ceil((bottom + 1) * scale_y) - 1,
    )


def _resize_fixture(source: Fixture, output_path: Path) -> Fixture:
    with Image.open(source.path) as image:
        original = image.convert("RGB")
        resized = original.resize((385, 264), Image.Resampling.LANCZOS)
        resized.save(output_path, format="JPEG", quality=84)
        scale_x = resized.width / original.width
        scale_y = resized.height / original.height
    value_scale = scale_y if source.orientation == "vertical" else scale_x
    category_scale = scale_x if source.orientation == "vertical" else scale_y
    value_axis = (
        source.value_axis[0] * value_scale,
        source.value_axis[1],
        source.value_axis[2] * value_scale,
        source.value_axis[3],
    )
    truth = []
    for record in source.truth:
        scaled = dict(record)
        if "error_lower_pixel" in scaled:
            scaled["error_lower_pixel"] *= value_scale
            scaled["error_upper_pixel"] *= value_scale
        truth.append(scaled)
    return replace(
        source,
        name=source.name.replace("_clean", "_lowres_jpeg"),
        path=output_path,
        raster_dimensions=(resized.width, resized.height),
        plot_bounds=_scaled_bounds(source.plot_bounds, scale_x, scale_y),
        value_axis=value_axis,
        categories=[
            (name, pixel * category_scale) for name, pixel in source.categories
        ],
        truth=truth,
        tolerance=82.0,
        error_tolerance=90.0,
        min_area=12,
        min_bar_thickness=2,
        min_fill_ratio=0.30,
        bridge_gap=2,
        baseline_tolerance_px=4.0,
        stack_gap_tolerance_px=4.0,
        expected_status="partial_visible",
    )


def _ambiguous_fixture(path: Path) -> Fixture:
    image = np.full((140, 200, 3), 255, dtype=np.uint8)
    image[45:105, 75:90] = (214, 39, 40)
    image[35:105, 110:125] = (214, 39, 40)
    Image.fromarray(image, mode="RGB").save(path)
    return Fixture(
        name="grouped_ambiguous_duplicate",
        path=path,
        raster_dimensions=(200, 140),
        plot_bounds=(20, 15, 180, 105),
        value_axis=(15.0, 9.0, 105.0, 0.0),
        orientation="vertical",
        layout="grouped",
        categories=[("A", 100.0)],
        series_colors={"red": SERIES_COLORS["red"]},
        truth=[{"category": "A", "series": "red", "value": None}],
        tolerance=1.0,
        min_area=20,
        expected_status="low_confidence",
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _measure_fixture(fixture: Fixture, output_dir: Path) -> dict[str, Any]:
    report = extract_bar_chart(
        fixture.path,
        plot_bounds=fixture.plot_bounds,
        value_axis=fixture.value_axis,
        orientation=fixture.orientation,
        layout=fixture.layout,
        series_colors=fixture.series_colors,
        categories=fixture.categories,
        tolerance=fixture.tolerance,
        min_area=fixture.min_area,
        min_bar_thickness=fixture.min_bar_thickness,
        min_fill_ratio=fixture.min_fill_ratio,
        bridge_gap=fixture.bridge_gap,
        baseline_tolerance_px=fixture.baseline_tolerance_px,
        stack_gap_tolerance_px=fixture.stack_gap_tolerance_px,
        expected_stack_total=fixture.expected_stack_total,
        error_color=fixture.error_color,
        error_tolerance=fixture.error_tolerance,
        error_search_radius=2,
        error_min_span=4,
    )
    overlay_name = f"{fixture.name}_overlay.png"
    write_overlay(fixture.path, report, output_dir / overlay_name)
    recreation_name = f"{fixture.name}_recreation.png"
    write_recreation(
        report,
        output_dir / recreation_name,
        title=f"{fixture.name}: recreation from extracted geometry",
    )
    truth_by_key = {
        (record["category"], record["series"]): record for record in fixture.truth
    }
    predicted = [mark for mark in report["marks"] if mark["status"] == "extracted"]
    matched = []
    value_errors = []
    error_endpoint_errors = []
    expected_error_bar_count = sum("error_lower_pixel" in record for record in fixture.truth)
    extracted_error_bar_count = 0
    for mark in predicted:
        key = (mark["category"], mark["series"])
        truth = truth_by_key.get(key)
        if truth is None or truth["value"] is None:
            continue
        matched.append(key)
        value_errors.append(abs(mark["value"] - truth["value"]))
        if "error_lower_pixel" in truth and mark.get("error_bar", {}).get("status") == "extracted":
            extracted_error_bar_count += 1
            error_endpoint_errors.extend(
                [
                    abs(mark["error_bar"]["lower_pixel"] - truth["error_lower_pixel"]),
                    abs(mark["error_bar"]["upper_pixel"] - truth["error_upper_pixel"]),
                ]
            )
    expected_numeric = [record for record in fixture.truth if record["value"] is not None]
    matched_count = len(set(matched))
    extracted_count = len(predicted)
    expected_count = len(expected_numeric)
    precision = matched_count / extracted_count if extracted_count else 0.0
    coverage = matched_count / expected_count if expected_count else 0.0
    f1 = 2 * precision * coverage / (precision + coverage) if precision + coverage else 0.0
    metrics = {
        "expected_mark_count": expected_count,
        "extracted_mark_count": extracted_count,
        "matched_mark_count": matched_count,
        "unmatched_prediction_count": extracted_count - matched_count,
        "missing_truth_count": expected_count - matched_count,
        "precision": precision,
        "coverage": coverage,
        "f1": f1,
        "mae": float(np.mean(value_errors)) if value_errors else None,
        "p95_abs_error": float(np.percentile(value_errors, 95)) if value_errors else None,
        "max_abs_error": float(np.max(value_errors)) if value_errors else None,
        "error_endpoint_p95_px": float(np.percentile(error_endpoint_errors, 95)) if error_endpoint_errors else None,
        "error_endpoint_max_px": float(np.max(error_endpoint_errors)) if error_endpoint_errors else None,
        "expected_error_bar_count": expected_error_bar_count,
        "extracted_error_bar_count": extracted_error_bar_count,
        "error_bar_coverage": extracted_error_bar_count / expected_error_bar_count if expected_error_bar_count else None,
    }
    return {
        "name": fixture.name,
        "expected_status": fixture.expected_status,
        "status": report["status"],
        "raster_dimensions": list(fixture.raster_dimensions),
        "plot_bounds": list(fixture.plot_bounds),
        "value_axis": list(fixture.value_axis),
        "orientation": fixture.orientation,
        "layout": fixture.layout,
        "categories": [
            {"name": name, "center_pixel": pixel} for name, pixel in fixture.categories
        ],
        "series_colors": fixture.series_colors,
        "expected_stack_total": fixture.expected_stack_total,
        "error_color": fixture.error_color,
        "truth": fixture.truth,
        "extraction": report,
        "metrics": metrics,
        "overlay": overlay_name,
        "recreation": recreation_name,
        "image_hash_sha256": _sha256(fixture.path),
    }


def _failure_reason(variant: dict[str, Any]) -> str | None:
    if variant["status"] != variant["expected_status"]:
        return f"{variant['name']} status {variant['status']} != {variant['expected_status']}"
    if variant["expected_status"] == "low_confidence":
        if any(mark.get("value") is not None for mark in variant["extraction"]["marks"]):
            return f"{variant['name']} emitted a value for an ambiguous category"
        return None
    metrics = variant["metrics"]
    if metrics["coverage"] < 1.0 or metrics["precision"] < 1.0 or metrics["f1"] < 1.0:
        return f"{variant['name']} mark precision/coverage/F1 is not 1.0"
    if metrics["mae"] is None or metrics["mae"] > 0.25:
        return f"{variant['name']} MAE exceeds 0.25"
    if metrics["max_abs_error"] is None or metrics["max_abs_error"] > 0.6:
        return f"{variant['name']} max error exceeds 0.6"
    if variant["error_color"] is not None:
        minimum_error_coverage = 0.75 if variant["expected_status"] == "partial_visible" else 1.0
        if metrics["error_bar_coverage"] is None or metrics["error_bar_coverage"] < minimum_error_coverage:
            return f"{variant['name']} error-bar coverage is below {minimum_error_coverage:.2f}"
        maximum_endpoint_error = 3.0 if variant["expected_status"] == "partial_visible" else 2.5
        if metrics["error_endpoint_max_px"] is None or metrics["error_endpoint_max_px"] > maximum_endpoint_error:
            return f"{variant['name']} error endpoint error exceeds {maximum_endpoint_error:.1f}px"
    if variant["layout"] == "percent_stacked":
        constraints = [
            diagnostic
            for diagnostic in variant["extraction"]["stack_diagnostics"]
            if diagnostic["kind"] == "stack_total"
        ]
        if not constraints or not all(item["within_tolerance"] for item in constraints):
            return f"{variant['name']} violates the 100% stack constraint"
    return None


def _write_csv(path: Path, variants: list[dict[str, Any]]) -> None:
    fields = [
        "fixture",
        "fixture_status",
        "failure_reason",
        "orientation",
        "layout",
        "image_hash_sha256",
        "plot_bounds",
        "value_axis",
        "category",
        "series",
        "mark_status",
        "truth_value",
        "extracted_value",
        "absolute_error",
        "error_lower_truth_pixel",
        "error_lower_extracted_pixel",
        "error_upper_truth_pixel",
        "error_upper_extracted_pixel",
        "overlay",
        "recreation",
    ]
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for variant in variants:
            truth_by_key = {
                (item["category"], item["series"]): item for item in variant["truth"]
            }
            for mark in variant["extraction"]["marks"]:
                truth = truth_by_key.get((mark["category"], mark["series"]), {})
                error_bar = mark.get("error_bar", {})
                truth_value = truth.get("value")
                extracted_value = mark.get("value")
                writer.writerow(
                    {
                        "fixture": variant["name"],
                        "fixture_status": variant["benchmark_status"],
                        "failure_reason": variant["failure_reason"],
                        "orientation": variant["orientation"],
                        "layout": variant["layout"],
                        "image_hash_sha256": variant["image_hash_sha256"],
                        "plot_bounds": json.dumps(variant["plot_bounds"]),
                        "value_axis": json.dumps(variant["value_axis"]),
                        "category": mark["category"],
                        "series": mark["series"],
                        "mark_status": mark["status"],
                        "truth_value": "" if truth_value is None else truth_value,
                        "extracted_value": "" if extracted_value is None else extracted_value,
                        "absolute_error": "" if truth_value is None or extracted_value is None else abs(extracted_value - truth_value),
                        "error_lower_truth_pixel": truth.get("error_lower_pixel", ""),
                        "error_lower_extracted_pixel": error_bar.get("lower_pixel", ""),
                        "error_upper_truth_pixel": truth.get("error_upper_pixel", ""),
                        "error_upper_extracted_pixel": error_bar.get("upper_pixel", ""),
                        "overlay": variant["overlay"],
                        "recreation": variant["recreation"],
                    }
                )


def _ensure_empty_output_dir(output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"refusing to overwrite non-empty evidence directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)


def run_benchmark(output_dir: Path) -> dict[str, Any]:
    output_dir = Path(output_dir)
    _ensure_empty_output_dir(output_dir)
    grouped_vertical = _render_grouped(output_dir / "grouped_vertical_clean.png", orientation="vertical")
    fixtures = [
        grouped_vertical,
        _resize_fixture(grouped_vertical, output_dir / "grouped_vertical_lowres.jpg"),
        _render_grouped(output_dir / "grouped_horizontal_clean.png", orientation="horizontal"),
        _render_stacked(output_dir / "stacked_vertical_clean.png", orientation="vertical", percent=False, dark=False),
        _render_stacked(output_dir / "percent_stacked_horizontal_dark.png", orientation="horizontal", percent=True, dark=True),
        _ambiguous_fixture(output_dir / "grouped_ambiguous_duplicate.png"),
    ]
    variants = [_measure_fixture(fixture, output_dir) for fixture in fixtures]
    failure_reasons = []
    for variant in variants:
        failure_reason = _failure_reason(variant)
        variant["benchmark_status"] = "failed" if failure_reason else (
            "rejected_as_expected" if variant["expected_status"] == "low_confidence" else "passed"
        )
        variant["failure_reason"] = failure_reason or ""
        if failure_reason:
            failure_reasons.append(failure_reason)
    report = {
        "schema_version": 1,
        "family": "bar_chart_candidate",
        "candidate_module": "candidate_digitize_bar_chart.py",
        "privacy": PRIVACY_STATEMENT,
        "gallery_role": "taxonomy_and_visual-stressor_reference_only; not numeric ground truth",
        "gallery_references": SCI_FIGURE_HUB_REFERENCES,
        "comparison": {
            "current_stable": "not_available_for_dedicated_bar_extraction",
            "webplotdigitizer": "not_compared; assisted comparison still required before promotion",
        },
        "status": "failed" if failure_reasons else "passed",
        "failure_reason": "; ".join(failure_reasons),
        "variants": variants,
    }
    (output_dir / "bar_benchmark_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    _write_csv(output_dir / "bar_benchmark_results.csv", variants)
    if failure_reasons:
        raise AssertionError(report["failure_reason"])
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    report = run_benchmark(args.output_dir)
    for variant in report["variants"]:
        metrics = variant["metrics"]
        print(
            f"{variant['name']}: {variant['benchmark_status']} "
            f"coverage={metrics['coverage']:.3f} "
            f"mae={metrics['mae'] if metrics['mae'] is not None else 'n/a'}"
        )


if __name__ == "__main__":
    main()

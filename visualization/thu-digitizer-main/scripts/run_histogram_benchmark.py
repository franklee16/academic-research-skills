"""Deterministic local benchmark for histogram extraction."""

import argparse
import csv
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

from digitize_histogram import extract_histogram


TRUTH = [3.0, 8.0, 5.0, 11.0, 6.0]
EXPECTED_BIN_CENTERS = [float(value) for value in np.arange(5)]
BAR_COLOR = "#1f77b4"
X_LIMITS = (-0.8, 4.8)
Y_LIMITS = (0.0, 12.0)
PRIVACY_STATEMENT = "All fixtures are deterministic and locally generated synthetic data."
MAX_CENTER_ERROR = 0.5


@dataclass(frozen=True)
class RenderedFixture:
    path: Path
    raster_dimensions: tuple[int, int]
    plot_bounds: tuple[int, int, int, int]
    x_axis: tuple[float, float, float, float]
    y_axis: tuple[float, float, float, float]


def _plot_bounds_from_bbox(bbox, image_height: int) -> tuple[int, int, int, int]:
    """Convert Matplotlib's display-space axes rectangle to raster bounds."""
    return (
        math.floor(bbox.x0),
        math.floor(image_height - bbox.y1),
        math.ceil(bbox.x1) - 1,
        math.ceil(image_height - bbox.y0) - 1,
    )


def _render_fixture(path: Path, *, dark: bool) -> RenderedFixture:
    figure_background = "#111111" if dark else "white"
    axes_background = "#181818" if dark else "white"
    foreground = "#eeeeee" if dark else "black"
    grid_color = "#d0d0d0" if dark else "#d9d9d9"

    figure, axis = plt.subplots(figsize=(6.4, 4.5), dpi=100)
    figure.patch.set_facecolor(figure_background)
    axis.set_facecolor(axes_background)
    figure.subplots_adjust(left=0.13, right=0.75, bottom=0.15, top=0.90)

    axis.bar(
        np.arange(5),
        TRUTH,
        width=0.82,
        color=BAR_COLOR,
        edgecolor=BAR_COLOR,
        linewidth=0,
        antialiased=False,
        label="Synthetic counts",
    )
    axis.set_xlim(*X_LIMITS)
    axis.set_ylim(*Y_LIMITS)
    axis.set_xticks(np.arange(5))
    axis.set_yticks(np.arange(0, 13, 2))
    axis.set_axisbelow(True)
    axis.grid(axis="y", color=grid_color, linewidth=0.8)
    axis.tick_params(colors=foreground)
    for spine in axis.spines.values():
        spine.set_color(foreground)

    legend = axis.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    legend.get_frame().set_facecolor(figure_background)
    legend.get_frame().set_edgecolor(foreground)
    for text in legend.get_texts():
        text.set_color(foreground)

    figure.canvas.draw()
    image_width, image_height = figure.canvas.get_width_height()
    axes_bbox = axis.get_window_extent()
    image = Image.frombuffer(
        "RGBA",
        (image_width, image_height),
        figure.canvas.buffer_rgba(),
        "raw",
        "RGBA",
        0,
        1,
    ).convert("RGB")
    image.save(path)
    plt.close(figure)

    return RenderedFixture(
        path=path,
        raster_dimensions=(image_width, image_height),
        plot_bounds=_plot_bounds_from_bbox(axes_bbox, image_height),
        x_axis=(float(axes_bbox.x0), X_LIMITS[0], float(axes_bbox.x1), X_LIMITS[1]),
        y_axis=(
            float(image_height - axes_bbox.y1),
            Y_LIMITS[1],
            float(image_height - axes_bbox.y0),
            Y_LIMITS[0],
        ),
    )


def _scale_bounds(
    bounds: tuple[int, int, int, int], scale_x: float, scale_y: float
) -> tuple[int, int, int, int]:
    left, top, right, bottom = bounds
    return (
        math.floor(left * scale_x),
        math.floor(top * scale_y),
        math.ceil((right + 1) * scale_x) - 1,
        math.ceil((bottom + 1) * scale_y) - 1,
    )


def _resize_fixture(clean: RenderedFixture, output_path: Path) -> RenderedFixture:
    with Image.open(clean.path) as clean_image:
        source = clean_image.convert("RGB")
        resized = source.resize((376, 263), Image.Resampling.LANCZOS)
        resized.save(output_path, format="JPEG", quality=86)
        scale_x = resized.width / source.width
        scale_y = resized.height / source.height

    def scale_axis(
        axis: tuple[float, float, float, float], scale: float
    ) -> tuple[float, float, float, float]:
        pixel_start, data_start, pixel_end, data_end = axis
        return (
            pixel_start * scale,
            data_start,
            pixel_end * scale,
            data_end,
        )

    return RenderedFixture(
        path=output_path,
        raster_dimensions=(resized.width, resized.height),
        plot_bounds=_scale_bounds(clean.plot_bounds, scale_x, scale_y),
        x_axis=scale_axis(clean.x_axis, scale_x),
        y_axis=scale_axis(clean.y_axis, scale_y),
    )


def _write_overlay(image_path: Path, bins: list[dict[str, float]], output_path: Path) -> None:
    with Image.open(image_path) as source:
        overlay = source.convert("RGB")
    draw = ImageDraw.Draw(overlay)
    for bin_ in bins:
        left = int(bin_["left_pixel"])
        top = int(bin_["top_pixel"])
        right = int(bin_["right_pixel"])
        bottom = int(bin_["bottom_pixel"])
        draw.rectangle((left, top, right - 1, bottom - 1), outline="red", width=2)
    overlay.save(output_path)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bin_center(bin_: dict[str, float]) -> float:
    return (bin_["x_left"] + bin_["x_right"]) / 2


def _align_bins_by_center(bins: list[dict[str, float]]) -> dict:
    """Match extracted bins to the known fixture positions by calibrated x centre."""
    sorted_bins = sorted(bins, key=_bin_center)
    available_indices = set(range(len(sorted_bins)))
    matched_pairs = []

    for expected_index, expected_center in enumerate(EXPECTED_BIN_CENTERS):
        candidates = [
            (abs(_bin_center(sorted_bins[index]) - expected_center), index)
            for index in available_indices
        ]
        if not candidates:
            continue
        distance, extracted_index = min(candidates)
        if distance <= MAX_CENTER_ERROR:
            available_indices.remove(extracted_index)
            matched_pairs.append((expected_index, sorted_bins[extracted_index]))

    matched_count = len(matched_pairs)
    extracted_count = len(sorted_bins)
    return {
        "expected_bin_count": len(EXPECTED_BIN_CENTERS),
        "extracted_bin_count": extracted_count,
        "matched_bin_count": matched_count,
        "unmatched_prediction_count": len(available_indices),
        "missing_truth_count": len(EXPECTED_BIN_CENTERS) - matched_count,
        "coverage": matched_count / len(EXPECTED_BIN_CENTERS),
        "precision": matched_count / extracted_count if extracted_count else 0.0,
        "matched_pairs": matched_pairs,
    }


def _measure_variant(fixture: RenderedFixture, output_dir: Path) -> dict:
    tolerance = 80.0 if fixture.path.suffix.lower() == ".jpg" else 16.0
    min_area = 50
    bins = extract_histogram(
        image_path=fixture.path,
        plot_bounds=fixture.plot_bounds,
        x_axis=fixture.x_axis,
        y_axis=fixture.y_axis,
        bar_color=BAR_COLOR,
        tolerance=tolerance,
        min_area=min_area,
    )
    alignment = _align_bins_by_center(bins)
    errors = np.abs(
        np.asarray(
            [bin_["height"] - TRUTH[expected_index] for expected_index, bin_ in alignment["matched_pairs"]],
            dtype=float,
        )
    )
    if alignment["matched_bin_count"]:
        mae = float(np.mean(errors))
        p95_abs_error = float(np.percentile(errors, 95))
        max_abs_error = float(np.max(errors))
    else:
        mae = None
        p95_abs_error = None
        max_abs_error = None

    overlay_name = f"{fixture.path.stem}_overlay.png"
    _write_overlay(fixture.path, bins, output_dir / overlay_name)
    return {
        "name": fixture.path.name,
        "raster_dimensions": list(fixture.raster_dimensions),
        "plot_bounds": list(fixture.plot_bounds),
        "x_axis": list(fixture.x_axis),
        "y_axis": list(fixture.y_axis),
        "bar_color": BAR_COLOR,
        "tolerance": tolerance,
        "min_area": min_area,
        "bins": bins,
        **{
            key: value
            for key, value in alignment.items()
            if key != "matched_pairs"
        },
        "mae": mae,
        "p95_abs_error": p95_abs_error,
        "max_abs_error": max_abs_error,
        "overlay": overlay_name,
        "image_hash_sha256": _sha256(fixture.path),
    }


def _quality_failure_reason(variant: dict) -> str | None:
    if variant["coverage"] < 1.0:
        return f"{variant['name']} coverage {variant['coverage']:.3f} is below 1.0"
    if variant["mae"] is None or variant["mae"] > 0.25:
        value = "unavailable" if variant["mae"] is None else f"{variant['mae']:.3f}"
        return f"{variant['name']} MAE {value} exceeds 0.25"
    if variant["unmatched_prediction_count"]:
        return (
            f"{variant['name']} has {variant['unmatched_prediction_count']} "
            "unmatched prediction(s)"
        )
    if variant["missing_truth_count"]:
        return (
            f"{variant['name']} has {variant['missing_truth_count']} "
            "missing truth bin(s)"
        )
    return None


def _assert_quality(variants: list[dict]) -> None:
    for variant in variants:
        reason = _quality_failure_reason(variant)
        if reason:
            raise AssertionError(reason)


def _write_csv(path: Path, variants: list[dict]) -> None:
    fields = [
        "name",
        "status",
        "failure_reason",
        "raster_dimensions",
        "plot_bounds",
        "x_axis",
        "y_axis",
        "bar_color",
        "tolerance",
        "min_area",
        "expected_bin_count",
        "extracted_bin_count",
        "matched_bin_count",
        "unmatched_prediction_count",
        "missing_truth_count",
        "coverage",
        "precision",
        "mae",
        "p95_abs_error",
        "max_abs_error",
        "overlay",
        "image_hash_sha256",
        "bin_x_left",
        "bin_x_right",
        "bin_height",
        "bin_left_pixel",
        "bin_right_pixel",
        "bin_top_pixel",
        "bin_bottom_pixel",
        "bin_pixel_area",
    ]
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for variant in variants:
            base_row = {
                key: variant.get(key, "")
                for key in fields
                if not key.startswith("bin_")
            }
            for key in ("raster_dimensions", "plot_bounds", "x_axis", "y_axis"):
                base_row[key] = json.dumps(base_row[key])
            for bin_ in variant["bins"] or [{}]:
                writer.writerow(
                    {
                        **base_row,
                        "bin_x_left": bin_.get("x_left", ""),
                        "bin_x_right": bin_.get("x_right", ""),
                        "bin_height": bin_.get("height", ""),
                        "bin_left_pixel": bin_.get("left_pixel", ""),
                        "bin_right_pixel": bin_.get("right_pixel", ""),
                        "bin_top_pixel": bin_.get("top_pixel", ""),
                        "bin_bottom_pixel": bin_.get("bottom_pixel", ""),
                        "bin_pixel_area": bin_.get("pixel_area", ""),
                    }
                )


def run_benchmark(output_dir: Path) -> dict:
    """Render local synthetic fixtures, measure extraction, and write its report."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    clean = _render_fixture(output_dir / "histogram_clean.png", dark=False)
    lowres = _resize_fixture(clean, output_dir / "histogram_lowres.jpg")
    dark = _render_fixture(output_dir / "histogram_dark.png", dark=True)
    variants = [_measure_variant(fixture, output_dir) for fixture in (clean, lowres, dark)]
    failure_reasons = []
    for variant in variants:
        failure_reason = _quality_failure_reason(variant)
        variant["status"] = "failed" if failure_reason else "passed"
        variant["failure_reason"] = failure_reason or ""
        if failure_reason:
            failure_reasons.append(failure_reason)

    report = {
        "schema_version": 1,
        "family": "histogram",
        "privacy": PRIVACY_STATEMENT,
        "truth": TRUTH,
        "status": "failed" if failure_reasons else "passed",
        "failure_reason": "; ".join(failure_reasons),
        "variants": variants,
    }
    (output_dir / "histogram_benchmark_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    _write_csv(output_dir / "histogram_benchmark_results.csv", variants)
    _assert_quality(variants)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report = run_benchmark(args.output_dir)
    for variant in report["variants"]:
        print(
            f"{variant['name']}: coverage={variant['coverage']:.3f}, "
            f"mae={variant['mae']:.4f}, p95={variant['p95_abs_error']:.4f}, "
            f"max={variant['max_abs_error']:.4f}"
        )


if __name__ == "__main__":
    main()

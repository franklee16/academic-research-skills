"""Deterministic local benchmark for calibrated boxplot extraction."""

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

from digitize_boxplot import extract_boxplots


BOX_COLOR = "#6baed6"
OUTLIER_COLOR = "#d62728"
LIGHT_LINE_COLOR = "#111111"
DARK_LINE_COLOR = "#f2f2f2"
VALUE_LIMITS = (0.0, 13.0)
LOW_RES_DIMENSIONS = (376, 263)
SUMMARY_FIELDS = ("q1", "median", "q3", "lower_whisker", "upper_whisker")
SUMMARY_MAE_LIMIT = 0.25
OUTLIER_MATCH_TOLERANCE = 0.25
PRIVACY_STATEMENT = "All fixtures are deterministic and locally generated synthetic data."

TRUTH = (
    {
        "label": "A",
        "whislo": 2.0,
        "q1": 3.0,
        "med": 4.5,
        "q3": 6.0,
        "whishi": 8.0,
        "fliers": [1.0],
    },
    {
        "label": "B",
        "whislo": 3.0,
        "q1": 4.0,
        "med": 6.2,
        "q3": 8.0,
        "whishi": 10.0,
        "fliers": [11.5],
    },
    {
        "label": "C",
        "whislo": 1.2,
        "q1": 2.5,
        "med": 3.7,
        "q3": 5.4,
        "whishi": 7.0,
        "fliers": [0.3],
    },
    {
        "label": "D",
        "whislo": 4.0,
        "q1": 5.0,
        "med": 7.1,
        "q3": 9.0,
        "whishi": 10.5,
        "fliers": [12.0],
    },
)


@dataclass(frozen=True)
class RenderedFixture:
    name: str
    path: Path
    orientation: str
    raster_dimensions: tuple[int, int]
    plot_bounds: tuple[int, int, int, int]
    x_axis: tuple[float, float, float, float]
    y_axis: tuple[float, float, float, float]
    box_color: str
    line_color: str
    outlier_color: str
    tolerance: float
    min_area: int


def _hex_rgb(colour: str) -> tuple[int, int, int]:
    colour = colour.lstrip("#")
    return tuple(int(colour[index : index + 2], 16) for index in range(0, 6, 2))


def _json_default(value):
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"{type(value).__name__} is not JSON serializable")


def _plot_bounds_from_bbox(bbox, image_height: int) -> tuple[int, int, int, int]:
    return (
        math.floor(bbox.x0),
        math.floor(image_height - bbox.y1),
        math.ceil(bbox.x1) - 1,
        math.ceil(image_height - bbox.y0) - 1,
    )


def _raster_bbox_from_display(bbox, image_width: int, image_height: int) -> tuple[int, int, int, int]:
    return (
        max(0, math.floor(bbox.x0) - 2),
        max(0, math.floor(image_height - bbox.y1) - 2),
        min(image_width - 1, math.ceil(bbox.x1) + 1),
        min(image_height - 1, math.ceil(image_height - bbox.y0) + 1),
    )


def _remove_median_colour(
    pixels: np.ndarray,
    median_regions: list[tuple[int, int, int, int]],
    *,
    line_color: str,
    background_color: str,
) -> None:
    """Erase only line-colour pixels within each known median segment."""
    line_rgb = np.asarray(_hex_rgb(line_color), dtype=np.int16)
    background_rgb = np.asarray(_hex_rgb(background_color), dtype=np.uint8)
    for left, top, right, bottom in median_regions:
        region = pixels[top : bottom + 1, left : right + 1]
        distance = np.linalg.norm(region.astype(np.int16) - line_rgb, axis=2)
        region[distance <= 80.0] = background_rgb


def _render_fixture(
    path: Path,
    *,
    name: str,
    orientation: str,
    dark: bool,
    remove_medians: bool = False,
) -> RenderedFixture:
    figure_background = "#111111" if dark else "#ffffff"
    axes_background = "#181818" if dark else "#ffffff"
    foreground = "#eeeeee" if dark else "#111111"
    grid_color = "#4d4d4d" if dark else "#dedede"
    line_color = DARK_LINE_COLOR if dark else LIGHT_LINE_COLOR

    figure, axis = plt.subplots(figsize=(6.4, 4.5), dpi=100)
    figure.patch.set_facecolor(figure_background)
    axis.set_facecolor(axes_background)
    figure.subplots_adjust(left=0.13, right=0.80, bottom=0.15, top=0.90)
    is_vertical = orientation == "vertical"
    if is_vertical:
        axis.set_xlim(0.45, 4.55)
        axis.set_ylim(*VALUE_LIMITS)
        axis.set_xticks(range(1, 5), [record["label"] for record in TRUTH])
        axis.set_yticks(range(0, 14, 2))
    else:
        axis.set_xlim(*VALUE_LIMITS)
        axis.set_ylim(4.55, 0.45)
        axis.set_yticks(range(1, 5), [record["label"] for record in TRUTH])
        axis.set_xticks(range(0, 14, 2))
    axis.set_axisbelow(True)
    axis.grid(axis="y" if is_vertical else "x", color=grid_color, linewidth=0.8)
    axis.tick_params(colors=foreground)
    for spine in axis.spines.values():
        spine.set_color(foreground)

    artists = axis.bxp(
        [dict(record) for record in TRUTH],
        positions=range(1, 5),
        widths=0.65,
        capwidths=0.55,
        orientation=orientation,
        patch_artist=True,
        shownotches=False,
        showfliers=True,
        manage_ticks=False,
        boxprops={
            "facecolor": BOX_COLOR,
            "edgecolor": BOX_COLOR,
            "linewidth": 1.0,
            "antialiased": False,
        },
        whiskerprops={"color": line_color, "linewidth": 2.0, "antialiased": False},
        capprops={"color": line_color, "linewidth": 2.0, "antialiased": False},
        medianprops={
            "color": line_color,
            "linewidth": 2.0,
            "antialiased": False,
            "solid_capstyle": "butt",
        },
        flierprops={
            "marker": "o",
            "markerfacecolor": OUTLIER_COLOR,
            "markeredgecolor": OUTLIER_COLOR,
            "markersize": 7,
            "linestyle": "none",
            "antialiased": False,
        },
    )
    for median in artists["medians"]:
        if is_vertical:
            start, end = sorted(float(value) for value in median.get_xdata())
            median.set_xdata((start + 0.04, end - 0.04))
        else:
            start, end = sorted(float(value) for value in median.get_ydata())
            median.set_ydata((start + 0.04, end - 0.04))
    figure.canvas.draw()
    image_width, image_height = figure.canvas.get_width_height()
    axes_bbox = axis.get_window_extent()
    pixels = np.asarray(figure.canvas.buffer_rgba(), dtype=np.uint8).copy()[:, :, :3]
    if remove_medians:
        renderer = figure.canvas.get_renderer()
        median_regions = [
            _raster_bbox_from_display(
                median.get_window_extent(renderer), image_width, image_height
            )
            for median in artists["medians"]
        ]
        _remove_median_colour(
            pixels,
            median_regions,
            line_color=line_color,
            background_color=axes_background,
        )

    image = Image.fromarray(pixels, mode="RGB")
    image.save(path)
    plt.close(figure)
    return RenderedFixture(
        name=name,
        path=path,
        orientation=orientation,
        raster_dimensions=(image_width, image_height),
        plot_bounds=_plot_bounds_from_bbox(axes_bbox, image_height),
        x_axis=(
            float(axes_bbox.x0),
            0.45 if is_vertical else VALUE_LIMITS[0],
            float(axes_bbox.x1),
            4.55 if is_vertical else VALUE_LIMITS[1],
        ),
        y_axis=(
            float(image_height - axes_bbox.y1),
            VALUE_LIMITS[1] if is_vertical else 4.55,
            float(image_height - axes_bbox.y0),
            VALUE_LIMITS[0] if is_vertical else 0.45,
        ),
        box_color=BOX_COLOR,
        line_color=line_color,
        outlier_color=OUTLIER_COLOR,
        tolerance=16.0,
        min_area=12,
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


def _resize_fixture(clean: RenderedFixture, *, name: str, output_path: Path) -> RenderedFixture:
    with Image.open(clean.path) as source:
        source = source.convert("RGB")
        resized = source.resize(LOW_RES_DIMENSIONS, Image.Resampling.LANCZOS)
        resized.save(output_path, format="JPEG", quality=92, subsampling=0)
        scale_x = resized.width / source.width
        scale_y = resized.height / source.height

    def scale_axis(axis: tuple[float, float, float, float], scale: float) -> tuple[float, float, float, float]:
        pixel_start, value_start, pixel_end, value_end = axis
        return pixel_start * scale, value_start, pixel_end * scale, value_end

    return RenderedFixture(
        name=name,
        path=output_path,
        orientation=clean.orientation,
        raster_dimensions=LOW_RES_DIMENSIONS,
        plot_bounds=_scale_bounds(clean.plot_bounds, scale_x, scale_y),
        x_axis=scale_axis(clean.x_axis, scale_x),
        y_axis=scale_axis(clean.y_axis, scale_y),
        box_color=clean.box_color,
        line_color=clean.line_color,
        outlier_color=clean.outlier_color,
        tolerance=70.0,
        min_area=8,
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _summary_truth(record: dict) -> dict[str, float]:
    return {
        "q1": float(record["q1"]),
        "median": float(record["med"]),
        "q3": float(record["q3"]),
        "lower_whisker": float(record["whislo"]),
        "upper_whisker": float(record["whishi"]),
    }


def _match_groups(groups: list[dict]) -> tuple[list[dict], list[float]]:
    matches = []
    errors = []
    for index, truth in enumerate(TRUTH):
        extracted = groups[index] if index < len(groups) else None
        expected_summary = _summary_truth(truth)
        extracted_summary = (
            {field: extracted.get(field) for field in SUMMARY_FIELDS} if extracted else None
        )
        complete = bool(
            extracted
            and extracted.get("status") == "extracted"
            and all(extracted.get(field) is not None for field in SUMMARY_FIELDS)
        )
        statistic_errors = {}
        if complete:
            statistic_errors = {
                field: abs(float(extracted[field]) - expected_summary[field])
                for field in SUMMARY_FIELDS
            }
            errors.extend(statistic_errors.values())
        matches.append(
            {
                "truth_group_index": index,
                "label": truth["label"],
                "expected": expected_summary,
                "extracted": extracted_summary,
                "matched": complete,
                "statistic_abs_errors": statistic_errors,
            }
        )
    return matches, errors


def _match_outliers(groups: list[dict]) -> dict:
    matches = []
    expected_count = sum(len(record["fliers"]) for record in TRUTH)
    observed_count = 0
    matched_count = 0
    for group_index, truth in enumerate(TRUTH):
        observed = []
        if group_index < len(groups):
            observed = [float(item["value"]) for item in groups[group_index].get("outliers", [])]
        observed_count += len(observed)
        available = set(range(len(observed)))
        for expected_value in truth["fliers"]:
            candidates = [
                (abs(observed[index] - expected_value), index) for index in available
            ]
            if candidates:
                error, observed_index = min(candidates)
            else:
                error, observed_index = None, None
            if error is not None and error <= OUTLIER_MATCH_TOLERANCE:
                available.remove(observed_index)
                matched_count += 1
                matches.append(
                    {
                        "group_index": group_index,
                        "expected_value": expected_value,
                        "observed_value": observed[observed_index],
                        "matched": True,
                    }
                )
            else:
                matches.append(
                    {
                        "group_index": group_index,
                        "expected_value": expected_value,
                        "observed_value": None,
                        "matched": False,
                    }
                )
        for observed_index in sorted(available):
            matches.append(
                {
                    "group_index": group_index,
                    "expected_value": None,
                    "observed_value": observed[observed_index],
                    "matched": False,
                }
            )
    precision = matched_count / observed_count if observed_count else 0.0
    recall = matched_count / expected_count if expected_count else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "outlier_expected_count": expected_count,
        "outlier_observed_count": observed_count,
        "outlier_matched_count": matched_count,
        "outlier_precision": precision,
        "outlier_recall": recall,
        "outlier_f1": f1,
        "outlier_matches": matches,
    }


def _write_overlay(image_path: Path, groups: list[dict], output_path: Path) -> None:
    with Image.open(image_path) as source:
        overlay = source.convert("RGB")
    draw = ImageDraw.Draw(overlay)
    for group in groups:
        bounds = group.get("box_bounds_pixel")
        if bounds:
            draw.rectangle(bounds, outline="#ff00ff", width=2)
        for outlier in group.get("outliers", []):
            x, y = outlier["center_pixel"]
            draw.ellipse((x - 4, y - 4, x + 4, y + 4), outline="#00ff00", width=2)
    overlay.save(output_path)


def _measure_fixture(fixture: RenderedFixture, output_dir: Path) -> dict:
    extracted = extract_boxplots(
        fixture.path,
        plot_bounds=fixture.plot_bounds,
        x_axis=fixture.x_axis,
        y_axis=fixture.y_axis,
        box_color=fixture.box_color,
        line_color=fixture.line_color,
        outlier_color=fixture.outlier_color,
        orientation=fixture.orientation,
        tolerance=fixture.tolerance,
        min_area=fixture.min_area,
    )
    groups = extracted["groups"]
    matches, errors = _match_groups(groups)
    coverage = sum(match["matched"] for match in matches) / len(TRUTH)
    if errors:
        summary_mae = float(np.mean(errors))
        summary_p95_abs_error = float(np.percentile(errors, 95))
        summary_max_abs_error = float(np.max(errors))
    else:
        summary_mae = None
        summary_p95_abs_error = None
        summary_max_abs_error = None
    outlier_evidence = _match_outliers(groups)
    overlay_name = f"{fixture.name}_overlay.png"
    _write_overlay(fixture.path, groups, output_dir / overlay_name)
    return {
        "name": fixture.name,
        "image": fixture.path.name,
        "image_hash_sha256": _sha256(fixture.path),
        "orientation": fixture.orientation,
        "raster_dimensions": list(fixture.raster_dimensions),
        "plot_bounds": list(fixture.plot_bounds),
        "x_axis": list(fixture.x_axis),
        "y_axis": list(fixture.y_axis),
        "colors": {
            "box_fill": fixture.box_color,
            "line": fixture.line_color,
            "flier": fixture.outlier_color,
        },
        "tolerance": fixture.tolerance,
        "min_area": fixture.min_area,
        "extractor_status": extracted["status"],
        "extractor_reason": extracted["reason"],
        "groups": groups,
        "group_matches": matches,
        "expected_group_count": len(TRUTH),
        "extracted_group_count": len(groups),
        "group_coverage": coverage,
        "summary_mae": summary_mae,
        "summary_p95_abs_error": summary_p95_abs_error,
        "summary_max_abs_error": summary_max_abs_error,
        "overlay": overlay_name,
        **outlier_evidence,
    }


def _success_failure_reason(variant: dict) -> str | None:
    if variant["extractor_status"] != "extracted":
        return f"{variant['name']} extractor status is {variant['extractor_status']}"
    if variant["extracted_group_count"] != len(TRUTH):
        return f"{variant['name']} extracted {variant['extracted_group_count']} groups, expected 4"
    if variant["group_coverage"] != 1.0:
        return f"{variant['name']} group coverage is {variant['group_coverage']:.3f}, expected 1.0"
    if variant["summary_mae"] is None or variant["summary_mae"] > SUMMARY_MAE_LIMIT:
        value = "unavailable" if variant["summary_mae"] is None else f"{variant['summary_mae']:.4f}"
        return f"{variant['name']} summary MAE {value} exceeds {SUMMARY_MAE_LIMIT}"
    if variant["outlier_f1"] != 1.0:
        return f"{variant['name']} outlier F1 is {variant['outlier_f1']:.3f}, expected 1.0"
    return None


def _rejection_failure_reason(variant: dict) -> str | None:
    if variant["extractor_status"] != "low_confidence":
        return f"{variant['name']} did not return conservative low_confidence"
    if not variant["groups"]:
        return f"{variant['name']} returned no group evidence"
    if any(group.get("status") != "low_confidence" for group in variant["groups"]):
        return f"{variant['name']} contains a non-conservative extracted group"
    if any(group.get("median") is not None for group in variant["groups"]):
        return f"{variant['name']} invented a median value"
    if not all("median" in group.get("reason", "") for group in variant["groups"]):
        return f"{variant['name']} did not explain missing median evidence"
    return None


def _rejection_diagnostic_reason(variant: dict) -> str:
    reasons = []
    for group in variant["groups"]:
        reason = group.get("reason", "").strip()
        if reason and reason not in reasons:
            reasons.append(reason)
    return "; ".join(reasons)


def _write_csv(path: Path, variants: list[dict]) -> None:
    fields = [
        "variant",
        "status",
        "failure_reason",
        "rejection_reason",
        "row_type",
        "group_index",
        "label",
        "image_hash_sha256",
        "plot_bounds",
        "x_axis",
        "y_axis",
        "colors",
        "tolerance",
        "group_status",
        "group_reason",
        "expected_q1",
        "expected_median",
        "expected_q3",
        "expected_lower_whisker",
        "expected_upper_whisker",
        "extracted_q1",
        "extracted_median",
        "extracted_q3",
        "extracted_lower_whisker",
        "extracted_upper_whisker",
        "expected_outlier",
        "observed_outlier",
        "outlier_matched",
        "group_coverage",
        "summary_mae",
        "summary_p95_abs_error",
        "summary_max_abs_error",
        "outlier_precision",
        "outlier_recall",
        "outlier_f1",
        "overlay",
    ]
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for variant in variants:
            base = {
                "variant": variant["name"],
                "status": variant["status"],
                "failure_reason": variant["failure_reason"],
                "rejection_reason": variant["rejection_reason"],
                "image_hash_sha256": variant["image_hash_sha256"],
                "plot_bounds": json.dumps(variant["plot_bounds"]),
                "x_axis": json.dumps(variant["x_axis"]),
                "y_axis": json.dumps(variant["y_axis"]),
                "colors": json.dumps(variant["colors"]),
                "tolerance": variant["tolerance"],
                "group_coverage": variant["group_coverage"],
                "summary_mae": variant["summary_mae"],
                "summary_p95_abs_error": variant["summary_p95_abs_error"],
                "summary_max_abs_error": variant["summary_max_abs_error"],
                "outlier_precision": variant["outlier_precision"],
                "outlier_recall": variant["outlier_recall"],
                "outlier_f1": variant["outlier_f1"],
                "overlay": variant["overlay"],
            }
            for group_index, match in enumerate(variant["group_matches"]):
                group = variant["groups"][group_index] if group_index < len(variant["groups"]) else {}
                expected = match["expected"]
                extracted = match["extracted"] or {}
                writer.writerow(
                    {
                        **base,
                        "row_type": "summary",
                        "group_index": group_index,
                        "label": match["label"],
                        "group_status": group.get("status", "missing"),
                        "group_reason": group.get("reason", "missing group"),
                        **{f"expected_{field}": expected[field] for field in SUMMARY_FIELDS},
                        **{f"extracted_{field}": extracted.get(field, "") for field in SUMMARY_FIELDS},
                    }
                )
            for outlier in variant["outlier_matches"]:
                writer.writerow(
                    {
                        **base,
                        "row_type": "outlier",
                        "group_index": outlier["group_index"],
                        "expected_outlier": outlier["expected_value"],
                        "observed_outlier": outlier["observed_value"],
                        "outlier_matched": outlier["matched"],
                    }
                )


def _assert_quality(successful: list[dict], rejected: dict) -> None:
    for variant in successful:
        reason = _success_failure_reason(variant)
        if reason:
            raise AssertionError(reason)
    rejection_reason = _rejection_failure_reason(rejected)
    if rejection_reason:
        raise AssertionError(rejection_reason)


def run_benchmark(output_dir: Path) -> dict:
    """Render local fixtures, persist evidence, then enforce benchmark gates."""
    output_dir = Path(output_dir)
    if output_dir.exists() and not output_dir.is_dir():
        raise FileExistsError(f"output path exists and is not a directory: {output_dir}")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(
            f"refusing to write benchmark evidence to a non-empty output directory: {output_dir}"
        )
    output_dir.mkdir(parents=True, exist_ok=True)

    vertical_clean = _render_fixture(
        output_dir / "vertical_clean.png",
        name="vertical_clean",
        orientation="vertical",
        dark=False,
    )
    vertical_lowres = _resize_fixture(
        vertical_clean,
        name="vertical_lowres_jpeg",
        output_path=output_dir / "vertical_lowres_jpeg.jpg",
    )
    vertical_dark = _render_fixture(
        output_dir / "vertical_dark.png",
        name="vertical_dark",
        orientation="vertical",
        dark=True,
    )
    horizontal_clean = _render_fixture(
        output_dir / "horizontal_clean.png",
        name="horizontal_clean",
        orientation="horizontal",
        dark=False,
    )
    horizontal_lowres = _resize_fixture(
        horizontal_clean,
        name="horizontal_lowres_jpeg",
        output_path=output_dir / "horizontal_lowres_jpeg.jpg",
    )
    horizontal_dark = _render_fixture(
        output_dir / "horizontal_dark.png",
        name="horizontal_dark",
        orientation="horizontal",
        dark=True,
    )
    vertical_missing_median = _render_fixture(
        output_dir / "vertical_missing_median.png",
        name="vertical_missing_median",
        orientation="vertical",
        dark=False,
        remove_medians=True,
    )
    fixtures = (
        vertical_clean,
        vertical_lowres,
        vertical_dark,
        horizontal_clean,
        horizontal_lowres,
        horizontal_dark,
        vertical_missing_median,
    )
    variants = [_measure_fixture(fixture, output_dir) for fixture in fixtures]
    successful = variants[:-1]
    rejected = variants[-1]
    failure_reasons = []
    for variant in successful:
        reason = _success_failure_reason(variant)
        variant["status"] = "passed" if reason is None else "failed"
        variant["failure_reason"] = reason or ""
        variant["rejection_reason"] = ""
        if reason:
            failure_reasons.append(reason)
    rejection_reason = _rejection_failure_reason(rejected)
    rejected["status"] = "rejected_as_expected" if rejection_reason is None else "failed"
    rejected["failure_reason"] = rejection_reason or ""
    rejected["rejection_reason"] = _rejection_diagnostic_reason(rejected)
    if rejection_reason:
        failure_reasons.append(rejection_reason)

    report = {
        "schema_version": 1,
        "family": "boxplot",
        "privacy": PRIVACY_STATEMENT,
        "truth": [dict(record) for record in TRUTH],
        "status": "passed" if not failure_reasons else "failed",
        "failure_reason": "; ".join(failure_reasons),
        "rejection_reason": "; ".join(
            f"{variant['name']}: {variant['rejection_reason']}"
            for variant in variants
            if variant["status"] == "rejected_as_expected"
        ),
        "variants": variants,
    }
    serialized_report = json.dumps(report, indent=2, default=_json_default)
    (output_dir / "boxplot_report.json").write_text(
        serialized_report + "\n", encoding="utf-8"
    )
    _write_csv(output_dir / "boxplot_results.csv", variants)
    _assert_quality(successful, rejected)
    return json.loads(serialized_report)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report = run_benchmark(args.output_dir)
    for variant in report["variants"]:
        print(
            f"{variant['name']}: status={variant['status']}, "
            f"coverage={variant['group_coverage']:.3f}, "
            f"mae={variant['summary_mae']}, f1={variant['outlier_f1']:.3f}"
        )


if __name__ == "__main__":
    main()

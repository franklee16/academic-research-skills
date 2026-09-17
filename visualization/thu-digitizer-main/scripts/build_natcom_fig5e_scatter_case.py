"""Build the calibrated, data-consistent gallery case for Nat. Commun. Fig. 5e.

The case recovers separable visible marker centres from the raster.  It does
not claim access to hidden or perfectly coincident source observations.  The
CSV, static recreation, and interactive SVG geometry are all generated from
the same recovered points.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import cv2
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw


CASE_ID = "nature-70099-fig5e"
CANVAS_SIZE = (1010, 360)
POINT_COLOR = "#282829"
LINE_COLOR = "#0058A2"
BAND_COLOR = "#DBE8F3"
Y_ANCHORS = [
    {"pixel": 100.5, "value": 3.0},
    {"pixel": 149.0, "value": 2.5},
    {"pixel": 197.5, "value": 2.0},
    {"pixel": 245.5, "value": 1.5},
    {"pixel": 293.5, "value": 1.0},
]
PANELS = [
    {
        "panel_id": "ab42_ab40_ratio",
        "label": "Aβ42/Aβ40 ratio",
        "plot_bounds": (106, 91, 340, 304),
        "detection_roi": (110, 130, 336, 280),
        "x_anchors": [
            {"pixel": 150.5, "value": 0.04},
            {"pixel": 207.5, "value": 0.06},
            {"pixel": 264.5, "value": 0.08},
            {"pixel": 321.5, "value": 0.10},
        ],
        "xlim": (0.0245, 0.1065),
        "xticks": [0.04, 0.06, 0.08, 0.10],
        "expected_points": 17,
        "annotated_r": -0.57,
        "annotated_p": 0.018,
        "annotation": r"$R = -0.57,\ p = 0.018$",
        "annotation_xy": (0.0282, 2.80),
        "overlay_color": "#DB28FF",
    },
    {
        "panel_id": "moca",
        "label": "MoCA",
        "plot_bounds": (403, 91, 638, 304),
        "detection_roi": (408, 130, 634, 280),
        "x_anchors": [
            {"pixel": 424.0, "value": 10},
            {"pixel": 474.5, "value": 15},
            {"pixel": 525.5, "value": 20},
            {"pixel": 576.5, "value": 25},
            {"pixel": 627.0, "value": 30},
        ],
        "xlim": (8.0, 31.0),
        "xticks": [10, 15, 20, 25, 30],
        "expected_points": 16,
        "annotated_r": -0.34,
        "annotated_p": 0.17,
        "annotation": r"$R = -0.34,\ p = 0.17$",
        "annotation_xy": (9.0, 2.80),
        "overlay_color": "#00B45A",
    },
    {
        "panel_id": "p_tau_181",
        "label": "p-Tau-181",
        "plot_bounds": (700, 91, 936, 304),
        "detection_roi": (706, 130, 932, 280),
        "x_anchors": [
            {"pixel": 736.5, "value": 50},
            {"pixel": 790.5, "value": 100},
            {"pixel": 844.5, "value": 150},
            {"pixel": 898.5, "value": 200},
        ],
        "xlim": (15.0, 235.0),
        "xticks": [50, 100, 150, 200],
        "expected_points": 15,
        "annotated_r": 0.12,
        "annotated_p": 0.66,
        "annotation": r"$R = 0.12,\ p = 0.66$",
        "annotation_xy": (26.0, 2.80),
        "overlay_color": "#FF7800",
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fit_axis(anchors: list[dict[str, float]]) -> dict[str, float]:
    pixels = np.asarray([anchor["pixel"] for anchor in anchors], dtype=float)
    values = np.asarray([anchor["value"] for anchor in anchors], dtype=float)
    slope, intercept = np.polyfit(pixels, values, 1)
    residuals = values - (slope * pixels + intercept)
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "anchor_rmse": float(np.sqrt(np.mean(residuals**2))),
        "anchor_max_abs_residual": float(np.max(np.abs(residuals))),
    }


def pixel_to_value(pixel: float | np.ndarray, calibration: dict[str, float]):
    return calibration["slope"] * pixel + calibration["intercept"]


def value_to_pixel(value: float | np.ndarray, calibration: dict[str, float]):
    return (value - calibration["intercept"]) / calibration["slope"]


def detect_visible_centres(
    image_rgb: np.ndarray, roi: tuple[int, int, int, int]
) -> list[dict[str, float]]:
    left, top, right, bottom = roi
    crop = image_rgb[top : bottom + 1, left : right + 1]
    gray = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)

    # A thin blue regression stroke also passes this gray threshold, but its
    # distance-transform radius is far below a marker core.  Local radius
    # maxima retain individually visible centres inside touching clusters.
    foreground = (gray < 150).astype(np.uint8)
    distance = cv2.distanceTransform(foreground, cv2.DIST_L2, 5)
    local_maximum = distance == cv2.dilate(distance, np.ones((7, 7), np.uint8))
    peaks = (local_maximum & (distance >= 4.2)).astype(np.uint8)
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(peaks, 8)

    centres: list[dict[str, float]] = []
    for label in range(1, count):
        center_x, center_y = centroids[label]
        centres.append(
            {
                "x_pixel": float(center_x + left),
                "y_pixel": float(center_y + top),
                "peak_area_pixels": int(stats[label, cv2.CC_STAT_AREA]),
                "marker_radius_evidence_pixels": float(distance[labels == label].max()),
            }
        )
    return centres


def regression_geometry(
    points: list[dict[str, float]],
    x_calibration: dict[str, float],
    y_calibration: dict[str, float],
) -> dict[str, Any]:
    x = np.asarray([point["x_value"] for point in points], dtype=float)
    y = np.asarray([point["y_value"] for point in points], dtype=float)
    design = np.column_stack([np.ones_like(x), x])
    beta = np.linalg.lstsq(design, y, rcond=None)[0]
    residuals = y - design @ beta
    residual_sd = float(np.sqrt((residuals @ residuals) / (len(x) - 2)))
    correlation = float(np.corrcoef(x, y)[0, 1])

    x_grid = np.linspace(float(x.min()), float(x.max()), 240)
    fitted = beta[0] + beta[1] * x_grid
    x_pixels = value_to_pixel(x_grid, x_calibration)
    fitted_pixels = value_to_pixel(fitted, y_calibration)
    upper_pixels = value_to_pixel(fitted + residual_sd, y_calibration)
    lower_pixels = value_to_pixel(fitted - residual_sd, y_calibration)
    polygon = [
        *[(float(px), float(py)) for px, py in zip(x_pixels, upper_pixels)],
        *[(float(px), float(py)) for px, py in zip(x_pixels[::-1], lower_pixels[::-1])],
    ]
    return {
        "intercept": float(beta[0]),
        "slope": float(beta[1]),
        "residual_sd": residual_sd,
        "correlation": correlation,
        "x_min": float(x_grid[0]),
        "x_max": float(x_grid[-1]),
        "y_min_fit": float(fitted[0]),
        "y_max_fit": float(fitted[-1]),
        "x_pixel_start": float(x_pixels[0]),
        "y_pixel_start": float(fitted_pixels[0]),
        "x_pixel_end": float(x_pixels[-1]),
        "y_pixel_end": float(fitted_pixels[-1]),
        "polygon": polygon,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "mathtext.fontset": "custom",
            "mathtext.rm": "Arial",
            "mathtext.it": "Arial:italic",
            "axes.linewidth": 1.15,
            "xtick.major.width": 1.0,
            "ytick.major.width": 1.0,
            "xtick.major.size": 4.0,
            "ytick.major.size": 4.0,
            "xtick.direction": "out",
            "ytick.direction": "out",
        }
    )


def render_recreation(
    output: Path,
    points_by_panel: dict[str, list[dict[str, float]]],
    fits_by_panel: dict[str, dict[str, Any]],
) -> None:
    configure_matplotlib()
    figure = plt.figure(figsize=(10.10, 3.60), dpi=100, facecolor="white")
    axes = [
        figure.add_axes([106 / 1010, 56 / 360, 234 / 1010, 213 / 360]),
        figure.add_axes([403 / 1010, 56 / 360, 235 / 1010, 213 / 360]),
        figure.add_axes([700 / 1010, 56 / 360, 236 / 1010, 213 / 360]),
    ]

    for index, (panel, axis) in enumerate(zip(PANELS, axes)):
        points = points_by_panel[panel["panel_id"]]
        fit = fits_by_panel[panel["panel_id"]]
        x = np.asarray([point["x_value"] for point in points], dtype=float)
        y = np.asarray([point["y_value"] for point in points], dtype=float)
        x_grid = np.linspace(float(x.min()), float(x.max()), 300)
        fitted = fit["intercept"] + fit["slope"] * x_grid
        residual_sd = fit["residual_sd"]

        axis.fill_between(
            x_grid,
            fitted - residual_sd,
            fitted + residual_sd,
            color=BAND_COLOR,
            linewidth=0,
            zorder=1,
        )
        axis.plot(x_grid, fitted, color=LINE_COLOR, linewidth=2.35, zorder=2)
        axis.scatter(
            x,
            y,
            s=70,
            facecolor=POINT_COLOR,
            edgecolor=POINT_COLOR,
            linewidth=0.35,
            zorder=3,
        )
        axis.set_xlim(*panel["xlim"])
        axis.set_ylim(0.90, 3.10)
        axis.set_xticks(panel["xticks"])
        axis.set_yticks([1.0, 1.5, 2.0, 2.5, 3.0])
        axis.set_xlabel(panel["label"], fontsize=16.5, fontweight="bold", labelpad=1.0)
        if index == 0:
            axis.set_ylabel(
                "Combined\nmodule score",
                fontsize=17.5,
                fontweight="bold",
                labelpad=8,
            )
        axis.tick_params(axis="both", labelsize=13.5, colors="#444444", pad=3)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.spines["left"].set_color("#111111")
        axis.spines["bottom"].set_color("#111111")
        axis.grid(False)
        axis.text(
            *panel["annotation_xy"],
            panel["annotation"],
            fontsize=14.5,
            fontweight="bold",
            ha="left",
            va="center",
        )

    figure.text(
        0.5,
        0.855,
        "Combined module vs CSF biomarkers and cognitive function",
        ha="center",
        va="center",
        fontsize=20.5,
        fontweight="bold",
        color="#28272A",
    )
    figure.text(
        0.003,
        0.992,
        "E)",
        ha="left",
        va="top",
        fontsize=32,
        fontweight="bold",
        color="#28272A",
    )
    figure.savefig(output, dpi=100, facecolor="white")
    plt.close(figure)


def build_geometry(
    points_by_panel: dict[str, list[dict[str, float]]],
    fits_by_panel: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    lines: list[dict[str, Any]] = []
    annotations: list[dict[str, Any]] = [
        {
            "text": "E)",
            "x": 3,
            "y": -3,
            "size": 44,
            "bold": True,
            "dominantBaseline": "hanging",
        },
        {
            "text": "Combined module vs CSF biomarkers and cognitive function",
            "x": 103,
            "y": 38,
            "size": 29,
            "bold": True,
            "dominantBaseline": "hanging",
        },
    ]
    polygons: list[dict[str, Any]] = []

    for panel_index, panel in enumerate(PANELS):
        left, top, right, bottom = panel["plot_bounds"]
        lines.extend(
            [
                {"x1": left, "y1": top, "x2": left, "y2": bottom, "width": 1.6},
                {"x1": left, "y1": bottom, "x2": right, "y2": bottom, "width": 1.6},
            ]
        )
        for anchor in panel["x_anchors"]:
            pixel = anchor["pixel"]
            value = anchor["value"]
            lines.append(
                {"x1": pixel, "y1": bottom, "x2": pixel, "y2": bottom + 6, "width": 1.2}
            )
            label = f"{value:.2f}" if panel_index == 0 else f"{value:g}"
            annotations.append(
                {
                    "text": label,
                    "x": pixel,
                    "y": bottom + 20,
                    "size": 17,
                    "anchor": "middle",
                    "dominantBaseline": "middle",
                }
            )
        for anchor in Y_ANCHORS:
            pixel = anchor["pixel"]
            lines.append(
                {"x1": left - 6, "y1": pixel, "x2": left, "y2": pixel, "width": 1.2}
            )
            annotations.append(
                {
                    "text": f"{anchor['value']:.1f}",
                    "x": left - 12,
                    "y": pixel,
                    "size": 17,
                    "anchor": "end",
                    "dominantBaseline": "middle",
                }
            )
        statistic = f"R = {panel['annotated_r']:.2f}, p = {panel['annotated_p']:g}"
        annotations.extend(
            [
                {
                    "text": statistic.replace("-", "−"),
                    "x": left + 11,
                    "y": 108,
                    "size": 17,
                    "italic": True,
                    "dominantBaseline": "middle",
                },
                {
                    "text": panel["label"],
                    "x": (left + right) / 2,
                    "y": 341,
                    "size": 21,
                    "bold": True,
                    "anchor": "middle",
                    "dominantBaseline": "middle",
                },
            ]
        )
        if panel_index == 0:
            annotations.append(
                {
                    "text": "Combined\nmodule score",
                    "x": 28,
                    "y": 202,
                    "size": 21,
                    "bold": True,
                    "anchor": "middle",
                    "rotate": -90,
                    "dominantBaseline": "middle",
                }
            )
        polygons.append(
            {
                "points": fits_by_panel[panel["panel_id"]]["polygon"],
                "fill": BAND_COLOR.lower(),
                "representation": "fitted line ± residual SD",
            }
        )
    return {
        "schema_version": 1,
        "coordinate_space": "original_raster_pixels",
        "lines": lines,
        "rects": [],
        "polygons": polygons,
        "annotations": annotations,
    }


def make_overlay(
    original: Image.Image,
    output: Path,
    points_by_panel: dict[str, list[dict[str, float]]],
) -> None:
    overlay = original.convert("RGB").copy()
    draw = ImageDraw.Draw(overlay)
    for panel in PANELS:
        color = panel["overlay_color"]
        left, top, right, bottom = panel["plot_bounds"]
        draw.rectangle((left, top, right, bottom), outline=color, width=1)
        for point in points_by_panel[panel["panel_id"]]:
            x, y = point["x_pixel"], point["y_pixel"]
            draw.ellipse((x - 8, y - 8, x + 8, y + 8), outline=color, width=2)
            draw.line((x - 3, y, x + 3, y), fill=color, width=1)
            draw.line((x, y - 3, x, y + 3), fill=color, width=1)
    overlay.save(output)


def update_manifest(path: Path, max_r_difference: float) -> None:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    sample = next(item for item in manifest["samples"] if item["id"] == CASE_ID)
    sample.update(
        {
            "status": "visible_geometry_candidate",
            "statusLabel": "候选 · 校准可见散点",
            "description": (
                "Fig. 5e 的三个散点面板：48 个可见圆点经坐标轴校准恢复；"
                "静态图、CSV 与交互 SVG 使用同一份点数据。回归线为可见点 OLS 重拟合，"
                "浅蓝带为拟合线 ± 残差标准差。"
            ),
            "metrics": [
                {"label": "visible points", "value": "48"},
                {"label": "panels", "value": "3"},
                {"label": "max |ΔR|", "value": f"{max_r_difference:.3f}"},
            ],
        }
    )
    style = sample["styleSpec"]
    style.update(
        {
            "renderer": "paper-native-geometry",
            "fidelity": "visible_geometry_candidate",
            "label": "48 个可见散点 · 同源 SVG 重绘",
            "note": (
                "所有悬停点均来自下载 CSV；回归线由这 48 个可见点 OLS 重拟合，"
                "浅蓝带定义为拟合线 ± 残差标准差，不推断完全重合或被遮挡的原始观测。"
            ),
            "canvas": {"width": CANVAS_SIZE[0], "height": CANVAS_SIZE[1]},
            "fontFamily": "Arial, Helvetica, sans-serif",
            "geometryAsset": f"assets/cases/{CASE_ID}/geometry.json",
        }
    )
    style.pop("rasterEvidenceInteractive", None)
    for stale_key in ("lines", "rects", "polygons", "annotations"):
        style.pop(stale_key, None)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_case(
    *,
    input_path: Path,
    output_dir: Path,
    crop: tuple[int, int, int, int] | None = None,
    manifest_path: Path | None = None,
) -> dict[str, Any]:
    source = Image.open(input_path).convert("RGB")
    original = source.crop(crop) if crop else source.copy()
    if original.size != CANVAS_SIZE:
        raise ValueError(f"expected {CANVAS_SIZE} raster, got {original.size}")
    image_rgb = np.asarray(original)
    y_calibration = fit_axis(Y_ANCHORS)

    output_dir.mkdir(parents=True, exist_ok=True)
    original.save(output_dir / "original.png")
    line_rows: list[dict[str, Any]] = []
    point_rows: list[dict[str, Any]] = []
    points_by_panel: dict[str, list[dict[str, float]]] = {}
    fits_by_panel: dict[str, dict[str, Any]] = {}
    panel_reports: list[dict[str, Any]] = []

    for panel in PANELS:
        x_calibration = fit_axis(panel["x_anchors"])
        centres = detect_visible_centres(image_rgb, panel["detection_roi"])
        if len(centres) != panel["expected_points"]:
            raise AssertionError(
                f"{panel['panel_id']}: expected {panel['expected_points']} visible centres, "
                f"found {len(centres)}"
            )
        x_uncertainty = math.hypot(
            abs(x_calibration["slope"]) * 0.75, x_calibration["anchor_rmse"]
        )
        y_uncertainty = math.hypot(
            abs(y_calibration["slope"]) * 0.75, y_calibration["anchor_rmse"]
        )
        points = []
        for centre in centres:
            points.append(
                {
                    **centre,
                    "x_value": float(pixel_to_value(centre["x_pixel"], x_calibration)),
                    "y_value": float(pixel_to_value(centre["y_pixel"], y_calibration)),
                }
            )
        points.sort(key=lambda item: (item["x_value"], -item["y_value"]))
        fit = regression_geometry(points, x_calibration, y_calibration)
        r_difference = abs(fit["correlation"] - panel["annotated_r"])
        if r_difference > 0.01:
            raise AssertionError(
                f"{panel['panel_id']}: extracted r={fit['correlation']:.4f} differs from "
                f"annotated r={panel['annotated_r']:.2f}"
            )

        points_by_panel[panel["panel_id"]] = points
        fits_by_panel[panel["panel_id"]] = fit
        line_rows.append(
            {
                "kind": "line",
                "series": panel["label"],
                "category": "OLS refit from extracted visible points",
                "x": round(fit["x_min"], 6),
                "y": round(fit["y_min_fit"], 6),
                "value": "OLS refit",
                "pixel_x": round(fit["x_pixel_start"], 3),
                "pixel_y": round(fit["y_pixel_start"], 3),
                "x2": round(fit["x_pixel_end"], 3),
                "y2": round(fit["y_pixel_end"], 3),
                "fit_intercept": round(fit["intercept"], 9),
                "fit_slope": round(fit["slope"], 9),
                "residual_sd": round(fit["residual_sd"], 9),
                "recomputed_r": round(fit["correlation"], 9),
                "annotated_r": panel["annotated_r"],
                "annotated_p": panel["annotated_p"],
                "stroke": LINE_COLOR,
                "stroke_width": 2.35,
                "value_status": "refit_from_extracted_visible_points",
            }
        )
        for point_index, point in enumerate(points, start=1):
            point_rows.append(
                {
                    "kind": "point",
                    "series": panel["label"],
                    "category": "visible point",
                    "point_id": point_index,
                    "x": round(point["x_value"], 6),
                    "y": round(point["y_value"], 6),
                    "value": round(point["y_value"], 6),
                    "pixel_x": round(point["x_pixel"], 3),
                    "pixel_y": round(point["y_pixel"], 3),
                    "radius": 5.8,
                    "fill": POINT_COLOR,
                    "x_uncertainty_approx": round(x_uncertainty, 6),
                    "y_uncertainty_approx": round(y_uncertainty, 6),
                    "marker_radius_evidence_pixels": round(
                        point["marker_radius_evidence_pixels"], 3
                    ),
                    "value_status": "visible_marker_extracted",
                }
            )
        panel_reports.append(
            {
                "panel_id": panel["panel_id"],
                "label": panel["label"],
                "visible_point_count": len(points),
                "plot_bounds": list(panel["plot_bounds"]),
                "detection_roi": list(panel["detection_roi"]),
                "x_anchors": panel["x_anchors"],
                "y_anchors": Y_ANCHORS,
                "x_calibration": x_calibration,
                "y_calibration": y_calibration,
                "annotated_r": panel["annotated_r"],
                "recomputed_r": fit["correlation"],
                "absolute_r_difference": r_difference,
                "residual_sd": fit["residual_sd"],
                "status": "validated_against_visible_correlation_annotation",
            }
        )

    rows = [*line_rows, *point_rows]
    write_csv(output_dir / "data.csv", rows)
    geometry = build_geometry(points_by_panel, fits_by_panel)
    (output_dir / "geometry.json").write_text(
        json.dumps(geometry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    render_recreation(output_dir / "recreated.png", points_by_panel, fits_by_panel)
    make_overlay(original, output_dir / "overlay.png", points_by_panel)

    max_r_difference = max(panel["absolute_r_difference"] for panel in panel_reports)
    report = {
        "schema_version": 1,
        "case_contract_version": 2,
        "case_id": CASE_ID,
        "status": "visible_geometry_candidate",
        "route": "assisted_distance_transform_scatter_centres",
        "input": {
            "file": str(input_path),
            "sha256": sha256(input_path),
            "crop": list(crop) if crop else None,
            "canvas": list(CANVAS_SIZE),
        },
        "visible_point_count": len(point_rows),
        "visible_points_by_panel": [
            len(points_by_panel[panel["panel_id"]]) for panel in PANELS
        ],
        "fit_representation": "OLS refit from extracted visible points",
        "ribbon_representation": "fitted line ± residual SD",
        "correlation_validation_max_abs_difference": max_r_difference,
        "panels": panel_reports,
        "outputs": {
            "data": "data.csv",
            "geometry": "geometry.json",
            "recreated": "recreated.png",
            "overlay": "overlay.png",
        },
        "comparison": {
            "prior_gallery_candidate": "36 visible points; failed dense touching-marker clusters",
            "webplotdigitizer": "not_compared",
        },
        "limitations": [
            "Values are calibrated from visible raster marker centres, not author raw observations.",
            "Perfectly coincident or fully occluded observations cannot be recovered.",
            "The regression line is a new OLS refit from extracted points, not proof of the authors' hidden fit settings.",
            "The ribbon is defined for this recreation as fitted line ± residual SD; the source author's interval definition is unknown.",
        ],
    }
    (output_dir / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if manifest_path:
        update_manifest(manifest_path, max_r_difference)
    return report


def parse_crop(value: str) -> tuple[int, int, int, int]:
    values = tuple(int(part.strip()) for part in value.split(","))
    if len(values) != 4:
        raise argparse.ArgumentTypeError("crop must be left,top,right,bottom")
    return values  # type: ignore[return-value]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--crop", type=parse_crop)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    report = build_case(
        input_path=args.input,
        output_dir=args.output_dir,
        crop=args.crop,
        manifest_path=args.manifest,
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "visible_point_count": report["visible_point_count"],
                "output_dir": str(args.output_dir),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

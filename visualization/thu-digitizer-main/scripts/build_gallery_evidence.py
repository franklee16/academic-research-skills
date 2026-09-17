"""Build reproducible evidence assets for the thu-digitizer project gallery.

The script works only from locally stored OA figures and source-data exports. It
does not download anything and it never treats a visually similar recreation as
numeric ground truth. Each case emits a CSV, overlay, recreation, and JSON report.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from scipy.optimize import curve_fit


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "gallery" / "assets" / "cases"
DATA_DIR = ROOT / "gallery" / "data"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    def encode_numpy(value):
        if isinstance(value, np.generic):
            return value.item()
        if isinstance(value, np.ndarray):
            return value.tolist()
        raise TypeError(f"Object of type {value.__class__.__name__} is not JSON serializable")

    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=encode_numpy),
        encoding="utf-8",
    )


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def affine(value: float, value0: float, pixel0: float, value1: float, pixel1: float) -> float:
    return pixel0 + (value - value0) * (pixel1 - pixel0) / (value1 - value0)


def inverse_affine(pixel: float, value0: float, pixel0: float, value1: float, pixel1: float) -> float:
    return value0 + (pixel - pixel0) * (value1 - value0) / (pixel1 - pixel0)


def font(size: int = 12) -> ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def nearest_ink_distances(mask: np.ndarray, points: list[tuple[float, float]]) -> list[float]:
    distance = ndimage.distance_transform_edt(~mask)
    height, width = mask.shape
    values = []
    for x, y in points:
        px = int(round(np.clip(x, 0, width - 1)))
        py = int(round(np.clip(y, 0, height - 1)))
        values.append(float(distance[py, px]))
    return values


def save_figure(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="#fbfaf6")
    plt.close(fig)


def build_borneo() -> dict:
    case_dir = CASES / "nature-borneo-edge"
    original = case_dir / "original.jpg"
    source_csv = case_dir / "source-data.csv"
    image = Image.open(original).convert("RGB")
    pixels = np.asarray(image)
    rows = read_csv(source_csv)

    points = []
    visible_rows = []
    extracted_rows = []
    for row in rows:
        distance = float(row["edge_distance_m"])
        agb_change = float(row["agb_change"])
        x_pixel = affine(distance, 0.0, 70.0, 2000.0, 419.0)
        y_pixel = affine(agb_change, 0.0, 169.0, 4.0, 93.0)
        panel_a_visible = 0.0 <= distance <= 2000.0 and -8.5 <= agb_change <= 5.5
        extracted = {
            **row,
            "panel_a_visible": panel_a_visible,
            "source_x_pixel": round(x_pixel, 3),
            "source_y_pixel": round(y_pixel, 3),
            "nearest_ink_distance_px": None,
            "raster_supported_5px": None,
        }
        extracted_rows.append(extracted)
        if panel_a_visible:
            points.append((x_pixel, y_pixel))
            visible_rows.append(extracted)

    gray = np.asarray(image.convert("L"))
    ink = gray < 225
    support_distances = nearest_ink_distances(ink, points)
    for row, distance in zip(visible_rows, support_distances):
        row["nearest_ink_distance_px"] = round(distance, 3)
        row["raster_supported_5px"] = distance <= 5.0

    output_csv = case_dir / "data.csv"
    write_csv(output_csv, list(extracted_rows[0].keys()), extracted_rows)

    overlay = image.copy()
    draw = ImageDraw.Draw(overlay)
    for (x, y), source_row in zip(points, visible_rows):
        color = (0, 177, 169) if source_row["edge_effects"].lower() == "no" else (255, 90, 54)
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), outline=color, width=2)
    draw.rounded_rectangle((12, 337, 392, 374), radius=8, fill=(15, 23, 23))
    draw.text((23, 346), "50 visible scatter rows / 71 histogram rows", fill=(255, 255, 255), font=font(13))
    overlay_path = case_dir / "overlay.png"
    overlay.save(overlay_path)

    distance_values = np.array([float(row["edge_distance_m"]) for row in rows])
    agb_values = np.array([float(row["agb_change"]) for row in rows])
    weighted_values = np.array([float(row["weighted_agb_change"]) for row in rows])
    edge_flags = np.array([row["edge_effects"].lower() == "yes" for row in rows])

    breakpoint = 448.0
    plateau = 1.14
    clipped = np.minimum(distance_values, breakpoint)
    slope = float(np.sum((clipped - breakpoint) * (agb_values - plateau)) / np.sum((clipped - breakpoint) ** 2))

    asymptote = 1.26

    def asymptotic_model(x: np.ndarray, start: float, scale: float) -> np.ndarray:
        return asymptote - (asymptote - start) * np.exp(-x / scale)

    try:
        (start, scale), _ = curve_fit(
            asymptotic_model,
            distance_values,
            agb_values,
            p0=(-2.0, 250.0),
            bounds=((-8.0, 20.0), (2.0, 3000.0)),
            maxfev=20000,
        )
    except (RuntimeError, ValueError):
        start, scale = -2.1, 250.0

    fig, (ax_scatter, ax_hist) = plt.subplots(
        1,
        2,
        figsize=(11.2, 5.2),
        gridspec_kw={"width_ratios": [2.35, 1]},
    )
    ax_scatter.scatter(
        distance_values,
        agb_values,
        marker="s",
        s=30,
        facecolors="white",
        edgecolors="#3f4a49",
        linewidths=0.9,
        zorder=3,
    )
    x_line = np.linspace(0, 2000, 500)
    hockey = plateau + slope * (np.minimum(x_line, breakpoint) - breakpoint)
    ax_scatter.plot(x_line, hockey, color="#1e2927", linewidth=1.6)
    ax_scatter.plot(x_line, asymptotic_model(x_line, start, scale), color="#68716f", linestyle="--", linewidth=1.2)
    ax_scatter.set(xlim=(-80, 2080), ylim=(-8.5, 5.5), xlabel="Distance to forest edge (m)", ylabel="AGB change (Mg ha⁻¹ per year)")
    ax_scatter.spines[["top", "right"]].set_visible(False)
    ax_scatter.text(-0.12, 1.03, "a", transform=ax_scatter.transAxes, fontsize=18, fontweight="bold")

    bins = np.arange(-8, 8, 2)
    ax_hist.hist(weighted_values[~edge_flags], bins=bins, color="#217a2a", alpha=0.9, label="Interior")
    ax_hist.hist(weighted_values[edge_flags], bins=bins, color="#f4a02f", alpha=0.85, label="Edge")
    ax_hist.axvline(1.01, color="#217a2a", linestyle="--", linewidth=1.5)
    ax_hist.axvline(-0.36, color="#f4a02f", linestyle="--", linewidth=1.5)
    ax_hist.set(xlim=(-8, 6), ylim=(0, 21), xlabel="AGB change\n(Mg ha⁻¹ per year)", ylabel="Number of plots")
    ax_hist.legend(frameon=False, loc="upper left")
    ax_hist.spines[["top", "right"]].set_visible(False)
    ax_hist.text(-0.25, 1.03, "b", transform=ax_hist.transAxes, fontsize=18, fontweight="bold")
    fig.suptitle("Recreated from Nature Communications Fig. 2 source data", fontsize=12, x=0.52, y=1.02)
    fig.tight_layout()
    recreation_path = case_dir / "recreated.png"
    save_figure(fig, recreation_path)

    report = {
        "schema_version": 1,
        "case_id": "nature-borneo-edge",
        "status": "official_source_data_mapped",
        "scope": "Full Fig. 2: panel a source points plus reported models; panel b source histogram geometry.",
        "original_sha256": sha256(original),
        "source_data_sha256": sha256(case_dir / "source-data.xlsx"),
        "source_rows": len(rows),
        "panel_a_visible_rows": len(visible_rows),
        "panel_a_out_of_range_rows": len(rows) - len(visible_rows),
        "groups": {"interior": int((~edge_flags).sum()), "edge": int(edge_flags.sum())},
        "calibration": {
            "panel_a_x": [{"pixel": 70, "value": 0}, {"pixel": 419, "value": 2000}],
            "panel_a_y": [{"pixel": 169, "value": 0}, {"pixel": 93, "value": 4}],
            "axis_type": "linear",
        },
        "validation": {
            "raster_support_within_5px": round(float(np.mean(np.array(support_distances) <= 5.0)), 4),
            "median_nearest_ink_distance_px": round(float(np.median(support_distances)), 3),
            "source_count_matches_caption": len(rows) == 71,
            "registration_denominator": "50 source rows inside the visible panel-a axis range",
        },
        "limitations": [
            "The solid and dashed model curves are reconstructed from the reported breakpoint/asymptote and source points; curve parameters beyond those reported are fitted for display.",
            "Twenty-one source rows have edge distances above the visible 2000 m panel-a axis limit; they remain in the CSV and panel-b histogram but are not drawn onto the panel-a overlay.",
            "Raster support checks registration against visible marks; they are not independent ground-truth measurements.",
        ],
    }
    write_json(case_dir / "report.json", report)
    return report


FOREST_LABELS = [
    "Vitamin D",
    "Monocytes",
    "Lymphocytes",
    "Random glucose",
    "Neutrophils",
    "HbA1c",
    "WBC count",
    "Eosinophils",
    "MCH",
    "Platelets",
    "MCV",
    "Phosphate",
    "RDW",
    "Total cholesterol",
    "RBC count",
    "LDL",
    "Total protein",
    "Urea",
    "Creatinine",
    "CRP",
    "Albumin",
    "Haemoglobin",
    "HDL",
    "ALT",
    "Triglycerides",
    "Calcium",
    "Bilirubin",
    "Haematocrit",
    "ALP",
]


def contiguous_runs(values: np.ndarray) -> list[tuple[int, int]]:
    indices = np.flatnonzero(values)
    if not len(indices):
        return []
    groups = np.split(indices, np.where(np.diff(indices) > 1)[0] + 1)
    return [(int(group[0]), int(group[-1])) for group in groups]


def build_forest() -> dict:
    case_dir = CASES / "nature-blood-forest"
    original = case_dir / "original.jpg"
    image = Image.open(original).convert("RGB")
    rgb = np.asarray(image)
    gray = np.asarray(image.convert("L"))
    height, width = gray.shape

    zero_px, one_px = 169.0, 441.0
    y_guesses = np.linspace(10.0, 398.0, len(FOREST_LABELS))
    dark = gray < 170
    colorfulness = (rgb.max(axis=2) - rgb.min(axis=2)).astype(float)
    point_density = ndimage.uniform_filter(colorfulness, size=(7, 7), mode="constant")

    observations = []
    overlay = image.copy()
    draw = ImageDraw.Draw(overlay)
    for label, y_guess in zip(FOREST_LABELS, y_guesses):
        y0 = max(0, int(round(y_guess)) - 4)
        y1 = min(height, int(round(y_guess)) + 5)
        local = point_density[y0:y1, 190:590]
        local_y, local_x = np.unravel_index(int(np.argmax(local)), local.shape)
        center_y = y0 + local_y
        center_x = 190 + local_x

        row_support = dark[max(0, center_y - 1) : min(height, center_y + 2), 185:590].any(axis=0)
        row_support = ndimage.binary_closing(row_support, structure=np.ones(9, dtype=bool))
        runs = [(left + 185, right + 185) for left, right in contiguous_runs(row_support) if right - left + 1 >= 5]
        containing = [run for run in runs if run[0] <= center_x <= run[1]]
        if containing:
            ci_left, ci_right = max(containing, key=lambda run: run[1] - run[0])
        else:
            left_runs = [run for run in runs if run[1] < center_x]
            right_runs = [run for run in runs if run[0] > center_x]
            ci_left = max(left_runs, key=lambda run: run[1])[0] if left_runs else center_x
            ci_right = min(right_runs, key=lambda run: run[0])[1] if right_runs else center_x

        estimate = inverse_affine(center_x, 0.0, zero_px, 1.0, one_px)
        ci_low = inverse_affine(ci_left, 0.0, zero_px, 1.0, one_px)
        ci_high = inverse_affine(ci_right, 0.0, zero_px, 1.0, one_px)
        confidence = min(1.0, 0.55 + 0.15 * bool(containing) + 0.3 * min(1.0, (ci_right - ci_left) / 80.0))
        sampled = tuple(int(channel) for channel in rgb[center_y, center_x])
        observations.append(
            {
                "trait": label,
                "estimate": round(estimate, 5),
                "ci_low": round(min(ci_low, ci_high), 5),
                "ci_high": round(max(ci_low, ci_high), 5),
                "estimate_x_pixel": center_x,
                "row_y_pixel": center_y,
                "ci_left_pixel": ci_left,
                "ci_right_pixel": ci_right,
                "sampled_rgb": "#%02x%02x%02x" % sampled,
                "confidence": round(confidence, 3),
            }
        )
        draw.line((ci_left, center_y, ci_right, center_y), fill=(0, 190, 180), width=2)
        draw.ellipse((center_x - 5, center_y - 5, center_x + 5, center_y + 5), outline=(255, 76, 45), width=2)
        draw.line((ci_left, center_y - 4, ci_left, center_y + 4), fill=(0, 190, 180), width=2)
        draw.line((ci_right, center_y - 4, ci_right, center_y + 4), fill=(0, 190, 180), width=2)

    output_csv = case_dir / "data.csv"
    write_csv(output_csv, list(observations[0].keys()), observations)
    draw.rounded_rectangle((373, 415, 664, 446), radius=7, fill=(15, 23, 23))
    draw.text((384, 423), "29 point estimates + visible CI geometry", fill="white", font=font(12))
    overlay_path = case_dir / "overlay.png"
    overlay.save(overlay_path)

    fig, ax = plt.subplots(figsize=(8.7, 7.2))
    y_positions = np.arange(len(observations))[::-1]
    cmap = plt.get_cmap("magma")
    estimates = np.array([row["estimate"] for row in observations])
    for y, row in zip(y_positions, observations):
        low = row["estimate"] - row["ci_low"]
        high = row["ci_high"] - row["estimate"]
        estimate_span = max(1e-9, float(np.ptp(estimates)))
        color = cmap(np.clip((row["estimate"] - estimates.min()) / estimate_span, 0, 1))
        ax.errorbar(
            row["estimate"],
            y,
            xerr=np.array([[low], [high]]),
            fmt="o",
            markersize=7,
            color=color,
            markeredgecolor="#4d4d4d",
            ecolor="#242424",
            elinewidth=1.2,
            capsize=0,
        )
    ax.axvline(0, color="#303030", linestyle=(0, (4, 3)), linewidth=1.3)
    ax.axvline(1, color="#303030", linestyle=(0, (4, 3)), linewidth=1.3)
    ax.set_yticks(y_positions, FOREST_LABELS)
    ax.set_xlim(-0.05, 1.55)
    ax.set_xlabel("Cross-ancestry genetic correlation")
    ax.set_ylabel("Trait")
    ax.grid(axis="both", color="#e9e9e6", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.set_title("Recreated from visible forest-plot geometry", loc="left", fontsize=12)
    fig.tight_layout()
    recreation_path = case_dir / "recreated.png"
    save_figure(fig, recreation_path)

    report = {
        "schema_version": 1,
        "case_id": "nature-blood-forest",
        "status": "visible_geometry_extracted",
        "scope": "Full Fig. 2: 29 point estimates and horizontal confidence-interval geometry.",
        "original_sha256": sha256(original),
        "supplementary_workbook_sha256": sha256(case_dir / "source-data.xlsx"),
        "observations": len(observations),
        "calibration": {
            "x": [{"pixel": zero_px, "value": 0.0}, {"pixel": one_px, "value": 1.0}],
            "axis_type": "linear",
            "source": "visible dashed reference lines and labeled ticks",
        },
        "validation": {
            "complete_point_rows": sum(row["ci_right_pixel"] > row["ci_left_pixel"] for row in observations),
            "mean_geometry_confidence": round(float(np.mean([row["confidence"] for row in observations])), 3),
        },
        "source_mapping": {
            "status": "not_mapped_in_this_build",
            "reason": "The official 7.2 MB Supplementary Data 1-9 workbook is preserved and linked, but the current spreadsheet importer timed out before a defensible sheet-to-figure mapping was completed.",
        },
        "limitations": [
            "Confidence intervals are visible geometry; the report does not infer the statistical method beyond the article caption.",
            "JPEG antialiasing and overlapping gridlines limit endpoint precision.",
        ],
    }
    write_json(case_dir / "report.json", report)
    return report


def build_ribotie() -> dict:
    case_dir = CASES / "nature-ribotie-multipanel"
    original = case_dir / "original.jpg"
    image = Image.open(original).convert("RGB")
    rgb = np.asarray(image)
    crop_box = (254, 276, 501, 464)
    panel = image.crop(crop_box)
    panel_path = case_dir / "original-panel-e.png"
    panel.save(panel_path)
    panel_rgb = np.asarray(panel)
    local_height, local_width = panel_rgb.shape[:2]

    maximum = panel_rgb.max(axis=2)
    minimum = panel_rgb.min(axis=2)
    chroma = maximum - minimum
    mask = (chroma > 16) & (maximum < 250)
    valid = np.zeros_like(mask)
    valid[6:178, 66:246] = True
    mask &= valid
    labels, count = ndimage.label(mask)
    objects = ndimage.find_objects(labels)
    points = []
    for component_id, slices in enumerate(objects, start=1):
        if slices is None:
            continue
        y_slice, x_slice = slices
        component = labels[y_slice, x_slice] == component_id
        area = int(component.sum())
        box_width = x_slice.stop - x_slice.start
        box_height = y_slice.stop - y_slice.start
        if not (4 <= area <= 180 and 2 <= box_width <= 18 and 2 <= box_height <= 18):
            continue
        ys, xs = np.where(component)
        center_x = float(x_slice.start + xs.mean())
        center_y = float(y_slice.start + ys.mean())
        color_pixels = panel_rgb[y_slice, x_slice][component]
        color = tuple(int(channel) for channel in np.median(color_pixels, axis=0))
        points.append((center_x, center_y, color, area))

    points.sort(key=lambda item: (item[0], item[1]))
    observations = []
    for index, (x_pixel, y_pixel, color, area) in enumerate(points, start=1):
        global_x = crop_box[0] + x_pixel
        global_y = crop_box[1] + y_pixel
        reads_log10 = inverse_affine(global_x, 14.0, 339.0, 18.0, 489.0)
        pr_auc = inverse_affine(global_y, 0.0, 452.0, 0.10, 288.0)
        observations.append(
            {
                "point_id": index,
                "reads_log10": round(reads_log10, 5),
                "pr_auc": round(pr_auc, 6),
                "x_pixel": round(x_pixel, 3),
                "y_pixel": round(y_pixel, 3),
                "sampled_rgb": "#%02x%02x%02x" % color,
                "component_pixels": area,
            }
        )

    output_csv = case_dir / "data.csv"
    if not observations:
        raise RuntimeError("No visible colored point components were detected in RiboTIE Fig. 2e")
    write_csv(output_csv, list(observations[0].keys()), observations)

    overlay = panel.copy()
    draw = ImageDraw.Draw(overlay)
    for x_pixel, y_pixel, _, _ in points:
        draw.ellipse((x_pixel - 5, y_pixel - 5, x_pixel + 5, y_pixel + 5), outline=(0, 190, 180), width=2)
    draw.rounded_rectangle((7, 155, 239, 184), radius=7, fill=(15, 23, 23))
    draw.text((16, 163), f"{len(observations)} visible color components", fill="white", font=font(11))
    overlay_path = case_dir / "overlay.png"
    overlay.save(overlay_path)

    x_values = np.array([row["reads_log10"] for row in observations])
    y_values = np.array([row["pr_auc"] for row in observations])
    colors = [row["sampled_rgb"] for row in observations]
    fig, ax = plt.subplots(figsize=(6.6, 5.0))
    ax.scatter(x_values, y_values, c=colors, s=34, edgecolors="white", linewidths=0.45, alpha=0.95)
    if len(observations) >= 3:
        slope, intercept = np.polyfit(x_values, y_values, 1)
        x_line = np.linspace(13.5, 18.3, 120)
        ax.plot(x_line, intercept + slope * x_line, color="#232323", linewidth=1.4)
    ax.set(xlim=(13.5, 18.3), ylim=(-0.005, 0.108), xlabel="Reads (log₁₀)", ylabel="PR AUC")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color="#ece9e1", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.set_title("Panel e · pixel-extracted visible points", loc="left", fontsize=12)
    fig.tight_layout()
    recreation_path = case_dir / "recreated.png"
    save_figure(fig, recreation_path)

    report = {
        "schema_version": 1,
        "case_id": "nature-ribotie-multipanel",
        "status": "partial_visible_geometry",
        "scope": "Panel e only from a ten-panel mixed-chart figure; colored point components and a visual-fit line are reconstructed.",
        "original_sha256": sha256(original),
        "source_inventory_sha256": sha256(case_dir / "source-data.xlsx"),
        "panel_crop_px": {"left": crop_box[0], "top": crop_box[1], "right": crop_box[2], "bottom": crop_box[3]},
        "observations": len(observations),
        "calibration": {
            "x": [{"pixel": 339, "value": 14.0}, {"pixel": 489, "value": 18.0}],
            "y": [{"pixel": 452, "value": 0.0}, {"pixel": 288, "value": 0.10}],
            "axis_type": "linear",
        },
        "validation": {
            "article_caption_n": 73,
            "visible_color_components": len(observations),
            "coverage_vs_caption_n": round(len(observations) / 73.0, 3),
        },
        "limitations": [
            "Overlapping or JPEG-merged markers may form one connected component, so component count is not asserted as sample count.",
            "Only panel e is reconstructed; the full mixed figure remains a challenge case for panel segmentation and semantic routing.",
            "The fitted line is for visual reconstruction and is not claimed to reproduce the article's inferential model exactly.",
        ],
    }
    write_json(case_dir / "report.json", report)
    return report


def build_manifest(reports: dict[str, dict]) -> None:
    cases = [
        {
            "id": "nature-borneo-edge",
            "featured": True,
            "title": "边缘效应：散点、模型与重叠直方图",
            "eyebrow": "官方源数据闭环",
            "summary": "71 个森林样地来自 Supplementary Data 1：其中 50 个落在 Fig. 2a 的可见横轴范围，71 个全部进入 Fig. 2b；复现散点、模型曲线与双组直方图。",
            "journal": "Nature Communications",
            "year": 2017,
            "articleTitle": "Long-term carbon sink in Borneo’s forests halted by drought and vulnerable to edge effects",
            "authors": "Qie et al.",
            "figure": "Fig. 2",
            "doi": "10.1038/s41467-017-01997-0",
            "articleUrl": "https://www.nature.com/articles/s41467-017-01997-0",
            "figureUrl": "https://www.nature.com/articles/s41467-017-01997-0/figures/2",
            "license": "CC BY 4.0",
            "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
            "sourceType": "Nature Communications OA",
            "verification": "official_source_data_mapped",
            "verificationLabel": "官方数据逐行映射",
            "chartTypes": ["scatter", "segmented model", "overlapping histogram"],
            "scope": "完整 Fig. 2",
            "assets": {
                "original": "assets/cases/nature-borneo-edge/original.jpg",
                "overlay": "assets/cases/nature-borneo-edge/overlay.png",
                "recreated": "assets/cases/nature-borneo-edge/recreated.png",
                "data": "assets/cases/nature-borneo-edge/data.csv",
                "report": "assets/cases/nature-borneo-edge/report.json",
                "sourceData": "assets/cases/nature-borneo-edge/source-data.xlsx",
            },
            "metrics": [
                {"label": "直方图样本", "value": str(reports["nature-borneo-edge"]["source_rows"])},
                {"label": "可见散点", "value": str(reports["nature-borneo-edge"]["panel_a_visible_rows"])},
                {"label": "验证等级", "value": "Source-mapped"},
            ],
        },
        {
            "id": "nature-blood-forest",
            "featured": True,
            "title": "29 项血液指标的森林图",
            "eyebrow": "复杂误差线几何",
            "summary": "自动恢复每项指标的点估计与可见 95% CI 端点；保留官方 Supplementary Data 1–9，但本轮不把未完成的表格映射冒充数值真值。",
            "journal": "Nature Communications",
            "year": 2024,
            "articleTitle": "Genetic architecture of routinely acquired blood tests in a British South Asian cohort",
            "authors": "Jacobs et al.",
            "figure": "Fig. 2",
            "doi": "10.1038/s41467-024-53091-x",
            "articleUrl": "https://www.nature.com/articles/s41467-024-53091-x",
            "figureUrl": "https://www.nature.com/articles/s41467-024-53091-x/figures/2",
            "license": "CC BY 4.0",
            "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
            "sourceType": "Nature Communications OA",
            "verification": "visible_geometry_extracted",
            "verificationLabel": "像素几何验证",
            "chartTypes": ["forest plot", "confidence interval", "color scale"],
            "scope": "完整 Fig. 2",
            "assets": {
                "original": "assets/cases/nature-blood-forest/original.jpg",
                "overlay": "assets/cases/nature-blood-forest/overlay.png",
                "recreated": "assets/cases/nature-blood-forest/recreated.png",
                "data": "assets/cases/nature-blood-forest/data.csv",
                "report": "assets/cases/nature-blood-forest/report.json",
                "sourceData": "assets/cases/nature-blood-forest/source-data.xlsx",
            },
            "metrics": [
                {"label": "指标行", "value": str(reports["nature-blood-forest"]["observations"])},
                {"label": "完整 CI", "value": str(reports["nature-blood-forest"]["validation"]["complete_point_rows"])},
                {"label": "验证等级", "value": "Geometry"},
            ],
        },
        {
            "id": "nature-ribotie-multipanel",
            "featured": True,
            "title": "十面板混合图中的局部路由",
            "eyebrow": "复杂多面板挑战",
            "summary": "从同时含箱线图、柱图、环图、散点图、火山图和直方图的 Fig. 2 中定位 panel e，并恢复低分辨率彩色散点的可见组件。",
            "journal": "Nature Communications",
            "year": 2025,
            "articleTitle": "Deep learning to decode sites of RNA translation in normal and cancerous tissues",
            "authors": "Clauwaert et al.",
            "figure": "Fig. 2 · panel e",
            "doi": "10.1038/s41467-025-56543-0",
            "articleUrl": "https://www.nature.com/articles/s41467-025-56543-0",
            "figureUrl": "https://www.nature.com/articles/s41467-025-56543-0/figures/2",
            "license": "CC BY 4.0",
            "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
            "sourceType": "Nature Communications OA",
            "verification": "partial_visible_geometry",
            "verificationLabel": "局部几何 / 不过度声称",
            "chartTypes": ["multi-panel", "colored scatter", "panel routing"],
            "scope": "panel e；完整原图保留",
            "assets": {
                "original": "assets/cases/nature-ribotie-multipanel/original.jpg",
                "panelOriginal": "assets/cases/nature-ribotie-multipanel/original-panel-e.png",
                "overlay": "assets/cases/nature-ribotie-multipanel/overlay.png",
                "recreated": "assets/cases/nature-ribotie-multipanel/recreated.png",
                "data": "assets/cases/nature-ribotie-multipanel/data.csv",
                "report": "assets/cases/nature-ribotie-multipanel/report.json",
                "sourceData": "assets/cases/nature-ribotie-multipanel/source-data.xlsx",
            },
            "metrics": [
                {"label": "可见色块", "value": str(reports["nature-ribotie-multipanel"]["observations"])},
                {"label": "图注 n", "value": "73"},
                {"label": "验证等级", "value": "Partial"},
            ],
        },
    ]
    payload = {
        "schemaVersion": 1,
        "generated": "2026-07-20",
        "title": "thu-digitizer OA Figure Gallery",
        "cases": cases,
        "challengeQueue": [
            {
                "id": "nature-nanopore-scatter",
                "title": "对数坐标散点＋边际直方图＋事件轨迹",
                "journal": "Nature Communications",
                "year": 2019,
                "figure": "Fig. 2",
                "articleUrl": "https://www.nature.com/articles/s41467-018-07924-1",
                "image": "assets/cases/nature-nanopore-scatter/original.jpg",
                "status": "challenge_queued",
                "note": "69.8 MB Source Data 已定位；待建立对数轴、密集重叠点与波形面板的联合证据链。",
            }
        ],
    }
    write_json(DATA_DIR / "cases.json", payload)


def main() -> None:
    reports = {
        "nature-borneo-edge": build_borneo(),
        "nature-blood-forest": build_forest(),
        "nature-ribotie-multipanel": build_ribotie(),
    }
    build_manifest(reports)
    print("gallery evidence built")
    for case_id, report in reports.items():
        print(f"{case_id}: {report['status']}")


if __name__ == "__main__":
    main()

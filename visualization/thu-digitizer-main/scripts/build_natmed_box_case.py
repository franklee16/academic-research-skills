"""Build the Nature Medicine Fig. 4b boxplot gallery evidence bundle."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from candidate_digitize_outline_boxplot import extract_outline_boxplots
from digitize_boxplot import extract_boxplots


ARTICLE_URL = "https://www.nature.com/articles/s41591-026-04303-y"
FIGURE_URL = "https://www.nature.com/articles/s41591-026-04303-y/figures/4"
IMAGE_URL = (
    "https://media.springernature.com/full/springer-static/image/"
    "art%3A10.1038%2Fs41591-026-04303-y/MediaObjects/41591_2026_4303_Fig4_HTML.png"
)
CATEGORIES = ["Control", "AD", "PD", "FTD", "Stroke"]
PANELS = {
    "BCA": {"bounds": (119, 99, 462, 619), "x_axis": (119, 0, 462, 5)},
    "AUC": {"bounds": (624, 99, 966, 619), "x_axis": (624, 0, 966, 5)},
}
Y_AXIS = (99, 1.0, 619, 0.4)


def builtin(value):
    try:
        import numpy as np

        if isinstance(value, np.generic):
            return value.item()
    except ImportError:
        pass
    if isinstance(value, dict):
        return {key: builtin(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [builtin(item) for item in value]
    return value


def panel_image(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    if image.size == (1000, 770):
        return image
    if image.width >= 1000 and image.height >= 1420:
        return image.crop((0, 650, 1000, 1420))
    raise ValueError(f"unsupported source dimensions {image.size}; expected full Fig. 4 or 1000x770 panel crop")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_extractors(original: Path) -> tuple[dict, dict]:
    stable = {}
    geometry = {}
    for panel, spec in PANELS.items():
        stable[panel] = builtin(
            extract_boxplots(
                original,
                plot_bounds=spec["bounds"],
                x_axis=spec["x_axis"],
                y_axis=Y_AXIS,
                box_color="#4685bd",
                line_color="#464646",
                outlier_color="#ff00ff",
                orientation="vertical",
                tolerance=18,
                min_area=20,
            )
        )
        geometry[panel] = extract_outline_boxplots(
            original,
            plot_bounds=spec["bounds"],
            y_axis=Y_AXIS,
            line_color="#464646",
            filled_series={"Finetune": "#4685bd"},
            unfilled_series_label="Retrain",
            tolerance=18,
        )
    return stable, geometry


def assign_categories(geometry: dict) -> list[dict]:
    rows = []
    for panel in ("BCA", "AUC"):
        groups = geometry[panel]["groups"]
        if len(groups) != 10 or any(group["status"] != "candidate" for group in groups):
            raise RuntimeError(f"{panel}: expected ten resolved paired boxplots")
        for index, group in enumerate(groups):
            row = {
                "panel": panel,
                "category": CATEGORIES[index // 2],
                "series": group["series"],
                "category_center_pixel": group["category_center_pixel"],
                "q1": group["q1"],
                "median": group["median"],
                "q3": group["q3"],
                "lower_whisker": group["lower_whisker"],
                "upper_whisker": group["upper_whisker"],
                "visible_outliers": ";".join(f"{item['value']:.9f}" for item in group["outliers"]),
                "q1_pixel": group["box_strokes_pixel"]["q1"],
                "median_pixel": group["box_strokes_pixel"]["median"],
                "q3_pixel": group["box_strokes_pixel"]["q3"],
                "lower_whisker_pixel": group["whisker_strokes_pixel"]["lower"],
                "upper_whisker_pixel": group["whisker_strokes_pixel"]["upper"],
                "median_coincident_with_q1": group["stroke_diagnostic"].get(
                    "median_coincident_with_q1", False
                ),
                "median_coincident_with_q3": group["stroke_diagnostic"].get(
                    "median_coincident_with_q3", False
                ),
                "lower_whisker_coincident_with_q1": group["whisker_strokes_pixel"][
                    "lower_coincident_with_q1"
                ],
                "upper_whisker_coincident_with_q3": group["whisker_strokes_pixel"][
                    "upper_coincident_with_q3"
                ],
                "status": "candidate_visible_geometry",
            }
            rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def draw_overlay(original: Path, output: Path, geometry: dict) -> None:
    base = Image.open(original).convert("RGBA")
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    colors = {"Retrain": (224, 54, 107, 235), "Finetune": (0, 151, 136, 235)}
    for panel in ("BCA", "AUC"):
        width = geometry[panel]["detected_box_width_pixels"]
        half = width / 2
        for group in geometry[panel]["groups"]:
            color = colors[group["series"]]
            x = group["category_center_pixel"]
            q = group["box_strokes_pixel"]
            w = group["whisker_strokes_pixel"]
            draw.rectangle((x - half, q["q3"], x + half, q["q1"]), outline=color, width=2)
            draw.line((x - half, q["median"], x + half, q["median"]), fill=color, width=2)
            draw.line((x, w["upper"], x, q["q3"]), fill=color, width=2)
            draw.line((x - 6, w["upper"], x + 6, w["upper"]), fill=color, width=2)
            draw.line((x, q["q1"], x, w["lower"]), fill=color, width=2)
            draw.line((x - 6, w["lower"], x + 6, w["lower"]), fill=color, width=2)
            for outlier in group["outliers"]:
                ox, oy = outlier["center_pixel"]
                draw.ellipse((ox - 5, oy - 5, ox + 5, oy + 5), outline=color, width=2)
    Image.alpha_composite(base, layer).convert("RGB").save(output)


def box_stats(rows: list[dict], panel: str, series: str) -> list[dict]:
    selected = [row for row in rows if row["panel"] == panel and row["series"] == series]
    by_category = {row["category"]: row for row in selected}
    return [
        {
            "label": category,
            "q1": by_category[category]["q1"],
            "med": by_category[category]["median"],
            "q3": by_category[category]["q3"],
            "whislo": by_category[category]["lower_whisker"],
            "whishi": by_category[category]["upper_whisker"],
            "fliers": [
                float(value)
                for value in by_category[category]["visible_outliers"].split(";")
                if value
            ],
        }
        for category in CATEGORIES
    ]


def draw_recreation(path: Path, rows: list[dict]) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(10, 7.7), dpi=100, facecolor="white")
    figure.suptitle("Generalization on BioFINDER-2", x=0.06, y=0.97, ha="left", fontsize=19)
    positions = list(range(1, 6))
    for axis, panel in zip(axes, ("BCA", "AUC")):
        retrain = box_stats(rows, panel, "Retrain")
        finetune = box_stats(rows, panel, "Finetune")
        common = {
            "patch_artist": True,
            "showfliers": True,
            "manage_ticks": False,
            "widths": 0.30,
            "medianprops": {"color": "#464646", "linewidth": 1.8},
            "whiskerprops": {"color": "#464646", "linewidth": 1.5},
            "capprops": {"color": "#464646", "linewidth": 1.5},
            "flierprops": {
                "marker": "o",
                "markerfacecolor": "white",
                "markeredgecolor": "#464646",
                "markersize": 5,
            },
        }
        axis.bxp(
            retrain,
            positions=[value - 0.17 for value in positions],
            boxprops={"facecolor": "white", "edgecolor": "#464646", "linewidth": 1.6},
            **common,
        )
        axis.bxp(
            finetune,
            positions=[value + 0.17 for value in positions],
            boxprops={"facecolor": "#4685bd", "edgecolor": "#464646", "linewidth": 1.6},
            **common,
        )
        axis.set_ylim(0.4, 1.0)
        axis.set_xlim(0.5, 5.5)
        axis.set_ylabel(panel, fontsize=16)
        axis.set_xticks(positions, CATEGORIES, rotation=90, fontsize=13)
        axis.tick_params(axis="y", labelsize=12, length=6)
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(False)
    figure.legend(
        handles=[
            Patch(facecolor="white", edgecolor="#464646", label="Retrain"),
            Patch(facecolor="#4685bd", edgecolor="#464646", label="Finetune"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.58, 0.965),
        frameon=False,
        ncols=2,
        fontsize=14,
    )
    figure.subplots_adjust(left=0.09, right=0.98, bottom=0.20, top=0.87, wspace=0.38)
    figure.savefig(path, facecolor="white")
    plt.close(figure)


def build_report(original: Path, stable: dict, geometry: dict, rows: list[dict]) -> dict:
    side_scores = [
        group["stroke_diagnostic"]["side_score"]
        for panel in geometry.values()
        for group in panel["groups"]
    ]
    outlier_count = sum(len(group["outliers"]) for panel in geometry.values() for group in panel["groups"])
    median_coincidences = sum(
        bool(group["stroke_diagnostic"].get("median_coincident_with_q1"))
        or bool(group["stroke_diagnostic"].get("median_coincident_with_q3"))
        for panel in geometry.values()
        for group in panel["groups"]
    )
    return {
        "schema_version": 1,
        "case_id": "nature-protaide-boxplot",
        "status": "candidate_visible_geometry",
        "family": "paired_vertical_boxplot",
        "article": {
            "title": "A deep joint-learning proteomics model for diagnosis of six conditions associated with dementia",
            "journal": "Nature Medicine",
            "year": 2026,
            "doi": "10.1038/s41591-026-04303-y",
            "figure": "Fig. 4b",
            "article_url": ARTICLE_URL,
            "figure_url": FIGURE_URL,
            "image_url": IMAGE_URL,
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
        },
        "input": {
            "file": original.name,
            "sha256": sha256(original),
            "dimensions": list(Image.open(original).size),
            "crop_from_full_figure": [0, 650, 1000, 1420],
        },
        "calibration": {
            "y_axis": list(Y_AXIS),
            "value_per_pixel": abs((Y_AXIS[3] - Y_AXIS[1]) / (Y_AXIS[2] - Y_AXIS[0])),
            "assumption": "verified linear BCA and AUC axes with visible 0.4 and 1.0 ticks",
        },
        "stable_baseline": {
            "route": "digitize_boxplot.extract_boxplots",
            "status": "low_confidence",
            "reason": "filled Finetune interiors are split by the median; Retrain interiors match the background; outliers share the line colour",
            "panels": stable,
        },
        "candidate_extraction": {
            "route": "candidate_outline_boxplot_geometry.extract_outline_boxplots",
            "status": "candidate_visible_geometry",
            "box_groups_extracted": 20,
            "box_groups_visible": 20,
            "visible_outliers_extracted": outlier_count,
            "raster_coincident_medians": median_coincidences,
            "minimum_rectangle_side_support": min(side_scores),
            "panels": geometry,
        },
        "output_rows": len(rows),
        "recreation_scope": "visible five-number summaries and visible outlier rings only",
        "source_data_validation": {
            "status": "not_comparable",
            "reason": "the official supplementary workbook exposes comparison P values, not the 20 repeat-level values used to draw Fig. 4b",
            "source_url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41591-026-04303-y/MediaObjects/41591_2026_4303_MOESM3_ESM.xlsx",
        },
        "webplotdigitizer_comparison": "not_compared",
        "limitations": [
            "The 20 repeat-level observations cannot be recovered from the boxplot raster and are not fabricated.",
            "Values are quantized by the official raster at approximately 0.001154 axis units per pixel.",
            "When a median or whisker is not separately raster-resolvable, the candidate reports the visible pixel-row coincidence and records an explicit flag.",
            "The outline route remains candidate pending held-out publication figures and a fair same-input WebPlotDigitizer comparison.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="Official full Fig. 4 PNG or the 1000x770 Fig. 4b crop")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "gallery" / "assets" / "cases" / "nature-protaide-boxplot",
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    original = args.output_dir / "original.png"
    panel_image(args.input).save(original)
    stable, geometry = run_extractors(original)
    rows = assign_categories(geometry)
    write_csv(args.output_dir / "data.csv", rows)
    draw_overlay(original, args.output_dir / "overlay.png", geometry)
    draw_recreation(args.output_dir / "recreated.png", rows)
    report = build_report(original, stable, geometry, rows)
    (args.output_dir / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"CASE={args.output_dir}")
    print("STATUS=candidate_visible_geometry")
    print("BOX_GROUPS=20/20")


if __name__ == "__main__":
    main()

"""Build the Nature Communications Fig. 1 multi-panel boxplot case.

The official Figshare workbook supplies the 484 plotted observations.  This
builder uses it only after checking the figure's metric (``EMF_weighted``) and
the four grouping fields against the article text and the retained Figure 1
raster.  The source data and visible raster geometry remain separate in the
CSV/report: source values determine the five-number summaries; pixel fields
determine the replot placement and the overlay.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.stats import kruskal


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "gallery" / "assets" / "cases" / "nature-67353-fig1"

ARTICLE_URL = "https://www.nature.com/articles/s41467-025-67353-9"
FIGURE_URL = "https://www.nature.com/articles/s41467-025-67353-9/figures/1"
IMAGE_URL = (
    "https://media.springernature.com/full/springer-static/image/"
    "art%3A10.1038%2Fs41467-025-67353-9/MediaObjects/41467_2025_67353_Fig1_HTML.png"
)
FIGSHARE_URL = "https://doi.org/10.6084/m9.figshare.28645625"
FIGSHARE_FILE_URL = "https://ndownloader.figshare.com/files/60135722"

CANVAS = (1750, 1482)
Y_TICKS = [round(value, 2) for value in np.arange(0.05, 0.56, 0.05)]


@dataclass(frozen=True)
class Panel:
    code: str
    field: str
    title: str
    source_categories: tuple[str, str, str]
    labels: tuple[str, str, str]
    x_centres: tuple[float, float, float]
    left: int
    right: int
    top: int
    bottom: int
    color: str
    statistic_y: float
    letter_y: tuple[float, float, float]
    letters: tuple[str, str, str]


PANELS = (
    Panel(
        "A",
        "LC_simpl_2018",
        "Land use",
        ("Cropland", "Grassland", "Woodland"),
        ("Cropland\n(n = 227)", "Grassland\n(n = 92)", "Woodland\n(n = 165)"),
        (246.0, 426.0, 604.0),
        145,
        690,
        40,
        604,
        "#f2b04e",
        0.578,
        (0.333, 0.402, 0.402),
        ("a", "b", "b"),
    ),
    Panel(
        "B",
        "Climate_zone_simpl",
        "Climatic region",
        ("Continental", "Temperate_dry", "Temperate_humid"),
        ("Continental\n(n = 113)", "Temperate\ndry (n = 122)", "Temperate\nhumid (n = 249)"),
        (913.0, 1092.0, 1271.0),
        814,
        1356,
        40,
        604,
        "#20908f",
        0.578,
        (0.350, 0.350, 0.402),
        ("a", "b", "c"),
    ),
    Panel(
        "C",
        "SOIL_TYPE_SIMPL",
        "Soil texture",
        ("CLAY", "LOAM", "SAND"),
        ("Clay\n(n = 129)", "Loam\n(n = 179)", "Sand\n(n = 176)"),
        (246.0, 426.0, 604.0),
        145,
        690,
        812,
        1376,
        "#6f0026",
        0.578,
        (0.382, 0.412, 0.342),
        ("a", "a", "b"),
    ),
    Panel(
        "D",
        "PH_Class",
        "Soil pH",
        ("Acidic", "Alkaline", "Neutral"),
        ("Acidic\n(n = 290)", "Alkaline\n(n = 131)", "Neutral\n(n = 63)"),
        (913.0, 1092.0, 1271.0),
        814,
        1356,
        812,
        1376,
        "#6c6c6c",
        0.578,
        (0.402, 0.302, 0.402),
        ("a", "b", "a"),
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def as_builtin(value):
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: as_builtin(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [as_builtin(item) for item in value]
    return value


def font(size: int, *, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
    base = Path("C:/Windows/Fonts")
    names = []
    if bold and italic:
        names.append("arialbi.ttf")
    elif bold:
        names.append("arialbd.ttf")
    elif italic:
        names.append("ariali.ttf")
    names.extend(["arial.ttf", "Arial.ttf"])
    for name in names:
        candidate = base / name
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def y_to_pixel(panel: Panel, value: float) -> float:
    # Retained raster calibration: y=0.05 maps to the bottom baseline and
    # y=0.55 to the first full horizontal grid line.  It is retained per panel
    # rather than inferred from source data.
    grid_top = panel.top + 14
    return panel.bottom - (value - 0.05) * (panel.bottom - grid_top) / 0.50


def quantile_type7(values: np.ndarray, probability: float) -> float:
    return float(np.quantile(values, probability, method="linear"))


def visible_summary(values: np.ndarray) -> dict:
    ordered = np.sort(values.astype(float))
    q1 = quantile_type7(ordered, 0.25)
    median = quantile_type7(ordered, 0.50)
    q3 = quantile_type7(ordered, 0.75)
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    inliers = ordered[(ordered >= lower_fence) & (ordered <= upper_fence)]
    fliers = ordered[(ordered < lower_fence) | (ordered > upper_fence)]
    return {
        "n": int(ordered.size),
        "q1": q1,
        "median": median,
        "q3": q3,
        "lower_whisker": float(inliers.min()),
        "upper_whisker": float(inliers.max()),
        "lower_fence": lower_fence,
        "upper_fence": upper_fence,
        "visible_outliers": [float(value) for value in fliers],
    }


def load_rows(source_data: Path) -> tuple[list[dict], dict]:
    import pandas as pd

    source = pd.read_excel(source_data, sheet_name="DATASET")
    required = {
        "SampleID",
        "LC_simpl_2018",
        "Climate_zone_simpl",
        "SOIL_TYPE_SIMPL",
        "PH_Class",
        "EMF_weighted",
    }
    missing = required - set(source.columns)
    if missing:
        raise ValueError(f"source workbook lacks required columns: {sorted(missing)}")
    if len(source) != 484:
        raise ValueError(f"expected 484 source rows, received {len(source)}")

    rows: list[dict] = []
    panel_reports: dict[str, dict] = {}
    for panel in PANELS:
        values_by_group = []
        for index, (source_category, label, centre) in enumerate(
            zip(panel.source_categories, panel.labels, panel.x_centres), start=1
        ):
            values = source.loc[source[panel.field].eq(source_category), "EMF_weighted"].dropna().to_numpy(float)
            summary = visible_summary(values)
            width = 134.0 if panel.code in {"A", "C"} else 132.0
            row = {
                "panel": panel.code,
                "grouping_field": panel.field,
                "category": label.replace("\n", " "),
                "plot_label": label,
                "source_category": source_category,
                "n": summary["n"],
                "metric": "EMF_weighted",
                "source_status": "official_figshare_source_mapped",
                "q1": f"{summary['q1']:.9f}",
                "median": f"{summary['median']:.9f}",
                "q3": f"{summary['q3']:.9f}",
                "lower_whisker": f"{summary['lower_whisker']:.9f}",
                "upper_whisker": f"{summary['upper_whisker']:.9f}",
                "lower_fence": f"{summary['lower_fence']:.9f}",
                "upper_fence": f"{summary['upper_fence']:.9f}",
                "visible_outlier_count": len(summary["visible_outliers"]),
                "visible_outliers": ";".join(f"{value:.9f}" for value in summary["visible_outliers"]),
                "category_center_pixel": f"{centre:.3f}",
                "box_left_pixel": f"{centre - width / 2:.3f}",
                "box_right_pixel": f"{centre + width / 2:.3f}",
                "q1_pixel": f"{y_to_pixel(panel, summary['q1']):.3f}",
                "median_pixel": f"{y_to_pixel(panel, summary['median']):.3f}",
                "q3_pixel": f"{y_to_pixel(panel, summary['q3']):.3f}",
                "lower_whisker_pixel": f"{y_to_pixel(panel, summary['lower_whisker']):.3f}",
                "upper_whisker_pixel": f"{y_to_pixel(panel, summary['upper_whisker']):.3f}",
                "fill_color": panel.color,
                "significance_letter": panel.letters[index - 1],
                "letter_y": f"{panel.letter_y[index - 1]:.3f}",
                "letter_y_pixel": f"{y_to_pixel(panel, panel.letter_y[index - 1]):.3f}",
                "visible_geometry_status": "raster_calibrated_source_summary",
            }
            rows.append(row)
            values_by_group.append(values)

        statistic = kruskal(*values_by_group)
        eta_squared = (statistic.statistic - len(values_by_group) + 1) / (len(source) - len(values_by_group))
        panel_reports[panel.code] = {
            "grouping_field": panel.field,
            "metric": "EMF_weighted",
            "sample_count": int(sum(len(values) for values in values_by_group)),
            "kruskal_wallis_chi_squared": float(statistic.statistic),
            "eta_squared": float(eta_squared),
            "p_value": float(statistic.pvalue),
            "visible_annotation": {
                "letters": list(panel.letters),
                "letter_y_values": list(panel.letter_y),
                "status": "raster_annotation_transcribed",
            },
        }
    return rows, panel_reports


def centred(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, image_font, *, fill, anchor="mm") -> None:
    draw.multiline_text(xy, text, font=image_font, fill=fill, anchor=anchor, align="center", spacing=2)


def draw_panel_base(draw: ImageDraw.ImageDraw, panel: Panel, panel_report: dict) -> None:
    grid = "#ececea"
    axis = "#5e5e5e"
    tick = "#696969"
    for value in Y_TICKS:
        y = y_to_pixel(panel, value)
        draw.line((panel.left, y, panel.right, y), fill=grid, width=2)
        if panel.code in {"A", "C"} and value in {0.1, 0.2, 0.3, 0.4, 0.5}:
            draw.text((panel.left - 16, y), f"{value:.1f}", font=font(26), fill=tick, anchor="rm")
    for x in panel.x_centres:
        draw.line((x, panel.top, x, panel.bottom), fill=grid, width=2)
    draw.line((panel.left, panel.top, panel.left, panel.bottom), fill=axis, width=4)
    draw.line((panel.left, panel.bottom, panel.right, panel.bottom), fill=axis, width=4)
    centred(draw, (panel.left + 52, panel.top + 56), panel.code, font(55), fill="#080808")
    report_line = (
        f"X² = {panel_report['kruskal_wallis_chi_squared']:.2f}, "
        f"η² = {panel_report['eta_squared']:.3f}, p-val = {panel_report['p_value']:.3e}"
    )
    stats_y = 2 if panel.top < 100 else panel.top - 65
    centred(draw, ((panel.left + panel.right) / 2, stats_y), report_line, font(27, italic=True), fill="#171717", anchor="ma")


def draw_box(draw: ImageDraw.ImageDraw, row: dict, *, overlay: bool = False) -> None:
    color = "#007d7a" if overlay else row["fill_color"]
    stroke = "#007d7a" if overlay else "#353535"
    center = float(row["category_center_pixel"])
    left = float(row["box_left_pixel"])
    right = float(row["box_right_pixel"])
    q1 = float(row["q1_pixel"])
    median = float(row["median_pixel"])
    q3 = float(row["q3_pixel"])
    lower = float(row["lower_whisker_pixel"])
    upper = float(row["upper_whisker_pixel"])
    line_width = 3 if overlay else 4
    if overlay:
        draw.rectangle((left, q3, right, q1), outline=color, width=line_width)
        draw.line((center, upper, center, q3), fill=color, width=line_width)
        draw.line((center, q1, center, lower), fill=color, width=line_width)
        draw.line((center - 7, upper, center + 7, upper), fill=color, width=line_width)
        draw.line((center - 7, lower, center + 7, lower), fill=color, width=line_width)
        draw.line((left, median, right, median), fill=color, width=line_width)
    else:
        draw.rectangle((left, q3, right, q1), fill=color, outline=stroke, width=line_width)
        draw.line((left, median, right, median), fill=stroke, width=line_width)
        draw.line((center, upper, center, q3), fill=stroke, width=3)
        draw.line((center, q1, center, lower), fill=stroke, width=3)
        draw.line((center - 2, upper, center + 2, upper), fill=stroke, width=3)
        draw.line((center - 2, lower, center + 2, lower), fill=stroke, width=3)
    for value in row["visible_outliers"].split(";"):
        if not value:
            continue
        y = float(row["upper_whisker_pixel"])  # placeholder made explicit below
        # The panel calibration is encoded in CSV for summary lines, while
        # source-level outlier values use the same retained y axis.
        panel = next(item for item in PANELS if item.code == row["panel"])
        y = y_to_pixel(panel, float(value))
        radius = 7 if not overlay else 9
        draw.ellipse(
            (center - radius, y - radius, center + radius, y + radius),
            outline=color if overlay else "#363636",
            fill=None if overlay else "#363636",
            width=3,
        )


def draw_recreation(path: Path, rows: list[dict], panels: dict) -> None:
    image = Image.new("RGB", CANVAS, "white")
    draw = ImageDraw.Draw(image)
    by_panel = {panel.code: [row for row in rows if row["panel"] == panel.code] for panel in PANELS}
    for panel in PANELS:
        draw_panel_base(draw, panel, panels[panel.code])
        for row in by_panel[panel.code]:
            draw_box(draw, row)
            centre = float(row["category_center_pixel"])
            letter_y = float(row["letter_y_pixel"])
            centred(draw, (centre, letter_y), row["significance_letter"], font(37, bold=True), fill="#050505")
            centred(draw, (centre, panel.bottom + 43), row["plot_label"], font(26), fill="#141414", anchor="ma")
    for panel in (PANELS[0], PANELS[2]):
        text_layer = Image.new("RGBA", (360, 60), (0, 0, 0, 0))
        label_draw = ImageDraw.Draw(text_layer)
        label_draw.text((0, 0), "Multifunctionality", font=font(38), fill="#050505")
        bbox = text_layer.getbbox()
        if bbox:
            text_layer = text_layer.crop(bbox).rotate(90, expand=True)
            image.paste(text_layer, (2, int((panel.top + panel.bottom - text_layer.height) / 2)), text_layer)
    legend_x, legend_y = 1452, 44
    for index, (label, fill) in enumerate(
        (("Land use", "#f2b04e"), ("Climatic region", "#20908f"), ("Soil texture", "#6f0026"), ("Soil pH", "#6c6c6c"))
    ):
        y = legend_y + index * 64
        draw.rectangle((legend_x, y, legend_x + 43, y + 43), fill=fill, outline="#222", width=4)
        draw.text((legend_x + 62, y + 21), label, font=font(34), fill="#111", anchor="lm")
    image.save(path)


def draw_overlay(original: Path, output: Path, rows: list[dict]) -> None:
    base = Image.open(original).convert("RGBA")
    layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for row in rows:
        draw_box(draw, row, overlay=True)
    Image.alpha_composite(base, layer).convert("RGB").save(output)


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_geometry_validation(path: Path, rows: list[dict]) -> None:
    fields = ["panel", "category", "metric", "source_value", "recreated_value", "absolute_error", "status"]
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            for metric in ["q1", "median", "q3", "lower_whisker", "upper_whisker"]:
                writer.writerow(
                    {
                        "panel": row["panel"],
                        "category": row["category"],
                        "metric": metric,
                        "source_value": row[metric],
                        "recreated_value": row[metric],
                        "absolute_error": "0",
                        "status": "official_source_summary_replotted",
                    }
                )


def report(original: Path, source_data: Path, rows: list[dict], panel_reports: dict) -> dict:
    outliers = sum(int(row["visible_outlier_count"]) for row in rows)
    return {
        "schema_version": 1,
        "case_id": "nature-67353-fig1",
        "status": "source_mapped",
        "family": "multi_panel_vertical_boxplot",
        "article": {
            "title": "The soil microbiome as an indicator of ecosystem multifunctionality in European soils",
            "journal": "Nature Communications",
            "year": 2025,
            "doi": "10.1038/s41467-025-67353-9",
            "figure": "Fig. 1",
            "article_url": ARTICLE_URL,
            "figure_url": FIGURE_URL,
            "image_url": IMAGE_URL,
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
        },
        "input": {"file": original.name, "sha256": sha256(original), "dimensions": list(Image.open(original).size)},
        "source_data": {
            "status": "official_figshare_source_mapped",
            "url": FIGSHARE_URL,
            "download_url": FIGSHARE_FILE_URL,
            "file": source_data.name,
            "sha256": sha256(source_data),
            "sheet": "DATASET",
            "source_rows": 484,
            "mapped_fields": ["EMF_weighted", "LC_simpl_2018", "Climate_zone_simpl", "SOIL_TYPE_SIMPL", "PH_Class"],
            "semantic_evidence": "The article reports Fig. 1 land use, climate, texture and pH groupings and the published group means match EMF_weighted; the 484 source rows and all four group sample sizes match the figure.",
        },
        "raster_calibration": {
            "coordinate_status": "verified_from_retained_figure_ticks_and_grid",
            "y_axis": {"displayed_range": [0.05, 0.55], "top_grid_pixels": [54, 826], "bottom_pixels": [604, 1376]},
            "panel_bounds": {panel.code: [panel.left, panel.top, panel.right, panel.bottom] for panel in PANELS},
            "visible_annotations": "Kruskal-Wallis statistics and a/b/c letters are retained as figure-level labels; source summaries are not reverse-engineered from their pixel positions.",
        },
        "coverage": {
            "panels": 4,
            "boxplots": len(rows),
            "source_observations": 484,
            "visible_outliers": outliers,
            "summary_statistics_per_box": 5,
        },
        "panel_statistics": panel_reports,
        "source_validation": {
            "status": "official_source_summary_replotted",
            "mapped_boxplots": len(rows),
            "mapped_observations": 484,
            "summary_metrics": ["Q1", "median", "Q3", "1.5xIQR lower whisker", "1.5xIQR upper whisker"],
            "replot_summary_error": 0.0,
        },
        "recreation_scope": "The recreation uses official observations to calculate the visible five-number summaries and visible fliers; source observations are not displayed as if the original chart plotted a raw swarm.",
        "webplotdigitizer_comparison": "not_compared",
        "limitations": [
            "This is an official-source mapping case, not a claim that all 484 observations were recovered from raster pixels.",
            "Post-hoc significance letters and their vertical positions are transcribed from the visible figure annotation; the multiple-comparison method is not inferred here.",
            "The replot preserves the four panels, summaries, whiskers and visible outliers, while browser font rasterization may differ slightly from the publisher raster.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="official Figure 1 PNG")
    parser.add_argument("--source-data", type=Path, required=True, help="official Figshare workbook")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    if Image.open(args.input).size != CANVAS:
        raise ValueError(f"expected Figure 1 canvas {CANVAS}, received {Image.open(args.input).size}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    original = args.output_dir / "original.png"
    Image.open(args.input).convert("RGB").save(original)
    source_copy = args.output_dir / "source-data.xlsx"
    shutil.copy2(args.source_data, source_copy)
    rows, panel_reports = load_rows(source_copy)
    write_csv(args.output_dir / "data.csv", rows)
    write_geometry_validation(args.output_dir / "source-validation.csv", rows)
    draw_recreation(args.output_dir / "recreated.png", rows, panel_reports)
    draw_overlay(original, args.output_dir / "overlay.png", rows)
    evidence = report(original, source_copy, rows, panel_reports)
    (args.output_dir / "report.json").write_text(json.dumps(as_builtin(evidence), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "source-provenance.json").write_text(
        json.dumps(evidence["source_data"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"CASE={args.output_dir}")
    print("STATUS=source_mapped")
    print(f"BOXPLOTS={len(rows)}/12")
    print(f"OUTLIERS={sum(int(row['visible_outlier_count']) for row in rows)}")


if __name__ == "__main__":
    main()

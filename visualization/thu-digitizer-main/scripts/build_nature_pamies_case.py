"""Build the source-mapped Nature Biomedical Engineering Fig. 1 gallery case.

The article figure is a grouped bar chart with visible replicate dots and error
bars.  The companion Figshare CSVs are the authoritative values for this demo;
the raster image is retained as a visual reference, while the normalized CSV
is explicitly labelled source-mapped rather than pixel-extracted.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw


SERIES = [
    ("Flights of stairs climbed", "#ffffff"),
    ("Walking and running distance", "#f0857f"),
    ("Steps taken", "#fdcc91"),
    ("Sleep quality", "#8cc0e7"),
]
P_VALUE_LABELS = [
    "****", "p = 0.0021", "p = 0.0039", "p = 0.0027", "p = 0.0026", "p = 0.0038", "p = 0.0061"
]


def pct(value: str) -> float:
    return float(value.strip().replace("%", ""))


def read_wide(path: Path) -> tuple[list[str], dict[str, list[float]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    categories = [row["Time (units)"] for row in rows]
    values = {name: [pct(row[name]) for row in rows] for name, _ in SERIES}
    return categories, values


def read_scatter(path: Path, categories: list[str]) -> dict[str, list[list[float]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    output = {name: [] for name, _ in SERIES}
    for row, category in zip(rows[1:], categories):
        if not row or row[0] != category:
            raise ValueError(f"scatter category mismatch: {row[0] if row else '<empty>'} != {category}")
        offset = 1
        for name, _ in SERIES:
            output[name].append([pct(value) for value in row[offset : offset + 4]])
            offset += 4
    return output


def write_data(output: Path, categories: list[str], means: dict[str, list[float]], sds: dict[str, list[float]], points: dict[str, list[list[float]]]) -> int:
    data_path = output / "data.csv"
    fieldnames = [
        "category", "series", "value", "sd", "unit", "category_index", "series_index", "points",
        "source_status", "source_mean_file", "source_sd_file", "source_scatter_file",
    ]
    with data_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        count = 0
        for category_index, category in enumerate(categories):
            for series_index, (name, _) in enumerate(SERIES):
                writer.writerow(
                    {
                        "category": category,
                        "series": name,
                        "value": f"{means[name][category_index]:.1f}",
                        "sd": f"{sds[name][category_index]:.1f}",
                        "unit": "%",
                        "category_index": category_index,
                        "series_index": series_index,
                        "points": ";".join(f"{value:.1f}" for value in points[name][category_index]),
                        "source_status": "official_figshare_source_mapped",
                        "source_mean_file": "bar-means.csv",
                        "source_sd_file": "bar-sd.csv",
                        "source_scatter_file": "scatter.csv",
                    }
                )
                count += 1
    return count


def render_recreated(output: Path, categories: list[str], means: dict[str, list[float]], sds: dict[str, list[float]], points: dict[str, list[list[float]]]) -> None:
    fig, ax = plt.subplots(figsize=(12, 7.93), dpi=100)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    x = np.arange(len(categories), dtype=float)
    width = 0.18
    offsets = np.linspace(-1.5, 1.5, len(SERIES)) * width
    for series_index, (name, color) in enumerate(SERIES):
        positions = x + offsets[series_index]
        edge = "#6b6b6b"
        ax.bar(
            positions,
            means[name],
            width=width * 0.93,
            color=color,
            edgecolor=edge,
            linewidth=0.9,
            yerr=sds[name],
            ecolor="#666666",
            error_kw={"elinewidth": 1.2, "capsize": 3, "capthick": 1.0},
            zorder=2,
            label=name,
        )
        for category_index, values in enumerate(points[name]):
            jitter = np.linspace(-0.045, 0.045, len(values))
            ax.scatter(
                np.full(len(values), positions[category_index]) + jitter,
                values,
                s=26,
                facecolors="white",
                edgecolors="#505050",
                linewidths=0.9,
                zorder=4,
            )

    ax.set_ylim(0, 105)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("Performance (%)", fontsize=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11)
    ax.tick_params(axis="y", labelsize=11, colors="#444444")
    ax.tick_params(axis="x", length=0, pad=8, colors="#444444")
    ax.grid(axis="y", color="#eeeeee", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#666666")
    ax.spines["bottom"].set_color("#666666")
    legend = ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.25),
        ncol=4,
        frameon=False,
        fontsize=12,
        handlelength=1.0,
        columnspacing=1.3,
    )
    for handle, (_, color) in zip(legend.legend_handles, SERIES):
        handle.set_edgecolor("#6b6b6b")
        handle.set_linewidth(0.9)
        handle.set_facecolor(color)
    # Keep the significance layer visible, while not pretending to recover its
    # statistical test from the raster. These labels are visual style only.
    fig.text(0.30, 0.965, P_VALUE_LABELS[1], ha="center", va="center", fontsize=10, color="#444444")
    fig.text(0.52, 0.965, P_VALUE_LABELS[5], ha="center", va="center", fontsize=10, color="#444444")
    fig.text(0.92, 0.965, P_VALUE_LABELS[6], ha="center", va="center", fontsize=10, color="#444444")
    fig.subplots_adjust(left=0.085, right=0.985, bottom=0.14, top=0.73)
    fig.savefig(output / "recreated.png", dpi=100, facecolor="white")
    plt.close(fig)


def render_overlay(output: Path, categories: list[str], means: dict[str, list[float]], sds: dict[str, list[float]], points: dict[str, list[list[float]]]) -> None:
    source = Image.open(output / "original-hi.jpg").convert("RGBA")
    overlay = Image.new("RGBA", source.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    # Manually verified chart ROI on the retained 1200 x 793 raster. This is an
    # evidence overlay for visual review, not a second numeric extraction.
    baseline = 759.0
    plot_top = 211.0
    plot_left = 101.0
    plot_right = 1194.0
    x_centers = np.linspace(plot_left + 75, plot_right - 27, len(categories))
    y = lambda value: baseline - (baseline - plot_top) * float(value) / 100.0
    bar_width = 31.0
    group_gap = 39.0
    colors = [(16, 125, 126, 220), (16, 125, 126, 220), (16, 125, 126, 220), (16, 125, 126, 220)]
    for category_index, center in enumerate(x_centers):
        for series_index, (name, _) in enumerate(SERIES):
            bar_center = center + (series_index - 1.5) * group_gap
            top = y(means[name][category_index])
            left = bar_center - bar_width / 2
            right = bar_center + bar_width / 2
            draw.rectangle((left, top, right, baseline), outline=colors[series_index], width=3)
            error_top = y(means[name][category_index] + sds[name][category_index])
            error_bottom = y(max(0, means[name][category_index] - sds[name][category_index]))
            draw.line((bar_center, error_top, bar_center, error_bottom), fill=(16, 125, 126, 220), width=2)
            draw.line((bar_center - 8, error_top, bar_center + 8, error_top), fill=(16, 125, 126, 220), width=2)
            draw.line((bar_center - 8, error_bottom, bar_center + 8, error_bottom), fill=(16, 125, 126, 220), width=2)
            for point_index, value in enumerate(points[name][category_index]):
                point_x = bar_center + (point_index - 1.5) * 8
                point_y = y(value)
                draw.ellipse((point_x - 5, point_y - 5, point_x + 5, point_y + 5), outline=(16, 125, 126, 230), width=2)
    composite = Image.alpha_composite(source, overlay).convert("RGB")
    composite.save(output / "overlay.png", quality=96)


def build_report(output: Path, data_rows: int, categories: list[str]) -> None:
    source_image = output / "original-hi.jpg"
    sha256 = hashlib.sha256(source_image.read_bytes()).hexdigest()
    report = {
        "schema_version": 1,
        "case_id": "nature-pamies-dots",
        "status": "candidate",
        "title": "Nature Biomedical Engineering Fig. 1 · 分组柱＋可见散点",
        "source": {
            "journal": "Nature Biomedical Engineering",
            "article_title": "Show the dots in plots",
            "article_url": "https://www.nature.com/articles/s41551-017-0079",
            "figure_url": "https://www.nature.com/articles/s41551-017-0079/figures/1",
            "figure": "Fig. 1",
            "doi": "10.1038/s41551-017-0079",
            "published": "2017-05-10",
            "caption": "An individual's monthly activity and sleep quality between January 2015 and December 2016 (data points), ordered from January to December, categorized according to four-month intervals, and normalized by the respective maxima within the two years.",
            "image_url": "https://media.springernature.com/lw1200/springer-static/image/art%3A10.1038%2Fs41551-017-0079/MediaObjects/41551_2017_Article_BFs415510170079_Fig1_HTML.jpg",
            "source_image_license": "not_stated_on_article_page",
            "source_data_url": "https://figshare.com/articles/dataset/May_2017_Editorial_Nature_Biomedical_Engineering/4928888",
            "source_data_license": "CC BY 4.0",
            "source_data_files": ["bar-means.csv", "bar-sd.csv", "scatter.csv", "p-values.csv"],
        },
        "source_image": {
            "file": "original-hi.jpg",
            "sha256": sha256,
            "width": 1200,
            "height": 793,
            "preflight_report": "preflight-report.json",
            "figure_spec": "figure-spec.json",
        },
        "mapping": {
            "status": "official_source_data_mapped",
            "chart_grammar": ["grouped_bar", "visible_replicate_points", "error_interval"],
            "categories": categories,
            "series": [name for name, _ in SERIES],
            "displayed_statistic": "bar height = official mean; error interval = official s.d.; four points = visible monthly observations per four-month interval",
            "summary_rows": data_rows,
            "visible_points": data_rows * 4,
            "pixel_extraction": "not_run",
            "numeric_values": "copied from official Figshare CSVs after panel/metric mapping",
        },
        "assets": {
            "original": "original-hi.jpg",
            "overlay": "overlay.png",
            "recreated": "recreated.png",
            "data": "data.csv",
            "report": "report.json",
        },
        "limitations": [
            "The figure is a Nature article image retained as a reference asset; its article page does not state an image redistribution licence.",
            "Numeric values in this demo are mapped from the authors' CC BY 4.0 Figshare CSVs, not silently inferred from pixels.",
            "The grouped-bar and pastel-bar point-overlay routes remain candidate routes; no WebPlotDigitizer same-input comparison is claimed.",
            "The recreated canvas preserves the series colours, grouped layout, dots and error bars, but typography and significance annotation placement are approximate.",
        ],
    }
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("gallery/assets/cases/nature-pamies-dots"))
    args = parser.parse_args()
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    categories, means = read_wide(output / "bar-means.csv")
    sd_categories, sds = read_wide(output / "bar-sd.csv")
    if categories != sd_categories:
        raise ValueError("mean and SD categories differ")
    points = read_scatter(output / "scatter.csv", categories)
    data_rows = write_data(output, categories, means, sds, points)
    render_recreated(output, categories, means, sds, points)
    render_overlay(output, categories, means, sds, points)
    build_report(output, data_rows, categories)
    print(json.dumps({"output": str(output), "rows": data_rows, "points": data_rows * 4}, ensure_ascii=False))


if __name__ == "__main__":
    main()

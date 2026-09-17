"""Build the public gallery bundle for Nature Communications Fig. 3.

The public CSV and both recreations contain only geometry recovered from the
visible vector PDF.  They do not contain, infer, or import the commercial
hourly/link-level observations summarized by the published figure.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from collections import defaultdict
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "artifacts" / "nature_fig3_s41467-025-63143-5"
DEFAULT_TARGET = ROOT / "gallery" / "assets" / "cases" / "nature-63143-fig3"

CASE_ID = "nature-63143-fig3"
ARTICLE_URL = "https://www.nature.com/articles/s41467-025-63143-5"
FIGURE_URL = f"{ARTICLE_URL}/figures/3"
ARTICLE_TITLE = "Electric transmission value and its drivers in United States power markets"
PDF_PAGE_INDEX = 3
CROP_PT = (88.0, 45.0, 527.0, 252.0)
SCALE = 4.0
CANVAS = (1756, 828)
BAR_WIDTH_PT = 12.296
BAR_COLOR = "#759adc"
LINE_COLOR = "#7f7f7f"
MARKER_FILL = "#bacdee"
MARKER_STROKE = "#3f3f3f"
OVERLAY_RING = "#00c7dd"
PANEL_BOUNDS = {
    "median_left": (96.904, 51.201, 270.581, 224.8521),
    "mean_right": (337.584, 51.201, 511.261, 224.8521),
}
PANEL_LABELS = {
    "median_left": ("Median", "median"),
    "mean_right": ("Mean", "mean"),
}
PUBLIC_FIELDS = [
    "figure",
    "pdf_page_1_based",
    "panel_id",
    "statistic",
    "year",
    "bar_series",
    "bar_value_usd_per_mwh",
    "bar_x_center_pt",
    "bar_top_y_pt",
    "bar_bottom_y_pt",
    "line_series",
    "line_value_usd_per_mwh",
    "line_marker_x_pt",
    "line_marker_y_pt",
    "bar_status",
    "line_status",
    "claim_scope",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def point_to_canvas(x_pt: float, y_pt: float) -> tuple[float, float]:
    return ((x_pt - CROP_PT[0]) * SCALE, (y_pt - CROP_PT[1]) * SCALE)


def render_original(pdf_path: Path, output: Path) -> None:
    document = fitz.open(pdf_path)
    try:
        page = document[PDF_PAGE_INDEX]
        pixmap = page.get_pixmap(
            matrix=fitz.Matrix(SCALE, SCALE),
            clip=fitz.Rect(*CROP_PT),
            alpha=False,
        )
        pixmap.save(output)
    finally:
        document.close()
    with Image.open(output) as image:
        if image.size != CANVAS:
            raise AssertionError(f"Unexpected original canvas {image.size}; expected {CANVAS}")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 22:
        raise AssertionError(f"Expected 22 visible annual rows, found {len(rows)}")
    if {row["panel_id"] for row in rows} != set(PANEL_BOUNDS):
        raise AssertionError("The extraction CSV does not contain the two verified panels")
    return rows


def write_public_csv(rows: list[dict[str, str]], output: Path) -> None:
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=PUBLIC_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in PUBLIC_FIELDS})


def centered(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, text_font, fill: str) -> None:
    draw.text(xy, text, font=text_font, fill=fill, anchor="mm")


def rotated_text(
    image: Image.Image,
    text: str,
    xy: tuple[float, float],
    *,
    text_font,
    fill: str,
    angle: int,
) -> None:
    box = text_font.getbbox(text)
    width = max(1, box[2] - box[0] + 12)
    height = max(1, box[3] - box[1] + 12)
    layer = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    layer_draw = ImageDraw.Draw(layer)
    layer_draw.text((6 - box[0], 6 - box[1]), text, font=text_font, fill=fill)
    rotated = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    image.alpha_composite(rotated, (round(xy[0] - rotated.width / 2), round(xy[1] - rotated.height / 2)))


def render_recreation(rows: list[dict[str, str]], output: Path) -> None:
    image = Image.new("RGBA", CANVAS, "white")
    draw = ImageDraw.Draw(image)
    tick_font = font(27)
    year_font = font(27)
    label_font = font(29)

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["panel_id"]].append(row)

    for panel_id, panel_rows in grouped.items():
        panel_rows.sort(key=lambda row: int(row["year"]))
        left_pt, top_pt, right_pt, bottom_pt = PANEL_BOUNDS[panel_id]
        left, top = point_to_canvas(left_pt, top_pt)
        right, bottom = point_to_canvas(right_pt, bottom_pt)

        for tick in range(0, 26, 5):
            y = bottom - (tick / 25.0) * (bottom - top)
            draw.line((left, y, right, y), fill="#ececec", width=2)
            draw.text((left - 20, y), str(tick), font=tick_font, fill="#444444", anchor="rm")
        for tick in range(0, 71, 10):
            y = bottom - (tick / 70.0) * (bottom - top)
            draw.text((right + 20, y), str(tick), font=tick_font, fill="#444444", anchor="lm")

        draw.rectangle((left, top, right, bottom), outline="#353535", width=3)
        for row in panel_rows:
            center_x, top_y = point_to_canvas(
                float(row["bar_x_center_pt"]),
                float(row["bar_top_y_pt"]),
            )
            _, base_y = point_to_canvas(
                float(row["bar_x_center_pt"]),
                float(row["bar_bottom_y_pt"]),
            )
            half_width = BAR_WIDTH_PT * SCALE / 2
            draw.rectangle(
                (center_x - half_width, top_y, center_x + half_width, base_y),
                fill=BAR_COLOR,
            )

        marker_points = [
            point_to_canvas(float(row["line_marker_x_pt"]), float(row["line_marker_y_pt"]))
            for row in panel_rows
        ]
        draw.line(marker_points, fill=LINE_COLOR, width=9, joint="curve")
        for row, (marker_x, marker_y) in zip(panel_rows, marker_points):
            draw.ellipse(
                (marker_x - 13, marker_y - 13, marker_x + 13, marker_y + 13),
                fill=MARKER_FILL,
                outline=MARKER_STROKE,
                width=5,
            )
            rotated_text(
                image,
                row["year"],
                (marker_x, bottom + 84),
                text_font=year_font,
                fill="#333333",
                angle=90,
            )

        _, statistic = PANEL_LABELS[panel_id]
        if panel_id == "median_left":
            rotated_text(
                image,
                f"Bars: {statistic} link's mean RT transmission market value ($/MWh)",
                (left - 86, (top + bottom) / 2),
                text_font=label_font,
                fill="#222222",
                angle=90,
            )
        else:
            rotated_text(
                image,
                f"Bars: {statistic} link's mean RT transmission market value ($/MWh)",
                (left - 86, (top + bottom) / 2),
                text_font=label_font,
                fill="#222222",
                angle=90,
            )
        rotated_text(
            image,
            f"Lines: {statistic} wholesale electricity RT price ($/MWh)",
            (right + 91, (top + bottom) / 2),
            text_font=label_font,
            fill="#222222",
            angle=90,
        )

    image.convert("RGB").save(output, optimize=True)
    with Image.open(output) as rendered:
        if rendered.size != CANVAS:
            raise AssertionError(f"Unexpected recreation canvas {rendered.size}; expected {CANVAS}")


def gallery_sample() -> dict:
    return {
        "id": "bar",
        "title": "双轴柱形折线图",
        "subtitle": "年度传输价值与批发电价",
        "status": "partial_visible",
        "statusLabel": "可见几何 · PDF 向量",
        "description": (
            "从 Nature Communications Fig. 3 的矢量 PDF 直接恢复两个面板中 "
            "2012–2022 年的 22 个柱端值与 22 个折线标记；不反推逐小时或链路级原始数据。"
        ),
        "metrics": [
            {"label": "可见柱", "value": "22 / 22"},
            {"label": "折线标记", "value": "22 / 22"},
        ],
        "metricNote": (
            "公开 CSV 仅含图中可见年度汇总及 PDF 坐标；文章未提供可核验的 Fig. 3 Source Data 文件。"
        ),
        "articleUrl": ARTICLE_URL,
        "journal": "Nature Communications",
        "articleTitle": ARTICLE_TITLE,
        "figure": "Fig. 3",
        "figureUrl": FIGURE_URL,
        "assets": {
            "original": f"assets/cases/{CASE_ID}/original.png",
            "overlay": f"assets/cases/{CASE_ID}/overlay.png",
            "recreated": f"assets/cases/{CASE_ID}/recreated.png",
            "data": f"assets/cases/{CASE_ID}/data.csv",
            "report": f"assets/cases/{CASE_ID}/report.json",
        },
        "styleSpec": {
            "renderer": "paper-dual-axis-bar-line",
            "fidelity": "visible_geometry_candidate",
            "label": "论文原生画布 · PDF 向量几何",
            "note": (
                "柱体与折线标记逐行来自公开主 CSV；悬停任一数据标记可读取生成它的完整行字段。"
            ),
            "canvas": {"width": CANVAS[0], "height": CANVAS[1]},
            "fontFamily": "Arial, Helvetica, sans-serif",
            "crop": {"x": CROP_PT[0], "y": CROP_PT[1], "scale": SCALE},
            "barWidthPt": BAR_WIDTH_PT,
            "barColor": BAR_COLOR,
            "lineColor": LINE_COLOR,
            "markerFill": MARKER_FILL,
            "markerStroke": MARKER_STROKE,
            "panels": [
                {
                    "id": panel_id,
                    "label": PANEL_LABELS[panel_id][0],
                    "statistic": PANEL_LABELS[panel_id][1],
                    "plotBoundsPt": list(PANEL_BOUNDS[panel_id]),
                    "barDomain": [0, 25],
                    "barTicks": [0, 5, 10, 15, 20, 25],
                    "lineDomain": [0, 70],
                    "lineTicks": [0, 10, 20, 30, 40, 50, 60, 70],
                }
                for panel_id in ("median_left", "mean_right")
            ],
        },
    }


def build(source_dir: Path, target_dir: Path) -> dict:
    source_dir = source_dir.resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = source_dir / "article.pdf"
    csv_path = source_dir / "figure3_extracted.csv"
    overlay_path = source_dir / "figure3_extraction_overlay.png"
    spec_path = source_dir / "figure_spec_verified.json"
    for path in (pdf_path, csv_path, overlay_path, spec_path):
        if not path.is_file():
            raise FileNotFoundError(path)

    rows = read_rows(csv_path)
    render_original(pdf_path, target_dir / "original.png")
    shutil.copy2(overlay_path, target_dir / "overlay.png")
    with Image.open(target_dir / "overlay.png") as overlay:
        if overlay.size != CANVAS:
            raise AssertionError(f"Unexpected overlay canvas {overlay.size}; expected {CANVAS}")
    write_public_csv(rows, target_dir / "data.csv")
    render_recreation(rows, target_dir / "recreated.png")

    source_spec = json.loads(spec_path.read_text(encoding="utf-8"))
    sanitized_spec = {
        "schema_version": source_spec["schema_version"],
        "status": source_spec["status"],
        "source": {
            "sha256": source_spec["source"]["sha256"],
            "media_kind": source_spec["source"]["media_kind"],
            "coordinate_space": source_spec["source"]["coordinate_space"],
            "measurement_space": source_spec["source"]["measurement_space"],
            "page": source_spec["source"]["page"],
        },
        "panels": source_spec["panels"],
        "evidence_contract": source_spec["evidence_contract"],
    }
    (target_dir / "figure-spec.json").write_text(
        json.dumps(sanitized_spec, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    report = {
        "schema_version": 1,
        "case_id": CASE_ID,
        "status": "partial_visible",
        "maturity": "assisted_candidate",
        "claim": (
            "Direct recovery of visible annual bar endpoints and line-marker centres "
            "from the vector PDF; not recovery of underlying hourly or link-level data."
        ),
        "source": {
            "article_url": ARTICLE_URL,
            "figure_url": FIGURE_URL,
            "article_title": ARTICLE_TITLE,
            "figure": "Fig. 3",
            "pdf_page_1_based": 4,
            "pdf_sha256": sha256(pdf_path),
            "official_source_data_validation": {
                "status": "not_available",
                "reason": (
                    "No separate Source Data file was exposed on the article page; "
                    "the data-availability statement describes commercial inputs."
                ),
            },
        },
        "route": {
            "route_id": "pdf_vector_assisted",
            "figure_spec_status": "ready_for_assisted_extraction",
            "coordinate_space": "pdf_pt",
        },
        "chart": {
            "composition": "two-panel bar chart with a line-marker overlay and dual linear y axes",
            "years": list(range(2012, 2023)),
            "panels": [
                {
                    "panel_id": panel_id,
                    "plot_bounds_pt": list(PANEL_BOUNDS[panel_id]),
                    "bar_axis": {"scale": "linear", "domain": [0, 25], "unit": "$/MWh"},
                    "line_axis": {"scale": "linear", "domain": [0, 70], "unit": "$/MWh"},
                }
                for panel_id in ("median_left", "mean_right")
            ],
        },
        "visible_mark_counts": {
            "bars_expected": 22,
            "bars_accepted": 22,
            "bars_rejected": 0,
            "line_markers_expected": 22,
            "line_markers_accepted": 22,
            "line_markers_rejected": 0,
        },
        "quality_checks": {
            "bar_fill": BAR_COLOR,
            "bar_baseline_range_pt": 0.0,
            "max_marker_bar_x_alignment_error_pt": 0.0010070000000155233,
            "marker_centres_derived_from_symmetric_outer_vector_ring": True,
            "legend_exclusion": "not_applicable_no_legend_in_figure_3",
        },
        "public_gallery": {
            "primary_csv": "data.csv",
            "primary_csv_row_count": len(rows),
            "primary_csv_fields": PUBLIC_FIELDS,
            "representation": "visible PDF geometry only",
            "original_and_recreation_canvas": list(CANVAS),
            "crop_pt": list(CROP_PT),
            "scale": SCALE,
            "source_data_used_by_renderer": False,
            "limitations": [
                "Only displayed annual summaries are recoverable.",
                "Underlying hourly observations and link-level values are not inferred.",
                "Displayed values are coordinate-derived estimates from the vector geometry.",
            ],
        },
    }
    report_path = target_dir / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    asset_names = [
        "original.png",
        "overlay.png",
        "recreated.png",
        "data.csv",
        "report.json",
        "figure-spec.json",
    ]
    manifest = {
        "schema_version": 1,
        "case_id": CASE_ID,
        "assets": {
            name: {"sha256": sha256(target_dir / name), "bytes": (target_dir / name).stat().st_size}
            for name in asset_names
        },
    }
    (target_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (target_dir / "README.md").write_text(
        "# Nature Communications Fig. 3 gallery case\n\n"
        "This bundle contains only annual bar endpoints and line-marker centres "
        "visibly recovered from page 4 of the article's vector PDF. The public "
        "CSV does not contain source-workbook, author-observation, hourly, or "
        "link-level data.\n",
        encoding="utf-8",
    )
    return gallery_sample()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--target-dir", type=Path, default=DEFAULT_TARGET)
    args = parser.parse_args()
    sample = build(args.source_dir, args.target_dir)
    print(json.dumps(sample, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

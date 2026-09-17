"""Build the white gallery's deterministic basic-chart evidence bundles.

The generated examples are local synthetic fixtures with retained truth.  Each
row includes the source raster, an extraction overlay, a recreation made only
from extracted values, CSV data, and a JSON report.  Published OA examples are
kept separate in the page manifest so benchmark evidence is not confused with
article provenance.
"""
from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
GALLERY = ROOT / "gallery"
OUTPUT = GALLERY / "assets" / "basics"
SCRATCH_BASE = Path(r"D:\Scratch\thu-digitizer-gallery-basics-20260720")
COLORS = {"red": "#d62728", "gray": "#7f7f7f", "blue": "#1f77b4", "green": "#2ca02c"}


def run_script(name: str, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, str(SCRIPTS / name), "--output-dir", str(output_dir)],
        cwd=ROOT,
        check=True,
    )


def copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def save_clean_figure(figure, path: Path) -> None:
    figure.savefig(path, dpi=120, facecolor="white", bbox_inches="tight")
    plt.close(figure)


def standard_axis(title: str, xlabel: str, ylabel: str):
    figure, axis = plt.subplots(figsize=(6.4, 4.5), dpi=100, facecolor="white")
    axis.set_title(title, loc="left", fontsize=12, pad=12)
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)
    axis.grid(axis="y", color="#e7e7e7", linewidth=0.8)
    axis.set_axisbelow(True)
    axis.spines[["top", "right"]].set_visible(False)
    return figure, axis


def build_line(synthetic_dir: Path) -> dict:
    sys.path.insert(0, str(SCRIPTS))
    from build_line_gallery_case import build_case

    canonical_source = OUTPUT / "line" / "original.png"
    if not canonical_source.is_file():
        canonical_source = synthetic_dir / "fixtures" / "line_clean.png"
    return build_case(canonical_source, write_manifest=False)


def build_scatter(synthetic_dir: Path) -> dict:
    sys.path.insert(0, str(SCRIPTS))
    import run_synthetic_benchmark as synthetic

    case_dir = OUTPUT / "scatter"
    case_dir.mkdir(parents=True, exist_ok=True)
    original = synthetic_dir / "fixtures" / "scatter.png"
    benchmark = json.loads((synthetic_dir / "benchmark_report.json").read_text(encoding="utf-8"))
    meta = next(item for item in benchmark["fixtures"] if item["name"] == "scatter")
    image = Image.open(original).convert("RGB")
    pixels = np.asarray(image)
    rows = []
    overlay = image.copy()
    draw = ImageDraw.Draw(overlay)
    for name in ("red", "blue", "green"):
        for component in synthetic.components(synthetic.mask(pixels, COLORS[name]), meta):
            x_pixel = float(component[:, 1].mean())
            y_pixel = float(component[:, 0].mean())
            rows.append(
                {
                    "series": name,
                    "x": synthetic.x_value(x_pixel, meta),
                    "y": synthetic.y_value(y_pixel, meta),
                    "x_pixel": x_pixel,
                    "y_pixel": y_pixel,
                }
            )
            radius = 7
            draw.ellipse((x_pixel - radius, y_pixel - radius, x_pixel + radius, y_pixel + radius), outline="#00a7a7", width=2)
    overlay.save(case_dir / "overlay.png")
    copy(original, case_dir / "original.png")
    with (case_dir / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["series", "x", "y", "x_pixel", "y_pixel"])
        writer.writeheader()
        writer.writerows(rows)

    results = [item for item in benchmark["results"] if item["case"] == "scatter" and item["method"] == "component_centroids"]
    scatter_report = {
        "schema_version": 1,
        "family": "scatter",
        "status": "validated_local_stable",
        "input_file": original.name,
        "raster_dimensions": meta["size"],
        "plot_bounds": meta["bounds"],
        "calibration": {"x": meta["xlim"], "y": meta["ylim"], "assumption": "verified linear axes"},
        "series": [item["series"] for item in results],
        "points": rows,
        "benchmark_metrics": results,
        "limitations": [
            "Only visible, colour-distinct marker components are recovered.",
            "Overlapped same-colour points and hidden source observations are not inferred.",
        ],
    }
    (case_dir / "report.json").write_text(json.dumps(scatter_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    figure, axis = standard_axis("Recreated from extracted points", "x", "y")
    for name in ("red", "blue", "green"):
        series = [row for row in rows if row["series"] == name]
        axis.scatter([row["x"] for row in series], [row["y"] for row in series], s=42, color=COLORS[name], edgecolor="white", linewidth=0.5, label=name)
    axis.set_xlim(0, 10)
    axis.set_ylim(0, 10)
    axis.legend(frameon=False, ncols=3, fontsize=8)
    save_clean_figure(figure, case_dir / "recreated.png")
    mean_mae = float(np.mean([item["mae"] for item in results]))
    return {
        "id": "scatter",
        "title": "散点图",
        "subtitle": "颜色分组的离散点",
        "status": "validated_local_stable",
        "statusLabel": "稳定 · 合成基准",
        "description": "以连通域中心恢复 3 组 15 个可见标记；不把重叠或被遮挡的点补成隐藏样本。",
        "metrics": [{"label": "点覆盖", "value": "15 / 15"}, {"label": "坐标 MAE", "value": f"{mean_mae:.3f}"}],
        "assets": assets("scatter"),
    }


def build_dose_response() -> dict:
    case_root = GALLERY / "assets" / "cases" / "nature-kahlous-dose-response"
    report = json.loads((case_root / "report.json").read_text(encoding="utf-8"))
    extraction = report["candidate_extraction"]["summary"]
    validation = report["source_validation"]
    return {
        "id": "dose-response",
        "title": "剂量—反应曲线",
        "subtitle": "断轴、散点、SEM 与曲线路径",
        "status": "candidate",
        "statusLabel": "候选 · 论文源数据核验",
        "description": "从 Nature Communications Fig. 4d 的 OA PDF 矢量层恢复三系列可见点、误差棒和曲线路径。",
        "metrics": [
            {
                "label": "点覆盖",
                "value": f"{validation['source_matched_markers']} + {validation['source_uncovered_vehicle_markers']}",
            },
            {"label": "点值 MAE", "value": f"{validation['marker_mae']:.3f}"},
        ],
        "articleUrl": "https://www.nature.com/articles/s41467-026-71361-8",
        "assets": {
            "original": "assets/cases/nature-kahlous-dose-response/original.png",
            "overlay": "assets/cases/nature-kahlous-dose-response/overlay.png",
            "recreated": "assets/cases/nature-kahlous-dose-response/recreated.png",
            "data": "assets/cases/nature-kahlous-dose-response/data.csv",
            "report": "assets/cases/nature-kahlous-dose-response/report.json",
        },
        "evidence": {
            "visibleMarkers": extraction["visible_marker_count"],
            "visibleErrorBars": extraction["visible_error_bar_count"],
            "tracedCurves": extraction["traced_curve_count"],
        },
    }


def build_histogram(histogram_dir: Path) -> dict:
    case_dir = OUTPUT / "histogram"
    case_dir.mkdir(parents=True, exist_ok=True)
    report_path = histogram_dir / "histogram_benchmark_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    variant = next(item for item in report["variants"] if item["name"] == "histogram_clean.png")
    copy(histogram_dir / variant["name"], case_dir / "original.png")
    copy(histogram_dir / variant["overlay"], case_dir / "overlay.png")
    copy(report_path, case_dir / "report.json")
    with (case_dir / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["bin", "x_left", "x_right", "height", "left_pixel", "right_pixel", "top_pixel", "bottom_pixel"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for index, bin_ in enumerate(variant["bins"], start=1):
            writer.writerow({"bin": index, **{key: bin_[key] for key in fields[1:]}})
    figure, axis = standard_axis("Recreated from extracted bins", "Bin", "Count")
    centers = [(item["x_left"] + item["x_right"]) / 2 for item in variant["bins"]]
    widths = [item["x_right"] - item["x_left"] for item in variant["bins"]]
    axis.bar(centers, [item["height"] for item in variant["bins"]], width=widths, color="#1f77b4", edgecolor="white", linewidth=0.8)
    axis.set_xlim(-0.8, 4.8)
    axis.set_ylim(0, 12)
    save_clean_figure(figure, case_dir / "recreated.png")
    return {
        "id": "histogram",
        "title": "直方图",
        "subtitle": "箱边界与箱高",
        "status": "validated_local_stable",
        "statusLabel": "稳定 · 合成基准",
        "description": "恢复每个可见矩形的左右边界与高度；这里只提取已绘制的箱，不反推箱内原始观测。",
        "metrics": [{"label": "箱覆盖", "value": "5 / 5"}, {"label": "高度 MAE", "value": f"{variant['mae']:.3f}"}],
        "assets": assets("histogram"),
    }


def build_boxplot_variant(
    boxplot_dir: Path,
    *,
    variant_name: str,
    case_id: str,
    title: str,
    subtitle: str,
) -> dict:
    case_dir = OUTPUT / case_id
    case_dir.mkdir(parents=True, exist_ok=True)
    report_path = boxplot_dir / "boxplot_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    variant = next(item for item in report["variants"] if item["name"] == variant_name)
    copy(boxplot_dir / variant["image"], case_dir / "original.png")
    copy(boxplot_dir / variant["overlay"], case_dir / "overlay.png")
    copy(report_path, case_dir / "report.json")
    rows = []
    for index, group in enumerate(variant["groups"]):
        row = {"group": chr(65 + index), **{key: group[key] for key in ["q1", "median", "q3", "lower_whisker", "upper_whisker"]}}
        row["visible_outliers"] = ";".join(str(item["value"]) for item in group["outliers"])
        rows.append(row)
    with (case_dir / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    bxp_stats = [
        {
            "label": row["group"],
            "q1": row["q1"],
            "med": row["median"],
            "q3": row["q3"],
            "whislo": row["lower_whisker"],
            "whishi": row["upper_whisker"],
            "fliers": [float(value) for value in row["visible_outliers"].split(";") if value],
        }
        for row in rows
    ]
    if variant["orientation"] == "vertical":
        figure, axis = standard_axis("Recreated visible box summaries", "Group", "Value")
    else:
        figure, axis = plt.subplots(figsize=(6.4, 4.5), dpi=100, facecolor="white")
        axis.set_title("Recreated visible box summaries", loc="left", fontsize=12, pad=12)
        axis.set_xlabel("Value")
        axis.set_ylabel("Group")
        axis.grid(axis="x", color="#e7e7e7", linewidth=0.8)
        axis.set_axisbelow(True)
        axis.spines[["top", "right"]].set_visible(False)
    axis.bxp(
        bxp_stats,
        orientation=variant["orientation"],
        patch_artist=True,
        boxprops={"facecolor": "#6baed6", "edgecolor": "#6baed6"},
        medianprops={"color": "#111111", "linewidth": 1.6},
        whiskerprops={"color": "#111111"},
        capprops={"color": "#111111"},
        flierprops={"marker": "o", "markerfacecolor": "#d62728", "markeredgecolor": "#d62728", "markersize": 5},
    )
    if variant["orientation"] == "vertical":
        axis.set_ylim(0, 13)
    else:
        axis.set_xlim(0, 13)
        axis.invert_yaxis()
    save_clean_figure(figure, case_dir / "recreated.png")
    return {
        "id": case_id,
        "title": title,
        "subtitle": subtitle,
        "status": "validated_local_stable",
        "statusLabel": "稳定 · 合成基准",
        "description": "逐组恢复 Q1、中位数、Q3、上下须及可见离群点；不会把箱线图伪装成原始样本表。",
        "metrics": [{"label": "组覆盖", "value": "4 / 4"}, {"label": "统计量 MAE", "value": f"{variant['summary_mae']:.3f}"}],
        "assets": assets(case_id),
    }


def build_boxplot(boxplot_dir: Path) -> dict:
    del boxplot_dir
    case_root = GALLERY / "assets" / "cases" / "nature-protaide-boxplot"
    report = json.loads((case_root / "report.json").read_text(encoding="utf-8"))
    extracted = report["candidate_extraction"]
    return {
        "id": "boxplot",
        "title": "纵向箱线图",
        "subtitle": "论文中的成对空心与填充箱体",
        "status": "candidate",
        "statusLabel": "候选 · 论文原图",
        "description": "从 Nature Medicine Fig. 4b 恢复 Retrain 与 Finetune 的五数概括、须线及可见离群点。",
        "metrics": [
            {"label": "箱体覆盖", "value": f"{extracted['box_groups_extracted']} / {extracted['box_groups_visible']}"},
            {"label": "可见离群点", "value": str(extracted["visible_outliers_extracted"])},
        ],
        "articleUrl": "https://www.nature.com/articles/s41591-026-04303-y",
        "assets": {
            "original": "assets/cases/nature-protaide-boxplot/original.png",
            "overlay": "assets/cases/nature-protaide-boxplot/overlay.png",
            "recreated": "assets/cases/nature-protaide-boxplot/recreated.png",
            "data": "assets/cases/nature-protaide-boxplot/data.csv",
            "report": "assets/cases/nature-protaide-boxplot/report.json",
        },
    }


def build_heatmap() -> dict:
    case_root = GALLERY / "assets" / "cases" / "nature-protaide-heatmap"
    report = json.loads((case_root / "report.json").read_text(encoding="utf-8"))
    validation = report["source_validation"]
    return {
        "id": "heatmap",
        "title": "热力图",
        "subtitle": "单元格、色条与显著性标记",
        "status": "candidate",
        "statusLabel": "候选 · 论文验证",
        "description": "从 Nature Medicine Fig. 4c 恢复 32×21 相关矩阵、色条区间和可见白色显著性星号。",
        "metrics": [
            {"label": "单元格覆盖", "value": f"{validation['matched_cells']} / {validation['visible_cells']}"},
            {"label": "色条内 MAE", "value": f"{validation['numeric_mae']:.4f}"},
        ],
        "articleUrl": "https://www.nature.com/articles/s41591-026-04303-y",
        "assets": {
            "original": "assets/cases/nature-protaide-heatmap/original.png",
            "overlay": "assets/cases/nature-protaide-heatmap/overlay.png",
            "recreated": "assets/cases/nature-protaide-heatmap/recreated.png",
            "data": "assets/cases/nature-protaide-heatmap/data.csv",
            "report": "assets/cases/nature-protaide-heatmap/report.json",
        },
    }


def build_horizontal_boxplot(boxplot_dir: Path) -> dict:
    return build_boxplot_variant(
        boxplot_dir,
        variant_name="horizontal_clean",
        case_id="boxplot-horizontal",
        title="横向箱线图",
        subtitle="横向数值轴与可见离群点",
    )


def build_bar_variant(
    bar_dir: Path,
    *,
    variant_name: str,
    case_id: str,
    title: str,
    subtitle: str,
) -> dict:
    case_dir = OUTPUT / case_id
    case_dir.mkdir(parents=True, exist_ok=True)
    report_path = bar_dir / "bar_benchmark_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    variant = next(item for item in report["variants"] if item["name"] == variant_name)
    copy(bar_dir / f"{variant['name']}.png", case_dir / "original.png")
    copy(bar_dir / variant["overlay"], case_dir / "overlay.png")
    copy(bar_dir / variant["recreation"], case_dir / "recreated.png")
    copy(report_path, case_dir / "report.json")
    marks = variant["extraction"]["marks"]
    with (case_dir / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["category", "series", "value", "status", "confidence", "error_lower", "error_upper"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for mark in marks:
            error = mark.get("error_bar", {})
            writer.writerow(
                {
                    "category": mark["category"],
                    "series": mark["series"],
                    "value": mark.get("value"),
                    "status": mark["status"],
                    "confidence": mark["confidence"],
                    "error_lower": error.get("lower_value"),
                    "error_upper": error.get("upper_value"),
                }
            )
    return {
        "id": case_id,
        "title": title,
        "subtitle": subtitle,
        "status": "candidate",
        "statusLabel": "候选 · 仅合成基准",
        "description": "候选引擎已在确定性基准中恢复 8 个矩形与可见区间；尚未完成真实矢量、真实栅格和同条件 WPD 对比。",
        "metrics": [
            {
                "label": "柱覆盖",
                "value": f"{variant['metrics']['matched_mark_count']} / {variant['metrics']['expected_mark_count']}",
            },
            {"label": "数值 MAE", "value": f"{variant['metrics']['mae']:.3f}"},
        ],
        "assets": assets(case_id),
    }


def build_bar(bar_dir: Path) -> dict:
    del bar_dir
    from build_natcom_transmission_fig3_gallery_case import gallery_sample

    return gallery_sample()


def build_horizontal_bar(bar_dir: Path) -> dict:
    del bar_dir
    from build_requested_nature_bar_gallery_cases import build_horizontal

    return build_horizontal()


def build_stacked_bar(bar_dir: Path) -> dict:
    del bar_dir
    from build_requested_nature_bar_gallery_cases import build_stacked

    return build_stacked()


def build_percent_stacked_bar(bar_dir: Path) -> dict:
    sys.path.insert(0, str(SCRIPTS))
    import run_bar_benchmark as bar_benchmark

    evidence_dir = bar_dir / "gallery_percent_stacked_white"
    evidence_dir.mkdir(parents=True, exist_ok=False)
    fixture = bar_benchmark._render_stacked(
        evidence_dir / "original.png",
        orientation="horizontal",
        percent=True,
        dark=False,
    )
    variant = bar_benchmark._measure_fixture(fixture, evidence_dir)
    failure_reason = bar_benchmark._failure_reason(variant)
    variant["benchmark_status"] = "failed" if failure_reason else "passed"
    variant["failure_reason"] = failure_reason or ""
    if failure_reason:
        raise AssertionError(failure_reason)

    report = {
        "schema_version": 1,
        "family": "bar_chart_candidate",
        "candidate_module": "candidate_digitize_bar_chart.py",
        "privacy": bar_benchmark.PRIVACY_STATEMENT,
        "comparison": {
            "current_stable": "not_available_for_dedicated_bar_extraction",
            "webplotdigitizer": "not_compared; assisted comparison still required before promotion",
        },
        "status": "passed",
        "failure_reason": "",
        "variants": [variant],
    }
    report_path = evidence_dir / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    data_path = evidence_dir / "data.csv"
    bar_benchmark._write_csv(data_path, [variant])

    case_dir = OUTPUT / "bar-percent-stacked"
    case_dir.mkdir(parents=True, exist_ok=True)
    copy(fixture.path, case_dir / "original.png")
    copy(evidence_dir / variant["overlay"], case_dir / "overlay.png")
    copy(evidence_dir / variant["recreation"], case_dir / "recreated.png")
    copy(data_path, case_dir / "data.csv")
    copy(report_path, case_dir / "report.json")
    return {
        "id": "bar-percent-stacked",
        "title": "100% 堆叠柱",
        "subtitle": "横向比例堆叠",
        "status": "candidate",
        "statusLabel": "候选 · 仅合成基准",
        "description": "白底确定性基准恢复每个可见比例段；尚未完成真实矢量、真实栅格和同条件 WPD 对比。",
        "metrics": [
            {
                "label": "分段覆盖",
                "value": f"{variant['metrics']['matched_mark_count']} / {variant['metrics']['expected_mark_count']}",
            },
            {"label": "数值 MAE", "value": f"{variant['metrics']['mae']:.3f}"},
        ],
        "assets": assets("bar-percent-stacked"),
    }


def build_pie_case() -> dict:
    from build_requested_nature_pie_gallery_case import build_case

    return build_case()


def build_forest_plot() -> dict:
    return {
        "id": "forest",
        "title": "区间 / 森林图",
        "subtitle": "点估计与可见区间端点",
        "status": "visible_geometry_extracted",
        "statusLabel": "真实图 · 几何提取",
        "description": "从 Nature Communications Fig. 2 恢复 29 个点估计和可见区间端点；这是单例几何证据，不是稳定引擎晋级。",
        "metrics": [{"label": "点覆盖", "value": "29 / 29"}, {"label": "证据", "value": "真实 OA 图"}],
        "assets": {
            "original": "assets/cases/nature-blood-forest/original.jpg",
            "overlay": "assets/cases/nature-blood-forest/overlay.png",
            "recreated": "assets/cases/nature-blood-forest/recreated.png",
            "data": "assets/cases/nature-blood-forest/data.csv",
            "report": "assets/cases/nature-blood-forest/report.json",
        },
    }


def build_china_mining_contour() -> dict | None:
    """Publish the local, visible-only raster contour evidence when available."""
    from build_china_mining_contour_gallery_case import DEFAULT_EVIDENCE, DEFAULT_OUTPUT, build

    if not DEFAULT_EVIDENCE.is_dir():
        return None
    return build(DEFAULT_EVIDENCE, DEFAULT_OUTPUT)


def assets(case_id: str) -> dict:
    root = f"assets/basics/{case_id}"
    return {
        "original": f"{root}/original.png",
        "overlay": f"{root}/overlay.png",
        "recreated": f"{root}/recreated.png",
        "data": f"{root}/data.csv",
        "report": f"{root}/report.json",
    }


def normalize_recreated_canvases(samples: list[dict]) -> None:
    """Keep generated recreations on the same pixel canvas as their originals.

    Several benchmark renderers use Matplotlib's tight bounding box, which can
    change the exported dimensions even when the plotted content is correct.
    The gallery overlay/compare UI requires an immutable one-to-one canvas.
    """
    for sample in samples:
        sample_assets = sample.get("assets", {})
        original_rel = sample_assets.get("original")
        recreated_rel = sample_assets.get("recreated")
        if not original_rel or not recreated_rel:
            continue
        original_path = GALLERY / original_rel
        recreated_path = GALLERY / recreated_rel
        if not original_path.is_file() or not recreated_path.is_file():
            continue
        with Image.open(original_path) as original, Image.open(recreated_path) as recreated:
            if recreated.size == original.size:
                continue
            resized = recreated.convert("RGB").resize(original.size, Image.Resampling.LANCZOS)
            resized.save(recreated_path)


def build_manifest(samples: list[dict]) -> None:
    target = GALLERY / "data" / "basics.json"
    existing_manifest = {}
    if target.is_file():
        existing_manifest = json.loads(target.read_text(encoding="utf-8"))

    generated_by_id = {sample["id"]: sample for sample in samples}
    merged_samples = []
    seen = set()
    for existing in existing_manifest.get("samples", []):
        case_id = existing["id"]
        generated = generated_by_id.get(case_id)
        # Case-specific builders carry richer provenance and pixel geometry.
        # Keep those fields authoritative while still accepting a newly added
        # basic sample on a clean checkout.
        merged_samples.append({**generated, **existing} if generated else existing)
        seen.add(case_id)
    merged_samples.extend(sample for sample in samples if sample["id"] not in seen)

    default_paper_cases = [
            {
                "id": "nature-borneo-edge",
                "title": "散点 + 模型曲线 + 重叠直方图",
                "journal": "Nature Communications",
                "figure": "Fig. 2",
                "articleTitle": "Long-term carbon sink in Borneo’s forests halted by drought and vulnerable to edge effects",
                "articleUrl": "https://www.nature.com/articles/s41467-017-01997-0",
                "statusLabel": "官方源数据映射",
                "description": "71 行作者源数据映射回 Fig. 2；其中 50 行位于散点面板可见横轴范围。",
                "assets": {
                    "original": "assets/cases/nature-borneo-edge/original.jpg",
                    "overlay": "assets/cases/nature-borneo-edge/overlay.png",
                    "recreated": "assets/cases/nature-borneo-edge/recreated.png",
                    "data": "assets/cases/nature-borneo-edge/data.csv",
                    "report": "assets/cases/nature-borneo-edge/report.json",
                },
            },
            {
                "id": "nature-ribotie-multipanel",
                "title": "多面板图中的彩色散点",
                "journal": "Nature Communications",
                "figure": "Fig. 2 · panel e",
                "articleTitle": "Deep learning to decode sites of RNA translation in normal and cancerous tissues",
                "articleUrl": "https://www.nature.com/articles/s41467-025-56543-0",
                "statusLabel": "局部几何提取",
                "description": "从复杂十面板图中路由 panel e，并恢复 18 个可分离的彩色组件。",
                "assets": {
                    "original": "assets/cases/nature-ribotie-multipanel/original-panel-e.png",
                    "overlay": "assets/cases/nature-ribotie-multipanel/overlay.png",
                    "recreated": "assets/cases/nature-ribotie-multipanel/recreated.png",
                    "data": "assets/cases/nature-ribotie-multipanel/data.csv",
                    "report": "assets/cases/nature-ribotie-multipanel/report.json",
                },
            },
        ]
    manifest = {
        **existing_manifest,
        "schemaVersion": 1,
        "generated": date.today().isoformat(),
        "title": "thu-digitizer Basic Extraction Gallery",
        "columnLabels": ["原图", "提取覆盖", "数据复现"],
        "samples": merged_samples,
        "paperCases": existing_manifest.get("paperCases", default_paper_cases),
        "claimNote": existing_manifest.get(
            "claimNote",
            "稳定状态仅指当前仓库中已通过本地基准的专用提取器。柱状图、剂量—反应曲线、论文配对箱线图与校准热力图路线仍为候选；WebPlotDigitizer 尚未进行同输入、同校准与同人工干预条件的比较。",
        ),
    }
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fresh_scratch_dir() -> Path:
    if not SCRATCH_BASE.exists():
        return SCRATCH_BASE
    for index in range(1, 1000):
        candidate = SCRATCH_BASE.with_name(f"{SCRATCH_BASE.name}-run-{index:03d}")
        if not candidate.exists():
            return candidate
    raise RuntimeError("could not allocate a fresh benchmark evidence directory")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    scratch = fresh_scratch_dir()
    synthetic_dir = scratch / "synthetic"
    histogram_dir = scratch / "histogram"
    boxplot_dir = scratch / "boxplot"
    bar_dir = scratch / "bar"
    run_script("run_synthetic_benchmark.py", synthetic_dir)
    run_script("run_histogram_benchmark.py", histogram_dir)
    run_script("run_boxplot_benchmark.py", boxplot_dir)
    run_script("run_bar_benchmark.py", bar_dir)
    transmission_source = ROOT / "artifacts" / "nature_fig3_s41467-025-63143-5"
    if transmission_source.is_dir():
        subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "build_natcom_transmission_fig3_gallery_case.py"),
                "--source-dir",
                str(transmission_source),
                "--target-dir",
                str(GALLERY / "assets" / "cases" / "nature-63143-fig3"),
            ],
            cwd=ROOT,
            check=True,
        )
    natmed_case = GALLERY / "assets" / "cases" / "nature-protaide-boxplot"
    subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "build_natmed_box_case.py"),
            "--input",
            str(natmed_case / "original.png"),
            "--output-dir",
            str(natmed_case),
        ],
        cwd=ROOT,
        check=True,
    )
    heatmap_case = GALLERY / "assets" / "cases" / "nature-protaide-heatmap"
    subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "build_natmed_heatmap_case.py"),
            "--input",
            str(heatmap_case / "original.png"),
            "--source-data",
            str(heatmap_case / "source-data.xlsx"),
            "--output-dir",
            str(heatmap_case),
        ],
        cwd=ROOT,
        check=True,
    )
    dose_response_case = GALLERY / "assets" / "cases" / "nature-kahlous-dose-response"
    subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "build_natcom_dose_response_case.py"),
            "--pdf",
            str(dose_response_case / "source-article.pdf"),
            "--source-data",
            str(dose_response_case / "source-data.xlsx"),
            "--output-dir",
            str(dose_response_case),
        ],
        cwd=ROOT,
        check=True,
    )
    samples = [
        build_line(synthetic_dir),
        build_scatter(synthetic_dir),
        build_dose_response(),
        build_bar(bar_dir),
        build_horizontal_bar(bar_dir),
        build_stacked_bar(bar_dir),
        build_percent_stacked_bar(bar_dir),
        build_pie_case(),
        build_histogram(histogram_dir),
        build_heatmap(),
        build_boxplot(boxplot_dir),
        build_horizontal_boxplot(boxplot_dir),
        build_forest_plot(),
    ]
    china_mining_contour = build_china_mining_contour()
    if china_mining_contour is not None:
        samples.append(china_mining_contour)
    normalize_recreated_canvases(samples)
    build_manifest(samples)
    print(f"BASIC_GALLERY={GALLERY / 'data' / 'basics.json'}")


if __name__ == "__main__":
    main()

"""Build the gallery's first line/scatter case from one verified raster image.

The primary numeric table is always produced by the registered
``digitize_line_chart.py`` implementation.  The synthetic generator values are
used only afterwards, in a separate validation file, and never as extraction
input.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
GALLERY = ROOT / "gallery"
CASE_DIR = GALLERY / "assets" / "basics" / "line"
MANIFEST = GALLERY / "data" / "basics.json"

SOURCE_SHA256 = "04efe900130ee60e291fdff77374c2283a16b0a0f0ae7a6568e6e3d134991d84"
PLOT_BOUNDS = (78, 44, 474, 336)
X_ANCHORS = ((89.207547, 0.0), (462.792453, 10.0))
Y_ANCHORS = ((336.0, 0.0), (44.0, 70.0))
SAMPLE_VALUES = list(range(11))
SERIES = {
    "biodiversity": {"label": "biodiversity", "color": "#d62728", "marker": "s", "line_style": "-"},
    "economic_language": {"label": "economic language", "color": "#1f77b4", "marker": "^", "line_style": "--"},
    "context": {"label": "context", "color": "#7f7f7f", "marker": "o", "line_style": "-"},
}
SYNTHETIC_TRUTH = {
    "biodiversity": [26, 10, 9, 6, 8, 10, 14, 8, 6, 18, 10],
    "economic_language": [40, 33, 25, 32, 35, 30, 43, 44, 37, 37, 40],
    "context": [27, 13, 12, 14, 19, 20, 28, 35, 32, 28, 21],
}
SYNTHETIC_CONTEXT_ERROR = [16, 8, 8, 9, 12, 12, 15, 18, 15, 14, 11]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_checked(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def run_registered_pipeline(source: Path, work: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    preflight = work / "preflight-report.json"
    figure_spec = work / "figure-spec.json"
    run_checked(
        [
            sys.executable,
            str(SCRIPTS / "thu_digitizer.py"),
            "inspect",
            "--input",
            str(source),
            "--chart-type",
            "line",
            "--output-report",
            str(preflight),
            "--output-spec",
            str(figure_spec),
        ]
    )

    raw_csv = work / "registered-output.csv"
    raw_report_path = work / "extraction-report.json"
    raw_overlay = work / "registered-overlay.png"
    command = [
        sys.executable,
        str(SCRIPTS / "digitize_line_chart.py"),
        "--input",
        str(source),
        "--output-csv",
        str(raw_csv),
        "--report",
        str(raw_report_path),
        "--overlay",
        str(raw_overlay),
        "--x-px-min",
        str(X_ANCHORS[0][0]),
        "--x-value-min",
        str(X_ANCHORS[0][1]),
        "--x-px-max",
        str(X_ANCHORS[1][0]),
        "--x-value-max",
        str(X_ANCHORS[1][1]),
        "--y-px-min",
        str(Y_ANCHORS[0][0]),
        "--y-value-min",
        str(Y_ANCHORS[0][1]),
        "--y-px-max",
        str(Y_ANCHORS[1][0]),
        "--y-value-max",
        str(Y_ANCHORS[1][1]),
        "--plot-bounds",
        ",".join(str(value) for value in PLOT_BOUNDS),
        "--sample-values",
        ",".join(str(value) for value in SAMPLE_VALUES),
    ]
    for name in SERIES:
        command.extend(["--series", f"{name}={SERIES[name]['color']}"])
    command.extend(
        [
            "--color-tolerance",
            "24",
            "--sample-radius",
            "3",
            "--error-color",
            "#d0d0d0",
            "--error-tolerance",
            "18",
            "--error-min-span",
            "8",
            "--trace-mode",
            "sample",
        ]
    )
    run_checked(command)
    with raw_csv.open(newline="", encoding="utf-8") as handle:
        wide_rows = list(csv.DictReader(handle))
    return (
        json.loads(preflight.read_text(encoding="utf-8")),
        json.loads(figure_spec.read_text(encoding="utf-8")),
        json.loads(raw_report_path.read_text(encoding="utf-8")),
        wide_rows,
    )


def make_primary_rows(raw: dict[str, Any], wide_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    errors_by_x = {float(item["x"]): item for item in raw.get("error_bars", [])}
    rows: list[dict[str, Any]] = []
    for series_name, style in SERIES.items():
        observations = raw["samples"][series_name]
        for index, source_row in enumerate(wide_rows):
            x_value = float(source_row["x"])
            observation = observations[index]
            error = errors_by_x.get(x_value) if series_name == "context" else None
            error_extracted = bool(error and error.get("status") == "extracted")
            rows.append(
                {
                    "record_id": f"{series_name}-{index:02d}",
                    "kind": "point",
                    "series": series_name,
                    "series_label": style["label"],
                    "x": f"{x_value:g}",
                    "value": source_row[series_name],
                    "pixel_x": source_row["x_pixel"],
                    "pixel_y": observation.get("y_pixel"),
                    "confidence": observation.get("confidence"),
                    "candidate_pixels": observation.get("candidate_pixels"),
                    "color": style["color"],
                    "marker": style["marker"],
                    "line_style": style["line_style"],
                    "error_lower": error.get("lower") if error_extracted else "",
                    "error_upper": error.get("upper") if error_extracted else "",
                    "error_top_pixel_y": error.get("top_y_pixel") if error_extracted else "",
                    "error_bottom_pixel_y": error.get("bottom_y_pixel") if error_extracted else "",
                    "error_confidence": error.get("confidence") if error_extracted else "",
                    "error_status": "visible_endpoints_extracted" if error_extracted else ("not_applicable" if error is None else "not_extracted"),
                    "value_status": "calibrated_original_pixel_sample",
                    "shape": "circle",
                    "radius": 8,
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_truth_validation(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    validation_rows: list[dict[str, Any]] = []
    absolute_errors: list[float] = []
    by_series: dict[str, list[float]] = {name: [] for name in SERIES}
    for row in rows:
        series = row["series"]
        x_index = int(float(row["x"]))
        extracted = float(row["value"])
        truth = float(SYNTHETIC_TRUTH[series][x_index])
        error = abs(extracted - truth)
        absolute_errors.append(error)
        by_series[series].append(error)
        validation_rows.append(
            {
                "kind": "point",
                "series": series,
                "x": row["x"],
                "image_extracted_value": row["value"],
                "synthetic_truth_value": f"{truth:g}",
                "absolute_error": f"{error:.6f}",
                "validation_status": "independent_validation_only",
            }
        )
    validation = {
        "role": "independent_synthetic_truth_validation_only",
        "truth_source": "scripts/run_synthetic_benchmark.py::render_line",
        "point_mae": round(float(np.mean(absolute_errors)), 6),
        "point_max_abs_error": round(float(max(absolute_errors)), 6),
        "per_series_mae": {name: round(float(np.mean(values)), 6) for name, values in by_series.items()},
        "note": "Synthetic truth is compared only after image extraction and does not populate data.csv.",
    }
    return validation_rows, validation


def make_overlay(source: Path, rows: list[dict[str, Any]], target: Path) -> None:
    image = Image.open(source).convert("RGB")
    draw = ImageDraw.Draw(image)
    outlines = {"biodiversity": "#ffb000", "economic_language": "#d000ff", "context": "#00a978"}
    for row in rows:
        x = float(row["pixel_x"])
        y = float(row["pixel_y"])
        color = outlines[row["series"]]
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), outline=color, width=1)
        if row["series"] == "context" and row["error_status"] == "visible_endpoints_extracted":
            top = float(row["error_top_pixel_y"])
            bottom = float(row["error_bottom_pixel_y"])
            draw.line((x, top, x, bottom), fill="#00a978", width=1)
            draw.line((x - 3, top, x + 3, top), fill="#00a978", width=1)
            draw.line((x - 3, bottom, x + 3, bottom), fill="#00a978", width=1)
    image.save(target)


def make_recreation(rows: list[dict[str, Any]], target: Path) -> None:
    grouped = {name: sorted((row for row in rows if row["series"] == name), key=lambda row: float(row["x"])) for name in SERIES}
    x_values = [float(row["x"]) for row in grouped["context"]]
    context_values = np.asarray([float(row["value"]) for row in grouped["context"]])
    context_lower = np.asarray([float(row["error_lower"]) for row in grouped["context"]])
    context_upper = np.asarray([float(row["error_upper"]) for row in grouped["context"]])

    figure = plt.figure(figsize=(6, 4), dpi=100, facecolor="white")
    axis = figure.add_axes([0.13, 0.16, 0.66, 0.73])
    axis.set(title="Synthetic line chart", xlim=(-0.3, 10.3), ylim=(0, 70), xlabel="Year", ylabel="% of releases")
    axis.grid(axis="y", color="#e6e6e6", linewidth=0.7)
    axis.set_axisbelow(True)
    axis.tick_params(labelsize=8)
    context_artist = axis.errorbar(
        x_values,
        context_values,
        yerr=np.vstack([context_values - context_lower, context_upper - context_values]),
        color=SERIES["context"]["color"],
        ecolor="#d0d0d0",
        marker="o",
        linewidth=1.2,
        capsize=3,
        label=SERIES["context"]["label"],
    )
    red_rows = grouped["biodiversity"]
    red_artist, = axis.plot(
        [float(row["x"]) for row in red_rows],
        [float(row["value"]) for row in red_rows],
        color=SERIES["biodiversity"]["color"],
        marker="s",
        linewidth=1.2,
        label=SERIES["biodiversity"]["label"],
    )
    blue_rows = grouped["economic_language"]
    blue_artist, = axis.plot(
        [float(row["x"]) for row in blue_rows],
        [float(row["value"]) for row in blue_rows],
        color=SERIES["economic_language"]["color"],
        marker="^",
        linestyle="--",
        linewidth=1.2,
        label=SERIES["economic_language"]["label"],
    )
    axis.legend(
        [red_artist, blue_artist, context_artist.lines[0]],
        ["biodiversity", "economic language", "context"],
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        fontsize=7,
        frameon=False,
    )
    figure.savefig(target, dpi=100, facecolor="white")
    plt.close(figure)


def sample_manifest(validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": "line",
        "title": "折线散点图",
        "subtitle": "三个语义系列、标记与可见误差线",
        "status": "validated_local_stable",
        "statusLabel": "稳定 · 合成基准",
        "description": "从附件原始像素中恢复 biodiversity、economic language 与 context 的 33 个采样点，并单独记录 11 组浅灰误差线可见端点。",
        "metrics": [
            {"label": "点覆盖", "value": "33 / 33"},
            {"label": "误差线", "value": "11 / 11"},
            {"label": "验证 MAE", "value": f"{validation['point_mae']:.3f}"},
        ],
        "assets": {
            "original": "assets/basics/line/original.png",
            "overlay": "assets/basics/line/overlay.png",
            "recreated": "assets/basics/line/recreated.png",
            "data": "assets/basics/line/data.csv",
            "report": "assets/basics/line/report.json",
        },
        "styleSpec": {
            "renderer": "paper-native-geometry",
            "fidelity": "evidence_backed_style_reconstruction",
            "label": "原图像素提取 · 交互命中",
            "note": "复现底图来自提取值；悬停点读取 data.csv 中的坐标、像素证据与可见误差端点。",
            "canvas": {"width": 600, "height": 400},
            "fontFamily": "DejaVu Sans, Arial, sans-serif",
            "rasterEvidenceInteractive": True,
        },
    }


def update_manifest(sample: dict[str, Any]) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    samples = manifest["samples"]
    index = next((index for index, item in enumerate(samples) if item["id"] == "line"), 0)
    if samples and samples[index]["id"] == "line":
        samples[index] = sample
    else:
        samples.insert(0, sample)
    manifest["generated"] = date.today().isoformat()
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_case(source: Path, *, write_manifest: bool = False) -> dict[str, Any]:
    source = source.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    with Image.open(source) as image:
        if image.size != (600, 400):
            raise ValueError(f"expected the verified 600x400 chart, got {image.size[0]}x{image.size[1]}")
    CASE_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="thu-line-gallery-") as temporary:
        work = Path(temporary)
        preflight, figure_spec, raw, wide_rows = run_registered_pipeline(source, work)
        rows = make_primary_rows(raw, wide_rows)
        validation_rows, validation = make_truth_validation(rows)

        original_target = CASE_DIR / "original.png"
        if source != original_target.resolve():
            shutil.copy2(source, original_target)
        write_csv(CASE_DIR / "data.csv", rows)
        write_csv(CASE_DIR / "truth-validation.csv", validation_rows)
        make_overlay(original_target, rows, CASE_DIR / "overlay.png")
        make_recreation(rows, CASE_DIR / "recreated.png")

        shutil.copy2(work / "registered-output.csv", CASE_DIR / "registered-output.csv")
        shutil.copy2(work / "extraction-report.json", CASE_DIR / "extraction-report.json")
        (CASE_DIR / "preflight-report.json").write_text(json.dumps(preflight, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        figure_spec["verification"] = {
            "status": "verified_for_case",
            "plot_bounds_px": {"left": 78, "top": 44, "right": 474, "bottom": 336},
            "x_anchors": [{"pixel": pixel, "value": value} for pixel, value in X_ANCHORS],
            "y_anchors": [{"pixel": pixel, "value": value} for pixel, value in Y_ANCHORS],
            "series_colors": {name: style["color"] for name, style in SERIES.items()},
            "sample_values": SAMPLE_VALUES,
        }
        (CASE_DIR / "figure-spec.json").write_text(json.dumps(figure_spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    found_points = sum(item["found_samples"] for item in raw["series"])
    found_errors = sum(item.get("status") == "extracted" for item in raw["error_bars"])
    report = {
        "schema_version": 1,
        "status": "validated_local_stable",
        "run_id": f"line-{sha256(CASE_DIR / 'original.png')[:12]}",
        "source": {
            "file": "original.png",
            "sha256": sha256(CASE_DIR / "original.png"),
            "width": 600,
            "height": 400,
            "measurement_space": "original_raster_pixels",
            "resampling_applied": False,
        },
        "visible_extraction": {
            "route_id": "raster_line_color",
            "implementation": "scripts/digitize_line_chart.py",
            "implementation_sha256": sha256(SCRIPTS / "digitize_line_chart.py"),
            "trace_mode": "sample",
            "registered_output": "registered-output.csv",
            "registered_report": "extraction-report.json",
            "coordinate_provenance": "calibrated original-image pixels",
        },
        "coverage": {
            "points_found": found_points,
            "points_expected": 33,
            "error_bars_found": found_errors,
            "error_bars_expected": 11,
        },
        "calibration": raw["calibration"],
        "plot_bounds_px": raw["plot_bounds_px"],
        "series": raw["series"],
        "error_bar_interpretation": {
            "meaning": "visible endpoint geometry only",
            "not_claimed": "SD, SEM, confidence interval, or hidden endpoint reconstruction",
            "occlusion_note": "Where another mark covers the pale stroke, the reported endpoint is the furthest visible supported pixel.",
        },
        "validation": validation,
        "limitations": raw["limitations"],
    }
    (CASE_DIR / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sample = sample_manifest(validation)
    if write_manifest:
        update_manifest(sample)
    return sample


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="verified source raster")
    parser.add_argument("--update-manifest", action="store_true")
    parser.add_argument("--require-source-sha", action="store_true", help="require the exact user attachment bytes")
    args = parser.parse_args()
    if args.require_source_sha and sha256(args.input) != SOURCE_SHA256:
        raise SystemExit(f"source SHA-256 does not match the requested attachment: {sha256(args.input)}")
    sample = build_case(args.input, write_manifest=args.update_manifest)
    print(f"CASE={sample['id']}")
    print(f"SOURCE_SHA256={sha256(CASE_DIR / 'original.png')}")
    print(f"DATA={CASE_DIR / 'data.csv'}")


if __name__ == "__main__":
    main()

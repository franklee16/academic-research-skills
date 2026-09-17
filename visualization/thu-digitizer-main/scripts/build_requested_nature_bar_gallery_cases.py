"""Publish the requested Nature horizontal and stacked bar evidence cases.

The public CSVs contain only raster-derived geometry.  Official Source Data is
retained beside each case for independent validation and never fills a missing
bar or stack segment.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import re
from pathlib import Path, PureWindowsPath

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts" / "agents"
CASES = ROOT / "gallery" / "assets" / "cases"
MANIFEST = ROOT / "gallery" / "data" / "basics.json"
FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_ITALIC = Path(r"C:\Windows\Fonts\ariali.ttf")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def scrub_local_paths(value):
    if isinstance(value, dict):
        return {key: scrub_local_paths(item) for key, item in value.items()}
    if isinstance(value, list):
        return [scrub_local_paths(item) for item in value]
    if isinstance(value, str) and re.match(r"^[A-Za-z]:[\\/]", value):
        return PureWindowsPath(value).name
    return value


def publish_evidence(source: Path, target: Path) -> None:
    """Copy evidence while removing workstation-specific paths from JSON."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix.lower() == ".json":
        payload = scrub_local_paths(json.loads(source.read_text(encoding="utf-8")))
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    elif source.resolve() != target.resolve():
        copy(source, target)


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.is_file():
            return path
    raise FileNotFoundError("No canonical evidence file found: " + ", ".join(map(str, paths)))


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def font(size: int, *, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_ITALIC if italic else FONT_BOLD if bold else FONT
    return ImageFont.truetype(str(path), size)


def vertical_text(canvas: Image.Image, xy: tuple[int, int], value: str, size: int) -> None:
    face = font(size)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bounds = probe.textbbox((0, 0), value, font=face)
    label = Image.new("RGBA", (bounds[2] - bounds[0] + 8, bounds[3] - bounds[1] + 8), (255, 255, 255, 0))
    ImageDraw.Draw(label).text((4 - bounds[0], 4 - bounds[1]), value, font=face, fill="#222")
    label = label.rotate(90, expand=True, resample=Image.Resampling.BICUBIC)
    canvas.paste(label, (int(xy[0] - label.width / 2), int(xy[1] - label.height / 2)), label)


def build_horizontal_recreation(rows: list[dict], spec: dict) -> Image.Image:
    canvas = Image.new("RGB", (2001, 360), "white")
    draw = ImageDraw.Draw(canvas)
    panels = {panel["panel_id"]: panel for panel in spec["panels"]}
    titles = {
        "fig8a-temperature-sensitivity": "Temperature sensitivity in grid cells",
        "fig8a-regional-contribution": "Contribution to the regional temperature response",
    }
    tick_sets = {
        "fig8a-temperature-sensitivity": [(-0.004, 268.5), (-0.003, 374.167), (-0.002, 479.833), (-0.001, 585.5), (0.0, 691.167), (0.001, 796.833), (0.002, 902.5)],
        "fig8a-regional-contribution": [(-0.001, 1438.5), (0.0, 1654.0), (0.001, 1869.5)],
    }
    draw.text((197, 2), "a", font=font(30, bold=True), fill="#080808", anchor="ma")
    draw.rectangle((230, 44, 360, 81), fill="#e5e5e5")
    draw.text((238, 62), "NfN–SSP1", font=font(24), fill="#111", anchor="lm")
    for panel_id, panel in panels.items():
        left, top, right, bottom = map(float, panel["plot_bounds"])
        draw.text(((left + right) / 2, 15), titles[panel_id], font=font(28), fill="#111", anchor="mm")
        for tick, px in tick_sets[panel_id]:
            draw.line((px, top, px, bottom), fill="#b0b0b0", width=2)
            label = "0.000" if tick == 0 else f"{tick:.3f}".replace("-", "−")
            draw.text((px, bottom + 25), label, font=font(24), fill="#111", anchor="mm")
        draw.rectangle((left, top, right, bottom), outline="#111", width=2)
        anchors = panel["axes"][0]["anchors"]
        for anchor in anchors:
            draw.line((left - 10, anchor["pixel"], left, anchor["pixel"]), fill="#111", width=2)
            draw.text((left - 16, anchor["pixel"]), anchor["value"], font=font(24), fill="#111", anchor="rm")
    for row in rows:
        panel = panels[row["panel"]]
        baseline = next(anchor["pixel"] for anchor in panel["axes"][1]["anchors"] if anchor["value"] == 0) if any(anchor["value"] == 0 for anchor in panel["axes"][1]["anchors"]) else (691.0 if row["panel"] == "fig8a-temperature-sensitivity" else 1654.0)
        if row["value_status"] == "not_extracted":
            cy = next(anchor["pixel"] for anchor in panel["axes"][0]["anchors"] if anchor["value"] == row["category"])
            draw.line((baseline - 9, cy - 9, baseline + 9, cy + 9), fill="#f18f01", width=3)
            draw.line((baseline - 9, cy + 9, baseline + 9, cy - 9), fill="#f18f01", width=3)
            continue
        x, y = float(row["pixel_x"]), float(row["pixel_y"])
        width, height = float(row["width"]), float(row["height"])
        draw.rectangle((x, y, x + width, y + height), fill=row["fill"], outline="#111", width=2)
        lower, upper = float(row["error_lower_pixel"]), float(row["error_upper_pixel"])
        cy = y + height / 2
        draw.line((lower, cy, upper, cy), fill="#050505", width=2)
        draw.line((lower, cy - 4, lower, cy + 4), fill="#050505", width=2)
        draw.line((upper, cy - 4, upper, cy + 4), fill="#050505", width=2)
    return canvas


def build_horizontal_overlay(original: Image.Image, rows: list[dict], spec: dict) -> Image.Image:
    canvas = original.copy()
    draw = ImageDraw.Draw(canvas)
    panels = {panel["panel_id"]: panel for panel in spec["panels"]}
    for row in rows:
        if row["value_status"] == "not_extracted":
            panel = panels[row["panel"]]
            baseline = 691.0 if row["panel"] == "fig8a-temperature-sensitivity" else 1654.0
            cy = next(anchor["pixel"] for anchor in panel["axes"][0]["anchors"] if anchor["value"] == row["category"])
            draw.line((baseline - 9, cy - 9, baseline + 9, cy + 9), fill="#f18f01", width=3)
            draw.line((baseline - 9, cy + 9, baseline + 9, cy - 9), fill="#f18f01", width=3)
            continue
        x, y = float(row["pixel_x"]), float(row["pixel_y"])
        width, height = float(row["width"]), float(row["height"])
        draw.rectangle((x, y, x + width, y + height), outline="#ff00ff", width=3)
        lower, upper = float(row["error_lower_pixel"]), float(row["error_upper_pixel"])
        cy = y + height / 2
        draw.line((lower, cy, upper, cy), fill="#00b8d4", width=3)
    return canvas


def build_horizontal() -> dict:
    artifact = ARTIFACTS / "nature-70284-fig8a"
    target = CASES / "nature-70284-fig8a"
    target.mkdir(parents=True, exist_ok=True)
    measurement = first_existing(
        artifact / "original" / "41467_2026_70284_Fig8_HTML.png",
        target / "measurement-source.png",
    )
    if measurement != target / "measurement-source.png":
        copy(measurement, target / "measurement-source.png")
    measurement = target / "measurement-source.png"

    candidate_csv = first_existing(artifact / "extraction" / "fig8a-primary.csv", target / "candidate-data.csv")
    candidate_report = first_existing(artifact / "extraction" / "fig8a-report.json", target / "candidate-report.json")
    figure_spec = first_existing(artifact / "figure-spec.json", target / "figure-spec.json")
    copy(candidate_csv, target / "candidate-data.csv") if candidate_csv != target / "candidate-data.csv" else None
    publish_evidence(candidate_report, target / "candidate-report.json")
    publish_evidence(figure_spec, target / "figure-spec.json")
    for source, name in [
        (artifact / "preflight-report.json", "preflight-report.json"),
        (artifact / "validation" / "source-validation-report.json", "source-validation.json"),
        (artifact / "provenance" / "SOURCES.md", "SOURCES.md"),
        (artifact / "README.md", "README.md"),
    ]:
        if source.is_file():
            publish_evidence(source, target / name)

    full = Image.open(measurement).convert("RGB")
    original = full.crop((0, 0, 2001, 360))
    original.save(target / "original.png")
    overlay_source = first_existing(artifact / "extraction" / "fig8a-overlay.png", target / "overlay-full.png")
    recreation_source = first_existing(artifact / "extraction" / "fig8a-recreation.png", target / "recreated-full.png")
    if overlay_source != target / "overlay-full.png":
        copy(overlay_source, target / "overlay-full.png")
    if recreation_source != target / "recreated-full.png":
        copy(recreation_source, target / "recreated-full.png")
    Image.open(target / "overlay-full.png").convert("RGB").crop((0, 0, 2001, 360)).save(target / "overlay.png")
    Image.open(target / "recreated-full.png").convert("RGB").crop((0, 0, 2001, 360)).save(target / "recreated.png")

    spec = json.loads((target / "figure-spec.json").read_text(encoding="utf-8"))
    panel_by_id = {panel["panel_id"]: panel for panel in spec["panels"]}
    rows: list[dict] = []
    with (target / "candidate-data.csv").open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            panel = panel_by_id[raw["panel_id"]]
            category_index = next(
                index for index, anchor in enumerate(panel["axes"][0]["anchors"])
                if anchor["value"] == raw["category"]
            )
            y_center = float(panel["axes"][0]["anchors"][category_index]["pixel"])
            fill = panel["series"][0]["bar_colors_by_category"][category_index]
            authorized = raw["numeric_output_authorized"].lower() == "true"
            start = float(raw["start_pixel"]) if authorized else None
            end = float(raw["end_pixel"]) if authorized else None
            rows.append({
                "kind": "rect",
                "shape": "rect",
                "panel": raw["panel_id"],
                "series": raw["metric"],
                "category": raw["category"],
                "scenario": raw["scenario"],
                "unit": raw["unit"],
                "value": raw["value"],
                "error_lower": raw["error_lower_value"],
                "error_upper": raw["error_upper_value"],
                "error_status": raw["error_status"],
                "error_lower_pixel": raw["error_lower_pixel"],
                "error_upper_pixel": raw["error_upper_pixel"],
                "confidence": raw["confidence"],
                "numeric_use_allowed": "true" if authorized else "false",
                "value_status": "visible_bar_with_interval" if authorized else "not_extracted",
                "reason": raw["unauthorized_reason"],
                "pixel_x": round(min(start, end), 3) if authorized else "",
                "pixel_y": round(y_center - 9, 3) if authorized else "",
                "width": round(abs(end - start), 3) if authorized else "",
                "height": 18 if authorized else "",
                "fill": fill,
            })
    write_csv(target / "data.csv", rows)
    build_horizontal_overlay(original, rows, spec).save(target / "overlay.png")
    build_horizontal_recreation(rows, spec).save(target / "recreated.png")
    report = json.loads((target / "candidate-report.json").read_text(encoding="utf-8"))
    public_report = {
        "schema_version": 1,
        "case_id": "nature-70284-fig8a",
        "status": "partial_visible",
        "route": report["route"],
        "expected_detection_count_passed": report["expected_detection_count_passed"],
        "source_data_role": "independent_validation_only",
        "measurement": {
            "file": "measurement-source.png",
            "sha256": digest(measurement),
            "size": [2001, 1235],
            "gallery_crop": [0, 0, 2001, 360],
            "resampling_applied": False,
        },
        "coverage": {"visible_slots": 16, "authorized_bars": 13, "not_extracted": 3, "fraction": 0.8125},
        "interval_coverage": {"authorized_bars_with_intervals": 13, "authorized_bars": 13},
        "validation": {"status": "not_comparable", "numerically_compared": 0, "filled_from_external_data": 0},
        "limitations": report["limitations"],
    }
    (target / "report.json").write_text(json.dumps(public_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "id": "bar-horizontal",
        "title": "横向发散柱状图",
        "subtitle": "双面板均值与 Bootstrap 区间",
        "status": "partial_visible",
        "statusLabel": "部分可见提取 · 13/16",
        "description": "从 Nature Communications Fig. 8a 的原始像素恢复两组发散横柱及区间；3 个被黑色区间线切断的浅色柱保留为未提取。",
        "metrics": [{"label": "授权柱", "value": "13 / 16"}, {"label": "区间覆盖", "value": "13 / 13"}],
        "journal": "Nature Communications",
        "figure": "Fig. 8a",
        "articleTitle": "Climate response to Nature Future scenarios in a regional Earth System Model",
        "articleUrl": "https://www.nature.com/articles/s41467-026-70284-8",
        "figureUrl": "https://www.nature.com/articles/s41467-026-70284-8/figures/8",
        "styleSpec": {
            "renderer": "paper-native-geometry",
            "fidelity": "visible_geometry_candidate",
            "label": "论文原生画布 · 部分可见提取",
            "note": "复现只绘制 13 个授权柱及其可见 Bootstrap 区间；橙色叉号对应 3 个未授权槽位。",
            "canvas": {"width": 2001, "height": 360},
            "rasterEvidenceInteractive": True,
        },
        "assets": {name: f"assets/cases/nature-70284-fig8a/{filename}" for name, filename in {
            "original": "original.png", "overlay": "overlay.png", "recreated": "recreated.png", "data": "data.csv", "report": "report.json"
        }.items()},
    }


def build_stacked_recreation(rows: list[dict], colors: dict[str, str]) -> Image.Image:
    canvas = Image.new("RGB", (709, 600), "white")
    draw = ImageDraw.Draw(canvas)
    plot_left, plot_right, top, baseline = 142, 446, 78, 489
    for tick in range(0, 101, 20):
        y = baseline - tick * (baseline - top) / 100
        draw.line((plot_left, y, plot_right, y), fill="#e8e8e8", width=1)
        draw.text((plot_left - 12, y), str(tick), font=font(15), fill="#555", anchor="rm")
    draw.line((plot_left, top, plot_left, baseline), fill="#333", width=2)
    draw.line((plot_left, baseline, plot_right, baseline), fill="#333", width=2)
    centers = {"G": 188.0, "K": 294.5, "L": 400.5}
    for row in rows:
        if row["value_status"] == "not_extracted":
            continue
        x = centers[row["category"]]
        y1, y2 = float(row["pixel_y"]), float(row["pixel_y"]) + float(row["height"])
        draw.rectangle((x - 44, y1, x + 45, y2), fill=colors[row["series"]])
    for category, x in centers.items():
        draw.text((x, baseline + 32), category, font=font(26), fill="#444", anchor="mm")
    draw.text((24, 5), "b", font=font(42, bold=True), fill="#050505")
    draw.text((355, 29), "Archaeal genera (top 10) grouped by center", font=font(25), fill="#111", anchor="mm")
    vertical_text(canvas, (72, 286), "Percentage", 20)
    for index, (series, color) in enumerate(colors.items()):
        y = 86 + index * 38
        draw.rectangle((489, y - 10, 508, y + 9), fill=color)
        draw.text((526, y), series, font=font(17, italic=series != "other"), fill="#111", anchor="lm")
    return canvas


def build_stacked() -> dict:
    artifact = ARTIFACTS / "nature-36825-fig1b"
    target = CASES / "nature-36825-fig1b"
    target.mkdir(parents=True, exist_ok=True)
    measurement = first_existing(artifact / "figure1-official.png", target / "measurement-source.png")
    if measurement != target / "measurement-source.png":
        copy(measurement, target / "measurement-source.png")
    measurement = target / "measurement-source.png"
    inputs = {
        "candidate-data.csv": artifact / "extraction-all-statuses.csv",
        "candidate-report.json": artifact / "extraction-report.json",
        "figure-spec.json": artifact / "figure-spec.json",
        "preflight-report.json": artifact / "preflight-report.json",
        "source-validation.json": artifact / "source-validation-summary.json",
        "SOURCES.md": artifact / "SOURCES.md",
        "README.md": artifact / "README.md",
    }
    for name, artifact_path in inputs.items():
        source = first_existing(artifact_path, target / name)
        publish_evidence(source, target / name)

    panel_crop = (1250, 0, 1959, 600)
    Image.open(measurement).convert("RGB").crop(panel_crop).save(target / "original.png")
    overlay_source = first_existing(artifact / "overlay.png", target / "overlay-full.png")
    if overlay_source != target / "overlay-full.png":
        copy(overlay_source, target / "overlay-full.png")
    Image.open(target / "overlay-full.png").convert("RGB").crop(panel_crop).save(target / "overlay.png")

    candidate = json.loads((target / "candidate-report.json").read_text(encoding="utf-8"))
    colors = {item["name"]: item["color"] for item in candidate["series"]}
    centers = {item["name"]: float(item["center_pixel"]) - panel_crop[0] for item in candidate["categories"]}
    rows: list[dict] = []
    with (target / "candidate-data.csv").open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            extracted = raw["status"] == "extracted"
            start = float(raw["start_pixel"]) if extracted else None
            end = float(raw["end_pixel"]) if extracted else None
            rows.append({
                "kind": "rect",
                "shape": "rect",
                "series": raw["series"],
                "category": raw["category"],
                "value": raw["value"],
                "start_value": raw["start_value"],
                "end_value": raw["end_value"],
                "confidence": raw["confidence"],
                "numeric_use_allowed": "false",
                "value_status": "visible_segment_candidate" if extracted else "not_extracted",
                "reason": raw["reason"],
                "pixel_x": round(centers[raw["category"]] - 44, 3) if extracted else "",
                "pixel_y": round(min(start, end), 3) if extracted else "",
                "width": 89 if extracted else "",
                "height": round(abs(end - start), 3) if extracted else "",
                "fill": colors[raw["series"]],
            })
    write_csv(target / "data.csv", rows)
    build_stacked_recreation(rows, colors).save(target / "recreated.png")
    public_report = {
        "schema_version": 1,
        "case_id": "nature-36825-fig1b",
        "status": "low_confidence",
        "route": "raster_bar_candidate",
        "expected_detection_count_passed": False,
        "source_data_role": "independent_validation_only",
        "measurement": {
            "file": "measurement-source.png", "sha256": digest(measurement), "size": [1959, 2040],
            "gallery_crop": list(panel_crop), "resampling_applied": False,
        },
        "coverage": {"requested_slots": 33, "visible_segment_candidates": 29, "not_extracted": 4},
        "numeric_output_authorized": False,
        "validation": {"status": "not_comparable_css_normalization_not_reproduced", "filled_from_external_data": 0},
        "limitations": [
            "The report-level low-confidence gate applies to all candidate values.",
            "Four absent or unsupported series/category slots remain not_extracted and are not treated as zero.",
            "One-pixel white separators prevent the visible fills from passing the strict percent-stack total gate.",
        ],
    }
    (target / "report.json").write_text(json.dumps(public_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "id": "bar-stacked",
        "title": "百分比堆叠柱状图",
        "subtitle": "三中心古菌属组成",
        "status": "low_confidence",
        "statusLabel": "低置信候选 · 29/33",
        "description": "从 Nature Communications Fig. 1b 恢复 29 个可见堆叠段；4 个未检出槽位保留为空，整例维持低置信候选而不宣称数值已授权。",
        "metrics": [{"label": "可见候选段", "value": "29 / 33"}, {"label": "缺失保持", "value": "4"}],
        "journal": "Nature Communications",
        "figure": "Fig. 1b",
        "articleTitle": "Clinical NEC prevention practices drive different microbiome profiles and functional responses in the preterm intestine",
        "articleUrl": "https://www.nature.com/articles/s41467-023-36825-1",
        "figureUrl": "https://www.nature.com/articles/s41467-023-36825-1/figures/1",
        "styleSpec": {
            "renderer": "paper-native-geometry",
            "fidelity": "visible_geometry_candidate",
            "label": "论文原生画布 · 低置信候选",
            "note": "透明命中层展示 29 个可见候选段；4 个未检出槽位不会被补零或由源数据回填。",
            "canvas": {"width": 709, "height": 600},
            "rasterEvidenceInteractive": True,
        },
        "assets": {name: f"assets/cases/nature-36825-fig1b/{filename}" for name, filename in {
            "original": "original.png", "overlay": "overlay.png", "recreated": "recreated.png", "data": "data.csv", "report": "report.json"
        }.items()},
    }


def replace_samples(replacements: list[dict]) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_id = {sample["id"]: sample for sample in replacements}
    manifest["samples"] = [by_id.get(sample["id"], sample) for sample in manifest["samples"]]
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    replace_samples([build_horizontal(), build_stacked()])
    print("published requested Nature bar gallery cases")


if __name__ == "__main__":
    main()

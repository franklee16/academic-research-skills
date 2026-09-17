from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CASE_ID = "nature-20563-fig6f"
CROP_TOP = 2240
CANVAS_SIZE = (1798, 310)
BLUE = "#0b72b9"
GRID = "#e0e1e2"
TEXT = "#272727"


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text_lf(path: Path, text: str) -> None:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    path.write_bytes(normalized.encode("utf-8"))


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def centered_text(draw: ImageDraw.ImageDraw, xy, text: str, text_font, fill=TEXT):
    draw.text(xy, text, font=text_font, fill=fill, anchor="mm")


def load_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sanitize_public_json(value, source_root: Path):
    if isinstance(value, dict):
        return {key: sanitize_public_json(item, source_root) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_public_json(item, source_root) for item in value]
    if isinstance(value, str):
        normalized = value.replace("\\", "/")
        normalized_root = str(source_root.resolve()).replace("\\", "/").rstrip("/")
        prefix = f"{normalized_root}/"
        if normalized.lower().startswith(prefix.lower()):
            return normalized[len(prefix) :]
    return value


def draw_recreation(rows: list[dict], report: dict, output: Path) -> None:
    canvas = Image.new("RGB", CANVAS_SIZE, "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((0, 0), "f", font=font(36, bold=True), fill=TEXT)
    centered_text(
        draw,
        (CANVAS_SIZE[0] / 2, 22),
        "Orientation of the force w.r.t extrusion site (angle θ)",
        font(35),
    )

    maxima = {"D30": 2500.0, "D15": 1200.0, "D10": 350.0}
    panels = {panel["panel_id"]: panel for panel in report["panels"]}
    for panel_id in ("D30", "D15", "D10"):
        panel = panels[panel_id]
        cx = float(panel["center_original_pixels"][0])
        cy = float(panel["center_original_pixels"][1]) - CROP_TOP
        calibration = panel["calibration"]
        sx = float(calibration["x_px_per_radial_unit"])
        sy = float(calibration["y_px_per_radial_unit"])
        maximum = maxima[panel_id]

        for tick in [float(ring["radial_value"]) for ring in calibration["rings"]] + [maximum]:
            rx = sx * tick
            ry = sy * tick
            draw.arc((cx - rx, cy - ry, cx + rx, cy + ry), 180, 360, fill=GRID, width=2)

        for angle in range(0, 181, 30):
            radians = math.radians(angle)
            x = cx + sx * maximum * math.cos(radians)
            y = cy - sy * maximum * math.sin(radians)
            draw.line((cx, cy, x, y), fill=GRID, width=2)
            label_x = cx + (sx * maximum + 24) * math.cos(radians)
            label_y = cy - (sy * maximum + 20) * math.sin(radians)
            centered_text(draw, (label_x, label_y), str(angle), font(18), fill="#4c4c4c")

        centered_text(draw, (cx, cy + 18), "0", font(18), fill="#4c4c4c")
        for ring in calibration["rings"]:
            tick = float(ring["radial_value"])
            centered_text(draw, (cx + sx * tick, cy + 18), f"{tick:g}", font(18), fill="#4c4c4c")

        panel_rows = [row for row in rows if row["panel_id"] == panel_id]
        for row in panel_rows:
            value = float(row["radial_value"])
            start = math.radians(float(row["theta_start_deg"]))
            end = math.radians(float(row["theta_end_deg"]))
            p1 = (cx + sx * value * math.cos(start), cy - sy * value * math.sin(start))
            p2 = (cx + sx * value * math.cos(end), cy - sy * value * math.sin(end))
            draw.line((cx, cy, *p1), fill=BLUE, width=4)
            draw.line((cx, cy, *p2), fill=BLUE, width=4)
            draw.line((*p1, *p2), fill=BLUE, width=4)

        centered_text(
            draw,
            (cx, 292),
            f"D = {panel['patch_diameter_um']} μm",
            font(26),
        )

    canvas.save(output)


def write_notes(target: Path) -> None:
    write_text_lf(
        target / "README.md",
        """# Nature Communications 2021 Fig. 6f evidence package

Status: `candidate`.

`data.csv` is the primary image-derived extraction. It contains 30 visible
18-degree polar-histogram bins across the D = 30, 15, and 10 μm panels, with
the calibrated radial value, approximate raster uncertainty, and original-
raster chord endpoints. `recreated.png` and the interactive gallery view are
driven only by this CSV and retained calibration; neither imports the official
workbook.

The recoverable representation is the visible bin interval and outer radial
chord. The original force-vector observations and an author-side exact count
table are not recoverable from the raster. The radial axis has printed numeric
ticks but no explicit unit label, so the CSV uses
`displayed_histogram_count`.

The official caption says Source Data for panels c–f are provided, but the
downloaded workbook has `Figure 6d` and `Figure 6e` sheets and no verifiable
`Figure 6f` polar-bin table. The separate validation report therefore records
`metric_absent_in_source_workbook`; it never fills or changes the primary CSV.
""",
    )
    write_text_lf(
        target / "SOURCES.md",
        """# Source and reuse note — Nature Communications Fig. 6f

- Article: “Adhesion-mediated heterogeneous actin organization governs apoptotic cell extrusion” (Nature Communications, 2021), DOI `10.1038/s41467-020-20563-9`.
- Article page: https://www.nature.com/articles/s41467-020-20563-9
- Figure page: https://www.nature.com/articles/s41467-020-20563-9/figures/6
- Full-size official figure: https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41467-020-20563-9/MediaObjects/41467_2020_20563_Fig6_HTML.png
- Official Source Data: https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-020-20563-9/MediaObjects/41467_2020_20563_MOESM14_ESM.xlsx
- Retrieved: 2026-07-21.

The article is licensed under the Creative Commons Attribution 4.0
International License. The gallery crop, extraction overlay, and recreation
are adaptations and must retain attribution, link the licence, and indicate
that changes were made.
""",
    )


def build(source: Path, target: Path) -> None:
    required = {
        "panel-f-crop.png",
        "panel-f-overlay.png",
        "figure6-original.png",
        "data.csv",
        "derived-direction-summary.csv",
        "report.json",
        "preflight-report.json",
        "figure-spec.json",
        "source-validation.csv",
        "source-validation-report.json",
    }
    missing = sorted(name for name in required if not (source / name).exists())
    if missing:
        raise SystemExit(f"Missing source evidence: {', '.join(missing)}")
    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty evidence directory: {target}")
    target.mkdir(parents=True, exist_ok=True)

    copies = {
        "panel-f-crop.png": "original.png",
        "panel-f-overlay.png": "overlay.png",
        "figure6-original.png": "measurement-source.png",
        "data.csv": "data.csv",
        "derived-direction-summary.csv": "derived-direction-summary.csv",
        "preflight-report.json": "preflight-report.json",
        "figure-spec.json": "figure-spec.json",
        "source-validation.csv": "source-validation.csv",
        "source-validation-report.json": "source-validation-report.json",
    }
    for src_name, dst_name in copies.items():
        source_path = source / src_name
        target_path = target / dst_name
        if source_path.suffix.lower() == ".json":
            payload = json.loads(source_path.read_text(encoding="utf-8"))
            write_text_lf(
                target_path,
                json.dumps(sanitize_public_json(payload, source), indent=2, ensure_ascii=False),
            )
        elif source_path.suffix.lower() == ".csv":
            write_text_lf(target_path, source_path.read_text(encoding="utf-8"))
        else:
            shutil.copy2(source_path, target_path)

    rows = load_rows(source / "data.csv")
    report = json.loads((source / "report.json").read_text(encoding="utf-8"))
    draw_recreation(rows, report, target / "recreated.png")

    report["public_gallery"] = {
        "case_id": CASE_ID,
        "primary_csv": "data.csv",
        "primary_csv_source": "image_derived_only",
        "original_asset": "original.png",
        "original_asset_role": "review_crop_not_measurement_source",
        "measurement_source": "measurement-source.png",
        "overlay_asset": "overlay.png",
        "recreation_asset": "recreated.png",
        "recreation_driven_by": "data.csv",
        "source_validation_separate": True,
        "original_and_recreation_canvas": list(CANVAS_SIZE),
    }
    write_text_lf(
        target / "report.json",
        json.dumps(report, indent=2, ensure_ascii=False),
    )
    write_notes(target)

    manifest = {
        "schema_version": 1,
        "case_id": CASE_ID,
        "status": "candidate",
        "primary_csv": "data.csv",
        "row_count": len(rows),
        "canvas": list(CANVAS_SIZE),
        "assets": {
            path.name: file_hash(path)
            for path in sorted(target.iterdir())
            if path.is_file() and path.name != "manifest.json"
        },
    }
    write_text_lf(
        target / "manifest.json",
        json.dumps(manifest, indent=2, ensure_ascii=False),
    )
    print(json.dumps({"case_id": CASE_ID, "rows": len(rows), "target": str(target)}))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path("outputs/natcom-s41467-020-20563-9-fig6f"),
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=Path(f"gallery/assets/cases/{CASE_ID}"),
    )
    args = parser.parse_args()
    build(args.source_dir.resolve(), args.target_dir.resolve())


if __name__ == "__main__":
    main()

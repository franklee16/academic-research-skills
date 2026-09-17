"""Publish the Fig. 3c marker-line evidence as a gallery case.

The three curve panels come from the immutable candidate FigureSpec run.  The
local cyan/green dot fields remain the previously extracted visible component
geometry from the same raster.  No article workbook or hidden source values are
used.  Static and interactive recreations share the merged primary CSV.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
CASE_ID = "nature-56055-fig3c"
OUT = ROOT / "gallery" / "assets" / "cases" / CASE_ID
DEFAULT_CASE_ROOT = ROOT / "outputs" / "interlayer-distance-panel-c"
DEFAULT_SPEC_RUN = DEFAULT_CASE_ROOT / "spec-runs" / "marker-line-spec-db310817cbeba0b3"
DEFAULT_RECREATION_RUN = DEFAULT_CASE_ROOT / "recreation-runs" / "line-recreation-f15e4f9e64a16310"

PANEL_STYLE = {
    "spontaneous_curvature": {"label": "Spontaneous curvature", "colour": "#fb8177"},
    "surface_reconstruction": {"label": "Surface reconstruction", "colour": "#2ba3ca"},
    "rigid": {"label": "Rigid", "colour": "#808080"},
}

FIELDS = [
    "kind",
    "series",
    "category",
    "x",
    "value",
    "pixel_x",
    "pixel_y",
    "radius",
    "fill",
    "confidence",
    "value_status",
    "candidate_value",
    "pixel_uncertainty",
    "value_uncertainty",
    "x2",
    "y2",
    "stroke",
    "stroke_width",
    "shape",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def strip_line_end_whitespace(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    cleaned = "\n".join(line.rstrip() for line in text.splitlines())
    if text.endswith(("\n", "\r")):
        cleaned += "\n"
    path.write_text(cleaned, encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def retained_local_dot_rows() -> list[dict[str, Any]]:
    data_path = OUT / "data.csv"
    if not data_path.is_file():
        raise FileNotFoundError(
            "the existing case data.csv is required once to retain its 57 visible local-dot components"
        )
    rows = [
        row
        for row in read_rows(data_path)
        if row.get("kind") == "point" and row.get("series", "").startswith("local dot field")
    ]
    if len(rows) != 57:
        raise ValueError(f"expected 57 retained local-dot components, found {len(rows)}")
    return [{field: row.get(field, "") for field in FIELDS} for row in rows]


def panel_directory(spec_run: Path, panel_manifest: dict[str, Any]) -> Path:
    directory = spec_run / panel_manifest["relative_directory"]
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    return directory


def curve_rows(spec_run: Path, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for panel_manifest in manifest["panels"]:
        panel_id = panel_manifest["panel_id"]
        if panel_id not in PANEL_STYLE:
            raise ValueError(f"unexpected marker-line panel {panel_id!r}")
        panel_dir = panel_directory(spec_run, panel_manifest)
        report = load_json(panel_dir / "report.json")
        if not report.get("numeric_output_authorized"):
            raise ValueError(f"panel {panel_id} has not authorized numeric output")
        series_name = next(iter(report["series"]))
        observations = report["series"][series_name]["observations"]
        style = PANEL_STYLE[panel_id]
        points: list[dict[str, Any]] = []
        for observation in observations:
            if observation["status"] != "extracted" or observation.get("value") is None:
                raise ValueError(f"panel {panel_id} contains a non-authorized declared sample")
            point = {
                "kind": "point",
                "series": style["label"],
                "category": "visible curve marker",
                "x": observation["x"],
                "value": observation["value"],
                "pixel_x": observation["x_pixel"],
                "pixel_y": observation["y_pixel"],
                "radius": 7,
                "fill": style["colour"],
                "confidence": observation["confidence"],
                "value_status": "candidate_marker_centre_global_path_v0.2.0",
                "candidate_value": observation["candidate_value"],
                "pixel_uncertainty": observation["pixel_uncertainty"],
                "value_uncertainty": observation["value_uncertainty"],
                "shape": "circle",
            }
            points.append(point)
            rows.append(point)
        for first, second in zip(points, points[1:]):
            rows.append(
                {
                    "kind": "line",
                    "series": style["label"],
                    "category": "visible marker connection",
                    "x": first["x"],
                    "value": "visible path between extracted markers",
                    "pixel_x": first["pixel_x"],
                    "pixel_y": first["pixel_y"],
                    "x2": second["pixel_x"],
                    "y2": second["pixel_y"],
                    "fill": "none",
                    "stroke": style["colour"],
                    "stroke_width": 2,
                    "value_status": "connection_of_authorized_visible_markers",
                    "shape": "line",
                }
            )
        summary = report["series"][series_name]["summary"]
        summaries.append(
            {
                "panel_id": panel_id,
                "series": style["label"],
                "run_id": report["run_id"],
                "algorithm_version": report["algorithm_version"],
                "implementation_sha256": report["implementation_sha256"],
                "declared_sample_slots": summary["total"],
                "authorized_markers": summary["extracted"],
                "mean_confidence": summary["mean_confidence"],
                "evidence": f"marker-line-evidence/{panel_id}/evidence.csv",
                "candidate_report": f"marker-line-evidence/{panel_id}/report.json",
            }
        )
    return rows, summaries


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def make_overlay(source: Path, rows: list[dict[str, Any]], target: Path) -> None:
    image = Image.open(source).convert("RGB")
    draw = ImageDraw.Draw(image)
    for row in rows:
        if row["kind"] == "line" and row.get("category") == "visible marker connection":
            draw.line(
                (float(row["pixel_x"]), float(row["pixel_y"]), float(row["x2"]), float(row["y2"])),
                fill=row["stroke"],
                width=2,
            )
    for row in rows:
        if row["kind"] != "point" or row.get("category") != "visible curve marker":
            continue
        x = float(row["pixel_x"])
        y = float(row["pixel_y"])
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), outline="#00a95c", width=2)
    image.save(target)


def copy_evidence(spec_run: Path, manifest: dict[str, Any]) -> None:
    for panel_manifest in manifest["panels"]:
        panel_id = panel_manifest["panel_id"]
        source_dir = panel_directory(spec_run, panel_manifest)
        target_dir = OUT / "marker-line-evidence" / panel_id
        target_dir.mkdir(parents=True, exist_ok=True)
        for name in ("configuration.json", "data.csv", "evidence.csv", "overlay.png", "report.json"):
            source_path = source_dir / name
            target_path = target_dir / name
            if name == "report.json":
                public_report = load_json(source_path)
                public_report["input_file"] = "../../original.png"
                write_json(target_path, public_report)
            else:
                shutil.copy2(source_path, target_path)


def publish_manifests(manifest: dict[str, Any], recreation_manifest: dict[str, Any]) -> None:
    public_spec_manifest = json.loads(json.dumps(manifest))
    public_spec_manifest["source"]["file"] = "original.png"
    public_spec_manifest["figure_spec"]["file"] = "figure-spec.json"
    for panel in public_spec_manifest["panels"]:
        panel["relative_directory"] = f"marker-line-evidence/{panel['panel_id']}"
    write_json(OUT / "figure-spec-run-manifest.json", public_spec_manifest)

    panel_by_run_id = {panel["run_id"]: panel["panel_id"] for panel in manifest["panels"]}
    public_recreation_manifest = json.loads(json.dumps(recreation_manifest))
    public_data = []
    for source_file, digest in public_recreation_manifest["identity"]["data"]:
        matches = [panel_id for run_id, panel_id in panel_by_run_id.items() if run_id in source_file]
        if len(matches) != 1:
            raise ValueError(f"cannot map recreation input to one published panel: {source_file}")
        public_data.append([f"marker-line-evidence/{matches[0]}/data.csv", digest])
    public_recreation_manifest["identity"]["data"] = public_data
    write_json(OUT / "recreation-manifest.json", public_recreation_manifest)


def build_case(spec_run: Path, recreation_run: Path, source: Path, figure_spec: Path, recreation_spec: Path) -> dict[str, Any]:
    spec_run = spec_run.resolve()
    recreation_run = recreation_run.resolve()
    source = source.resolve()
    manifest = load_json(spec_run / "manifest.json")
    if not manifest.get("numeric_output_authorized"):
        raise ValueError("the FigureSpec run does not authorize numeric output")
    if manifest["source"]["sha256"] != sha256(source):
        raise ValueError("source hash does not match the immutable FigureSpec run")
    recreation_manifest = load_json(recreation_run / "manifest.json")
    if recreation_manifest.get("status") != "rendered":
        raise ValueError("recreation run is not complete")
    with Image.open(source) as image:
        if image.size != (1495, 1278):
            raise ValueError(f"expected the original 1495x1278 canvas, got {image.size}")

    local_rows = retained_local_dot_rows()
    extracted_rows, panel_summaries = curve_rows(spec_run, manifest)
    primary_rows = extracted_rows + local_rows
    curve_points = [row for row in primary_rows if row["category"] == "visible curve marker"]
    if len(curve_points) != 168:
        raise ValueError(f"expected 168 authorized curve markers, found {len(curve_points)}")

    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, OUT / "original.png")
    shutil.copy2(recreation_run / "recreated.png", OUT / "recreated.png")
    shutil.copy2(recreation_run / "recreated.svg", OUT / "recreated.svg")
    strip_line_end_whitespace(OUT / "recreated.svg")
    shutil.copy2(recreation_run / "recreated.pdf", OUT / "recreated.pdf")
    shutil.copy2(figure_spec, OUT / "figure-spec.json")
    shutil.copy2(recreation_spec, OUT / "recreation-spec.json")
    publish_manifests(manifest, recreation_manifest)
    write_csv(OUT / "data.csv", primary_rows)
    make_overlay(source, extracted_rows, OUT / "overlay.png")
    copy_evidence(spec_run, manifest)

    report = {
        "schema_version": 1,
        "case_id": CASE_ID,
        "status": "visible_geometry_candidate",
        "route": "raster_marker_line_candidate_plus_retained_visible_dot_components",
        "source": {
            "file": "original.png",
            "sha256": sha256(OUT / "original.png"),
            "width": 1495,
            "height": 1278,
            "measurement_space": "original_raster_pixels",
            "resampling_applied": False,
        },
        "visible_extraction": {
            "implementation": "scripts/candidate_digitize_marker_line.py",
            "runner": "scripts/run_marker_line_spec.py",
            "figure_spec": "figure-spec.json",
            "figure_spec_run_id": manifest["run_id"],
            "numeric_output_authorized": True,
            "panels": panel_summaries,
        },
        "coverage": {
            "declared_curve_marker_slots": 168,
            "authorized_curve_markers": 168,
            "curve_marker_coverage": 1.0,
            "retained_local_dot_components": len(local_rows),
        },
        "primary_csv": {
            "file": "data.csv",
            "curve_points": 168,
            "curve_connections": 165,
            "local_dot_components": len(local_rows),
            "source_data_used": False,
        },
        "recreation": {
            "renderer": "scripts/recreate_line_figure.py",
            "run_id": recreation_manifest["run_id"],
            "manifest": "recreation-manifest.json",
            "png": "recreated.png",
            "svg": "recreated.svg",
            "pdf": "recreated.pdf",
            "source_raster_embedded": False,
        },
        "source_data_role": "not_used",
        "limitations": [
            "Curve values are visible compact-marker centres at verified sample positions, not source simulation records.",
            "Lines connect adjacent authorized marker centres and do not recover hidden model parameters.",
            "The 57 local cyan/green components retain visible position, colour and radius only; no hidden variable is inferred.",
            "The marker-line route remains a candidate pending held-out real cases and a matched WebPlotDigitizer comparison.",
        ],
    }
    write_json(OUT / "report.json", report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-run", type=Path, default=DEFAULT_SPEC_RUN)
    parser.add_argument("--recreation-run", type=Path, default=DEFAULT_RECREATION_RUN)
    parser.add_argument("--source", type=Path, default=DEFAULT_CASE_ROOT / "source.png")
    parser.add_argument("--figure-spec", type=Path, default=DEFAULT_CASE_ROOT / "candidate-figure-spec.json")
    parser.add_argument("--recreation-spec", type=Path, default=DEFAULT_CASE_ROOT / "recreation-spec.json")
    args = parser.parse_args()
    report = build_case(args.spec_run, args.recreation_run, args.source, args.figure_spec, args.recreation_spec)
    print(
        json.dumps(
            {
                "status": report["status"],
                "case_id": report["case_id"],
                "curve_markers": report["coverage"]["authorized_curve_markers"],
                "local_dot_components": report["coverage"]["retained_local_dot_components"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

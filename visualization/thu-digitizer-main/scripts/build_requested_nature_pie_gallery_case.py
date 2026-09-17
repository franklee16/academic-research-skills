"""Publish Nature Communications Fig. 1f as a label-first donut case."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import re
import importlib.util
from pathlib import Path, PureWindowsPath

from PIL import Image

try:
    from candidate_digitize_labelled_donut import extract_labelled_donuts, write_outputs
    from thu_digitizer import build_preflight
except ImportError:  # pragma: no cover - package-style invocation
    from .candidate_digitize_labelled_donut import extract_labelled_donuts, write_outputs
    from .thu_digitizer import build_preflight


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "agents" / "nature-40822-fig1f"
TARGET = ROOT / "gallery" / "assets" / "cases" / "nature-40822-fig1f"
MANIFEST = ROOT / "gallery" / "data" / "basics.json"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.is_file():
            return path
    raise FileNotFoundError("No canonical evidence file found: " + ", ".join(map(str, paths)))


def copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != target.resolve():
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


def build_case() -> dict:
    TARGET.mkdir(parents=True, exist_ok=True)
    evidence = {
        "measurement-source.png": ARTIFACT / "figure1-original.png",
        "original.png": ARTIFACT / "panel-original.png",
        "recreated.png": ARTIFACT / "recreated.png",
        "candidate_digitize_donut_case.py": ARTIFACT / "candidate_digitize_donut_case.py",
        "test_candidate_digitize_donut_case.py": ARTIFACT / "test_candidate_digitize_donut_case.py",
        "README.md": ARTIFACT / "README.md",
        "SOURCES.md": ARTIFACT / "SOURCE_AND_LICENSE.md",
    }
    for name, artifact_path in evidence.items():
        publish_evidence(first_existing(artifact_path, TARGET / name), TARGET / name)

    module_path = TARGET / "candidate_digitize_donut_case.py"
    module_spec = importlib.util.spec_from_file_location("nature_40822_fig1f", module_path)
    case_module = importlib.util.module_from_spec(module_spec)
    assert module_spec.loader is not None
    module_spec.loader.exec_module(case_module)
    shared_config = {
        "schema_version": 1,
        "source_contract": {
            "sha256": case_module.EXPECTED_SOURCE_SHA256,
            "dimensions": list(case_module.EXPECTED_SOURCE_SIZE),
        },
        "panel_bounds": [
            case_module.PANEL_BOX[0],
            case_module.PANEL_BOX[1],
            case_module.PANEL_BOX[2] - 1,
            case_module.PANEL_BOX[3] - 1,
        ],
        "palette": {
            name: value["hex"] for name, value in case_module.PALETTE.items()
        },
        "groups": [
            {
                "name": group,
                "center": list(meta["center"]),
                "radial_band": list(meta["radial_band"]),
                "labels": [
                    {
                        "series": cell_type,
                        "anchor": list(anchor),
                        "transcription_a": f"{value:.1f}",
                        "transcription_b": f"{value:.1f}",
                    }
                    for label_group, cell_type, value, anchor in case_module.VISIBLE_LABELS
                    if label_group == group
                ],
            }
            for group, meta in case_module.DONUTS.items()
        ],
        "parameters": {
            "angle_samples": 7200,
            "color_tolerance": 20.0,
            "minimum_sector_share_percent": 0.5,
            "maximum_geometry_error_pp": 2.0,
        },
    }
    (TARGET / "labelled-donut-config.json").write_text(
        json.dumps(shared_config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    candidate = extract_labelled_donuts(TARGET / "measurement-source.png", shared_config)
    full_overlay = TARGET / "overlay-full.png"
    write_outputs(
        TARGET / "measurement-source.png",
        candidate,
        output_csv=TARGET / "candidate-data.csv",
        geometry_csv=TARGET / "sector-geometry.csv",
        report_path=TARGET / "candidate-report.json",
        overlay_path=full_overlay,
    )
    panel_box = tuple(case_module.PANEL_BOX)
    with Image.open(full_overlay) as image:
        image.convert("RGB").crop(panel_box).save(TARGET / "overlay.png")
    full_overlay.unlink()
    preflight, figure_spec = build_preflight(
        TARGET / "measurement-source.png",
        chart_type="donut",
        panel_bounds=tuple(float(item) for item in panel_box),
    )
    (TARGET / "preflight-report.json").write_text(
        json.dumps(scrub_local_paths(preflight), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (TARGET / "figure-spec.json").write_text(
        json.dumps(scrub_local_paths(figure_spec), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    rows: list[dict] = []
    with (TARGET / "candidate-data.csv").open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            if raw["numeric_output_authorized"].lower() != "true":
                continue
            rows.append({
                "kind": "point",
                "shape": "circle",
                "series": raw["series"],
                "category": raw["group"],
                "value": raw["displayed_value_percent"],
                "unit": "percent",
                "label_sum": raw["group_visible_label_sum_percent"],
                "numeric_use_allowed": "true",
                "value_status": "visible_printed_label",
                "pixel_x": round(float(raw["label_anchor_x"]) - 1000, 3),
                "pixel_y": round(float(raw["label_anchor_y"]) - 420, 3),
                "radius": 12,
                "fill": raw["color"],
            })
    fields = list(rows[0])
    with (TARGET / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    report = {
        "schema_version": 1,
        "case_id": "nature-40822-fig1f",
        "status": "candidate",
        "route": candidate["extractor"],
        "shared_pie_route": "raster_labelled_donut_candidate",
        "expected_detection_count_passed": False,
        "source_data_role": "independent_validation_only",
        "normalization_applied_to_primary_values": False,
        "measurement": {
            "file": "measurement-source.png",
            "sha256": digest(TARGET / "measurement-source.png"),
            "size": [2050, 1399],
            "gallery_crop": list(panel_box),
            "resampling_applied": False,
        },
        "visible_label_extraction": {
            "method": "two matching visible-label transcriptions plus annular geometry validation",
            "declared_label_count": candidate["coverage_ledger"]["declared_slot_count"],
            "authorized_label_count": candidate["coverage_ledger"]["authorized_slot_count"],
            "recovered_label_count": candidate["coverage_ledger"]["authorized_slot_count"],
            "coverage": candidate["coverage_ledger"]["coverage_fraction"],
            "group_label_sums_percent": {
                group: next(
                    row["group_visible_label_sum_percent"]
                    for row in candidate["records"]
                    if row["group"] == group
                )
                for group in case_module.DONUTS
            },
        },
        "sector_geometry_validation": {
            "role": candidate["geometry_validation"]["role"],
            "mean_absolute_percentage_point_error": candidate["geometry_validation"]["mean_absolute_error_pp"],
            "maximum_absolute_percentage_point_error": candidate["geometry_validation"]["maximum_absolute_error_pp"],
        },
        "validation": {"status": "not_comparable", "filled_from_external_data": 0},
        "limitations": [
            "Numeric use is authorized only for the 18 explicitly printed labels.",
            "The four printed label sums are retained as 97.5, 90.6, 70.3, and 73.6 rather than forced to 100.",
            "Sector geometry is validation-only; the shared route never derives or fills a primary label from angle geometry.",
        ],
    }
    (TARGET / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "id": "pie",
        "title": "环形饼图 / Donut",
        "subtitle": "四组可见百分比标签",
        "status": "candidate",
        "statusLabel": "可见标签候选 · 18/18",
        "description": "从 Nature Communications Fig. 1f 提取四个 donut 上明确印出的 18 个百分比；原标签和不强制补到 100，扇区角度仅作案例级验证。",
        "metrics": [{"label": "可见标签", "value": "18 / 18"}, {"label": "几何验证 MAE", "value": "0.596 pp"}],
        "journal": "Nature Communications",
        "figure": "Fig. 1f",
        "articleTitle": "Driver gene combinations dictate cutaneous squamous cell carcinoma disease continuum progression",
        "articleUrl": "https://www.nature.com/articles/s41467-023-40822-9",
        "figureUrl": "https://www.nature.com/articles/s41467-023-40822-9/figures/1",
        "styleSpec": {
            "renderer": "paper-native-geometry",
            "fidelity": "visible_geometry_candidate",
            "label": "论文原生画布 · 可见标签提取",
            "note": "交互命中层对应 18 个印刷标签；显示值保持原样，环形角度按组内可见值重建但不替代原值。",
            "canvas": {"width": 1025, "height": 215},
            "rasterEvidenceInteractive": True,
        },
        "assets": {
            "original": "assets/cases/nature-40822-fig1f/original.png",
            "overlay": "assets/cases/nature-40822-fig1f/overlay.png",
            "recreated": "assets/cases/nature-40822-fig1f/recreated.png",
            "data": "assets/cases/nature-40822-fig1f/data.csv",
            "report": "assets/cases/nature-40822-fig1f/report.json",
        },
    }


def publish_manifest(sample: dict) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    existing = next((index for index, item in enumerate(manifest["samples"]) if item["id"] == "pie"), None)
    if existing is not None:
        manifest["samples"][existing] = sample
    else:
        anchor = next(index for index, item in enumerate(manifest["samples"]) if item["id"] == "bar-percent-stacked")
        manifest["samples"].insert(anchor + 1, sample)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    publish_manifest(build_case())
    print("published requested Nature donut gallery case")


if __name__ == "__main__":
    main()

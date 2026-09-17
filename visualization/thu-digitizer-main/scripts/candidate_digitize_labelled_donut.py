"""Candidate extraction for pie/donut charts with visible numeric labels.

The caller supplies verified group centres, annular bands, palette colours,
label anchors, and two independent transcriptions of each visible label.  The
script authorizes only matching transcriptions whose normalized label share is
consistent with independently sampled sector geometry.  It never forces a
group total to 100 and never invents an unlabeled sector value.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw

try:
    from extraction_contract import build_coverage_ledger
except ImportError:  # pragma: no cover - package-style invocation
    from .extraction_contract import build_coverage_ledger


ALGORITHM = "candidate_labelled_donut_annular_validation"
ALGORITHM_VERSION = "1.0.0"
NUMBER = re.compile(r"^[+\-]?(?:\d+(?:\.\d*)?|\.\d+)$")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _rgb(value: str) -> tuple[int, int, int]:
    text = value.strip().lstrip("#")
    if len(text) != 6:
        raise ValueError("palette colours must use #RRGGBB")
    try:
        return tuple(int(text[index : index + 2], 16) for index in (0, 2, 4))
    except ValueError as error:
        raise ValueError("palette colours must use #RRGGBB") from error


def _number(value: Any) -> float:
    text = str(value).strip().removesuffix("%").strip()
    if not NUMBER.fullmatch(text):
        raise ValueError(f"visible label is not a plain numeric percentage: {value!r}")
    return float(text)


def _bounds(value: Any, *, width: int, height: int, name: str) -> tuple[int, int, int, int]:
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"{name} must contain four inclusive integer bounds")
    left, top, right, bottom = (int(item) for item in value)
    if not (0 <= left < right < width and 0 <= top < bottom < height):
        raise ValueError(f"{name} must fit the original {width}x{height} raster")
    return left, top, right, bottom


def _circular_components(indices: np.ndarray, count: int) -> list[np.ndarray]:
    if not len(indices):
        return []
    chunks = np.split(indices, np.where(np.diff(indices) > 1)[0] + 1)
    if len(chunks) > 1 and chunks[0][0] == 0 and chunks[-1][-1] == count - 1:
        chunks = [np.concatenate((chunks[-1], chunks[0]))] + chunks[1:-1]
    return chunks


def sample_annular_geometry(
    rgb: np.ndarray,
    *,
    center: tuple[int, int],
    radial_band: tuple[int, int],
    palette: dict[str, str],
    angle_samples: int,
    tolerance: float,
    minimum_sector_share_percent: float,
) -> dict[str, Any]:
    """Measure visible colour support without receiving label values/counts."""

    if angle_samples < 360:
        raise ValueError("angle_samples must be at least 360")
    if tolerance <= 0:
        raise ValueError("colour tolerance must be positive")
    inner, outer = radial_band
    if not 0 < inner <= outer:
        raise ValueError("radial_band must satisfy 0 < inner <= outer")
    height, width = rgb.shape[:2]
    cx, cy = center
    if cx - outer < 0 or cy - outer < 0 or cx + outer >= width or cy + outer >= height:
        raise ValueError("donut radial band must fit the original raster")

    names = list(palette)
    colours = np.asarray([_rgb(palette[name]) for name in names], dtype=float)
    angles = np.linspace(-math.pi, math.pi, angle_samples, endpoint=False)
    votes = np.zeros((angle_samples, len(names)), dtype=np.int16)
    for radius in range(inner, outer + 1):
        xs = np.rint(cx + radius * np.cos(angles)).astype(int)
        ys = np.rint(cy + radius * np.sin(angles)).astype(int)
        pixels = rgb[ys, xs].astype(float)
        distances = np.sqrt(
            np.sum((pixels[:, None, :] - colours[None, :, :]) ** 2, axis=2)
        )
        nearest = np.argmin(distances, axis=1)
        accepted = distances[np.arange(angle_samples), nearest] <= tolerance
        votes[np.arange(angle_samples)[accepted], nearest[accepted]] += 1

    classification = np.argmax(votes, axis=1)
    classified = np.max(votes, axis=1) > 0
    masks: dict[str, np.ndarray] = {}
    rejected = []
    for colour_index, name in enumerate(names):
        indices = np.flatnonzero(classified & (classification == colour_index))
        mask = np.zeros(angle_samples, dtype=bool)
        for component in _circular_components(indices, angle_samples):
            share = 100.0 * len(component) / angle_samples
            if share >= minimum_sector_share_percent:
                mask[component] = True
            else:
                rejected.append(
                    {
                        "series": name,
                        "angle_count": int(len(component)),
                        "full_circle_share_percent": share,
                        "reason": "below_minimum_sector_share",
                    }
                )
        masks[name] = mask
    union = np.logical_or.reduce(list(masks.values()))
    accepted_count = int(np.count_nonzero(union))
    sectors = []
    for name, mask in masks.items():
        count = int(np.count_nonzero(mask))
        if not count:
            continue
        unit_angles = angles[mask]
        mid_angle = math.atan2(
            float(np.mean(np.sin(unit_angles))), float(np.mean(np.cos(unit_angles)))
        )
        sectors.append(
            {
                "series": name,
                "color": palette[name],
                "classified_angle_count": count,
                "geometry_share_percent": 100.0 * count / accepted_count,
                "mid_angle_degrees": math.degrees(mid_angle),
                "component_count": len(
                    _circular_components(np.flatnonzero(mask), angle_samples)
                ),
                "status": "validation_geometry_only",
            }
        )
    return {
        "center": list(center),
        "radial_band": list(radial_band),
        "angle_samples": angle_samples,
        "classified_coverage": accepted_count / angle_samples,
        "sectors": sectors,
        "rejected_support": rejected,
    }


def extract_labelled_donuts(
    input_path: Path,
    config: dict[str, Any],
) -> dict[str, Any]:
    input_path = Path(input_path)
    with Image.open(input_path) as source:
        image = source.convert("RGB")
    rgb = np.asarray(image)
    source_sha = _sha256(input_path)
    source_contract = config.get("source_contract", {})
    if source_contract.get("sha256") and source_contract["sha256"] != source_sha:
        raise ValueError("source SHA-256 does not match the configured original raster")
    if source_contract.get("dimensions") and list(image.size) != list(
        source_contract["dimensions"]
    ):
        raise ValueError("source dimensions do not match the configured original raster")

    panel_bounds = _bounds(
        config["panel_bounds"], width=image.width, height=image.height, name="panel_bounds"
    )
    palette = dict(config.get("palette", {}))
    if not palette:
        raise ValueError("palette must contain at least one named colour")
    for colour in palette.values():
        _rgb(colour)
    groups = list(config.get("groups", []))
    if not groups:
        raise ValueError("groups must contain at least one pie/donut")

    parameters = dict(config.get("parameters", {}))
    angle_samples = int(parameters.get("angle_samples", 3600))
    tolerance = float(parameters.get("color_tolerance", 24.0))
    minimum_sector_share = float(parameters.get("minimum_sector_share_percent", 0.5))
    transcription_tolerance = float(parameters.get("transcription_tolerance", 1e-9))
    geometry_error_max = float(parameters.get("maximum_geometry_error_pp", 3.0))
    if transcription_tolerance < 0 or geometry_error_max <= 0:
        raise ValueError("transcription and geometry tolerances must be valid")

    geometry_by_group: dict[str, dict[str, Any]] = {}
    declared_labels: list[dict[str, Any]] = []
    group_names: set[str] = set()
    for group in groups:
        name = str(group.get("name", "")).strip()
        if not name or name in group_names:
            raise ValueError("group names must be non-empty and unique")
        group_names.add(name)
        center = tuple(int(item) for item in group["center"])
        radial_band = tuple(int(item) for item in group["radial_band"])
        if len(center) != 2 or len(radial_band) != 2:
            raise ValueError("center and radial_band must each contain two integers")
        geometry_by_group[name] = sample_annular_geometry(
            rgb,
            center=center,  # type: ignore[arg-type]
            radial_band=radial_band,  # type: ignore[arg-type]
            palette=palette,
            angle_samples=angle_samples,
            tolerance=tolerance,
            minimum_sector_share_percent=minimum_sector_share,
        )
        series_seen: set[str] = set()
        for label in group.get("labels", []):
            series = str(label.get("series", "")).strip()
            if series not in palette:
                raise ValueError(f"label series {series!r} is absent from the palette")
            if series in series_seen:
                raise ValueError(f"duplicate visible label for {name}/{series}")
            series_seen.add(series)
            anchor = tuple(int(item) for item in label["anchor"])
            if len(anchor) != 2:
                raise ValueError("label anchor must contain x,y original pixels")
            if not (
                panel_bounds[0] <= anchor[0] <= panel_bounds[2]
                and panel_bounds[1] <= anchor[1] <= panel_bounds[3]
            ):
                raise ValueError(f"label anchor for {name}/{series} is outside panel_bounds")
            first = _number(label.get("transcription_a"))
            second = _number(label.get("transcription_b"))
            declared_labels.append(
                {
                    "group": name,
                    "series": series,
                    "color": palette[series],
                    "label_anchor_x": anchor[0],
                    "label_anchor_y": anchor[1],
                    "transcription_a": first,
                    "transcription_b": second,
                    "transcriptions_match": abs(first - second) <= transcription_tolerance,
                }
            )

    matched_totals: dict[str, float] = {}
    for group_name in group_names:
        matched_totals[group_name] = sum(
            row["transcription_a"]
            for row in declared_labels
            if row["group"] == group_name and row["transcriptions_match"]
        )

    records = []
    comparisons = []
    for row in declared_labels:
        geometry = next(
            (
                sector
                for sector in geometry_by_group[row["group"]]["sectors"]
                if sector["series"] == row["series"]
            ),
            None,
        )
        value = row["transcription_a"] if row["transcriptions_match"] else None
        total = matched_totals[row["group"]]
        normalized = 100.0 * value / total if value is not None and total > 0 else None
        geometry_error = (
            abs(normalized - geometry["geometry_share_percent"])
            if normalized is not None and geometry is not None
            else None
        )
        if not row["transcriptions_match"]:
            status = "low_confidence"
            reason_code = "ambiguous_geometry"
            reason = "the two visible-label transcriptions disagree"
        elif geometry is None or geometry["component_count"] != 1:
            status = "low_confidence"
            reason_code = "no_supported_geometry"
            reason = "no unique matching visible sector geometry"
        elif geometry_error is None or geometry_error > geometry_error_max:
            status = "low_confidence"
            reason_code = "calibration_geometry_conflict"
            reason = "visible label is inconsistent with independently sampled sector geometry"
        else:
            status = "extracted"
            reason_code = "visible_label_verified"
            reason = "matching transcriptions and independent annular geometry validation"
        authorized = status == "extracted"
        record = {
            **row,
            "status": status,
            "reason_code": reason_code,
            "reason": reason,
            "displayed_value_percent": value if authorized else None,
            "group_visible_label_sum_percent": total,
            "normalized_visible_label_share_validation_only": normalized,
            "geometry_share_percent_validation_only": (
                geometry["geometry_share_percent"] if geometry is not None else None
            ),
            "geometry_error_pp": geometry_error,
            "numeric_output_authorized": authorized,
            "values_normalized_or_completed": False,
        }
        records.append(record)
        if geometry_error is not None:
            comparisons.append(geometry_error)

    ledger = build_coverage_ledger(records, slot_fields=("group", "series"))
    if ledger["authorized_slot_count"] == ledger["declared_slot_count"]:
        status = "candidate"
    elif ledger["authorized_slot_count"]:
        status = "partial_visible"
    else:
        status = "low_confidence"
    canonical_config = json.dumps(config, sort_keys=True, separators=(",", ":"))
    run_id = hashlib.sha256(
        f"{ALGORITHM_VERSION}:{source_sha}:{canonical_config}".encode("utf-8")
    ).hexdigest()[:16]
    return {
        "schema_version": 1,
        "extractor": ALGORITHM,
        "algorithm_version": ALGORITHM_VERSION,
        "deterministic_run_id": run_id,
        "status": status,
        "numeric_output_authorized": ledger["authorized_slot_count"] > 0,
        "numeric_authorization_scope": (
            "all_declared_visible_labels"
            if ledger["authorized_slot_count"] == ledger["declared_slot_count"]
            else "authorized_records_only"
            if ledger["authorized_slot_count"]
            else "none"
        ),
        "input": {
            "file": input_path.name,
            "sha256": source_sha,
            "dimensions": list(image.size),
            "coordinate_space": "original_raster_pixels",
            "resampled_for_measurement": False,
        },
        "panel_bounds": list(panel_bounds),
        "parameters": {
            "angle_samples": angle_samples,
            "color_tolerance": tolerance,
            "minimum_sector_share_percent": minimum_sector_share,
            "transcription_tolerance": transcription_tolerance,
            "maximum_geometry_error_pp": geometry_error_max,
        },
        "recoverable_representation": "explicitly visible numeric labels validated against visible sector geometry",
        "primary_values_normalized_or_forced_to_100": False,
        "records": records,
        "geometry_by_group": geometry_by_group,
        "coverage_ledger": ledger,
        "geometry_validation": {
            "comparison_count": len(comparisons),
            "mean_absolute_error_pp": float(np.mean(comparisons)) if comparisons else None,
            "maximum_absolute_error_pp": max(comparisons) if comparisons else None,
            "role": "validation_only_never_fills_or_normalizes_a_label",
        },
        "limitations": [
            "The route requires two verified transcriptions of every declared visible label.",
            "It does not discover OCR labels, infer unlabeled sectors, or recover source observations.",
            "Displayed values remain unchanged even when their group sum differs from 100.",
            "Sector geometry is normalized only for independent validation and never replaces primary labels.",
        ],
    }


def write_outputs(
    input_path: Path,
    report: dict[str, Any],
    *,
    output_csv: Path,
    geometry_csv: Path,
    report_path: Path,
    overlay_path: Path,
) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    primary_fields = [
        "group",
        "series",
        "color",
        "status",
        "reason_code",
        "reason",
        "displayed_value_percent",
        "group_visible_label_sum_percent",
        "label_anchor_x",
        "label_anchor_y",
        "numeric_output_authorized",
        "values_normalized_or_completed",
        "normalized_visible_label_share_validation_only",
        "geometry_share_percent_validation_only",
        "geometry_error_pp",
    ]
    with output_csv.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=primary_fields)
        writer.writeheader()
        for record in report["records"]:
            writer.writerow({field: record.get(field, "") for field in primary_fields})

    geometry_fields = [
        "group",
        "series",
        "color",
        "classified_angle_count",
        "geometry_share_percent",
        "mid_angle_degrees",
        "component_count",
        "status",
    ]
    with geometry_csv.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=geometry_fields)
        writer.writeheader()
        for group, geometry in report["geometry_by_group"].items():
            for sector in geometry["sectors"]:
                writer.writerow({"group": group, **sector})

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with Image.open(input_path) as source:
        overlay = source.convert("RGB")
    draw = ImageDraw.Draw(overlay)
    for group, geometry in report["geometry_by_group"].items():
        cx, cy = geometry["center"]
        inner, outer = geometry["radial_band"]
        draw.ellipse((cx - outer, cy - outer, cx + outer, cy + outer), outline="#00a6ff", width=2)
        draw.ellipse((cx - inner, cy - inner, cx + inner, cy + inner), outline="#00a6ff", width=1)
    for record in report["records"]:
        x, y = record["label_anchor_x"], record["label_anchor_y"]
        colour = "#00a65a" if record["numeric_output_authorized"] else "#d000d0"
        draw.rectangle((x - 5, y - 5, x + 5, y + 5), outline=colour, width=2)
    overlay_path.parent.mkdir(parents=True, exist_ok=True)
    overlay.save(overlay_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    parser.add_argument("--geometry-csv", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--overlay", required=True, type=Path)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    report = extract_labelled_donuts(args.input, config)
    write_outputs(
        args.input,
        report,
        output_csv=args.output_csv,
        geometry_csv=args.geometry_csv,
        report_path=args.report,
        overlay_path=args.overlay,
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "numeric_output_authorized": report["numeric_output_authorized"],
                "authorized_label_count": report["coverage_ledger"]["authorized_slot_count"],
            }
        )
    )


if __name__ == "__main__":
    main()

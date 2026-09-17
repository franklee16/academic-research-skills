"""Case-local Fig. 1f donut evidence builder.

This file is deliberately outside the shared extractor path.  THU Digitizer's
registry marks pie/donut charts unsupported.  Consequently, the only primary
numeric values emitted here are the percentages visibly printed beside the
four donuts.  Annular colour sampling is retained as validation-only geometry;
it is never used to replace or complete a printed value.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ALGORITHM = "case_local_visible_label_donut_geometry"
ALGORITHM_VERSION = "0.1.0"
EXPECTED_SOURCE_SHA256 = (
    "4dd50564058d2823dfe740ec3df49d6f451088cebd402b51d9890fdfc3282e46"
)
EXPECTED_SOURCE_SIZE = (2050, 1399)
PANEL_BOX = (1000, 420, 2025, 635)

# Exact flat colours observed in the official 2050 x 1399 PNG.  The nearby PDF
# vectors encode the same semantic palette with small colour-space differences.
PALETTE = {
    "TSK": {"rgb": (239, 102, 51), "hex": "#ef6633", "pdf_hex": "#ee6632"},
    "Tumor_KC_Diff": {"rgb": (121, 154, 185), "hex": "#799ab9", "pdf_hex": "#7899b8"},
    "Tumor_KC_Basal": {"rgb": (84, 202, 245), "hex": "#54caf5", "pdf_hex": "#58caf5"},
    "Tumor_KC_Cyc": {"rgb": (157, 204, 128), "hex": "#9dcc80", "pdf_hex": "#9cca7f"},
    "Normal_KC_Cyc": {"rgb": (207, 223, 231), "hex": "#cfdfe7", "pdf_hex": "#cddde6"},
    "Normal_KC_Basal": {"rgb": (241, 169, 62), "hex": "#f1a93e", "pdf_hex": "#f0a83f"},
    "Normal_KC_Diff": {"rgb": (246, 199, 79), "hex": "#f6c74f", "pdf_hex": "#f5c64f"},
}

DONUTS = {
    "Normal": {"center": (1169, 535), "radial_band": (52, 65)},
    "AK": {"center": (1405, 536), "radial_band": (52, 65)},
    "Primary": {"center": (1645, 535), "radial_band": (52, 65)},
    "MET": {"center": (1860, 535), "radial_band": (52, 65)},
}

# Values manually transcribed twice from the official full-size raster and
# checked against the figure rendering embedded on PDF page 3.  These are
# explicit visible labels, not source-workbook values and not inferred angles.
VISIBLE_LABELS = [
    ("Normal", "Normal_KC_Diff", 59.5, (1118, 542)),
    ("Normal", "Tumor_KC_Cyc", 16.6, (1227, 454)),
    ("Normal", "Tumor_KC_Basal", 18.9, (1248, 516)),
    ("Normal", "TSK", 2.5, (1227, 592)),
    ("AK", "Normal_KC_Diff", 48.7, (1327, 512)),
    ("AK", "Tumor_KC_Diff", 9.2, (1410, 443)),
    ("AK", "Tumor_KC_Cyc", 3.3, (1456, 469)),
    ("AK", "Tumor_KC_Basal", 22.2, (1490, 535)),
    ("AK", "TSK", 7.2, (1441, 594)),
    ("Primary", "Normal_KC_Diff", 10.3, (1584, 447)),
    ("Primary", "Tumor_KC_Diff", 25.9, (1720, 478)),
    ("Primary", "Tumor_KC_Basal", 17.5, (1648, 616)),
    ("Primary", "TSK", 16.6, (1572, 538)),
    ("MET", "Normal_KC_Diff", 6.6, (1811, 452)),
    ("MET", "Normal_KC_Basal", 1.8, (1856, 443)),
    ("MET", "Tumor_KC_Diff", 7.2, (1895, 453)),
    ("MET", "Tumor_KC_Basal", 19.6, (1944, 538)),
    ("MET", "TSK", 38.4, (1788, 594)),
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_run_id(source_sha256: str, parameters: dict) -> str:
    payload = json.dumps(
        {
            "algorithm": ALGORITHM,
            "version": ALGORITHM_VERSION,
            "source_sha256": source_sha256,
            "parameters": parameters,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def _circular_components(indices: np.ndarray, n_angles: int) -> list[np.ndarray]:
    if len(indices) == 0:
        return []
    chunks = np.split(indices, np.where(np.diff(indices) > 1)[0] + 1)
    if len(chunks) > 1 and chunks[0][0] == 0 and chunks[-1][-1] == n_angles - 1:
        chunks = [np.concatenate((chunks[-1], chunks[0]))] + chunks[1:-1]
    return chunks


def sample_annular_geometry(
    rgb: np.ndarray,
    center: tuple[int, int],
    radial_band: tuple[int, int],
    *,
    angle_samples: int = 7200,
    tolerance: float = 20.0,
    minimum_sector_share_percent: float = 0.5,
) -> dict:
    """Sample flat sector colours across an annular band.

    The routine knows colours and verified geometry only.  It receives no
    expected values, sector counts, or labels.  Tiny isolated classifications
    below the declared minimum share are retained as rejected noise.
    """

    angles = np.linspace(-math.pi, math.pi, angle_samples, endpoint=False)
    palette_names = list(PALETTE)
    palette_rgb = np.asarray([PALETTE[name]["rgb"] for name in palette_names], dtype=float)
    votes = np.zeros((angle_samples, len(palette_names)), dtype=np.int16)
    x0, y0 = center
    r0, r1 = radial_band
    for radius in range(r0, r1 + 1):
        xs = np.rint(x0 + radius * np.cos(angles)).astype(int)
        ys = np.rint(y0 + radius * np.sin(angles)).astype(int)
        pixels = rgb[ys, xs].astype(float)
        distances = np.sqrt(np.sum((pixels[:, None, :] - palette_rgb[None, :, :]) ** 2, axis=2))
        nearest = np.argmin(distances, axis=1)
        accepted = distances[np.arange(angle_samples), nearest] <= tolerance
        votes[np.arange(angle_samples)[accepted], nearest[accepted]] += 1

    class_index = np.argmax(votes, axis=1)
    classified = np.max(votes, axis=1) > 0
    initial_coverage = float(np.mean(classified))
    accepted_masks: dict[str, np.ndarray] = {}
    rejected: list[dict] = []

    # Keep only colour support that forms a sector-sized circular run.  This
    # removes isolated anti-alias classifications without inventing gaps.
    for colour_index, name in enumerate(palette_names):
        indices = np.flatnonzero(classified & (class_index == colour_index))
        mask = np.zeros(angle_samples, dtype=bool)
        for component in _circular_components(indices, angle_samples):
            share = 100.0 * len(component) / angle_samples
            if share >= minimum_sector_share_percent:
                mask[component] = True
            else:
                rejected.append(
                    {
                        "cell_type": name,
                        "angle_count": int(len(component)),
                        "full_circle_share_percent": share,
                        "reason": "below_minimum_sector_share",
                    }
                )
        accepted_masks[name] = mask

    accepted_union = np.logical_or.reduce(list(accepted_masks.values()))
    accepted_total = int(np.sum(accepted_union))
    sectors = []
    if accepted_total:
        for name, mask in accepted_masks.items():
            count = int(np.sum(mask))
            if not count:
                continue
            component_list = _circular_components(np.flatnonzero(mask), angle_samples)
            # A legitimate donut series should appear as one sector.  Multiple
            # runs are exposed, never silently merged into a value claim.
            unit_angles = angles[mask]
            mean_angle = math.atan2(float(np.mean(np.sin(unit_angles))), float(np.mean(np.cos(unit_angles))))
            sectors.append(
                {
                    "cell_type": name,
                    "color_hex": PALETTE[name]["hex"],
                    "classified_angle_count": count,
                    "geometry_share_percent": 100.0 * count / accepted_total,
                    "mid_angle_deg_image": math.degrees(mean_angle),
                    "component_count": len(component_list),
                    "status": "validation_only_case_local_candidate",
                }
            )

    return {
        "center": list(center),
        "radial_band": list(radial_band),
        "angle_samples": angle_samples,
        "tolerance_rgb_euclidean": tolerance,
        "minimum_sector_share_percent": minimum_sector_share_percent,
        "initial_classified_coverage": initial_coverage,
        "accepted_classified_coverage": float(accepted_total / angle_samples),
        "sectors": sectors,
        "rejected_support": rejected,
        "status": "geometry_measured_validation_only" if sectors else "no_classifiable_sector",
    }


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_primary_rows(geometry_by_group: dict[str, dict]) -> list[dict]:
    geometry_lookup = {
        (group, sector["cell_type"]): sector
        for group, result in geometry_by_group.items()
        for sector in result["sectors"]
    }
    totals = Counter()
    for group, _, value, _ in VISIBLE_LABELS:
        totals[group] += value

    rows = []
    for record_id, (group, cell_type, value, label_anchor) in enumerate(VISIBLE_LABELS, 1):
        geometry = geometry_lookup.get((group, cell_type))
        rows.append(
            {
                "record_id": f"fig1f-label-{record_id:02d}",
                "panel_id": "Fig.1f",
                "chart_group": group,
                "cell_type": cell_type,
                "color_hex": PALETTE[cell_type]["hex"],
                "displayed_label": f"{value:.1f}",
                "displayed_value_percent": f"{value:.1f}",
                "label_anchor_x_original_px": label_anchor[0],
                "label_anchor_y_original_px": label_anchor[1],
                "label_status": "manual_verified_visible_label",
                "label_value_numeric_authorized": "true",
                "group_label_sum_percent": f"{totals[group]:.1f}",
                "normalized_label_share_percent": f"{100.0 * value / totals[group]:.6f}",
                "geometry_share_percent_validation_only": (
                    f"{geometry['geometry_share_percent']:.6f}" if geometry else ""
                ),
                "geometry_status": geometry["status"] if geometry else "not_detected",
                "source_representation": "visible_label_on_official_raster",
            }
        )
    return rows


def make_overlay(panel: Image.Image, primary_rows: list[dict], output_path: Path) -> None:
    overlay = panel.convert("RGB").copy()
    draw = ImageDraw.Draw(overlay)
    font = ImageFont.load_default()
    left, top, _, _ = PANEL_BOX
    for group, meta in DONUTS.items():
        x, y = meta["center"]
        x -= left
        y -= top
        draw.ellipse((x - 72, y - 72, x + 72, y + 72), outline=(220, 0, 0), width=2)
        draw.ellipse((x - 46, y - 46, x + 46, y + 46), outline=(220, 0, 0), width=1)
        draw.text((x - 22, y - 7), group, fill=(160, 0, 0), font=font)
    for row in primary_rows:
        x = int(row["label_anchor_x_original_px"]) - left
        y = int(row["label_anchor_y_original_px"]) - top
        colour = tuple(int(row["color_hex"][i : i + 2], 16) for i in (1, 3, 5))
        label = row["displayed_label"]
        box = draw.textbbox((x, y), label, font=font)
        draw.rectangle((box[0] - 2, box[1] - 1, box[2] + 2, box[3] + 1), outline=colour, width=2)
    overlay.save(output_path)


def make_recreation(primary_rows: list[dict], output_path: Path) -> None:
    width = PANEL_BOX[2] - PANEL_BOX[0]
    height = PANEL_BOX[3] - PANEL_BOX[1]
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    bold = ImageFont.load_default()
    draw.text((4, 9), "f)", fill=(35, 31, 32), font=bold)
    by_group: dict[str, list[dict]] = {group: [] for group in DONUTS}
    for row in primary_rows:
        by_group[row["chart_group"]].append(row)

    # Order follows the clockwise visible sector order at 12 o'clock.  Values
    # are the primary visible labels; Pillow normalizes each group's total.
    order = {
        "Normal": ["Tumor_KC_Cyc", "Tumor_KC_Basal", "TSK", "Normal_KC_Diff"],
        "AK": ["Tumor_KC_Diff", "Tumor_KC_Cyc", "Tumor_KC_Basal", "TSK", "Normal_KC_Diff"],
        "Primary": ["Tumor_KC_Diff", "Tumor_KC_Basal", "TSK", "Normal_KC_Diff"],
        "MET": ["Tumor_KC_Diff", "Tumor_KC_Basal", "TSK", "Normal_KC_Diff", "Normal_KC_Basal"],
    }

    for group, meta in DONUTS.items():
        cx = meta["center"][0] - PANEL_BOX[0]
        cy = meta["center"][1] - PANEL_BOX[1]
        lookup = {row["cell_type"]: row for row in by_group[group]}
        records = [lookup[name] for name in order[group]]
        total = sum(float(row["displayed_value_percent"]) for row in records)
        angle = -90.0
        for row in records:
            extent = 360.0 * float(row["displayed_value_percent"]) / total
            colour = tuple(int(row["color_hex"][i : i + 2], 16) for i in (1, 3, 5))
            draw.pieslice((cx - 72, cy - 72, cx + 72, cy + 72), angle, angle + extent, fill=colour, outline="white", width=2)
            angle += extent
        draw.ellipse((cx - 45, cy - 45, cx + 45, cy + 45), fill="white")
        text_box = draw.textbbox((0, 0), group, font=font)
        draw.text((cx - (text_box[2] - text_box[0]) / 2, cy - 5), group, fill=(35, 31, 32), font=font)
        for row in records:
            x = int(row["label_anchor_x_original_px"]) - PANEL_BOX[0]
            y = int(row["label_anchor_y_original_px"]) - PANEL_BOX[1]
            draw.text((x, y), row["displayed_label"], fill=(35, 31, 32), font=font)
    canvas.save(output_path)


def build(input_path: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    source_sha256 = sha256_file(input_path)
    image = Image.open(input_path).convert("RGB")
    if image.size != EXPECTED_SOURCE_SIZE:
        raise ValueError(f"source dimensions {image.size} do not match {EXPECTED_SOURCE_SIZE}")
    if source_sha256 != EXPECTED_SOURCE_SHA256:
        raise ValueError("source SHA-256 does not match the official full-size Figure 1 PNG")

    parameters = {
        "panel_box_original_px": list(PANEL_BOX),
        "donuts": DONUTS,
        "palette": PALETTE,
        "angle_samples": 7200,
        "rgb_tolerance": 20.0,
        "minimum_sector_share_percent": 0.5,
    }
    run_id = stable_run_id(source_sha256, parameters)
    rgb = np.asarray(image)
    geometry_by_group = {
        group: sample_annular_geometry(
            rgb,
            tuple(meta["center"]),
            tuple(meta["radial_band"]),
            angle_samples=parameters["angle_samples"],
            tolerance=parameters["rgb_tolerance"],
            minimum_sector_share_percent=parameters["minimum_sector_share_percent"],
        )
        for group, meta in DONUTS.items()
    }

    primary_rows = build_primary_rows(geometry_by_group)
    primary_fields = list(primary_rows[0])
    write_csv(output_dir / "data.csv", primary_rows, primary_fields)

    geometry_rows = []
    for group, result in geometry_by_group.items():
        for sector in result["sectors"]:
            geometry_rows.append(
                {
                    "panel_id": "Fig.1f",
                    "chart_group": group,
                    "cell_type": sector["cell_type"],
                    "color_hex": sector["color_hex"],
                    "center_x_original_px": result["center"][0],
                    "center_y_original_px": result["center"][1],
                    "radial_band_min_px": result["radial_band"][0],
                    "radial_band_max_px": result["radial_band"][1],
                    "classified_angle_count": sector["classified_angle_count"],
                    "geometry_share_percent": f"{sector['geometry_share_percent']:.6f}",
                    "mid_angle_deg_image": f"{sector['mid_angle_deg_image']:.6f}",
                    "component_count": sector["component_count"],
                    "geometry_status": sector["status"],
                }
            )
    write_csv(output_dir / "sector-geometry.csv", geometry_rows, list(geometry_rows[0]))

    panel = image.crop(PANEL_BOX)
    panel.save(output_dir / "panel-original.png")
    make_overlay(panel, primary_rows, output_dir / "overlay.png")
    make_recreation(primary_rows, output_dir / "recreated.png")

    comparisons = []
    for row in primary_rows:
        if not row["geometry_share_percent_validation_only"]:
            continue
        label_share = float(row["normalized_label_share_percent"])
        geometry_share = float(row["geometry_share_percent_validation_only"])
        comparisons.append(
            {
                "chart_group": row["chart_group"],
                "cell_type": row["cell_type"],
                "normalized_visible_label_share_percent": label_share,
                "geometry_share_percent": geometry_share,
                "absolute_percentage_point_error": abs(label_share - geometry_share),
            }
        )
    maximum_error = max(item["absolute_percentage_point_error"] for item in comparisons)
    mean_error = sum(item["absolute_percentage_point_error"] for item in comparisons) / len(comparisons)
    retained_source_files = {}
    for name in ("article.pdf", "supplementary-data-file-6.xlsx", "source-data.xlsx"):
        candidate_path = output_dir / name
        if candidate_path.exists():
            retained_source_files[name] = {
                "sha256": sha256_file(candidate_path),
                "size_bytes": candidate_path.stat().st_size,
            }

    report = {
        "schema_version": 1,
        "status": "partial_visible",
        "numeric_output_authorized": True,
        "numeric_authorization_scope": "18 explicitly visible percentage labels only",
        "algorithm": ALGORITHM,
        "algorithm_version": ALGORITHM_VERSION,
        "deterministic_run_id": run_id,
        "input": {
            "file": str(input_path.resolve()),
            "sha256": source_sha256,
            "width": image.width,
            "height": image.height,
            "coordinate_space": "original_raster_pixels",
            "resampled_for_measurement": False,
            "official_url": "https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41467-023-40822-9/MediaObjects/41467_2023_40822_Fig1_HTML.png",
        },
        "panel": {"id": "Fig.1f", "bounds_original_px": list(PANEL_BOX), "verified": True},
        "preflight": {
            "route_id": "unsupported_coordinate_route",
            "maturity": "not_implemented_or_case_only",
            "registered_automated_extraction": False,
            "preflight_numeric_authorized": False,
        },
        "recoverable_representation": {
            "primary": "visible percentage labels keyed by donut group and visibly mapped sector colour",
            "validation_only": "normalized annular colour-sector geometry",
            "not_recoverable": [
                "individual-sample CIBERSORTx proportions",
                "an unlabeled absolute percentage for a sector not visibly printed",
                "the aggregation statistic used to form the donut labels",
                "raw cells or counts underlying the proportions",
            ],
        },
        "visible_label_extraction": {
            "method": "manual double transcription from official full-size raster, checked against official PDF page 3 rendering",
            "requested_label_count": 18,
            "recovered_label_count": len(primary_rows),
            "coverage": len(primary_rows) / 18,
            "per_group_counts": dict(Counter(row["chart_group"] for row in primary_rows)),
            "group_label_sums_percent": {
                group: sum(
                    float(row["displayed_value_percent"])
                    for row in primary_rows
                    if row["chart_group"] == group
                )
                for group in DONUTS
            },
            "important_semantics": "The printed values do not all sum to 100; rendered sector angles are proportional to the within-donut sum rather than interpreted as omitted percentages.",
        },
        "sector_geometry_validation": {
            "numeric_output_authorized": False,
            "role": "case-local validation only; not a registered pie/donut extractor",
            "parameters": parameters,
            "results": geometry_by_group,
            "comparison_to_normalized_visible_labels": comparisons,
            "mean_absolute_percentage_point_error": mean_error,
            "maximum_absolute_percentage_point_error": maximum_error,
        },
        "official_source_validation": {
            "status": "not_comparable",
            "article_caption_evidence": "The Figure 1 caption states that Source Data are provided for panels b and e; it does not include panel f.",
            "supplementary_data_file_6_role": "related input table retained only; no verified group/statistic mapping to the 18 donut labels",
            "source_values_used_to_fill_primary_csv": False,
        },
        "sources": {
            "retrieved_date": "2026-07-21",
            "article": "https://www.nature.com/articles/s41467-023-40822-9",
            "figure_page": "https://www.nature.com/articles/s41467-023-40822-9/figures/1",
            "article_pdf": "https://www.nature.com/articles/s41467-023-40822-9.pdf",
            "supplementary_data_file_6": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-40822-9/MediaObjects/41467_2023_40822_MOESM9_ESM.xlsx",
            "source_data_file": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-40822-9/MediaObjects/41467_2023_40822_MOESM22_ESM.xlsx",
            "retained_file_identities": retained_source_files,
        },
        "license": {
            "article_license": "Creative Commons Attribution 4.0 International",
            "url": "http://creativecommons.org/licenses/by/4.0/",
            "third_party_material_caveat": "The article license notice requires checking credit lines for material excluded from the article's Creative Commons licence.",
        },
        "evidence_files": [
            "data.csv",
            "sector-geometry.csv",
            "panel-original.png",
            "overlay.png",
            "recreated.png",
            "preflight-report.json",
            "figure-spec.json",
            "pdf-page3-vector-inspection.json",
        ],
    }
    (output_dir / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report = build(args.input, args.output_dir)
    print(
        json.dumps(
            {
                "status": report["status"],
                "numeric_output_authorized": report["numeric_output_authorized"],
                "label_count": report["visible_label_extraction"]["recovered_label_count"],
                "geometry_max_abs_pp_error": report["sector_geometry_validation"]["maximum_absolute_percentage_point_error"],
                "run_id": report["deterministic_run_id"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

"""Candidate extractor for raster line charts with compact filled markers.

The candidate targets marker-on-line panels where anti-aliased reference lines,
background-dependent alpha compositing, or decorative same-colour marks defeat
the legacy greedy sampler.  It keeps every visible candidate, selects a global
marker path, calibrates through the shared ``AxisCalibration`` object, and
writes an immutable evidence bundle under a deterministic run ID.

This remains a candidate route.  It recovers visible marker centres only; it
does not infer hidden samples, source curve parameters, or values between the
configured marker positions.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np
from PIL import Image, ImageDraw

try:
    from raster_digitizer_core import AxisCalibration
except ImportError:  # pragma: no cover
    from .raster_digitizer_core import AxisCalibration


ALGORITHM_VERSION = "marker_line_global_path_v0.2.0-candidate"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_color(value: str) -> tuple[int, int, int]:
    text = value.strip().lstrip("#")
    if len(text) != 6:
        raise argparse.ArgumentTypeError("colours must use #RRGGBB")
    try:
        result = tuple(int(text[index : index + 2], 16) for index in (0, 2, 4))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("colours must use #RRGGBB") from exc
    return result  # type: ignore[return-value]


def parse_series(value: str) -> tuple[str, tuple[tuple[int, int, int], ...]]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("series must use NAME=#RRGGBB or NAME=#RRGGBB|#RRGGBB")
    name, colour_text = value.split("=", 1)
    name = name.strip()
    if not name or name in {"x", "x_pixel", "series", "value"}:
        raise argparse.ArgumentTypeError("choose a non-empty, non-reserved series name")
    colours = tuple(parse_color(item) for item in colour_text.split("|") if item.strip())
    if not colours:
        raise argparse.ArgumentTypeError("each series needs at least one colour template")
    if len(set(colours)) != len(colours):
        raise argparse.ArgumentTypeError("series colour templates must be unique")
    return name, colours


def parse_values(value: str) -> list[float]:
    try:
        values = [float(item.strip()) for item in value.split(",") if item.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("values must be comma-separated numbers") from exc
    if not values or len(set(values)) != len(values):
        raise argparse.ArgumentTypeError("values must be a non-empty unique list")
    if values != sorted(values):
        raise argparse.ArgumentTypeError("sample values must be strictly increasing")
    return values


def parse_anchor(value: str) -> tuple[float, float]:
    try:
        pixel, numeric = (float(item.strip()) for item in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("anchors must use pixel,value") from exc
    return pixel, numeric


def parse_bounds(value: str) -> tuple[int, int, int, int]:
    try:
        bounds = tuple(int(item.strip()) for item in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("bounds must use left,top,right,bottom") from exc
    if len(bounds) != 4 or bounds[0] >= bounds[2] or bounds[1] >= bounds[3]:
        raise argparse.ArgumentTypeError("bounds must satisfy left < right and top < bottom")
    return bounds  # type: ignore[return-value]


def colour_masks(
    pixels: np.ndarray,
    colours: Sequence[Sequence[int]],
    tolerance: float,
) -> tuple[np.ndarray, list[np.ndarray]]:
    rgb = pixels.astype(np.int32)
    masks: list[np.ndarray] = []
    for colour in colours:
        target = np.asarray(colour, dtype=np.int32)
        distance_squared = np.square(rgb - target).sum(axis=2)
        masks.append(distance_squared <= tolerance * tolerance)
    return np.logical_or.reduce(masks), masks


def _row_groups(rows: np.ndarray, *, max_gap: int = 2) -> list[np.ndarray]:
    unique = np.unique(rows)
    if not len(unique):
        return []
    breaks = np.where(np.diff(unique) > max_gap)[0] + 1
    return [group for group in np.split(unique, breaks) if len(group)]


def marker_candidates(
    mask: np.ndarray,
    template_masks: Sequence[np.ndarray],
    *,
    x_pixel: float,
    bounds: tuple[int, int, int, int],
    sample_radius: int,
    marker_radius_min: int,
    reference_y_pixels: Sequence[float],
) -> list[dict[str, Any]]:
    x0, y0, x1, y1 = bounds
    centre_x = int(round(x_pixel))
    left = max(x0, centre_x - sample_radius)
    right = min(x1, centre_x + sample_radius)
    cropped = mask[y0 : y1 + 1, left : right + 1]
    local_rows, local_columns = np.where(cropped)
    if not len(local_rows):
        return []
    absolute_rows = local_rows + y0
    absolute_columns = local_columns + left
    candidates: list[dict[str, Any]] = []
    required_span = max(2, marker_radius_min * 2)
    for group in _row_groups(absolute_rows):
        group_set = set(int(row) for row in group)
        selected = np.asarray([int(row) in group_set for row in absolute_rows], dtype=bool)
        rows = absolute_rows[selected]
        columns = absolute_columns[selected]
        if not len(rows):
            continue
        pixel_count = int(len(rows))
        vertical_span = int(rows.max() - rows.min() + 1)
        horizontal_span = int(columns.max() - columns.min() + 1)
        compactness = float(min(vertical_span, horizontal_span) / max(vertical_span, horizontal_span))
        fill_fraction = float(pixel_count / max(vertical_span * horizontal_span, 1))
        size_support = float(
            min(1.0, vertical_span / required_span)
            * min(1.0, horizontal_span / required_span)
        )
        horizontal_excess = float(max(0, horizontal_span - vertical_span) / max(vertical_span, 1))
        y_centre = float(np.median(rows))
        template_counts = []
        for template_mask in template_masks:
            template_counts.append(int(template_mask[rows, columns].sum()))
        # Pixel amount and two-dimensional support dominate continuity.  This
        # is what prevents a one-pixel anti-aliased dash from beating a marker
        # merely because the dash is closer to the previously selected row.
        evidence_score = (
            math.log1p(pixel_count)
            + 3.2 * size_support
            + 1.4 * compactness
            + 1.2 * min(1.0, fill_fraction / 0.5)
            - 0.8 * min(3.0, horizontal_excess)
        )
        distance_to_reference = (
            min(abs(y_centre - line_y) for line_y in reference_y_pixels)
            if reference_y_pixels
            else None
        )
        structure_line_like = vertical_span <= max(2, marker_radius_min - 1)
        if structure_line_like:
            evidence_score -= 4.0 + 0.5 * min(4.0, horizontal_excess)
        if structure_line_like and distance_to_reference is not None and distance_to_reference <= 2.0:
            evidence_score -= 1.5
        candidates.append(
            {
                "y_pixel": y_centre,
                "pixel_count": pixel_count,
                "vertical_span": vertical_span,
                "horizontal_span": horizontal_span,
                "compactness": round(compactness, 6),
                "fill_fraction": round(fill_fraction, 6),
                "size_support": round(size_support, 6),
                "horizontal_excess": round(horizontal_excess, 6),
                "evidence_score": round(float(evidence_score), 6),
                "template_pixel_counts": template_counts,
                "dominant_template_index": int(np.argmax(template_counts)),
                "distance_to_reference_line_px": (
                    None if distance_to_reference is None else round(float(distance_to_reference), 3)
                ),
                "structure_line_like": structure_line_like,
                "bbox_px": [int(columns.min()), int(rows.min()), int(columns.max()), int(rows.max())],
                "is_gap": False,
            }
        )
    return sorted(candidates, key=lambda item: item["y_pixel"])


def _transition_cost(first: dict[str, Any], second: dict[str, Any], weight: float) -> float:
    if first["is_gap"] or second["is_gap"]:
        return 2.0
    return weight * abs(float(second["y_pixel"]) - float(first["y_pixel"]))


def _curvature_cost(
    first: dict[str, Any],
    second: dict[str, Any],
    third: dict[str, Any],
    weight: float,
) -> float:
    if first["is_gap"] or second["is_gap"] or third["is_gap"]:
        return 0.0
    curvature = abs(
        float(third["y_pixel"])
        - 2.0 * float(second["y_pixel"])
        + float(first["y_pixel"])
    )
    return weight * curvature


def select_global_path(
    candidate_sets: Sequence[Sequence[dict[str, Any]]],
    *,
    transition_weight: float,
    curvature_weight: float,
    gap_penalty: float,
) -> list[dict[str, Any]]:
    if not candidate_sets:
        return []
    states: list[list[dict[str, Any]]] = []
    for candidates in candidate_sets:
        current = [dict(item) for item in candidates]
        current.append(
            {
                "y_pixel": None,
                "pixel_count": 0,
                "vertical_span": 0,
                "horizontal_span": 0,
                "compactness": 0.0,
                "fill_fraction": 0.0,
                "size_support": 0.0,
                "horizontal_excess": 0.0,
                "evidence_score": -float(gap_penalty),
                "template_pixel_counts": [],
                "dominant_template_index": None,
                "distance_to_reference_line_px": None,
                "structure_line_like": False,
                "bbox_px": None,
                "is_gap": True,
            }
        )
        states.append(current)
    if len(states) == 1:
        return [max(states[0], key=lambda item: item["evidence_score"])]

    pair_costs: dict[tuple[int, int], float] = {}
    pair_back: list[dict[tuple[int, int], int]] = [{} for _ in states]
    for first_index, first in enumerate(states[0]):
        for second_index, second in enumerate(states[1]):
            pair_costs[(first_index, second_index)] = (
                -float(first["evidence_score"])
                - float(second["evidence_score"])
                + _transition_cost(first, second, transition_weight)
            )
    for position in range(2, len(states)):
        next_costs: dict[tuple[int, int], float] = {}
        back: dict[tuple[int, int], int] = {}
        for previous_index, previous in enumerate(states[position - 1]):
            possible_prior = [
                (prior_index, cost)
                for (prior_index, current_previous), cost in pair_costs.items()
                if current_previous == previous_index
            ]
            for current_index, current in enumerate(states[position]):
                best: tuple[float, int] | None = None
                for prior_index, prior_cost in possible_prior:
                    candidate_cost = (
                        prior_cost
                        - float(current["evidence_score"])
                        + _transition_cost(previous, current, transition_weight)
                        + _curvature_cost(
                            states[position - 2][prior_index],
                            previous,
                            current,
                            curvature_weight,
                        )
                    )
                    if best is None or candidate_cost < best[0]:
                        best = (candidate_cost, prior_index)
                if best is not None:
                    next_costs[(previous_index, current_index)] = best[0]
                    back[(previous_index, current_index)] = best[1]
        pair_costs = next_costs
        pair_back[position] = back
    final_pair = min(pair_costs, key=pair_costs.get)
    selected_indices = [0] * len(states)
    selected_indices[-2], selected_indices[-1] = final_pair
    for position in range(len(states) - 1, 1, -1):
        selected_indices[position - 2] = pair_back[position][
            (selected_indices[position - 1], selected_indices[position])
        ]
    return [states[index][selected_indices[index]] for index in range(len(states))]


def _sigmoid(value: float) -> float:
    if value >= 0:
        return 1.0 / (1.0 + math.exp(-value))
    exp_value = math.exp(value)
    return exp_value / (1.0 + exp_value)


def score_selected_path(
    selected: Sequence[dict[str, Any]],
    candidate_sets: Sequence[Sequence[dict[str, Any]]],
    *,
    marker_radius_min: int,
    confidence_threshold: float,
    transition_weight: float,
) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    minimum_pixels = max(12, int(round(math.pi * marker_radius_min**2 * 0.85)))
    for index, chosen in enumerate(selected):
        if chosen["is_gap"]:
            observations.append(
                {
                    **chosen,
                    "status": "not_extracted",
                    "confidence": 0.0,
                    "path_margin": None,
                    "reason": "no marker-like colour evidence selected",
                }
            )
            continue
        neighbour_rows = [
            float(selected[neighbor]["y_pixel"])
            for neighbor in (index - 1, index + 1)
            if 0 <= neighbor < len(selected) and not selected[neighbor]["is_gap"]
        ]
        predicted = float(np.mean(neighbour_rows)) if neighbour_rows else float(chosen["y_pixel"])
        chosen_adjusted = float(chosen["evidence_score"]) - transition_weight * abs(
            float(chosen["y_pixel"]) - predicted
        )
        alternative_adjusted = [
            float(candidate["evidence_score"])
            - transition_weight * abs(float(candidate["y_pixel"]) - predicted)
            for candidate in candidate_sets[index]
            if candidate is not chosen and abs(float(candidate["y_pixel"]) - float(chosen["y_pixel"])) > 0.25
        ]
        margin = chosen_adjusted - max(alternative_adjusted) if alternative_adjusted else 4.0
        morphology = (
            0.4 * float(chosen["size_support"])
            + 0.2 * float(chosen["compactness"])
            + 0.2 * min(1.0, float(chosen["fill_fraction"]) / 0.5)
            + 0.2 * min(1.0, float(chosen["pixel_count"]) / max(minimum_pixels * 2, 1))
        )
        confidence = _sigmoid(0.9 * (margin - 0.25)) * (0.35 + 0.65 * morphology)
        marker_like = (
            int(chosen["pixel_count"]) >= minimum_pixels
            and int(chosen["vertical_span"]) >= marker_radius_min + 1
            and float(chosen["size_support"]) >= 0.25
            and float(chosen["fill_fraction"]) >= 0.15
        )
        if marker_like and confidence >= confidence_threshold:
            status = "extracted"
            reason = None
        else:
            status = "review_required"
            reason = "selected evidence is too line-like, too small, or insufficiently separated from an alternative"
        observations.append(
            {
                **chosen,
                "status": status,
                "confidence": round(float(confidence), 6),
                "path_margin": round(float(margin), 6),
                "reason": reason,
            }
        )
    return observations


def extract_marker_line(
    pixels: np.ndarray,
    *,
    plot_bounds: tuple[int, int, int, int],
    x_axis: AxisCalibration,
    y_axis: AxisCalibration,
    sample_values: Sequence[float],
    series: Sequence[tuple[str, Sequence[Sequence[int]]]],
    color_tolerance: float = 12.0,
    sample_radius: int = 8,
    marker_radius_min: int = 3,
    reference_lines: Sequence[float] = (),
    transition_weight: float = 0.08,
    curvature_weight: float = 0.03,
    confidence_threshold: float = 0.55,
) -> dict[str, Any]:
    if color_tolerance <= 0 or sample_radius < 1 or marker_radius_min < 1:
        raise ValueError("colour tolerance and marker radii must be positive")
    sample_pixels = [x_axis.pixel_at_value(value) for value in sample_values]
    x0, _, x1, _ = plot_bounds
    if any(pixel < x0 or pixel > x1 for pixel in sample_pixels):
        raise ValueError("every sample value must map inside plot bounds")
    reference_y_pixels = [y_axis.pixel_at_value(value) for value in reference_lines]
    series_results: dict[str, Any] = {}
    for name, colours in series:
        union_mask, template_masks = colour_masks(pixels, colours, color_tolerance)
        candidate_sets = [
            marker_candidates(
                union_mask,
                template_masks,
                x_pixel=x_pixel,
                bounds=plot_bounds,
                sample_radius=sample_radius,
                marker_radius_min=marker_radius_min,
                reference_y_pixels=reference_y_pixels,
            )
            for x_pixel in sample_pixels
        ]
        selected = select_global_path(
            candidate_sets,
            transition_weight=transition_weight,
            curvature_weight=curvature_weight,
            gap_penalty=8.0,
        )
        observations = score_selected_path(
            selected,
            candidate_sets,
            marker_radius_min=marker_radius_min,
            confidence_threshold=confidence_threshold,
            transition_weight=transition_weight,
        )
        for x_value, x_pixel, observation in zip(sample_values, sample_pixels, observations):
            observation["x"] = float(x_value)
            observation["x_pixel"] = round(float(x_pixel), 6)
            y_pixel = observation["y_pixel"]
            if y_pixel is None:
                observation["candidate_value"] = None
                observation["value"] = None
                observation["pixel_uncertainty"] = None
                observation["value_uncertainty"] = None
            else:
                candidate_value = y_axis.value_at_pixel(float(y_pixel))
                pixel_uncertainty = max(
                    0.5,
                    min(2.0, float(observation["vertical_span"]) / max(math.sqrt(observation["pixel_count"]), 1.0)),
                )
                observation["candidate_value"] = round(float(candidate_value), 8)
                observation["value"] = (
                    round(float(candidate_value), 8)
                    if observation["status"] == "extracted"
                    else None
                )
                observation["pixel_uncertainty"] = round(pixel_uncertainty, 6)
                observation["value_uncertainty"] = round(
                    float(y_axis.uncertainty_at_pixel(float(y_pixel), pixel_sigma=pixel_uncertainty)),
                    8,
                )
        found = sum(item["status"] == "extracted" for item in observations)
        review = sum(item["status"] == "review_required" for item in observations)
        missing = sum(item["status"] == "not_extracted" for item in observations)
        series_results[name] = {
            "colours_rgb": [list(map(int, colour)) for colour in colours],
            "candidate_sets": candidate_sets,
            "observations": observations,
            "summary": {
                "extracted": found,
                "review_required": review,
                "not_extracted": missing,
                "total": len(observations),
                "coverage": round(found / len(observations), 6) if observations else 0.0,
                "mean_confidence": round(
                    float(np.mean([item["confidence"] for item in observations])), 6
                ) if observations else 0.0,
            },
        }
    authorized = all(
        result["summary"]["coverage"] == 1.0
        and result["summary"]["review_required"] == 0
        and result["summary"]["not_extracted"] == 0
        for result in series_results.values()
    )
    return {
        "sample_values": [float(value) for value in sample_values],
        "sample_pixels": sample_pixels,
        "reference_lines": [float(value) for value in reference_lines],
        "reference_y_pixels": reference_y_pixels,
        "series": series_results,
        "numeric_output_authorized": authorized,
        "status": "candidate_extracted" if authorized else "low_confidence",
    }


def create_overlay(
    image: Image.Image,
    result: dict[str, Any],
    output: Path,
) -> None:
    overlay = image.convert("RGB").copy()
    draw = ImageDraw.Draw(overlay)
    for line_y in result["reference_y_pixels"]:
        draw.line((0, int(round(line_y)), overlay.width - 1, int(round(line_y))), fill=(150, 0, 180), width=1)
    selected_colours = [(0, 170, 70), (0, 130, 220), (220, 120, 0), (160, 0, 200)]
    for series_index, (_, series_result) in enumerate(result["series"].items()):
        selected_colour = selected_colours[series_index % len(selected_colours)]
        for candidates, observation in zip(series_result["candidate_sets"], series_result["observations"]):
            x = int(round(observation["x_pixel"]))
            for candidate in candidates:
                y = int(round(candidate["y_pixel"]))
                draw.ellipse((x - 2, y - 2, x + 2, y + 2), outline=(150, 150, 150), width=1)
            if observation["y_pixel"] is None:
                draw.line((x - 4, 4, x + 4, 12), fill=(210, 0, 0), width=2)
                draw.line((x + 4, 4, x - 4, 12), fill=(210, 0, 0), width=2)
                continue
            y = int(round(observation["y_pixel"]))
            colour = selected_colour if observation["status"] == "extracted" else (255, 140, 0)
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), outline=colour, width=2)
            bbox = observation.get("bbox_px")
            if bbox:
                draw.rectangle(tuple(bbox), outline=colour, width=1)
    overlay.save(output)


def _canonical_run_configuration(
    *,
    source_sha256: str,
    image_size: tuple[int, int],
    plot_bounds: tuple[int, int, int, int],
    x_axis: AxisCalibration,
    y_axis: AxisCalibration,
    sample_values: Sequence[float],
    series: Sequence[tuple[str, Sequence[Sequence[int]]]],
    parameters: dict[str, Any],
) -> dict[str, Any]:
    return {
        "algorithm_version": ALGORITHM_VERSION,
        "implementation_sha256": file_sha256(Path(__file__).resolve()),
        "source_sha256": source_sha256,
        "image_size": list(image_size),
        "plot_bounds": list(plot_bounds),
        "x_axis": x_axis.report(),
        "y_axis": y_axis.report(),
        "sample_values": list(map(float, sample_values)),
        "series": [
            {"name": name, "colours_rgb": [list(map(int, colour)) for colour in colours]}
            for name, colours in series
        ],
        "parameters": parameters,
    }


def write_evidence_bundle(
    *,
    input_path: Path,
    output_root: Path,
    plot_bounds: tuple[int, int, int, int],
    x_axis: AxisCalibration,
    y_axis: AxisCalibration,
    sample_values: Sequence[float],
    series: Sequence[tuple[str, Sequence[Sequence[int]]]],
    color_tolerance: float,
    sample_radius: int,
    marker_radius_min: int,
    reference_lines: Sequence[float],
    transition_weight: float,
    curvature_weight: float,
    confidence_threshold: float,
) -> Path:
    input_path = input_path.resolve()
    with Image.open(input_path) as opened:
        image = opened.convert("RGB")
    pixels = np.asarray(image)
    source_hash = file_sha256(input_path)
    parameters = {
        "color_tolerance": color_tolerance,
        "sample_radius": sample_radius,
        "marker_radius_min": marker_radius_min,
        "reference_lines": list(map(float, reference_lines)),
        "transition_weight": transition_weight,
        "curvature_weight": curvature_weight,
        "confidence_threshold": confidence_threshold,
    }
    configuration = _canonical_run_configuration(
        source_sha256=source_hash,
        image_size=image.size,
        plot_bounds=plot_bounds,
        x_axis=x_axis,
        y_axis=y_axis,
        sample_values=sample_values,
        series=series,
        parameters=parameters,
    )
    configuration_hash = hashlib.sha256(
        json.dumps(configuration, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    run_id = f"marker-line-{configuration_hash[:16]}"
    output_dir = output_root.resolve() / run_id
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"immutable evidence directory already exists and is non-empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=False)
    result = extract_marker_line(
        pixels,
        plot_bounds=plot_bounds,
        x_axis=x_axis,
        y_axis=y_axis,
        sample_values=sample_values,
        series=series,
        color_tolerance=color_tolerance,
        sample_radius=sample_radius,
        marker_radius_min=marker_radius_min,
        reference_lines=reference_lines,
        transition_weight=transition_weight,
        curvature_weight=curvature_weight,
        confidence_threshold=confidence_threshold,
    )
    with (output_dir / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["x", "x_pixel", *[name for name, _ in series]]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index, x_value in enumerate(sample_values):
            row: dict[str, Any] = {
                "x": float(x_value),
                "x_pixel": round(float(result["sample_pixels"][index]), 6),
            }
            for name, _ in series:
                row[name] = result["series"][name]["observations"][index]["value"]
            writer.writerow(row)
    with (output_dir / "evidence.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "series", "x", "x_pixel", "y_pixel", "value", "candidate_value", "status",
            "confidence", "pixel_count", "vertical_span", "horizontal_span", "size_support",
            "compactness", "path_margin", "pixel_uncertainty", "value_uncertainty",
            "fill_fraction",
            "dominant_template_index", "distance_to_reference_line_px", "reason",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for name, _ in series:
            for observation in result["series"][name]["observations"]:
                writer.writerow({key: observation.get(key) for key in fieldnames} | {"series": name})
    create_overlay(image, result, output_dir / "overlay.png")
    implementation_path = Path(__file__).resolve()
    report = {
        "schema_version": 1,
        "status": result["status"],
        "numeric_output_authorized": result["numeric_output_authorized"],
        "extraction_strategy": "deterministic_candidate",
        "algorithm_version": ALGORITHM_VERSION,
        "implementation": "scripts/candidate_digitize_marker_line.py",
        "implementation_sha256": file_sha256(implementation_path),
        "run_id": run_id,
        "configuration_sha256": configuration_hash,
        "input_file": str(input_path),
        "input_sha256": source_hash,
        "image_size": {"width": image.width, "height": image.height},
        "measurement_space": "original_raster_pixels",
        "configuration": configuration,
        "series": {
            name: {
                "colours_rgb": series_result["colours_rgb"],
                "summary": series_result["summary"],
                "observations": series_result["observations"],
                "candidate_sets": series_result["candidate_sets"],
            }
            for name, series_result in result["series"].items()
        },
        "artifacts": {
            "data_csv": "data.csv",
            "evidence_csv": "evidence.csv",
            "overlay": "overlay.png",
            "report": "report.json",
        },
        "limitations": [
            "Candidate route for compact filled markers at verified sample positions.",
            "Review-required and missing observations remain blank in the primary CSV.",
            "Straight or fitted source-curve parameters are not recovered from marker centres.",
        ],
    }
    (output_dir / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "configuration.json").write_text(
        json.dumps(configuration, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--plot-bounds", required=True, type=parse_bounds)
    parser.add_argument("--x-anchor", required=True, action="append", type=parse_anchor)
    parser.add_argument("--y-anchor", required=True, action="append", type=parse_anchor)
    parser.add_argument("--x-transform", choices=("linear", "log10", "displayed_log10"), default="linear")
    parser.add_argument("--y-transform", choices=("linear", "log10", "displayed_log10"), default="linear")
    parser.add_argument("--sample-values", required=True, type=parse_values)
    parser.add_argument("--series", required=True, action="append", type=parse_series)
    parser.add_argument("--color-tolerance", type=float, default=12.0)
    parser.add_argument("--sample-radius", type=int, default=8)
    parser.add_argument("--marker-radius-min", type=int, default=3)
    parser.add_argument("--reference-line", action="append", type=float, default=[])
    parser.add_argument("--transition-weight", type=float, default=0.08)
    parser.add_argument("--curvature-weight", type=float, default=0.03)
    parser.add_argument("--confidence-threshold", type=float, default=0.55)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if len(args.x_anchor) < 2 or len(args.y_anchor) < 2:
        raise SystemExit("at least two x and two y anchors are required")
    if len({name for name, _ in args.series}) != len(args.series):
        raise SystemExit("series names must be unique")
    x_axis = AxisCalibration.fit(args.x_anchor, scale=args.x_transform)
    y_axis = AxisCalibration.fit(args.y_anchor, scale=args.y_transform)
    output_dir = write_evidence_bundle(
        input_path=args.input,
        output_root=args.output_root,
        plot_bounds=args.plot_bounds,
        x_axis=x_axis,
        y_axis=y_axis,
        sample_values=args.sample_values,
        series=args.series,
        color_tolerance=args.color_tolerance,
        sample_radius=args.sample_radius,
        marker_radius_min=args.marker_radius_min,
        reference_lines=args.reference_line,
        transition_weight=args.transition_weight,
        curvature_weight=args.curvature_weight,
        confidence_threshold=args.confidence_threshold,
    )
    report = json.loads((output_dir / "report.json").read_text(encoding="utf-8"))
    print(
        json.dumps(
            {
                "status": report["status"],
                "numeric_output_authorized": report["numeric_output_authorized"],
                "run_id": report["run_id"],
                "output_dir": str(output_dir),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

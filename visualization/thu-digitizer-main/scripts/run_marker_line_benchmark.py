"""Run deterministic marker-line candidate and stable-baseline benchmarks.

The suite covers clean markers, same-colour reference-line conflicts,
background-dependent marker colours, and a line-only refusal panel.  Synthetic
truth is used only after extraction for evaluation.  WebPlotDigitizer is
recorded as not compared unless a matched assisted session is supplied.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw

try:
    from candidate_digitize_marker_line import file_sha256, write_evidence_bundle
    from digitize_line_chart import color_mask, extract_series
    from raster_digitizer_core import AxisCalibration
except ImportError:  # pragma: no cover
    from .candidate_digitize_marker_line import file_sha256, write_evidence_bundle
    from .digitize_line_chart import color_mask, extract_series
    from .raster_digitizer_core import AxisCalibration


BENCHMARK_VERSION = "marker_line_benchmark_v0.1.0"
WIDTH, HEIGHT = 300, 220
BOUNDS = (30, 20, 270, 190)
SAMPLES = list(range(11))
VALUES = [4, 5, 6, 7, 9, 11, 12, 10, 7, 5, 4]
OUTSIDE = (251, 129, 119)
INSIDE = (252, 106, 98)
SHADE = (245, 235, 235)
REFERENCE_VALUE = 8.0


def calibrations() -> tuple[AxisCalibration, AxisCalibration]:
    return (
        AxisCalibration.fit([(40, 0), (150, 5), (260, 10)], scale="linear"),
        AxisCalibration.fit([(180, 0), (130, 5), (80, 10), (30, 15)], scale="linear"),
    )


def render_fixture(*, markers: bool, shaded: bool, reference: bool) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    x_axis, y_axis = calibrations()
    shade_left = 150
    if shaded:
        draw.rectangle((shade_left, BOUNDS[1], BOUNDS[2], BOUNDS[3]), fill=SHADE)
    points = [
        (round(x_axis.pixel_at_value(x)), round(y_axis.pixel_at_value(y)))
        for x, y in zip(SAMPLES, VALUES)
    ]
    for first, second in zip(points, points[1:]):
        colour = INSIDE if shaded and (first[0] + second[0]) / 2 >= shade_left else OUTSIDE
        draw.line((*first, *second), fill=colour, width=1)
    if reference:
        reference_y = round(y_axis.pixel_at_value(REFERENCE_VALUE))
        for left in range(BOUNDS[0], BOUNDS[2] + 1, 10):
            colour = INSIDE if shaded and left >= shade_left else OUTSIDE
            draw.line((left, reference_y, min(left + 5, BOUNDS[2]), reference_y), fill=colour, width=1)
    if markers:
        for x_pixel, y_pixel in points:
            colour = INSIDE if shaded and x_pixel >= shade_left else OUTSIDE
            draw.ellipse((x_pixel - 4, y_pixel - 4, x_pixel + 4, y_pixel + 4), fill=colour)
    return image


def _metrics(values: list[float | None], truth: list[float]) -> dict[str, Any]:
    errors = [abs(value - expected) for value, expected in zip(values, truth) if value is not None]
    return {
        "coverage": round(len(errors) / len(truth), 6),
        "mae": round(float(np.mean(errors)), 6) if errors else None,
        "max_abs_error": round(float(max(errors)), 6) if errors else None,
    }


def _stable_baseline(image: Image.Image, colours: list[tuple[int, int, int]], reference: bool) -> dict[str, Any]:
    pixels = np.asarray(image)
    mask = np.logical_or.reduce([color_mask(pixels, colour, 2) for colour in colours])
    x_axis, y_axis = calibrations()
    sample_pixels = [x_axis.pixel_at_value(value) for value in SAMPLES]
    observations, confidence = extract_series(mask, sample_pixels, BOUNDS, 7)
    values = [
        None if item["y_pixel"] is None else y_axis.value_at_pixel(float(item["y_pixel"]))
        for item in observations
    ]
    reference_y = y_axis.pixel_at_value(REFERENCE_VALUE)
    unsafe_reference_selections = sum(
        reference
        and item["y_pixel"] is not None
        and abs(float(item["y_pixel"]) - reference_y) <= 1.0
        and abs(truth - REFERENCE_VALUE) >= 1.0
        for item, truth in zip(observations, VALUES)
    )
    return {
        **_metrics(values, VALUES),
        "mean_confidence": round(float(confidence), 6),
        "unsafe_reference_selections": int(unsafe_reference_selections),
        "values": values,
        "observations": observations,
    }


def _write_truth(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["x", "truth_value"])
        writer.writerows(zip(SAMPLES, VALUES))


def run_benchmark(output_root: Path) -> Path:
    script = Path(__file__).resolve()
    candidate = script.with_name("candidate_digitize_marker_line.py")
    stable = script.with_name("digitize_line_chart.py")
    identity = {
        "benchmark_version": BENCHMARK_VERSION,
        "benchmark_sha256": file_sha256(script),
        "candidate_sha256": file_sha256(candidate),
        "stable_sha256": file_sha256(stable),
    }
    run_hash = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    output_dir = output_root.resolve() / f"marker-line-benchmark-{run_hash[:16]}"
    if output_dir.exists():
        raise FileExistsError(f"immutable benchmark directory already exists: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=False)
    x_axis, y_axis = calibrations()
    cases = [
        {"id": "clean_markers", "markers": True, "shaded": False, "reference": False, "expected": "success"},
        {"id": "same_colour_reference", "markers": True, "shaded": False, "reference": True, "expected": "success"},
        {"id": "shaded_multi_template_reference", "markers": True, "shaded": True, "reference": True, "expected": "success"},
        {"id": "line_only_refusal", "markers": False, "shaded": False, "reference": True, "expected": "refusal"},
    ]
    reports = []
    for case in cases:
        case_dir = output_dir / case["id"]
        case_dir.mkdir()
        source = case_dir / "source.png"
        render_fixture(markers=case["markers"], shaded=case["shaded"], reference=case["reference"]).save(source)
        _write_truth(case_dir / "truth.csv")
        colours = [OUTSIDE, INSIDE] if case["shaded"] else [OUTSIDE]
        candidate_dir = write_evidence_bundle(
            input_path=source,
            output_root=case_dir / "candidate",
            plot_bounds=BOUNDS,
            x_axis=x_axis,
            y_axis=y_axis,
            sample_values=SAMPLES,
            series=[("curve", colours)],
            color_tolerance=2,
            sample_radius=7,
            marker_radius_min=3,
            reference_lines=[REFERENCE_VALUE] if case["reference"] else [],
            transition_weight=0.08,
            curvature_weight=0.03,
            confidence_threshold=0.55,
        )
        candidate_report = json.loads((candidate_dir / "report.json").read_text(encoding="utf-8"))
        observations = candidate_report["series"]["curve"]["observations"]
        candidate_values = [item["value"] for item in observations]
        candidate_metrics = _metrics(candidate_values, VALUES)
        candidate_metrics.update(
            {
                "status": candidate_report["status"],
                "numeric_output_authorized": candidate_report["numeric_output_authorized"],
                "mean_confidence": candidate_report["series"]["curve"]["summary"]["mean_confidence"],
                "relative_evidence_directory": str(candidate_dir.relative_to(output_dir)).replace("\\", "/"),
            }
        )
        stable_metrics = _stable_baseline(Image.open(source).convert("RGB"), colours, case["reference"])
        if case["expected"] == "success":
            passed = (
                candidate_metrics["numeric_output_authorized"]
                and candidate_metrics["coverage"] == 1.0
                and candidate_metrics["mae"] <= 0.05
                and candidate_metrics["max_abs_error"] <= 0.11
            )
        else:
            passed = (
                not candidate_metrics["numeric_output_authorized"]
                and candidate_metrics["status"] == "low_confidence"
                and candidate_metrics["coverage"] == 0.0
            )
        reports.append(
            {
                "case_id": case["id"],
                "expected": case["expected"],
                "source_sha256": file_sha256(source),
                "candidate": candidate_metrics,
                "stable_baseline": stable_metrics,
                "gate_passed": bool(passed),
            }
        )
    success = all(item["gate_passed"] for item in reports)
    report = {
        "schema_version": 1,
        "status": "passed" if success else "failed",
        "run_id": output_dir.name,
        "identity": identity,
        "truth_role": "independent_synthetic_validation_only_after_extraction",
        "cases": reports,
        "webplotdigitizer": {
            "status": "not_compared",
            "reason": "No matched assisted WebPlotDigitizer session was available in this local run.",
        },
        "promotion_scope": "candidate evidence only; real held-out and user-approved promotion gates remain open",
    }
    (output_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not success:
        raise RuntimeError(f"marker-line benchmark gates failed; evidence preserved at {output_dir}")
    return output_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()
    output_dir = run_benchmark(args.output_root)
    print(json.dumps({"status": "passed", "run_id": output_dir.name, "output_dir": str(output_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

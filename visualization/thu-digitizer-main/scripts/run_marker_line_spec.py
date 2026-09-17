"""Execute the candidate compact-marker line route from a verified FigureSpec.

This adapter closes the gap between a descriptive FigureSpec and the actual
candidate invocation.  It validates every route-specific field, verifies the
source bytes and dimensions, binds the declared axes/colours/sample positions
to the extractor, and writes a new immutable evidence directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Sequence

from PIL import Image

try:
    from candidate_digitize_marker_line import file_sha256, write_evidence_bundle
    from figure_spec import assert_valid_figure_spec, figure_spec_readiness
    from raster_digitizer_core import AxisCalibration
except ImportError:  # pragma: no cover
    from .candidate_digitize_marker_line import file_sha256, write_evidence_bundle
    from .figure_spec import assert_valid_figure_spec, figure_spec_readiness
    from .raster_digitizer_core import AxisCalibration


ROUTE_ID = "raster_marker_line_candidate"
RUNNER_VERSION = "marker_line_figure_spec_v0.1.0-candidate"
PANEL_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")


class MarkerLineSpecError(ValueError):
    """Raised when a valid generic FigureSpec lacks candidate route inputs."""


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _parse_sample_values(value: Any, *, path: str) -> list[float]:
    if isinstance(value, list) and value and all(_is_number(item) for item in value):
        samples = [float(item) for item in value]
    elif isinstance(value, str):
        parts = value.split(":")
        if len(parts) != 3:
            raise MarkerLineSpecError(f"{path} must be a numeric list or start:step:stop")
        try:
            start, step, stop = (float(item) for item in parts)
        except ValueError as exc:
            raise MarkerLineSpecError(f"{path} contains a non-numeric range") from exc
        if step <= 0 or stop < start:
            raise MarkerLineSpecError(f"{path} range requires step > 0 and stop >= start")
        count = int(round((stop - start) / step))
        if abs(start + count * step - stop) > max(1e-9, abs(step) * 1e-8):
            raise MarkerLineSpecError(f"{path} stop must lie exactly on the declared step")
        samples = [start + index * step for index in range(count + 1)]
    else:
        raise MarkerLineSpecError(f"{path} must be a non-empty numeric list or start:step:stop")
    if samples != sorted(samples) or len(set(samples)) != len(samples):
        raise MarkerLineSpecError(f"{path} must be strictly increasing and unique")
    return samples


def _parse_colours(series: dict[str, Any], *, path: str) -> list[tuple[int, int, int]]:
    raw = series.get("marker_colors_rgb")
    if raw is None and "marker_color_rgb" in series:
        raw = [series["marker_color_rgb"]]
    if raw is None:
        raw = series.get("colours_rgb")
    if not isinstance(raw, list) or not raw:
        raise MarkerLineSpecError(f"{path} needs marker_color_rgb or marker_colors_rgb")
    colours: list[tuple[int, int, int]] = []
    for index, colour in enumerate(raw):
        if (
            not isinstance(colour, list)
            or len(colour) != 3
            or not all(isinstance(channel, int) and not isinstance(channel, bool) for channel in colour)
            or not all(0 <= channel <= 255 for channel in colour)
        ):
            raise MarkerLineSpecError(f"{path}.marker_colors_rgb[{index}] must be three integers in 0..255")
        colours.append(tuple(colour))
    if len(set(colours)) != len(colours):
        raise MarkerLineSpecError(f"{path} marker colour templates must be unique")
    return colours


def _verified_axis(panel: dict[str, Any], orientation: str, *, path: str) -> AxisCalibration:
    matches = [axis for axis in panel.get("axes", []) if axis.get("orientation", axis.get("axis_id")) == orientation]
    if len(matches) != 1:
        raise MarkerLineSpecError(f"{path}.axes must contain exactly one {orientation!r} axis")
    axis = matches[0]
    if axis.get("verification") != "verified":
        raise MarkerLineSpecError(f"{path} {orientation}-axis must be verified")
    scale = axis.get("scale")
    if scale not in {"linear", "log10", "displayed_log10"}:
        raise MarkerLineSpecError(f"{path} {orientation}-axis scale {scale!r} is unsupported")
    anchors = [(float(item["pixel"]), float(item["value"])) for item in axis["anchors"]]
    return AxisCalibration.fit(anchors, scale=scale)


def _number_parameter(parameters: dict[str, Any], name: str, default: float) -> float:
    value = parameters.get(name, default)
    if not _is_number(value):
        raise MarkerLineSpecError(f"extraction_parameters.{name} must be numeric")
    return float(value)


def bind_panel(panel: dict[str, Any], *, panel_index: int) -> dict[str, Any]:
    path = f"panels[{panel_index}]"
    panel_id = panel.get("panel_id")
    if not isinstance(panel_id, str) or not PANEL_ID_PATTERN.fullmatch(panel_id):
        raise MarkerLineSpecError(f"{path}.panel_id must be filesystem-safe")
    route = panel.get("route", {})
    if route.get("route_id") != ROUTE_ID:
        raise MarkerLineSpecError(f"{path}.route.route_id must equal {ROUTE_ID!r}")
    if panel.get("coordinate_model") != "cartesian_linear":
        raise MarkerLineSpecError(f"{path} currently supports cartesian_linear only")
    grammars = set(panel.get("mark_grammars", []))
    if "marker" not in grammars:
        raise MarkerLineSpecError(f"{path}.mark_grammars must include 'marker'")
    plot_bounds = tuple(int(value) for value in panel["plot_bounds"])
    x_axis = _verified_axis(panel, "x", path=path)
    y_axis = _verified_axis(panel, "y", path=path)
    raw_series = panel.get("series")
    if not isinstance(raw_series, list) or not raw_series:
        raise MarkerLineSpecError(f"{path}.series must be a non-empty list")
    series: list[tuple[str, Sequence[Sequence[int]]]] = []
    sample_values: list[float] | None = None
    names: set[str] = set()
    for series_index, item in enumerate(raw_series):
        series_path = f"{path}.series[{series_index}]"
        if not isinstance(item, dict):
            raise MarkerLineSpecError(f"{series_path} must be an object")
        name = item.get("name")
        if not isinstance(name, str) or not name or name in names:
            raise MarkerLineSpecError(f"{series_path}.name must be non-empty and unique")
        names.add(name)
        current_samples = _parse_sample_values(
            item.get("sample_values", panel.get("sample_values")), path=f"{series_path}.sample_values"
        )
        if sample_values is None:
            sample_values = current_samples
        elif current_samples != sample_values:
            raise MarkerLineSpecError(f"{path} all series must declare identical sample_values")
        series.append((name, _parse_colours(item, path=series_path)))
    parameters = panel.get("extraction_parameters", {})
    if not isinstance(parameters, dict):
        raise MarkerLineSpecError(f"{path}.extraction_parameters must be an object")
    reference_lines = panel.get("reference_lines", parameters.get("reference_lines", []))
    if not isinstance(reference_lines, list) or not all(_is_number(value) for value in reference_lines):
        raise MarkerLineSpecError(f"{path}.reference_lines must be a numeric list")
    bound_parameters = {
        "color_tolerance": _number_parameter(parameters, "color_tolerance", 12.0),
        "sample_radius": int(_number_parameter(parameters, "sample_radius", 8)),
        "marker_radius_min": int(_number_parameter(parameters, "marker_radius_min", 3)),
        "transition_weight": _number_parameter(parameters, "transition_weight", 0.08),
        "curvature_weight": _number_parameter(parameters, "curvature_weight", 0.03),
        "confidence_threshold": _number_parameter(parameters, "confidence_threshold", 0.55),
    }
    if bound_parameters["color_tolerance"] <= 0 or bound_parameters["sample_radius"] < 1 or bound_parameters["marker_radius_min"] < 1:
        raise MarkerLineSpecError(f"{path} colour tolerance and marker radii must be positive")
    if not 0 < bound_parameters["confidence_threshold"] < 1:
        raise MarkerLineSpecError(f"{path}.extraction_parameters.confidence_threshold must lie in (0, 1)")
    return {
        "panel_id": panel_id,
        "plot_bounds": plot_bounds,
        "x_axis": x_axis,
        "y_axis": y_axis,
        "sample_values": sample_values or [],
        "series": series,
        "reference_lines": [float(value) for value in reference_lines],
        **bound_parameters,
    }


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def execute_spec(spec_path: Path, output_root: Path) -> Path:
    spec_path = spec_path.resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    assert_valid_figure_spec(spec)
    readiness = figure_spec_readiness(spec)
    if readiness["status"] != "ready_for_assisted_extraction":
        raise MarkerLineSpecError("FigureSpec confirmations are not ready for assisted extraction")
    source = spec["source"]
    input_path = Path(source.get("input_file", ""))
    if not input_path.is_absolute():
        input_path = (spec_path.parent / input_path).resolve()
    if not input_path.is_file():
        raise MarkerLineSpecError(f"source.input_file does not exist: {input_path}")
    actual_hash = file_sha256(input_path)
    if actual_hash != source["sha256"]:
        raise MarkerLineSpecError("source SHA-256 does not match FigureSpec")
    with Image.open(input_path) as image:
        if image.size != (int(source["width"]), int(source["height"])):
            raise MarkerLineSpecError("source raster dimensions do not match FigureSpec")
    bindings = [bind_panel(panel, panel_index=index) for index, panel in enumerate(spec["panels"])]
    implementation_path = Path(__file__).with_name("candidate_digitize_marker_line.py").resolve()
    execution_identity = {
        "runner_version": RUNNER_VERSION,
        "runner_sha256": file_sha256(Path(__file__).resolve()),
        "extractor_sha256": file_sha256(implementation_path),
        "figure_spec_sha256": hashlib.sha256(_canonical_json(spec)).hexdigest(),
        "source_sha256": actual_hash,
    }
    execution_hash = hashlib.sha256(_canonical_json(execution_identity)).hexdigest()
    run_dir = output_root.resolve() / f"marker-line-spec-{execution_hash[:16]}"
    if run_dir.exists():
        raise FileExistsError(f"immutable FigureSpec run directory already exists: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=False)
    panel_reports = []
    try:
        for binding in bindings:
            panel_root = run_dir / "panels" / binding["panel_id"]
            panel_dir = write_evidence_bundle(
                input_path=input_path,
                output_root=panel_root,
                plot_bounds=binding["plot_bounds"],
                x_axis=binding["x_axis"],
                y_axis=binding["y_axis"],
                sample_values=binding["sample_values"],
                series=binding["series"],
                color_tolerance=binding["color_tolerance"],
                sample_radius=binding["sample_radius"],
                marker_radius_min=binding["marker_radius_min"],
                reference_lines=binding["reference_lines"],
                transition_weight=binding["transition_weight"],
                curvature_weight=binding["curvature_weight"],
                confidence_threshold=binding["confidence_threshold"],
            )
            report = json.loads((panel_dir / "report.json").read_text(encoding="utf-8"))
            panel_reports.append(
                {
                    "panel_id": binding["panel_id"],
                    "run_id": report["run_id"],
                    "status": report["status"],
                    "numeric_output_authorized": report["numeric_output_authorized"],
                    "relative_directory": str(panel_dir.relative_to(run_dir)).replace("\\", "/"),
                }
            )
    except Exception as exc:
        (run_dir / "failure.json").write_text(
            json.dumps({"status": "failed", "error_type": type(exc).__name__, "message": str(exc)}, indent=2) + "\n",
            encoding="utf-8",
        )
        raise
    authorized = all(item["numeric_output_authorized"] for item in panel_reports)
    manifest = {
        "schema_version": 1,
        "status": "candidate_extracted" if authorized else "low_confidence",
        "numeric_output_authorized": authorized,
        "run_id": run_dir.name,
        "execution_identity": execution_identity,
        "source": {"file": str(input_path), "sha256": actual_hash},
        "figure_spec": {"file": str(spec_path), "sha256": execution_identity["figure_spec_sha256"]},
        "panels": panel_reports,
        "immutability": "A repeated identical execution is refused instead of overwriting evidence.",
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure-spec", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()
    run_dir = execute_spec(args.figure_spec, args.output_root)
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    print(json.dumps({"status": manifest["status"], "run_id": manifest["run_id"], "output_dir": str(run_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

"""Shared, auditable configuration schema for THU Digitizer figure routes.

The schema deliberately separates proposals from verified extraction inputs.
A syntactically valid spec is not evidence that a chart was correctly
classified or calibrated; verification statuses remain explicit fields.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
MEDIA_KINDS = {"raster", "pdf"}
COORDINATE_MODELS = {
    "unknown",
    "cartesian_linear",
    "cartesian_log_x",
    "cartesian_displayed_log_x",
    "cartesian_log_y",
    "cartesian_log_log",
    "cartesian_date_x",
    "categorical_value",
    "grid_color",
    "lattice_composite",
    "interval_rows",
    "polar",
    "ternary",
    "geospatial",
    "graph",
    "flow",
    "event_raster",
}
AXIS_SCALES = {
    "linear",
    "log10",
    "displayed_log10",
    "date",
    "categorical",
    "color",
    "none",
    "unknown",
}
SPEC_STATUSES = {
    "needs_chart_type_confirmation",
    "needs_verified_configuration",
    "ready_for_assisted_extraction",
    "not_automated",
    "unsupported",
    "low_confidence",
}
VERIFICATION_STATUSES = {"missing", "proposed", "user_provided", "verified", "not_applicable"}


class FigureSpecError(ValueError):
    """Raised when a figure spec violates the shared structural contract."""


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate_bounds(
    bounds: Any,
    *,
    width: float,
    height: float,
    path: str,
    errors: list[str],
) -> None:
    if not isinstance(bounds, list) or len(bounds) != 4 or not all(_is_number(item) for item in bounds):
        errors.append(f"{path} must contain four numeric coordinates")
        return
    left, top, right, bottom = (float(item) for item in bounds)
    if not (0 <= left < right <= width and 0 <= top < bottom <= height):
        errors.append(
            f"{path}={bounds} must satisfy 0 <= left < right <= {width} and "
            f"0 <= top < bottom <= {height}"
        )


def _validate_axis(axis: Any, *, path: str, errors: list[str]) -> None:
    if not isinstance(axis, dict):
        errors.append(f"{path} must be an object")
        return
    scale = axis.get("scale")
    if scale not in AXIS_SCALES:
        errors.append(f"{path}.scale must be one of {sorted(AXIS_SCALES)}")
    verification = axis.get("verification")
    if verification not in VERIFICATION_STATUSES:
        errors.append(f"{path}.verification must be one of {sorted(VERIFICATION_STATUSES)}")
    anchors = axis.get("anchors", [])
    if not isinstance(anchors, list):
        errors.append(f"{path}.anchors must be a list")
        return
    if verification == "verified" and scale in {"linear", "log10", "displayed_log10", "date", "color"} and len(anchors) < 2:
        errors.append(f"{path} requires at least two anchors when verified")

    pixels: list[float] = []
    numeric_values: list[float] = []
    for anchor_index, anchor in enumerate(anchors):
        anchor_path = f"{path}.anchors[{anchor_index}]"
        if not isinstance(anchor, dict):
            errors.append(f"{anchor_path} must be an object")
            continue
        if not _is_number(anchor.get("pixel")):
            errors.append(f"{anchor_path}.pixel must be numeric")
        else:
            pixels.append(float(anchor["pixel"]))
        value = anchor.get("value")
        if scale in {"linear", "log10", "displayed_log10", "color"}:
            if not _is_number(value):
                errors.append(f"{anchor_path}.value must be numeric for {scale}")
            else:
                numeric_values.append(float(value))
                if scale == "log10" and float(value) <= 0:
                    errors.append(f"{anchor_path}.value must be positive for log10 calibration")
        elif scale == "date" and not isinstance(value, str):
            errors.append(f"{anchor_path}.value must be an ISO-like string for date calibration")

    if verification == "verified" and len(pixels) >= 2 and len(set(pixels)) != len(pixels):
        errors.append(f"{path} verified anchor pixels must be distinct")
    if (
        verification == "verified"
        and scale in {"linear", "log10", "displayed_log10", "color"}
        and len(numeric_values) >= 2
        and len(set(numeric_values)) != len(numeric_values)
    ):
        errors.append(f"{path} verified anchor values must be distinct")


def validate_figure_spec(spec: Any) -> list[str]:
    """Return all structural validation errors without mutating the spec."""

    errors: list[str] = []
    if not isinstance(spec, dict):
        return ["figure spec must be a JSON object"]
    if spec.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must equal {SCHEMA_VERSION}")
    if spec.get("status") not in SPEC_STATUSES:
        errors.append(f"status must be one of {sorted(SPEC_STATUSES)}")

    source = spec.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
        return errors
    if source.get("media_kind") not in MEDIA_KINDS:
        errors.append(f"source.media_kind must be one of {sorted(MEDIA_KINDS)}")
    if source.get("media_kind") == "raster" and source.get("coordinate_space") != "pixel":
        errors.append("raster source.coordinate_space must equal 'pixel'")
    measurement_space = source.get("measurement_space")
    if measurement_space not in {None, "original_raster_pixels", "pdf_page_points"}:
        errors.append("source.measurement_space must be original_raster_pixels or pdf_page_points")
    if source.get("media_kind") == "raster" and measurement_space not in {None, "original_raster_pixels"}:
        errors.append("raster measurements must stay in original_raster_pixels")
    if source.get("resampling_applied") is True:
        errors.append("source.resampling_applied must be false for extraction measurements")
    width = source.get("width")
    height = source.get("height")
    if not _is_number(width) or float(width) <= 0:
        errors.append("source.width must be positive")
    if not _is_number(height) or float(height) <= 0:
        errors.append("source.height must be positive")
    if not isinstance(source.get("sha256"), str) or len(source.get("sha256", "")) != 64:
        errors.append("source.sha256 must be a 64-character hexadecimal digest")

    panels = spec.get("panels")
    if not isinstance(panels, list) or not panels:
        errors.append("panels must be a non-empty list")
        return errors
    if not _is_number(width) or not _is_number(height):
        return errors

    panel_ids = set()
    for panel_index, panel in enumerate(panels):
        path = f"panels[{panel_index}]"
        if not isinstance(panel, dict):
            errors.append(f"{path} must be an object")
            continue
        panel_id = panel.get("panel_id")
        if not isinstance(panel_id, str) or not panel_id:
            errors.append(f"{path}.panel_id must be a non-empty string")
        elif panel_id in panel_ids:
            errors.append(f"{path}.panel_id must be unique")
        else:
            panel_ids.add(panel_id)
        _validate_bounds(
            panel.get("bounds"),
            width=float(width),
            height=float(height),
            path=f"{path}.bounds",
            errors=errors,
        )
        if panel.get("bounds_verification") not in VERIFICATION_STATUSES:
            errors.append(f"{path}.bounds_verification must be one of {sorted(VERIFICATION_STATUSES)}")
        _validate_bounds(
            panel.get("plot_bounds"),
            width=float(width),
            height=float(height),
            path=f"{path}.plot_bounds",
            errors=errors,
        )
        if panel.get("plot_bounds_verification") not in VERIFICATION_STATUSES:
            errors.append(
                f"{path}.plot_bounds_verification must be one of {sorted(VERIFICATION_STATUSES)}"
            )
        panel_bounds = panel.get("bounds")
        plot_bounds = panel.get("plot_bounds")
        if (
            isinstance(panel_bounds, list)
            and len(panel_bounds) == 4
            and all(_is_number(item) for item in panel_bounds)
            and isinstance(plot_bounds, list)
            and len(plot_bounds) == 4
            and all(_is_number(item) for item in plot_bounds)
        ):
            if not (
                panel_bounds[0] <= plot_bounds[0] < plot_bounds[2] <= panel_bounds[2]
                and panel_bounds[1] <= plot_bounds[1] < plot_bounds[3] <= panel_bounds[3]
            ):
                errors.append(f"{path}.plot_bounds must stay inside panel bounds")
        if panel.get("coordinate_model") not in COORDINATE_MODELS:
            errors.append(
                f"{path}.coordinate_model must be one of {sorted(COORDINATE_MODELS)}"
            )
        axes = panel.get("axes", [])
        if not isinstance(axes, list):
            errors.append(f"{path}.axes must be a list")
        else:
            for axis_index, axis in enumerate(axes):
                _validate_axis(axis, path=f"{path}.axes[{axis_index}]", errors=errors)
        if not isinstance(panel.get("mark_grammars", []), list):
            errors.append(f"{path}.mark_grammars must be a list")
        route = panel.get("route")
        if not isinstance(route, dict) or not isinstance(route.get("route_id"), str):
            errors.append(f"{path}.route.route_id must be a string")
        required_confirmations = panel.get("required_confirmations", [])
        confirmations = panel.get("confirmations", {})
        if not isinstance(required_confirmations, list):
            errors.append(f"{path}.required_confirmations must be a list")
        if not isinstance(confirmations, dict):
            errors.append(f"{path}.confirmations must be an object")
        elif isinstance(required_confirmations, list):
            for name in required_confirmations:
                if confirmations.get(name) not in VERIFICATION_STATUSES:
                    errors.append(
                        f"{path}.confirmations.{name} must be one of {sorted(VERIFICATION_STATUSES)}"
                    )
                elif spec.get("status") == "ready_for_assisted_extraction" and confirmations[name] not in {
                    "verified",
                    "not_applicable",
                }:
                    errors.append(
                        f"{path}.confirmations.{name} must be verified before ready_for_assisted_extraction"
                    )

    return errors


def assert_valid_figure_spec(spec: Any) -> None:
    errors = validate_figure_spec(spec)
    if errors:
        raise FigureSpecError("; ".join(errors))


def figure_spec_readiness(spec: Any) -> dict[str, Any]:
    errors = validate_figure_spec(spec)
    if errors:
        return {"status": "invalid", "errors": errors, "panels": []}
    panels = []
    for panel in spec["panels"]:
        missing = [
            name
            for name in panel.get("required_confirmations", [])
            if panel.get("confirmations", {}).get(name) not in {"verified", "not_applicable"}
        ]
        panels.append({"panel_id": panel["panel_id"], "missing_confirmations": missing})
    ready = all(not panel["missing_confirmations"] for panel in panels)
    return {
        "status": "ready_for_assisted_extraction" if ready else "needs_verified_configuration",
        "errors": [],
        "panels": panels,
    }


def write_figure_spec(path: Path, spec: dict[str, Any]) -> None:
    assert_valid_figure_spec(spec)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_figure_spec(path: Path) -> dict[str, Any]:
    spec = json.loads(path.read_text(encoding="utf-8"))
    assert_valid_figure_spec(spec)
    return spec

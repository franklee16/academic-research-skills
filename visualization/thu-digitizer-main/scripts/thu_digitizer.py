"""Unified preflight router for THU Digitizer.

This CLI inspects an input, selects a conservative registered route, and writes
an auditable FigureSpec template.  It does not turn a route proposal into a
verified extraction and does not silently execute an incompatible extractor.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import fitz
import numpy as np
from PIL import Image

try:
    from extractor_registry import registry_document, select_route
    from figure_spec import (
        assert_valid_figure_spec,
        figure_spec_readiness,
        read_figure_spec,
        write_figure_spec,
    )
    from inspect_pdf_vectors import inspect_page
except ImportError:  # pragma: no cover - package-style invocation
    from .extractor_registry import registry_document, select_route
    from .figure_spec import (
        assert_valid_figure_spec,
        figure_spec_readiness,
        read_figure_spec,
        write_figure_spec,
    )
    from .inspect_pdf_vectors import inspect_page


RASTER_SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_bounds(value: str) -> tuple[float, float, float, float]:
    parts = value.split(",")
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("bounds must be left,top,right,bottom")
    try:
        bounds = tuple(float(item) for item in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("bounds must contain four numbers") from exc
    left, top, right, bottom = bounds
    if not left < right or not top < bottom:
        raise argparse.ArgumentTypeError("bounds must satisfy left < right and top < bottom")
    return bounds


def _appearance(rgb: np.ndarray) -> dict[str, Any]:
    rows, columns, _ = rgb.shape
    border = np.concatenate(
        [
            rgb[0, :, :],
            rgb[-1, :, :],
            rgb[:, 0, :],
            rgb[:, -1, :],
        ],
        axis=0,
    ).astype(float)
    luminance = 0.2126 * border[:, 0] + 0.7152 * border[:, 1] + 0.0722 * border[:, 2]
    colour_span = border.max(axis=1) - border.min(axis=1)
    median_luminance = float(np.median(luminance))
    if median_luminance >= 210:
        background = "light"
    elif median_luminance <= 55:
        background = "dark"
    else:
        background = "mixed_or_coloured"
    return {
        "background_proposal": background,
        "border_median_luminance_0_255": median_luminance,
        "border_colour_span_median_0_255": float(np.median(colour_span)),
        "pixel_count": int(rows * columns),
        "role": "appearance proposal only; not chart classification or numeric evidence",
    }


def inspect_input(path: Path, *, page_number: int | None = None) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    suffix = path.suffix.lower()
    common = {
        "input_file": str(path.resolve()),
        "input_sha256": sha256(path),
        "file_size_bytes": path.stat().st_size,
    }
    if suffix == ".pdf":
        with fitz.open(path) as document:
            page = page_number or 1
            if not 1 <= page <= len(document):
                raise ValueError(f"page must be within 1..{len(document)}")
            page_report = inspect_page(document, page - 1)
            rectangle = document[page - 1].rect
            return {
                **common,
                "media_kind": "pdf",
                "coordinate_space": "pdf_pt",
                "page_count": len(document),
                "selected_page": page,
                "page_selection": "user_provided" if page_number is not None else "default_first_page_proposal",
                "width": float(rectangle.width),
                "height": float(rectangle.height),
                "pdf_composition": page_report["composition_status"],
                "pdf_inspection": page_report,
            }
    if suffix not in RASTER_SUFFIXES:
        raise ValueError(
            f"unsupported input suffix {suffix or '<none>'}; expected PDF or one of {sorted(RASTER_SUFFIXES)}"
        )
    with Image.open(path) as image:
        image.load()
        rgb = np.asarray(image.convert("RGB"))
        return {
            **common,
            "media_kind": "raster",
            "coordinate_space": "pixel",
            "format": image.format,
            "mode": image.mode,
            "width": int(image.width),
            "height": int(image.height),
            "appearance": _appearance(rgb),
        }


def _axis_templates(coordinate_model: str) -> list[dict[str, Any]]:
    if coordinate_model in {
        "cartesian_linear",
        "cartesian_log_x",
        "cartesian_displayed_log_x",
        "cartesian_log_y",
        "cartesian_log_log",
        "cartesian_date_x",
    }:
        x_scale = {
            "cartesian_log_x": "log10",
            "cartesian_displayed_log_x": "displayed_log10",
            "cartesian_log_log": "log10",
            "cartesian_date_x": "date",
        }.get(coordinate_model, "linear")
        y_scale = "log10" if coordinate_model in {"cartesian_log_y", "cartesian_log_log"} else "linear"
        return [
            {"axis_id": "x", "orientation": "x", "scale": x_scale, "verification": "missing", "anchors": []},
            {"axis_id": "y", "orientation": "y", "scale": y_scale, "verification": "missing", "anchors": []},
        ]
    if coordinate_model == "categorical_value":
        return [
            {"axis_id": "category", "orientation": "category", "scale": "categorical", "verification": "missing", "anchors": []},
            {"axis_id": "value", "orientation": "value", "scale": "linear", "verification": "missing", "anchors": []},
        ]
    if coordinate_model == "grid_color":
        return [
            {"axis_id": "row", "orientation": "row", "scale": "categorical", "verification": "missing", "anchors": []},
            {"axis_id": "column", "orientation": "column", "scale": "categorical", "verification": "missing", "anchors": []},
            {"axis_id": "color", "orientation": "color", "scale": "color", "verification": "missing", "anchors": []},
        ]
    if coordinate_model == "lattice_composite":
        return [
            {"axis_id": "column", "orientation": "column", "scale": "categorical", "verification": "missing", "anchors": []},
            {"axis_id": "row", "orientation": "row", "scale": "categorical", "verification": "missing", "anchors": []},
            {"axis_id": "column_value", "orientation": "y", "scale": "linear", "verification": "missing", "anchors": []},
            {"axis_id": "row_value", "orientation": "x", "scale": "linear", "verification": "missing", "anchors": []},
        ]
    if coordinate_model == "interval_rows":
        return [
            {"axis_id": "row", "orientation": "row", "scale": "categorical", "verification": "missing", "anchors": []},
            {"axis_id": "value", "orientation": "value", "scale": "linear", "verification": "missing", "anchors": []},
        ]
    return []


def build_preflight(
    path: Path,
    *,
    chart_type: str | None = None,
    page_number: int | None = None,
    panel_bounds: tuple[float, float, float, float] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    inspection = inspect_input(path, page_number=page_number)
    selection = select_route(
        chart_type=chart_type,
        media_kind=inspection["media_kind"],
        pdf_composition=inspection.get("pdf_composition"),
    )
    route = selection["primary"]
    coordinate_models = route["coordinate_models"]
    coordinate_model = coordinate_models[0] if len(coordinate_models) == 1 else "unknown"
    bounds = list(panel_bounds) if panel_bounds is not None else [0.0, 0.0, inspection["width"], inspection["height"]]
    bounds_verification = "user_provided" if panel_bounds is not None else "proposed"

    figure_spec = {
        "schema_version": 1,
        "status": selection["decision"],
        "source": {
            "input_file": inspection["input_file"],
            "sha256": inspection["input_sha256"],
            "media_kind": inspection["media_kind"],
            "coordinate_space": inspection["coordinate_space"],
            "measurement_space": (
                "original_raster_pixels"
                if inspection["media_kind"] == "raster"
                else "pdf_page_points"
            ),
            "resampling_applied": False,
            "width": inspection["width"],
            "height": inspection["height"],
            "page": inspection.get("selected_page"),
        },
        "panels": [
            {
                "panel_id": "panel-1",
                "bounds": bounds,
                "bounds_verification": bounds_verification,
                "plot_bounds": bounds,
                "plot_bounds_verification": "proposed",
                "chart_type": selection["chart_type"] or "unknown",
                "chart_type_verification": "user_provided" if chart_type else "missing",
                "coordinate_model": coordinate_model,
                "coordinate_model_verification": "proposed" if coordinate_model != "unknown" else "missing",
                "axes": _axis_templates(coordinate_model),
                "series": [],
                "mark_grammars": route["mark_grammars"],
                "route": {
                    "route_id": route["route_id"],
                    "maturity": route["maturity"],
                    "implementation": route["implementation"],
                    "automated_extraction": route["automated_extraction"],
                },
                "required_confirmations": route["required_confirmations"],
                "confirmations": {
                    name: (
                        "user_provided"
                        if name == "panel_roi" and panel_bounds is not None
                        else "user_provided"
                        if name == "page" and inspection.get("page_selection") == "user_provided"
                        else "proposed"
                        if name == "page" and inspection.get("selected_page") is not None
                        else "missing"
                    )
                    for name in route["required_confirmations"]
                },
                "recoverable": route["recoverable"],
                "non_recoverable": route["non_recoverable"],
            }
        ],
        "evidence_contract": {
            "required": [
                "input_hash",
                "panel_and_plot_bounds",
                "calibration_anchors",
                "immutable_extraction_csv",
                "json_report",
                "overlay_or_recreation",
                "confidence_and_refusal_reasons",
            ],
            "source_data_role": "independent_validation_only",
        },
    }
    assert_valid_figure_spec(figure_spec)

    report = {
        "schema_version": 1,
        "status": selection["decision"],
        "inspection": inspection,
        "route_selection": selection,
        "figure_spec_status": "valid_template_not_yet_verified",
        "safety": {
            "numeric_extraction_authorized": False,
            "reason": "Preflight routing never converts proposed chart type, ROI, axes, or series into verified values.",
        },
    }
    return report, figure_spec


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    routes = subparsers.add_parser("routes", help="List registered stable, candidate, and refusal routes")
    routes.add_argument("--output", type=Path)

    inspect = subparsers.add_parser("inspect", help="Inspect an input and write a conservative route/spec template")
    inspect.add_argument("--input", required=True, type=Path)
    inspect.add_argument("--page", type=int)
    inspect.add_argument("--chart-type")
    inspect.add_argument("--panel-bounds", type=parse_bounds)
    inspect.add_argument("--output-report", required=True, type=Path)
    inspect.add_argument("--output-spec", required=True, type=Path)

    validate = subparsers.add_parser("validate-spec", help="Validate a FigureSpec without running extraction")
    validate.add_argument("--spec", required=True, type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "routes":
        document = registry_document()
        if args.output:
            _write_json(args.output, document)
        else:
            print(json.dumps(document, ensure_ascii=False, indent=2))
        return
    if args.command == "validate-spec":
        spec = read_figure_spec(args.spec)
        readiness = figure_spec_readiness(spec)
        print(
            json.dumps(
                {"status": "valid", "readiness": readiness, "panels": len(spec["panels"])},
                ensure_ascii=False,
            )
        )
        return

    report, spec = build_preflight(
        args.input,
        chart_type=args.chart_type,
        page_number=args.page,
        panel_bounds=args.panel_bounds,
    )
    _write_json(args.output_report, report)
    write_figure_spec(args.output_spec, spec)
    print(
        json.dumps(
            {
                "status": report["status"],
                "route": report["route_selection"]["primary"]["route_id"],
                "report": str(args.output_report),
                "spec": str(args.output_spec),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

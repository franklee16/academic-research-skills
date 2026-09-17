"""Recreate multi-panel line figures from extracted CSV data and a style spec.

The renderer uses an exact pixel canvas, keeps all plot geometry vector-native,
and writes an immutable bundle containing PNG, 3x PNG, SVG, PDF, and a manifest.
It never reads the source figure as a visual layer; the recreation is driven by
declared style geometry plus extracted CSV values.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image


RENDERER_VERSION = "exact_canvas_line_recreation_v0.1.0"


class RecreationSpecError(ValueError):
    """Raised when a recreation spec is structurally incomplete."""


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _numbers(value: Any, count: int, path: str) -> list[float]:
    if not isinstance(value, list) or len(value) != count or not all(_is_number(item) for item in value):
        raise RecreationSpecError(f"{path} must contain {count} numbers")
    return [float(item) for item in value]


def _resolve_file(raw: Any, *, spec_path: Path, path: str) -> Path:
    if not isinstance(raw, str) or not raw:
        raise RecreationSpecError(f"{path} must be a file path")
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = (spec_path.parent / candidate).resolve()
    if not candidate.is_file():
        raise RecreationSpecError(f"{path} does not exist: {candidate}")
    return candidate


def validate_and_bind_spec(spec: Any, spec_path: Path) -> dict[str, Any]:
    if not isinstance(spec, dict) or spec.get("schema_version") != 1:
        raise RecreationSpecError("schema_version must equal 1")
    canvas = spec.get("canvas")
    if not isinstance(canvas, dict):
        raise RecreationSpecError("canvas must be an object")
    width = canvas.get("width")
    height = canvas.get("height")
    if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
        raise RecreationSpecError("canvas width and height must be positive integers")
    default_csv = None
    if "data_csv" in spec:
        default_csv = _resolve_file(spec["data_csv"], spec_path=spec_path, path="data_csv")
    panels = spec.get("panels")
    if not isinstance(panels, list) or not panels:
        raise RecreationSpecError("panels must be a non-empty list")
    bound_panels = []
    panel_ids: set[str] = set()
    for panel_index, panel in enumerate(panels):
        path = f"panels[{panel_index}]"
        if not isinstance(panel, dict):
            raise RecreationSpecError(f"{path} must be an object")
        panel_id = panel.get("panel_id")
        if not isinstance(panel_id, str) or not panel_id or panel_id in panel_ids:
            raise RecreationSpecError(f"{path}.panel_id must be non-empty and unique")
        panel_ids.add(panel_id)
        bounds = _numbers(panel.get("bounds_px"), 4, f"{path}.bounds_px")
        left, top, right, bottom = bounds
        if not (0 <= left < right <= width and 0 <= top < bottom <= height):
            raise RecreationSpecError(f"{path}.bounds_px must stay within the canvas")
        xlim = _numbers(panel.get("xlim"), 2, f"{path}.xlim")
        ylim = _numbers(panel.get("ylim"), 2, f"{path}.ylim")
        if xlim[0] >= xlim[1] or ylim[0] >= ylim[1]:
            raise RecreationSpecError(f"{path} axis limits must be increasing")
        data_csv = (
            _resolve_file(panel["data_csv"], spec_path=spec_path, path=f"{path}.data_csv")
            if "data_csv" in panel
            else default_csv
        )
        if data_csv is None:
            raise RecreationSpecError(f"{path} needs data_csv or a top-level data_csv")
        series = panel.get("series")
        if not isinstance(series, list) or not series:
            raise RecreationSpecError(f"{path}.series must be a non-empty list")
        with data_csv.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            columns = set(reader.fieldnames or [])
            rows = list(reader)
        if not rows:
            raise RecreationSpecError(f"{path}.data_csv has no rows")
        for series_index, item in enumerate(series):
            item_path = f"{path}.series[{series_index}]"
            if not isinstance(item, dict):
                raise RecreationSpecError(f"{item_path} must be an object")
            for field in ("x_column", "y_column"):
                if item.get(field) not in columns:
                    raise RecreationSpecError(f"{item_path}.{field} is not a CSV column")
        bound_panels.append({**panel, "bounds_px": bounds, "xlim": xlim, "ylim": ylim, "data_csv_path": data_csv, "rows": rows})
    return {**spec, "canvas": {**canvas, "width": width, "height": height}, "bound_panels": bound_panels}


def _float_rows(rows: list[dict[str, str]], x_column: str, y_column: str) -> tuple[list[float], list[float]]:
    points = []
    for row in rows:
        if row.get(x_column, "") == "" or row.get(y_column, "") == "":
            continue
        points.append((float(row[x_column]), float(row[y_column])))
    points.sort(key=lambda item: item[0])
    return [item[0] for item in points], [item[1] for item in points]


def _apply_axis_style(axis: Any, panel: dict[str, Any]) -> None:
    style = panel.get("axis_style", {})
    axis.set_xlim(*panel["xlim"])
    axis.set_ylim(*panel["ylim"])
    if "x_ticks" in panel:
        axis.set_xticks(panel["x_ticks"])
    if "y_ticks" in panel:
        axis.set_yticks(panel["y_ticks"])
    axis.tick_params(
        axis="both",
        which="major",
        direction=style.get("tick_direction", "in"),
        length=float(style.get("tick_length", 6)),
        width=float(style.get("tick_width", 1.2)),
        labelsize=float(style.get("tick_label_size", 10)),
        top=bool(style.get("ticks_top", False)),
        right=bool(style.get("ticks_right", False)),
        labelbottom=bool(panel.get("show_x_tick_labels", True)),
        labelleft=bool(panel.get("show_y_tick_labels", True)),
    )
    if style.get("minor_ticks", False):
        axis.minorticks_on()
    for spine in axis.spines.values():
        spine.set_linewidth(float(style.get("spine_width", 1.2)))
        spine.set_color(style.get("spine_color", "black"))
    axis.set_xlabel(panel.get("xlabel", ""), fontsize=float(style.get("axis_label_size", 12)), labelpad=float(style.get("xlabel_pad", 8)))
    axis.set_ylabel(panel.get("ylabel", ""), fontsize=float(style.get("axis_label_size", 12)), labelpad=float(style.get("ylabel_pad", 8)))


def _draw_decorations(axis: Any, decorations: list[dict[str, Any]]) -> None:
    for index, decoration in enumerate(decorations):
        kind = decoration.get("type")
        if kind == "scatter":
            points = decoration.get("points", [])
            if not isinstance(points, list) or not all(isinstance(point, list) and len(point) == 2 for point in points):
                raise RecreationSpecError(f"decorations[{index}].points must contain [x, y] pairs")
            colours = decoration.get("colors", decoration.get("color", "#2ca02c"))
            axis.scatter(
                [point[0] for point in points],
                [point[1] for point in points],
                s=float(decoration.get("size", 30)),
                c=colours,
                marker=decoration.get("marker", "o"),
                edgecolors=decoration.get("edgecolor", "none"),
                linewidths=float(decoration.get("edge_width", 0)),
                zorder=float(decoration.get("zorder", 4)),
                clip_on=bool(decoration.get("clip_on", True)),
            )
        elif kind == "vline":
            axis.vlines(
                float(decoration["x"]),
                float(decoration["y_min"]),
                float(decoration["y_max"]),
                colors=decoration.get("color", "black"),
                linewidth=float(decoration.get("line_width", 1)),
                linestyles=decoration.get("line_style", "--"),
                zorder=float(decoration.get("zorder", 3)),
            )
        else:
            raise RecreationSpecError(f"unsupported decoration type {kind!r}")


def build_figure(bound: dict[str, Any]):
    width = bound["canvas"]["width"]
    height = bound["canvas"]["height"]
    figure = plt.figure(figsize=(width / 72.0, height / 72.0), dpi=72, facecolor=bound["canvas"].get("background", "white"))
    for panel in bound["bound_panels"]:
        left, top, right, bottom = panel["bounds_px"]
        axis = figure.add_axes([left / width, 1.0 - bottom / height, (right - left) / width, (bottom - top) / height])
        for span in panel.get("spans", []):
            axis.axvspan(float(span["x_min"]), float(span["x_max"]), color=span.get("color", "#dddddd"), alpha=float(span.get("alpha", 1.0)), linewidth=0, zorder=float(span.get("zorder", 0)))
        for line in panel.get("reference_lines", []):
            artist = axis.axhline(float(line["y"]), color=line.get("color", "black"), linewidth=float(line.get("line_width", 1)), linestyle=line.get("line_style", "--"), zorder=float(line.get("zorder", 1)))
            if "dashes" in line:
                artist.set_dashes(line["dashes"])
        for series in panel["series"]:
            x_values, y_values = _float_rows(panel["rows"], series["x_column"], series["y_column"])
            axis.plot(
                x_values,
                y_values,
                label=series.get("label"),
                color=series.get("line_color", series.get("color", "#1f77b4")),
                linewidth=float(series.get("line_width", 1.2)),
                linestyle=series.get("line_style", "-"),
                marker=series.get("marker", "o"),
                markersize=float(series.get("marker_size", 5)),
                markerfacecolor=series.get("marker_face_color", series.get("color", series.get("line_color", "#1f77b4"))),
                markeredgecolor=series.get("marker_edge_color", "white"),
                markeredgewidth=float(series.get("marker_edge_width", 0.5)),
                zorder=float(series.get("zorder", 3)),
            )
        _draw_decorations(axis, panel.get("decorations", []))
        _apply_axis_style(axis, panel)
        legend = panel.get("legend")
        if isinstance(legend, dict) and legend.get("show", True):
            axis.legend(
                loc=legend.get("loc", "best"),
                fontsize=float(legend.get("font_size", 10)),
                frameon=bool(legend.get("frame", True)),
                facecolor=legend.get("facecolor", "white"),
                edgecolor=legend.get("edgecolor", "black"),
                framealpha=float(legend.get("frame_alpha", 1.0)),
                borderpad=float(legend.get("border_pad", 0.3)),
                handlelength=float(legend.get("handle_length", 2.0)),
            )
    for item in bound.get("figure_text", []):
        figure.text(
            float(item["x_px"]) / width,
            1.0 - float(item["y_px"]) / height,
            str(item["text"]),
            fontsize=float(item.get("font_size", 12)),
            fontweight=item.get("font_weight", "normal"),
            rotation=float(item.get("rotation", 0)),
            ha=item.get("ha", "left"),
            va=item.get("va", "top"),
            color=item.get("color", "black"),
        )
    return figure


def _patch_svg_size(path: Path, width: int, height: int) -> None:
    text = path.read_text(encoding="utf-8")
    text, count = re.subn(
        r'(<svg[^>]*?)width="[^"]+" height="[^"]+"',
        rf'\1width="{width}px" height="{height}px"',
        text,
        count=1,
    )
    if count != 1:
        raise RuntimeError("could not normalize SVG canvas size")
    path.write_text(text, encoding="utf-8")


def render_spec(spec_path: Path, output_root: Path) -> Path:
    spec_path = spec_path.resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    bound = validate_and_bind_spec(spec, spec_path)
    implementation = Path(__file__).resolve()
    identity = {
        "renderer_version": RENDERER_VERSION,
        "implementation_sha256": file_sha256(implementation),
        "spec_sha256": hashlib.sha256(json.dumps(spec, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest(),
        "data": sorted(
            {str(panel["data_csv_path"]): file_sha256(panel["data_csv_path"]) for panel in bound["bound_panels"]}.items()
        ),
    }
    run_hash = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    output_dir = output_root.resolve() / f"line-recreation-{run_hash[:16]}"
    if output_dir.exists():
        raise FileExistsError(f"immutable recreation directory already exists: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=False)
    figure = build_figure(bound)
    width = bound["canvas"]["width"]
    height = bound["canvas"]["height"]
    png = output_dir / "recreated.png"
    png_3x = output_dir / "recreated-3x.png"
    svg = output_dir / "recreated.svg"
    pdf = output_dir / "recreated.pdf"
    try:
        figure.savefig(png, dpi=72, facecolor=figure.get_facecolor())
        figure.savefig(png_3x, dpi=216, facecolor=figure.get_facecolor())
        figure.savefig(svg, format="svg", facecolor=figure.get_facecolor())
        figure.savefig(pdf, format="pdf", facecolor=figure.get_facecolor())
    finally:
        plt.close(figure)
    _patch_svg_size(svg, width, height)
    with Image.open(png) as image:
        if image.size != (width, height):
            raise RuntimeError(f"renderer produced {image.size}, expected {(width, height)}")
    with Image.open(png_3x) as image:
        if image.size != (width * 3, height * 3):
            raise RuntimeError("3x renderer did not preserve the declared scale")
    manifest = {
        "schema_version": 1,
        "status": "rendered",
        "run_id": output_dir.name,
        "identity": identity,
        "canvas": {"width": width, "height": height, "coordinate_space": "exact_output_pixels"},
        "source_raster_embedded": False,
        "artifacts": {
            "png": "recreated.png",
            "png_3x": "recreated-3x.png",
            "svg": "recreated.svg",
            "pdf": "recreated.pdf",
        },
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()
    output_dir = render_spec(args.spec, args.output_root)
    print(json.dumps({"status": "rendered", "run_id": output_dir.name, "output_dir": str(output_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

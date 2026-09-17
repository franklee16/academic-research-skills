"""Build retained, provenance-first gallery evidence for six Nature figures.

The cases deliberately keep source-mapped values separate from raster-derived
values.  This script is deterministic and only uses the retained official
figure assets/source-data files plus local image processing.
"""

from __future__ import annotations

import csv
import json
import math
import shutil
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from candidate_digitize_bar_chart import extract_bar_chart
from raster_digitizer_core import AxisCalibration, sample_traced_path, trace_colour_path


ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp" / "nature-six"
OUT = ROOT / "gallery" / "assets" / "cases"

# Visible panel order retained from Nature Communications Fig. 6a.  Keep this
# separate from the sparse source worksheet: omission from the sheet must not
# silently shift the position or label of a plotted interaction.
BUBBLE_VISIBLE_ROWS = [
    "Treg_C4_TNFRSF4.DC_C3_LAMP3",
    "Treg_C3_MKI67.DC_C3_LAMP3",
    "Treg_C2_HSPA1A.DC_C3_LAMP3",
    "Treg_C1_SELL.DC_C3_LAMP3",
    "DC_C3_LAMP3.Treg_C4_TNFRSF4",
    "DC_C3_LAMP3.Treg_C3_MKI67",
    "DC_C3_LAMP3.Treg_C2_HSPA1A",
    "DC_C3_LAMP3.Treg_C1_SELL",
]
BUBBLE_VISIBLE_COLUMNS = [
    "ADORA2A_ENTPD1", "BTLA_TNFRSF14", "CD80_CD274", "CTLA4_CD80", "CTLA4_CD86", "LGALS9_HAVCR2", "PDCD1_CD274", "PDCD1_PDCD1LG2", "TNF_FAS",
    "CD27_CD70", "CD28_CD80", "CD28_CD86", "CD40_TNFSF13B", "CD55_ADGRE5", "CD6_ALCAM", "CSF1_SIRPA", "TNF_ICOS", "TNFSF9_TNFRSF9",
    "CCL22_CCR4", "CCR4_CCL17", "CCR6_CCL20", "CCR7_CCL19", "CXCL10_CXCR3", "CXCR3_CCL19", "CXCR3_CXCL9", "CXCR6_CXCL16",
]
BUBBLE_GRID_BOUNDS = (347, 5, 1096, 296)


def _paper_figure(image: Image.Image):
    """Return a raster-sized Matplotlib canvas with a white paper background."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    width, height = image.size
    figure = plt.figure(figsize=(width / 100, height / 100), dpi=100, facecolor="white")
    return figure, plt


def _axes_at(figure, image: Image.Image, bounds: tuple[float, float, float, float]):
    """Add axes using original-raster coordinates (left, top, right, bottom)."""
    width, height = image.size
    left, top, right, bottom = bounds
    return figure.add_axes((left / width, 1 - bottom / height, (right - left) / width, (bottom - top) / height))


def _axis_value(axis: dict, pixel: float) -> float:
    transformed = float(axis["pixel_slope"]) * float(pixel) + float(axis["transformed_intercept"])
    return 10.0**transformed if axis.get("scale") == "log10" else transformed


def _trace_xy(evidence: dict) -> tuple[list[float], list[float]]:
    """Return the full visible path in calibrated data coordinates, preserving gaps."""
    trace = evidence["trace"]
    x_axis, y_axis = evidence["axis_x"], evidence["axis_y"]
    xs, ys = [], []
    for point in trace["path"]:
        if point.get("y_pixel") is None:
            xs.append(math.nan)
            ys.append(math.nan)
            continue
        xs.append(_axis_value(x_axis, point["x_pixel"]))
        ys.append(_axis_value(y_axis, point["y_pixel"]))
    return xs, ys


def _finish_paper_figure(figure, plt, path: Path, image: Image.Image) -> None:
    """Save a data-derived recreation at exactly the original raster dimensions."""
    figure.savefig(path, dpi=100, facecolor="white")
    plt.close(figure)
    with Image.open(path) as rendered:
        if rendered.size != image.size:
            rendered.convert("RGB").resize(image.size, Image.Resampling.LANCZOS).save(path)


def extract_visible_bubble_nodes(image: Image.Image) -> tuple[dict[tuple[str, str], dict], dict]:
    """Recover separable Fig. 6a marker geometry from the retained raster.

    The dot plot has no numeric axes: each categorical grid location can support
    a visible marker, whose centre, solid colour and area are measurable.  Those
    measurements are deliberately kept distinct from Supplementary Data values.
    A coloured component is associated with a grid node only when it is closest
    to that node and remains within 38% of one cell width/height.
    """
    left, top, right, bottom = BUBBLE_GRID_BOUNDS
    pixels = np.asarray(image.convert("RGB"))
    if pixels.shape[1] < right or pixels.shape[0] < bottom:
        raise ValueError("Fig. 6a bubble-grid bounds exceed the retained raster")

    crop = pixels[top:bottom, left:right]
    working = crop.astype(np.int16)
    chroma = working.max(axis=2) - working.min(axis=2)
    # Black dividers/text have near-zero chroma.  A threshold of 12 retains the
    # pale anti-aliased red/blue dots while excluding the white background.
    marker_mask = (chroma > 12) & (working.min(axis=2) < 252)
    visited = np.zeros(marker_mask.shape, dtype=bool)
    components: list[dict] = []
    height, width = marker_mask.shape

    for start_y, start_x in zip(*np.nonzero(marker_mask)):
        if visited[start_y, start_x]:
            continue
        visited[start_y, start_x] = True
        stack = [(int(start_y), int(start_x))]
        coordinates: list[tuple[int, int]] = []
        while stack:
            y, x = stack.pop()
            coordinates.append((y, x))
            for yy in range(max(0, y - 1), min(height, y + 2)):
                for xx in range(max(0, x - 1), min(width, x + 2)):
                    if not visited[yy, xx] and marker_mask[yy, xx]:
                        visited[yy, xx] = True
                        stack.append((yy, xx))

        # All actual dots are at least 32 pixels under this mask.  The cut also
        # removes isolated anti-aliasing specks from labels at the plot edge.
        if len(coordinates) < 6:
            continue
        ys = np.fromiter((point[0] for point in coordinates), dtype=float)
        xs = np.fromiter((point[1] for point in coordinates), dtype=float)
        rgb = np.asarray([crop[y, x] for y, x in coordinates], dtype=np.uint8)
        colours, counts = np.unique(rgb, axis=0, return_counts=True)
        solid_colour = colours[int(np.argmax(counts))]
        components.append(
            {
                "pixel_x": left + float(xs.mean()),
                "pixel_y": top + float(ys.mean()),
                "area_px": len(coordinates),
                "radius_px": math.sqrt(len(coordinates) / math.pi),
                "visible_color": "#{:02x}{:02x}{:02x}".format(*solid_colour.tolist()),
            }
        )

    cell_width = (right - left) / len(BUBBLE_VISIBLE_COLUMNS)
    cell_height = (bottom - top) / len(BUBBLE_VISIBLE_ROWS)
    maximum_distance = min(cell_width, cell_height) * 0.38
    remaining = set(range(len(components)))
    recovered: dict[tuple[str, str], dict] = {}
    missing_cells: list[dict] = []

    for row_index, row_name in enumerate(BUBBLE_VISIBLE_ROWS):
        for column_index, column_name in enumerate(BUBBLE_VISIBLE_COLUMNS):
            expected_x = left + (column_index + 0.5) * cell_width
            expected_y = top + (row_index + 0.5) * cell_height
            if not remaining:
                missing_cells.append({"row": row_name, "column": column_name})
                continue
            component_index = min(
                remaining,
                key=lambda index: (components[index]["pixel_x"] - expected_x) ** 2
                + (components[index]["pixel_y"] - expected_y) ** 2,
            )
            component = components[component_index]
            distance = math.hypot(component["pixel_x"] - expected_x, component["pixel_y"] - expected_y)
            if distance > maximum_distance:
                missing_cells.append({"row": row_name, "column": column_name})
                continue
            remaining.remove(component_index)
            recovered[(row_name, column_name)] = {
                **component,
                "match_distance_px": distance,
                "confidence": max(0.0, 1.0 - distance / maximum_distance),
                "visible_mark": "dot" if component["radius_px"] < 5 else "circle",
            }

    return recovered, {
        "grid_bounds_px": list(BUBBLE_GRID_BOUNDS),
        "grid_shape": [len(BUBBLE_VISIBLE_ROWS), len(BUBBLE_VISIBLE_COLUMNS)],
        "candidate_components": len(components),
        "visible_nodes": len(recovered),
        "unmatched_cells": missing_cells,
        "unassigned_components": len(remaining),
        "colour_mask": {"minimum_chroma": 12, "maximum_minimum_rgb": 251},
        "node_matching": {"maximum_distance_px": maximum_distance, "rule": "nearest categorical-grid centre"},
    }


def _style_axes(axis, *, x_ticks: list[float], y_ticks: list[float], label_size: float = 7) -> None:
    axis.set_xticks(x_ticks)
    axis.set_yticks(y_ticks)
    axis.tick_params(labelsize=label_size, direction="out", length=3, width=0.65, pad=1.5)
    for spine in axis.spines.values():
        spine.set_linewidth(0.7)
        spine.set_color("#222")


def _paper_line_recreation(path: Path, image: Image.Image, case_id: str, report: dict) -> None:
    figure, plt = _paper_figure(image)
    if case_id == "nature-00142-fig3a":
        bounds = (176, 63, 945, 252)
        evidence = report["calibration"]
        axis = _axes_at(figure, image, bounds)
        xs, ys = _trace_xy(evidence)
        axis.plot(xs, ys, color="#111", linewidth=1.4)
        axis.set(xlim=(0, 850), ylim=(0.4, 1.35), xlabel="", ylabel="Signal")
        _style_axes(axis, x_ticks=[0, 200, 400, 600, 800], y_ticks=[0.4, 0.8, 1.2], label_size=8)
        figure.text(0.016, 0.73, "a", fontsize=19, fontweight="bold")
        figure.text(0.53, 0.93, "Mackey-Glass Time-Series", ha="center", fontsize=11)
    elif case_id == "nature-00142-fig4a":
        bounds = (88, 39, 408, 223)
        evidence = report["calibration"]
        axis = _axes_at(figure, image, bounds)
        xs, ys = _trace_xy(evidence)
        axis.plot(xs, ys, color="#111", linewidth=1.4)
        axis.set(xlim=(1973, 1999), ylim=(0.95, 1.55), xlabel="Year", ylabel="Monthly Exchange Rate")
        _style_axes(axis, x_ticks=[1975, 1980, 1985, 1990, 1995, 2000], y_ticks=[1.0, 1.1, 1.2, 1.3, 1.4, 1.5], label_size=7)
        figure.text(0.01, 0.89, "a", fontsize=16, fontweight="bold")
        figure.text(0.58, 0.95, "1973-1999 CAN/US Exchange Rate", ha="center", fontsize=8.5)
    else:
        bounds = (103, 45, 591, 265)
        axis = _axes_at(figure, image, bounds)
        colours = {
            "Bacteria (phylum)": "#8ec3e8",
            "Eukarya (phylum)": "#ed6e6f",
            "Bacteria (OTU)": "#073bb7",
            "Eukarya (OTU)": "#d81919",
        }
        for series, evidence in report["calibration"].items():
            xs, ys = _trace_xy(evidence)
            axis.plot(xs, ys, color=colours[series], linewidth=1.25, marker="+", markersize=3.7, markeredgewidth=0.9)
        axis.set(xlim=(0, 40), ylim=(0.15, 1.0), xlabel="Time lag (Δ days)", ylabel="Similarity")
        _style_axes(axis, x_ticks=[0, 5, 10, 15, 20, 25, 30, 35, 40], y_ticks=[0.2, 0.4, 0.6, 0.8, 1.0], label_size=7)
        axis.text(26.5, 0.87, "Bacteria (phylum)", fontsize=7)
        axis.text(26.5, 0.73, "Eukarya (phylum)", fontsize=7)
        axis.text(26.5, 0.45, "Bacteria (OTU)", fontsize=7)
        axis.text(26.5, 0.27, "Eukarya (OTU)", fontsize=7)
        figure.text(0.035, 0.81, "d", fontsize=16, fontweight="bold")
    _finish_paper_figure(figure, plt, path, image)


def _paper_bar_recreation(path: Path, image: Image.Image, rows: list[dict]) -> None:
    figure, plt = _paper_figure(image)
    axis = _axes_at(figure, image, (108, 14, 588, 518))
    categories = list(dict.fromkeys(row["category"] for row in rows))
    series = list(dict.fromkeys(row["series"] for row in rows))
    colours = {"MViT": "#99c2ff", "CNN-LSTM": "#ffadad", "FGL": "#85d685"}
    positions = np.arange(len(categories), dtype=float)
    width = 0.24
    for index, name in enumerate(series):
        selected = [next(row for row in rows if row["category"] == category and row["series"] == name) for category in categories]
        values = [float(row["value"]) for row in selected]
        offset = (index - (len(series) - 1) / 2) * width
        axis.bar(positions + offset, values, width=width, color=colours[name], label=name, edgecolor="none")
        for position, row, value in zip(positions + offset, selected, values):
            if row.get("error_lower") is None or row.get("error_upper") is None:
                continue
            lower = value - float(row["error_lower"])
            upper = float(row["error_upper"]) - value
            axis.errorbar(position, value, yerr=[[lower], [upper]], color="#222", capsize=2, linewidth=0.7)
    axis.set(xlim=(-0.6, 1.6), ylim=(0, 1), xticks=positions, xticklabels=categories, xlabel="Dataset", ylabel="AUC-ROC")
    _style_axes(axis, x_ticks=list(positions), y_ticks=[0, 0.2, 0.4, 0.6, 0.8, 1], label_size=6.5)
    axis.legend(loc="lower right", fontsize=5.5, frameon=False, handlelength=1.1)
    axis.grid(axis="y", color="#e8e8e8", linewidth=0.5)
    axis.set_axisbelow(True)
    figure.text(0.59, 0.97, "Average", ha="center", fontsize=7)
    figure.text(0.5, 0.02, "(c)", ha="center", fontsize=7)
    _finish_paper_figure(figure, plt, path, image)


def _paper_bubble_recreation(path: Path, image: Image.Image, rows: list[dict]) -> None:
    """Rebuild the visible Fig. 6a grid at the source panel's exact order.

    Raster-extracted marker geometry supplies every separable dot/circle.  The
    workbook supplies numeric mean/P fields only where their pair mapping is
    explicit; it must not be used to fabricate the smaller raster-only marks.
    """
    figure, plt = _paper_figure(image)
    from matplotlib.patches import Rectangle

    # Coordinates and group divisions are measured from the retained panel
    # raster.  Keep the original order instead of alphabetising source rows.
    axis = _axes_at(figure, image, BUBBLE_GRID_BOUNDS)
    names = BUBBLE_VISIBLE_ROWS
    columns = BUBBLE_VISIBLE_COLUMNS
    left, top, right, bottom = BUBBLE_GRID_BOUNDS
    cell_width = (right - left) / len(columns)
    cell_height = (bottom - top) / len(names)
    for row in rows:
        if row.get("visible_marker") != "true":
            continue
        # Matplotlib's marker area is in points squared.  At 100 dpi, this
        # converts the measured raster radius to the same physical diameter.
        radius = float(row["visible_radius_px"])
        area_points = math.pi * (radius * 72 / 100) ** 2
        axis.scatter(
            float(row["pixel_x"]),
            float(row["pixel_y"]),
            s=area_points,
            color=row["visible_color"],
            edgecolors="none",
            linewidths=0,
            zorder=3,
        )
    x_centres = [left + (index + 0.5) * cell_width for index in range(len(columns))]
    y_centres = [top + (index + 0.5) * cell_height for index in range(len(names))]
    axis.set(
        xlim=(left, right),
        ylim=(bottom, top),
        xticks=x_centres,
        yticks=y_centres,
        yticklabels=names,
    )
    axis.set_xticklabels(columns, rotation=90, fontsize=7.5, va="top")
    axis.tick_params(axis="y", labelsize=8.6)
    axis.tick_params(length=0, pad=2)
    axis.axhline(top + 4 * cell_height, color="#222", linewidth=0.8)
    for boundary in (left + 9 * cell_width, left + 18 * cell_width):
        axis.axvline(boundary, color="#222", linewidth=0.7)
    for spine in axis.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color("#222")

    # The source panel also boxes the two cell-type label blocks.  These are
    # categorical structure (not data marks), so reproduce them at their
    # measured raster positions without changing the marker evidence.
    label_left, label_right = 80 / image.width, 340 / image.width
    for block_top, block_bottom in ((5, 146), (154, 296)):
        figure.patches.append(
            Rectangle(
                (label_left, 1 - block_bottom / image.height),
                label_right - label_left,
                (block_bottom - block_top) / image.height,
                transform=figure.transFigure,
                fill=False,
                edgecolor="#222",
                linewidth=0.8,
                zorder=2,
            )
        )

    # The coloured strips are part of the panel's semantic grouping, not a
    # decorative approximation.  They sit behind the vertically set labels.
    group_specs = (
        (0, 9, "#e7f5ec", "#10944a", "Immune-suppressive molecules"),
        (9, 18, "#fee0dc", "#f02b52", "Co-stimulatory molecules"),
        (18, 26, "#fee9cf", "#f37d16", "Chemokines"),
    )
    plot_left, plot_right = left / image.width, right / image.width
    bottom_height = (image.height - 304) / image.height
    for start, end, background, text_colour, label in group_specs:
        x0 = plot_left + (plot_right - plot_left) * start / len(columns)
        width = (plot_right - plot_left) * (end - start) / len(columns)
        figure.patches.append(Rectangle((x0, 0), width, bottom_height, transform=figure.transFigure, facecolor=background, edgecolor="none", zorder=-1))
        figure.text(x0 + width / 2, 0.016, label, ha="center", va="bottom", fontsize=9.5, color=text_colour)
    figure.text(0.017, 0.895, "a", fontsize=18, fontweight="bold")
    _finish_paper_figure(figure, plt, path, image)


def _paper_upset_recreation(path: Path, image: Image.Image, rows: list[dict]) -> None:
    """Recreate Fig. 2b in the source panel's measured raster layout."""
    figure, plt = _paper_figure(image)
    rows = sorted(rows, key=lambda row: int(row["intersection"]))
    # These panel edges and the intersection centres were measured on the
    # retained 1200 x 645 raster, rather than laid out as a generic UpSet plot.
    top = _axes_at(figure, image, (157, 24, 1105, 500))
    matrix = _axes_at(figure, image, (157, 503, 1105, 609))
    inset = _axes_at(figure, image, (836, 69, 1093, 264))
    indices = np.arange(len(rows))
    counts = [int(row["count"]) for row in rows]
    top.bar(indices, counts, color="#444", width=0.62)
    top.set(xlim=(-1, len(rows)), ylim=(0, 2150), xticks=[], yticks=[0, 500, 1000, 1500, 2000])
    top.set_ylabel("Intersection Size", fontsize=16, labelpad=24)
    top.tick_params(labelsize=13, length=4, width=1)
    top.spines[["top", "right"]].set_visible(False)
    top.spines["left"].set_linewidth(1.2)
    top.spines["bottom"].set_linewidth(1.2)
    for index, value in enumerate(counts):
        top.text(index, value + 42, str(value), ha="center", va="bottom", fontsize=10, color="#4b4b4b")

    # The source's row order is intentionally non-numeric.  Keep it both for
    # labels and membership links; changing to FunC-1..4 changes the graph.
    matrix_keys = ["FunC_2", "FunC_4", "FunC_3", "FunC_1"]
    matrix_names = ["FunC-2", "FunC-4", "FunC-3", "FunC-1"]
    matrix.set(xlim=(-1, len(rows)), ylim=(3.5, -0.5), yticks=range(4), yticklabels=matrix_names, xticks=[])
    matrix.axhspan(0.5, 1.5, color="#fafafa", zorder=0)
    matrix.axhspan(2.5, 3.5, color="#f5f5f5", zorder=0)
    matrix.tick_params(labelsize=13, length=0, pad=10)
    matrix.spines[["top", "left", "right"]].set_visible(False)
    matrix.spines["bottom"].set_linewidth(1.2)
    for index, row in enumerate(rows):
        active = [int(row[key]) == 1 for key in matrix_keys]
        locations = [position for position, value in enumerate(active) if value]
        if len(locations) > 1:
            matrix.plot([index, index], [min(locations), max(locations)], color="#444", linewidth=1.2, zorder=1)
        matrix.scatter([index] * 4, range(4), s=[46 if value else 30 for value in active], color=["#3f3f3f" if value else "#e5e5e5" for value in active], edgecolors="none", zorder=2)

    inset_specs = [
        ("FunC_4", "FunC-4", "#984ea3"),
        ("FunC_3", "FunC-3", "#4daf4a"),
        ("FunC_2", "FunC-2", "#377eb8"),
        ("FunC_1", "FunC-1", "#e41a1c"),
    ]
    totals = [sum(int(row["count"]) * int(row[key]) for row in rows) for key, _, _ in inset_specs]
    inset.barh(range(4), totals, color=[colour for _, _, colour in inset_specs], height=0.9)
    inset.set(xlim=(0, 4300), xticks=[0, 1000, 2000, 3000, 4000], yticks=range(4), yticklabels=[label for _, label, _ in inset_specs], xlabel="Sum of unique KO annotations")
    inset.tick_params(labelsize=13, length=3, width=1, pad=4)
    inset.set_xlabel("Sum of unique KO annotations", fontsize=14, labelpad=8)
    inset.spines[["top", "right"]].set_visible(False)
    inset.spines["left"].set_linewidth(1.1)
    inset.spines["bottom"].set_linewidth(1.1)
    inset.invert_yaxis()
    figure.text(0.027, 0.93, "b", fontsize=16, fontweight="bold")
    _finish_paper_figure(figure, plt, path, image)


def save_paper_static_recreation(path: Path, image: Image.Image, case_id: str, rows: list[dict], report: dict) -> bool:
    """Render the six paper cases from retained visible data and source layout."""
    if case_id in {"nature-00142-fig3a", "nature-00142-fig4a", "nature-02571-fig1d"}:
        _paper_line_recreation(path, image, case_id, report)
    elif case_id == "nature-63786-fig1c":
        _paper_bar_recreation(path, image, rows)
    elif case_id == "nature-21043-fig6a":
        _paper_bubble_recreation(path, image, rows)
    elif case_id == "nature-19006-fig2b":
        _paper_upset_recreation(path, image, rows)
    else:
        return False
    return True


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload.setdefault("schema_version", 1)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def copy_crop(source: Path, target: Path, box: tuple[int, int, int, int]) -> Image.Image:
    image = Image.open(source).convert("RGB")
    crop = image.crop(box)
    target.parent.mkdir(parents=True, exist_ok=True)
    crop.save(target)
    return crop


def save_static_recreation(
    path: Path,
    image: Image.Image,
    mode: str,
    rows: list[dict],
    report: dict | None = None,
    pixel_origin: tuple[int, int] = (0, 0),
) -> None:
    """Make a lightweight, reviewable recreation; interactive SVG is rendered in home.js."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if mode == "source-image":
        image.save(path)
        return
    width, height = image.size
    out = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(out)
    if mode == "line":
        groups = {}
        for row in rows:
            if row.get("value") is not None:
                groups.setdefault(row["series"], []).append(row)
        visible_rows = [row for points in groups.values() for row in points]
        colors = {"Mackey-Glass": "#151515", "CAN/USD": "#151515", "Bacteria (phylum)": "#8ec3e8", "Eukarya (phylum)": "#ed6e6f", "Bacteria (OTU)": "#073bb7", "Eukarya (OTU)": "#d81919"}
        left, right, top, bottom = 80, width - 32, 50, height - 48
        if not visible_rows:
            image.save(path)
            return
        x_origin, y_origin = pixel_origin
        # If the extractor retained original pixel coordinates, use those
        # coordinates directly.  This avoids a second, lossy rescaling in the
        # review image and keeps the recreation aligned to the source raster.
        use_pixels = all(r.get("pixel_x") is not None and r.get("pixel_y") is not None for r in visible_rows)
        if use_pixels:
            anchors_x = ((report or {}).get("calibration") or {}).get("axis_x", {}).get("anchors", [])
            anchors_y = ((report or {}).get("calibration") or {}).get("axis_y", {}).get("anchors", [])
            left = min((float(a["pixel"]) for a in anchors_x), default=80.0) - x_origin
            right = max((float(a["pixel"]) for a in anchors_x), default=width - 32.0) - x_origin
            top = min((float(a["pixel"]) for a in anchors_y), default=50.0) - y_origin
            bottom = max((float(a["pixel"]) for a in anchors_y), default=height - 48.0) - y_origin
        else:
            xmin = min(float(r["x"]) for r in visible_rows)
            xmax = max(float(r["x"]) for r in visible_rows)
            ymin = min(float(r["value"]) for r in visible_rows)
            ymax = max(float(r["value"]) for r in visible_rows)
            left, right, top, bottom = 80, width - 32, 50, height - 48
        for key, points in groups.items():
            points = sorted(points, key=lambda r: float(r["x"]))
            xy = []
            for row in points:
                if use_pixels:
                    x = float(row["pixel_x"]) - x_origin
                    y = float(row["pixel_y"]) - y_origin
                else:
                    x = left + (float(row["x"]) - xmin) / max(1e-9, xmax - xmin) * (right - left)
                    y = bottom - (float(row["value"]) - ymin) / max(1e-9, ymax - ymin) * (bottom - top)
                xy.append((x, y))
            draw.line(xy, fill=colors.get(key, "#111"), width=3)
        draw.rectangle((left, top, right, bottom), outline="#202020", width=1)
    elif mode == "bars":
        groups = list(dict.fromkeys(r["category"] for r in rows))
        series = list(dict.fromkeys(r["series"] for r in rows))
        colors = {"MViT": "#99c2ff", "CNN-LSTM": "#ffadad", "FGL": "#85d685"}
        left, right, top, bottom = 80, width - 26, 18, height - 54
        ymax = 1.0
        slot = (right - left) / max(1, len(groups))
        bw = slot / (len(series) + 1)
        for i, category in enumerate(groups):
            for j, method in enumerate(series):
                row = next(r for r in rows if r["category"] == category and r["series"] == method)
                value = float(row["value"])
                x0 = left + i * slot + (j + 0.5) * bw
                y0 = bottom - value / ymax * (bottom - top)
                draw.rectangle((x0, y0, x0 + bw * 0.82, bottom), fill=colors.get(method, "#777"))
        draw.rectangle((left, top, right, bottom), outline="#202020", width=1)
    elif mode == "upset":
        groups = sorted(rows, key=lambda r: -int(r["count"]))
        left, right, top, bottom = 40, width - 20, 30, height - 32
        baseline = bottom - 80
        max_count = max(int(r["count"]) for r in groups)
        slot = (right - left) / max(1, len(groups))
        for i, row in enumerate(groups):
            count = int(row["count"])
            x = left + (i + 0.2) * slot
            y = baseline - count / max_count * (baseline - top)
            draw.rectangle((x, y, x + slot * 0.58, baseline), fill="#444")
        draw.rectangle((left, top, right, baseline), outline="#202020", width=1)
    elif mode == "bubble":
        rows_unique = list(dict.fromkeys(r["row"] for r in rows))
        cols_unique = list(dict.fromkeys(r["column"] for r in rows))
        left, right, top, bottom = 125, width - 130, 28, height - 40
        max_size = max(float(r["size"]) for r in rows) or 1
        for row in rows:
            x = left + cols_unique.index(row["column"]) / max(1, len(cols_unique) - 1) * (right - left)
            y = top + rows_unique.index(row["row"]) / max(1, len(rows_unique) - 1) * (bottom - top)
            size = 2 + 13 * float(row["size"]) / max_size
            value = float(row["mean"])
            t = max(0.0, min(1.0, value / 1.4))
            color = (int(215 * t + 40), int(120 * (1 - t) + 75), int(180 * (1 - t) + 160))
            draw.ellipse((x - size, y - size, x + size, y + size), fill=color, outline="#555")
        draw.rectangle((left, top, right, bottom), outline="#202020", width=1)
    out.save(path)


def save_evidence_overlay(
    path: Path,
    image: Image.Image,
    mode: str,
    rows: list[dict],
    report: dict,
    pixel_origin: tuple[int, int] = (0, 0),
) -> None:
    """Draw only measured geometry on the retained raster for human review."""
    overlay = image.convert("RGB").copy()
    draw = ImageDraw.Draw(overlay)
    if mode == "line":
        colours = {
            "Mackey-Glass": "#ff8c00",
            "CAN/USD": "#ff8c00",
            "Bacteria (phylum)": "#005f9e",
            "Eukarya (phylum)": "#b22222",
            "Bacteria (OTU)": "#003399",
            "Eukarya (OTU)": "#990000",
        }
        for row in rows:
            if row.get("pixel_y") is None:
                continue
            x, y = float(row["pixel_x"]) - pixel_origin[0], float(row["pixel_y"]) - pixel_origin[1]
            colour = colours.get(row.get("series"), "#ff8c00")
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), outline=colour, width=1)
    elif mode == "bars":
        for mark in report.get("marks", []):
            if mark.get("status") != "extracted":
                continue
            component = mark.get("component", {})
            left = component.get("left_pixel")
            right = component.get("right_pixel")
            end = mark.get("end_pixel")
            if left is None or right is None or end is None:
                continue
            colour = "#d97706" if mark.get("baseline_status") == "occluded_by_overlay" else "#111111"
            draw.line((left, end, right, end), fill=colour, width=2)
    elif mode == "bubble":
        for row in rows:
            if row.get("visible_marker") != "true":
                continue
            x, y = float(row["pixel_x"]), float(row["pixel_y"])
            radius = float(row["visible_radius_px"]) + 1.5
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline="#f59e0b", width=1)
    overlay.save(path)


def sample_traced_line(
    image: Image.Image,
    roi: tuple[int, int, int, int],
    x_values: list[float],
    x_domain: tuple[float, float],
    y_domain: tuple[float, float],
    series: str,
    target: tuple[int, int, int],
    *,
    sigma: float = 42.0,
    score_threshold: float = 0.22,
) -> tuple[list[dict], dict]:
    """Trace a curve across all raster columns, then sample requested x values."""

    pixels = np.asarray(image.convert("RGB"))
    x0, y0, x1, y1 = roi
    x_axis = AxisCalibration.fit([(x0, x_domain[0]), (x1, x_domain[1])])
    y_axis = AxisCalibration.fit([(y0, y_domain[1]), (y1, y_domain[0])])
    trace = trace_colour_path(
        pixels,
        target=target,
        plot_bounds=roi,
        sigma=sigma,
        tolerance=96.0,
        score_threshold=score_threshold,
        edge_margin=3,
        smoothness=0.08,
        gap_penalty=0.75,
        max_step=16.0,
    )
    sampled = sample_traced_path(trace, x_values=x_values, x_axis=x_axis, y_axis=y_axis, sample_radius_px=3)
    rows = []
    for item in sampled:
        rows.append(
            {
                "series": series,
                "x": item["x"],
                "value": item["y"],
                "pixel_x": item["x_pixel"],
                "pixel_y": item["y_pixel"],
                "uncertainty_px": item.get("uncertainty_px"),
                "uncertainty_value": item.get("uncertainty_value"),
                "confidence": item.get("confidence", 0.0),
                "value_status": item["status"],
            }
        )
    return rows, {"axis_x": x_axis.report(), "axis_y": y_axis.report(), "trace": trace}


def make_case(case_id: str, source_name: str, crop: tuple[int, int, int, int], mode: str, rows: list[dict], report: dict) -> None:
    directory = OUT / case_id
    directory.mkdir(parents=True, exist_ok=True)
    original = copy_crop(TMP / source_name, directory / "original.png", crop)
    pixel_origin = crop[:2] if mode == "line" else (0, 0)
    recreated_path = directory / "recreated.png"
    if not save_paper_static_recreation(recreated_path, original, case_id, rows, report):
        save_static_recreation(recreated_path, original, mode, rows, report, pixel_origin)
    save_evidence_overlay(directory / "overlay.png", original, mode, rows, report, pixel_origin)
    write_csv(directory / "data.csv", rows)
    write_json(directory / "report.json", report)


def build_bubble() -> None:
    import openpyxl

    wb = openpyxl.load_workbook(TMP / "21043-sd8.xlsx", read_only=True, data_only=True)
    ws = wb["SD 6-1"]
    source_image = Image.open(TMP / "nature-21043-fig6.png").convert("RGB")
    visible_nodes, pixel_evidence = extract_visible_bubble_nodes(source_image)
    rows = []
    selected: dict[tuple[str, str], tuple[float, float]] = {}
    for values in ws.iter_rows(min_row=4, values_only=True):
        interaction, cell_types, p_value, mean = values[:4]
        if not cell_types or not interaction:
            continue
        pair = str(cell_types)
        name = str(interaction)
        if pair in BUBBLE_VISIBLE_ROWS and name in BUBBLE_VISIBLE_COLUMNS:
            selected[(pair, name)] = (float(p_value or 0), float(mean or 0))
    for row_name in BUBBLE_VISIBLE_ROWS:
        for column_name in BUBBLE_VISIBLE_COLUMNS:
            key = (row_name, column_name)
            source_value = selected.get(key)
            visible = visible_nodes.get(key)
            # Preserve the one source pair whose coloured marker is not
            # separable in this raster.  It belongs in the auditable table but
            # is never drawn as a fabricated circle.
            if visible is None and source_value is None:
                continue
            record = {"row": row_name, "column": column_name}
            if source_value is not None:
                p_value, mean = source_value
                record.update(
                    {
                        "mean": f"{mean:.6g}",
                        "p_value": f"{p_value:.6g}",
                        "source_size_proxy": f"{min(2.0, -math.log10(max(p_value, 1e-6)) / 4):.6g}",
                        "source_status": "official_source_mapped",
                    }
                )
            else:
                record.update({"mean": "", "p_value": "", "source_size_proxy": "", "source_status": "not_supplied_for_pair"})
            if visible is not None:
                record.update(
                    {
                        "pixel_x": f"{visible['pixel_x']:.3f}",
                        "pixel_y": f"{visible['pixel_y']:.3f}",
                        "visible_radius_px": f"{visible['radius_px']:.3f}",
                        "visible_color": visible["visible_color"],
                        "visible_mark": visible["visible_mark"],
                        "visible_marker": "true",
                        "pixel_match_distance": f"{visible['match_distance_px']:.3f}",
                        "confidence": f"{visible['confidence']:.3f}",
                        "visible_geometry_status": "raster_detected_marker",
                        "value_status": "official_source_mapped_and_visible" if source_value is not None else "visible_geometry_extracted",
                    }
                )
            else:
                record.update(
                    {
                        "pixel_x": "",
                        "pixel_y": "",
                        "visible_radius_px": "",
                        "visible_color": "",
                        "visible_mark": "not_visible",
                        "visible_marker": "false",
                        "pixel_match_distance": "",
                        "confidence": "",
                        "visible_geometry_status": "no_separable_marker_in_raster",
                        "value_status": "official_source_not_visible_in_raster",
                    }
                )
            rows.append(record)
    source_visible = sum(row["source_status"] == "official_source_mapped" and row["visible_marker"] == "true" for row in rows)
    source_only = sum(row["source_status"] == "official_source_mapped" and row["visible_marker"] == "false" for row in rows)
    raster_only = sum(row["source_status"] == "not_supplied_for_pair" and row["visible_marker"] == "true" for row in rows)
    report = {
        "status": "partial_visible_with_source_mapping",
        "route": "candidate_raster_bubble_matrix_with_source_mapping",
        "source_file": "Supplementary Data 6-1",
        "panel_mapping": "Fig. 6a rows/columns follow the retained panel raster. Source mean/P fields are retained only for exact pair names; marker colour, centre and radius are measured from the raster.",
        "rows": len(rows),
        "pixel_extraction": pixel_evidence,
        "coverage": {
            "categorical_grid_slots": len(BUBBLE_VISIBLE_ROWS) * len(BUBBLE_VISIBLE_COLUMNS),
            "visible_raster_markers": sum(row["visible_marker"] == "true" for row in rows),
            "source_pairs_total": len(selected),
            "source_pairs_with_visible_marker": source_visible,
            "source_pairs_without_separable_marker": source_only,
            "raster_only_visible_markers": raster_only,
        },
        "limitations": [
            "The 207 separable raster markers support only their visible centre, colour and radius. Raster-only markers do not receive inferred significance means or P values.",
            "One official source pair has no separable coloured marker under the retained raster evidence and is retained in the table without a drawn mark.",
            "This is a candidate categorical bubble-matrix route. The locally verified geometry improves the recreation but does not recover hidden source observations.",
        ],
    }
    make_case("nature-21043-fig6a", "nature-21043-fig6.png", (0, 0, 1120, 480), "bubble", rows, report)


def build_upset() -> None:
    """Rebuild Fig. 2b through the canonical original-pixel UpSet audit."""

    try:
        from build_upset_gallery_cases import build_case_19006
    except ImportError:  # pragma: no cover - package-style invocation
        from .build_upset_gallery_cases import build_case_19006

    build_case_19006()


def build_lines() -> None:
    image = Image.open(TMP / "nature-00142-fig3.png").convert("RGB")
    x_values = list(range(0, 851, 25))
    rows, evidence = sample_traced_line(image, (176, 63, 945, 252), x_values, (0, 850), (0.4, 1.35), "Mackey-Glass", (20, 20, 20))
    report = {"status": "visible_geometry_candidate", "route": "calibrated_raster_candidate", "panel_mapping": "Fig. 3a Mackey-Glass training time series", "rows": len(rows), "pixel_extraction": "black-line sampling after verified plot ROI", "source_data": "not available on the article page", "limitations": ["Values are visible-curve candidates sampled from the raster; they are not the hidden time-series records."]}
    report["calibration"] = evidence
    report["observed_rows"] = sum(row.get("value") is not None for row in rows)
    make_case("nature-00142-fig3a", "nature-00142-fig3.png", (0, 0, 1000, 315), "line", rows, report)

    image = Image.open(TMP / "nature-00142-fig4.png").convert("RGB")
    x_values = list(range(1973, 2000))
    rows, evidence = sample_traced_line(image, (88, 39, 408, 223), x_values, (1973, 1999), (0.95, 1.55), "CAN/USD", (20, 20, 20))
    report = {"status": "visible_geometry_candidate", "route": "calibrated_raster_candidate", "panel_mapping": "Fig. 4a monthly U.S.–Canada exchange rate", "rows": len(rows), "pixel_extraction": "black-line sampling after verified plot ROI", "source_data": "not available on the article page", "limitations": ["Values are downsampled visible-curve candidates; monthly observations and log transformations are not inferred beyond plotted geometry."]}
    report["calibration"] = evidence
    report["observed_rows"] = sum(row.get("value") is not None for row in rows)
    make_case("nature-00142-fig4a", "nature-00142-fig4.png", (0, 0, 430, 280), "line", rows, report)


def build_similarity() -> None:
    image = Image.open(TMP / "nature-02571-fig1.jpg").convert("RGB")
    x_values = list(range(0, 41, 2))
    rows: list[dict] = []
    trace_evidence = {}
    colors = {"Bacteria (phylum)": (130, 192, 229), "Eukarya (phylum)": (231, 105, 105), "Bacteria (OTU)": (15, 59, 183), "Eukarya (OTU)": (210, 22, 22)}
    for series, color in colors.items():
        sampled, evidence = sample_traced_line(image, (703, 605, 1191, 825), x_values, (0, 40), (0.18, 1.0), series, color, sigma=48.0, score_threshold=0.18)
        rows.extend(sampled)
        trace_evidence[series] = evidence
    report = {"status": "visible_geometry_candidate", "route": "calibrated_raster_candidate", "panel_mapping": "Fig. 1d similarity vs. time lag", "rows": len(rows), "pixel_extraction": "four colour-line sampling after verified plot ROI", "source_data": "not directly provided for this panel", "limitations": ["Error bars are not extracted in this demo; each row is a visible line candidate, not an inferred replicate summary."]}
    report["calibration"] = trace_evidence
    report["observed_rows"] = sum(row.get("value") is not None for row in rows)
    make_case("nature-02571-fig1d", "nature-02571-fig1.jpg", (600, 560, 1200, 896), "line", rows, report)


def build_grouped_bars() -> None:
    # The panel is intentionally extracted from the retained raster rather than
    # copied from a hand-entered table.  The calibrated baseline is the y=0
    # axis, while the three exact fill colours are measured from the image.
    panel = TMP / "fig1c-panel.png"
    if not panel.exists():
        copy_crop(TMP / "nature-63786-fig1.png", panel, (590, 0, 1200, 590))
    extractor = extract_bar_chart(
        panel,
        plot_bounds=(108, 14, 588, 518),
        value_axis=(518.0, 0.0, 14.0, 1.0),
        orientation="vertical",
        layout="grouped",
        series_colors={"MViT": "#99c2ff", "CNN-LSTM": "#ffadad", "FGL": "#85d685"},
        categories=[("CHBMIT", 229.0), ("AES", 490.0)],
        tolerance=30.0,
        min_area=200,
        min_bar_thickness=8,
        min_bar_length=10,
        baseline_tolerance_px=4.0,
        bridge_gap=2,
        value_gap=3,
        prefer_baseline_connected=True,
        error_color="#000000",
        error_tolerance=80.0,
        error_search_radius=8,
        error_min_span=3,
    )
    rows = []
    for mark in extractor["marks"]:
        row = {
            "category": mark["category"],
            "series": mark["series"],
            "value": mark.get("value"),
            "pixel_start": mark.get("start_pixel"),
            "pixel_end": mark.get("end_pixel"),
            "confidence": mark.get("confidence", 0.0),
            "value_status": (
                "visible_geometry_occluded_by_overlay"
                if mark.get("baseline_status") == "occluded_by_overlay"
                else "visible_geometry_observed"
                if mark.get("status") == "extracted"
                else "not_extracted"
            ),
        }
        error_bar = mark.get("error_bar") or {}
        if row["value"] is not None:
            if error_bar.get("status") == "extracted":
                row["error_lower"] = error_bar["lower_value"]
                row["error_upper"] = error_bar["upper_value"]
                row["error_lower_pixel"] = error_bar["lower_pixel"]
                row["error_upper_pixel"] = error_bar["upper_pixel"]
                row["error_confidence"] = error_bar.get("confidence", 0.0)
                row["error_status"] = "visible_interval_observed"
            else:
                row["error_status"] = "not_extracted_needs_manual_review"
        rows.append(row)
    report = {
        "status": extractor["status"],
        "route": "calibrated_raster_candidate",
        "panel_mapping": "Fig. 1c dataset averages; three methods and visible variance bars",
        "rows": len(rows),
        "pixel_extraction": "colour-mask bar endpoints with value-axis calibration, baseline-connected legend suppression and occlusion diagnostics",
        "source_data": "not linked on the article page",
        "extractor_summary": extractor["summary"],
        "marks": extractor["marks"],
        "limitations": [
            "The article page exposes supplementary information but no panel-level source workbook; values are display-level candidates and must not be presented as author raw data.",
            "Only dark error intervals that bracket a bar endpoint are emitted; short, occluded or axis-confounded intervals remain not_extracted.",
        ],
    }
    make_case("nature-63786-fig1c", "nature-63786-fig1.png", (590, 0, 1200, 590), "bars", rows, report)


def main() -> None:
    build_bubble()
    build_upset()
    build_lines()
    build_similarity()
    build_grouped_bars()
    print("built", ", ".join(sorted(p.name for p in OUT.glob("nature-*-fig*"))))


if __name__ == "__main__":
    main()

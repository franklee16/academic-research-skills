"""Generate local chart fixtures and compare calibrated reverse-extraction methods.

No user data, models, network calls, or OCR services are used. The output folder
contains the synthetic images, complete ground truth, and the method comparison.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict, deque
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

from raster_digitizer_core import AxisCalibration, sample_traced_path, trace_colour_path


C = {"red": "#d62728", "gray": "#7f7f7f", "blue": "#1f77b4", "green": "#2ca02c", "error": "#d0d0d0"}


def rgb(color: str) -> np.ndarray:
    color = color.lstrip("#")
    return np.array([int(color[i : i + 2], 16) for i in range(0, 6, 2)], dtype=np.int32)


def make_ax(title: str, xlim: tuple[float, float], ylim: tuple[float, float]):
    fig = plt.figure(figsize=(6, 4), dpi=100, facecolor="white")
    # Reserve a right margin for legends so geometric extraction is evaluated
    # on the plot region, not on legend swatches.
    ax = fig.add_axes([0.13, 0.16, 0.66, 0.73])
    ax.set(title=title, xlim=xlim, ylim=ylim)
    ax.grid(axis="y", color="#e6e6e6", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=8)
    return fig, ax


def save_figure(fig, ax, path: Path, xlim, ylim) -> dict:
    fig.canvas.draw()
    width, height = fig.canvas.get_width_height()
    left, bottom = ax.transData.transform((xlim[0], ylim[0]))
    right, top = ax.transData.transform((xlim[1], ylim[1]))
    fig.savefig(path, dpi=100, facecolor="white")
    plt.close(fig)
    return {
        "image": path.name,
        "size": [width, height],
        "bounds": {"left": float(left), "top": float(height - top), "right": float(right), "bottom": float(height - bottom)},
        "xlim": list(xlim),
        "ylim": list(ylim),
    }


def resize_meta(meta: dict, source: Path, target: Path, size: tuple[int, int]) -> dict:
    original = Image.open(source).convert("RGB")
    sx, sy = size[0] / original.width, size[1] / original.height
    original.resize(size, Image.Resampling.LANCZOS).save(target, quality=86)
    result = {**meta, "image": target.name, "size": list(size), "bounds": dict(meta["bounds"])}
    for key in ("left", "right"):
        result["bounds"][key] *= sx
    for key in ("top", "bottom"):
        result["bounds"][key] *= sy
    return result


def bounds(meta: dict) -> tuple[int, int, int, int]:
    b = meta["bounds"]
    return round(b["left"]), round(b["top"]), round(b["right"]), round(b["bottom"])


def x_pixel(value: float, meta: dict) -> float:
    b = meta["bounds"]
    lo, hi = meta["xlim"]
    return b["left"] + (value - lo) * (b["right"] - b["left"]) / (hi - lo)


def x_value(pixel: float, meta: dict) -> float:
    b = meta["bounds"]
    lo, hi = meta["xlim"]
    return lo + (pixel - b["left"]) * (hi - lo) / (b["right"] - b["left"])


def y_value(pixel: float, meta: dict) -> float:
    b = meta["bounds"]
    lo, hi = meta["ylim"]
    return hi + (pixel - b["top"]) * (lo - hi) / (b["bottom"] - b["top"])


def y_span(meta: dict) -> float:
    return abs(meta["ylim"][1] - meta["ylim"][0])


def mask(image: np.ndarray, color: str, tolerance: float = 80.0) -> np.ndarray:
    diff = image.astype(np.int32) - rgb(color)
    return np.square(diff).sum(axis=2) <= tolerance * tolerance


def nearby_rows(colormask: np.ndarray, x: float, meta: dict, radius: int) -> np.ndarray:
    left, top, right, bottom = bounds(meta)
    x0, x1 = max(left, round(x) - radius), min(right, round(x) + radius)
    rows, _ = np.where(colormask[top : bottom + 1, x0 : x1 + 1])
    return rows + top


def clusters(rows: np.ndarray) -> list[tuple[float, int]]:
    if not len(rows):
        return []
    unique = np.unique(np.sort(rows))
    pieces = np.split(unique, np.where(np.diff(unique) > 3)[0] + 1)
    return [(float(np.median(rows[np.isin(rows, piece)])), int(np.isin(rows, piece).sum())) for piece in pieces]


def line_column(colormask: np.ndarray, xs: list[float], meta: dict) -> list[float | None]:
    output = []
    for x in xs:
        rows = nearby_rows(colormask, x, meta, 0)
        output.append(None if not len(rows) else y_value(float(np.median(rows)), meta))
    return output


def line_trace(colormask: np.ndarray, xs: list[float], meta: dict) -> list[float | None]:
    output, previous = [], None
    for x in xs:
        options = clusters(nearby_rows(colormask, x, meta, 3))
        if not options:
            output.append(None)
            continue
        choice = max(options, key=lambda row: row[1]) if previous is None else min(options, key=lambda row: abs(row[0] - previous) - 0.35 * row[1])
        previous = choice[0]
        output.append(y_value(choice[0], meta))
    return output


def raster_core_trace(image: np.ndarray, color: str, xs: list[float], meta: dict) -> list[float | None]:
    """Run the shared soft-colour/continuity candidate on a held-out fixture."""
    b = meta["bounds"]
    plot_bounds = bounds(meta)
    x_axis = AxisCalibration.fit([(b["left"], meta["xlim"][0]), (b["right"], meta["xlim"][1])])
    y_axis = AxisCalibration.fit([(b["top"], meta["ylim"][1]), (b["bottom"], meta["ylim"][0])])
    trace = trace_colour_path(
        image,
        target=tuple(int(color.lstrip("#")[index : index + 2], 16) for index in (0, 2, 4)),
        plot_bounds=plot_bounds,
        sigma=42.0,
        tolerance=80.0,
        score_threshold=0.22,
        max_step=18.0,
    )
    sampled = sample_traced_path(trace, x_values=xs, x_axis=x_axis, y_axis=y_axis, sample_radius_px=3)
    return [item["y"] for item in sampled]


def components(colormask: np.ndarray, meta: dict, min_area: int = 5) -> list[np.ndarray]:
    left, top, right, bottom = bounds(meta)
    view = colormask[top : bottom + 1, left : right + 1]
    seen = np.zeros_like(view, dtype=bool)
    result = []
    height, width = view.shape
    for start_y, start_x in zip(*np.where(view)):
        if seen[start_y, start_x]:
            continue
        queue = deque([(int(start_y), int(start_x))])
        seen[start_y, start_x] = True
        group = []
        while queue:
            y, x = queue.popleft()
            group.append((y + top, x + left))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < height and 0 <= xx < width and view[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = True
                        queue.append((yy, xx))
        if len(group) >= min_area:
            result.append(np.asarray(group, dtype=float))
    return result


def scalar_metric(predicted: list[float | None], truth: list[float], scale: float) -> dict:
    errors = [abs(value - target) for value, target in zip(predicted, truth) if value is not None]
    coverage = len(errors) / len(truth)
    mae = float(np.mean(errors)) if errors else float("inf")
    return {"mae": mae, "coverage": coverage, "normalized_score": mae / scale + 1 - coverage, "count": len(errors)}


def point_metric(predicted: list[tuple[float, float]], truth: list[tuple[float, float]], scale: float) -> dict:
    pairs = list(zip(sorted(predicted), sorted(truth)))
    errors = [(abs(x - tx) + abs(y - ty)) / 2 for (x, y), (tx, ty) in pairs]
    coverage = len(pairs) / len(truth)
    mae = float(np.mean(errors)) if errors else float("inf")
    return {"mae": mae, "coverage": coverage, "normalized_score": mae / scale + 1 - coverage, "count": len(errors)}


def render_line(fixtures: Path):
    x = np.arange(11, dtype=float)
    values = {
        "red": [26, 10, 9, 6, 8, 10, 14, 8, 6, 18, 10],
        "gray": [27, 13, 12, 14, 19, 20, 28, 35, 32, 28, 21],
        "blue": [40, 33, 25, 32, 35, 30, 43, 44, 37, 37, 40],
    }
    fig, ax = make_ax("Synthetic line chart", (-0.3, 10.3), (0, 70))
    ax.errorbar(x, values["gray"], yerr=[16, 8, 8, 9, 12, 12, 15, 18, 15, 14, 11], color=C["gray"], ecolor=C["error"], marker="o", linewidth=1.2, capsize=3, label="context")
    ax.plot(x, values["red"], color=C["red"], marker="s", linewidth=1.2, label="biodiversity")
    ax.plot(x, values["blue"], color=C["blue"], marker="^", linestyle="--", linewidth=1.2, label="economic language")
    ax.set(xlabel="Year", ylabel="% of releases")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=7, frameon=False)
    source = fixtures / "line_clean.png"
    clean = save_figure(fig, ax, source, (-0.3, 10.3), (0, 70))
    clean["name"] = "line_clean"
    lowres = resize_meta(clean, source, fixtures / "line_lowres.jpg", (376, 263))
    lowres["name"] = "line_lowres_jpeg"
    # Benchmark the plotted observations. Sampling arbitrary positions on a
    # dashed raster would test interpolation through intentionally blank gaps,
    # not chart digitization of the displayed data points.
    samples = x.tolist()
    truth = {name: list(ys) for name, ys in values.items()}
    return [clean, lowres], samples, truth


def render_scatter(fixtures: Path):
    truth = {
        "red": [(0.9, 2.1), (2.4, 3.4), (4.1, 2.7), (6.1, 5.0), (8.4, 4.1)],
        "blue": [(1.2, 7.5), (3.2, 6.1), (4.9, 7.2), (7.0, 6.4), (8.7, 8.0)],
        "green": [(1.8, 4.8), (3.9, 5.2), (5.3, 4.2), (6.8, 3.6), (9.1, 5.1)],
    }
    fig, ax = make_ax("Synthetic scatter plot", (0, 10), (0, 10))
    for name, points in truth.items():
        data = np.asarray(points)
        ax.scatter(data[:, 0], data[:, 1], s=42, c=C[name], edgecolors="white", linewidths=0.35, label=name)
    ax.set(xlabel="x", ylabel="y")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=7, frameon=False)
    meta = save_figure(fig, ax, fixtures / "scatter.png", (0, 10), (0, 10))
    meta["name"] = "scatter"
    return meta, truth


def render_grouped(fixtures: Path):
    categories = np.arange(5, dtype=float)
    truth = {"red": [28, 35, 22, 45, 31], "blue": [42, 27, 48, 36, 52], "green": [18, 31, 29, 24, 39]}
    offsets = {"red": -0.24, "blue": 0.0, "green": 0.24}
    fig, ax = make_ax("Synthetic grouped bars", (-0.7, 4.7), (0, 70))
    for name, values in truth.items():
        ax.bar(categories + offsets[name], values, width=0.22, color=C[name], label=name)
    ax.set(xticks=categories, xticklabels=list("ABCDE"), ylabel="value")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=7, frameon=False)
    meta = save_figure(fig, ax, fixtures / "grouped_bars.png", (-0.7, 4.7), (0, 70))
    meta.update(name="grouped_bars", offsets=offsets)
    return meta, categories.tolist(), truth


def render_stacked(fixtures: Path):
    categories = np.arange(4, dtype=float)
    truth = {"red": [18, 22, 14, 25], "blue": [27, 19, 31, 18], "green": [16, 23, 20, 28]}
    fig, ax = make_ax("Synthetic stacked bars", (-0.6, 3.6), (0, 80))
    bottom = np.zeros(4)
    for name, values in truth.items():
        ax.bar(categories, values, width=0.58, bottom=bottom, color=C[name], label=name)
        bottom += values
    ax.set(xticks=categories, xticklabels=list("ABCD"), ylabel="value")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=7, frameon=False)
    meta = save_figure(fig, ax, fixtures / "stacked_bars.png", (-0.6, 3.6), (0, 80))
    meta["name"] = "stacked_bars"
    return meta, categories.tolist(), truth


def record(rows: list[dict], case: str, family: str, series: str, method: str, metric: dict) -> None:
    rows.append({"case": case, "family": family, "series": series, "method": method, **metric})


def evaluate_line(meta: dict, fixtures: Path, samples: list[float], truth: dict[str, list[float]], rows: list[dict]) -> None:
    image = np.asarray(Image.open(fixtures / meta["image"]).convert("RGB"))
    pixels = [x_pixel(value, meta) for value in samples]
    for name, expected in truth.items():
        colormask = mask(image, C[name])
        record(rows, meta["name"], "line", name, "single_column", scalar_metric(line_column(colormask, pixels, meta), expected, y_span(meta)))
        record(rows, meta["name"], "line", name, "continuity_trace", scalar_metric(line_trace(colormask, pixels, meta), expected, y_span(meta)))
        record(rows, meta["name"], "line", name, "raster_core_continuity", scalar_metric(raster_core_trace(image, C[name], samples, meta), expected, y_span(meta)))


def evaluate_scatter(meta: dict, fixtures: Path, truth: dict[str, list[tuple[float, float]]], rows: list[dict]) -> None:
    image = np.asarray(Image.open(fixtures / meta["image"]).convert("RGB"))
    for name, expected in truth.items():
        colormask = mask(image, C[name])
        yy, xx = np.where(colormask)
        global_centroid = [] if not len(xx) else [(x_value(float(xx.mean()), meta), y_value(float(yy.mean()), meta))]
        points = []
        for component in components(colormask, meta):
            points.append((x_value(float(component[:, 1].mean()), meta), y_value(float(component[:, 0].mean()), meta)))
        record(rows, meta["name"], "scatter", name, "global_color_centroid", point_metric(global_centroid, expected, y_span(meta)))
        record(rows, meta["name"], "scatter", name, "component_centroids", point_metric(points, expected, y_span(meta)))


def column_tops(colormask: np.ndarray, centers: list[float], meta: dict, radius: int = 0) -> list[float | None]:
    result = []
    for center in centers:
        candidates = nearby_rows(colormask, x_pixel(center, meta), meta, radius)
        result.append(None if not len(candidates) else y_value(float(candidates.min()), meta))
    return result


def component_tops(colormask: np.ndarray, centers: list[float], meta: dict) -> list[float | None]:
    found = components(colormask, meta, min_area=10)
    result = []
    for center in centers:
        if not found:
            result.append(None)
            continue
        target = x_pixel(center, meta)
        component = min(found, key=lambda item: abs(item[:, 1].mean() - target))
        result.append(y_value(float(component[:, 0].min()), meta))
    return result


def evaluate_grouped(meta: dict, fixtures: Path, categories: list[float], truth: dict[str, list[float]], rows: list[dict]) -> None:
    image = np.asarray(Image.open(fixtures / meta["image"]).convert("RGB"))
    for name, expected in truth.items():
        centers = [category + meta["offsets"][name] for category in categories]
        colormask = mask(image, C[name])
        record(rows, meta["name"], "grouped_bar", name, "center_column_top", scalar_metric(column_tops(colormask, centers, meta), expected, y_span(meta)))
        record(rows, meta["name"], "grouped_bar", name, "component_bounds", scalar_metric(component_tops(colormask, centers, meta), expected, y_span(meta)))


def segment_heights(colormask: np.ndarray, centers: list[float], meta: dict) -> list[float | None]:
    result = []
    for center in centers:
        candidates = nearby_rows(colormask, x_pixel(center, meta), meta, 1)
        if not len(candidates):
            result.append(None)
        else:
            result.append(abs(y_value(float(candidates.min()), meta) - y_value(float(candidates.max()), meta)))
    return result


def evaluate_stacked(meta: dict, fixtures: Path, categories: list[float], truth: dict[str, list[float]], rows: list[dict]) -> None:
    image = np.asarray(Image.open(fixtures / meta["image"]).convert("RGB"))
    for name, expected in truth.items():
        colormask = mask(image, C[name])
        record(rows, meta["name"], "stacked_bar", name, "top_as_height_baseline", scalar_metric(column_tops(colormask, categories, meta, 1), expected, y_span(meta)))
        record(rows, meta["name"], "stacked_bar", name, "segment_run_height", scalar_metric(segment_heights(colormask, categories, meta), expected, y_span(meta)))


def recommendations(rows: list[dict]) -> list[dict]:
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        groups[(row["family"], row["method"])].append(row)
    candidates: dict[str, list[dict]] = defaultdict(list)
    for (family, method), values in groups.items():
        candidates[family].append({"family": family, "method": method, "mean_mae": float(np.mean([value["mae"] for value in values])), "mean_coverage": float(np.mean([value["coverage"] for value in values])), "mean_normalized_score": float(np.mean([value["normalized_score"] for value in values]))})
    return [min(values, key=lambda item: item["mean_normalized_score"]) for _, values in sorted(candidates.items())]


def summary_plot(rows: list[dict], output: Path) -> None:
    groups: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for row in rows:
        groups[(row["case"], row["family"], row["method"])].append(row["normalized_score"])
    labels = [f"{case}\n{method}" for case, _, method in groups]
    scores = np.asarray([np.mean(values) for values in groups.values()])
    order = np.argsort(scores)
    fig, ax = plt.subplots(figsize=(11, 6), dpi=130)
    positions = np.arange(len(scores))
    ax.barh(positions, scores[order], color="#2c7fb8")
    ax.set(yticks=positions, yticklabels=np.asarray(labels)[order], xlabel="normalized error + missing-data penalty (lower is better)", title="Synthetic chart digitization benchmark")
    ax.tick_params(axis="y", labelsize=7)
    ax.grid(axis="x", color="#e6e6e6")
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, facecolor="white")
    plt.close(fig)


def fixture_gallery(fixtures: Path, names: list[str], output: Path) -> None:
    images = [(name, Image.open(fixtures / name).convert("RGB")) for name in names]
    cell_w, cell_h, margin, label_h = 330, 240, 14, 22
    gallery = Image.new("RGB", (3 * cell_w + 4 * margin, 2 * (cell_h + label_h) + 3 * margin), "white")
    draw = ImageDraw.Draw(gallery)
    for index, (name, image) in enumerate(images):
        row, col = divmod(index, 3)
        copy = image.copy()
        copy.thumbnail((cell_w, cell_h), Image.Resampling.LANCZOS)
        x = margin + col * (cell_w + margin) + (cell_w - copy.width) // 2
        y = margin + row * (cell_h + label_h + margin) + label_h
        gallery.paste(copy, (x, y))
        draw.text((margin + col * (cell_w + margin), y - label_h + 3), name, fill="black")
    gallery.save(output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    root, fixtures = args.output_dir, args.output_dir / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)
    line_cases, line_samples, line_truth = render_line(fixtures)
    scatter_case, scatter_truth = render_scatter(fixtures)
    grouped_case, grouped_categories, grouped_truth = render_grouped(fixtures)
    stacked_case, stacked_categories, stacked_truth = render_stacked(fixtures)
    rows: list[dict] = []
    for line_case in line_cases:
        evaluate_line(line_case, fixtures, line_samples, line_truth, rows)
    evaluate_scatter(scatter_case, fixtures, scatter_truth, rows)
    evaluate_grouped(grouped_case, fixtures, grouped_categories, grouped_truth, rows)
    evaluate_stacked(stacked_case, fixtures, stacked_categories, stacked_truth, rows)
    best = recommendations(rows)
    with (root / "benchmark_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["case", "family", "series", "method", "mae", "coverage", "normalized_score", "count"])
        writer.writeheader()
        writer.writerows(rows)
    report = {"schema_version": 1, "privacy": "All fixtures are deterministic and locally generated synthetic data.", "fixtures": [*line_cases, scatter_case, grouped_case, stacked_case], "results": rows, "recommendations": best}
    (root / "benchmark_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary_plot(rows, root / "benchmark_summary.png")
    fixture_gallery(fixtures, ["line_clean.png", "line_lowres.jpg", "scatter.png", "grouped_bars.png", "stacked_bars.png"], root / "fixture_gallery.png")
    print(f"RESULTS={root / 'benchmark_results.csv'}")
    print(f"REPORT={root / 'benchmark_report.json'}")
    for item in best:
        print(f"BEST {item['family']}: {item['method']} score={item['mean_normalized_score']:.4f}")


if __name__ == "__main__":
    main()

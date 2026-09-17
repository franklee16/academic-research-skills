#!/usr/bin/env python3
"""Extract low-level, reproducible clues from a scientific figure raster."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def hex_color(rgb: np.ndarray | tuple[int, int, int]) -> str:
    r, g, b = (int(v) for v in rgb)
    return f"#{r:02X}{g:02X}{b:02X}"


def border_pixels(rgb: np.ndarray) -> np.ndarray:
    h, w, _ = rgb.shape
    band = max(1, min(h, w) // 100)
    return np.concatenate(
        [
            rgb[:band].reshape(-1, 3),
            rgb[-band:].reshape(-1, 3),
            rgb[:, :band].reshape(-1, 3),
            rgb[:, -band:].reshape(-1, 3),
        ]
    )


def dominant_colors(image: Image.Image, count: int) -> list[dict[str, object]]:
    sample = image.copy()
    sample.thumbnail((600, 600))
    quantized = sample.quantize(colors=count, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette() or []
    total = sample.width * sample.height
    result = []
    for n, index in sorted(quantized.getcolors() or [], reverse=True):
        rgb = tuple(palette[index * 3 : index * 3 + 3])
        result.append({"hex": hex_color(rgb), "rgb": list(rgb), "fraction": round(n / total, 5)})
    return result


def consecutive_groups(values: np.ndarray) -> list[list[int]]:
    if values.size == 0:
        return []
    groups: list[list[int]] = [[int(values[0])]]
    for value in values[1:]:
        value = int(value)
        if value == groups[-1][-1] + 1:
            groups[-1].append(value)
        else:
            groups.append([value])
    return groups


def axis_line_candidates(rgb: np.ndarray, background: np.ndarray) -> dict[str, list[dict[str, int]]]:
    distance = np.linalg.norm(rgb.astype(float) - background.astype(float), axis=2)
    luminance = 0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2]
    ink = (distance > 45) & (luminance < 150)
    h, w = ink.shape
    row_hits = np.flatnonzero(ink.sum(axis=1) >= max(20, int(0.35 * w)))
    col_hits = np.flatnonzero(ink.sum(axis=0) >= max(20, int(0.35 * h)))
    return {
        "horizontal": [
            {"start_y": g[0], "end_y": g[-1], "thickness_px": len(g)}
            for g in consecutive_groups(row_hits)
        ],
        "vertical": [
            {"start_x": g[0], "end_x": g[-1], "thickness_px": len(g)}
            for g in consecutive_groups(col_hits)
        ],
    }


def analyze(path: Path, color_count: int) -> dict[str, object]:
    with Image.open(path) as source:
        original_mode = source.mode
        dpi = source.info.get("dpi")
        rgba = source.convert("RGBA")
        rgb_image = Image.new("RGB", rgba.size, "white")
        rgb_image.paste(rgba, mask=rgba.getchannel("A"))
        rgb = np.asarray(rgb_image)

    border = border_pixels(rgb)
    background = np.median(border, axis=0).round().astype(np.uint8)
    distance = np.linalg.norm(rgb.astype(float) - background.astype(float), axis=2)
    foreground = distance > 18
    ys, xs = np.nonzero(foreground)
    bbox = None if xs.size == 0 else [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    colored = (rgb.max(axis=2) - rgb.min(axis=2) > 12) & foreground
    return {
        "source": str(path.resolve()),
        "width_px": rgb_image.width,
        "height_px": rgb_image.height,
        "aspect_ratio": round(rgb_image.width / rgb_image.height, 6),
        "source_mode": original_mode,
        "embedded_dpi": list(dpi) if dpi else None,
        "estimated_background": hex_color(background),
        "border_color_std_rgb": [round(float(v), 2) for v in border.std(axis=0)],
        "non_background_bbox_xyxy": bbox,
        "non_background_fraction": round(float(foreground.mean()), 5),
        "colored_pixel_fraction": round(float(colored.mean()), 5),
        "dominant_colors": dominant_colors(rgb_image, color_count),
        "long_dark_line_candidates": axis_line_candidates(rgb, background),
        "limitations": [
            "Axis candidates are projection heuristics and may include gridlines or panel borders.",
            "Dominant colors include background, text, and antialiased mixtures.",
            "Semantic chart classification and text reading require visual inspection.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Input PNG/JPEG/TIFF image")
    parser.add_argument("--output", required=True, type=Path, help="Output JSON path")
    parser.add_argument("--colors", type=int, default=12, help="Number of dominant palette colors")
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"Input does not exist: {args.input}")
    if not 2 <= args.colors <= 64:
        parser.error("--colors must be between 2 and 64")
    report = analyze(args.input, args.colors)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

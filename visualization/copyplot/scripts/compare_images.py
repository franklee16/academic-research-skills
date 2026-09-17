#!/usr/bin/env python3
"""Compare a recreated figure with a reference and write diagnostics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageOps


def load_rgb(path: Path, size: tuple[int, int] | None = None) -> Image.Image:
    with Image.open(path) as source:
        rgba = source.convert("RGBA")
        canvas = Image.new("RGB", rgba.size, "white")
        canvas.paste(rgba, mask=rgba.getchannel("A"))
    if size and canvas.size != size:
        canvas = canvas.resize(size, Image.Resampling.LANCZOS)
    return canvas


def edge_mask(gray: np.ndarray) -> np.ndarray:
    gray = gray.astype(float)
    gx = np.abs(np.diff(gray, axis=1, prepend=gray[:, :1]))
    gy = np.abs(np.diff(gray, axis=0, prepend=gray[:1, :]))
    magnitude = gx + gy
    threshold = max(12.0, float(np.percentile(magnitude, 90)))
    return magnitude >= threshold


def compare(reference: Image.Image, candidate: Image.Image) -> tuple[dict[str, object], Image.Image]:
    a = np.asarray(reference).astype(float)
    b = np.asarray(candidate).astype(float)
    delta = a - b
    mae = float(np.abs(delta).mean())
    rmse = float(np.sqrt(np.mean(delta**2)))
    flat_a = a.mean(axis=2).ravel()
    flat_b = b.mean(axis=2).ravel()
    correlation = float(np.corrcoef(flat_a, flat_b)[0, 1]) if flat_a.std() and flat_b.std() else 0.0
    edge_a = edge_mask(a.mean(axis=2))
    edge_b = edge_mask(b.mean(axis=2))
    union = np.logical_or(edge_a, edge_b).sum()
    edge_iou = float(np.logical_and(edge_a, edge_b).sum() / union) if union else 1.0
    metrics = {
        "reference_size": list(reference.size),
        "candidate_size_after_resize": list(candidate.size),
        "mean_absolute_error_0_255": round(mae, 4),
        "root_mean_square_error_0_255": round(rmse, 4),
        "grayscale_correlation": round(correlation, 6),
        "edge_intersection_over_union": round(edge_iou, 6),
        "warning": "Metrics are visual diagnostics, not evidence of numerical or scientific equivalence.",
    }
    diff = ImageChops.difference(reference, candidate)
    diff = ImageOps.autocontrast(diff.convert("L")).convert("RGB")
    return metrics, diff


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    if not args.reference.is_file() or not args.candidate.is_file():
        parser.error("Both reference and candidate images must exist")
    reference = load_rgb(args.reference)
    original_candidate = load_rgb(args.candidate)
    same_size = original_candidate.size == reference.size
    candidate = original_candidate if same_size else original_candidate.resize(reference.size, Image.Resampling.LANCZOS)
    metrics, diff = compare(reference, candidate)
    metrics["candidate_original_size"] = list(original_candidate.size)
    metrics["same_size_before_comparison"] = same_size
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "comparison.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    diff.save(args.output_dir / "difference.png")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

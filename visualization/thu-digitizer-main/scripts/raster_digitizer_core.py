"""Reusable, local pixel-level primitives for auditable raster digitization.

The functions in this module intentionally stop at visible geometry.  They do
not infer raw observations, hidden replicates, fit parameters, or uncertainty
semantics that are not drawn in the figure.  They are shared by the candidate
line and bar routes so calibration, colour evidence, and confidence reporting
do not drift between case builders.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Iterable, Sequence

import numpy as np


VALID_AXIS_SCALES = {"linear", "log10", "displayed_log10"}


def _as_rgb(target: Sequence[int] | str) -> np.ndarray:
    if isinstance(target, str):
        value = target.strip().lstrip("#")
        if len(value) != 6:
            raise ValueError("colour must be #RRGGBB")
        try:
            target = tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))
        except ValueError as exc:
            raise ValueError("colour must be #RRGGBB") from exc
    if len(target) != 3 or any(int(channel) < 0 or int(channel) > 255 for channel in target):
        raise ValueError("colour must contain three channels in 0..255")
    return np.asarray(tuple(int(channel) for channel in target), dtype=np.float32)


def _transform_value(value: float, scale: str) -> float:
    if scale not in VALID_AXIS_SCALES:
        raise ValueError(f"axis scale must be one of {sorted(VALID_AXIS_SCALES)}")
    if scale == "log10":
        if value <= 0:
            raise ValueError("log10 axis values must be positive")
        return math.log10(value)
    return float(value)


def _inverse_value(value: float, scale: str) -> float:
    return float(10.0**value) if scale == "log10" else float(value)


@dataclass(frozen=True)
class AxisCalibration:
    """A robust pixel-to-value affine calibration in transformed value space."""

    pixel_slope: float
    transformed_intercept: float
    scale: str
    anchors: tuple[tuple[float, float], ...]
    residuals_pixels: tuple[float, ...]
    rmse_transformed: float
    max_abs_residual_transformed: float
    pixel_uncertainty: float

    @classmethod
    def fit(
        cls,
        anchors: Iterable[tuple[float, float]],
        *,
        scale: str = "linear",
        huber_delta: float = 1.5,
    ) -> "AxisCalibration":
        pairs = tuple((float(pixel), float(value)) for pixel, value in anchors)
        if len(pairs) < 2:
            raise ValueError("at least two axis anchors are required")
        if len({pixel for pixel, _ in pairs}) != len(pairs):
            raise ValueError("axis anchor pixels must be unique")
        transformed = np.asarray([_transform_value(value, scale) for _, value in pairs], dtype=float)
        pixels = np.asarray([pixel for pixel, _ in pairs], dtype=float)
        if np.ptp(pixels) <= 0 or np.ptp(transformed) <= 0:
            raise ValueError("axis anchors must span both pixel and value coordinates")
        design = np.column_stack([pixels, np.ones_like(pixels)])
        # Start from the pairwise model with the largest consensus rather than
        # ordinary least squares.  A single mistyped tick can otherwise pull a
        # four-anchor fit enough to create a systematic value error.
        if len(pairs) >= 3:
            models: list[tuple[float, float, float, int]] = []
            for first in range(len(pairs) - 1):
                for second in range(first + 1, len(pairs)):
                    slope = (transformed[second] - transformed[first]) / (pixels[second] - pixels[first])
                    intercept = transformed[first] - slope * pixels[first]
                    residuals = transformed - (slope * pixels + intercept)
                    absolute = np.abs(residuals)
                    median_abs = float(np.median(absolute))
                    inlier_cutoff = max(0.25, 2.5 * median_abs)
                    inliers = int(np.count_nonzero(absolute <= inlier_cutoff))
                    models.append((float(slope), float(intercept), median_abs, inliers))
            slope, intercept, _, _ = min(models, key=lambda item: (item[2], -item[3]))
        else:
            slope, intercept = np.linalg.lstsq(design, transformed, rcond=None)[0]
        initial_residuals = transformed - (slope * pixels + intercept)
        initial_scale = max(
            1.4826 * float(np.median(np.abs(initial_residuals - np.median(initial_residuals)))),
            0.25,
        )
        initial_z = np.abs(initial_residuals) / initial_scale
        weights = np.ones(len(pairs), dtype=float)
        outliers = initial_z > huber_delta
        weights[outliers] = huber_delta / initial_z[outliers]
        for _ in range(8):
            weighted_design = design * weights[:, None]
            weighted_values = transformed * weights
            slope, intercept = np.linalg.lstsq(weighted_design, weighted_values, rcond=None)[0]
            residuals = transformed - (slope * pixels + intercept)
            if len(pairs) < 3:
                break
            scale_estimate = 1.4826 * float(np.median(np.abs(residuals - np.median(residuals))))
            scale_estimate = max(scale_estimate, 0.25)
            robust_z = np.abs(residuals) / scale_estimate
            weights = np.ones(len(pairs), dtype=float)
            outliers = robust_z > huber_delta
            weights[outliers] = huber_delta / robust_z[outliers]
        residuals = transformed - (slope * pixels + intercept)
        rmse = float(np.sqrt(np.mean(np.square(residuals))))
        # One pixel is a conservative raster-location floor; additional anchor
        # disagreement is propagated as a data-space uncertainty below.
        pixel_uncertainty = max(0.5, rmse / max(abs(float(slope)), 1e-12))
        return cls(
            pixel_slope=float(slope),
            transformed_intercept=float(intercept),
            scale=scale,
            anchors=pairs,
            residuals_pixels=tuple(float(residual / slope) for residual in residuals),
            rmse_transformed=rmse,
            max_abs_residual_transformed=float(np.max(np.abs(residuals))),
            pixel_uncertainty=float(pixel_uncertainty),
        )

    def transformed_at_pixel(self, pixel: float) -> float:
        return float(self.pixel_slope * float(pixel) + self.transformed_intercept)

    def value_at_pixel(self, pixel: float) -> float:
        return _inverse_value(self.transformed_at_pixel(pixel), self.scale)

    def pixel_at_value(self, value: float) -> float:
        return (
            _transform_value(float(value), self.scale) - self.transformed_intercept
        ) / self.pixel_slope

    def uncertainty_at_pixel(self, pixel: float, *, pixel_sigma: float = 0.75) -> float:
        transformed = self.transformed_at_pixel(pixel)
        transformed_sigma = math.sqrt(
            (abs(self.pixel_slope) * max(pixel_sigma, 0.0)) ** 2
            + self.rmse_transformed**2
        )
        if self.scale == "log10":
            return abs(math.log(10.0) * _inverse_value(transformed, self.scale) * transformed_sigma)
        return transformed_sigma

    def report(self) -> dict[str, Any]:
        return {
            "scale": self.scale,
            "anchors": [{"pixel": pixel, "value": value} for pixel, value in self.anchors],
            "pixel_slope": self.pixel_slope,
            "transformed_intercept": self.transformed_intercept,
            "residuals_pixels": list(self.residuals_pixels),
            "rmse_transformed": self.rmse_transformed,
            "max_abs_residual_transformed": self.max_abs_residual_transformed,
            "pixel_uncertainty": self.pixel_uncertainty,
            "fit": "robust_huber_affine_in_transformed_value_space",
        }


def colour_distance(image: np.ndarray, target: Sequence[int] | str) -> np.ndarray:
    """Return Euclidean RGB distance without uint8 overflow."""

    rgb = np.asarray(image, dtype=np.float32)
    if rgb.ndim != 3 or rgb.shape[-1] != 3:
        raise ValueError("image must be an HxWx3 RGB array")
    return np.linalg.norm(rgb - _as_rgb(target), axis=2)


def colour_score(
    image: np.ndarray,
    target: Sequence[int] | str,
    *,
    sigma: float = 24.0,
    tolerance: float = 48.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Return a soft anti-aliased colour score and a conservative hard mask.

    The soft score preserves partially blended edge pixels.  The hard mask is
    deliberately stricter and is used only as evidence for an observed mark;
    an unobserved column is never silently interpolated into accepted data.
    """

    if sigma <= 0 or tolerance <= 0:
        raise ValueError("sigma and tolerance must be positive")
    distance = colour_distance(image, target)
    score = np.exp(-0.5 * np.square(distance / float(sigma))).astype(np.float32)
    return score, distance <= float(tolerance)


def _column_candidates(
    score: np.ndarray,
    *,
    threshold: float,
    top: int,
    bottom: int,
    edge_margin: int,
) -> list[list[dict[str, float]]]:
    """Collapse thick anti-aliased runs into weighted per-column candidates."""

    height, width = score.shape
    candidates: list[list[dict[str, float]]] = []
    lower = max(0, top + edge_margin)
    upper = min(height - 1, bottom - edge_margin)
    for x in range(width):
        active = score[lower : upper + 1, x] >= threshold
        rows = np.flatnonzero(active) + lower
        if not len(rows):
            candidates.append([])
            continue
        groups = np.split(rows, np.where(np.diff(rows) > 1)[0] + 1)
        column = []
        for group in groups:
            weights = score[group, x].astype(float)
            support = float(weights.sum())
            column.append(
                {
                    "y": float(np.average(group, weights=weights)),
                    "support": support,
                    "peak": float(weights.max()),
                    "width": float(len(group)),
                }
            )
        candidates.append(column)
    return candidates


def trace_colour_path(
    image: np.ndarray,
    *,
    target: Sequence[int] | str,
    plot_bounds: tuple[int, int, int, int],
    sigma: float = 24.0,
    tolerance: float = 48.0,
    score_threshold: float = 0.35,
    edge_margin: int = 3,
    smoothness: float = 0.10,
    gap_penalty: float = 0.85,
    max_step: float | None = 14.0,
) -> dict[str, Any]:
    """Trace one visible colour curve with continuity-aware dynamic programming.

    A path is chosen among colour-supported runs in each raster column.  The
    result retains observed-vs-gap states, support, path jumps, and a local
    pixel uncertainty; callers must keep gap columns as missing values.
    """

    rgb = np.asarray(image)
    if rgb.ndim != 3 or rgb.shape[-1] != 3:
        raise ValueError("image must be an HxWx3 RGB array")
    left, top, right, bottom = (int(value) for value in plot_bounds)
    height, width = rgb.shape[:2]
    if not (0 <= left < right < width and 0 <= top < bottom < height):
        raise ValueError("plot_bounds must fit image dimensions")
    score_full, hard_full = colour_score(rgb, target, sigma=sigma, tolerance=tolerance)
    score = score_full[top : bottom + 1, left : right + 1]
    hard = hard_full[top : bottom + 1, left : right + 1]
    candidates = _column_candidates(
        score,
        threshold=score_threshold,
        top=0,
        bottom=score.shape[0] - 1,
        edge_margin=edge_margin,
    )
    # Remove candidates that are long, perfectly horizontal border/grid lines;
    # these are common in black raster plots and are not curve evidence.
    for y in range(score.shape[0]):
        occupancy = float(np.mean(score[y] >= score_threshold))
        if occupancy > 0.78:
            for column in candidates:
                column[:] = [candidate for candidate in column if abs(candidate["y"] - y) > 2.5]

    states: list[list[dict[str, float]]] = []
    predecessor: list[list[tuple[int, int] | None]] = []
    costs: list[list[float]] = []
    for column_index, column in enumerate(candidates):
        current = list(column) + [{"y": math.nan, "support": 0.0, "peak": 0.0, "width": 0.0}]
        states.append(current)
        predecessor.append([None] * len(current))
        costs.append([math.inf] * len(current))
        if column_index == 0:
            for index, candidate in enumerate(current):
                costs[-1][index] = gap_penalty if math.isnan(candidate["y"]) else -candidate["support"]
        else:
            for index, candidate in enumerate(current):
                best_cost = math.inf
                best_prev: int | None = None
                for prev_index, prev_candidate in enumerate(states[-2]):
                    prev_cost = costs[-2][prev_index]
                    if not math.isfinite(prev_cost):
                        continue
                    if math.isnan(candidate["y"]) or math.isnan(prev_candidate["y"]):
                        transition = gap_penalty
                    else:
                        jump = abs(candidate["y"] - prev_candidate["y"])
                        if max_step is not None and jump > max_step:
                            continue
                        transition = smoothness * jump
                    candidate_cost = prev_cost + transition - (candidate["support"] if not math.isnan(candidate["y"]) else 0.0)
                    if candidate_cost < best_cost:
                        best_cost = candidate_cost
                        best_prev = prev_index
                costs[-1][index] = best_cost
                if best_prev is not None:
                    predecessor[-1][index] = (len(states) - 2, best_prev)
    if not states:
        return {"status": "not_extracted", "path": [], "coverage": 0.0, "hard_mask_pixels": 0}
    last_index = int(np.argmin(costs[-1]))
    selected: list[dict[str, float]] = [{"y": math.nan, "support": 0.0, "peak": 0.0, "width": 0.0}] * len(states)
    cursor = last_index
    for column_index in range(len(states) - 1, -1, -1):
        selected[column_index] = states[column_index][cursor]
        previous = predecessor[column_index][cursor]
        if previous is None:
            break
        _, cursor = previous
    path = []
    observed = 0
    jumps = []
    previous_y_value: float | None = None
    for index, candidate in enumerate(selected):
        if math.isnan(candidate["y"]):
            path.append({"x_pixel": left + index, "y_pixel": None, "status": "gap", "support": 0.0, "uncertainty_px": None})
            previous_y_value = None
            continue
        observed += 1
        if previous_y_value is not None:
            jumps.append(abs(candidate["y"] - previous_y_value))
        previous_y_value = candidate["y"]
        support_uncertainty = max(0.35, 1.2 / math.sqrt(max(candidate["support"], 1e-6)))
        path.append(
            {
                "x_pixel": left + index,
                "y_pixel": round(top + candidate["y"], 4),
                "status": "observed",
                "support": round(candidate["support"], 4),
                "peak_score": round(candidate["peak"], 4),
                "run_width_px": round(candidate["width"], 4),
                "uncertainty_px": round(support_uncertainty, 4),
            }
        )
    coverage = observed / max(1, len(path))
    return {
        "status": "extracted" if coverage >= 0.85 else "partial_visible",
        "path": path,
        "coverage": round(float(coverage), 4),
        "mean_jump_px": round(float(np.mean(jumps)), 4) if jumps else None,
        "p95_jump_px": round(float(np.percentile(jumps, 95)), 4) if jumps else None,
        "hard_mask_pixels": int(np.count_nonzero(hard)),
        "colour": list(map(int, _as_rgb(target))),
        "parameters": {
            "sigma": sigma,
            "tolerance": tolerance,
            "score_threshold": score_threshold,
            "edge_margin": edge_margin,
            "smoothness": smoothness,
            "gap_penalty": gap_penalty,
            "max_step": max_step,
        },
    }


def sample_traced_path(
    trace: dict[str, Any],
    *,
    x_values: Sequence[float],
    x_axis: AxisCalibration,
    y_axis: AxisCalibration,
    sample_radius_px: int = 3,
) -> list[dict[str, Any]]:
    """Map a traced pixel path to requested x values without filling gaps."""

    if sample_radius_px < 0:
        raise ValueError("sample_radius_px must be non-negative")
    observed = [item for item in trace.get("path", []) if item.get("y_pixel") is not None]
    by_x = {int(item["x_pixel"]): item for item in observed}
    result = []
    for x_value in x_values:
        x_pixel = x_axis.pixel_at_value(float(x_value))
        centre = int(round(x_pixel))
        nearby = [item for pixel, item in by_x.items() if abs(pixel - centre) <= sample_radius_px]
        if not nearby:
            result.append(
                {
                    "x": float(x_value),
                    "x_pixel": round(float(x_pixel), 4),
                    "y": None,
                    "y_pixel": None,
                    "status": "not_extracted",
                    "confidence": 0.0,
                }
            )
            continue
        weights = np.asarray([max(float(item.get("support", 0.0)), 1e-6) for item in nearby], dtype=float)
        y_pixels = np.asarray([float(item["y_pixel"]) for item in nearby], dtype=float)
        y_pixel = float(np.average(y_pixels, weights=weights))
        uncertainty_px = float(np.sqrt(np.average(np.square(y_pixels - y_pixel), weights=weights)))
        uncertainty_px = max(uncertainty_px, max(float(item.get("uncertainty_px") or 0.0) for item in nearby))
        confidence = min(1.0, 0.4 + 0.3 * min(1.0, float(weights.sum()) / 8.0) + 0.3 * math.exp(-uncertainty_px))
        result.append(
            {
                "x": float(x_value),
                "x_pixel": round(float(x_pixel), 4),
                "y": round(y_axis.value_at_pixel(y_pixel), 8),
                "y_pixel": round(y_pixel, 4),
                "uncertainty_px": round(uncertainty_px, 4),
                "uncertainty_value": round(y_axis.uncertainty_at_pixel(y_pixel, pixel_sigma=uncertainty_px), 8),
                "status": "visible_geometry_observed",
                "confidence": round(confidence, 4),
            }
        )
    return result

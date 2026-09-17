"""Machine-readable extractor registry and conservative route selection."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class RouteDescriptor:
    route_id: str
    title: str
    chart_types: tuple[str, ...]
    media_kinds: tuple[str, ...]
    coordinate_models: tuple[str, ...]
    mark_grammars: tuple[str, ...]
    maturity: str
    implementation: str | None
    required_confirmations: tuple[str, ...]
    recoverable: str
    non_recoverable: str
    automated_extraction: bool

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for key in (
            "chart_types",
            "media_kinds",
            "coordinate_models",
            "mark_grammars",
            "required_confirmations",
        ):
            data[key] = list(data[key])
        return data


ROUTES = (
    RouteDescriptor(
        "raster_line_color",
        "Colour-distinct calibrated raster line (sample or continuity candidate)",
        ("line",),
        ("raster",),
        ("cartesian_linear",),
        ("curve", "marker", "error_interval"),
        "validated_local_stable",
        "scripts/digitize_line_chart.py",
        ("panel_roi", "plot_bounds", "x_axis", "y_axis", "axis_transform", "series_colors", "sample_positions", "trace_mode", "anchor_residual_review"),
        "Visible colour-distinct curve samples, or continuity-traced visible spans with support/gap uncertainty, plus separately visible pale error intervals.",
        "Hidden spans, source model parameters, and raw observations.",
        True,
    ),
    RouteDescriptor(
        "raster_marker_line_candidate",
        "Compact filled marker-on-line with global path selection",
        ("marker_line",),
        ("raster",),
        ("cartesian_linear",),
        ("curve", "marker", "reference_line"),
        "candidate",
        "scripts/candidate_digitize_marker_line.py",
        (
            "panel_roi",
            "plot_bounds",
            "x_axis",
            "y_axis",
            "axis_transform",
            "series_colors",
            "sample_positions",
            "compact_filled_marker_grammar",
            "reference_line_conflicts",
            "overlay_review",
            "anchor_residual_review",
        ),
        "Visible compact marker centres at verified sample positions, including background-dependent marker colours and same-colour reference-line conflicts.",
        "Unmarked curve values, hidden samples, source model parameters, and unsupported hollow or non-compact markers.",
        True,
    ),
    RouteDescriptor(
        "raster_scatter_color",
        "Compact filled calibrated raster scatter with touching-marker splitting",
        ("scatter",),
        ("raster",),
        ("cartesian_linear",),
        ("point",),
        "candidate",
        "scripts/candidate_digitize_scatter.py",
        (
            "panel_roi",
            "plot_bounds",
            "x_axis",
            "y_axis",
            "axis_transform",
            "compact_filled_marker_grammar",
            "marker_polarity_or_color",
            "overlay_review",
        ),
        "Centres of compact filled visible markers, including partially touching markers with distinct distance peaks.",
        "Perfectly coincident, fully occluded, hollow, non-compact, or size-encoded bubble markers and hidden source rows.",
        True,
    ),
    RouteDescriptor(
        "raster_complex_line_candidate",
        "Complex line/step/fit composite",
        (
            "multi_line",
            "time_series",
            "learning_curve",
            "calibration_curve",
            "roc_curve",
            "pr_curve",
            "survival_curve",
            "scatter_with_fit",
        ),
        ("raster",),
        ("cartesian_linear", "cartesian_log_x", "cartesian_log_y", "cartesian_date_x"),
        ("curve", "step_curve", "point", "error_interval", "reference_line"),
        "candidate_or_not_implemented_by_variant",
        None,
        (
            "panel_roi",
            "plot_bounds",
            "axis_transform",
            "series_association",
            "crossing_and_occlusion_review",
        ),
        "Only visibly separable trace spans, markers, steps, and reference lines.",
        "Occluded spans, thresholds not drawn, model state, and source parameters.",
        False,
    ),
    RouteDescriptor(
        "raster_histogram_color",
        "Calibrated colour-distinct histogram",
        ("histogram",),
        ("raster",),
        ("cartesian_linear",),
        ("bin_rectangle",),
        "validated_local_stable",
        "scripts/digitize_histogram.py",
        ("panel_roi", "plot_bounds", "x_axis", "y_axis", "bar_color"),
        "Visible bin edges and heights.",
        "Original observations inside bins.",
        True,
    ),
    RouteDescriptor(
        "raster_boxplot_color",
        "Calibrated filled boxplot",
        ("box",),
        ("raster",),
        ("categorical_value",),
        ("box_summary", "outlier"),
        "validated_local_stable",
        "scripts/digitize_boxplot.py",
        ("panel_roi", "plot_bounds", "value_axis", "orientation", "box_line_outlier_colors"),
        "Visible five-number summaries and separable visible outliers.",
        "Raw samples and hidden/fused outliers.",
        True,
    ),
    RouteDescriptor(
        "raster_outline_boxplot_candidate",
        "Paired outline/split-fill publication boxplot",
        ("paired_outline_box", "box_with_overlay"),
        ("raster",),
        ("categorical_value",),
        ("box_summary", "outlier", "overlay_point"),
        "candidate",
        "scripts/candidate_digitize_outline_boxplot.py",
        ("panel_roi", "plot_bounds", "value_axis", "orientation", "series_style", "overlay_review"),
        "Visible box summaries and uniquely separable visible overlay points.",
        "Raw samples and fused or box-edge-conflicted points.",
        True,
    ),
    RouteDescriptor(
        "raster_bar_candidate",
        "Simple/grouped/stacked calibrated raster bars",
        ("bar", "grouped_bar", "stacked_bar", "percent_stacked_bar", "negative_bar"),
        ("raster",),
        ("categorical_value",),
        ("rectangle", "stack_segment", "error_interval"),
        "candidate",
        "scripts/candidate_digitize_bar_chart.py",
        (
            "panel_roi",
            "plot_bounds",
            "value_axis",
            "orientation",
            "layout",
            "category_centers",
            "series_colors",
            "legend_exclusions",
        ),
        "Visible rectangle endpoints/segments and separately visible error intervals.",
        "Hidden samples, zero/occluded segments, and unverified SD/SEM/CI semantics.",
        True,
    ),
    RouteDescriptor(
        "raster_heatmap_candidate",
        "Rectangular heatmap with readable continuous colour bar",
        ("heatmap", "confusion_matrix"),
        ("raster",),
        ("grid_color",),
        ("cell", "colorbar", "text_or_symbol"),
        "candidate",
        "scripts/candidate_digitize_heatmap.py",
        ("panel_roi", "grid_bounds", "row_column_order", "colorbar_bounds", "colorbar_values"),
        "Visible cells, missing-cell mask, calibrated colours, and separately visible symbols.",
        "Values without a readable scale and hidden annotations.",
        True,
    ),
    RouteDescriptor(
        "raster_lattice_composite_candidate",
        "Repeated aligned bars with categorical membership lattice",
        ("upset", "lattice_composite"),
        ("raster",),
        ("lattice_composite",),
        ("aligned_bar", "row_bar", "membership_cell", "connector", "categorical_strip"),
        "candidate",
        "scripts/candidate_digitize_lattice_composite.py",
        (
            "original_raster",
            "panel_roi",
            "layer_grammar",
            "column_bar_color",
            "row_bar_color",
            "node_color",
            "semantic_labels",
            "row_value_axis",
            "overlay_review",
        ),
        "Original-pixel repeated bar geometry, complete active/inactive/ambiguous cell classification, and independently validated visible values when supplied.",
        "Hidden records, occluded cells, unverified text, and meanings not visibly encoded by the aligned layers.",
        True,
    ),
    RouteDescriptor(
        "raster_labelled_donut_candidate",
        "Visible-label pie/donut with annular geometry validation",
        ("pie", "donut"),
        ("raster",),
        ("polar",),
        ("visible_numeric_label", "color_sector", "annular_band"),
        "assisted_candidate",
        "scripts/candidate_digitize_labelled_donut.py",
        (
            "original_raster",
            "panel_roi",
            "group_centers",
            "radial_bands",
            "series_palette",
            "two_pass_visible_label_transcription",
            "label_anchors",
            "overlay_review",
        ),
        "Explicitly visible numeric labels whose duplicate transcription agrees and whose normalized shares match independently sampled sector geometry.",
        "Unlabeled sectors, hidden source values, raw observations, and any value inferred only from an angle.",
        True,
    ),
    RouteDescriptor(
        "pdf_dose_response_vector",
        "Vector-PDF dose-response geometry",
        ("dose_response",),
        ("pdf",),
        ("cartesian_displayed_log_x",),
        ("point", "error_interval", "curve", "broken_axis_control"),
        "candidate",
        "scripts/candidate_digitize_dose_response_pdf.py",
        (
            "page",
            "panel_roi",
            "plot_bounds",
            "x_axis",
            "y_axis",
            "series_marker_shapes",
            "marker_and_curve_colors",
            "legend_exclusions",
        ),
        "Visible marker centres, visible error endpoints, broken-axis controls, and traced curve paths.",
        "Raw replicates and author fit parameters unless independently provided.",
        True,
    ),
    RouteDescriptor(
        "pdf_vector_assisted",
        "Generic verified vector-PDF inspection and assisted recovery",
        (
            "line",
            "scatter",
            "histogram",
            "box",
            "bar",
            "grouped_bar",
            "stacked_bar",
            "forest_plot",
            "scatter_with_fit",
        ),
        ("pdf",),
        (
            "cartesian_linear",
            "cartesian_log_x",
            "cartesian_log_y",
            "categorical_value",
            "interval_rows",
        ),
        ("vector_path", "vector_marker", "vector_rectangle", "text"),
        "assisted_candidate",
        "scripts/inspect_pdf_vectors.py",
        ("page", "panel_roi", "axis_transform", "path_to_data_verification", "legend_exclusions"),
        "Only vector objects visually verified as plotted marks and calibrated to verified axes.",
        "Any path whose panel, semantic role, or transform remains ambiguous.",
        False,
    ),
    RouteDescriptor(
        "unsupported_coordinate_route",
        "Coordinate-specific route not implemented",
        (
            "matrix_plot",
            "area",
            "stacked_area",
            "waterfall",
            "radar",
            "polar",
            "ternary",
            "geospatial_map",
            "network_plot",
            "sankey_alluvial",
            "event_raster",
            "table_like",
            "density",
            "violin",
            "bubble_plot",
            "dot_plot",
            "volcano_plot",
            "umap_tsne_pca",
        ),
        ("raster", "pdf"),
        ("unknown",),
        ("unknown",),
        "not_implemented_or_case_only",
        None,
        ("chart_specific_contract", "coordinate_specific_benchmark"),
        "A panel-specific visible representation only after a dedicated route is implemented.",
        "No values should be accepted through a generic XY fallback.",
        False,
    ),
    RouteDescriptor(
        "unknown_refuse",
        "Unknown chart: refuse numeric extraction",
        ("unknown",),
        ("raster", "pdf"),
        ("unknown",),
        ("unknown",),
        "refusal",
        None,
        ("chart_type", "coordinate_model", "recoverable_representation"),
        "Input metadata and routing diagnostics only.",
        "All numeric values until the chart grammar and coordinate model are verified.",
        False,
    ),
)

ROUTE_BY_ID = {route.route_id: route for route in ROUTES}

ALIASES = {
    "boxplot": "box",
    "box_plot": "box",
    "groupedbar": "grouped_bar",
    "stackedbar": "stacked_bar",
    "100%_stacked_bar": "percent_stacked_bar",
    "dose-response": "dose_response",
    "dose response": "dose_response",
    "forest": "forest_plot",
    "heat_map": "heatmap",
    "scatter_fit": "scatter_with_fit",
    "scatter_plot": "scatter",
    "upset_plot": "upset",
    "upsetplot": "upset",
    "lattice": "lattice_composite",
}


def normalize_chart_type(chart_type: str | None) -> str | None:
    if chart_type is None:
        return None
    normalized = chart_type.strip().lower().replace("-", "_").replace(" ", "_")
    return ALIASES.get(chart_type.strip().lower(), ALIASES.get(normalized, normalized))


def _raster_route(chart_type: str) -> RouteDescriptor:
    candidates = [
        route
        for route in ROUTES
        if "raster" in route.media_kinds and chart_type in route.chart_types
    ]
    if not candidates:
        return ROUTE_BY_ID["unknown_refuse"]
    implemented = [route for route in candidates if route.implementation is not None]
    return implemented[0] if implemented else candidates[0]


def select_route(
    *,
    chart_type: str | None,
    media_kind: str,
    pdf_composition: str | None = None,
) -> dict[str, Any]:
    """Select a route without converting a hint into a verified classification."""

    normalized = normalize_chart_type(chart_type)
    if normalized is None:
        route = ROUTE_BY_ID["unknown_refuse"]
        return {
            "chart_type": None,
            "primary": route.as_dict(),
            "fallback": None,
            "decision": "needs_chart_type_confirmation",
            "reason": "No chart-type hint was provided; numeric extraction is refused until classification is verified.",
        }

    known_types = {item for route in ROUTES for item in route.chart_types}
    if normalized not in known_types:
        route = ROUTE_BY_ID["unknown_refuse"]
        return {
            "chart_type": normalized,
            "primary": route.as_dict(),
            "fallback": None,
            "decision": "unsupported",
            "reason": "The chart type is not registered and must not be forced through an XY route.",
        }

    if media_kind == "pdf" and pdf_composition in {"vector_paths_detected", "mixed_vector_and_raster"}:
        if normalized == "dose_response":
            route = ROUTE_BY_ID["pdf_dose_response_vector"]
            return {
                "chart_type": normalized,
                "primary": route.as_dict(),
                "fallback": None,
                "decision": "needs_verified_configuration",
                "reason": "A dedicated vector-PDF dose-response candidate exists; panel, axes, series, and paths still require verification.",
            }
        generic = ROUTE_BY_ID["pdf_vector_assisted"]
        raster = _raster_route(normalized)
        if normalized not in generic.chart_types:
            if raster.route_id == "unsupported_coordinate_route":
                return {
                    "chart_type": normalized,
                    "primary": raster.as_dict(),
                    "fallback": None,
                    "decision": "not_automated",
                    "reason": "This chart family needs a dedicated coordinate/mark contract and must not enter generic vector or XY recovery.",
                }
            if raster.route_id == "unknown_refuse":
                return {
                    "chart_type": normalized,
                    "primary": raster.as_dict(),
                    "fallback": None,
                    "decision": "unsupported",
                    "reason": "No compatible vector or raster route is registered for this chart type.",
                }
            return {
                "chart_type": normalized,
                "primary": raster.as_dict(),
                "fallback": None,
                "decision": (
                    "needs_rasterization_and_verified_configuration"
                    if raster.automated_extraction
                    else "not_automated"
                ),
                "reason": "No compatible vector adapter is registered; the selected raster route may be used only after explicit page rendering and its normal verification gates.",
                "preprocessing_required": "render_verified_pdf_page_to_raster",
            }
        return {
            "chart_type": normalized,
            "primary": generic.as_dict(),
            "fallback": raster.as_dict() if raster.route_id != "unknown_refuse" else None,
            "decision": "needs_verified_configuration",
            "reason": "Vector content is preferred, but path-to-data identity must be visually verified before coordinate recovery.",
        }

    raster = _raster_route(normalized)
    if raster.route_id == "unknown_refuse":
        return {
            "chart_type": normalized,
            "primary": raster.as_dict(),
            "fallback": None,
            "decision": "unsupported",
            "reason": "No dedicated raster extractor is registered for this chart type.",
        }
    if raster.implementation is None or not raster.automated_extraction:
        decision = "not_automated"
    else:
        decision = "needs_verified_configuration"
    return {
        "chart_type": normalized,
        "primary": raster.as_dict(),
        "fallback": None,
        "decision": decision,
        "reason": "A route is registered, but all required confirmations remain explicit before extraction.",
    }


def registry_document() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "claim": "Registry presence is routing metadata, not proof of extraction support.",
        "routes": [route.as_dict() for route in ROUTES],
    }

import unittest
from pathlib import Path

try:
    from extractor_registry import ROUTES, select_route
    from figure_spec import validate_figure_spec
    from thu_digitizer import build_preflight
except ImportError:  # pragma: no cover - package-style unittest invocation
    from .extractor_registry import ROUTES, select_route
    from .figure_spec import validate_figure_spec
    from .thu_digitizer import build_preflight


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"


class UnifiedRouterTests(unittest.TestCase):
    def test_registry_ids_are_unique_and_every_route_declares_limits(self):
        self.assertEqual(len({route.route_id for route in ROUTES}), len(ROUTES))
        for route in ROUTES:
            with self.subTest(route=route.route_id):
                self.assertTrue(route.recoverable)
                self.assertTrue(route.non_recoverable)
                self.assertGreater(len(route.required_confirmations), 0)

        ownership = {}
        for route in ROUTES:
            for media_kind in route.media_kinds:
                for chart_type in route.chart_types:
                    key = (media_kind, chart_type)
                    self.assertNotIn(
                        key,
                        ownership,
                        msg=(
                            f"{media_kind}/{chart_type} is declared by both "
                            f"{ownership.get(key)} and {route.route_id}"
                        ),
                    )
                    ownership[key] = route.route_id

    def test_real_vector_pdf_routes_to_dose_response_without_authorizing_values(self):
        pdf = (
            GALLERY
            / "assets"
            / "cases"
            / "nature-kahlous-dose-response"
            / "source-article.pdf"
        )
        report, spec = build_preflight(pdf, chart_type="dose_response", page_number=7)
        self.assertEqual(report["inspection"]["pdf_composition"], "vector_paths_detected")
        self.assertEqual(report["route_selection"]["primary"]["route_id"], "pdf_dose_response_vector")
        self.assertEqual(report["status"], "needs_verified_configuration")
        self.assertFalse(report["safety"]["numeric_extraction_authorized"])
        panel = spec["panels"][0]
        self.assertEqual(panel["coordinate_model"], "cartesian_displayed_log_x")
        self.assertEqual(panel["axes"][0]["scale"], "displayed_log10")
        self.assertEqual(validate_figure_spec(spec), [])

    def test_real_raster_histogram_routes_to_stable_limited_extractor(self):
        image = GALLERY / "assets" / "basics" / "histogram" / "original.png"
        report, spec = build_preflight(image, chart_type="histogram")
        route = report["route_selection"]["primary"]
        self.assertEqual(route["route_id"], "raster_histogram_color")
        self.assertEqual(route["maturity"], "validated_local_stable")
        self.assertEqual(report["inspection"]["appearance"]["background_proposal"], "light")
        self.assertEqual(validate_figure_spec(spec), [])

    def test_raster_scatter_routes_to_fixed_compact_marker_candidate(self):
        image = GALLERY / "assets" / "cases" / "nature-70099-fig5e" / "original.png"
        report, spec = build_preflight(image, chart_type="scatter")
        route = report["route_selection"]["primary"]
        self.assertEqual(route["route_id"], "raster_scatter_color")
        self.assertEqual(route["maturity"], "candidate")
        self.assertEqual(route["implementation"], "scripts/candidate_digitize_scatter.py")
        self.assertIn("compact_filled_marker_grammar", route["required_confirmations"])
        self.assertIn("overlay_review", route["required_confirmations"])
        self.assertFalse(report["safety"]["numeric_extraction_authorized"])
        self.assertEqual(validate_figure_spec(spec), [])

    def test_upset_routes_to_original_pixel_lattice_candidate(self):
        image = GALLERY / "assets" / "cases" / "nature-27341-fig1" / "original.png"
        report, spec = build_preflight(image, chart_type="upset")
        route = report["route_selection"]["primary"]
        self.assertEqual(route["route_id"], "raster_lattice_composite_candidate")
        self.assertEqual(route["implementation"], "scripts/candidate_digitize_lattice_composite.py")
        self.assertEqual(spec["source"]["measurement_space"], "original_raster_pixels")
        self.assertFalse(spec["source"]["resampling_applied"])
        self.assertEqual(spec["panels"][0]["coordinate_model"], "lattice_composite")
        self.assertIn("layer_grammar", route["required_confirmations"])
        self.assertFalse(report["safety"]["numeric_extraction_authorized"])
        self.assertEqual(validate_figure_spec(spec), [])

    def test_missing_or_unknown_chart_type_refuses_numeric_extraction(self):
        missing = select_route(chart_type=None, media_kind="raster")
        self.assertEqual(missing["primary"]["route_id"], "unknown_refuse")
        self.assertEqual(missing["decision"], "needs_chart_type_confirmation")

        unknown = select_route(chart_type="atomistic_structure", media_kind="raster")
        self.assertEqual(unknown["primary"]["route_id"], "unknown_refuse")
        self.assertEqual(unknown["decision"], "unsupported")

    def test_raster_dose_response_does_not_reuse_pdf_only_extractor(self):
        selected = select_route(chart_type="dose_response", media_kind="raster")
        self.assertEqual(selected["primary"]["route_id"], "unknown_refuse")
        self.assertEqual(selected["decision"], "unsupported")

    def test_labelled_donut_routes_to_shared_assisted_candidate(self):
        selected = select_route(chart_type="donut", media_kind="raster")
        self.assertEqual(
            selected["primary"]["route_id"], "raster_labelled_donut_candidate"
        )
        self.assertEqual(selected["decision"], "needs_verified_configuration")
        self.assertEqual(
            selected["primary"]["implementation"],
            "scripts/candidate_digitize_labelled_donut.py",
        )

        pdf = select_route(
            chart_type="pie",
            media_kind="pdf",
            pdf_composition="vector_paths_detected",
        )
        self.assertEqual(pdf["primary"]["route_id"], "raster_labelled_donut_candidate")
        self.assertEqual(
            pdf["decision"], "needs_rasterization_and_verified_configuration"
        )

    def test_non_cartesian_vector_pdf_never_enters_generic_vector_recovery(self):
        unsupported = next(
            route for route in ROUTES if route.route_id == "unsupported_coordinate_route"
        )
        for chart_type in unsupported.chart_types:
            with self.subTest(chart_type=chart_type):
                selected = select_route(
                    chart_type=chart_type,
                    media_kind="pdf",
                    pdf_composition="vector_paths_detected",
                )
                self.assertEqual(
                    selected["primary"]["route_id"], "unsupported_coordinate_route"
                )
                self.assertEqual(selected["decision"], "not_automated")

    def test_vector_pdf_without_compatible_adapter_requires_explicit_rasterization(self):
        selected = select_route(
            chart_type="heatmap",
            media_kind="pdf",
            pdf_composition="vector_paths_detected",
        )
        self.assertEqual(selected["primary"]["route_id"], "raster_heatmap_candidate")
        self.assertEqual(
            selected["decision"], "needs_rasterization_and_verified_configuration"
        )
        self.assertEqual(
            selected["preprocessing_required"],
            "render_verified_pdf_page_to_raster",
        )


if __name__ == "__main__":
    unittest.main()

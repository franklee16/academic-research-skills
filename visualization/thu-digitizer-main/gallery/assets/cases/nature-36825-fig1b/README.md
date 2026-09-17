# Figure 1b extraction status

The registered `scripts/candidate_digitize_bar_chart.py` route was run on the exact `1959 × 2040` publisher raster. Its verified configuration is recorded in `figure-spec.json`: original-pixel plot bounds `(1392, 78, 1696, 490)`, linear value anchors `(489 px, 0%)` and `(78 px, 100%)`, vertical percent-stacked grammar, category centers G `1438`, K `1544.5`, L `1650.5`, and the eleven palette entries visible in the legend.

The candidate found **29 visible stack rectangles** and returned four series/category combinations as `not_extracted`. The overlay places every accepted magenta rectangle on a visible colored segment and does not ring legend swatches. However, the registered report status is deliberately retained as **`low_confidence`**:

- requested category × legend combinations: 33;
- extracted visible rectangles: 29;
- `not_extracted`: G/Methanocorpusculum, K/Methanohalophilus, K/other, L/Methanospirillum;
- percent-stack visible-fill totals: G `98.5401%`, K `98.7835%`, L `98.7835%`, outside the candidate’s `±0.75` percentage-point gate because one-pixel white boundaries between rendered segments are not bar fill.

`extraction-all-statuses.csv` and `extraction-report.json` are the immutable registered-candidate outputs. `visible-segments-candidate.csv` is only a filtered view of the 29 `status=extracted` rows and does **not** upgrade authorization or confidence. No expected detected-mark count was passed to the extractor. No absent/zero/occluded segment was filled.

The official source files are used only in `source-validation.csv` and `source-validation-summary.json`. Semantic mapping is verified, but numerical source validation is `not_comparable_css_normalization_not_reproduced`: the source mapping states CSS normalization while the retained tables do not pin the exact implementation parameters/aggregation settings. Raw-count group aggregates are kept only as contextual evidence and never drive the raster CSV or recreation.


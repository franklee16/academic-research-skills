# Economics Chart Recipes

Choose the recipe based on the inferential object, not on the software's default chart type.

## Descriptive time series and trends

- Use a line only when the x-axis is meaningfully continuous and the ordering matters.
- Keep the raw/focal series darker than comparison series. Use markers for annual or otherwise sparse observations; omit most markers for dense monthly/daily data.
- For two groups, default to bright blue solid circles and orange dashed squares. Direct-label the final values when this avoids a detached legend.
- Label interventions with a thin dashed vertical line and short text. Multiple event lines may use neutral gray for context and one accent for the focal event.
- If showing an interrupted trend, display observed points and pre/post fitted segments separately. Do not join the fitted segments across the intervention.
- When seasonality or level differences dominate, consider indexing, logs, residualization, or small multiples only if that transformation is substantively justified and declared.

## Categorical comparisons

- Prefer a dot plot for precise comparisons, especially when estimates have intervals. Use bars for amounts or shares whose common zero baseline is meaningful.
- Sort by a conceptually meaningful order; otherwise sort by value. Keep treatment/control or demographic pairs adjacent.
- Use horizontal orientation for long labels. Wrap labels in the stub/margin rather than rotating them vertically.
- For bars, use a neutral light-gray fill with dark intervals or one accent fill for a focal category. Put short values inside or just above bars only when they reduce lookup effort.
- Never use 3-D bars, gradients, exploded pies, or decorative pictograms. For part-to-whole comparisons, prefer sorted bars, a 100% stacked bar with few categories, or a compact table.

## Distributions and descriptive densities

- Use histograms for counts/density, ECDFs for distributional comparison, box/violin plots for compact summaries, and ridgelines only when many distributions must be compared.
- Fix bin boundaries and bandwidth across groups. State the bin width or bandwidth when it affects interpretation.
- Use outlines, low-opacity fills, or small multiples rather than fully opaque overlapping histograms.
- For randomization or placebo inference, show the simulated distribution in light gray, the actual statistic as a diagnostic-red vertical dashed line, and the randomization p-value in a quiet annotation. State the number of draws and whether the p-value is one- or two-sided.

## Scatter, binned scatter, and regression discontinuity

- Use small, partially transparent raw points for modest datasets. For dense data, use bins/hexagons or a binned scatter and report how bins were formed.
- Highlight only observations or labels discussed in the text; keep the remainder in light gray.
- For RD plots, put the cutoff at zero when possible, use the same binning logic on both sides, and fit separate lines/curves without extrapolating beyond the support.
- Draw the cutoff as an ink or diagnostic-red vertical line, and draw the outcome-zero line only if substantively meaningful.
- State polynomial order, bandwidth, kernel, bin selection, covariate adjustment, and whether the plotted fit matches the reported estimator. Avoid high-order global polynomials.
- Do not let the graphic substitute for the formal RD estimate and uncertainty.

## Event studies and parallel-trend figures

Default form: coefficient dots with 95% confidence intervals, a horizontal zero line, and a vertical treatment-onset marker.

Before drawing, determine whether treatment timing is common or staggered and what the supplied estimator identifies. With staggered timing, do not present an unchecked lead/lag TWFE regression as dynamic ATT when treatment effects may be heterogeneous. Preserve the researcher's chosen estimator, but label it precisely and verify its cohort/event-time support, comparison groups, aggregation weights, and changing composition across event time. If the estimand or support changes in tail periods, bin or trim only with a declared rule.

Resolve uncertainty before computing plot bounds:

1. If lower/upper bounds are supplied by the fitted object or result extract, use them and preserve their stated method.
2. If only estimates and SEs are supplied, recover the model's reference distribution, degrees of freedom, covariance construction, and confidence level before calculating bounds. Do not silently assume `estimate ± 1.96×SE`, especially with few clusters or finite-sample corrections.
3. For bootstrap, randomization, profile, simultaneous, or inverted-test intervals, use the method's stored quantiles/critical value or recompute through the estimator's supported API.
4. If the metadata needed to reproduce uncertainty are unavailable, pause and request them; do not label guessed bounds as confidence intervals.

1. Order event time numerically and preserve endpoint bins such as `≤−5` and `≥6` in their labels.
2. Identify the omitted period, normally `t = −1`, in the axis/caption. Either show an explicit zero marker with no interval or leave a visible gap; never present it as an estimated coefficient.
3. Put the treatment boundary between `−1` and `0`, or shade the post period beginning at `0`. Use one convention throughout the paper.
4. Plot 95% intervals by default. State whether bands are pointwise or simultaneous; never describe pointwise intervals as a simultaneous pre-trend band. If two estimators or samples are compared, horizontally dodge estimates slightly and use redundant marker/line encodings.
5. Default to unconnected dots for a diagnostic coefficient display or when support/composition differs across event time. Thin connectors are acceptable when event time is discrete, support is comparable, and the dynamic path is the intended reading. If connected, break every series at the omitted category; do not bridge it as if estimated.
6. Use the same y-range across outcomes when magnitude comparison is meaningful. Otherwise label differing scales clearly.
7. Put the joint pre-trend p-value in the note or a quiet annotation only if it was pre-specified and correctly computed. Do not use failure to reject as proof of parallel trends.
8. The note must state estimator, fixed effects/control structure if nonstandard, clustering/bootstrap, sample, reference period, endpoint binning, and—under staggered timing—the cohort/support and aggregation convention. Put cohort or observation support by event time in the note, an aligned auxiliary panel, or an appendix diagnostic when composition materially changes.

When multiple estimators share exactly the same normalization, use either one centered neutral hollow reference marker or one hollow marker per horizontally dodged estimator. Prefer one shared marker when it reduces clutter; use separate markers when retaining series identity is important. In either case, label the point as normalized, draw no interval, and state the convention once in the note.

For a multi-outcome event study, use 2×2, 3×2, or a 4+3 appendix layout, one shared legend, and panel-specific outcome titles. Outcomes with a common unit and estimand share the y-scale. Outcomes with different units may use panel-specific y-scales, but panel sizes, event-time positions, and zero lines must align and every y-axis must state its unit. For a primary outcome plus gender/subgroup decomposition, the centered aggregate panel above two subgroup panels used in the supplied samples is acceptable.

## Coefficient plots and nested confidence intervals

- Put variable/specification labels on the y-axis and estimates on the x-axis. Use a vertical zero line.
- Show one row per estimand. Use a conceptual order: main estimate, design alternatives, inference alternatives, sample alternatives, then controls/measurement alternatives.
- A useful nested interval design draws 95% intervals in mid gray behind 90% intervals and points in research blue. Explain both levels once in a shared legend.
- Keep a common scale across facets. If estimates have incompatible units, separate them into panels or standardize only with explicit justification.
- Do not print significance stars beside points. The interval already communicates sampling uncertainty.

## Heterogeneity forest plots

Use a forest plot rather than a bar chart.

- Start with the overall estimate, followed by pre-specified subgroup families. Use bold family headings and indent subgroup labels.
- Plot point estimates and 95% intervals on a common x-axis with a thin zero line. Reserve a right-side text column for `Estimate (SE/CI)`, subgroup `N`, and the interaction/difference p-value when space permits.
- Use one consistent focal color; use shape or light/dark variants only to distinguish estimators or samples. Do not give every subgroup a new color.
- Order subgroups substantively, not by effect size, p-value, or significance. Show both members of a partition and use the same reference definition as the model.
- Report the p-value for equality/interaction for each subgroup family. Do not claim heterogeneous effects because confidence intervals cross zero differently.
- Markers may scale with precision or sample size only when the size encoding is explained and bounded so it does not dominate.
- Long labels belong in a left text column. Alternate very faint row shading only for dense forests; avoid boxed cells and heavy separators.
- If outcomes use different units, facet by outcome with separate labeled axes. If one scale is shared, align zero lines exactly.

## Robustness and specification displays

- For up to roughly six models with a small number of coefficients, a compact coefficient plot is usually clearer than another regression table.
- For many one-at-a-time checks, use a robustness forest: specification names at left, estimates/95% intervals in the middle, and key sample/model facts at right.
- Put the baseline first and visually distinguish it with a filled point or bold label, not a different axis.
- A specification curve is appropriate only when the specification universe is defined systematically. Show the estimate panel, inclusion matrix, uncertainty/significance rule, and a defensible ordering without implying data mining is validation.
- Keep diagnostics such as weak-IV statistics, pre-trend tests, or sample sizes in aligned text columns rather than encoding them as arbitrary colors.

## Multi-series and many-category data

- At four or fewer series, use color plus marker/line type and direct labels.
- Above four series, prefer small multiples or highlight-one-series-at-a-time panels. A dense spaghetti plot is rarely acceptable for the main paper.
- In small multiples, keep all context series thin and light, and the focal series dark. Use the same axes and label the focal series directly.
- Do not repeat legends inside every panel. Preserve a stable category-to-color mapping across the entire paper.

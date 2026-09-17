---
name: econfigure
description: Create, revise, or audit publication-ready economics figures and plotting code, including lines, bars, histograms or densities, scatter and binned plots, event studies and parallel trends, coefficient plots, RD, and heterogeneity or robustness forests. Use when producing or assessing a research figure; pair with econtable for mixed figure-and-table requests.
---

# Econfigure

Produce figures that are econometrically honest, visually quiet, reproducible, and legible at final journal size. Preserve the user's estimand, sample, units, language, and software unless a change is necessary and disclosed.

## Start with the research object

Before styling, identify or infer from the project:

- the question the figure must answer and the comparison readers should make;
- the observation unit, sample, outcome units or transformation, and time/category order;
- whether values are raw data, fitted values, coefficients, marginal effects, or predictions;
- the uncertainty definition, confidence level, standard-error construction, weights, and clustering;
- the target medium and final physical width.

Do not invent data, estimates, confidence intervals, labels, or model details. Do not silently rebase, normalize, winsorize, aggregate, bin, smooth, or omit observations. When required information is absent but recoverable from data or model objects, inspect those objects rather than asking the user.

If the request requires a real figure but no data, model object, or extractable estimates are available, pause and request the minimum missing input. Generate synthetic values only for an explicitly requested mockup or test, label them as synthetic in the artifact, and never let them flow into a research deliverable. Do not ship unresolved placeholders for sample, units, or inference in a final caption.

## Route to the detailed guidance

- Read [references/visual-system.md](references/visual-system.md) for every figure. It defines the sample-derived typography, color, axis, panel, caption, and export defaults.
- Read [references/chart-recipes.md](references/chart-recipes.md) for the requested chart family, especially event studies, parallel-trend plots, and heterogeneity forests.
- Read [references/implementation-recipes.md](references/implementation-recipes.md) when writing or revising R, Stata, Python, or LaTeX assembly code.
- Read [references/sample-derived-decisions.md](references/sample-derived-decisions.md) only when matching the supplied examples closely, explaining provenance, or deciding between competing layouts.

## Working sequence

1. Inspect the data/model object and nearby project code. Reuse the project's language, packages, variable labels, and export path when they are serviceable.
2. Validate the plotted values: ordering, units, missingness, reference category, confidence-interval formula, and panel comparability.
3. Choose the chart form that makes the intended comparison easiest. Estimates with uncertainty normally use dots and intervals, not bars.
4. Apply the visual system. Make the data darker than scaffolding; encode important distinctions with at least two of color, shape, line type, or direct labels.
5. Add only interpretively necessary reference lines and annotations. Keep the figure-level title, number, caption, and long notes in the manuscript unless the target is a slide or standalone image.
6. Export at final dimensions, render the actual output, and inspect it at 100% and reduced size. Check grayscale and color-vision robustness when more than one series is present.

## Econometric integrity

- Mark the omitted/reference category unambiguously in coefficient and event-study plots. Do not connect across a missing reference period in a way that implies an estimated coefficient.
- Show the requested confidence level and state it in the caption or note. A 95% interval is the default for inference; nested 90% and 95% intervals are acceptable when both are explicitly identified.
- In heterogeneity work, report or reserve space for the interaction or cross-group difference test. Do not infer heterogeneity from one subgroup being significant and another not.
- Use a common axis for panels intended for magnitude comparison. If different scales are necessary, state that prominently and do not invite visual comparison of slopes or distances.
- Bar charts start at zero. Truncated axes are acceptable for line or estimate plots only when clearly labeled and not misleading.
- Smoothers, fitted segments, and binned means must be visually distinct from raw observations and described in the note.
- Do not use dual axes by default. Use them only when the relationship is essential, units are explicit, scales are not tuned to manufacture correlation, and direct labels make the mapping unmistakable.

## Delivery contract

When creating or editing a figure, return or save:

- executable source code tied to the underlying data or stored model objects;
- manuscript files required by the target journal's current author guide; absent a specified journal, use vector PDF/SVG plus a white-background PNG preview at the requested size, normally 300 dpi or higher;
- a concise caption/note draft that defines the sample, unit, estimand, uncertainty, reference period, and any non-obvious construction;
- concise alt text that states the chart type, comparison, direction/magnitude of the main pattern, and essential uncertainty without duplicating the full caption;
- a short QA statement identifying the dimensions and the checks performed.

Keep intermediate data and graphics out of the final directory unless the project already uses a documented build structure. Never hand-edit plotted values after export.

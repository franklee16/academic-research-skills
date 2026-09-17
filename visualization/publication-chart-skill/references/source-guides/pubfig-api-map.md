# pubfig API map (source-driven)

This guide maps the public `pubfig` API from `pubfig/src/pubfig/__init__.py` to the underlying modules.

## 1. Stable entrypoint

The public contract is defined by re-exports in `pubfig.__init__`.

For agents, this means:

- if a symbol is re-exported there, it is a good default public entrypoint;
- if a helper only exists in deep internal modules, treat it as implementation detail unless there is a strong reason not to.

## 2. Public API groups

### Themes

Public re-exports:

- `set_default_theme`
- `get_default_theme`
- `get_theme`
- `register_theme`

Use these when the task is really about reusable visual policy.
Do not hardcode theme assumptions if a registry call is more appropriate.

### Colors and palettes

Public re-exports include:

- `DEFAULT`, `NATURE`, `SCIENCE`, `LANCET`, `JAMA`
- `get_palette`
- `register_palette`
- `color_to_rgba`
- `darken_color`
- `show_palette`

Source fact:

- palette registration and palette inspection are exposed from the package root.

Operational implication:

- treat palette selection and palette registration as public API usage, not as deep internal customization.

### Export

Public re-exports:

- `save_figure`
- `batch_export`
- `PanelExportRecord`
- `export_panel`
- `export_panels`
- `package_figma_bundle`
- `validate_figma_bundle`
- `inspect_figma_bundle`

Skill implication:

- normal paper figures should usually stop at `save_figure` or `batch_export`
- panel workflows should use `export_panel(s)`
- bundle helpers are for bridge/Figma handoff, not the default answer

### Figure specs

Public re-exports:

- `FigureSpec`
- `get_figure_spec`
- `register_figure_spec`
- `list_figure_specs`

Use this layer whenever the user asks for venue-aware width, journal defaults, or a custom export profile.

### Plot families

The public plot surface is broad, but the source still clusters naturally.

#### Comparison / summary figures

Representative public calls:

- `bar`
- `bar_scatter`
- `stacked_bar`
- `stacked_ratio_barh`
- `donut`
- `dumbbell`
- `forest_plot`
- `grouped_scatter`
- `upset`

Use these for benchmark, ablation, summary, composition, and set-overlap tasks.

#### Distribution figures

Representative public calls:

- `ecdf`
- `qq`
- `box`
- `density`
- `hexbin`
- `histogram`
- `raincloud`
- `strip`
- `ridgeline`
- `violin`

Use these when the scientific claim is about spread, calibration of assumptions, or cohort structure.

#### Trend / profile figures

Representative public calls:

- `line`
- `area`
- `parallel_coordinates`
- `radar`
- `radial_hierarchy`
- `circular_stacked_bar`
- `circular_grouped_bar`

Not all of these are equally strong for publication use. The skill should still apply chart-selection discipline before calling them.

#### Relationship / embedding figures

Representative public calls:

- `scatter`
- `volcano`
- `bubble`
- `contour2d`
- `paired`
- `heatmap`
- `corr_matrix`
- `clustermap`
- `dimreduce`
- `pca_biplot`

Use these for association, error structure, feature layout, and representation views.

#### Evaluation figures

Representative public calls:

- `roc`
- `pr_curve`
- `calibration`
- `bland_altman`

This cluster matters because the source gives them dedicated implementation in `plots/evaluation.py`, which is a sign that evaluation charts are a first-class use case.

## 3. Return-value contract

The source in `export/io.py` makes a subtle but important contract explicit:

- export functions accept a Matplotlib `Figure`,
- or an `Axes`,
- or any object exposing a `.figure` attribute that resolves to a `Figure`.

Source fact:

- the export layer accepts standard Matplotlib figure objects or figure-bearing wrappers.

Operational implication:

- keep the `Figure` handle available and route export through the standard Matplotlib-facing export path.

For the skill, the safest phrasing is:

- create the figure,
- keep a handle to the `Figure`,
- then export explicitly.

## 4. What is not the main stable plotting interface

From the source tree, the CLI is not where normal chart creation happens.
It is mostly an operational layer for Figma bundle and bridge actions.

So if a user says “generate a paper-ready figure,” the skill should not default to a CLI answer.

## 5. Safe public usage pattern

The most source-faithful pattern is:

1. choose a public plot function from `pubfig`
2. generate a `Figure`
3. export via `save_figure(...)` or `batch_export(...)`
4. only use panel/bundle helpers when composition is actually required

## 6. Source-guided caution points

- Do not mix up plot-time design sizing with export-time publication sizing.
- Do not use `save_figure(...)` as a multi-format exporter; the source now pushes that role to `batch_export(...)`.
- Do not route ordinary figure-generation tasks through the Figma bridge CLI.
- Do not assume all public plot families are equally appropriate; the skill must still filter by scientific communication quality.

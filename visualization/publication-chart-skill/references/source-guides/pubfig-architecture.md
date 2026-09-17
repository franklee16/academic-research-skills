# pubfig architecture (source-driven)

This guide reads `pubfig` from the source tree rather than from high-level overview material.

Source root:

- `pubfig/src/pubfig/__init__.py`
- `pubfig/src/pubfig/plots/`
- `pubfig/src/pubfig/export/`
- `pubfig/src/pubfig/specs.py`
- `pubfig/src/pubfig/themes/`
- `pubfig/src/pubfig/colors/`
- `pubfig/src/pubfig/cli.py`

## 1. Start at `pubfig.__init__`

The stable user-facing surface is re-exported from `__init__.py`.

That file tells you the package is organized into five main layers:

1. **plot constructors** from `plots/`
2. **export helpers** from `export/`
3. **publication sizing** from `specs.py`
4. **theme and palette registries** from `themes/` and `colors/`
5. **Figma/bridge helpers** and related CLI support

For skill design, this is the most important architectural fact:

- figure generation lives in `plots/`
- figure export lives in `export/`
- venue sizing lives in `specs.py`
- multi-panel/Figma handoff is a separate downstream layer

The default mental model is **plot first, export second, compose third**.

## 2. Package boundaries

### `plots/`

This is the core figure-construction layer.

Representative files:

- `plots/line.py`
- `plots/comparison.py`
- `plots/evaluation.py`
- `plots/_grouped_scatter.py`

From the source, plot functions usually do the same sequence:

1. normalize/coerce input data,
2. enter `theme_context(theme)`,
3. resolve design-time size via `resolve_design_dpi(...)`,
4. allocate figure/axes via `get_fig_ax(...)`,
5. style axes/legends through helpers in `_style.py`,
6. return a Matplotlib `Figure`.

Interpretation from source:

- `pubfig` behaves as a **Matplotlib-first figure factory layer**, not as a separate scene-graph runtime.

### `export/`

This is intentionally separated from plotting.

Important files:

- `export/io.py`
- `export/panels.py`

`export/io.py` handles normal figure export:

- coerce Figure/Axes into a real `Figure`
- enforce explicit suffixes
- apply publication width/height rules
- write vector or raster output

Current source implication:

- `batch_export(...)` now belongs to the same publication-aware export layer, rather than to a simple multi-format `savefig` wrapper.

`export/panels.py` handles panel-level export for composite or Figma-oriented workflows:

- one panel at a time or many panels together
- optional publication-aware sizing
- optional title stripping
- metadata index generation (`panel-index.json`)

### `specs.py`

This file is the publication-sizing contract.

`FigureSpec` defines:

- `font_family`
- `design_dpi`
- `single_column_mm`
- `double_column_mm`
- `default_raster_dpi`
- `background_color`

Built-in registry entries include:

- `nature`
- `science`
- `cell`

The source shows a strong split between:

- **design size** used when constructing interactive figures,
- **physical export size** used when saving publication figures.

That split is why the skill should not treat `width` in plot calls and `width` in export calls as the same semantic layer.

### `themes/` and `colors/`

These are registries, not plain constants.

From `__init__.py`, the public surface includes:

- `get_theme`, `register_theme`, `set_default_theme`
- `get_palette`, `register_palette`, `show_palette`

Operational implication:

- treat theme and palette selection as first-class API configuration rather than as hardcoded styling trivia.

### `cli.py`

The current CLI is not the main figure-generation interface.

From the source, `cli.py` is mainly about:

- Figma bridge serving
- bundle packaging/inspection/validation
- sync job submission and waiting
- local bridge auto-start logic

So for this skill:

- **Python API is the primary route for figure generation**
- `pubfig.cli` is a secondary operational layer for bridge/Figma workflows

## 3. Plotting architecture pattern

From `line.py`, `comparison.py`, and `evaluation.py`, the recurring internal pattern is:

- input normalization is local to the chart family,
- shared visual behavior is delegated to internal helpers,
- returned artifact is still a standard Matplotlib figure.

This is why the skill should map requests to a chart family first, instead of jumping directly to export or panel assembly.

Examples from source:

- `line.py` groups time/trend style plots
- `comparison.py` groups comparison-style statistical displays like `dumbbell` and `forest_plot`
- `evaluation.py` groups metric/evaluation plots like `roc`, `pr_curve`, and `calibration`
- `_grouped_scatter.py` contains the more specialized placement/jitter/annotation logic behind grouped scatter layouts

## 4. Export architecture pattern

From `export/io.py` and `export/panels.py`, `pubfig` uses three distinct output modes:

1. **single explicit artifact** via `save_figure(...)`
2. **publication-aware multi-format artifact set** via `batch_export(...)`
3. **panel bundle workflow** via `export_panel(...)` / `export_panels(...)`

Those are different contracts, and the skill should keep them separate in its recommendations.

## 5. Reading order for deep debugging

When a skill or agent needs source-level certainty, use this order:

1. `pubfig/src/pubfig/__init__.py`
2. relevant chart-family module in `plots/`
3. `pubfig/src/pubfig/specs.py`
4. `pubfig/src/pubfig/export/io.py`
5. `pubfig/src/pubfig/export/panels.py`
6. `pubfig/src/pubfig/cli.py` only if the task involves bridge/Figma sync

## 6. Implications for this skill

This source layout implies the skill should:

- default to **Python plot API + explicit export call**,
- treat publication sizing as an export concern,
- treat panel/Figma work as optional downstream composition,
- avoid presenting the CLI as the main path for ordinary figure generation,
- keep chart selection logically ahead of export tuning.

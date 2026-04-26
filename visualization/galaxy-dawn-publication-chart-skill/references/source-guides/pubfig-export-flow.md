# pubfig export flow (source-driven)

This guide explains how `pubfig` moves from a generated Matplotlib figure to paper-ready files.

Primary source files:

- `pubfig/src/pubfig/export/io.py`
- `pubfig/src/pubfig/export/panels.py`
- `pubfig/src/pubfig/specs.py`

## 1. Core export contract

`export/io.py` separates two concerns:

- **coercing a valid figure object**
- **writing explicit output files**

The helper `_coerce_mpl_figure(...)` accepts:

- a `Figure`
- an `Axes`
- an object with a `.figure` attribute pointing to a `Figure`

The export layer is standardized around Matplotlib figures, even if upstream plotting code returns a richer wrapper.

## 2. `save_figure(...)` is now single-target and suffix-explicit

A key source-level rule lives in `_resolve_save_figure_target(...)`:

- `save_figure(...)` now requires an explicit filename suffix,
- supported examples include `.pdf`, `.svg`, `.png`, `.jpg`, `.tif`, `.eps`, `.ps`,
- if there is no suffix, the function raises an error,
- if multiple outputs are wanted, the source tells you to use `batch_export(...)`.

Skill implication:

- always write `results/figure1.pdf` rather than `results/figure1`
- when you want several formats, recommend `batch_export(...)`, not legacy vector/raster format lists

## 3. Publication sizing path

`save_figure(...)` is publication-aware.

Internally it does the following:

1. load the chosen `FigureSpec` via `get_figure_spec(...)`
2. resolve width through `resolve_width_mm(...)`
3. resolve height through `resolve_height_mm(...)`
4. set the Matplotlib figure size in inches using mm-to-inch conversion
5. choose raster DPI from the spec unless overridden
6. save the explicit target file
7. restore original caller state afterward

Interpretation from source:

- export sizing is more than a file-write step; it can temporarily resize the figure to venue-oriented physical dimensions before output.

## 4. Width and height semantics

From `specs.py`:

- width can be `single`, `double`, or a numeric mm value
- the built-in registry contains `nature`, `science`, and `cell`
- height can be explicit `height_mm`
- otherwise height is derived from `aspect_ratio`

That yields a clean rule for the skill:

- if the user asks for publication width, use `save_figure(..., spec=..., width=...)`
- if the user only wants quick draft export, keep the recommendation minimal

## 5. `batch_export(...)`

`batch_export(...)` is the publication-aware multi-format lane.

Source behavior:

- it takes a `base_path`
- it accepts publication export controls such as `spec`, `width`, `height_mm`, `aspect_ratio`, and `dpi`
- appends each explicit suffix from `formats`
- relayouts the figure through `_export_with_publication_layout(...)` for each target format
- restores the original in-memory figure size/state after export

This is the right recommendation when the user needs, for example:

- `PDF` for manuscript submission
- `SVG` for downstream editing
- `PNG` for slides or issue threads

Operational implication:

- use `batch_export(...)` when the task needs multiple publication-style outputs from the same figure,
- do not describe it as a plain `savefig` loop.

## 6. What `_save_basic_figure(...)` still does

`_save_basic_figure(...)` is still relevant, but it is no longer the main multi-format path for `batch_export(...)`.

It remains the lower-level path used for:

- direct basic export helpers,
- size-preserving panel export in `export/panels.py`,
- and internal single-target save operations that do not need publication relayout.

From the source, it also handles:

- output directory creation
- vector-text rcParams (important for editable SVG/PDF text handling)
- post-layout legend alignment
- post-layout callbacks attached by plot code
- trim/tight bbox behavior

So export quality is partially centralized in the export layer, not only inside plot modules.

## 7. Panel export lane

`export/panels.py` defines the multi-panel handoff path.

Key components:

- `PanelExportRecord`
- `export_panel(...)`
- `export_panels(...)`
- `_write_panel_index(...)`

A `PanelExportRecord` stores:

- `panel_id`
- `path`
- `format`
- `exported_at`
- `figma_node_name`
- `pubfig_version`
- optional `title`
- optional `label`

This shows that panel export is not only file emission. It also preserves minimal sync metadata.

## 8. Title stripping is intentional

One subtle but important source behavior:

- `_temporarily_strip_titles(...)` removes figure/axes titles during panel export by default unless `include_title=True`

Operational implication:

- panel-first composite assembly usually wants clean panel artwork,
- whole-figure titles and layout labels are often handled later,
- prefer exporting clean panel art first and adding whole-figure titles or layout labels downstream when needed.

## 9. Publication-aware vs size-preserving panel export

`export_panel(...)` has two modes:

### Publication-aware mode

Triggered when any of these are supplied:

- `spec`
- `width`
- `height_mm`

Then it delegates to `save_figure(...)`.

### Size-preserving mode

If none of those are supplied, it falls back to `_save_basic_figure(...)` and preserves the figure’s current size.

Skill implication:

- for reproducible paper panels, specify publication export parameters
- for design review or quick composition, preserving current size may be acceptable

## 10. Multiple panel export

`export_panels(...)` does three main things:

1. normalize and validate panel ids,
2. resolve labels for each panel,
3. export each panel and optionally write `panel-index.json`.

Default recommendation:

- prefer this route when the user wants a structured panel directory rather than a single whole-figure asset.

## 11. Overwrite and safety behavior

From `_ensure_writable_target(...)`:

- an existing panel file raises unless `overwrite=True`

That is useful for skill guidance because it means refresh-in-place is an explicit decision.

## 12. Recommended source-faithful export patterns

### Single paper figure

- plot with `pubfig.<chart_family>(...)`
- save with `save_figure(fig, 'out/figure1.pdf', spec='nature', width='single')`

### Same figure in several formats

- plot once
- export with `batch_export(fig, 'out/figure1', formats=('pdf', 'svg', 'png'), spec='nature', width='single', dpi=300)`

### Multi-panel downstream assembly

- generate each panel as a separate `Figure`
- export with `export_panels(...)`
- use the index file for composite/Figma-aware downstream handling

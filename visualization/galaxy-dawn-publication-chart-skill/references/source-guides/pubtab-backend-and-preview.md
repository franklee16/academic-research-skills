# pubtab backend and preview internals (source-driven)

This guide focuses on the two most important deeper layers in `pubtab`:

- backend/theme separation
- real preview/compile execution

Primary source files:

- `pubtab/src/pubtab/themes/__init__.py`
- `pubtab/src/pubtab/backends/__init__.py`
- `pubtab/src/pubtab/renderer.py`
- `pubtab/src/pubtab/_preview.py`

## 1. Theme and backend are different contracts

The source separates them cleanly.

### Theme layer

In `themes/__init__.py`, a theme resolves to `ThemeConfig`.

It carries style defaults such as:

- `column_sep`
- `font_size`
- `caption_position`
- `SpacingConfig`

### Backend layer

In `backends/__init__.py`, a backend resolves to:

- `BackendConfig`
- a Jinja template string

`BackendConfig` carries things like:

- package requirements
- preamble hints
- backend identity

Operational implication:

- theme = stylistic defaults
- backend = LaTeX environment/template machinery

## 2. Legacy normalization exists, but it is not the conceptual model

The source still supports legacy composite theme names like `_tabularray` suffixed themes.

Normalization happens in places like:

- `_normalize_theme_backend_choice(...)`
- `resolve_theme(...)`

But that compatibility layer should not define the skill’s main explanation.
The current conceptual model is still **separate theme + backend**.

## 3. What `render(...)` actually does

`renderer.py` is the core place where theme/backend decisions become concrete LaTeX.

Inside `render(...)`, the source does roughly this:

1. normalize theme/backend choice
2. load theme config
3. load backend config and template
4. merge default/theme/user spacing
5. compute or project column specs
6. branch into backend-specific row/cell rendering
7. render through Jinja

Backend choice changes the internal rendering algorithm, not only the final environment name.

## 4. `tabular` vs `tabularray` from the source perspective

The source suggests this practical distinction:

### `tabular`

- more classic LaTeX path
- column spec and rules are handled in the traditional environment
- when source `column_spec` exists, renderer tries to preserve classic rule structure

### `tabularray`

- dedicated `tblr`-style rendering path
- special handling for promoted vertical lines and grouped header boundaries
- extra sanitization in preview compile path

Interpretation from source:

- `tabularray` is a distinct renderer path with its own structural handling, not merely a cosmetic wrapper around `tabular`.

## 5. Why backend choice sometimes matters a lot

From `renderer.py`, backend differences affect:

- how colspec is interpreted
- how vertical rules are preserved or promoted
- how merged cells are encoded
- how row coloring and header boundaries are emitted

So if a table is structurally complex, the skill should not present backend choice as arbitrary.

## 6. Preview is a real LaTeX toolchain

`_preview.py` proves preview is a full execution pipeline.

Major steps:

1. locate `pdflatex`
2. install TinyTeX if missing
3. build a standalone document around the table
4. compile with `pdflatex`
5. auto-install missing LaTeX packages when possible
6. return PDF or convert to PNG

Preview is therefore a genuine verification step.

## 7. `pdflatex` discovery and TinyTeX fallback

The source checks:

- system `PATH`
- pubtab-managed TinyTeX under `~/.pubtab/TinyTeX`

If neither exists, it installs TinyTeX automatically.

This is why the skill can confidently describe preview as relatively self-healing, while still warning that first-run setup may download TeX assets.

## 8. Missing package retry

A particularly important source behavior:

- compile logs are scanned for missing `.sty`
- missing style names are mapped to `tlmgr` package names when needed
- `tlmgr install <pkg>` is run automatically
- compilation is retried

This is strong evidence that the recommended workflow should include preview, because preview can repair part of the environment on the way.

## 9. Standalone preview wrapping

`_build_standalone(...)` does more than wrap text in a document.

It also:

- imports backend-required packages
- preserves setup commands outside the `resizebox` body
- wraps the body in a preview-friendly standalone/minipage layout
- converts `\caption{...}` into `\captionof{table}{...}` during float stripping

This explains why preview output can differ from naive manual compilation if the user simply pastes a table fragment into a document incorrectly.

## 10. `tabularray` preview sanitization

Before compilation, `_sanitize_tblr_for_compile(...)` removes some commands that break inside `tblr` preview contexts, including certain row-color and `\cmidrule` forms.

So when debugging preview-vs-final-document differences, this source behavior matters.

## 11. PDF to PNG conversion fallback stack

For PNG previews, the source tries:

1. `pdf2image`
2. fallback to PyMuPDF (`fitz`)

Preview generation remains resilient even after PDF compilation succeeds.

## 12. Practical skill guidance from the source

### Recommend `tabular` when

- the table is simple/classic,
- the user wants conservative LaTeX output,
- compatibility matters more than modern layout features.

### Recommend `tabularray` when

- grouped headers and more complex structural layouts matter,
- the user is already targeting a `tblr`-capable workflow,
- the roundtrip/source table has rule structure that benefits from the dedicated renderer path.

### Recommend preview almost always when

- the table is intended for publication,
- the user is changing backend/theme/colspec,
- the task involves debugging table layout,
- the task depends on compile-time package correctness.

## 13. Failure triage order

When the generated table is wrong, debug in this order:

1. check theme/backend choice,
2. inspect `render(...)` inputs (`TableData`, colspec, span settings),
3. run preview/compile,
4. inspect missing package or backend-specific compile issues,
5. only then move into manuscript-level integration debugging.

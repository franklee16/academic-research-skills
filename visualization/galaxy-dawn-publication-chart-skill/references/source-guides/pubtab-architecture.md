# pubtab architecture (source-driven)

This guide explains `pubtab` from the actual package layout under `pubtab/src/pubtab`.

Core files:

- `__init__.py`
- `cli.py`
- `models.py`
- `reader.py`
- `renderer.py`
- `config.py`
- `_preview.py`
- `tex_reader.py`
- `backends/`
- `themes/`

## 1. Start at `pubtab.__init__`

The public contract is defined in `__init__.py`.

Public exports are intentionally small:

- `xlsx2tex`
- `preview`
- `compile_pdf`
- `tex_to_excel`
- `SpacingConfig`

This is the key architectural signal: `pubtab` exposes a compact API, while the real complexity is pushed into reader/renderer/preview internals.

## 2. Core data model layer

`models.py` defines the structured table representation.

Important dataclasses:

- `CellStyle`
- `Cell`
- `TableData`
- `SpacingConfig`
- `ThemeConfig`
- `BackendConfig`

Source fact:

- the shared structured representation is `TableData`, not raw Excel cells or raw LaTeX text.

Forward and reverse conversions both pass through this structured table model.

## 3. Forward pipeline: Excel to LaTeX

The main forward path is:

1. `xlsx2tex(...)` in `__init__.py`
2. `read_excel(...)` in `reader.py`
3. `render(...)` in `renderer.py`
4. optional preview through `_preview.py`

This gives a clean source-driven decomposition:

- `reader.py` = file ingestion and structure recovery
- `renderer.py` = LaTeX generation
- `_preview.py` = compile and raster preview

## 4. Reverse pipeline: LaTeX to Excel

The reverse path is:

1. `tex_to_excel(...)` in `__init__.py`
2. `read_tex_multi(...)` from `tex_reader.py`
3. writer functions to `.xlsx`

So roundtrip support is not an afterthought. It is a real architecture branch.

## 5. `reader.py` is richer than a plain spreadsheet loader

From the source, `reader.py` does much more than “read cells”:

- supports `.xlsx` and `.xls`
- extracts rich text segments
- reconstructs merged cells and spans
- reads styling information
- trims only trailing globally empty columns
- reads pubtab metadata sheets
- restores group separators, multicolumn alignment hints, and math-script hints

Interpretation from source:

- `pubtab` is optimized for **publication table semantics**, rather than for plain tabular text dumping.

## 6. `renderer.py` is the central logic hub

`renderer.py` turns `TableData` into backend-specific LaTeX.

From the source, it handles:

- style/theme loading
- backend template loading
- spacing resolution
- column spec construction or projection
- tabular vs tabularray differences
- merged cells, row/column spans, header rules, vertical rules
- background colors and grouped separators
- final template rendering

This file is where most of the difficult publication logic lives.

For skill design, that means:

- backend choice is not a cosmetic toggle
- column spec and rule behavior are structural concerns
- preview/render bugs usually require reading `renderer.py`

## 7. Theme vs backend is a real split

The codebase separates:

- **themes** in `themes/`
- **LaTeX backends** in `backends/`

That is reflected in two dataclasses:

- `ThemeConfig`
- `BackendConfig`

And in two loaders:

- `load_theme(...)`
- `load_backend(...)`

This is a major architectural point for the skill:

- theme decides stylistic defaults,
- backend decides LaTeX environment/template behavior.

Do not explain them as if they were the same thing.

## 8. Config precedence is explicit

In `xlsx2tex(...)`, the source implements a clear precedence order:

1. hardcoded defaults
2. YAML config loaded by `config.py`
3. explicit function kwargs
4. in some roundtrip cases, values recovered from `TableData`

This is why user-facing guidance should say “CLI flags or function kwargs override YAML config.”

## 9. Multi-file and multi-sheet support are first-class

From `__init__.py`:

- directory input is supported for both forward and reverse paths
- sheet enumeration is supported when `sheet=None`
- multi-sheet export produces `*_sheetNN.tex`

The default skill guidance can therefore recommend batch/file-driven workflows, not only one-table-at-a-time usage.

## 10. Preview is a real compilation layer

`preview(...)` and `compile_pdf(...)` in `__init__.py` delegate into `_preview.py`.

That layer:

- finds or installs `pdflatex`
- builds a standalone document
- compiles the output
- retries missing packages through `tlmgr`
- converts PDF to PNG when requested

Preview is not a fake HTML-like snapshot. It is a real LaTeX compile pipeline.

## 11. `tex_reader.py` closes the roundtrip loop

`tex_reader.py` is substantial, not decorative.

From the source it supports parsing of:

- `tabular`
- `tblr`
- `longtblr`
- `talltblr`

It also handles:

- color parsing
- rule parsing
- multirow/multicolumn reconstruction
- metadata extraction
- grouped rows and placeholder cleanup

This makes `pubtab` suitable for source-aware roundtrip and migration tasks, rather than only one-way Excel export.

## 12. Reading order for source debugging

When you need source-level certainty, use this order:

1. `pubtab/src/pubtab/__init__.py`
2. `pubtab/src/pubtab/models.py`
3. `pubtab/src/pubtab/reader.py`
4. `pubtab/src/pubtab/renderer.py`
5. `pubtab/src/pubtab/_preview.py`
6. `pubtab/src/pubtab/tex_reader.py`
7. `pubtab/src/pubtab/backends/` and `themes/`
8. `pubtab/src/pubtab/cli.py` for flag-to-API mapping only

## 13. Implications for this skill

The source says the most faithful default workflow is:

- use `xlsx2tex(...)` or CLI `xlsx2tex` for forward generation,
- use `preview(...)` to verify actual compile output,
- use `tex_to_excel(...)` for roundtrip or migration tasks,
- explain theme/backend separately,
- escalate into renderer/source debugging only when table structure or LaTeX behavior is the real problem.

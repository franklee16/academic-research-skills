# pubtab CLI and API flow (source-driven)

This guide follows the actual control flow from `pubtab/src/pubtab/cli.py` into the public API and then into the internal pipeline.

## 1. Architectural headline

`cli.py` is a **thin Click wrapper** over the public API in `pubtab.__init__`.

Operational implication:

- command-line behavior should usually match Python API behavior,
- when docs disagree, the source of truth is `pubtab.__init__`, not CLI help text alone.

## 2. CLI commands exposed in `cli.py`

The main commands are:

- `pubtab xlsx2tex`
- `pubtab themes`
- `pubtab tex2xlsx`
- `pubtab preview`

There is also a hidden backward-compatible alias:

- `convert` -> `xlsx2tex`

## 3. `xlsx2tex` command flow

CLI entrypoint:

- `xlsx2tex_cmd(...)` in `cli.py`

Control flow:

1. validate input/output shape
2. coerce `--sheet` into int when possible
3. build kwargs only for explicitly provided options
4. call `pubtab.xlsx2tex(input_file, output, **kwargs)`
5. print output summary based on sheet count and preview mode

This thin-wrapper design matters because the CLI does **not** reimplement conversion logic.

## 4. `xlsx2tex(...)` API flow

The public API in `__init__.py` adds the real orchestration:

### Input modes

- single Excel file
- directory of Excel files
- single sheet
- all sheets (`sheet=None`)

### Output path behavior

- single-sheet export can target a direct `.tex` path
- directory input must target a directory
- multi-sheet export uses `*_sheetNN.tex`

This behavior is implemented by `_build_sheet_output_paths(...)` and directory iteration helpers.

## 5. Config precedence in the real API

Inside `xlsx2tex(...)`, the source builds parameters in this order:

1. defaults
2. YAML config via `load_config(...)`
3. explicit kwargs passed from CLI or Python
4. roundtrip-restored values where relevant

Operational rule:

- YAML config sets baseline behavior,
- CLI flags / Python kwargs override it.

## 6. Sheet expansion behavior

When `sheet is None`, the source does not simply choose the first sheet.
It calls `list_excel_sheets(...)` and expands all sheet names into separate outputs.

That is why a single workbook can generate:

- `table_sheet01.tex`
- `table_sheet02.tex`
- ...

The skill should explicitly mention this when users want appendix exports or workbook-wide conversion.

## 7. Read -> render -> write flow

For each selected sheet, `xlsx2tex(...)` does:

1. `read_excel(...)`
2. optional header or group-separator reconstruction
3. `render(...)`
4. write `.tex`
5. optional preview generation to `.png`

Preview is downstream of actual `.tex` generation, not an alternate renderer.

## 8. `preview` command flow

CLI entrypoint:

- `preview_cmd(...)`

The CLI again mostly validates paths and forwards to `pubtab.preview(...)`.

The public `preview(...)` API supports:

- raw LaTeX content
- a single `.tex` file
- a directory of `.tex` files
- `png` or `pdf` output

A key source detail: when backend is omitted, `preview(...)` may infer it from the LaTeX content using `_resolve_preview_inputs(...)`.

## 9. Backend inference path

`_infer_latex_backend(...)` checks for environments like:

- `tblr`
- `longtblr`
- `talltblr`

If found, backend becomes `tabularray`; otherwise `tabular`.

Operational implication:

- a preview or compile call can often resolve the correct backend without requiring an explicit `--latex-backend` flag.

## 10. `compile_pdf(...)` API flow

Public `compile_pdf(...)` in `__init__.py` does:

1. detect whether input is raw LaTeX or a file path,
2. infer theme/backend if needed,
3. delegate to `_preview.compile_pdf(...)`.

The compile path is still part of the public API, even though the heavy lifting is in `_preview.py`.

## 11. `tex2xlsx` command flow

CLI entrypoint:

- `tex2xlsx(...)` in `cli.py`

It forwards to `pubtab.tex_to_excel(...)`.

The public API then handles:

- single `.tex` file -> one `.xlsx`
- multi-table `.tex` -> one workbook with multiple sheets
- directory of `.tex` files -> one `.xlsx` per file

This keeps the reverse path operationally symmetric with the forward path.

## 12. Why the CLI should stay thin in this skill

Because the real logic is centralized in `pubtab.__init__`, the skill should:

- use CLI examples for file-driven shell workflows,
- use Python API examples for notebooks or scripted pipelines,
- avoid duplicating pseudo-logic that already exists in the library.

## 13. Recommended source-faithful routing

### Use CLI when

- the user already has Excel or `.tex` files on disk,
- the task is batch conversion,
- the user wants a terminal-first workflow.

### Use Python API when

- the user is in a notebook or script,
- the table needs custom preprocessing before render,
- the agent is composing a larger Python pipeline.

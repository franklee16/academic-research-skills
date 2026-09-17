# pubtab Recipes

`pubtab` is the default engine for publication-ready tables.

## Core routes

### Excel to LaTeX

```bash
pubtab xlsx2tex results.xlsx -o results.tex
```

### LaTeX to Excel

```bash
pubtab tex2xlsx tables.tex -o tables.xlsx
```

### Preview

```bash
pubtab preview results.tex -o results.png --dpi 300
pubtab preview results.tex --format pdf -o results.pdf
```

## Python route

```python
import pubtab

pubtab.xlsx2tex("results.xlsx", output="results.tex", theme="three_line")
pubtab.preview("results.tex", output="results.png", dpi=300)
```

## Route selection rule

Prefer the **CLI** when:

- the user already speaks in files,
- the source is Excel or `.tex`,
- the main need is export and preview.

Prefer the **Python API** when:

- the task already lives inside a notebook or script,
- the table generation is part of a larger reproducible pipeline.

## Current practical notes

- `xlsx2tex` exports **all sheets by default** when `--sheet` is not set.
- `preview` can render **PNG or PDF**.
- `--latex-backend tabularray` is useful only when the manuscript/backend really requires `tblr`.
- `preview` can auto-detect `tblr`, but explicit backend override is still fine when needed.
- for a robust preview-first workflow, preview the table body first and add the final `caption` / `label` in the manuscript or in a final non-preview export step when needed.

## When to use `tabularray`

Use `--latex-backend tabularray` when:

- the user explicitly wants `tblr`,
- the manuscript already uses `tabularray`,
- or the backend must match an existing paper template.

Example:

```bash
pubtab xlsx2tex results.xlsx -o results_tblr.tex --theme three_line --latex-backend tabularray
```

## Common publication controls

Use these when they are justified:

- `--caption`
- `--label`
- `--span-columns`
- `--preview`
- `--latex-backend`
- `--sheet`
- `--with-resizebox`
- `--without-resizebox`
- `--resizebox-width`

## Default guidance

- start with the smallest `xlsx2tex` route,
- preview before treating the table as final,
- use a publication table when exact values matter more than quick pattern perception,
- keep figure and table roles distinct in mixed deliverables.

## Minimal recipe patterns

### Benchmark table from Excel

```bash
pubtab xlsx2tex benchmark.xlsx -o benchmark.tex --caption "Main benchmark results." --label "tab:benchmark"
```

### Two-column table

```bash
pubtab xlsx2tex benchmark.xlsx -o benchmark.tex --span-columns
```

### Preview before submission

```bash
pubtab xlsx2tex benchmark.xlsx -o benchmark_preview.tex
pubtab preview benchmark_preview.tex -o benchmark.png --dpi 300
```

Use this route when the immediate goal is a reliable visual check of the table body.
Keep `caption` / `label` as a separate manuscript-facing step if the preview is the main verification target.

### Final manuscript-facing export

```bash
pubtab xlsx2tex benchmark.xlsx -o benchmark.tex --caption "Main benchmark results." --label "tab:benchmark"
```

### All-sheets export

```bash
pubtab xlsx2tex benchmark.xlsx -o out/benchmark.tex
```

### Native file-pipeline batch roundtrip

```bash
pubtab tex2xlsx ./tables_tex -o ./out/xlsx
pubtab xlsx2tex ./out/xlsx -o ./out/tex
pubtab preview ./out/tex -o ./out/png --format png --dpi 300
```

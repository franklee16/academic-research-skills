# DOCX Workflow

This reference is a long-term skill resource for Word, OMML, rendering, and QA work for econometric research papers, course reports, and economics/management empirical documents.

## Formula Strategy

Generate or edit formulas as Word-native OMML/OOXML inside the `.docx` using the following workflow:

1. Generate or edit formulas as Word-native OMML/OOXML inside the `.docx`.
2. Preserve existing document structure, tables, figures, references, and styles.
3. Save as a new formal version unless the user explicitly asks to overwrite.
4. Render the `.docx` and inspect pages before delivery.
5. Clean temporary scripts and render outputs.

## OMML Checks

When formulas are in scope:

- Count `<m:oMath` before and after.
- Ensure inline formulas are not converted to plain Unicode when Word-native math is required.
- Check common course-report inline formulas carefully: summations, lag operators, unit-root statistics, VAR coefficient matrices, fixed effects restrictions, kernel weights, bandwidth rates, time-varying coefficients such as `β(t)` or `β(τ)`, and panel constraints such as `Σ_i α_i = 0`.
- Use `≤` and `∈` rather than ASCII-only `<=` and `in` when rendering math in final prose/formulas.
- Avoid OMML `m:nary` structures with an empty operand; Word shows these as empty square placeholder boxes.
- If using a summation with limits, either provide the operand correctly or use a scripted `∑` formula object that renders without empty boxes.

## Style and Layout Checks

After document edits:

- Confirm headings are black, not Word's default blue heading color.
- Preserve Times New Roman or the existing course-paper font pattern unless the user specifies otherwise.
- Use three-line tables as the default for economics/management papers and course reports: top rule, header-bottom rule, and bottom rule only; no vertical borders and no full grid lines unless the user explicitly requests grid tables or the source document already requires them.
- For regression tables, summary-statistics tables, robustness tables, and method-comparison tables, keep notes below the table rather than adding extra boxed rows when possible.
- For tables and figures, follow `tables-figures-style.md`: self-contained captions/legends, readable figure labels, source notes after other notes, and text callouts before or near each object.
- Keep figure data colors when they carry meaning; only title/labels should be normalized if color is a formatting problem.
- If numeric citations or note markers are required, use true Word superscript runs (`w:vertAlign w:val="superscript"`), not plain text markers such as `[1]`, `^1`, or Unicode superscript as the main representation.
- Confirm page count when prior versions had a known count, especially the 9-page versions.
- Check no blank pages, clipped equations, overflowed tables, missing captions, or broken references.

## Citation And Reference Checks

When citations are in scope:

- Follow `literature-citation-workflow.md` before adding or formatting references.
- Verify reference metadata before including it in the final reference list.
- Confirm every in-text citation has a reference-list entry and every reference-list entry is cited.
- For Word superscript citations, run `scripts/check_docx_integrity.py` and confirm `superscript_run_count` is positive when superscript markers are expected.
- Inspect `plain_numeric_citation_markers_preview`; if it contains citation markers that should be superscript, revise the document.

## Rendering

Use the available document rendering toolchain when layout matters. Prefer the skill wrapper because it can use a configured Python runtime and prepend configured native binaries:

```bash
python3 scripts/render_validate_docx.py output.docx --output-dir .qa/econ_docx_render
```

The wrapper discovers the `documents` renderer at runtime. It checks `DOCX_RENDER_SCRIPT` or `DOCUMENTS_RENDER_SCRIPT`, then searches directories listed in `DOCUMENTS_SKILL_ROOT` or `DOCUMENT_RENDERER_SEARCH_ROOTS`.

Render outputs are temporary QA artifacts. Put them in a clearly temporary working directory such as `.qa/econ_docx_render` and remove them after inspection unless the user asks to keep them.

## DOCX Builder Options

`scripts/build_paper_docx.py` preserves a supplied template's styles by default. Use `--apply-default-style` only when the output should override the template with the built-in Times New Roman paper layout.

For tables with spanned headers or grouped categories, table specs may include `header_merges` or `merges` supporting both horizontal and vertical merges:

- **Horizontal Merge (Row-based)**:
  `{"row": 0, "start_col": 1, "end_col": 2}` or list `[row, start_col, end_col]`.
- **Vertical Merge (Column-based)**:
  `{"col": 0, "start_row": 1, "end_row": 3}` or list `[col, start_row, end_row, "vertical"]`.

```json
{
  "type": "table",
  "caption": "Table 2. Baseline estimates",
  "rows": [
    ["", "Outcome A", "", "Outcome B", ""],
    ["", "(1)", "(2)", "(3)", "(4)"]
  ],
  "header_merges": [
    {"row": 0, "start_col": 1, "end_col": 2},
    {"row": 0, "start_col": 3, "end_col": 4}
  ]
}
```

Any cell text containing math indicators (such as `_`, `^`, or Greek letter names like `beta`, `alpha`) is automatically rendered as an inline Word OMML equation instead of plain text, enabling mathematical notation inside table cells.

Three-line formatting remains the default unless `style` is explicitly set to `grid`.

## File Status Language

In final responses after document generation or cleanup, explicitly state:

- Which file is the final authoritative version.
- Which files are formal archives.
- Which files were temporary and were removed.
- Which reproducibility materials were intentionally kept.

Examples:

- A file named `*_final.docx` or explicitly selected by the user is a final authoritative version.
- A version named `*_OMML.docx`, `*_style_revised.docx`, or `*_method_revised.docx` can be a formal archive if it marks a meaningful version boundary.
- Scratch scripts, render folders, temporary PDFs/PNGs, smoke-test documents, and Word lock files are temporary.

## Independent Agent Pattern

Independent agents can be useful for:

- Review-only academic critique.
- Method-fit review against the lecture scope.
- Style tightening without changing data, tables, figures, references, or formulas.
- Main-thread QA after a worker edits the document.

When using a worker or subagent, pass raw task constraints and file paths. Do not pass hidden conclusions unless they are explicit user requirements. Main thread should still verify formula counts, table/figure preservation, citation marker styling, reference integrity, rendering, and cleanup before final delivery.

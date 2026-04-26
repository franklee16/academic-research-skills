---
name: publication-chart-skill
description: This skill should be used when the user asks for a publication-quality scientific figure or table, wants help choosing the right chart for results, needs a paper-ready pubfig or pubtab workflow, wants a figure + companion table for a results section, wants an Excel sheet turned into publication-ready LaTeX, or wants an existing scientific figure/table reviewed and upgraded.
version: 0.2.0
---

# Publication Chart Skill

## Goal

Use this skill to turn research results into **publication-grade figures and tables** with an end-to-end workflow.

Primary production stack:

- **`pubfig`** for figures
- **`pubtab`** for publication tables

This skill covers the full delivery chain:

1. understand the scientific communication goal,
2. choose the right artifact type,
3. map the task to `pubfig`, `pubtab`, or both,
4. generate concrete runnable instructions,
5. export paper-ready assets,
6. run publication QA,
7. propose targeted revisions.

## Use this skill when

Trigger this skill for requests like:

- “make a publication-quality figure”
- “choose the right chart for these results”
- “turn these results into a paper-ready figure”
- “make a benchmark / ablation / calibration / forest / heatmap / scatter / line / bar figure”
- “make a benchmark / appendix / ablation table from Excel”
- “convert this Excel table into publication-ready LaTeX”
- “prepare one summary figure plus one companion table for the results section”
- “review and improve this scientific figure/table”
- “I already have a weak chart / screenshot / draft plot — make it publication-ready”
- “export panels for a paper figure”

## Do not use this skill for

Do **not** use this skill when the task is mainly:

- manuscript prose writing,
- statistical testing without artifact design,
- raw exploratory analysis with no publication deliverable,
- Figma-first layout work before the figure/table content is solid.

For simple composite assembly after the figure content is already strong, use the optional secondary workflow in `references/composite-assembly.md`.

## Primary contract

### Inputs

Expect some combination of:

- the scientific communication goal,
- available data shape,
- venue or style constraints,
- whether the artifact is a figure, table, or mixed deliverable,
- optional existing assets such as code, spreadsheets, `.tex`, screenshots, or draft plots,
- whether the user needs a first draft, a publication-ready artifact, or a review/revision pass.

### Outputs

The minimum useful output is:

- the recommended figure/table form,
- the recommended `pubfig` / `pubtab` route,
- a minimal runnable code snippet or CLI command,
- explicit export filenames and formats,
- a publication QA summary,
- and, when needed, a revision plan.

## Default workflow

### 0. Probe the environment and artifact state

Before generating anything, identify:

- whether `pubfig` or `pubtab` is actually available,
- whether the user already has code / spreadsheets / `.tex` / screenshots,
- whether the deliverable is a fresh build or a revision,
- whether the result needs exact values, fast visual perception, or both.

Prefer the smallest environment check that helps execution. When the bundled helper script is available, use it first:

- `python3 scripts/ensure_publication_tooling.py --require pubfig --json`
- `python3 scripts/ensure_publication_tooling.py --require pubtab --json`

Equivalent manual checks are still acceptable when needed:

- `python -c "import pubfig; print(pubfig.__version__)"`
- `python -c "import pubtab; print(pubtab.__version__)"`
- `pubtab --help`

Report the result clearly as **available** or **missing**.

If a dependency is missing and the task requires runnable execution:

- **auto-install it by default**,
- prefer the user’s active environment instead of guessing a random global interpreter,
- use `python3 scripts/ensure_publication_tooling.py --require ...` as the default bundled route when the script is present,
- let that helper choose `uv` vs `python -m pip` against the active interpreter,
- re-run the availability probe after installation,
- and only then continue with the artifact workflow.

Equivalent concrete commands include:

- `python3 scripts/ensure_publication_tooling.py --require pubfig`
- `python3 scripts/ensure_publication_tooling.py --require pubtab`
- `uv pip install pubfig`
- `uv pip install pubtab`
- `python -m pip install pubfig`
- `python -m pip install pubtab`

If auto-install fails, report the exact failure and then degrade gracefully.

Do not block on a full environment audit.

### 1. Classify the task

Classify the request along these axes:

- **artifact type**: figure / table / mixed deliverable
- **maturity**: exploratory draft / publication-ready generation / revision of an existing artifact
- **structure**: single panel / multi-panel / figure-plus-table package
- **evidence mode**: pattern perception / exact value lookup / both

Do not jump into plotting code before the communication target is clear.

### 2. Choose the representation

Choose the representation based on the scientific claim, not novelty or visual flair.

Common families:

- **comparison** — grouped scatter, bar, line comparison, benchmark summary, companion table
- **ablation** — grouped comparison, dumbbell, paired comparison, compact table
- **distribution** — box, violin, raincloud, histogram, density, ECDF, QQ
- **relationship** — scatter, bubble, contour2d, hexbin
- **trend** — line, area
- **evaluation / diagnostic** — calibration, ROC, PR, Bland–Altman, forest plot, volcano
- **composition / hierarchy** — UpSet, stacked ratio, donut, radial hierarchy, circular grouped or stacked bars
- **table** — benchmark table, ablation table, dataset summary, appendix table, error breakdown

Avoid weak defaults:

- avoid pie/donut when exact comparison matters and a bar/table is clearer,
- avoid radar unless the comparison is genuinely profile-like and low-cardinality,
- avoid 3D, decorative gradients, and dense legends used only for style,
- avoid forcing every result into a figure when a publication table communicates the evidence better.

If the request is ambiguous, explicitly state what scientific claim the artifact is supposed to support.

### 3. Map to the toolchain

Default mapping:

- **Figures** → `pubfig`
- **Tables** → `pubtab`
- **Mixed deliverables** → use both, with each artifact carrying a distinct role

Tool roles:

- `pubfig` is the default figure engine for scientific plots and paper-ready export.
- `pubtab` is the default table engine for Excel ↔ LaTeX workflows, preview, and publication-ready table export.
- Figma/composite assembly is an **optional secondary branch** for multi-panel finishing.

Route selection rules:

- prefer **Python** for `pubfig` figure generation,
- prefer **CLI** for `pubtab` when the task is file-driven,
- prefer **Python** for `pubtab` when the task is already inside a notebook or scripted pipeline,
- keep the figure and table responsibilities separate in mixed requests.

### 4. Generate concrete artifact instructions

Prefer the smallest production-ready artifact first:

- minimal runnable Python for `pubfig`, or
- minimal CLI/Python for `pubtab`

Then add publication parameters only when justified:

- labels, caption, width, export format, backend, preview, panel packaging, or composite layout.

Keep filenames and suffixes explicit.

Good defaults:

- figures: one `pubfig` call + one `save_figure(...)`
- multiple figure outputs: `batch_export(...)`
- tables: one `pubtab xlsx2tex ...` or `pubtab.preview ...`
- mixed requests: one figure route + one table route, clearly separated

### 5. Define the delivery contract

For every response, make these explicit when possible:

- the claim the artifact supports,
- which part is handled by `pubfig` and which by `pubtab`,
- the output filenames,
- the output formats,
- whether the artifact is draft / final / revision,
- what still needs user-provided data or manuscript context.

### 6. Run publication QA

After generation, check:

- title and legend density,
- axis labels and units,
- category ordering and baseline clarity,
- color accessibility and grayscale robustness,
- font / line-weight consistency,
- caption readiness,
- figure/table readability after downscaling,
- panel consistency for multi-panel figures,
- venue-fit issues such as width, crowding, or over-annotation.

The QA output must be concrete. Do not say “looks better” without naming why.

### 7. Revise

If the result is weak, revise with specific changes such as:

- switch chart family,
- remove chartjunk,
- reorder categories,
- move exact values into a table,
- split a crowded panel,
- add or simplify the caption,
- change export width,
- or convert the deliverable from figure-first to table-first.

## Missing dependency behavior

If `pubfig` or `pubtab` is not available:

- do **not** fail immediately,
- first attempt automatic installation into the active environment,
- prefer `python3 scripts/ensure_publication_tooling.py --require ...` when the bundled script exists,
- explicitly state which dependency is missing,
- state which install command or helper route is being used,
- re-check availability after installation,
- if installation succeeds, continue with the runnable workflow,
- if installation fails, degrade to a design/specification workflow,
- provide pseudocode or draft commands,
- preserve the recommended figure/table structure,
- still provide QA and revision guidance.

## Composite assembly rule

Treat composite or Figma assembly as **secondary**:

- use it when the user explicitly wants a multi-panel paper figure,
- or when panel-level export and layout polishing are genuinely needed.

Do not escalate simple figure tasks into composite/Figma workflows by default.

## Output style rules

- Prefer direct, implementation-usable outputs.
- Explain the **why** of chart/table choice briefly, then give the runnable route.
- When execution matters, include a short environment status block such as `pubfig: available/missing`, `pubtab: available/missing`.
- If a dependency is missing, state the exact helper command or install command, perform the installation, and report the post-install status.
- When a table is stronger than a figure, say so explicitly.
- When a figure is stronger than a table, say so explicitly.
- When both are needed, assign them different communication roles.
- Keep revision guidance actionable and falsifiable.

## Recommended response shape

A strong response using this skill usually has 6 parts:

1. **Artifact decision** — figure / table / paired deliverable, and why
2. **Tool route** — `pubfig`, `pubtab`, or both
3. **Minimal implementation** — runnable code or CLI
4. **Export plan** — filenames, formats, width/backend/preview choices
5. **Publication QA** — what to verify before paper submission
6. **Revision plan** — what to change if the current artifact is weak

## Resources

Load these as needed:

- `references/workflow.md` — full end-to-end decision order and delivery contract
- `references/chart-selection.md` — task-to-chart mapping and anti-patterns
- `references/execution-and-verification.md` — environment probing, forced install behavior, and runnable verification
- `scripts/ensure_publication_tooling.py` — bundled probe + auto-install helper for `pubfig` / `pubtab`
- `references/pubfig-recipes.md` — shortest useful figure patterns and export routes
- `references/pubtab-recipes.md` — shortest useful table routes and backend guidance
- `references/source-guides/pubfig-architecture.md` — package layout and figure-generation boundaries from source
- `references/source-guides/pubfig-api-map.md` — stable public pubfig surface and chart-family map from `__init__.py`
- `references/source-guides/pubfig-export-flow.md` — figure export, publication sizing, and panel-export flow from source
- `references/source-guides/pubtab-architecture.md` — package layout and forward/reverse conversion architecture from source
- `references/source-guides/pubtab-cli-api-flow.md` — CLI-to-API control flow and batch/sheet behavior from source
- `references/source-guides/pubtab-backend-and-preview.md` — backend/theme split and real preview compile pipeline from source
- `references/publication-qa-checklist.md` — figure/table QA checklist
- `references/composite-assembly.md` — optional multi-panel and Figma branch

For prompt-shaped examples, see `examples/`.

# Composite Assembly

## Principle

Composite assembly is a **secondary branch**, not the default workflow.

Use it when:

- the user explicitly wants a multi-panel paper figure,
- panel-level maintenance matters,
- or the final paper figure needs finishing beyond a single exported plot.

## Default stance

- Single-panel figure → stay in `pubfig` normal export mode.
- Multi-panel figure with real assembly needs → use panel/composite export.
- Figma is optional and should not be introduced unless it solves a real assembly problem.

## pubfig routes

Relevant `pubfig` capabilities:

- `export_panel(...)`
- `export_panels(...)`
- `batch_export(...)`
- `save_figure(...)`

If the environment already uses a pubfig/Figma bridge workflow, keep `figure_id` stable across revisions.

## Practical rule

Escalate to composite assembly only after the panel content itself is strong.

Do not use Figma/composite assembly to hide weak chart choice, poor labels, or overloaded panels.

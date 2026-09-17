# Research Workflows

Use these workflows when the user needs research decisions, writing support, or project transfer rather than a plain paper summary. Default output is Markdown in the conversation. Save as `.md` only when the user asks for a file.

## Paper Scorecard

Use `paper_scorecard` when the user asks whether a paper is worth reading, citing, reproducing, or building on.

Score from 1 to 5 and include a one-sentence rationale for each score.

| Dimension | Score | Rationale |
|---|---:|---|
| Novelty |  | Is the contribution genuinely new relative to closest prior work? |
| Evidence |  | Do experiments, theory, or analysis support the claims? |
| Reproducibility |  | Are code, data, settings, and metrics available enough to reproduce? |
| Transferability |  | Can the idea transfer to the user's project, task, or domain? |
| Risk |  | Are there serious threats: weak baselines, leakage, bias, cost, or unclear assumptions? |
| Reading Priority |  | Should the user skim, read carefully, reproduce, or skip? |

End with:

```text
Decision: skim / read deeply / cite carefully / reproduce / build on / skip
Why:
Next action:
```

## Related Work Draft

Use `related_work_draft` when the user asks for related work paragraphs, literature positioning, or paper-writing support.

Choose the organization that best fits the evidence:

- Timeline: how the field evolved.
- Method family: group by RNN, Transformer, GNN, retrieval, diffusion, etc.
- Problem evolution: from task definition to limitations to current gap.
- Motivation gap: prior work solved X, but left Y unresolved; the target paper addresses Y.
- Dataset/benchmark: organize around evaluation settings.

Before drafting, build a compact evidence map:

| Paper | Role | Key idea | Limitation or gap | Link to target work |
|---|---|---|---|---|

Then draft 1-3 cohesive paragraphs. Keep claims citation-grounded. Do not overstate the target paper's novelty.

## Idea Incubator

Use `idea_incubator` when the user asks for research directions, thesis ideas, experiments, or "what can I do next?"

Generate a small portfolio instead of a long list:

| Type | Direction | Hypothesis | Minimal experiment | Expected positive signal | Negative result meaning | Cost | Risk |
|---|---|---|---|---|---|---|---|
| Low-cost experiment |  |  |  |  |  | low/med/high | low/med/high |
| Workshop-scale idea |  |  |  |  |  | low/med/high | low/med/high |
| Main-paper direction |  |  |  |  |  | low/med/high | low/med/high |
| High-risk/high-reward |  |  |  |  |  | low/med/high | low/med/high |

For each direction, also include:

- Nearest baselines.
- Required datasets or artifacts.
- One possible title.
- Why it is not just an incremental ablation.

Avoid directions whose only value is filling a table. Stop when additional ideas have low marginal information gain.

## Paper-to-Project

Use `paper_to_project` when the user wants to adapt a paper into their repository, model, dataset, or experiment plan.

First inspect the current project only as much as needed. Do not edit code unless the user asks for implementation.

Output:

| Paper component | Reusable unit | Target project location | Adaptation needed | Risk | Minimal verification |
|---|---|---|---|---|---|
| Method / loss / metric / preprocessing / config / checkpoint |  |  |  |  |  |

Then provide:

```text
Recommended transfer:
Do not transfer:
Smallest useful experiment:
Success criterion:
Files likely involved:
```

Prefer reimplementing ideas or small modules over copying code unless the license and packaging are clean.

## Output Forms

Default to Markdown:

- Tables for comparison, scorecards, and experiment portfolios.
- Short sections for reading notes and recommendations.
- Prose paragraphs for related-work drafts.
- Code blocks for compact graphs, timelines, prompts, or command plans.
- `.md` files only when the user asks to save or create a reusable note.

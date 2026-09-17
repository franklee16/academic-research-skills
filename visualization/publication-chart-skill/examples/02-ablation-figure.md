# Example 2 — Ablation figure

## User-style prompt

Turn these ablation results into a paper-ready figure that makes the contribution of each module easy to read.

## Expected skill interpretation

- artifact: figure
- maturity: publication-ready generation
- structure: single panel or compact paired panel
- goal: isolate incremental effect clearly

## Preferred route

- primary tool: `pubfig`
- likely family: `dumbbell` or `paired` for low-cardinality paired ablations, otherwise a compact grouped comparison chart or companion table
- do not default to a crowded decorative chart

## Minimum acceptable output shape

- recommend the ablation-focused visual form and why
- provide runnable `pubfig` code
- export to a paper-ready format
- include a QA note on baseline clarity and ordering

# Example 1 — Benchmark comparison figure

## User-style prompt

Help me make a publication-quality benchmark comparison figure for six methods across three datasets.

## Expected skill interpretation

- artifact: figure
- maturity: publication-ready generation
- structure: single panel
- goal: fast comparison across methods and datasets

## Preferred route

- primary tool: `pubfig`
- likely family: `grouped_scatter` or `bar_scatter`
- companion table: optional, only if exact values must be preserved nearby

## Minimum acceptable output shape

- explain why the chosen comparison form is better than a raw grouped bar if density is high
- provide a minimal `pubfig` implementation
- provide one explicit export command/path such as `benchmark.pdf`
- provide a short QA note about readability, legend density, and category ordering

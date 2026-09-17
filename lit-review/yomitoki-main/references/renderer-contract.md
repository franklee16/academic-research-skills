# Renderer Contract

Use this when you are ready to fit the paper-first note into Yomitoki's HTML renderer.

Tool surfaces:

- `python3 scripts/extract.py --describe`: extractor inputs, outputs, and next steps.
- `python3 scripts/assemble.py --describe`: assembler inputs, outputs, checks, and limits.
- `python3 scripts/assemble.py --print-contract`: print this file.

## Files

The assembler expects:

- `analysis.json`: metadata, short prose blocks, tables, section manifests, figures.
- `sections/*.html`: long method or result prose, referenced by `body_html_file`.
- `coderefs.json`: side-panel implementation references.
- `figures/`: curated paper figures referenced from `analysis.json`.
- `assets/`: `styles.css` and `main.js`.

Long explanations belong in `sections/*.html`, not inside JSON strings.

## Common `analysis.json` Keys

Do not invent top-level keys. Unknown fields do not render.

| Field | Shape |
|---|---|
| `title`, `authors`, `venue`, `year` | strings / number |
| `subtitle` | one concrete sentence |
| `difficulty` | 1-5 |
| `difficulty_label` | what makes the paper hard |
| `estimated_reading_time` | e.g. `18 min` |
| `tags` | 3-6 lowercase strings |
| `prerequisites` | list of concept objects |
| `tldr` | `{"summary": "..."}` |
| `paper_overview` | `{"problem", "background", "solution", "contributions": [...]}` |
| `tech_timeline` | list of `{"year", "label", "delta", "current"}` |
| `where_this_matters` | optional `{"intro", "items": [...]}` |
| `method_subsections` | list of `{"title", "body_html_file"}` |
| `experiments_setup_summary` | string |
| `main_results` | `{"headline", "findings", "tables", "ablations"}` |
| `methods_comparison` | `{"headers", "rows", "highlight_row", "note"}` |
| `related_work` | optional `foundational`, `comparable`, `closest_with_delta` |
| `limitations` | list of `{"limit", "softening"}` |
| `use_cases`, `open_questions` | lists of strings |
| `qa` | list of `{"q", "a", "type"}` |
| `quiz` | list of `{"q", "model_answer"}` |
| `paper_figures` | list of figure objects |
| `jargon` | optional term-to-gloss object |

For missing table values, write `n/a`.

## Important Item Shapes

### Paper Overview

```json
"paper_overview": {
  "problem": "What breaks or costs too much?",
  "background": "What prior methods do, where they fail, and why.",
  "solution": "The paper's actual move.",
  "contributions": [
    "First concrete mechanism or artifact.",
    "Second concrete mechanism or result."
  ]
}
```

`contributions` must be a list of strings, not one long string.

### Prerequisites

```json
{
  "term": "Backpropagation through computational graphs",
  "brief": "Reverse-mode autodiff: accumulate gradients backward through a recorded graph.",
  "beginner_link": "https://colah.github.io/posts/2015-08-Backprop/",
  "beginner_title": "Calculus on Computational Graphs: Backpropagation (Christopher Olah)",
  "primary_link": "https://www.nature.com/articles/323533a0",
  "primary_title": "Learning representations by back-propagating errors (Rumelhart, Hinton & Williams)"
}
```

Use real beginner-friendly links and primary links when possible.

### Method Subsections

```json
"method_subsections": [
  {"title": "Overall architecture", "body_html_file": "sections/01-architecture.html"},
  {"title": "Attention block", "body_html_file": "sections/02-attention.html"}
]
```

`body_html_file` paths are relative to `analysis.json`.

### Results

```json
"main_results": {
  "headline": "On WMT 2014 English-to-German, the big model reaches 28.4 BLEU while training faster than prior recurrent/convolutional models.",
  "findings": ["Self-attention improves BLEU while reducing sequential depth."],
  "tables": [
    {
      "caption": "Table 2 - BLEU vs training cost",
      "headers": ["Model", "BLEU", "Training cost"],
      "rows": [["Transformer big", "28.4", "2.3e19 FLOPs"]],
      "highlight_row": 0
    }
  ],
  "ablations": []
}
```

`table` singular is still accepted for one-table notes, but `tables` is clearer.

### Related Work

```json
"related_work": {
  "foundational": [{"title": "...", "authors": "...", "year": 2017, "why": "..."}],
  "comparable": [{"title": "...", "authors": "...", "year": 2018, "why": "..."}],
  "closest_with_delta": {"title": "...", "year": 2018, "key_delta": "..."}
}
```

Use `key_delta`, not `delta`, inside `closest_with_delta`.

### Figures

```json
{
  "id": "model-architecture",
  "src": "03-architecture-transformer-stack.png",
  "caption": "Figure 1 - Transformer model architecture. <strong>Shows</strong>: encoder and decoder stacks with attention, feed-forward layers, residual paths, and normalization. <strong>From paper</strong>: §3.",
  "anchor_section": "architecture"
}
```

Figure rules:

- Captions include `<strong>Shows</strong>` and `<strong>From paper</strong>`.
- `anchor_section` is one of: `header`, `overview`, `motivation`, `architecture`, `method`, `experiments`, `comparison`, `related`, `limits`, `inline`.
- Use `anchor_section: "architecture"` for the overall architecture figure.
- Method figures use `anchor_phrase` copied from nearby prose.

### Q&A and Quiz

```json
"qa": [
  {"q": "Why does the scaling term matter?", "a": "Without scaling, dot products grow with width...", "type": "principle"}
],
"quiz": [
  {"q": "What changes if the sequence length doubles?", "model_answer": "The attention matrix grows quadratically."}
]
```

Q&A keys are `q` and `a`. Quiz keys are `q` and `model_answer`.

## Code Refs

Save `coderefs.json` as:

```json
{"refs": [
  {
    "section": "method",
    "source": "author_repo",
    "title": "Scaled dot-product attention forward pass",
    "repo": "owner/repo",
    "path": "model.py",
    "url": "https://github.com/owner/repo/blob/main/model.py#L10-L40",
    "anchor_phrase": "scores every query against every key",
    "snippet": "# shape preview; see linked lines for exact implementation\n...",
    "note": "Line range matching the paper's attention equation."
  }
]}
```

Valid `section` IDs:

`tldr`, `overview`, `timeline`, `context`, `method`, `experiments`, `comparison`, `related`, `limits`, `qa`, `quiz`

For sourcing rules, read `references/code-ref-waterfall.md`.

## Prose and Math

- JSON prose may use `<strong>`, `<em>`, `<code>`, `<b>`, `<i>`.
- Avoid authored em-dashes; `--check` treats them as failures.
- Use KaTeX for math: inline `\(x_i\)`, display `\[ ... \]`.
- Do not put math in `<code>`; KaTeX does not render inside code blocks.
- After a display equation, explain the symbols in prose.

## Assemble

```bash
python3 scripts/assemble.py \
  --analysis /tmp/yomitoki/<slug>/analysis.json \
  --coderefs /tmp/yomitoki/<slug>/coderefs.json \
  --figures /tmp/yomitoki/<slug>/figures/ \
  --assets assets \
  --out ./yomitoki-out/<slug>/ \
  --check --strict
```

Use `--check` while drafting. Use `--check --strict` before shipping.

`--strict` upgrades code-ref quality warnings to failures:

- method refs without `anchor_phrase`
- `author_repo` refs without GitHub line ranges
- `author_repo` refs without snippets

`--check` validates structure, not paper coverage or prose quality.

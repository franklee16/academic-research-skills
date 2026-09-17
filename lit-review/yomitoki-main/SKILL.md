---
name: yomitoki
description: "Turn a research paper into a faithful, technical, code-augmented HTML reading note."
---

## First-Run Welcome

When invoked without a paper:

> **I turn dense research papers into clear, technical HTML study notes.**
>
> Send an arXiv link, arXiv ID, PDF path, PDF URL, or paper title.

If given only a title or natural-language description, search arXiv and confirm the match before proceeding.

## Core Goal

Create a self-contained reading note that helps a technical reader answer:

1. **Why did this paper need to exist?**
2. **What exactly is the move the paper makes?**
3. **Why does that move work?**
4. **Where does it win, by how much, and where does it stop winning?**
5. **How would I start implementing or verifying it?**

The output is HTML, but the job is not to fill an HTML template. The job is to make the paper understandable.

The note must be:

- **Complete**: cover the core technical details and explain the actual contribution.
- **Accurate**: grounded in the paper, with no unsupported claims.
- **Readable**: calm technical-blog voice, deep but easy to follow.
- **Reflective**: use analysis, Q&A, and quiz to help readers understand design choices, limits, and transfer.

## Writing Style

### Do

1. **Use precise technical language.** Match the paper's formulas, symbols, and terminology.
2. **Make hard ideas understandable.** Give intuition before formulas. Explain every important variable and symbol.
3. **Organize clearly.** Use diagrams, tables, and code only when they reduce explanation cost.
4. **Add real analysis.** Explain design choices, tradeoffs, limits, and concrete differences from prior work.

Other style rules:

- Prefer one sharp paragraph over three complete but low-signal paragraphs.
- Use concrete nouns, numbers, and mechanisms.
- Explain the hard part before cataloging components.
- Cite paper sections, figures, and tables when they help verification.
- Keep the reader moving: motivation first, detail second, caveats third.

### Avoid

1. **AI-template phrases.** Avoid "The core contribution is...", "It is worth noting...", "This has broad significance...", and similar filler.
2. **Empty evaluation.** Do not call the work important, novel, powerful, or promising without concrete evidence.
3. **Over-decoration.** No emoji in the body. Do not bold every sentence.
4. **Unneeded first person.** Avoid "I think" and "my understanding".
5. **Em-dashes.** Use periods, commas, or parentheses instead.

## Paper-First Workflow

### 1. Extract

```bash
python3 scripts/extract.py <input> --out /tmp/yomitoki/<paper-slug>/
```

Inputs: arXiv URL/ID, local PDF, or PDF URL. Outputs include `extracted.txt`, `figures/`, `figures.json`, and a skeleton `analysis.json`.

Use `python3 scripts/extract.py --describe` for the extractor's input/output contract. Do not read the script for authoring rules.

### 2. Read by Headings

Before authoring, create `/tmp/yomitoki/<paper-slug>/coverage.md`. It is the source of truth for section coverage and prevents dropped headings.

For every paper heading, decide:

- **Deep**: main algorithm, module, mechanism, proof, system component, or result.
- **Brief**: supporting definition, assumption, dataset step, training detail, implementation note, or ablation setup.
- **Mention**: housekeeping, repeated setup, or context that should be acknowledged but does not need its own explanation.

Read the local text for a heading before deciding. Token efficiency is not permission to skip unread sections. If the paper has `5.1`, `5.1.1`, and `5.1.2`, account for all three. Minor but valid subsections should become a brief paragraph, table row, or named note rather than disappearing. If a heading adds almost nothing new, still mention where it is covered or why it is folded into another note section.

Then write the five-line spine:

```text
Problem / Old way / Failure mode / Paper's move / Payoff
```

Use the spine to order and weight the note. Do not use it to erase sections you have not read.

Use this compact shape:

```text
Spine: Problem / Old way / Failure mode / Paper's move / Payoff

Contribution inventory:
| Paper heading | Decision: deep/brief/mention | Note placement | Evidence / reason |

Method plan:
| Section file | Paper headings covered | Formula/algorithm/module | Code/diagram need |

Experiment map:
| Claim | Metric / dataset / baseline | Paper table/figure | Note placement |

Coverage checklist:
| Paper heading | Present in note? | Where |
```

### 3. Write the Note

Write paper-first, then fit the result into renderer artifacts.

Required reader sections:

- Header metadata.
- Prerequisites, 3-6 concrete concepts with links.
- TL;DR, 2-3 sentences.
- Paper Overview: problem, background, solution, contributions.
- Tech Timeline: usually 4-6 verified lineage nodes with this paper marked `current`.
- Core Method.
- Experiments / Main Results.
- Methods Comparison or Related Work, whichever best explains the contrast.
- Limitations / Use Cases / Open Questions.
- Q&A and short quiz.

Optional sections:

- `where_this_matters`: for foundational primitives used in later systems.
- `jargon`: for terms a hover tooltip genuinely helps. Skip generic terms.

### 4. Fit Into Renderer Artifacts

Use the renderer contract only after the paper coverage and story are clear.

- `analysis.json`: metadata, short structured fields, tables, section manifests, figures.
- `sections/*.html`: long method or result prose.
- `coderefs.json`: code references for the right panel.
- `paper_figures`: curated figures.

Read `references/renderer-contract.md` before writing or repairing these files.
You can also run `python3 scripts/assemble.py --print-contract`.

### 5. Assemble and Review

Run:

```bash
python3 scripts/assemble.py \
  --analysis /tmp/yomitoki/<slug>/analysis.json \
  --coderefs /tmp/yomitoki/<slug>/coderefs.json \
  --figures /tmp/yomitoki/<slug>/figures/ \
  --assets assets \
  --out ./yomitoki-out/<slug>/ \
  --check --strict
```

Use `--check` while drafting. Use `--check --strict` before shipping. Fix hard failures. Review warnings and revise when they point to a real issue.

`--check` validates structure, not coverage. Before calling the note done, walk the paper headings again and confirm each covered heading appears in the note. If a stated contribution is absent, add it before shipping.

## Core Method

This is the heart of the note. Cover the method completely and deeply.

Start from the paper's own method headings. A subsection that looks minor may still carry a definition, assumption, dataset construction step, loss term, training detail, or ablation setup. Cover it briefly if it supports the method.

Organize Core Method like this:

1. **Overall architecture / data flow**
   - Show the architecture figure or a simple Mermaid schematic when the method has multiple moving parts.
   - Explain the data flow from input to output.
   - Name the key modules before diving into formulas.
2. **Core module details**
   - Input and output.
   - Core formula or algorithm, with a prose gloss for every symbol.
   - Pseudocode or code when it helps the reader implement or verify the idea.
   - Design-choice analysis: why this choice beats the obvious alternative, and what tradeoff it introduces.
3. **Key technical details**
   - Training strategy.
   - Hyperparameters.
   - Implementation tricks.
   - Inference tricks.
   - Data preprocessing.
   - Reproduction risks.

Write substantial method subsections in `sections/*.html` and reference them from `analysis.json` with `body_html_file`. Keep `analysis.json` compact.

Use "Why..." callouts for non-obvious design choices:

```html
<p><strong>Why keep this state instead of recomputing it?</strong> The state is small enough to stay local, while recomputing would scan the full input again. The tradeoff is extra update arithmetic per element.</p>
```

Good "Why..." questions name the design choice, compare it with the obvious alternative, and explain the tradeoff.

Use code when the paper defines an algorithm, recurrence, kernel, or implementation detail. A short runnable Python demo with an `assert` is useful when it clarifies the idea. Do not force code into prose-only sections.

Read `references/method-example.md` when authoring the first method section.

## Results and Comparison

Experiments are analysis, not a number dump. State the conclusions first, then use tables and figures as evidence.

For results, capture:

- **Headline**: workload, baseline, metric, magnitude, and regime.
- **Findings**: 2-5 claims, each backed by evidence.
- **Tables**: compare regimes, not every number.
- **Ablations**: explain which mechanism earned which gain.
- **Honest read**: note narrow evaluations, missing tasks, or weak evidence.

For comparison, use axes the reader would actually weigh: cost, latency, memory, path length, data needed, or parallelism. State when each method wins and where this paper's method stops winning.

## Figures and Diagrams

Use visuals when they teach. Do not add a diagram because a section feels empty.

- Paper architecture or method-flow figures belong in Core Method.
- Result plots belong in Experiments.
- Comparison diagrams belong in Comparison or Related Work.
- Mermaid is useful when the reader must track modules, tensors, stages, loop states, branches, or memory movement.

Read `references/diagrams.md` for figure curation, Mermaid syntax, and image naming.

## Code References

Code refs are implementation handles for claims in the note.

Use them when the reader would ask:

- Where is this algorithm implemented?
- What lines correspond to this formula?
- How did they measure this result?
- Is there a small runnable version I can inspect?

Prefer:

1. Exact author-repo line ranges.
2. High-quality official docs or tutorials.
3. Credible community implementations.
4. Synthesized snippets only when justified.

If an official or author-linked repo exists but you still use a synthesized snippet, say why in the ref note. Do not use synthesized code just because it is faster to write.

Read `references/code-ref-waterfall.md` before writing `coderefs.json`.

## Q&A

Q&A is the reader's self-check. Write 5-8 questions across several angles and difficulty levels. Include a question only if a reader who studied the note would still pause on it. Skip rhetorical recaps like "What is the main idea?" and anything the body already answers.

Use these types:

- `intuition` (0-1): easy gut-check. "In one line, why does this work?"
- `principle` (1-2): design rationale. "Why this choice instead of the obvious alternative?"
- `detail` (1-2): mechanical clarity. "What does this symbol, step, or module actually do?"
- `limit` (0-1): failure condition. "When does this break?"
- `engineering` (1-2): performance envelope. "How does the gain scale, what does it cost, and where does it stop winning?"
- `extension` (0-1): transfer. "Where else could this idea apply, and what would need to change?"

Answer rules:

- Do not fabricate. If the paper does not settle an answer, say what it shows and where the evidence stops.
- Show, don't assert. Use a worked example, a few lines of code, napkin math, or paper numbers when that makes the answer click.
- Mix difficulty. Readers need a few easy intuition wins, not only deep questions.
- For engineering questions, probe scaling and tradeoffs: input size, hardware, memory, latency, accuracy, extra FLOPs, or where another method wins.
- Use numbered lists when an answer has multiple reasons, conditions, or steps.

Example engineering Q&A:

```text
Q: LoRA quality depends on rank r. What sets the right r, and where does increasing r stop paying off?

A: The rank sweep shows three forces:
1. Task difficulty: simple classification saturates at low rank; harder generation needs larger r.
2. Subspace coverage: most task updates live in a few dominant directions, so small ranks often match full finetuning.
3. Cost ceiling: higher r raises finetune memory, while merged adapters do not add inference latency.

Takeaway: start small, then sweep upward only if validation quality stays below the full-finetune line.
```

## Final Self-Review

Before calling the note done, read the TL;DR, Overview, and first method subsection as a reader. Ask:

- Can the reader explain the problem and the fix in five minutes?
- Does the contrast with prior methods appear before implementation detail?
- Are the strongest numbers tied to the regime where they apply?
- Are code refs real and line-specific when a repo exists?
- Did any section become a checklist rather than an explanation?

Then walk the paper's headings in order. A heading with its own formula, algorithm, module, result, dataset step, training detail, or assumption should not disappear into a background sentence.

Update `/tmp/yomitoki/<paper-slug>/coverage.md` before finishing. The `Coverage checklist` should show where every paper heading appears or is mentioned in the note.

## Reference Files

- `references/renderer-contract.md`: JSON schemas, valid keys, figure shape, `coderefs.json`, and assemble command.
- `references/code-ref-waterfall.md`: code reference sourcing, line anchors, snippets.
- `references/diagrams.md`: figure curation and Mermaid safety.
- `references/method-example.md`: worked module deep-dive.
- `scripts/extract.py`: paper extraction.
- `scripts/assemble.py`: HTML rendering and validation.

---
name: paper-taste
description: >
  Research taste and writing quality guide for empirical finance and economics papers.
  Synthesizes advice from Nanda, Perez, Foerster, and Steinhardt, adapted for
  empirical social science. Covers narrative construction, paper structure, evidence
  rigor, writing style, figures/tables, and LaTeX conventions.
  TRIGGER when: drafting or polishing an empirical finance/economics paper; reviewing
  paper quality; evaluating claims, evidence, or narrative strength; preparing for
  journal submission; writing or editing any section of an empirical research paper.
---

# Paper Taste: Empirical Finance Writing Guide

A lightweight taste layer. Other skills (write, review, paper-editor) reference this for style and quality standards.

## Quick Reference

| Topic | File | When to Read |
|-------|------|-------------|
| Narrative and claims | [references/narrative.md](references/narrative.md) | Framing the paper, writing introduction, responding to "what's your contribution?" |
| Paper structure | [references/structure.md](references/structure.md) | Outlining or restructuring the paper |
| Evidence and rigor | [references/evidence.md](references/evidence.md) | Designing tests, writing results, responding to identification concerns |
| Writing style | [references/style.md](references/style.md) | Drafting or polishing any section; checking prose quality |
| Figures and tables | [references/figures-tables.md](references/figures-tables.md) | Creating or revising tables and figures |
| LaTeX conventions | [references/latex.md](references/latex.md) | Formatting, citations, equations, cross-references |

## Core Principles (Always Apply)

**1. Every paper is a narrative of 1-3 claims with supporting evidence.**
Not a data dump. Not a methods showcase. State claims precisely, motivate why they matter, provide rigorous evidence.

**2. Precision over complexity.**
Replace "performance" with "monthly alpha." Replace "significant" with "t = 3.41." Be specific about what you measured and what it means.

**3. One idea per sentence. Early verbs.**
Research is hard to follow; don't make it harder with run-on sentences. Put the verb near the subject. If a sentence has two ideas, split it.

**4. The reader has no context.**
You spent months on this. The reader has 10 minutes. Explain before you assume. Define notation before using it. Motivate before presenting.

**5. Consistent terminology.**
Never use synonyms for key concepts. If you call it "DS Score" on page 1, call it "DS Score" on page 30 -- not "the text score," "the qualitative measure," or "our indicator."

## Finance-Specific Softening

This guide adapts ML-paper advice for empirical social science. Key adjustments:

- **Passive voice**: Acceptable in methodology and data sections ("Data are obtained from CSMAR") but avoid in results ("It is found that..." -> "We find...")
- **Hedging**: Some hedging is appropriate ("Our results suggest...") but avoid stacking hedging words ("It may perhaps potentially suggest...")
- **Statistical thresholds**: Report t-statistics and economic magnitudes, not just asterisks. A result can be statistically significant but economically trivial.
- **Novelty framing**: In finance, incremental contribution is fine. State clearly what is new and what builds on prior work.

## Workflow Integration

This skill is a **reference layer** -- it does not execute workflows. Other skills load specific reference files as needed:

- `/write` reads [references/style.md](references/style.md) and [references/structure.md](references/structure.md) when drafting
- `/review` reads [references/evidence.md](references/evidence.md) and [references/narrative.md](references/narrative.md) when evaluating
- `/paper-editor` reads all references during editorial review
- Any skill can reference these files independently

## Sources

Advice synthesized from:
- Neel Nanda (paper writing tips)
- Ethan Perez (research communication)
- Jacob Foerster (rigorous evidence)
- Jacob Steinhardt (clarity and precision)

Adapted for empirical finance/economics conventions.

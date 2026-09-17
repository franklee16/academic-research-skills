---
name: top-journal-manuscript-review
description: Audit, review, restructure, and rewrite research manuscripts for top multidisciplinary and field-leading journals. Use when evaluating whether a paper is ready for editorial screening or external review; diagnosing desk-rejection risks; aligning title, abstract, introduction, results, figures, methods, discussion, supplementary materials, and cover letter around one contribution; checking claim-evidence boundaries, causal language, methodological triangulation, narrative coherence, or journal fit; or revising manuscripts for Nature, Science, Cell, PNAS, Nature Human Behaviour, Management Science, ISR, and comparable journals.
---

# Top-Journal Manuscript Review

Evaluate argument before language. A polished manuscript with a weak contribution, broken evidence chain, or inflated claims is not submission-ready.

## Required workflow

1. Identify the target journal, article type, central question, principal claim, and strongest evidence.
2. Read the latest complete manuscript before judging it. When multiple versions exist, determine the latest version from filenames and modification times.
3. Write the manuscript's current claim in one sentence. Separately write the strongest claim actually supported by the evidence.
4. Apply the six editorial standards in [editorial-standards.md](references/editorial-standards.md).
5. Apply the eight writing standards in [manuscript-writing.md](references/manuscript-writing.md), including the sentence-level reader-centred writing audit.
6. Build a claim-evidence map for every main figure and section.
7. Report findings by priority, then propose the smallest coherent revision that fixes the argument.
8. Rewrite text only after the conceptual diagnosis is complete.

## Review stance

- Think first like an editor deciding whether to send the paper for review.
- Then think like a skeptical reviewer testing identification, measurement, robustness, and boundaries.
- Distinguish importance from grand language. Importance must arise from the problem and evidence.
- Treat sample size as supporting evidence, not as the contribution itself.
- Prefer one defensible conceptual advance over several loosely connected findings.
- Do not invent mechanisms, causality, data, citations, novelty, or journal fit.
- Preserve the author's intended contribution when defensible; state plainly when the evidence requires a narrower claim.

## Claim-evidence discipline

For every major statement, classify it as one of:

- `directly shown`: estimated or experimentally demonstrated by the study.
- `supported interpretation`: consistent with multiple results but not directly identified.
- `plausible mechanism`: one explanation among alternatives.
- `implication`: consequence if the interpretation holds.
- `speculation`: not established by the present evidence.

Never allow a lower category to be written as a higher one. In particular, do not equate proxy traces with observed behaviour, measured novelty with underlying contribution, association with causation, or reviewer scores with scientific quality.

## Section audit

Check sections in this order:

1. **Title and abstract:** Do they state the supported contribution without reproducing the entire Results section?
2. **Introduction:** Does it establish a consequential problem, the exact unresolved gap, and the study's answer without previewing every result?
3. **Results and figures:** Does each section answer one question and make the next question necessary?
4. **Methods:** Can a specialist reproduce each measure and understand what each design does and does not identify?
5. **Discussion:** Does it elevate the concept, locate the evidence boundary, and avoid repeating results?
6. **Supplement:** Does it support the main line without housing evidence essential to the central claim?
7. **Cover letter:** Does it state importance, credibility, and journal fit briefly rather than summarize every analysis?

## Output modes

Choose the mode implied by the request.

### Editorial audit

Return:

1. `Editorial verdict`: likely send-out, borderline, or likely desk rejection, with a concise reason.
2. `Major findings`: ordered by severity, each tied to a section, figure, or exact wording.
3. `Claim-evidence risks`: overclaims, hidden assumptions, proxy confusion, and causal slippage.
4. `Revision priorities`: the three to seven changes most likely to improve editorial outcome.
5. `Residual risks`: issues that rewriting alone cannot solve.

### Section rewrite

Return:

1. A one-sentence diagnosis of the section's current failure mode.
2. A polished replacement.
3. Three to five brief revision notes focused on argument and evidence, not cosmetic wording.

### Full-manuscript restructuring

Return:

1. One central claim.
2. A figure-to-claim evidence map.
3. A section architecture showing the function of each section.
4. Text requiring deletion, movement, compression, or qualification.
5. Revised sections in an order that preserves a single narrative.

## Final checks

Before delivering, verify:

- The title, abstract, introduction, results, discussion, and cover letter describe the same paper.
- Every main figure has one indispensable argumentative function.
- No robustness test is presented as a new contribution.
- No conclusion is stronger than the design supporting it.
- The broad implication is stated once and bounded.
- The prose is direct, readable across disciplines, and free of unnecessary long sentences.
- Sentence subjects, construct names, and evidence levels remain stable; no claim becomes stronger through wording alone.

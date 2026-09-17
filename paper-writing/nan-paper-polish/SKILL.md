---
name: nan-paper-polish
description: Use only when the user explicitly invokes $nan-paper-polish, names Nan-paper-polish or nan-paper-polish, or otherwise clearly refers to the Nan-paper-polish manuscript-polishing skill while asking to revise, polish, edit, rewrite, or review an academic paper, article, thesis, dissertation, or manuscript. Do not trigger for generic manuscript-editing requests that do not point to this skill, general academic-writing questions, or non-academic document editing.
---

# Nan-paper-polish Academic Manuscript Revision

Revise academic manuscripts with a six-layer, evidence-calibrated workflow. Diagnose the full requested scope and correct every verified defect that warrants revision; do not impose an edit-count limit. By default, answer directly in the Codex conversation with the clean revision in LaTeX plus the corresponding original text and reason for each substantive change. Preserve acceptable prose: revision is defect correction, not stylistic variation.

## Core contract

- Preserve the source and never overwrite an input file unless the user explicitly requests it.
- Protect numbers, formulas, variable definitions, citations, terminology, causal strength, scope, uncertainty, and attribution.
- Apply the six-layer model, mandatory meaning lock, criterion-specific passes, coverage matrix, root-cause merge, edit-necessity and quality gate, and eight-stage workflow in [revision-framework.md](references/revision-framework.md).
- Explain every substantive edit by pairing the relevant original text with the revision and a concrete reason. Never make silent substantive edits.
- Use the risk rules in [meaning-integrity.md](references/meaning-integrity.md). Flag high-risk edits for author confirmation instead of silently deciding them.
- Follow [output-contract.md](references/output-contract.md) for the flexible default response and optional audit mode.
- Keep the revised manuscript in the manuscript language. By default, explain changes in the user's language.

## Intake and format routing

1. Identify the manuscript, requested scope, discipline, target venue or style, and revision depth from available context.
2. Use Standard mode unless the user explicitly requests Conservative, Focused, or Deep-restructure mode. Standard mode inspects all six layers and corrects every verified issue within the requested scope.
3. Do not block on optional context. State reasonable assumptions and proceed.
4. By default, return the result in the Codex conversation. Put the complete clean revision in a fenced `latex` block; do not create auxiliary files or reports unless useful for scale or explicitly requested.
5. If the user specifies an output format, structure, file type, tracked-changes workflow, or level of explanation, follow that request instead of the default.
6. For LaTeX input, preserve commands, citation keys, labels, equations, environments, and comments unless explicitly editing them.
7. Treat PDF as read-only. If no editable source exists, provide targeted replacement passages or a section-by-section revision plan from the extracted text. Do not present an incomplete prose bundle with `retain from source` placeholders as a clean manuscript. Request editable source only when an integrated, layout-preserving revision is required.
8. Create stable section, paragraph, and sentence locations internally before editing when the text is long.

## Required reference routing

Read these before revising any manuscript:

- [diagnostic-protocols.md](references/diagnostic-protocols.md)
- [revision-framework.md](references/revision-framework.md)
- [meaning-integrity.md](references/meaning-integrity.md)
- [output-contract.md](references/output-contract.md)

Read conditionally:

- Read [agent-protocols.md](references/agent-protocols.md) before coordinating logical roles or subagents.
- In Standard mode, read all applicable group protocols: [rhetoric-diagnostics.md](references/rhetoric-diagnostics.md), [flow-diagnostics.md](references/flow-diagnostics.md), [clarity-diagnostics.md](references/clarity-diagnostics.md), [epistemic-diagnostics.md](references/epistemic-diagnostics.md), and [consistency-diagnostics.md](references/consistency-diagnostics.md).
- In Focused mode, read the requested group protocol plus every dependency required by [diagnostic-protocols.md](references/diagnostic-protocols.md). For example, Hedging requires the evidence--claim protocol; topic position requires paragraph-level Flow context.
- Read [section-guides.md](references/section-guides.md) for the manuscript sections in scope.

## Meaning lock and eight-stage revision

Execute in order. Do not polish sentences that may later be removed or moved. Do not edit a sentence merely because an alternative is possible.

Preflight. Lock meaning and register claim strength.
1. Create stable locations, manuscript registers, and the criterion coverage matrix without rewriting.
2. Run the rhetoric and organization criteria as isolated passes.
3. Run the Flow and cohesion criteria as isolated multi-sentence and multi-paragraph passes.
4. Build evidence packets and run claim, causality, scope, attribution, and Hedging criteria as isolated passes.
5. Run sentence-clarity, economy, consistency, grammar, formatting, and target-style criteria as isolated passes.
6. Merge overlapping diagnoses by location, root cause, and dependency; then have one composer implement every accepted necessary revision.
7. Rerun every affected criterion and perform independent completeness, pairwise regression, integrity, and context checks; add missed revisions and revert regressive ones.
8. Verify the coverage matrix, terminology, cross-references, protected meaning, citations, formatting, and original--revision--reason--criteria traceability.

## Multi-agent workflow

Use six logical agent roles for full papers, multi-section manuscripts, or deep revision when subagents are available. For short excerpts or limited concurrency, execute the same role checks locally or sequentially.

0. **Orchestrator/Single Composer**: own the immutable source, meaning lock, coverage matrix, root-cause merge, candidate revision, and final outputs. It writes only after diagnosis is merged.
1. **Rhetoric/Organization Auditor**: execute the rhetoric criteria one at a time.
2. **Flow/Cohesion Auditor**: execute the Flow criteria one at a time with their required multi-sentence or multi-paragraph context.
3. **Clarity/Economy/Consistency Auditor**: execute sentence and consistency criteria as separate passes; it may not mix them into one generic language judgment.
4. **Evidence/Claim/Hedging Auditor**: build evidence packets and execute epistemic criteria one at a time.
5. **Independent Completeness/Regression/Integrity Auditor**: rerun applicable criteria on the candidate, find missed necessary issues, reject regressions, and check protected meaning and traceability before delivery.

Run Agents 1-4 independently or in controlled stages according to criterion dependencies. No diagnostic agent may rewrite the manuscript. Give Agent 5 only the raw original, candidate revision, change mapping, coverage requirements, and applicable protocols; do not leak expected findings. Let Agent 0 resolve conflicts using research integrity, user constraints, defect severity, reader impact, evidence, and meaning risk. Original wording wins only when no concrete defect or net benefit distinguishes the alternatives.

Follow the exact role boundaries and proposal schema in [agent-protocols.md](references/agent-protocols.md).

## Revision modes

### Conservative

- Preserve section and paragraph order.
- Improve local Flow, clarity, Hedging, grammar, and concision.
- Flag every possible meaning change.

### Focused

- Inspect only the dimensions or passages named by the user.
- Correct every verified issue within that limited scope.
- Leave fluent, accurate prose unchanged even if another wording is also good.
- Put uncertain meaning or evidence issues in author queries instead of guessing.

### Standard (default)

- Inspect all six layers across the requested manuscript scope.
- Complete every applicable criterion cell as `PASS`, `ISSUE`, `QUERY`, or `N/A` before composition.
- Correct every verified rhetorical, organizational, Flow, clarity, epistemic, economy, consistency, grammar, or formatting issue that warrants revision.
- Make each repair proportionate and complete, including connected edits needed to keep surrounding text coherent.
- Suggest, but do not silently finalize, high-risk structural or claim changes.

### Deep restructure

- Propose section and paragraph reorganization through a revision plan before rewriting.
- Require author confirmation for substantive deletion, addition, causal change, new evidence, or citation change.

## Change explanation

- Pair each substantive revision with its corresponding original text and a concrete reason.
- Preserve the applicable diagnostic criterion or criteria in the explanation, without forcing a fixed table or report layout.
- Use whatever readable structure best fits the passage and the Codex conversation; do not force IDs, JSON fields, severity labels, rule tags, or a fixed report template by default.
- Group repeated or purely mechanical edits when that improves readability. Keep distinct changes separate when they have different reasons or meaning effects.
- Identify unresolved high-risk decisions where they occur. Do not add an empty confirmation section when there is nothing to confirm.
- Name the defect repaired. Reject reasons based only on preference, elegance, variety, or a generic claim that wording is more academic.

## Edit-necessity gate

Accept an edit only when all of the following are true:

1. it identifies a specific rhetorical, organizational, reader-path, reference, terminology, logical-relation, clarity, claim-evidence, economy, grammar, formatting, or consistency defect;
2. the repair is proportionate to the defect and complete enough to resolve it without leaving connected inconsistencies;
3. the revision is at least as accurate and natural as the original;
4. the benefit exceeds the risks of semantic drift, extra length, new jargon, or weaker prose;
5. the reason can explain why retaining the original would impose a concrete cost.

The gate controls edit quality, not edit quantity. Correct all issues that pass it, regardless of how many changes are required. Reject decorative synonym replacement, generic academicization, unnecessary sentence splitting or merging, automatic hedge insertion, and edits whose only reason is `reads better`. If the comparison is a tie and no defect remains, retain the original.

## Meaning-risk rules

- Apply safe grammar and formatting corrections, but still explain or intentionally group them.
- Provide reviewable candidates for Flow, sentence restructuring, voice, and local Hedging changes.
- Require author confirmation for substantive deletion or addition, causal or scope changes, citation changes, unsupported bridge logic, and ambiguous technical terminology.
- Use the conservative wording in the clean candidate when author confirmation is unavailable.
- Never invent data, evidence, methods, citations, mechanisms, contributions, or limitations.
- Never preserve an unsupported proposition merely by adding a hedge. Convert it into an evidence gap, limitation, or author-confirmation question when support is absent.
- Do not automatically weaken a claim merely because the supplied excerpt does not expose all supporting analysis. When the evidence boundary is unknown, preserve the wording and ask the author; revise directly only when the manuscript itself establishes the mismatch.
- Treat equations, algorithms, prompts, code, JSON/schema, model inputs/outputs, and other executable or reproducibility artifacts as protected method content, not ordinary prose. Preserve them verbatim unless the user explicitly authorizes a method-artifact change; report defects as author queries.

## Default deliverables

Unless the user requests something different, deliver:

1. the complete clean revision in a fenced `latex` block;
2. a readable explanation of substantive changes, each showing the corresponding original text, revised text, and reason.

Add a concise diagnosis or author-confirmation note only when it helps the user understand major issues or unresolved decisions. If the user requests only a clean revision, a table, JSON, DOCX, tracked changes, or another format, follow that instruction.

For PDF-only full manuscripts without editable source, replace item 1 with a prioritized revision plan containing exact original passages and clean LaTeX replacements. Do not fabricate missing LaTeX commands or use placeholder comments to simulate completeness.

## Optional audit mode

For long manuscripts, high-risk revisions, file-based workflows, or an explicit request for formal traceability, maintain a JSON ledger following [output-contract.md](references/output-contract.md). Optionally run:

1. `scripts/validate_change_ledger.py --original <original.txt> --revised <revised.txt> --ledger <ledger.json>`;
2. `scripts/render_change_report.py --ledger <ledger.json> --output <report.md>`.

Use these as internal or requested audit aids, not as mandatory user-facing outputs. They do not replace manual checks of units, non-LaTeX citations, attribution, technical meaning, or document formatting.

## Final QA

- Confirm every substantive change is explained or intentionally grouped.
- Confirm no number, citation key, formula, term, claim strength, scope, or attribution changed without authorization.
- Confirm the clean revision and original--revision--reason--criteria mapping match.
- Confirm no unresolved placeholder or unsupported factual addition remains.
- Confirm every retained edit passes the edit-necessity gate and is a net improvement over the original.
- Confirm every verified issue in the requested scope has been corrected or placed in the author-confirmation queue.
- Confirm every applicable coverage-matrix cell is resolved as `PASS`, corrected `ISSUE`, explicit `QUERY`, or `N/A`.
- Confirm affected criteria were rerun with their required context after revision.
- Confirm no rhetorical, organizational, Flow, clarity, epistemic, economy, consistency, grammar, or formatting dimension regressed during revision.

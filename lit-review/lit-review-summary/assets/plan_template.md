# Multi-Agent Plan: Literature-Review Summary

**Status:** APPROVED (auto-approved per lit-review-summary skill protocol)
**Created:** {timestamp}
**Working dir:** `{output_folder}`

## Objective
Apply the {framework_name} to the {N} papers in `{papers_folder}`. Produce, per paper, a Tier 1 Reference Sheet; aggregate into a Tier 2 Cheat Sheet; synthesize a Tier 3 Synthesis Matrix.

## Papers ({N}) — input files
{paper_list_numbered}

## Output structure
```
{output_folder}/
  plan.md                       <- this file
  summaries/01..NN_<slug>.md    <- one Tier-1 sheet per paper
  reviews/review_A_*.md, ...    <- critic reports (Phase 3)
  cheat_sheet.md                <- Tier 2 aggregate
  synthesis_matrix.md           <- Tier 3 aggregate
  final_literature_review.md    <- combined deliverable (Tiers 1+2+3)
```

## Phases

### Phase 1 — Planning & inventory (DONE)
- Inventoried `{papers_folder}` ({N} files).
- Confirmed framework.
- Output: this `plan.md`.

### Phase 2 — Execution: per-paper Tier-1 summaries (parallel)
- {N} summarizer subagents (one per paper), dispatched in waves of up to 10.
- Each reads its paper, applies Tier 1, and saves to `summaries/NN_<slug>.md`. Returns only a status line.

### Phase 3 — Review (parallel critics)
- {n_critics} critic subagents split the sheets (~7 each).
- Each scores 0-100 with deductions, lists fixes, saves to `reviews/`. Returns status summary only.

### Phase 4 — Revision
- {n_revisers} reviser subagents mirror the critics' splits.
- Each applies fixes in place (Edit). Returns status summary only.

### Phase 5 — Aggregation & synthesis
- 1 aggregator reads all revised sheets, writes `cheat_sheet.md` (Tier 2) and `synthesis_matrix.md` (Tier 3).

### Phase 6 — Final assembly
- Mother agent concatenates on disk (via Bash) into `final_literature_review.md`: framework recap + Tier 2 + Tier 3 + appendix of all Tier-1 sheets. No re-generation.

## Context-engineering rules
- Subagents save outputs locally and return ONLY a one-line status.
- Mother agent never reads full papers or full sheets into its own context.
- Tool grants per subagent: Read, Write, Edit, Bash.

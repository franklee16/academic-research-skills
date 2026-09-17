# {{PROJECT_NAME}}

AI co-mathematician research project.
Initialized {{DATE}}.

## Research question

{{RESEARCH_QUESTION}}

(See [`goals.md`](goals.md) for the full goal structure and approval status.)

## Layout

| Path | Purpose |
|---|---|
| [`paper.tex`](paper.tex) | The living working paper. All claims, proofs, and references live here. |
| [`goals.md`](goals.md) | Research question and approved sub-goals. |
| [`decisions.md`](decisions.md) | Append-only log of project decisions. |
| [`co-math-config.json`](co-math-config.json) | Per-project settings (strict mode, review policy). |
| [`workstreams/`](workstreams/) | One directory per workstream (literature, computational, prover, lean-prover, readability). |
| [`references/`](references/) | Downloaded papers and notes, indexed by arxiv id. |
| [`failed-explorations/`](failed-explorations/) | Durable record of approaches that didn't work. |
| [`.co-math/`](.co-math/) | System state: workstream registry, reviewer approvals. |
| [`.claude/settings.json`](.claude/settings.json) | Per-project Claude Code hooks (constraints). |

## Working with this project

1. **Refine `goals.md`.** Talk to the `project-coordinator` agent (or just edit
   the file directly) until the research question and sub-goals match your
   intent. Mark `Approval: YES` when ready.
2. **Spawn workstreams.** Each sub-goal becomes one (or more) workstream. The
   project-coordinator delegates to specialized sub-agents
   (literature-reviewer, prover, coder). For results worth machine-checking, it
   can dispatch a `lean-prover` workstream that formalises the lemma in Lean 4
   and verifies it with `lake build` — a green build is the strongest evidence
   the system supports.
3. **Review and steer.** Read incremental reports in
   `workstreams/W*/report.md`. Intervene at any time by messaging the
   project-coordinator.
4. **Polish accepted proofs.** Once a prover or lean-prover workstream is
   APPROVED, the coordinator may run a `W{NNN}-readability-{slug}` pass (the
   `proof-readability` skill) — an exposition-only edit that never changes the
   mathematics, re-reviewed for content preservation and plumbing only.
5. **Compile the paper.** `paper.tex` is the durable artifact. Margin notes
   record provenance, `\unproven{}` blocks flag every unverified step,
   `\leanproved{W{NNN}}` marks machine-checked results, and the "Open
   obligations" appendix lists every remaining gap.

## Discipline rules (enforced by hooks once Phase 3 ships)

- A workstream cannot be marked `complete` without an approval file from the
  `paper-reviewer` agent in `.co-math/approvals/`.
- A `\begin{theorem}` block in `paper.tex` must have a matching `\proof` block,
  be closed by `\leanproved{W{NNN}}` (a Lean-verified result needs no informal
  proof), or be wrapped with `\unproven{}`.
- Every `\cite{...}` must resolve to an entry whose source has been verified
  by the literature-reviewer.

## Strict mode

This project's `strict_mode` is recorded in `co-math-config.json`. In strict
mode (the default), the prover must never hand-wave a proof step — every gap
is explicitly `\unproven{...}`. To relax this for this project, edit
`co-math-config.json`, set `"strict_mode": false`, and document the decision
in `decisions.md` with your rationale.

# Roadmap

This is the maintainer's view of where the Theorist Toolbox is headed. It is a
direction, not a contract — and it is discussed in the open. To weigh in, comment on
the pinned **[RFC] Roadmap** issue or open a [Discussion](../../discussions).

## The vision

A shared, opinionated toolkit that lets an economic theorist get *trustworthy*
machine help on a proof — from a single careful pass, to an adversarial verifier, to
a full research-team workflow that can reject its own work. The invariant across
everything we add: **the tool makes the model more correct, never just more
confident.**

The core stays small. Growth happens at the edges, as modules:

- **skills** — disciplines the model follows (proving, checking, writing).
- **agents** — co-math sub-agents with a job, tools, and an honest failure mode.
- **case studies** — worked, reproducible examples that show the discipline holding
  (or honestly failing).

## Strategic priorities (the hard problems)

These are the structural problems with the current system. They matter more than any
single new skill, because they decide whether the toolkit is *usable at scale*. Each
is open for design discussion in the RFC.

1. **Token efficiency.** The co-math workflow is wasteful: many sub-agents, each
   re-reading shared context (`paper.tex`, prior reports), with the adversarial
   reviewer invoked more than it needs to be. Directions worth exploring: scope each
   agent to its workstream rather than the whole paper; cache/diff instead of
   re-reading; invoke the reviewer only at gates; per-workstream token budgets.
2. **Model routing (stop always using the strongest model).** Today every agent runs
   the top model. Most of the work doesn't need it — literature formatting, status
   rendering, readability lint, and plumbing-only review are cheap-model tasks; only
   proving and adversarial verification need the strongest. Plan: a per-agent `model`
   tier in `co-math-config.json`, with the coordinator routing by task.
3. **Economic significance, not just mathematical truth.** The system happily proves
   results that are *true but economically uninteresting*, and sometimes the math
   generalises in a way that *strips* the economic content (a trivialising hypothesis,
   an assumption that voids the mechanism). We need a taste/relevance gate — an
   `economics-referee` agent or a `economic-significance` skill that applies the
   "so what?" test and flags when a generalisation reduces economic value. This is the
   editor in the room, and arguably the most distinctive thing the toolkit could add.
4. **Output sharing.** A way for people to publish and browse co-math outputs — the
   paper, the prompts, the workstream logs — so the community learns from real runs.
   Start GitHub-native (a curated `showcase/` + the "Show and tell" discussions),
   graduate to a dedicated gallery/site only if volume justifies it.

## Candidate next modules

Smaller, self-contained wins. Pick one up, or argue for a different ordering in the RFC.

- **Boundary-condition / edge-case skill.** Force enumeration of degenerate cases
  (empty type space, ties, corner solutions, measure-zero events) before a proof is
  declared complete — the most common gap in theory proofs.
- **Counterexample-search agent.** A sibling to `coder` whose job is purely
  adversarial: given a conjecture, search numerically/symbolically for a refutation
  before any proof effort is spent.
- **Extensive-form / game-tree reasoning skill.** Subgame perfection, information sets,
  backward induction — where LLMs currently flail.
- **Wider Lean coverage.** Helpers mapping common econ-theory constructs (preference
  relations, fixed-point arguments, measure-theoretic limits) onto mathlib, lowering
  the cost of a `lean-prover` workstream.

## Out of scope (for now)

- Heavy governance machinery (CLAs, SLAs, multi-track review).
- Provider lock-in. Skills should encode discipline, not hard-code one model's quirks.

## How priorities get set

If you want to build one of these, say so and it moves up.

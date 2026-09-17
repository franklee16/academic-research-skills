---
name: paper-reading-research-framing
description: Use when one research source chain is stable enough to turn into paper framing or a provisional framing sketch by comparing closest related works, checking claim-level citation support, clarifying positioning and differentiation, and producing a writing blueprint.
---

# Research Framing

Use this skill for the motivation: 形成论文表达 / 研究定位 / 引用支撑.

This skill merges the former citation-checking, differentiation, and writing-pattern motivations. They are not separate workflows here; they are three lenses on one question:

> How should this current research be stated as a paper, compared with similar work, and made to look both credible and distinctive?

Treat Research Framing as a `Source Chain -> Close Work Threats -> Claim Safety -> Paper Blueprint` converter. It does not start from free-form paper-writing help. It starts from exactly one upstream research lineage and turns that lineage into a paper-facing framing package or a clearly marked provisional sketch.

## Output Root

Set `{workspace-root}` before creating, scanning, or updating artifacts:

- Default `{workspace-root}` to `workspace` (the repo-local `workspace/` directory).
- If the user specifies a workspace root, use that path exactly and do not add another `workspace/` layer.
- If the user provides an existing artifact or workflow path, infer `{workspace-root}` from that path and keep related artifacts under the same root.
- Do not create new generated workflow directories directly at the repository root.

## Core Workflow

1. Identify exactly one Research Framing Source Chain and its deepest stable Research Framing Leaf Source.
2. Pass the Research Framing Source Gate by recording the Source Chain Trace, leaf source, stable claims, provisional claims, writing goal, scope, and output status.
3. Create or resume a Research Framing Workspace at `{workspace-root}/research-framing/{project-slug}/`.
4. Write or update `source_research.md`.
5. Run the Research Framing Context Review before paper search: preserve the leaf source's claims, evidence routes, baseline pressures, metric validity risks, ablations, unsafe claims, and upstream warnings.
6. Build the Close Work Set from local artifacts first, especially the Baseline Pressure Matrix when the leaf source is an Experiment Design, then use targeted paper search only to verify or fill close-work gaps.
7. Pass the Close Work Selection Gate by confirming, revising, or explicitly delegating the 3-8 close works and their threat roles.
8. Extract each close work's problem, method, setting, assumptions, evaluation, claims, limitations, writing moves, and threat role into `close_works.md`.
9. Draft `claim_support_bank.md`, mapping the user's paper-facing claims to papers that support, weaken, narrow, contradict, or merely background them.
10. Draft `positioning_matrix.md`, comparing the user's work with close works across problem, setting, method, evaluation, contribution type, and novelty boundary.
11. Draft `story_spine.md`, including the One-Sentence Paper Pitch, 7-sentence Story Spine, contribution highlights, and candidate novelty boundary.
12. Draft `writing_blueprint.md`, turning the story, positioning, claim support, and writing moves into an introduction outline, related-work outline, and contribution bullets.
13. Pass the Story And Claim Safety Gate by confirming, revising, or explicitly delegating the pitch, novelty boundary, safe claims, claims to avoid, and claim downgrades required by evidence support.
14. Write `research_framing_package.md` as either a final Research Framing Package or a Provisional Framing Sketch according to source status.
15. Stop when the user can state the paper story, name the closest works, explain the difference from each, and support or safely downgrade the main paper-facing claims.

## Framing Boundary

Research Framing is a writing-facing comparison workflow. It does not invent a new research problem, commit a method, or design experiments.

Use it to decide:

- what story the paper should tell,
- which close works define the comparison frame,
- which claims are citation-supported,
- how the paper differs from similar research,
- which contribution highlights are worth foregrounding,
- and which writing moves can be borrowed structurally.

Do not use it to:

- run a broad Field Map Workflow,
- validate whether the problem is real,
- choose the actual method,
- select baselines or metrics,
- revise an experiment design,
- or produce reviewer objections beyond writing-relevant positioning risks.

Do not treat planned evidence as results. If experiment results do not exist yet, state evaluation claims as "we evaluate whether...", "the experiment is designed to test...", or another safe planned-evidence form.

## Output Status

Research Framing has two possible output statuses.

**Research Framing Package**:

- Use only when the leaf source is a reviewed Experiment Design, or the user provides an equivalent stable experiment plan with explicit source chain, claims, evidence routes, baseline pressures, and scope.
- The package may still describe planned experiments, but it must not claim empirical success before results exist.

**Provisional Framing Sketch**:

- Use when the leaf source is only a Committed Method Design, Research Question Card, proposal draft, paper draft, or user-provided research brief.
- It may preview the pitch, story, close works, positioning, safe claims, and writing blueprint.
- It must mark missing experiment-backed evidence and must not be presented as a final Research Framing Package.

## Research Framing Source Gate

The workflow must begin from exactly one Research Framing Source Chain, not a collage of all upstream artifacts. Use the deepest stable leaf source available:

1. reviewed Experiment Design, preferred for a final Research Framing Package
2. Committed Method Design, allowed for a Provisional Framing Sketch
3. Research Question Card, allowed for a more provisional story and positioning preview
4. proposal draft, paper draft, or user-provided research brief, only after normalizing it into exactly one source chain

The gate is passed only when the following are recorded:

- Research Framing Leaf Source artifact or user-provided source text,
- Source Chain Trace, including upstream question, method, and experiment artifacts when present,
- output status: final package or provisional sketch,
- current problem statement,
- current method or intervention, if any,
- current experiment plan, if any,
- target contribution type,
- stable claims and provisional claims that need support,
- known close works or suspected close works,
- intended venue or audience, if known,
- provisional or unstable parts that should not be overclaimed,
- scope boundaries and non-goals,
- writing goal: introduction, related work, proposal, rebuttal prep, method positioning, or full paper framing,
- and recommended routing: proceed to final package, proceed provisionally, or route upstream.

If a deeper stable leaf source exists locally, use it rather than a shallower source. If there are multiple possible source chains, ask the user to choose exactly one. If the source is not stable enough even for a provisional sketch, recommend the upstream workflow that should run first, such as `paper-reading-research-question`, `paper-reading-method-commitment`, or `paper-reading-experiment-design`.

## Research Framing Context Review

Before building the Close Work Set or searching for papers, inspect the local artifacts in the selected Source Chain.

If the leaf source is an Experiment Design, read available artifacts in the experiment folder:

- `source_experiment_context.md`
- `claim_evidence_map.md`
- `baseline_pressure_matrix.md`
- `claim_metric_map.md`
- `experiment_design.md`
- `ablation_and_controls.md`

Use `baseline_pressure_matrix.md` as the primary local source for initial close-work candidates and reviewer comparison threats. Do not restart from a broad related-work search.

For upstream context, read the linked Committed Method Design, Method Commitment Summary, Research Question Card, Problem Reality Check, Method Inspiration artifacts, or theoretical grounding artifacts when they are referenced by the source chain and relevant to claim safety.

Preserve inherited unsafe claims, evidence gaps, do-not-route warnings, and result-interpretation constraints. The framing package must not erase fragilities exposed by upstream workflows.

## Research Framing Workspace

Create durable artifacts at:

```text
{workspace-root}/research-framing/{project-slug}/
```

Use this structure:

- `source_research.md`
- `close_works.md`
- `claim_support_bank.md`
- `positioning_matrix.md`
- `story_spine.md`
- `writing_blueprint.md`
- `research_framing_package.md`

Use the reference templates in this directory when creating these artifacts.

## Close Work Selection Gate

Build a Close Work Set of 3-8 papers, systems, benchmarks, or methods. Treat the set as a threat list, not a general related-work list.

Each Close Work should record one or more threat roles:

- same-problem work
- same-method-family work
- same-setting or system work
- same-evaluation work
- baseline-threat work
- novelty-threat work

One work may fill multiple roles. Do not pad the set just to fill every role.

Before final positioning or story decisions, ask the user to confirm, revise, or explicitly delegate:

- each included Close Work,
- its threat role,
- why it is close,
- what reviewer challenge it raises,
- and why any obvious suspected close work is excluded or left for later search.

If the user requests a fully automatic run, keep close-work selection provisional and produce only a Provisional Framing Sketch unless a stable reviewed experiment source and low-risk close-work set already exist.

## Reading Lenses

Read close papers with five lenses.

**Claim support**:
For each user claim, record whether a paper directly supports it, weakly supports it, contradicts it, narrows it, or only provides background. A citation is usable only when the paper supports the actual strength and scope of the claim.

**Positioning and differentiation**:
Compare the user's work with each close work across problem, method, setting, assumptions, evidence, and contribution. The goal is not to prove total uniqueness; it is to state a defensible novelty boundary.

**Story spine**:
Identify the narrative route that makes the current research feel necessary: known situation, unresolved tension, closest-work limitation, intervention, evidence plan, and contribution.

**Contribution highlights**:
Name what should be foregrounded because it is both true and differentiating: new problem framing, new mechanism, new setting, stronger evidence, clearer evaluation, useful system behavior, theoretical reframing, or practical constraint.

**Writing moves**:
Extract reusable rhetorical structures without copying prose: motivation openings, gap packaging, contrast transitions, contribution lists, related-work grouping, limitation handling, and figure or table patterns. Do not keep writing moves as a standalone final-package section; absorb useful moves into the Paper Writing Blueprint.

## Claim Support Bank

Map paper-facing claims to their support boundaries. Use these claim types:

- motivation claim
- gap claim
- novelty claim
- mechanism claim
- method claim
- evaluation claim
- practical relevance claim
- limitation claim

For each claim, record:

- claim text,
- claim type,
- supporting evidence,
- support strength,
- safe version,
- avoid,
- and whether the claim depends on planned experiment evidence.

Respect the Result Claim Boundary. Without actual experiment results, do not write outcome-achieved claims such as "our method improves Z." Use safe planned-evidence forms such as "we evaluate whether the method improves Z under..." or "the experiment is designed to test whether...".

## Story And Claim Safety Gate

Before writing `research_framing_package.md`, ask the user to confirm, revise, or explicitly delegate the core framing decisions:

- One-Sentence Paper Pitch
- novelty boundary
- 7-sentence Story Spine
- safe claims
- claims to avoid
- claim downgrades required by weak citation support, provisional evidence, or missing results
- contribution bullets that should be foregrounded

This gate is passed only when the paper story and claim boundary are safe relative to the Close Work Set, Positioning Matrix, Claim Support Bank, and Result Claim Boundary.

## Required Final Package

`research_framing_package.md` must include:

1. Source Research Summary
   - Source Chain Trace
   - working title
   - research question
   - target problem
   - proposed method or intervention
   - target setting
   - target user or stakeholder
   - current experiment plan
   - intended venue or audience
   - current maturity
2. One-Sentence Paper Pitch
3. Story Spine
   - known situation
   - emerging tension
   - why existing work is insufficient
   - key insight
   - proposed approach
   - evidence plan
   - main takeaway
4. Close Work Set
   - Work
   - why it is close
   - threat role
   - what it solves
   - what it does not solve
   - how this work differs
5. Positioning Matrix
   - problem
   - setting
   - method
   - evaluation
   - contribution type
   - novelty boundary
6. Claim Support Bank
   - claim
   - claim type
   - supporting evidence
   - support strength
   - safe version
   - avoid
7. Safe Claims / Claims To Avoid
8. Paper Writing Blueprint
   - recommended introduction outline
   - recommended related-work outline
   - contribution bullets

Contribution highlights should appear inside the Story Spine and Paper Writing Blueprint, not as a separate final-package section.

## Required Templates

Use the reference templates in this directory:

- `references/source-research-template.md`
- `references/close-works-template.md`
- `references/claim-support-bank-template.md`
- `references/positioning-matrix-template.md`
- `references/story-spine-template.md`
- `references/writing-blueprint-template.md`
- `references/research-framing-package-template.md`

## Hard Confirmation Gates

Do not skip these gates:

1. **Source chain confirmed**: do not build close works until exactly one source chain and leaf source are selected, unless the user explicitly requests a provisional sketch.
2. **Close works selected**: do not finalize positioning, story, or novelty boundary until the Close Work Set and threat roles are confirmed or explicitly delegated.
3. **Story and claim safety reviewed**: do not write the final package until the pitch, novelty boundary, safe claims, and claims to avoid are confirmed or explicitly delegated.

If a gate is delegated, record the delegation rather than rewriting it as confirmation. If gates are unreviewed because the user requested a fully automatic run, keep the output provisional.

## Stop Conditions

Stop when all are true:

- the user can name the 3-8 closest works,
- the user can explain the difference from each close work,
- the main motivation and contribution claims have citation support or safer wording,
- the paper story is stated in a compact form,
- unsafe, weak, or result-dependent claims have been downgraded,
- the output status is explicit,
- and the user has an introduction outline, related-work outline, and contribution bullets that can be transferred into paper writing.

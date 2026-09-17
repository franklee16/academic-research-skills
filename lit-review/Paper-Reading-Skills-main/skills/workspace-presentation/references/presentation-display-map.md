# Presentation Display Map

Use this map to classify artifacts and order modules for a Workspace Presentation. If a file is missing, keep the module visible only when its absence matters; otherwise list it in Source Files with `missing` status.

## Display Categories

- **Primary Display Artifact**: final or near-final user-facing research state. Show directly with summary, key fields, and source preview.
- **Summarize-Then-Link Artifact**: important process, decision, evidence, or risk material that is too cumbersome for default full display. Generate a structured module summary and link to the source.
- **Link-Only Artifact**: routing, template-like, repetitive, mechanical, very long, or audit-oriented material. Keep in Source Files or a drawer unless a summary is needed for missing-source context.

## Global Section Order

1. Research State Overview
2. Source Trace
3. Main Artifacts
4. Decisions & Evidence
5. Risks & Gaps
6. Next Actions
7. Source Files

## Field Map Workspace

Source kind: `field-map-workspace`

Expected path: `{workspace-root}/field-maps/{field-slug}/`

Primary Display:

- `field_boundary.md`
- `research_clusters.md`
- `research_opportunities.md`
- `index.html` when present, as a source link rather than embedded source of truth

Summarize Then Link:

- `search_strategy.md`
- representative files in `seed_papers/`
- representative files in `all_papers/`

Link Only:

- full `seed_papers/` and `all_papers/` file lists beyond representative papers

Recommended modules:

- Boundary & Scope
- Cluster Map
- Opportunity Candidates
- Search Strategy
- Representative Papers
- Paper Record Index

## Research Question Workspace

Source kind: `research-question-workspace`

Expected path: `{workspace-root}/research-questions/{field-slug}/`

Primary Display:

- `research_question_cards.md`
- files in `cards/`

Summarize Then Link:

- `candidate_angles.md`
- `writing_intent.md`
- files in `evidence/`

Link Only:

- `source_field_map.md`

Recommended modules:

- Selected Research Questions
- Writing Intent
- Candidate Angle Comparison
- Evidence Sufficiency
- Card Index

## Problem Reality Check Workspace

Source kind: `problem-reality-check-workspace`

Expected path: `{workspace-root}/research-question-checks/{field-slug}/`

Primary Display:

- `problem_reality_checks.md`
- `checks/{question-slug}/problem_reality_check.md`

Summarize Then Link:

- `checks/{question-slug}/interrogation_transcript.md`
- `checks/{question-slug}/source_card.md`

Link Only:

- `source_research_questions.md`

Recommended modules:

- Problem Reality Verdict
- Unsafe Motivation Claims
- Targeted Evidence Needs
- Interrogation Highlights
- Checked Card Source

## Theoretical Grounding Workspace

Source kind: `theoretical-grounding-workspace`

Expected path: `{workspace-root}/theoretical-groundings/{field-slug}/`

Primary Display:

- `theoretical_groundings.md`
- `groundings/{question-slug}/theoretical_grounding.md`
- `groundings/{question-slug}/selected_theoretical_traditions.md`

Summarize Then Link:

- `groundings/{question-slug}/problem_theory_decomposition.md`
- `groundings/{question-slug}/theory_hooks.md`
- `groundings/{question-slug}/candidate_theoretical_traditions.md`

Link Only:

- `source_research_question_checks.md`
- `groundings/{question-slug}/source_problem.md`

Recommended modules:

- Theory-Backed Problem Framing
- Selected Theoretical Traditions
- Theory-Support Claims
- Theory Hooks
- Remaining Theory Evidence Needs

## Method Inspiration Workspace

Source kind: `method-inspiration-workspace`

Expected path: `{workspace-root}/method-inspirations/{field-slug}/`

Primary Display:

- `method_candidate_libraries.md`
- `inspirations/{problem-slug}/method_candidate_library.md`
- `inspirations/{problem-slug}/candidate_methods.md`

Summarize Then Link:

- `inspirations/{problem-slug}/method_need_decomposition.md`
- `inspirations/{problem-slug}/targeted_method_search.md`
- `inspirations/{problem-slug}/method_patterns.md`
- `inspirations/{problem-slug}/transfer_mapping.md`

Link Only:

- `source_research_questions.md`
- `inspirations/{problem-slug}/source_problem.md`

Recommended modules:

- Method Candidate Library
- Candidate Method Comparison
- Method Needs
- Transfer Mapping
- Search Sufficiency & Pattern Risks

## Method Commitment Workspace

Source kind: `method-commitment-workspace`

Expected path: `{workspace-root}/method-commitments/{field-slug}/{method-slug}/`

Primary Display:

- `method_commitment_summary.md`
- exactly one status output when present: `committed_method_design.md`, `provisional_method_design.md`, `method_redesign_brief.md`, or `method_rejection_note.md`

Summarize Then Link:

- `method_reconstruction.md`
- `method_decision_log.md`
- `method_attack_transcript.md`

Link Only:

- `source_method.md`

Recommended modules:

- Commitment Status
- Method Design or Status Outcome
- Mechanistic Claim & Weakest Link
- Design Decisions
- Attack Highlights
- Downstream Routing

## Experiment Design Workspace

Source kind: `experiment-design-workspace`

Expected path: `{workspace-root}/experiment-designs/{field-slug}/{method-or-question-slug}/`

Primary Display:

- `experiment_design.md`
- `baseline_pressure_matrix.md`
- `claim_metric_map.md`
- `ablation_and_controls.md`

Summarize Then Link:

- `source_experiment_context.md`
- `claim_evidence_map.md`

Link Only:

- none by default

Recommended modules:

- Experiment Stack & Protocol
- Claim-Evidence Map
- Baseline Pressure Matrix
- Claim-Metric Map
- Ablations & Controls
- Result Interpretation Contract
- Provisional Status & Inherited Warnings

## Research Framing Workspace

Source kind: `research-framing-workspace`

Expected path: `{workspace-root}/research-framing/{project-slug}/`

Primary Display:

- `research_framing_package.md`
- `story_spine.md`
- `writing_blueprint.md`
- `positioning_matrix.md`

Summarize Then Link:

- `source_research.md`
- `close_works.md`
- `claim_support_bank.md`

Link Only:

- none by default

Recommended modules:

- Research Framing Package
- Source Chain Trace
- One-Sentence Pitch & Story Spine
- Close Work Threats
- Positioning Matrix
- Claim Support & Safe Claims
- Paper Writing Blueprint

## Source Chain Presentations

Source kind: `source-chain`

Use when one coherent chain spans multiple workflow folders, such as Research Question Card -> Method Commitment -> Experiment Design -> Research Framing.

Primary Display:

- deepest stable leaf artifact
- status or summary artifacts from upstream workspaces
- final package, plan, or committed design when present

Summarize Then Link:

- upstream decision logs, claim maps, baseline matrices, attack transcripts, problem checks, and transfer maps

Link Only:

- source gate files and repetitive paper records unless needed for a visible risk or evidence gap

Recommended modules:

- Source Chain Trace
- Current Leaf State
- Upstream Decisions
- Evidence & Claim Safety
- Risks Inherited Across Workflows
- Next Recommended Workflow

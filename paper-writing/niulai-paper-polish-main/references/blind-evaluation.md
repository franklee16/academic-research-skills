# Blind evaluation protocol

Use this for high-stakes full-paper revision, Skill testing, or when the user asks whether the revision genuinely improved the paper.

## Blind setup

1. Create isolated X and Y projects from the same complete source tree. Conceal which is baseline and which is revision from evaluators.
2. Remove change logs, guard reports, filenames, or metadata that reveal the mapping.
3. Evaluate both orders when feasible. Order-mirrored rereads by one evaluator test order sensitivity but do not count as independent reviewers.
4. Keep preservation auditing separate from quality scoring. A preservation failure cannot be averaged away by better prose.

## Preservation invariants

Require proposition-level comparison of:

1. numbers, uncertainty, metrics, samples, rankings, and values in row/column context;
2. methods, datasets, settings, splits, baselines, assumptions, and protocols;
3. comparison directions, causal strength, qualifiers, and evidence boundaries;
4. negative, null, mixed, subgroup, failure-case, and limitation content;
5. citations, prior-work descriptions, equations, algorithms, figures, tables, and code;
6. ethics, approvals, consent, disclosures, identity, and acknowledgments;
7. LaTeX structure, assets, build output, anonymity, and venue compliance;
8. coverage of every manuscript section and caption, including documented no-change decisions.

Use `PASS`, `CONDITIONAL PASS`, or `FAIL`. Any changed scientific fact, reversed comparison, fabricated evidence, hidden material result, or unsupported causal escalation is `FAIL`. An environment-shared build problem can be conditional if it is demonstrably unrelated to the revision, but the manuscript is not release-ready until resolved.

## Rhetorical-quality score, 0–4 each

- **Evidence framing (25%):** claims are traceable to exact existing evidence, comparison axes, conditions, uncertainty, and limiting results.
- **Novelty stance (20%):** the precise delta from closest work is decisive but calibrated; no unsupported first/SOTA/mechanism claim.
- **Scope (15%):** widest supported scope is stated positively, with important untested conditions separated.
- **Contribution structure (15%):** a small, consistent contribution set guides the abstract, results, limitations, and conclusion.
- **Technical precision (15%):** terminology and formalism remove ambiguity without prestige complexity.
- **Readability (10%):** syntax exposes scientific relations without oversimplification or ornament.

## Peer-review-quality score, 0–4 each

- soundness and claim support (25%);
- contribution, novelty, and significance (20%);
- evaluation and evidence adequacy (20%);
- clarity and organization (15%);
- reproducibility and transparency (10%);
- limitations, ethics, and responsible scope (10%).

Presentation may raise clarity and scientific legibility. It must not raise soundness, contribution, evaluation, or the overall acceptance tier unless existing technical evidence becomes materially more verifiable under the venue rubric. Missing science remains missing.

## Overclaim handling

- Local calibration defect: repair before release.
- Unsupported robustness, consistency, strongest-baseline, significance, mechanism, or broad-scope claim: cap the affected dimension and require a second pass.
- Causal escalation, universalization, omitted counter-result, unfair prior-work comparison, or unsupported priority claim affecting a headline: preservation failure until repaired.
- Changed result, number, sample, ranking, dataset, method, equation meaning, approval, consent, or reversed comparison: automatic failure.

## Outcome labels

- **Robust improvement:** preservation passes and multiple perspectives agree that scientific legibility improves without overclaim.
- **Presentation-only improvement:** clarity or contribution salience improves, while scientific-quality and acceptance tier remain unchanged.
- **No reliable change:** differences lie within reviewer disagreement or tie bands.
- **Reward-hack signal:** a standard evaluator prefers the revision but a strict or preservation evaluator identifies unsupported rhetoric.
- **Regression:** legibility declines or new confusion is introduced.
- **Preservation failure:** any critical invariant fails; the candidate is ineligible regardless of review score.

Report separate reviewer judgments and disagreements. Do not optimize their average or recursively rewrite until they agree.

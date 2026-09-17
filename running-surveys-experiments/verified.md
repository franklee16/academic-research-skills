# Verified Candidates (Stage 1.5 output)

> Triple-verification of candidates from `candidates/`. Each unit that passed V1+V2+V3 enters Stage 2.

## Verification rubric

- **V1 (cross-domain)**: Does the unit appear in 2+ independent contexts in the book? (Different sections/scenarios, not the same example re-cited.)
- **V2 (predictive power)**: Can the unit answer a new question that the book didn't directly discuss?
- **V3 (exclusivity)**: Is the insight non-obvious — i.e., would a random smart person not say this?

---

## Frameworks

### f01 — Three-layer survey integrity — PASS
- V1: whole paper is structurally organized as §2 (questions) → §3 (operations) → §4 (platform); each subsection reinforces the layer
- V2: tells you which layer to fix when a survey fails (e.g., if participants answer but answers don't replicate, the problem is in §2, not §4)
- V3: non-obvious; surveys are commonly treated as one undifferentiated task. The author's claim that *quality breaks at any layer invalidate the next* is counter-intuitive to most newcomers.

### f02 — Respondent's answer = ability × willingness × interpretation — PASS
- V1: three sub-types × multiple examples (privacy on income, memory on behavior, introspection on decision context)
- V2: any new survey design can be classified along these three axes to predict which questions will fail
- V3: most survey-design textbooks focus on wording; the × notation (all three must be satisfied simultaneously) is non-obvious and load-bearing

### f03 — Relative vs. absolute — PASS
- V1: introduced in §2.2 with multiple examples (XYZ probability vs XYZ vs. ABC); also referenced in §2.4 concreteness discussion
- V2: directly tells you which conclusions you can draw from your data, *independent of question framing*
- V3: extremely non-obvious — economists are trained to care about levels; the paper's argument that levels are usually undefendable is counter-cultural to the field

### f04 — Converging evidence — PASS (low confidence)
- V1: §2.3 with worked example; also implicit in §3 (multi-source validation)
- V2: applies to any survey construct — design at least two items per hypothesis
- V3: borderline. *Some* version of "triangulate" is common in psychology/psychometrics. The paper's emphasis in an economics context is novel.
- **Decision**: retained, but bundled with the umbrella "survey-design-checklist" so it doesn't stand alone. The standalone skill (`converging-evidence-design`) is justified by the granular economics-application content, not the general triangulation idea.

### f05 — Clarity / anti-attribute-substitution — PASS
- V1: §2.4 with example + §2.5 cross-reference to ambiguity-driven social desirability
- V2: predicts which abstract questions will yield respondent-judgment-substitution; concrete heuristic for fixing them
- V3: very non-obvious — designers assume clearer = simpler language. The paper's argument is that clearer = *concrete* (named index, named dates, named alternatives).

### f06 — Two-stage field test — PASS
- V1: explicit in §3.1 (pretest with non-economists → pilot 50-100 → full launch)
- V2: guides the operational order of testing
- V3: non-obvious; most researchers skip pretest, or merge pretest and pilot, or analyze pilot for hypothesis results. The three-stage discipline is the actionable insight.

### f07 — Three checks distinguished (attention / comprehension / manipulation) — PASS
- V1: §3.2 with explicit table-like treatment; also referenced in §2.7 in different framing
- V2: directly diagnoses *which* check to use when a problem surfaces. Different checks → different fixes → different implications for the study.
- V3: very non-obvious. Most survey designers treat all checks as one thing ("are they paying attention"). The author's tri-partition is the actionable insight.

### f08 — Selective attrition — PASS
- V1: §3.2, with Zhou & Fishbach 2016 cite, plus implicit in §4 (sample composition differences)
- V2: predicts when a treatment effect is likely confounded with respondent type post-hoc
- V3: very non-obvious — most economists will compute the headline difference and not check drop-out / fail-rate by condition

### f09 — Platform as implicit population choice — PASS
- V1: §4.3 plus §4.4 with multiple example comparisons
- V2: drives platform choice from research question rather than from convenience
- V3: borderline common sense; the specific framing (MTurk ≠ MTurk-via-CloudResearch ≠ Prolific ≠ Lucid) is the actionable insight

### f10 — Reputation as data-quality investment — PASS
- V1: §3.3 + §3.4 with the Turker-review site specifics
- V2: predicts which platform arrangements produce good data over time
- V3: non-obvious — academic researchers usually don't think about their visibility on a marketplace

## Principles (selected)

- p01 (privacy/$ brackets): PASS — specific dollar-bracket heuristic is non-obvious
- p02 (shorten time horizon): PASS — memory-research insight applied
- p03 (make abstract concrete): PASS — concrete technique
- p04 (strip leading framing): PASS — specific technique
- p05 (yes/no → open): PASS — specific technique
- p07 (1-2 attention checks): PASS — diminishing-returns insight non-obvious
- p08 (free-text at end of pilot): PASS — discipline-non-obvious
- p09 (pay screeners): PASS — two-step design non-obvious
- p10 (sensitive questions fail): PASS — list-experiments/alternatives non-obvious
- p11 (don't analyze pilot for hypothesis): PASS — discipline-non-obvious
- p12 (platform-specific pay): PASS — specific norms non-obvious

## Consolidated skill plan (10 atomic skills)

Each candidate unit is folded into one of these 10 skills. The plan is **boundary**-oriented: each skill has a clear single use case, so trigger ambiguity is minimized.

| Skill slug | Backing units | Single-line purpose |
|---|---|---|
| `survey-design-checklist` | f01 + f02 + umbrella | The headline skill — runs you through 7-question checklist before writing each item |
| `clarity-concreteness` | f05 + p03 + p05 | Kill attribute-substitution by replacing abstraction with concreteness |
| `avoid-leading-questions` | §2.5 + p04 + p10 + ce04 + ce08 | Spot and remove demand-bias-inducing framing |
| `relative-vs-absolute` | f03 + c01 + glossary g13 | Know what conclusions your data can actually support |
| `converging-evidence-design` | f04 + c02 | Multi-item per construct (state-vs-revealed / recall-vs-infer) |
| `pilot-protocol` | f06 + p07 + p08 + p11 + c05 | Two-stage field test before full launch |
| `quality-checks-diagnosis` | f07 + g09/g10/g11 + ce06 | Pick the right check for the failure mode |
| `selective-attrition-audit` | f08 + ce09 | Diagnose condition-asymmetric drop-out |
| `platform-selection` | f09 + p12 + c06 + ce11 + ce12 | Match the platform to your target population |
| `fair-pay-and-reputation` | p09 + p12 + c04 + ce12 | Pay screeners, hit platform norms, manage reputation |

## Rejected units (audit trail)

These candidates were extracted but folded into other skills rather than built as standalone skills:

- **f04 by itself** — folded into `converging-evidence-design`. The triangulation idea alone is too generic; the paper's value is the specific *economics-application* elaboration.
- **p06 (counterbalance)** — folded into `pilot-protocol` (Step 3 of pre-flight checklist). Too text-book to be a standalone skill.
- **ce01, ce02, ce03, ce05, ce10, ce11** — folded into B-sections of relevant skills (clarity-concreteness, privacy/recall, etc.).
- All glossary entries (g01–g15) — not skills; embedded in BOOK_OVERVIEW.md and any skill that references them.
- All case entries — embedded as A1 (Past Application) of relevant skills.

## Pass rate summary

- **Extracted**: ~56 candidate units
- **Standalone skills**: 10
- **Rejection rate** (folded / rejected): ~82%
- This is above the expected 30-50%. Justification: the paper is dense-best-practice material with overlapping coverage of the same themes from different angles. Multiple candidates routinely point at the same actionable design surface. Bundling them is more useful than 25 thin skills.

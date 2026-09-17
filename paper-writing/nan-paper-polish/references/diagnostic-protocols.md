# Criterion-specific diagnostic protocols

Use this file before any manuscript diagnosis. It defines how every diagnostic criterion is executed, recorded, merged, and rechecked. The group files define the individual tests.

## 1. Non-negotiable architecture

- Do not give an LLM a generic instruction to inspect all writing dimensions at once.
- Execute each criterion as an isolated pass with its own applicability rule, context window, intermediate representation, decision test, repair boundary, and recheck.
- The same model may run several passes sequentially, but each pass must receive a criterion-specific instruction and produce a separate record.
- A pass may batch several text units for the same criterion. Do not batch unrelated criteria into one unrestricted judgment.
- Diagnostic passes propose actions; they do not independently rewrite the manuscript.
- Merge diagnoses before composition. One underlying defect may receive several criterion labels but only one coordinated repair.
- After composition, rerun every criterion affected by an edit and then run the global regression checks.

## 2. Common preflight

Before any criterion pass:

1. keep the source immutable and create stable section, paragraph, and sentence identifiers;
2. build the meaning lock from [meaning-integrity.md](meaning-integrity.md);
3. index technical terms, abbreviations, citations, labels, figures, tables, equations, numbers, and units;
4. register research questions, major claims, stated contributions, and where each is restated;
5. identify the sections and text spans in the user's requested scope;
6. distinguish deterministic checks from semantic checks.

Use deterministic inspection when possible for locations, first occurrences, abbreviations, number preservation, LaTeX keys, labels, and change coverage. Use semantic reasoning for rhetorical function, logical relation, reader inference, emphasis, ambiguity, and evidence--claim fit.

## 3. Context hierarchy

Select the smallest context that is sufficient for the criterion, not the smallest text fragment available.

| Level | Required material | Typical use |
|---|---|---|
| Manuscript | title, abstract, section order, research questions, claim register | global argument and cross-section consistency |
| Section | all paragraph-function summaries plus relevant raw paragraphs | rhetoric, scope progression, paragraph order |
| Paragraph group | previous, current, and next paragraphs or their function summaries | paragraph relations and topic shifts |
| Full paragraph | every sentence in original order | sentence relations, topic chain, old--new progression |
| Local span | target sentence plus required neighbors and registers | reference, stress position, grammar, terminology |
| Evidence packet | claim, relevant Methods/Results, statistics, limitations, and restatements | evidence--claim, causality, scope, Hedging |

Never evaluate Flow from an isolated sentence. Never evaluate claim strength from a claim sentence without the available evidence packet.

## 4. Criterion record

Every criterion applied to every in-scope unit must return one of:

- `PASS`: inspected and no defect found;
- `ISSUE`: a verified defect supports a direct proposal;
- `QUERY`: the concern cannot be resolved without author intent, unavailable evidence, or a high-risk decision;
- `N/A`: the criterion does not apply to this unit.

Use this internal shape. Compact `PASS` and `N/A` records may omit proposal fields, but the coverage matrix must retain their statuses.

```json
{
  "criterion_id": "SENTENCE-RELATION",
  "status": "ISSUE",
  "location": "Discussion P3 S2-S3",
  "context_used": ["Discussion P3", "P2/P4 function summaries"],
  "observation": "S3 cannot be assigned a valid relation to S2.",
  "test_result": "The text lacks a premise; no connective can make the inference valid.",
  "root_cause": "missing_argument_step",
  "proposed_action": "Ask the author to state the evidential or theoretical link.",
  "dependencies": [],
  "risk_level": "C",
  "meaning_risk": "possible_new_premise",
  "author_confirmation": true
}
```

Do not use `ISSUE` without an exact observation and a failed decision test. Do not use `PASS` merely because no issue was immediately salient.

## 5. Criterion-specific prompt boundary

Each semantic pass must explicitly narrow the model's task. A suitable instruction pattern is:

```text
Audit only SENTENCE-RELATION. Do not evaluate grammar, Hedging,
concision, tone, or general style. Use the complete paragraph and the
adjacent paragraph-function summaries. First label each adjacent
sentence relation. Then return PASS, ISSUE, QUERY, or N/A with exact
locations. If no valid relation exists, mark a semantic or argumentative
gap; do not invent a premise or add a decorative transition.
```

The prompt must name:

1. the only criterion being judged;
2. excluded dimensions;
3. required context;
4. required intermediate representation;
5. the decision threshold;
6. prohibited false repairs;
7. the record format.

## 6. Coverage matrix

Maintain an internal matrix whose rows are criteria and whose columns are the in-scope units. A full-manuscript Standard revision cannot proceed to composition while an applicable cell is blank.

Example:

| Criterion | Introduction P1 | Introduction P2 | Discussion P1 |
|---|---|---|---|
| CRGP | PASS | ISSUE | N/A |
| SENTENCE-RELATION | PASS | ISSUE | PASS |
| HEDGING | N/A | QUERY | ISSUE |

The matrix is an internal completeness control. Show it to the user only when requested or when formal audit mode makes it useful.

## 7. Root-cause merge

The orchestrator merges records before any prose is rewritten:

1. cluster overlapping locations;
2. compare root causes rather than merely comparing proposed wording;
3. identify supporting, conflicting, and dependent diagnoses;
4. order dependencies: macrostructure before local Flow; evidence--claim before Hedging; topic continuity before voice; meaning before concision;
5. create one accepted action that resolves the shared root cause and all connected defects;
6. retain every applicable criterion as an internal tag;
7. route unsupported bridges, ambiguous terms, missing evidence, and high-risk meaning changes to author confirmation;
8. reject duplicate or decorative proposals.

For example, `TERM-INTRODUCTION`, `OLD-NEW`, `TOPIC-POSITION`, and `SENTENCE-RELATION` may all identify one abrupt method introduction. The merge should produce one coordinated repair, not four alternative rewrites.

## 8. Composition boundary

Only the single designated composer may modify the candidate manuscript. It must:

- implement the accepted merged plan;
- make all connected changes required for a complete repair;
- preserve protected content;
- create the original--revision--reason--criteria mapping with each substantive edit;
- make no independent synonym, tone, hedge, sentence-boundary, or structure edits outside accepted records;
- leave unresolved `QUERY` items unchanged or use an explicitly authorized conservative alternative.

## 9. Recheck and stopping condition

After an edit:

1. rerun every criterion whose input or intermediate representation changed;
2. rerun neighboring Flow units after any local edit;
3. rerun cross-section claim checks after any claim-strength edit;
4. update the coverage matrix and change mapping;
5. run the independent completeness, regression, integrity, and traceability checks.

Stop when every applicable unit is `PASS`, corrected through an accepted `ISSUE`, or retained as an explicit `QUERY`; every edit passes regression; and no protected-content discrepancy remains.

## 10. Diagnostic group routing

- Read [rhetoric-diagnostics.md](rhetoric-diagnostics.md) for rhetorical purpose, C--R--G--P, L1--L3, paragraph functions, Gap--Purpose, and cross-section alignment.
- Read [flow-diagnostics.md](flow-diagnostics.md) for global/section Flow, paragraph and sentence relations, topic chains, old--new progression, references, term introduction, topic/stress position, transitions, and parallelism.
- Read [clarity-diagnostics.md](clarity-diagnostics.md) for agent--action, nominalization, subject--verb distance, voice, noun strings, sentence load, grammar, and punctuation.
- Read [epistemic-diagnostics.md](epistemic-diagnostics.md) for claim class, evidence--claim alignment, causality, Hedging, scope, boosters, null claims, attribution, and cross-section strength.
- Read [consistency-diagnostics.md](consistency-diagnostics.md) for redundancy, shell phrases, light verbs, terminology, abbreviations, tense, cross-references, formatting, and target style.

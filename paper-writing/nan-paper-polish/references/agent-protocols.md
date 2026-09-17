# Multi-agent protocols

## Contents

1. Shared rules
2. Criterion isolation
3. Phase A diagnostics
4. Merge gate 1
5. Phase B composition
6. Phase C QA
7. Merge gate 2
8. Diagnostic record schema

## Shared rules

- Use six logical roles: Agent 0 Orchestrator/Single Composer, Agent 1 Rhetoric/Organization Auditor, Agent 2 Flow/Cohesion Auditor, Agent 3 Clarity/Economy/Consistency Auditor, Agent 4 Evidence/Claim/Hedging Auditor, and Agent 5 Independent Completeness/Regression/Integrity Auditor.
- Let Agent 0 own source files, meaning lock, coverage matrix, merge decisions, the only candidate revision, and final outputs.
- Give workers raw manuscript material and the applicable references, not expected findings.
- Do not let multiple workers edit the same manuscript file concurrently.
- Require criterion records from [diagnostic-protocols.md](diagnostic-protocols.md), including status, exact observation, test result, context used, root cause, risk, and confirmation state. A proposed action is required for `ISSUE` and `QUERY`.
- Never use majority vote to override research-integrity risk.
- Treat the epistemic-integrity role as a veto on unsupported strengthening, causal promotion, scope expansion, or invented evidence.
- Keep the original immutable.
- Treat each edit as a hypothesis that must beat the original in a pairwise comparison. Original wording wins ties.
- Treat equations, algorithms, prompts, code, JSON/schema, templates, and other method artifacts as verbatim-protected unless the user explicitly authorizes changing them.

## Criterion isolation

- Give each diagnostic call one criterion-specific protocol and the exact context window that protocol requires.
- Do not ask any diagnostic worker to `check everything`, `improve the paper`, or freely mix its assigned criteria.
- The same worker may execute several criteria sequentially, but it must reset the instruction boundary and create a separate record for every pass.
- Batch multiple text units only when they are being tested under the same criterion.
- Require `PASS`, `ISSUE`, `QUERY`, or `N/A` for every applicable unit. A blank coverage cell is unfinished work.
- Diagnostic workers return records only. They may quote a proposed replacement or structural action, but they never produce an independently revised manuscript.
- Run dependencies in order: rhetoric/structure before local Flow; evidence--claim before Hedging; topic continuity before voice; meaning before economy.

## Phase A diagnostics

Run these roles independently when their criteria do not depend on unresolved upstream structure. Parallelize only dependency-safe passes.

### Agent 1: Rhetoric and organization auditor

Execute separately under [rhetoric-diagnostics.md](rhetoric-diagnostics.md):

- section and paragraph functions;
- `[C][R][G][P]` moves;
- `[L1][L2][L3]` scope narrowing;
- Gap-Purpose alignment;
- research-question consistency across sections;
- duplication, missing functions, and misplaced material.
- Gap--Purpose component alignment;
- literature organization and synthesis.

Return proposals only. Do not line-edit the manuscript. In Focused mode, propose a structural change only when it repairs a specific reader-path failure; do not redesign a defensible argument merely because another organization is possible.

### Agent 2: Flow and Cohesion auditor

Execute separately under [flow-diagnostics.md](flow-diagnostics.md):

- reverse outline and paragraph sequence;
- topic and keyword chains;
- old-new progression;
- topic and stress positions;
- transitions, parallel structures, and summary nouns;
- missing logical steps and abrupt topic shifts.
- ambiguous references and unclear summary nouns;
- technical terms, acronyms, proper nouns, components, and labels that appear before their role is established;
- sentence-to-sentence logical relations.

Never report only `flow is weak`. Identify the broken link and the repair.

### Agent 3: Clarity, economy, and consistency auditor

Execute separately under [clarity-diagnostics.md](clarity-diagnostics.md) and [consistency-diagnostics.md](consistency-diagnostics.md):

- agent--action and nominalization;
- subject--verb distance and sentence load;
- voice, noun strings, ambiguity, grammar, and punctuation;
- redundancy, shell phrases, and light verbs;
- terminology, abbreviations, and tense;
- cross-references, formatting, and explicit target style.

Do not treat awkwardness, sentence length, passive voice, or repeated terminology as defects without the applicable decision test.

### Agent 4: Evidence, claim, and Hedging auditor

Build the required evidence packet and execute separately under [epistemic-diagnostics.md](epistemic-diagnostics.md):

- claim classification;
- evidence--claim alignment;
- causal warrant;
- Hedging and boosters;
- scope and generalization;
- null claims;
- citation and viewpoint attribution;
- cross-section claim strength.

Mark any unsupported strengthening as a blocking integrity issue.
Do not automatically weaken a claim when support is merely unavailable in the supplied excerpt. Separate `verified mismatch`, `safe direct repair`, and `author query`. Audit unnecessary over-hedging as well as overclaiming.

## Merge gate 1

Have Agent 0 merge diagnostic records into a revision plan only after every applicable coverage cell is nonblank.

Resolve conflicts using research integrity, explicit user constraints, defect severity, reader impact, evidence, and meaning risk. Use the following only as a practical tie-breaker:

1. research integrity and evidence;
2. explicit user constraints;
3. rhetorical purpose and idea organization;
4. Flow and Cohesion;
5. sentence clarity;
6. evidence-claim calibration and Hedging;
7. economy and consistency;
8. optional stylistic preference.

Cluster records by overlapping location, then compare root causes and dependencies. Combine supporting diagnoses into one action and resolve conflicts before prose is changed. Preserve all applicable criterion IDs on the merged action.

For each merged action, assign `accept`, `query`, or `reject`. Accept when the records name an exact defect, explain the cost of preserving the original, provide a proportionate and complete repair, and show a clear net benefit. Accept every action that meets these criteria; do not cap the number of changes. Reject duplicate proposals, decorative rewriting, generic academicization, unnecessary hedge insertion, and any proposal whose revision is less natural or merely different.

Put substantive deletion or addition, causal change, scope change, citation change, ambiguous terminology, and unsupported bridge logic into the author-confirmation queue.

## Phase B composition

Use Agent 0 as the single composer to produce the candidate clean revision and an original--revision--reason--criteria mapping. Create a formal ledger only in audit mode.

The composing editor must:

- follow the merged revision plan;
- preserve protected content;
- apply clarity and concision only after structure decisions;
- create a change explanation at the moment of each substantive change;
- use conservative wording for unresolved Level C items;
- avoid adding evidence or citations.
- implement only accepted proposals plus unambiguous Level A corrections;
- make no independent synonym, tone, sentence-boundary, or hedge edits outside the merged plan;
- preserve every untouched span exactly when the source format permits.
- never replace unavailable PDF content with editorial placeholders and call the result a clean manuscript.

For a long manuscript, process sections sequentially or in controlled batches using one shared terminology list, meaning lock, claim register, and change map. Do not concatenate unrelated whole-manuscript rewrites from multiple agents.

## Phase C QA

Use one fresh Agent 5, the Independent Completeness, Regression, and Integrity Auditor. Give it only the original, candidate revision, change mapping, coverage requirements, and applicable protocols.

### Pairwise regression check

For every substantive edit, compare original and revision on accuracy, naturalness, reader-path continuity, concision, and evidential force. Reject or revert an edit when:

- it has no named defect;
- it changes more text than necessary;
- it adds jargon, abstraction, repetition, or false precision;
- it weakens a supported claim or strengthens an unsupported claim;
- its only advantage is preference;
- the original and revision are tied.

### Completeness check

Rerun the applicable criterion protocols and identify any verified issue in the requested scope that the candidate failed to correct. Distinguish genuinely missed defects from optional alternative phrasings. Require Agent 0 to address every missed necessary issue or place high-risk items in the author-confirmation queue. Confirm that no applicable coverage cell is blank.

### Flow and structure regression check

Check whether local editing introduced:

- broken topic chains;
- missing paragraph bridges;
- duplicated or displaced content;
- stress-position mistakes;
- inconsistent section functions.
- unresolved ambiguous references, abrupt term introductions, and relationless sentence jumps present in the original;
- Flow defects that were diagnosed but displaced by lower-priority stylistic edits.

### Epistemic integrity check

Check:

- numbers, definitions, study design, and findings;
- causal strength, uncertainty, and scope;
- hedges and boosters;
- citation and viewpoint attribution;
- cross-section claim consistency.

### Traceability check

Check:

- every substantive difference has an explanation or an intentional mechanical grouping;
- each original excerpt exists in the source;
- each revised excerpt exists in the candidate;
- the original--revision--reason--criteria mappings are accurate and author questions are present when needed;
- formal record types and fields are correct when audit mode is used;
- no unsupported fact, placeholder, or silent protected-content change exists.

Do not tell Agent 5 which defects are expected. Use its output as an independent evaluation surface. Agent 5 may run the three checks sequentially, but they remain one logical audit role.

## Merge gate 2

Have the orchestrator:

1. resolve QA findings using the same priority order;
2. add every missed necessary revision and revert every edit that fails pairwise regression, then update the candidate and change explanations together;
3. rerun affected criteria and verify protected content, coverage, and the original--revision--reason--criteria mappings;
4. run and render the optional ledger only in audit mode;
5. verify unresolved author questions;
6. deliver the clean revision in LaTeX and the change explanations unless the user requested another format.

## Diagnostic record schema

Require each criterion result to include:

```json
{
  "record_id": "D-FLOW-001",
  "criterion_id": "TERM-INTRODUCTION",
  "status": "ISSUE",
  "location": "Introduction, paragraph 2, sentence 3",
  "context_used": ["Introduction P2", "P1 function summary"],
  "observation": "The named component first appears before its role or definition is established.",
  "test_result": "First-occurrence register has no definition or inference path.",
  "root_cause": "abrupt_term_introduction",
  "proposed_action": "Connect the component to the previously introduced framework before naming it.",
  "dependencies": ["PARAGRAPH-RELATION"],
  "risk_level": "B",
  "meaning_risk": "none",
  "author_confirmation": false
}
```

Compact `PASS` and `N/A` records may omit proposal fields but must retain criterion, status, unit, and context. Reject `ISSUE` records that omit exact evidence, use generic style preferences, invent content, or cross the criterion boundary without explaining the dependency.

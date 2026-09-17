# Revision framework

## Contents

1. Six-layer model
2. Criterion-specific diagnostic architecture
3. Meaning lock plus eight revision passes
4. Cross-layer decision rules
5. Framework tags

## Six-layer model

The six layers are equally available diagnostic lenses, not six quotas for editing. In Standard mode, inspect every applicable criterion across the requested scope and correct every verified defect that warrants revision. A clean sentence need not be changed merely because every layer was inspected, but no verified issue should be left unresolved merely to keep the edit count low.

### 1. Rhetorical purpose

Check whether the manuscript explains why the research matters and how the study responds to a defensible problem.

- Mark Introduction moves as `[C]` Context, `[R]` Review, `[G]` Gap, and `[P]` Purpose.
- Verify that Review supports Gap and Purpose answers Gap.
- Remove broad background that does not contribute to the research problem.
- Verify that Abstract, Introduction, Results, Discussion, and Conclusion answer the same research questions.

Use [rhetoric-diagnostics.md](rhetoric-diagnostics.md) for the executable criteria.

### 2. Idea organization

Track scope as `[L1]` general area, `[L2]` sub-area, and `[L3]` key topic.

- Move from general to specific without an unexplained jump.
- Give every section and paragraph one identifiable function.
- Organize literature by question, evidence, method, or position rather than by author list.
- Place necessary context before a new technical concept.

Use [rhetoric-diagnostics.md](rhetoric-diagnostics.md) for scope progression, functions, and alignment.

### 3. Flow and Cohesion

Treat Flow as the reader's experience of moving through a coherent, cohesive text.

- Check global sequence with a reverse outline.
- Keep technical terms and topic chains stable.
- Move from old information to new information.
- Use transitions only when the logical relation is real.
- Use parallel structures for peer items.
- Prefer `this/these + summary noun` over an ambiguous bare `this`.
- Put the current story or backward link in topic position.
- Put emphasis-worthy new information in stress position.

Read [flow-diagnostics.md](flow-diagnostics.md) for the isolated, context-specific tests.

### 4. Sentence clarity

- Use concrete subjects that name the agent, object, method, result, or current topic.
- Put the main action in a verb when nominalization obscures it.
- Keep the grammatical subject and main verb reasonably close.
- Shorten low-information sentence openings.
- Choose active or passive voice according to topic continuity and agency.
- Preserve established technical compounds; unpack ambiguous noun strings.
- Split sentences that carry too many cognitive tasks and merge fragments that repeat low-value material.

Read [clarity-diagnostics.md](clarity-diagnostics.md) for the executable criteria.

### 5. Epistemic calibration

Match claim strength to evidence.

- Distinguish direct observation, association, interpretation, untested mechanism, and extrapolation.
- Preserve causal boundaries, scope, uncertainty, and alternative explanations.
- Use hedges precisely and avoid hedge stacking.
- Remove unsupported boosters such as `clearly`, `obviously`, or `prove`.
- Prevent hedging erosion during concision edits.

Read [epistemic-diagnostics.md](epistemic-diagnostics.md) for evidence packets, the claim ladder, and the executable criteria.

### 6. Economy and consistency

- Delete redundancy, shell phrases, empty metadiscourse, and unsupported intensifiers.
- Prefer direct verbs over light-verb phrases when meaning is unchanged.
- Preserve necessary qualifications, reproducibility details, evidence, and citations.
- Keep terminology, abbreviations, tense choices, voice, numbering, and formatting consistent.

Read [consistency-diagnostics.md](consistency-diagnostics.md) for the executable criteria.

## Criterion-specific diagnostic architecture

Follow [diagnostic-protocols.md](diagnostic-protocols.md). Every criterion has its own applicability rule, context window, intermediate representation, decision test, repair boundary, and recheck. Do not replace these passes with one generic request to improve the manuscript.

For every applicable text unit, record `PASS`, `ISSUE`, `QUERY`, or `N/A` in the coverage matrix. Diagnostic passes propose actions only. Merge overlapping findings by location, root cause, and dependency before the single composer changes any prose.

## Meaning lock plus eight revision passes

### Preflight: Meaning lock

Create a register of protected facts and claims:

- research questions and hypotheses;
- data, numbers, formulas, variables, and units;
- study design and sample;
- causal or associational status;
- uncertainty and scope;
- citations and attribution;
- technical terms.

Classify important claims as observation, association, interpretation, mechanism, or extrapolation.

### Pass 1: Preprocessing and coverage setup

Create stable locations, the term/abbreviation index, research-question and claim registers, cross-reference inventory, and criterion coverage matrix. Write one factual function sentence for each section and paragraph without editing.

### Pass 2: Rhetoric and organization criteria

Run CRGP, L1--L3, section/paragraph function, Gap--Purpose, cross-section alignment, and literature-organization passes independently. Stabilize high-risk structure decisions before local diagnosis.

### Pass 3: Flow and cohesion criteria

Use the context required by each Flow criterion. At minimum, build:

- a reference map for pronouns, demonstratives, and summary nouns;
- a terminology-introduction register for each acronym, proper term, label, and construct;
- a topic chain for consecutive sentences and paragraphs;
- a sentence-relation map using relations such as continuation, contrast, cause, consequence, evidence, example, interpretation, and sequence.

Also run global/section Flow, paragraph relation, old--new, reference resolution, topic position, stress position, transitions, and parallelism as separate passes. Flag a relation only when it is missing, false, ambiguous, or requires unreasonable inference.

Never diagnose Flow from an isolated sentence.

### Pass 4: Evidence, claim, and Hedging criteria

Build an evidence packet for each main claim from the available Methods, Results, statistics, limitations, citations/attribution, and cross-section restatements. Then run claim classification, evidence--claim, causality, Hedging, scope, booster, null-claim, attribution, and cross-section-strength passes independently.

Unknown support is not absent support. If the evidence needed to decide is unavailable, preserve the source claim and ask the author.

### Pass 5: Clarity, economy, and consistency criteria

Run agent--action, nominalization, subject--verb distance, voice, noun-string, sentence-load, ambiguity, grammar, redundancy, shell-phrase, light-verb, terminology, abbreviation, tense, cross-reference, formatting, and target-style passes independently. Distinguish actual defects from optional stylistic alternatives.

### Pass 6: Root-cause merge and complete revision

Cluster records by overlapping location, common root cause, and dependency. Resolve supporting and conflicting findings, retain all applicable criterion tags, and create one coordinated action per root cause. Only then may the single composer implement every accepted proposal. Do not invent premises, evidence, or citations. Put unresolved high-risk changes in the author-confirmation queue.

### Pass 7: Criterion recheck, completeness, and regression gate

For every edit, ask:

1. What exact defect does it fix?
2. What concrete cost remains if the original is kept?
3. Is the repair proportionate to the defect and complete across connected text?
4. Is the revision more accurate, coherent, and natural without avoidable extra length?
5. Did it introduce jargon, false precision, new claims, or a weaker rhythm?

Add or extend a revision when a verified defect remains unresolved. Revert an edit when no defect can be named, the benefit is merely stylistic, or the original and revision are tied after the defect has been resolved. This gate prevents unsupported edits; it does not cap the number of necessary changes.

Rerun every affected criterion with its required context. Reinspect neighboring Flow units after local changes and every cross-section restatement after claim changes. Confirm the coverage matrix contains no blank applicable cells.

### Pass 8: Final consistency and traceability

Verify terminology, abbreviations, tense, voice, citations, cross-references, figures, tables, equations, grammar, punctuation, target-style requirements, protected meaning, and original--revision--reason--criteria traceability.

## Cross-layer decision rules

Resolve conflicts using research integrity, explicit user constraints, defect severity, reader impact, evidence, and meaning risk. When those factors do not resolve the conflict, use this layer order as a practical guide rather than a declaration that one writing dimension is universally central:

1. research integrity and evidence;
2. explicit user constraints;
3. rhetorical purpose and idea organization;
4. Flow and Cohesion;
5. sentence clarity;
6. evidence-claim calibration and Hedging;
7. economy and consistency;
8. optional stylistic preference.

Do not improve Flow by inventing a missing logical premise. Flag the gap. Do not improve concision by deleting uncertainty or scope. Do not vary terminology merely to avoid repetition.

## Edit-density rule

Do not target a number or percentage of changed sentences. High-quality output may contain few or many edits depending on the manuscript. Preserve acceptable source sentences, but correct every verified issue within the requested scope rather than stopping after an arbitrary amount of revision.

## Framework tags

- `[C][R][G][P]`: Introduction moves
- `[L1][L2][L3]`: scope level
- `[FLOW-GLOBAL][FLOW-LOCAL][FLOW-GAP]`: Flow issues
- `[TOPIC-POSITION][STRESS-POSITION][OLD→NEW]`: information placement
- `[AGENT][ACTION][NOM][VOICE]`: sentence clarity
- `[HEDGE][BOOSTER][CLAIM-STRENGTH][SCOPE]`: epistemic calibration
- `[EVIDENCE-CLAIM-MISMATCH][HEDGE-STACK][HEDGING-EROSION]`: claim risk
- `[CUT][MEANING-RISK]`: concision and integrity
- `[PASS][ISSUE][QUERY][N/A]`: criterion coverage status

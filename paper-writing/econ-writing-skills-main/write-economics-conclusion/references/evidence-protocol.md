# Evidence Protocol for Manuscript-Grounded Writing

This protocol is a hard gate. Use it in draft, rewrite, audit, and fact-check modes. It converts a manuscript into a traceable set of claims before prose generation.

## 1. Establish the evidence universe

Inventory every supplied manuscript file and identify versions. Record which file appears current, but do not silently discard conflicting versions. Read the body as the principal evidence source. Treat the introduction, current abstract, conclusion, title, presentation slides, and user notes as claims to verify unless the user explicitly confirms them as authoritative facts.

For a long manuscript, first map sections and then read the full local context of relevant passages. Search helps locate evidence; it does not replace interpretation.

## 2. Classify the paper

Choose one or more:

- causal empirical;
- associational or descriptive;
- measurement;
- structural or quantitative;
- theoretical;
- historical;
- mixed.

This classification controls allowed language. Do not search for an “identification strategy” in a theory paper or treat a structural counterfactual as a reduced-form estimate.

## 3. Build the claim ledger

For every candidate claim, record:

| Field | Meaning |
|---|---|
| `claim_id` | Stable short ID used in the output plan |
| `claim_type` | question, data, design, model, result, mechanism, heterogeneity, null, robustness, limit, implication, contribution, future direction |
| `exact_claim` | Conservative statement of what the source supports |
| `source_file` | File name or user-confirmed source |
| `source_location` | Section, page, table, figure, theorem, or paragraph |
| `support_level` | explicit, strongly implied, author interpretation, absent, conflicting |
| `status` | main, secondary, robustness, exploratory, not eligible |
| `causal_status` | causal, associational, descriptive, theoretical, model-implied, unclear |
| `number` | Estimate or quantity exactly as reported |
| `unit` | Exact reported unit |
| `denominator` | Exact denominator or `not reported` |
| `comparison_baseline` | Exact comparison/baseline or `not reported` |
| `scope` | Population, place, institution, period, outcome, horizon |
| `uncertainty` | Standard error, interval, sensitivity, or qualification when material |
| `mechanism_level` | identified, model-implied, direct test, exclusion evidence, consistent-with, suggestive, speculative |
| `allowed_wording` | Strongest wording the evidence permits |
| `output_priority` | essential, useful, optional, exclude |
| `conflict_or_gap` | What remains unresolved |
| `clause_support` | Evidence for subordinate explanations, appositives, adjectives, and modifiers |
| `evaluation_basis` | Source benchmark for labels such as low-cost, large, substantial, or meaningful |
| `measured_object` | Exact outcome or proxy actually measured |
| `null_status` | Exact null form: no detectable/statistically significant/economically meaningful change, with outcome and specification |
| `forbidden_broadenings` | Unsupported synonyms, umbrella objects, causal/mechanism upgrades, and stronger null restatements |
| `surface_policy` | locked, equivalent, or free |
| `locked_surface` | Exact source span for a constructed sample, eligibility condition, treatment, outcome, proxy, time window, or institutional definition |
| `identified_treatment` | Actually assigned or identified intervention; the only causal subject licensed for the identified treatment effect |
| `identified_outcomes` | Outcomes for which that treatment effect is identified |
| `mechanism_candidate` | Proposed latent channel kept separate from the identified treatment |
| `mechanism_identification_status` | identified, direct-test, supportive, consistent-with, suggestive, or speculative |
| `context_scope` | Exact setting and population that license any opening contextual claim |
| `prevalence_support` | Source evidence for words such as many, often, widespread, or common; absent by default |
| `future_premises` | Exact documented boundary facts that license a future question; empty means omit future work |
| `structural_component` | Exact selection, preparation, equilibrium, or accounting component |
| `component_object` | Ability, preparation effort, entry, quality proxy, surplus, or other object actually changed |
| `component_direction` | Exact reported sign or `ambiguous/not separately signed` |
| `component_relation` | reinforcing, offsetting, separate, or not established; inferred only from reported signs |

The ledger is an internal control object. Show it only in audit or fact-check mode, or when the user asks.

## 4. Verify quantitative claims

Before using a number, verify all of the following:

1. sign or direction;
2. raw unit versus percentage or percentage point;
3. denominator and baseline;
4. estimand and specification;
5. sample and period;
6. whether it is the main estimate, a range, a simulation, or a robustness result;
7. whether uncertainty or a qualifier is necessary to avoid distortion.

Treat every quantitative statement as a closed tuple: value, direction, unit, denominator/baseline, estimand, population, and horizon. Reproduce only tuple members explicitly supplied. Record `not reported` rather than filling a blank from convention or nearby language. If a source reports that a metric changes by 0.18 percent, do not add `of baseline`, `relative to baseline`, or `percentage points` unless explicitly reported.

A number appearing somewhere in the paper is not automatically eligible. It must also be central and interpretable in the target genre.

Preserve the manuscript's technical nouns and classifications. Do not turn `output per employee` into `productivity`, `linked firm-worker panel` into `matched employer-employee data`, or an eligibility threshold into an unreported label such as `mid-sized`. Use a synonym only when it is substantively equivalent and cannot alter the estimand, sample, design, or contribution.

Apply a closed-world paraphrase rule. A supported clause licenses only its exact economic object, scope, causal status, mechanism level, and centrality. It does not license a broader umbrella noun or a stronger interpretation merely because that phrasing is conventional. A winning price is not automatically procurement cost, and a measured proxy is not automatically the underlying construct.

Lock any definition built from an action/status, institution/place, threshold, lookback window, or conjunction of conditions. Preserve the source surface verbatim except for capitalization, punctuation, and surrounding grammar. A behavior-history condition is not an entity-status label. Verify every selected locked surface by normalized-string comparison before delivery.

Do not manufacture a broad motivation sentence. An opening such as `In many procurement markets` asserts prevalence beyond the study and requires its own source evidence. If `prevalence_support` is absent, open with the paper's exact setting, documented actor report, research question, or intervention.

Future research is not exempt from closed-world evidence. Every premise—including an allegedly short horizon, cumulative process, delayed effect, unmeasured outcome, or missing mechanism—must appear in `future_premises`. Absence of evidence about long-run effects does not establish that the observed horizon is too short or that effects accumulate. If the field is empty, omit future work.

Preserve null claims at every repetition. `No detectable change in the reported quality measures` must not become `no effect on quality`, `quality was unchanged`, or `without eroding quality`. Keep the detection or significance qualifier, the measured proxy, the relevant specification, and the scope whenever the null does interpretive work.

## 5. Calibrate causal language

Use the manuscript's design and stated estimand, not the topic, to select verbs.

- **Causal evidence:** `increases`, `reduces`, `causes`, `the effect of` may be available when the design and scope support them.
- **Associational evidence:** prefer `is associated with`, `covaries with`, `predicts`, or descriptive language.
- **Structural/model results:** distinguish estimated objects, calibrated quantities, model-implied mechanisms, and counterfactual predictions.
- **Theory:** state propositions, mechanisms, equilibria, conditions, and comparative statics; do not invent empirical validation.
- **Historical evidence:** preserve the design's actual causal or descriptive status and the relevant institutional scope.

Do not let a causal word in an old abstract override ambiguity or weaker language in the body.

## 6. Calibrate mechanisms

Never collapse these categories:

1. **Identified or directly tested mechanism** — the design separately supports the channel.
2. **Model-implied mechanism** — the result follows inside a stated model under its assumptions.
3. **Exclusion evidence** — alternatives are weakened but the preferred channel is not fully identified.
4. **Consistent-with evidence** — observed patterns fit the mechanism but do not establish it.
5. **Suggestive evidence** — limited or indirect support.
6. **Speculation** — an author interpretation or possible explanation without a test.

Use wording that exposes the category. Omit a weak mechanism when compression would erase the qualification.

Enforce a two-sentence firewall when the treatment is identified but the mechanism is only supportive. Sentence 1 may state what the identified intervention changed, with that intervention as grammatical subject. Sentence 2 may state only that separate patterns are `consistent with` or `suggestive of` the channel. Do not make the channel, friction, or its reduction the subject of `shows`, `causes`, `broadens`, `raises`, or `reduces`; do not write `suggests X drove Y`.

If space cannot accommodate both the weak-mechanism statement and its qualification, omit the mechanism. Never compress by upgrading it.

Structural selection discipline is closed-world. A statement that higher preparation costs affect entry does not establish the average ability of entrants; ability and preparation cost may be separately distributed or jointly selected. Preserve the manuscript's exact conditional statement. Use `offsetting` only for explicitly opposite-signed contributions. When both reported components push an outcome in the same direction, do not call them offsetting; when a component is unsiged, do not invent its sign.

| Evidence level | Safe ceiling | Forbidden upgrade without separate support |
|---|---|---|
| identified/direct mediation | `mediates`, `operates through`, within reported scope | exclusive/only unless established |
| direct test/supportive | `supports the channel`, `provides evidence for` | principal/main, drives, explains |
| consistent-with | `is consistent with`, `supports an interpretation in which` | channel is, principal channel, operates through |
| suggestive | `suggests`, `is suggestive of` | demonstrates, establishes, explains |
| speculative/author interpretation | `the authors discuss/interpret` | present-tense conclusion fact |

`Principal` is a ranking claim, not a stylistic synonym for `consistent with`. A later hedge does not repair an earlier upgrade.

Audit every subordinate clause, adjective, adverb, appositive, and comparison as a separate claim. Delete an explanation attached with `where`, `because`, `especially when`, or `reflecting` unless it has its own ledger support.

Treat `low-cost`, `inexpensive`, `large`, `small`, `substantial`, `modest`, `meaningful`, `important`, `cost-effective`, and similar labels as quantitative comparisons. Use one only when the manuscript provides the benchmark or explicitly makes that evaluation; otherwise report the neutral number.

## 7. Treat contribution and implication as claims

`First`, `new`, `novel`, `unique`, `fills a gap`, and broad contribution statements require explicit and scoped support. Prefer demonstrating contribution through the concrete data, design, object, model, or finding.

Policy and welfare language must respect:

- the studied population and institution;
- equilibrium versus partial-equilibrium evidence;
- observed outcomes versus modeled welfare;
- implementation costs and countervailing effects reported in the paper;
- external-validity limits.

Do not infer a policy command from a local average treatment effect or a model result without the assumptions that connect them.

## 8. Resolve conflicts and missing evidence

When sources conflict on a core direction, number, sample, causal status, or conclusion:

- do not choose silently;
- locate whether one source is an outdated draft, alternative specification, or different estimand;
- ask the user if the conflict changes the target text;
- omit the claim if it is optional and unresolved.

Ask only blocking questions. A blocking issue changes the central research claim, credibility, or interpretation. Do not interrupt for a preference that can be handled with a transparent default.

Never convert “not reported” into “does not exist.” Never create a limitation, null result, or policy analysis because the genre often contains one.

## 9. Plan and audit the output

Before writing, map each planned sentence or title promise to one or more claim IDs. After writing, run both directions:

- **Output to ledger:** every substantive element has support and calibrated wording.
- **Ledger to output:** essential claims and boundaries are not displaced by attractive secondary content.

Any of the following is a critical factual failure:

- wrong number, unit, sign, baseline, sample, period, or object;
- association presented as causation;
- suggestive mechanism presented as established;
- unsupported novelty or contribution claim;
- invented robustness, limitation, citation, implication, or future direction;
- a title promise the body does not deliver;
- a new result introduced in an abstract or conclusion.
- an unreported qualitative label or terminology substitution that changes the economic object, sample, design, or contribution.
- a null restated more strongly than its source or detached from its measured proxy and qualification.
- a broader result noun, welfare object, causal claim, mechanism claim, or contribution than the source licenses.

Critical factual failures cannot be offset by good prose.

For conclusion selection, an `exploratory` claim defaults to exclude. Upgrade it only if it changes the first-order boundary, the manuscript gives it interpretive prominence, and it can be included without speculative explanation.

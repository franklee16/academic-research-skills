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
| `unit_baseline` | Units, denominator, comparison group, baseline, or scaling |
| `scope` | Population, place, institution, period, outcome, horizon |
| `uncertainty` | Standard error, interval, sensitivity, or qualification when material |
| `mechanism_level` | identified, model-implied, direct test, exclusion evidence, consistent-with, suggestive, speculative |
| `allowed_wording` | Strongest wording the evidence permits |
| `output_priority` | essential, useful, optional, exclude |
| `conflict_or_gap` | What remains unresolved |
| `measured_object` | Exact outcome, proxy, price, quantity, index, or welfare object actually measured |
| `forbidden_broadenings` | Nearby but unsupported umbrella terms, synonyms, and causal or mechanism upgrades |
| `locked_sample_definition` | Source-faithful condition including event, geography/institution, lookback period, and threshold |
| `surface_policy` | locked, equivalent, or free |
| `locked_surface` | Exact source span for a constructed sample, eligibility condition, treatment, outcome, proxy, time window, or institutional definition |
| `lock_reason` | constructed_sample, eligibility, treatment, outcome, time_window, proxy, or institutional_definition |
| `locked_scope_tokens` | Population, subgroup, proxy, place, and horizon that must accompany every use of the claim |
| `evaluation_basis` | Explicit source comparison licensing labels such as modest, large, meaningful, or important |
| `assignment_unit` | Unit randomized or assigned to condition |
| `treatment_recipient` | Person, firm, office, or other entity that actually receives the intervention |
| `delivery_actor` | Entity or system delivering the intervention |
| `observation_unit` | Unit at which outcomes are observed |
| `analysis_unit` | Unit used for estimation or inference |
| `identified_treatment` | Actually assigned or identified intervention; required causal subject for treatment-effect and implication sentences |
| `mechanism_candidate` | Proposed channel that cannot replace the identified treatment unless separately identified |
| `structural_component` | Exact selection, preparation, equilibrium, or decomposition component |
| `component_direction` | Exact reported sign or ambiguous/not separately signed |
| `relative_strength` | Explicit reported dominance/offset/share comparison, or `not established` |

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

A number appearing somewhere in the paper is not automatically eligible. It must also be central and interpretable in the target genre.

Preserve the manuscript's technical nouns and classifications. Do not turn `output per employee` into `productivity`, `linked firm-worker panel` into `matched employer-employee data`, or an eligibility threshold into an unreported label such as `mid-sized`. Use a synonym only when it is substantively equivalent and cannot alter the estimand, sample, design, or contribution.

Apply a closed-world paraphrase rule: the ledger licenses only the stated claim and genuinely equivalent wording, not a broader economic object. A winning price is not automatically a procurement cost; an application count is not automatically market participation; a measured proxy is not the latent construct it may imperfectly represent. Preserve the exact measured object or explicitly retain the manuscript's own proxy qualification.

Constructed sample definitions are controlled strings, not opportunities for elegant labeling. Copy the source definition and shorten only by deleting words that do not alter its event, institution/place, threshold, or time window. `Had not bid in the municipality during the preceding three years` cannot become `new to the municipality`, `new firm`, or `new supplier`.

Set `surface_policy: locked` automatically for a constructed group or eligibility definition. Insert `locked_surface` verbatim, allowing only capitalization, punctuation, and surrounding grammatical changes. Before delivery, normalize whitespace and confirm that each selected locked surface appears; if absent, regenerate the sentence rather than judge a synonym informally.

Lock scope-bearing modifiers inside outcomes and quantities, not only the headline noun. Store the population/subgroup, proxy status, place, and horizon as `locked_scope_tokens`; every sentence and closing synthesis using that claim must contain their faithful equivalents. A qualifier stated once does not carry forward implicitly.

Evaluation words require an `evaluation_basis`. Without one, use the neutral reported object or number; do not add `modest`, `large`, `small`, `meaningful`, `important`, or similar labels for rhetorical rhythm.

Treat design roles as a closed tuple. Random assignment at the municipality level does not mean municipalities received supplier alerts. If roles differ, write two propositions: municipalities were assigned to the alert program; verified suppliers in treated municipalities received the notices. Audit subject–verb compatibility (`assigned`, `received`, `delivered`, `observed`, `analyzed`) rather than compressing these roles into one sentence.

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

For `consistent-with`, supportive, or suggestive evidence, select from a closed syntax set: `patterns are consistent with X`, `evidence supports an X interpretation`, or `evidence is suggestive of X`, no stronger than the source. In the same sentence, forbid causal predicates such as `drove`, `explains`, `accounts for`, `operates through`, `mediates`, `because`, and `by reducing`. A leading `suggests` does not weaken a later `drove`.

Enforce an identified-treatment firewall. An identified effect licenses causal language only with `identified_treatment` as grammatical subject. If the mechanism is not separately identified, `reducing X can/does increase Y`, `X expands Y`, and `the findings indicate that X changes Y` are forbidden even in a closing implication. Either state the treatment effect (`timely alerts increased participation`) or use a separate weak-mechanism sentence (`portal and survey patterns are consistent with reduced information frictions, but do not establish that channel`). If both do not fit, omit the mechanism.

Structural component relations are closed-world. Do not infer that preparation dominates selection, that selection offsets preparation, or that one channel outweighs another from the sign of a single counterfactual. The theoretical net effect may remain ambiguous because it depends on a joint distribution even when an estimated counterfactual produces a signed outcome. Use relative-strength language only when the source explicitly supplies it.

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
- a broader result noun, welfare object, causal claim, mechanism claim, or contribution than the source licenses, even when it sounds like a natural summary.

Critical factual failures cannot be offset by good prose.

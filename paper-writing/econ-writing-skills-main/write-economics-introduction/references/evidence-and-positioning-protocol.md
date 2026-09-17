# Evidence and Positioning Protocol for Economics Introductions

Use this protocol in draft, rewrite, outline, audit, fact-check, and positioning modes. It separates what the manuscript establishes from how the paper may truthfully position itself. The first is a manuscript-evidence problem; the second is a relationship between the manuscript and verifiable prior work.

## Contents

1. Establish the evidence universe
2. Classify the paper and evidence
3. Determine readiness
4. Build the manuscript fact ledger
5. Build the literature and positioning ledger
6. Build the contribution comparison matrix
7. Preserve hierarchy and scope
8. Calibrate design, causal, model, and mechanism language
9. Verify citations, gaps, and novelty
10. Verify motivation and contextual claims
11. Control introduction promises
12. Resolve conflicts and missing evidence
13. Plan and audit the output

## 1. Establish the evidence universe

Inventory every supplied manuscript file and identify versions. Record which appears current, but retain conflicts until they are resolved. Read the body as the principal source for what the paper actually delivers. Treat the current introduction, abstract, title, conclusion, slides, referee responses, and author notes as claims to verify unless the user explicitly confirms a fact.

Inventory all positioning materials separately: bibliography files, literature reviews, cited papers, research notes, annotated references, search results, and user-confirmed statements. Record whether the full source, an abstract, a bibliographic entry, or only an author note is available. These evidence levels are not interchangeable.

For long manuscripts, first map sections and then read the full local context of relevant passages. Search locates evidence; it does not establish an estimand, mechanism, contribution, or literature relationship.

Do not let a polished introduction or a remembered literature claim override a narrower statement in the paper body or cited source.

## 2. Classify the paper and evidence

Choose one or more paper types:

- causal empirical;
- associational or descriptive;
- structural or quantitative;
- theoretical;
- historical;
- measurement;
- mixed.

For each candidate claim, distinguish causal evidence, association, description, measurement, theoretical result, estimated structural object, model-implied mechanism, and counterfactual prediction. A mixed paper may use different evidence types for different claims; do not assign one causal label to the entire paper.

For a theoretical or structural model, inventory its ontology before drafting: actors; objects and whether they are observed or latent; information sets; timing; available actions; contractible variables; resource and feasibility constraints; equilibrium concept; propositions; parameter conditions; comparative statics; and any intuition explicitly supplied by the manuscript. Mark an unreported cell `unknown`. Do not fill it with the conventional version of a familiar model.

## 3. Determine readiness

Assess five dimensions:

| Dimension | Ready when | Conservative-ready when | Blocked when |
|---|---|---|---|
| Research identity | Question and paper type are stable | One secondary emphasis remains open | Competing versions imply different questions |
| Principal answer | Direction, object, and status are clear | Optional quantities or secondary results are missing | Main result, proposition, or counterfactual is missing or conflicting |
| Credibility | Design variation, measurement solution, or model logic is interpretable | Technical detail is incomplete but the claim ceiling is clear | Causal versus associational or observed versus model-implied status is unresolved |
| Positioning | Closest relationships and citations are verified | Concrete contribution is supportable but global novelty is not | The user requires final gap/priority claims with no verifiable literature basis |
| Delivery | Requested genre and language are clear | Journal, roadmap, or exact length is unspecified | Output requirements conflict in a way that changes the artifact |

Proceed in a conservative-ready state by omitting unsupported positioning, not by inserting placeholders or familiar gap language. Ask only when the blocked item would change the introduction's central identity, answer, credibility, or requested final positioning.

## 4. Build the manuscript fact ledger

Record one row for every claim that might enter the introduction:

| Field | Meaning |
|---|---|
| `claim_id` | Stable identifier for planning and audit |
| `claim_type` | motivation, question, setting, data, design, model, result, mechanism, null, heterogeneity, robustness, boundary, implication, contribution |
| `exact_claim` | Conservative statement the body supports |
| `source_type` | manuscript fact, external fact, model assumption, model result, author interpretation, or logical transition |
| `semantic_role` | data granularity, specification component, measured outcome, latent object, model result, proof intuition, literature-set classification, selection evidence, external-validity boundary, risk-status statement, or other exact role |
| `source_file` | Manuscript or user-confirmed source |
| `source_location` | Section, page, table, figure, proposition, theorem, or paragraph |
| `support_level` | explicit, strongly implied, author interpretation, absent, conflicting |
| `source_reported_status` | primary, secondary, exploratory, robustness, unspecified |
| `causal_status` | causal, associational, descriptive, theoretical, model-implied, counterfactual, unclear |
| `number` | Exact reported estimate or quantity |
| `unit_baseline` | Unit, denominator, comparison, normalization, or baseline |
| `scope` | Population, place, institution, occupation, period, outcome, and horizon |
| `uncertainty` | Interval, sensitivity, equilibrium selection, assumption, or other material qualification |
| `measured_object` | Exact outcome, proxy, index, price, welfare object, or latent model object |
| `design_roles` | Assignment unit, recipient, delivery actor, observation unit, and analysis unit when relevant |
| `identified_treatment` | Exact intervention or variation the design identifies, including all bundled components |
| `question_subject` | Exact subject the research question is allowed to name |
| `effect_subject` | Exact subject of any causal or comparative effect statement |
| `method_component` | Fixed effect, cluster, instrument, timing, comparison, or other design component exactly as reported |
| `source_authorized_role` | What the source explicitly says that component controls, identifies, absorbs, or permits |
| `mechanism_level` | identified, directly tested, model-implied, exclusion evidence, consistent-with, suggestive, speculative |
| `mechanism_candidate` | Exact candidate channel, kept separate from the identified treatment |
| `null_scope` | Population, outcome or proxy, horizon, power or precision, and detection limit attached to a null |
| `object_identity` | latent construct, observed proxy, realized outcome, estimated object, or counterfactual statistic |
| `reported_result` | Exact result or proposition supplied by the source |
| `authorized_explanation` | Source-stated explanation or intuition; blank when absent |
| `explanation_status` | proved, model-implied, suggestive, or absent |
| `evaluation_basis` | Author wording or explicit benchmark licensing a size, importance, cost, robustness, or policy judgment |
| `observed_pretrend` | Exact pre-existing pattern actually shown |
| `authorized_selection_interpretation` | Source-supported statement about selection; otherwise only the existence of selection risk |
| `allowed_wording` | Strongest wording the evidence permits |
| `forbidden_broadening` | Nearby causal, scope, object, welfare, mechanism, or centrality upgrades |
| `introduction_priority` | core, boundary-changing, useful, omit |
| `conflict_or_gap` | What remains unresolved |

Preserve exact technical nouns when a smooth synonym could change the economic object. A measured price is not automatically cost; an application rate is not automatically market participation; an observed proxy is not the underlying latent quality; a model-implied decision is not directly observed behavior.

Treat object identity as a semantic lock, not a one-time definition. A latent construct, observed measure, realized outcome, estimated object, and model counterfactual may be related, but none may silently stand in for another in a later sentence. Repeat the precise object when a broader synonym would change what was observed or inferred.

Lock the full meaning of fragile claims: number, direction, unit, denominator or baseline, population, institution, horizon, and evidence status. A qualifier stated in one paragraph does not automatically govern a later restatement.

Treat every derived quantity as a new claim. Do not translate a percentage point into days, dollars, standard deviations, people affected, annualized values, or shares of a baseline unless the evidence universe supplies every conversion input and authorizes the relevant population and horizon. Recompute the transformation and preserve its assumptions. When any input is missing, use the reported magnitude rather than an intuitive calculation.

Separate a reported result from its explanation. A theorem, estimate, comparative static, or counterfactual can be reported at its stated conditions without explaining why it holds. Use a source-stated intuition only at its recorded strength. If `authorized_explanation` is empty, do not create a mechanism through an added compound noun, prepositional phrase, causal clause, physical channel, or familiar proof story.

## 5. Build the literature and positioning ledger

For every citation-dependent statement, record:

| Field | Meaning |
|---|---|
| `citation_id` | Stable identifier or bibliography key |
| `bibliographic_identity` | Authors, year, title, outlet or version |
| `source_available` | full text, relevant excerpt, abstract only, bibliography only, author note, unavailable |
| `source_location` | Page, section, theorem, table, or passage supporting the relationship |
| `neighboring_claim` | Exact introduction statement the citation would support |
| `literature_role` | context, closest precursor, theory source, method precedent, data precedent, mechanism evidence, contrast, synthesis |
| `prior_work_claim` | Conservative statement of what the prior work does or finds |
| `data_type` | Survey, administrative, experimental, archival, model, or other source type only when verified |
| `design_or_identification_unit` | Randomization, assignment, comparison, or identification unit only when verified |
| `treatment_or_model_change` | Exact intervention, variation, assumption, or model feature in that source |
| `sample_level` | Verified population, institution, geography, and period |
| `outcomes` | Exact verified outcome objects |
| `source_term` | Exact category or institutional label used by the source |
| `classification_relation` | Parent, child, overlap, mutual exclusion, or difference only when the source verifies that relation |
| `comparison_axis` | question, object, data, design, measurement, model, mechanism, setting, population, result, or interpretation |
| `relationship_to_this_paper` | extends, distinguishes, applies, measures, identifies, unifies, revisits, contradicts, complements, or other exact relation |
| `comparison_universe` | Named papers, verified literature stream, documented search scope, or whole field actually examined |
| `meta_relation_claim` | Any claim that literatures are separate, ignored, disconnected, unified, or bridged |
| `support_level` | verified, partially verified, author characterization, unverified, conflicting |
| `allowed_positioning` | Strongest wording the available source licenses |
| `citation_status` | eligible, needs verification, omit |
| `version_issue` | Working paper, published version, title change, duplicate, or unresolved identity |

A bibliography-only source licenses a citation key and identity check, not a substantive characterization. An abstract may support a high-level question or finding but usually cannot establish a nuanced statement about identification, mechanisms, limitations, or exactly how the current paper differs.

Map each literature sentence to all citations needed for its clauses. A citation cluster does not license a synthetic claim unless the constituent sources jointly support it.

Apply an attribute lock to every cited study. Do not infer its data type, randomization or identification unit, sample level, treatment, outcomes, or limitations from a title, setting, sample count, or analogy to the current paper. Mark a missing attribute `not established`. Never stitch an attribute or baseline from one cited study into another cited study or into the current paper's treatment.

Preserve exact category labels. `Middle school`, `secondary school`, `elementary school`, institution types, occupation groups, policy regimes, and geographic units may overlap or nest differently across settings. Unless the source verifies a hierarchy or mutual exclusion, list the exact categories rather than claiming one study did not examine the other's category.

## 6. Build the contribution comparison matrix

Use one row per proposed contribution:

| Field | Meaning |
|---|---|
| `contribution_id` | Stable identifier |
| `this_paper_adds` | Specific data, design, measurement, model, mechanism, setting, finding, or synthesis |
| `body_support_ids` | Manuscript claims that deliver the addition |
| `comparison_set` | Verified citations or defined literature stream |
| `comparison_axis` | Exact dimension on which the paper differs |
| `prior_state` | What the cited work establishes on that dimension |
| `increment` | What is newly learned or made possible here |
| `why_it_matters` | Economic or inferential consequence of the increment |
| `scope` | Population, setting, theory class, method, or outcome for which the comparison holds |
| `novelty_confidence` | verified narrow, concrete difference only, unverified, conflicting |
| `allowed_wording` | Strongest defensible contribution sentence |

Both sides must be supported. Body evidence alone cannot establish novelty; literature evidence alone cannot establish that the manuscript delivers the claimed advance.

Contributions need not appear as a numbered list or a standalone paragraph. They may be integrated with results and literature when that improves the argument. Distinct contributions should differ in substance, not split one contribution into several rhetorical claims.

A paper's joint treatment of several margins supports a positive description of that joint object. It does not prove that a result is invisible, impossible, or unavailable when any one margin is studied separately. Reserve necessity and impossibility comparisons for an explicit proposition or verified source comparison.

## 7. Preserve hierarchy and scope

Copy the manuscript's reported primary, secondary, exploratory, and robustness hierarchy. Source-reported status overrides the writer's impression that a result is surprising or attractive.

Preserve research-status labels exactly. Evidence weakness can lower `allowed_wording`, but it cannot create a source-absent label such as exploratory, robustness, validation, or formal limitation. Likewise, do not invent an external-validity concern, generalizability list, or future-research agenda merely because such material often closes an introduction.

The introduction spine should use primary claims. A secondary or exploratory claim may enter only when it changes the central interpretation and can carry its qualification without displacing the main answer. Routine robustness belongs in the body unless it addresses the first threat a reader must resolve to trust the headline result.

Preserve exact population, place, institution, occupation, period, and outcome scope. A municipal setting does not license a public-sector-wide claim; selected states do not imply national representativeness; one occupation does not define an entire labor market.

Treat prevalence and importance language as factual. `Many`, `often`, `widespread`, `common`, `central`, and `important` need evidence for the claimed universe. If support is absent, open with the exact setting, documented fact, economic tension, or research question.

## 8. Calibrate design, causal, model, and mechanism language

Use the source of variation or interpretation rather than a method label alone. State what was assigned, compared, measured, modeled, or varied and why it speaks to the claim.

- Causal designs may license effect verbs only for the identified treatment, outcome, population, and estimand.
- Associational studies should use relationship or descriptive language and make selection limits visible when material.
- Structural papers must distinguish observed moments, estimated objects, model-implied mechanisms, and counterfactual predictions.
- Theory papers should state mechanisms, propositions, cases, and conditions without inventing empirical validation.
- Historical studies should preserve the actual design status, period, and institution.
- Measurement papers should distinguish the measure, validation evidence, and latent construct.

Keep identified treatments separate from candidate mechanisms. A randomized alert may increase participation even when reduced information frictions are only a supported interpretation. A closing or contribution sentence cannot substitute the mechanism for the treatment.

Track causal subjects across every rhetorical position, not only result sentences. The hook, research question, answer, mechanism discussion, literature comparison, implication, contribution, and closing must all retain the identified treatment as the effect-bearing subject. For a bundled treatment, evidence consistent with timing, personalization, information, salience, or another component does not identify that component separately. State the bundle's effect first and put candidate mechanisms in a separate, evidence-calibrated sentence.

A method component may be named exactly as reported, but its study-specific role may be explained only when `source_authorized_role` is supported. Do not automatically gloss fixed effects as seasonality, clustering as correction for a named dependence structure, an instrument as satisfying exclusion, or a pretrend as identifying the selecting type. If the source shows only a pre-existing trend, state the trend and its limit on causal interpretation; do not infer who selects, why, or which latent trait explains selection.

Treat statistical and design labels as opaque when their role is not supplied. Do not infer what a fixed effect absorbs, which exact variation remains, what a control removes, what an instrument identifies, or which pattern a pretrend reveals from statistical convention alone. Naming the reported specification is sufficient.

A calendar label in a fixed effect does not establish observation frequency. `Month fixed effects` do not license `monthly data`, a seasonal interpretation, or a claim that all remaining variation is within unit over time. Those are separate empirical attributes and require separate source support.

Audit evaluative modifiers as evidence-bearing claims. Size, importance, modesty, efficiency, stability, precision, cost-effectiveness, welfare desirability, and policy attractiveness require an author statement or explicit benchmark in `evaluation_basis`. Without one, report the exact magnitude, interval, sensitivity, or object and let the reader evaluate it.

Never infer structural component directions, dominance, offsetting relations, equilibrium uniqueness, or external validity from the sign of one counterfactual. State model dependence and conditions where they change interpretation.

## 9. Verify citations, gaps, and novelty

Before using a citation, verify:

1. bibliographic identity and relevant version;
2. that the cited source is available at a level sufficient for the claim;
3. the exact clause it supports;
4. whether the current paper's characterization is fair;
5. whether the citation belongs adjacent to that clause;
6. that the citation key exists in the supplied bibliography when formal keys are used.

Do not invent authors, years, titles, outlets, findings, methods, or citation keys. Do not cite a paper solely because it is topically related.

Treat gap and priority language as higher-burden claims:

- `no work`, `first`, `only`, and `unique` normally require evidence beyond a small curated bibliography;
- `little is known`, `few studies`, and `understudied` still assert a literature distribution and require support;
- `fills a gap` requires a verified gap and a body result that fills it;
- `to our knowledge` lowers rhetorical confidence but does not supply evidence.

When comprehensive support is unavailable, describe the concrete relation instead: what prior work studies, what this paper changes, and why the comparison matters. Specific difference is often more informative than priority language.

Literature-size and trend labels are distributional claims too. `Small`, `nascent`, `growing`, `large`, `extensive`, `burgeoning`, and `a vast literature` require evidence about the relevant literature universe. A packet containing three verified papers establishes three usable comparisons, not that the literature has exactly three papers or is small.

Do not infer a within-paper causal comparison from effect sizes reported by different studies. Differences in population, treatment, design, outcome, or sampling may explain different estimates. Cross-study magnitudes can provide a documented benchmark, but they do not establish that the current paper's timing, personalization, setting, or design caused the difference unless the evidence directly supports that conclusion.

Limit meta-relations to the verified comparison universe. A few neighboring papers can support paper-specific differences; they do not establish that whole literatures were previously separate, disconnected, silent, or unified for the first time. When that wider relation is not independently verified, state the concrete connection the current paper makes without a historical claim about the field.

If the user requests external literature verification and suitable search tools are available, use primary papers or authoritative versions. Record what was actually read. Search-result snippets are discovery aids, not final support for nuanced positioning.

## 10. Verify motivation and contextual claims

A hook is part of the evidence universe. Verify statistics, historical facts, institutional rules, quotations, prevalence claims, policy descriptions, and asserted puzzles before using them.

The same rule applies to plausible context that is not presented as a citation. General knowledge about an industry, a region, a policy debate, institutional practice, or likely behavioral response remains outside the closed evidence universe unless the user requests and authorizes external verification. Do not use such context to make a synthetic or incomplete manuscript sound more realistic.

Do not invent illustrative confounders, omitted variables, mechanisms, implementation details, or alternative explanations. If the manuscript establishes selection but does not name its sources, write `time-varying differences may remain` or preserve the manuscript's own language; do not supply examples such as wages, management quality, training, preferences, or local shocks. Likewise, do not call an estimate `robust`, `stable`, or `precise` without the reported checks or uncertainty that license the description.

Keep a null's qualification locally attached every time it matters. A null for a selected sample, proxy outcome, short horizon, underpowered analysis, or imprecise estimate may not later become an unqualified statement of no effect. Put the relevant population, object, horizon, and detection or precision boundary in the same main claim.

When evidence is sparse, begin from a supplied research task, exact sample contrast, descriptive fact, or theoretical possibility. Do not manufacture an industry routine, real-world trend, generic causal chain, or illustrative life constraint to make the opening feel broad.

Preserve supplied thresholds and categories rather than replacing them with approximate prose such as `weeks in advance` or `a few days` when the exact comparison is `at least 14 days` versus `less than 7 days`. State the study's exact sample boundary without adding an unsupplied external-validity claim or prescribing what future research must do.

Do not manufacture a broad opening because introductions conventionally begin with importance. A paper can open with:

- a documented fact or contrast;
- an explicit unresolved question;
- a real theoretical tension;
- a distinctive identification opportunity;
- a measurement obstacle;
- the paper's central answer when it creates the clearest entry.

The hook should create the need for the paper's question. It should not merely decorate the topic or promise more drama than the evidence supplies.

## 11. Control introduction promises

Build a promise-delivery map:

| Introduction promise | Claim or contribution IDs | Body delivery location | Status |
|---|---|---|---|
| Research question answered | | | delivered / partial / absent / conflicting |
| Design or model capability | | | delivered / partial / absent / conflicting |
| Headline finding | | | delivered / partial / absent / conflicting |
| Mechanism or interpretation | | | delivered / partial / absent / conflicting |
| Contribution | | | delivered / partial / absent / conflicting |
| Scope or policy implication | | | delivered / partial / absent / conflicting |

Reject a promise marked absent or conflicting. Weaken or omit a partial promise unless the limitation can appear naturally with it.

Also audit in reverse: ensure the paper's principal answer and the information that makes it credible are not omitted while secondary content receives space. The introduction need not reproduce every result, but it must identify the same paper that the body delivers.

## 12. Resolve conflicts and missing evidence

When sources conflict on a central number, direction, sample, design, proposition, counterfactual, causal status, citation characterization, or contribution:

- determine whether the conflict reflects an outdated draft, alternative specification, different estimand, or source version;
- do not choose the rhetorically stronger version by default;
- ask the user when the resolution changes the central introduction;
- omit the claim when it is optional and unresolved.

Ask source-specific questions. `Table 4 reports X while the current conclusion reports Y; which is the final main estimate?` is useful. `Please provide more context` is not.

Never convert `not supplied` into `does not exist`. Missing literature evidence does not prove a gap, and missing robustness evidence does not prove fragility.

## 13. Plan and audit the output

Before prose, map each paragraph function and substantive sentence to manuscript claim IDs and, where applicable, citation IDs. Let rhetoric vary after the semantic plan is stable.

After prose, run four semantic checks:

- **manuscript truth:** every paper claim preserves its object, strength, hierarchy, and scope;
- **citation truth:** every cited relationship is traceable to a source sufficient for that characterization;
- **positioning truth:** every gap and contribution comparison has support on both sides;
- **promise truth:** every advertised result or contribution is delivered by the body.

Any failure in these four categories is a hard failure. Natural prose, an elegant hook, or correct length cannot compensate.

Use exact-surface locking only for fragile definitions, technical objects, constructed groups, or formal quantities where paraphrase changes meaning. Otherwise enforce semantic equivalence rather than forcing repetitive source wording.

Keep ledgers internal in draft and rewrite modes. In audit, fact-check, or positioning mode, show only the mappings and conclusions useful for revision, not hidden reasoning.

The classification, readiness state, spine, ledgers, comparison matrix, and audit results are internal control objects. In draft or rewrite mode, the output must begin with manuscript prose and contain no process preamble or post-hoc audit unless a material unresolved risk genuinely requires a brief note outside the formal introduction.

Before rendering, perform a claim-span provenance pass. Split the draft into every externally testable span: main clauses, compound nouns, adjectives and adverbs, category relations, prepositional explanations, causal and purpose clauses, intuition, transitions, pronouns that summarize an earlier claim, and user-facing risk statements. Each span must map to `source_type`, `semantic_role`, `exact_claim` or `source_term`, `source_location`, `support_level`, `authorized_explanation`, and the relevant comparison universe. The source and output roles must match: a specification component cannot support a data-granularity claim merely because both contain `month`, and a joint model cannot support an impossibility claim about models outside the evidence universe. Bind `this pattern`, `this result`, `reverses`, `offsets`, and other relational language to an exact antecedent claim ID. Delete any span that depends only on plausibility.

Preserve support status in all user-visible content. Use the distinctions `supported`, `partially supported`, `unsupported`, `unverified`, `contradicted`, and `conflicting`; do not report an unverified literature claim or unevaluated policy as contradicted, and do not report absence of analysis as evidence of no effect.

Use evidence exhaustion as a stopping rule. After the supported question, result, necessary credibility boundary, and eligible mechanism or positioning are expressed, do not fill a missing conventional module with generic future work, unreported generalizability limits, a new contribution label, or a policy agenda.

Audit after rendering the complete response, not only before drafting the note. First draft the English introduction; then render any necessary risk note from a private `note_ledger` containing `missing_source_type`, `affected_claim_type`, `support_status`, and `safe_user_message`; combine both; and rerun claim-span, semantic-role, and support-status checks across everything the user will see. The note must not bypass the final audit.

In a conservative-ready response, keep any external risk note concise: identify the unavailable source content and the exact kind of claim that remains unsupported. Do not turn the note into a claim-by-claim audit or repeat the reasoning already embodied in omissions.

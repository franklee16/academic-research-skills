# Introduction Patterns by Economics Paper Type

Examples and type patterns in this file are diagnostic counterexamples and expression aids, not evidence or completion rules. Classify the current paper from its own materials before reading a type section. Never import an example's actors, timing, mechanisms, institutional facts, model primitives, or missing-data expectations into the current paper, and never change a frozen fact-ledger field merely because a familiar paper type usually contains it.

Classify the paper before planning its introduction. Use the dominant inferential burden, not the author's field label. A labor paper may be primarily structural; a health paper may be primarily measurement; a historical paper may use a causal design. If two burdens are indispensable, use the mixed-paper protocol rather than forcing one template.

Every type still needs the same invariant spine:

`why this question arises -> what the paper asks -> what the paper does -> what it finds -> why the reader should believe and care about that answer`

The type determines what counts as credibility, what result language is admissible, and which details deserve space.

## 1. Causal empirical papers

### Central burden

Convince the reader that the identifying variation supports the causal claim and that the estimated object answers the stated economic question.

### Useful progression

`substantive tension -> causal question -> setting and treatment/comparison -> identifying variation -> main effect with scale -> decisive mechanism, null, or alternative-design evidence -> scope and implication -> literature relationship -> optional roadmap`

Name the source of variation rather than only the estimator. Explain only the source-authorized assignment, discontinuity, policy change, instrument, timing, or comparison that moves treatment. State an identifying assumption, its role, or the reason a second design changes credibility only when the manuscript itself supplies that interpretation. For a randomized study, the exact assignment fact and unit are sufficient; do not add which characteristics randomization balances, why preregistration reduces discretion, or why delivery mechanics strengthen compliance unless those claims are sourced.

Preserve treatment, outcome, unit, population, period, estimand, uncertainty, and causal scope. An association used as mechanism evidence must remain an association. A null must retain its detection and precision qualifications. Include robustness only when it addresses the principal live threat, not as a checklist.

Keep an identified intervention as the grammatical and conceptual subject of the research question, answer, and contribution. If the intervention bundles timing, personalization, information, delivery, or salience, supportive evidence about one channel does not license rewriting the paper as the causal effect of that channel. Cross-study differences do not unbundle the treatment. Attach any null's sample, proxy, horizon, and detection or precision boundary to the null claim itself.

### Avoid

- presenting `IV`, `RDD`, `DiD`, or fixed effects as self-validating labels;
- calling quasi-random variation randomized;
- turning suggestive heterogeneity into a causal mechanism;
- reporting many outcomes without an ordered economic story;
- generalizing beyond the treated population, institutional setting, or variation.

## 2. Structural and quantitative papers

### Central burden

Explain why the economic question requires a model, which margins and data discipline the answer, and which conclusions are observed, estimated, calibrated, or counterfactual.

### Useful progression

`economic tradeoff or policy problem -> why reduced-form evidence is insufficient -> essential model margins -> data and parameter identification -> model fit or empirical discipline -> principal counterfactual or welfare result -> decision-changing sensitivity or limitation -> literature relationship -> roadmap when the sequence is complex`

Describe only the model primitives needed to understand the answer. Connect each essential parameter to its source of empirical discipline. Make the transition from estimates to counterfactual explicit. State whose welfare is measured, the policy regime, equilibrium response, baseline, and scenario assumptions when they determine interpretation.

Maintain separate names for latent model objects, observed moments or proxies, estimated parameters, realized outcomes, and counterfactual statistics. A counterfactual value may inform a latent concept without becoming a direct measure of it. Report magnitudes without labels such as modest, large, efficient, or attractive unless the source provides a benchmark for that evaluation.

Never label an observed measure a `proxy` for a latent construct unless the manuscript explicitly defines that measurement relation. If the manuscript reports realized output and separately models latent quality, keep both names rather than using one parenthetically to define the other.

Reuse the source's exact object names when reporting costs, welfare components, physical outcomes, and model statistics. A near-synonym may imply a different accounting object, and a welfare component does not license an unreported physical channel that generates it.

Second-layer results deserve space when they establish model fit, distinguish a margin responsible for the counterfactual, or show that the policy ranking survives a consequential alternative. Routine estimation detail and a catalogue of auxiliary counterfactuals belong later.

### Avoid

- presenting model output as directly observed evidence;
- hiding the policy conclusion behind a long inventory of equations or estimation steps;
- omitting an equilibrium margin that reverses the result;
- reporting welfare numbers without the population, baseline, policy instruments, and maintained assumptions;
- using the structural model merely as a novelty label.

## 3. Pure theory papers

### Central burden

Show the paper's exact theoretical question, environment, central characterization, conditions, source-authorized intuition, and verified relation to neighboring models. Do not presume that existing theory cannot organize the phenomenon unless the supplied literature evidence establishes that claim.

### Useful progression

`supported theoretical tension -> new environment and key primitives -> main equilibrium characterization -> conditional cases or comparative statics -> source-authorized intuition, if supplied -> distributional or organizational consequences -> extensions and boundaries -> exact relationship to neighboring theories`

State assumptions when they create the result, not as a complete model specification. Organize propositions around economic cases and only the intuition the source actually supplies. Replace empirical-magnitude requirements with clear conditional claims: who changes behavior, in which direction, and under what reported parameter or resource condition. Add an equilibrium force only when it is stated or proved in the supplied manuscript.

Before explaining intuition, freeze the model's stated information structure, timing, action set, contractibility, constraints, and result conditions. Do not invent a standard principal-agent timeline, assign private information to an actor, describe an unreported screening action, or infer a proof step simply because it would rationalize the proposition. If the packet states the comparative static but supplies only limited intuition, explain only that supplied force and leave the rest to the model section.

Distinguish a model possibility from a real-world fact. In the absence of verified external evidence, introduce an imperfect or scalable technology as the environment studied or an economic possibility, not as an increasingly common practice, typical imperfection, or documented trend. Report a proposition without an added `because` explanation when the manuscript supplies no authorized intuition.

Connect neighboring theories by the verified dimensions of comparison. Do not infer that whole literatures were previously separate, disconnected, or unified for the first time from a finite packet of nearby papers.

Do not infer from a paper's joint determination of several margins that the core result would be invisible or impossible if any margin were studied alone. That necessity claim requires an explicit proposition. Preserve the exact comparative static: if low precision reduces delegation, do not describe it as reversing an ability-delegation ranking unless the model states that ranking reversal.

An extension belongs in the introduction when it tests whether the central result depends on a defining assumption, such as resource scarcity, autonomy, market structure, information, or communication technology. A separate related-literature subsection is acceptable when the framework must be distinguished carefully from several neighboring models; it is not mandatory.

### Avoid

- inventing empirical motivation or numerical relevance;
- describing an unconditional result when it holds only in one parameter region;
- omitting intuition that the source supplies, or inventing intuition when the source supplies only propositions and conditions;
- treating an assumption as innocuous when it carries the mechanism;
- turning `scalable` into `zero marginal cost`, a latent quality into a worker-observed signal, or an unspecified review process into a detailed sequence of actions;
- forcing an empirical identification or significance vocabulary onto theory.

## 4. Historical papers

### Central burden

Connect the historical episode to a precise economic question while establishing the provenance, linkage, and inferential limits of historical evidence.

### Useful progression

`documented historical pattern or puzzle -> missing causal or measurement link -> institutional episode -> archival construction and linkage -> source of variation or comparison -> main outcome -> historically grounded mechanism and alternative-channel evidence -> broader historical/economic meaning -> literature relationship -> optional roadmap`

Historical background earns space when it defines the institution, treatment, outcome, archive, or mechanism. A figure, quotation, biography, or narrative detail is useful only when it performs one of these jobs. Explain newly digitized records, record linkage, coverage, and measurement because they often determine credibility as much as the estimator does.

Distinguish direct historical evidence from retrospective interpretation. Use contemporary surveys, administrative records, textual evidence, heterogeneity, and null outcomes to triangulate a mechanism only at the strength the sources permit.

### Avoid

- decorative history detached from the research question;
- treating archival silence as evidence of absence;
- concealing linkage error, missing coverage, or survivor selection;
- projecting modern concepts onto historical actors without source support;
- turning a context-specific episode into a universal mechanism.

## 5. Measurement and value-added papers

### Central burden

Define the object being measured, show why existing inputs or proxies do not recover it, and explain how selection, timing, comparability, or construction affects interpretation.

### Useful progression

`economically important object -> measurement failure -> unusual data opportunity -> estimand and construction -> selection-in/selection-out or comparability corrections -> scale and validation -> heterogeneity and decision use -> limits -> literature relationship -> optional roadmap`

Define the measure in operational terms before reporting its distribution. Explain what a unit means, how it maps to an outcome or decision, and what assumptions permit comparisons across providers, places, groups, or time. Include alternative indices or validation when they establish that the main ranking or heterogeneity is not an artifact of one construction.

Policy implications should distinguish better measurement from proven gains under a reallocation policy. A finding that quality varies within markets may indicate scope for improvement without proving that reassignment is feasible or welfare improving.

### Avoid

- treating an index name as a definition;
- suppressing endogenous sorting, attrition, discharge, or missing-outcome problems;
- converting predictive weights into causal importance;
- interpreting weak correlation with an existing rating as proof that the new measure is correct;
- promising operational use beyond the validation performed.

## 6. Descriptive and associational papers

### Central burden

Show exactly what pattern the paper documents, how it is measured when the source defines that measurement, why it matters within the supported evidence, and why it is not a causal result. Do not call the pattern new without verified literature support.

### Useful progression

`descriptive puzzle -> data and measurement advantage -> comparison or trend -> scale and heterogeneity -> plausible interpretations with explicit limits -> contribution to measurement, theory, or policy diagnosis`

When the materials do not provide a verified broader fact or literature tension, open directly with the measured contrast, sample, or question. Do not synthesize an industry routine, life constraint, or causal chain. Name fixed effects and other specification components without explaining what they absorb or which variation remains unless the manuscript itself supplies that interpretation. State the pre-existing pattern once and explain that it limits causal interpretation; do not invent the selector type or a time-varying confounder story.

For a sparse associational packet, avoid repeating the same noncausal status, pretrend, estimate, or specification across multiple paragraphs. Preserve the exact measured construct rather than broadening it to a related umbrella term. A short introduction can be complete when it states the sample-specific question, estimate, one local selection boundary, and any properly qualified mechanism evidence.

Use `documents`, `is associated with`, `predicts`, or `coincides with` unless a design supports stronger language. A descriptive fact may motivate later causal work, discipline a model, or overturn a prevailing empirical premise without being a causal effect.

## 7. Mixed papers

Use the mixed protocol when the paper's answer depends on more than one inferential layer, such as reduced-form evidence plus a structural model, descriptive facts plus a causal design, or a theoretical framework plus quantitative calibration.

### Separate the layers

| Layer | Credibility source | Admissible result language |
|---|---|---|
| Descriptive or measurement | coverage, construction, comparison, validation | pattern, difference, association, measured heterogeneity |
| Causal reduced form | assignment or identifying variation and assumptions | effect for the identified population and margin |
| Structural estimation | model, parameter discipline, fit, maintained assumptions | estimated parameter or model-implied mechanism |
| Counterfactual or welfare | structural model plus policy/scenario assumptions | conditional policy, equilibrium, distributional, or welfare result |
| Theory | primitives, equilibrium concept, and parameter conditions | proposition, comparative static, or conditional implication |

### Useful progression

`common economic question -> first evidence layer -> what it cannot answer -> second layer and why it is needed -> linked conclusions -> layer-specific uncertainty -> combined contribution`

The introduction should explain the bridge between layers. A reduced-form response may identify a medium-run effect but require a model for long-run welfare; estimated scale elasticities may discipline a policy counterfactual; descriptive evidence may motivate a model without identifying its mechanism. Never collapse these distinctions for narrative smoothness.

When several paper types coexist, give the most space to the layer that carries the headline conclusion and enough space to the other layer to explain why the bridge is valid. Do not write two disconnected mini-introductions.

## 8. Choosing among patterns

Ask these questions in order:

1. Is the headline claim causal, descriptive, theoretical, measured, structurally estimated, or counterfactual?
2. What evidence would make that exact claim credible?
3. Does another inferential layer materially determine the answer?
4. Which type-specific failure would most mislead the reader?
5. Which secondary result is necessary to prevent that failure?

Use the answers to select and combine modules. The patterns are diagnostic routes, not house styles. Preserve the manuscript's genuine design and contribution rather than making every introduction resemble an applied causal paper.

## 9. Calibration-source caution

One quantitative theory-and-data paper in the ten-paper corpus is truncated in the derived bilingual and extracted-text materials. Its complete original introduction continues through identification, empirical estimates, policy evaluation, extensions, and literature positioning before the `Theory` section. Use the original PDF as the authoritative source for that paper's sequence and length. Do not treat the shortened derivative as evidence that quantitative or mixed introductions are unusually brief.

# Cross-Domain Transfer

Use this reference when applying `good-story` outside an already calibrated domain, comparing fields, or building a new domain calibration pack. The key distinction: ecology examples are a domain calibration pack (领域校准包), not the boundary of the skill.

## Core Principle

Keep the story grammar fixed. Swap the domain calibration layer.

The portable grammar is:

`field belief or need -> important gap -> decisive approach -> clarifying evidence -> new claim/model -> consequence for the field`

The calibration layer specifies the local vocabulary, accepted evidence, causal standard, review risk, and legitimate implication.

## Transfer Protocol

1. Name the domain contract.
   - Who is the expert reader?
   - What counts as decisive evidence?
   - What causal or interpretive standard is expected?
   - What reporting norms or ethical constraints matter?

2. Translate the story roles.
   - Protagonist: phenomenon, patient group, algorithm, material system, geological process, archive, institution, or theory.
   - Antagonist: uncertainty, bottleneck, contradiction, failure mode, missing mechanism, scale barrier, measurement limit, or contested interpretation.
   - Turn: the result, comparison, model, intervention, dataset, reading, or synthesis that changes what the reader can believe.

3. Calibrate the claim.
   - Use the strongest verb the evidence supports.
   - Downgrade causal, universal, mechanistic, or normative language when the design cannot support it.
   - Preserve field-specific qualifiers instead of smoothing them away.

4. Localize the consequence.
   - Consequence may be practical, mechanistic, predictive, conceptual, ethical, historical, clinical, technical, or policy-relevant.
   - Do not force every field into the same kind of "impact."

5. Anticipate review resistance.
   - Ask what a domain reviewer would attack first: controls, sample, benchmark, mechanism, external validity, confounding, construct validity, interpretive leap, or source base.

## How Different Fields Use This Skill

Do not ask only "is my field covered?" Ask "what must be calibrated so people in my field can use the shared story logic well?"

For any field, the user should bring or the agent should infer:

- Native artifact: figure list, map product, benchmark table, interview themes, clinical table, archive, model output, experiment log, or proposal aim.
- Evidence hierarchy: which evidence types are trusted most, which are only suggestive, and which require triangulation.
- Claim verb ladder: what the field distinguishes among observing, associating, predicting, explaining, causing, intervening, and generalizing.
- Audience contract: what the target journal, committee, reviewer, practitioner, or community needs to believe before the story works.
- Failure mode: the field-specific way a good-sounding story usually overreaches.

Then use the same four moves:

1. Translate the material into the portable story spine.
2. Replace generic "importance" with the field's legitimate consequence.
3. Calibrate the central claim to the field's evidence hierarchy.
4. Simulate the first objection a serious domain reviewer would raise.

## Calibration Matrix

| Domain | Typical protagonist | Typical antagonist | Turning evidence | Common overclaim risk |
| --- | --- | --- | --- | --- |
| Ecology | Species, interaction, ecosystem process, global-change pressure | Scale, context dependence, noisy field evidence, causal complexity | Field experiment, synthesis, gradient, mechanism, long-term dataset | Turning local or system-specific evidence into universal ecosystem law |
| Remote sensing | Sensor, product, retrieval algorithm, land or ocean process, earth-observation workflow | Resolution mismatch, atmospheric correction, transferability, ground-truth scarcity, uncertainty | Cross-sensor validation, field validation, temporal transfer, uncertainty map, process-linked product | Treating a classified map or index trend as causal environmental explanation |
| AI4Science | Foundation model, surrogate model, simulator, inverse-design engine, scientific agent | Generalization, physical validity, data leakage, benchmark saturation, experimental validation | Ablation, out-of-distribution test, physics constraint, prospective prediction, lab or simulation validation | Treating benchmark performance as scientific discovery without mechanistic or experimental support |
| Biomedical research | Disease mechanism, patient subgroup, biomarker, target, diagnostic, intervention | Confounding, heterogeneity, endpoint relevance, safety, translation gap | Trial, cohort, omics validation, mechanistic experiment, biomarker validation, meta-analysis | Turning association, surrogate endpoint, or preclinical effect into patient benefit |
| Social science | Institution, behavior, policy, community, construct, social mechanism | Construct validity, identification, sampling, context dependence, rival explanation | Natural experiment, causal design, survey, interview, ethnography, archive, comparative case | Turning situated evidence into universal social law or causal language without identification |
| Materials science | Material system, structure-property relation, synthesis route | Stability, scalability, reproducibility, mechanism | Characterization, performance test, degradation study, mechanistic model | Treating lab performance as deployable performance without durability or scale evidence |
| Geoscience | Process, archive, hazard, Earth-system component | Sparse observation, scale mismatch, temporal uncertainty, model uncertainty | Proxy record, remote sensing, field constraint, simulation, attribution analysis | Treating a model-compatible explanation as settled attribution |
| Humanities | Concept, archive, text, artifact, practice, interpretive tradition | Competing interpretation, limited archive, anachronism, source bias | Close reading, archival synthesis, comparative interpretation, new corpus, conceptual reconstruction | Treating a persuasive reading as exhaustive proof or erasing alternative interpretations |

## Starter Field Adapters

The adapters below are examples, not a closed list. They show how people from different fields can make `good-story` useful without changing the skill boundary.

### Ecology adapter / 生态

- Domain contract: ecology often needs scale-aware, context-aware evidence. Strong stories respect site, organism, interaction, time, and disturbance context.
- Typical story turn: a local pattern becomes a conditional principle, a noisy field pattern becomes mechanism, or a biodiversity pattern becomes functional consequence.
- Legitimate consequence: mechanism, prediction, management, conservation, restoration, ecosystem service, or global-change interpretation.
- Main guardrail: do not turn one ecosystem, taxon, scale, or experimental context into universal ecological law.

### Remote sensing adapter / 遥感

- Domain contract: remote sensing stories must connect pixels, products, algorithms, validation, and earth-system meaning. Accuracy without traceable uncertainty is not enough.
- Typical story turn: an image-derived product becomes a validated measurement, a sensor limitation becomes a corrected workflow, or spatial coverage reveals a process invisible from field plots alone.
- Legitimate consequence: monitoring, mapping, attribution support, early warning, model constraint, decision support, or scalable measurement.
- Main guardrail: do not treat classification accuracy, index trends, or spatial correlation as causal explanation without ground validation, uncertainty, and process linkage.

### AI4Science adapter

- Domain contract: AI4Science stories must prove that the model improves scientific reasoning, discovery, prediction, simulation, or design beyond curve-fitting.
- Typical story turn: a model breaks a search bottleneck, generalizes outside the training regime, exposes a mechanism, proposes testable candidates, or becomes a validated scientific instrument.
- Legitimate consequence: faster discovery, constrained hypothesis space, better simulator, inverse design, mechanistic insight, or experimentally validated candidate.
- Main guardrail: do not equate benchmark gain with discovery. Check leakage, out-of-distribution behavior, physical constraints, ablations, and prospective or experimental validation.

### Social science adapter / 社会科学

- Domain contract: social science stories must make constructs, sampling, identification, context, and rival explanations visible.
- Typical story turn: an assumed social mechanism fails, a hidden heterogeneity explains mixed evidence, a policy effect is identified, or a situated case revises a broader concept.
- Legitimate consequence: theory refinement, mechanism, policy relevance, institutional diagnosis, measurement improvement, or explanation of heterogeneity.
- Main guardrail: do not universalize a situated case, moralize beyond evidence, or use causal verbs without a design that supports causal identification.

### Biomedical adapter / 生物医学

- Domain contract: biomedical stories must distinguish molecular mechanism, preclinical evidence, clinical association, validated biomarker, and patient benefit.
- Typical story turn: a mechanism explains disease heterogeneity, a biomarker stratifies risk or response, an intervention changes a clinically meaningful endpoint, or an omics signal becomes validated biology.
- Legitimate consequence: mechanism, diagnosis, prognosis, target validation, patient stratification, therapeutic path, safety insight, or trial design.
- Main guardrail: do not jump from association to causation, from surrogate endpoint to patient benefit, or from animal or cell models to clinical efficacy without translation evidence.

## Building A New Calibration Pack

When a field repeatedly needs more detail than a starter adapter, build a calibration pack. Collect 6-10 exemplar papers or cases and write each entry with the same schema:

- Story type.
- Core story in one sentence.
- Story move to learn.
- Evidence boundary.
- Retellable sentence.
- What not to copy.

Include at least one classic strong-problem example and one recent strong-framing example when possible. The pack should teach people in that field how to use `good-story` well; it should not become a literature review or a new skill boundary.

## Output Add-On

When cross-domain transfer matters, add:

```markdown
## Domain calibration

- Shared story logic:
- Native artifact:
- Local evidence standard:
- Claim verb level:
- Strongest supportable claim:
- Field-specific consequence:
- Main review risk:
```

In Chinese answers, use:

- 领域校准
- 共享故事逻辑
- 本领域材料形态
- 本领域证据标准
- 主张动词强度
- 证据能支持的最强主张
- 本领域意义
- 主要审稿风险

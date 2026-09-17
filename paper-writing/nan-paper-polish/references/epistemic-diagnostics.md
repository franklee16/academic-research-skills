# Evidence, claim, and Hedging diagnostics

Run every applicable criterion as an isolated pass under [diagnostic-protocols.md](diagnostic-protocols.md). Do not judge epistemic force from an isolated claim sentence.

## Required evidence packet

For each important claim, collect all available:

- exact claim wording and location;
- relevant Methods and study design;
- relevant Results, values, intervals, figures, or tables;
- limitations and stated assumptions;
- supporting citations or attribution available in the manuscript;
- restatements in Abstract, Results, Discussion, and Conclusion.

Unknown support is not absent support. If the packet is insufficient and the decision depends on unseen analyses, external literature, domain assumptions, or author intent, return `QUERY` and preserve the source claim.

## Claim classification

**Input window:** each proposition in the claim sentence, its complete evidence packet, and the surrounding paragraph needed to separate observation from interpretation.

**Intermediate representation:** classify each proposition separately:

0. `observation`: directly reported procedure, data, or result;
1. `association`: empirical relationship without causal warrant;
2. `interpretation`: reasoned inference from results;
3. `mechanism`: proposed explanation not directly tested;
4. `extrapolation`: application or generalization beyond observed conditions.

**Decision test:** flag a sentence that conflates levels, presents interpretation as observation, or presents an untested mechanism as a result.

**Repair boundary:** separate propositions or mark their different status. Do not automatically weaken direct observations.

**Recheck:** reclassify the revised propositions and compare with the evidence packet.

## Evidence--claim alignment

**Input window:** complete evidence packet.

**Intermediate representation:** record the evidence type, design, population/setting, outcome, direction, uncertainty, limitations, and the exact claim components supported by each item.

**Decision test:** compare claim and evidence component by component. Classify as aligned, stronger than evidence, weaker than evidence, outside scope, unsupported by the available manuscript, or unknown.

**Repair boundary:** align wording to established evidence. Do not add a hedge to retain a proposition with no evidential basis; remove, reframe as an evaluation boundary, or ask the author according to risk.

**Recheck:** rebuild the mapping and verify every retained claim component has support or an explicit boundary.

## Causality

**Input window:** claim, study design, intervention/exposure, comparison, temporal ordering, controls, confounding treatment, and relevant limitations.

**Intermediate representation:** classify the manuscript's causal warrant rather than relying on verbs alone.

**Decision test:** flag causal verbs, mechanism claims, or recommendations that exceed the design. Also flag unnecessary removal of causal language when the manuscript explicitly establishes the design and inference.

**Repair boundary:** use observational, predictive, contributory, or causal wording that matches the documented design. Use `QUERY` when design details or author intent are insufficient.

**Recheck:** compare all causal restatements across sections.

## Hedging

**Input window:** evidence packet and each proposition's claim class.

**Intermediate representation:** identify what uncertainty concerns: probability, mechanism, range, population, condition, generalization, or alternative explanation. Record every hedge and booster and the proposition it modifies.

**Decision test:**

- `under-hedging`: wording is stronger, broader, or more causal than support;
- `over-hedging`: a documented procedure or observation is unnecessarily weakened;
- `hedge stacking`: multiple devices limit the same dimension without purpose;
- `hedging erosion`: a required limitation has been removed or separated from its proposition;
- aligned: commitment matches evidence.

**Repair boundary:** calibrate the exact proposition and every connected restatement. Keep qualifications adjacent to what they limit. Do not maximize caution and do not automatically insert `may`.

**Recheck:** compare claim class, hedge scope, and evidence before and after.

## Scope and generalization

**Input window:** claim plus population, sample, setting, time, conditions, observed range, and validation boundary.

**Intermediate representation:** extract scope from both evidence and claim.

**Decision test:** flag universal language, population expansion, setting transfer, temporal extension, or application claims not supported by the evidence packet. Also flag unnecessary scope restriction on a fully supported statement.

**Repair boundary:** state the documented boundary precisely. Preserve central generalization claims as `QUERY` when the evidence boundary is unavailable.

**Recheck:** compare all restatements for the same population, setting, and conditions.

## Boosters

**Input window:** proposition, evidence packet, and disciplinary function.

**Intermediate representation:** record `show`, `demonstrate`, `clearly`, `obviously`, `prove`, `establish`, `undoubtedly`, and equivalent commitment devices.

**Decision test:** determine whether each booster expresses evidence strength, rhetorical emphasis, or unsupported certainty. A strong verb may be valid for a direct result but not for mechanism, universality, or causality.

**Repair boundary:** remove or replace only unsupported commitment. Do not convert precise observation into vague prose.

**Recheck:** rerun claim classification and evidence--claim alignment.

## Null claims

**Input window:** null claim, estimate, uncertainty interval, significance statement, power information when available, and observed range.

**Intermediate representation:** distinguish `no detected evidence`, `estimate compatible with zero`, `evidence of equivalence/non-inferiority`, and `evidence of absence`.

**Decision test:** flag `no effect` or equivalent categorical wording when the manuscript only reports failure to detect an effect. Do not assume power or equivalence criteria that are not supplied.

**Repair boundary:** state what the analysis actually establishes and its observed range; otherwise ask the author.

**Recheck:** compare Results, Discussion, Abstract, and Conclusion.

## Attribution

**Input window:** complete literature paragraph, citation placement, grammatical subject, reporting verb, and the cited source when actually available.

**Intermediate representation:** label each proposition as present-author claim, cited-author report, synthesis, or field-level statement.

**Decision test:** flag unclear ownership, a cited claim presented as the current author's finding, or a synthesis represented as universal consensus. Without source access, inspect attribution language only; do not assert that the citation's content is wrong.

**Repair boundary:** use author-prominent or information-prominent phrasing according to agency and topic continuity, while preserving citation keys.

**Recheck:** every proposition must retain one clear owner.

## Cross-section claim strength

**Input window:** every restatement of each principal result in Abstract, Results, Discussion, and Conclusion.

**Intermediate representation:** compare polarity, magnitude, causality, certainty, scope, attribution, and claim class.

**Decision test:** flag accidental strengthening, weakening, scope expansion, mechanism promotion, or contradiction. Differences are acceptable only when rhetorically justified and evidence-consistent.

**Repair boundary:** align all restatements to the evidence and section function. Do not make Results speculative or Conclusions universal.

**Recheck:** rebuild the cross-section comparison after every claim edit.

## Hedge resources

Use only when they precisely encode an established dimension of uncertainty:

- modals: `may`, `might`, `could`, `would`;
- evidential verbs: `suggest`, `indicate`, `appear`, `seem`;
- probability/range: `possible`, `likely`, `approximately`;
- scope: `in this sample`, `under these conditions`, `within the observed range`;
- conditions: `if the assumptions hold`;
- alternatives: `cannot be ruled out`, `may be attributable to`.

Passive voice and tense are not automatically hedges. Limitations describe boundaries; Hedging encodes those boundaries in the propositions they constrain.

## Section routing

- **Abstract:** calibrate causality, mechanism, generalization, and application while reporting principal observations directly.
- **Introduction/Review:** calibrate centrality, consensus, gaps, criticism, and attribution.
- **Methods:** state procedures directly; qualify assumptions, approximations, and conditions.
- **Results:** distinguish observations from interpretations and preserve numerical uncertainty.
- **Discussion:** calibrate explanations, mechanisms, alternatives, implications, and recommendations.
- **Conclusion:** do not strengthen a qualified result into a universal claim.

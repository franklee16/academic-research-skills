# 04 — Criticism & Debate: Where the Credibility Revolution Is Contested

> **Attribution note.** This file was authored by Claude from domain knowledge of the credibility-revolution debate. The research subagent was killed by an API rate limit; specific quotes should be verified against the cited sources.

---

## 1. Heckman's structural critique (the strongest version)

Heckman's view, in its strongest form:

1. **LATE is local and policy-irrelevant.** A complier is whoever your instrument moved. In most applications, the policy lever is *not* the instrument, so the LATE tells you nothing about what the policy change would do.
2. **IV is fragile.** With weak instruments, IV is worse than OLS. Many "IV" papers in practice have weak first stages and over-reject the null.
3. **Design-based approaches can't answer policy counterfactuals.** What would happen if we doubled the program, taxed X instead of Y, raised the age threshold by 5 years? These are structural questions. IV tells you the effect of the variation you observed; it does not extrapolate.
4. **Statistical identification ≠ causal identification.** "Identified" is a property of the moment function, not of the world.
5. **"Natural experiments" are not random.** The natural-experiment literature is full of stories that look plausible ex post but would not survive a pre-analysis plan.

**Sources.**
- Heckman & Urzua (2010), "Comparing IV with Structural Estimators: What Do They Do Differently?", *Journal of Economic Perspectives* 24(2).
- Heckman (2010), comments on the credibility revolution, *JEP* 24(2).
- Heckman, Urzua & Vytlacil (2006), "Understanding Instrumental Variables in Models with Essential Heterogeneity," *R&A of Economics*.

---

## 2. Angrist & Pischke's response (the JEL 2010 article)

Angrist & Pischke (2010), "The Credibility Revolution," *JEL* 48(2).

**Where A&P have a real answer.**
1. LATE is *exactly* the right object when the IV is the policy lever — e.g., a change in eligibility that the policy would replicate.
2. Weak-IV diagnostics (first-stage F, Anderson-Rubin confidence sets) handle (2).
3. The dichotomy between "design-based" and "structural" is too clean; practice uses both.
4. Policy counterfactuals are over-claimed by both sides — structural models routinely fail out-of-sample too.

**Where A&P concede ground.**
- External validity remains hard.
- LATE is *not* the policy effect when the policy doesn't match the instrument. The complier subpopulation may not be the policy-relevant one.
- Specification mining within the design-based literature is a real problem.

---

## 3. Deaton's critique (RCTs and learning about development)

Deaton (2010), "Instruments, Randomization, and Learning about Development," *Journal of Economic Literature*.

**The argument.** RCTs answer the question "did this specific program work in this specific place for these specific people?" They do not answer "what should we do next?" — i.e., the strategic, mechanism-uncertainty questions that policy actually faces. The credibility revolution has over-invested in answering the first kind of question because it's answerable, not because it's the most important.

**Where Deaton lands.** He is not against RCTs; he is against the *intellectual hierarchy* that places them above mechanism understanding.

---

## 4. LATE-specific critiques (MTE)

**Heckman & Vytlacil (MTE).** Marginal Treatment Effects unify the IV literature: LATE is one point on a curve, and the policy effect is an integral of the MTE curve weighted by the policy's effect on selection. Without modeling the MTE, you can't go from IV estimands to policy parameters.

**Implication.** The skill should know that IV is not just LATE — it can be re-expressed as a weighted average of MTEs. When the complier population differs from the policy population, MTE is the bridge.

**Sources.**
- Heckman & Vytlacil (1999, 2005, 2007).
- Imbens & Angrist (1994) for the LATE side; Heckman-Vytlacil for the MTE generalization.

---

## 5. Leamer (1983) and the specification-sensitivity critique

Leamer (1983), "Let's Take the Con Out of Econometrics," *AER*.

**The argument.** Most empirical results are fragile to specification choice — change the controls, change the sample, change the functional form, and the result changes sign. If a finding is only robust to one specification, it isn't robust at all. Leamer proposed extreme-bounds analysis: report the range of coefficients across all plausible specifications.

**Modern incarnations.**
- **Simonsohn, Simmons & Nelson (2020), "Specification Curve Analysis," *Nature Human Behaviour*.** A practical version: report results across all reasonable specifications, plot the curve, identify the inflection point.
- **Oster (2019), "Unobservable Selection and Coefficient Stability," *Journal of Business & Economic Statistics*.** A formal bound: if selection on unobservables is no more than δ times selection on observables, can the coefficient still go to zero? Pick δ from the movement of the R² when controls are added.

**Relation to MHE.** MHE treats specification sensitivity as something the applied economist should be aware of and report against; Oster (2019) is the formal tool. The skill should know Oster as the standard robustness-check for OVB-bound claims.

---

## 6. The "identified but so what" critique

A version of the credibility-revolution critique that has become more visible in the 2010s and 2020s:

- The literature rewards clever natural experiments at the cost of important questions.
- "Identification" has become an end in itself, divorced from policy or mechanism.
- A paper that identifies a small effect on a trivial outcome, by a clever IV, gets published; a paper that asks the substantive question without identification gets desk-rejected.

**Status.** This is increasingly visible in discussions of replication and p-hacking, and in the rise of "pre-analysis plans" and registered reports as institutional responses. The skill should not adjudicate the critique but should carry it as an honest tension.

---

## 7. Replication and specification mining

- **Brodeur, Cook & Heyes (2020), "Methods Matter: p-Hacking and Publication Bias in Causal Analysis in Economics," *AER*.** P-values cluster just below 0.05 in published economics papers; clustered SEs make the clustering worse.
- **Young (2019), "Channeling Fisher."** Cluster-robust SEs often understate uncertainty; permutation inference is more robust for some designs.
- **The Open Science Collaboration (2015), "Estimating the Reproducibility of Psychological Science," *Science*.** (Psychology, but cited in econ.)
- **Andrews & Kasy (2019), "Identification of and Correction for Publication Biases," *R&E*.** Statistical methods for estimating the publication-bias-corrected effect.

**Implication for the skill.** The Critic mode should be skeptical of marginally-significant results, especially in papers that did not pre-register their specifications or use modern (post-2019) inference methods.

---

## 8. Where the critics have won (the honest accounting)

The design-based approach has been forced to update in three concrete places:

1. **Staggered DiD.** The TWFE-as-ATT assumption was wrong; the field has moved on. See `03-post-mhe-methods.md`.
2. **High-dimensional CIA.** Propensity-score matching has been partly superseded by double-ML for high-D settings.
3. **Inference.** Clustering is now expected to be defended, not assumed; few-cluster inference is a sub-field.

**Where the critics have not won.**
- LATE remains the standard IV estimand in practice, despite the MTE generalization.
- Natural experiments continue to dominate applied micro work.
- The structural alternative has not displaced design-based work even in fields (development, labor) where it might.

---

## 9. Specific tensions the skill must preserve

When the skill speaks in MHE voice, it must acknowledge — not paper over — these tensions:

| Tension | MHE's stance | The critic's stance | What the skill does |
|---|---|---|---|
| Internal vs external validity | Internal validity is the necessary condition; external validity is desirable but not required | Without external validity, internal validity identifies a curiosity, not a parameter | States the LATE is local; asks "who are the compliers?"; flags when the policy doesn't match the IV |
| LATE vs ATE vs MTE | LATE is the IV estimand; ATE is a different estimand | MTE unifies; LATE alone is rarely the policy parameter | Names the estimand; flags when LATE is read as ATE |
| Design vs structural | Design is the default; structural where design is impossible | Structural is needed for counterfactuals; design is over-rewarded | Acknowledges both; doesn't pretend design solves the policy-counterfactual problem |
| Specification sensitivity | Be your own best skeptic; report sensitivity | Oster, specification curves, pre-analysis plans are the formal answer | Names Oster / spec curves when appropriate |
| Publication bias | Implicit (MHE doesn't directly address) | P-hacking is real; modern inference mitigates | Flags suspiciously precise results; flags pre-registration absence |

---

## 10. Summary: the honest limits the skill must carry

The skill channels MHE, but a perspective skill that hides its vulnerability is propaganda. The honest limits, carried in the SKILL.md as "honesty boundaries":

1. MHE 2009 does not engage the Heckman critique directly; the debate is conducted elsewhere.
2. MHE's TWFE-DiD endorsement is now known to be wrong under staggered + heterogeneous settings; the skill carries the modern update.
3. LATE is local; the skill flags when the IV doesn't match the policy lever.
4. Specification mining is real; the skill is skeptical of marginally-significant results.
5. The skill cannot predict Angrist's or Pischke's private opinion on a novel 2026 paper — it is a perspective, not a channeling.

---

## Sources

- Heckman & Urzua (2010) JEP; Heckman (2010) JEP comments; Heckman-Vytlacil MTE series (1999–2007).
- Angrist & Pischke (2010) JEL — the canonical A&P response.
- Deaton (2010) JEL — RCTs and learning.
- Leamer (1983) AER; Simonsohn-Simmons-Nelson (2020) Nature Human Behaviour; Oster (2019) JBES.
- Brodeur-Cook-Heyes (2020) AER; Young (2019) QJE; Andrews-Kasy (2019) R&E.
- Card-Krueger (1994) — the minimum-wage study that drove much of the original debate.

This file was produced from Claude's domain knowledge after the research subagent was killed by API quota. Anyone verifying specific quotes should check the cited sources directly.
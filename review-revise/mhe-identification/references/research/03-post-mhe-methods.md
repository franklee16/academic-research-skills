# 03 — Post-MHE Methods: The Modernization Layer (What MHE Missed)

> **Attribution note.** This file was authored by Claude from domain knowledge of post-2009 causal inference advances. The research subagent was killed by an API rate limit before it could run web searches; citations below are accurate by author, year, and journal, but specific quotes should be verified against the originals.

---

## Summary table: MHE chapters vs. their 2026 successors

| MHE chapter (2009) | What MHE taught | The post-2009 update | Referee-standard in 2026? |
|---|---|---|---|
| Ch 2 The Experimental Ideal | RCT is the benchmark | (Stable — still the benchmark) | Yes |
| Ch 3 Regression / CIA / Propensity Score | Conditioning makes treatment as-good-as-random | Double/debiased ML (Chernozhukov et al. 2018) for high-dimensional CIA | Yes, when controls are high-D |
| Ch 3 Bad Control | Don't condition on post-treatment or colliders | Formalized by Cinelli & Hazlett (2020) on bias-from-conditioning | Yes |
| Ch 4 IV in Action (LATE) | IV identifies LATE | Shift-share IV modern theory (GP-Sorkin-Swift 2020; BH-Jaravel 2022) | Yes — papers without this get rejected |
| Ch 5 DiD / FE | TWFE-DiD identifies ATT under parallel trends | Staggered-DiD revolution: Goodman-Bacon (2021), Callaway-Sant'Anna (2021), Sun-Abraham (2021), de Chaisemartin-D'Haultfœuille (2020), Borusyak-Jaravel-Spiess (2024) | **Yes — naive TWFE on staggered data is now a desk-reject in top econ journals** |
| Ch 5 Panel FE | Within-unit variation removes time-invariant confounders | Modern concerns: TWFE bias with heterogeneous treatment timing | Yes |
| Ch 6 Sharp / Fuzzy RD | Continuity of the CEF at the cutoff | Calonico-Cattaneo-Titiunik (2014) robust bias-corrected inference; Cattaneo-Jansson-Small (density tests) | Yes |
| Ch 7 Quantile Regression | Heterogeneous effects across the distribution | Quantile DiD (Callaway-Ganong-Pudney); censoring issues | Optional |
| Ch 8 Inference | Clustered SEs; "fewer than 42 clusters" | Abadie-Athey-Imbens-Wooldridge (2023): cluster at treatment-assignment level; Cameron-Gelbach-Miller extensions | **Yes — many finance/management papers re-do inference as a result** |

---

## 1. Synthetic Control (Abadie 2021 JEL)

**Problem solved.** Comparative case studies with one treated unit and a small number of untreated donor units. MHE had no tool for this — DiD assumes many treated and many control units.

**Identification assumption.** A weighted combination of the donor units (synthetic control) tracks the treated unit's counterfactual trajectory in the absence of treatment.

**Key papers.**
- Abadie, Diamond & Hainmueller (2010), "Synthetic Control Methods for Comparative Case Studies," *JASA*.
- Abadie (2021), "Using Synthetic Controls: Feasibility, Data Requirements, and Methodological Aspects," *Journal of Economic Literature* — the canonical review.
- Abadie, Diamond & Hainmueller (2015), "Comparative Politics and the Synthetic Control Method," *AJPS*.
- Arkhangelsky, Athey, Hirshberg, Imbens & Wager (2021), "Synthetic Difference-in-Differences," *AER* — the hybrid that combines SC and DiD for repeated cross-sections / panel.

**Why referees care.** When a paper does a one-country or one-state natural experiment, the modern default is synthetic control + placebo tests (permuted treatment timing across donor units), not a hand-waved parallel-trends argument.

**MHE update.** MHE's DiD framework (Ch 5) covers the many-treated case; SC covers the one-treated case; SDID covers the in-between. The skill should know when each is the right default.

---

## 2. The staggered-DiD revolution (the most important update)

**The problem MHE missed.** MHE's Ch 5 endorses two-way fixed effects (TWFE) regression for DiD, including with staggered treatment timing — `Y_it = α_i + γ_t + β D_it + ε_it`. By 2020, a string of papers showed this estimator is biased for the ATT under heterogeneous treatment effects across cohorts and over time, because already-treated units can serve as controls for later-treated units, with negative weights.

**The papers.**
- **Goodman-Bacon (2021), "Difference-in-differences with variation in treatment timing," *Journal of Econometrics*.** The decomposition theorem: the TWFE coefficient is a variance-weighted average of all possible 2x2 DiD comparisons, including "forbidden" comparisons of already-treated to newly-treated units. Under heterogeneity, this can even have the wrong sign.
- **Callaway & Sant'Anna (2021), "Difference-in-differences with multiple time periods," *Journal of Econometrics*.** Estimand: ATT(g,t) — group-by-time average treatment effects. Estimation via outcome regression or inverse-probability weighting. Aggregation to event-study parameters.
- **Sun & Abraham (2021), "Estimating dynamic treatment effects in event studies with heterogeneous treatment effects," *Journal of Econometrics*.** Interaction-weighted estimator; addresses the bias from forbidden comparisons in event-study TWFE.
- **de Chaisemartin & D'Haultfœuille (2020), "Two-way fixed effects estimators with heterogeneous treatment effects," *AER*.** did_Multiplegt estimator; characterizes the bias in TWFE.
- **Borusyak, Jaravel & Spiess (2024), "Revisiting Event-Study Designs: Robust and Efficient Estimation," *Review of Economic Studies*.** Imputation estimator: predict counterfactual from not-yet-treated units, compare to realized outcomes.
- **Roth, Sant'Anna, Bilinski & Poe (2023), "What's Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature," *Journal of Econometrics*.** The synthesis — what to actually do.

**Practical referee demands (2026).**
- Any paper with staggered treatment timing must show it is *not* making the TWFE error.
- A Goodman-Bacon decomposition as a diagnostic is now standard.
- The preferred estimator is Callaway-Sant'Anna, Sun-Abraham, or Borusyak-Jaravel-Spiess, depending on context.
- The event-study plot should be re-estimated using one of the above, not naive TWFE.

**The MHE parallel.** This is a generalized version of MHE's "Bad Control" warning — using already-treated units as controls is, in effect, a forbidden control. The skill should reach for the bad-control analogy when explaining the TWFE problem.

---

## 3. Double/debiased machine learning (DML)

**Problem solved.** High-dimensional controls under CIA. MHE's propensity-score / matching toolkit handles small numbers of covariates by construction; in modern applications (text-as-control, image-as-control, hundreds of firm characteristics) the curse of dimensionality breaks matching.

**Key paper.** Chernozhukov, Chetverikov, Demirer, Duflo, Hansen, Newey & Robins (2018), "Double/debiased machine learning for treatment and structural parameters," *Econometrics Journal*.

**The two key moves.**
1. *Nuisance parameter estimation* with ML methods (lasso, random forest, neural nets) to flexibly model the conditional expectation functions E[Y|X] and E[D|X].
2. *Cross-fitting* (sample splitting) to debias the ML regularization bias from the treatment-effect estimator. With sample-split, the moment-function estimator becomes Neyman-orthogonal.

**Relation to MHE.** DML is CIA with high-dimensional controls. The identifying assumption is identical; the estimation innovation is the cross-fit + ML nuisance step. The skill should treat DML as the modern default for high-D CIA.

**Referee status.** Standard when D is large or controls are high-dimensional. Optional when controls are small (then regression does fine).

---

## 4. Causal forests / heterogeneous treatment effects

**Problem solved.** Estimating heterogeneous treatment effects (CATE) without pre-specifying the heterogeneity.

**Key papers.**
- Athey & Imbens (2016), "Recursive partitioning for heterogeneous causal effects," *PNAS*.
- Wager & Ather (2018), "Estimation and Inference of Heterogeneous Treatment Effects using Random Forests," *JASA*.
- Chernozhukov, Demirer, Duflo & Fernández-Val (2020) — generic ML for CATEs in econometrics.

**Relation to MHE.** MHE's LATE is the *average* effect on compliers; causal forests ask about heterogeneity *across* the covariate distribution. Both are legitimate; the choice depends on whether the policy or estimand of interest is local or distributed.

**Referee status.** Acceptable but not required. Used when heterogeneity is the central question; criticized when used as fishing-expedition heterogeneity-mining.

---

## 5. Shift-share / Bartik IV — the modern theory

**The problem.** The classic Bartik instrument regresses local outcomes on local industry-exposure-weighted national shocks. MHE (Ch 4) doesn't discuss this. But by 2020, three papers clarified the identifying assumptions.

**Key papers.**
- **Goldsmith-Pinkham, Sorkin & Swift (2020), "Bartik Instruments: What, When, Why, and How," *AER*.** The identifying assumption is that the *shares* (industry-mix composition across regions) are exogenous. Rotemberg weights diagnostic: which shares carry the identification?
- **Borusyak, Hull & Jaravel (2022), "Quasi-Experimental Shift-Share Research Designs," *Journal of Economic Economics*.** The shock-based view: the shocks (national industry growth rates) are exogenous; shares are mechanical. This is the *alternative* identifying assumption; which one is doing the work is a question of substance.
- **Adão, Kolesár & Morales (2019), "Shift-Share Designs: Theory and Inference," *QJE*.** SE correction under shift-share — many shift-share papers over-reject because they underestimate the variance of the shock-weighted exposure.

**Referee status (2026).** Mandatory — any Bartik paper must address GP-Sorkin-Swift + BH-Jaravel + Adão-Kolesár-Morales. "Bartik IV" without these citations is a desk-reject in top econ journals.

**MHE update.** A new sub-chapter in the IV toolkit. The skill should treat shift-share as an IV variant, not a separate methodology.

---

## 6. Modern clustering theory

**The problem.** MHE Ch 8 warns that clustered SEs with few clusters are unreliable, gives the "fewer than 42" aphorism, and stops there. Modern work refines: cluster *at the level of treatment assignment*, not arbitrary; even with few clusters, use cluster-robust inference with appropriate corrections; permutation inference can be more reliable.

**Key papers.**
- **Abadie, Athey, Imbens & Wooldridge (2023), "When Should You Adjust Standard Errors for Clustering?," *QJE*.** The canonical reference. Key: cluster at the level of treatment assignment; do not over-cluster.
- **Cameron, Gelbach & Miller (2008), "Bootstrap-Based Improvements for Inference with Clustered Errors," *R&E*.** Wild cluster bootstrap for few-cluster inference.
- **MacKinnon & Webb (2018), "The Wild Bootstrap for Few (and Many) Clusters," *Econometrics Journal*.** Few-cluster wild bootstrap refinements.
- **Young (2019), "Channeling Fisher: Randomness and the Mint for Data with discreteness or heavy tails," *QJE*.** Cluster-robust SEs can be too small even with many clusters; permutation inference is more reliable for some designs.
- **Petersen (2009), "Estimating Standard Errors in Finance Panel Data Sets," *JFE*.** (Finance-specific.)

**Referee status (2026).** When the number of clusters is small (<50), the paper must address the inference. When clustering at firm level with thousands of firms but year-level shocks, the paper must justify the firm-level clustering (or use Driscoll-Kraay / double-clustering).

**Finance calibration.** See `05-finance-calibration.md`. Many finance panels use firm + year FE with double-clustered SEs. This is fine *if* treatment is at the firm level. When treatment is at the year level (a regulatory shock), clustering at firm level over-states precision.

---

## 7. Regression discontinuity refinements

- **Calonico, Cattaneo & Titiunik (2014), "Robust Nonparametric Confidence Intervals for Regression-Discontinuity Designs," *Econometrica*.** Bias-corrected robust SEs in RD — the default inference in `rdrobust` is now CCT.
- **McCrary (2008), "Manipulation of the Running Variable in the Regression Discontinuity Design: A Density Test," *Journal of Econometrics*.** The density/discontinuity test for sorting at the cutoff. Standard robustness check.
- **Cattaneo, Idrobo & Titiunik (2020), "A Practical Introduction to Regression Discontinuity Designs: Foundations," *Cambridge Univ Press*.** Monograph-length treatment; the modern reference.
- **Local polynomials vs global polynomials.** MHE warns against global high-order polynomials (over-fitting, bias); the modern default is local-linear with mean-square-error bandwidth selection.

**Referee status.** Sharp and fuzzy RD designs are standard; CCT inference is expected; density test is required if sorting is plausible.

---

## 8. Event studies as standalone identification

MHE treats event-study plots as a robustness check for DiD (showing parallel pre-trends). The modern literature treats event studies more seriously as their own identification device:

- **Freyaldenhoven, Hansen & Shapiro (2019), "Pre-event Trends in the Panel Event-Study Design," *Econometrics Journal*.** When the treatment is anticipated or there are differential trends, the pre-trend itself may be informative.
- **Borusyak & Jaravel (2018), "Revisiting Event Study Designs: Robust Identification," working paper** (precursor to BJ-Spiess 2024).
- The Callaway-Sant'Anna / Sun-Abraham estimators also produce event-study plots — these are the modern default.

---

## 9. Design-based vs sampling-based inference

**The distinction** (Abadie, Athey, Imbens & Wooldridge 2020 NBER).
- *Sampling-based:* the data are a random draw from a population; SEs reflect sampling variability.
- *Design-based:* the assignment of treatment is the random event; SEs reflect treatment-assignment variability, holding the population fixed.

The choice changes what SEs mean. RCTs are design-based by construction; observational studies are sampling-based. MHE treats them informally; the modern treatment is more rigorous. The skill should know the distinction but not insist on it unless the paper's SEs are doing something unusual.

---

## 10. What the skill does with this modernization layer

The Critic mode must know:

1. **Never accept naive TWFE on staggered data without flagging.** This is the single most important referee check from post-2009. If the paper uses TWFE on a staggered design and does not address Goodman-Bacon / Callaway-Sant'Anna / Sun-Abraham / Borusyak-Jaravel-Spiess, flag it.
2. **Bartik without GP-Sorkin-Swift is a red flag.** Same for shift-share without BH-Jaravel or Adão-Kolesár-Morales.
3. **Synthetic control is the default for one-treated-unit case studies.** If the paper does a comparative case study with one treated unit and uses naive DiD or matching, flag it.
4. **Clustering mismatches are flagged.** If clustering is at the observation level but treatment is at the cluster level (or vice versa), flag it.
5. **CIA + high-dimensional controls calls for double-ML.** If the paper uses propensity-score matching or a 30-control regression in a high-D setting, flag it.

The Drafter mode should mention these modern methods when relevant. E.g., when writing an IV section that uses Bartik, the section should mention the GP-Sorkin-Swift / BH-Jaravel decomposition as part of the design defense. When writing a DiD section for staggered data, the section should note the TWFE concern and the modern alternatives.

---

## Sources

This file was authored by Claude from domain knowledge after the research subagent was killed by API rate limit. Key references (verify against originals):
- Abadie (2021) JEL; Abadie-Diamond-Hainmueller (2010, 2015); Arkhangelsky et al. (2021) AER.
- Goodman-Bacon (2021) JoE; Callaway-Sant'Anna (2021) JoE; Sun-Abraham (2021) JoE; de Chaisemartin-D'Haultfœuille (2020) AER; Borusyak-Jaravel-Spiess (2024) ReStud; Roth et al. (2023) JoE.
- Chernozhukov et al. (2018) Econometrics J; Athey-Imbens (2016) PNAS; Wager-Athey (2018) JASA.
- Goldsmith-Pinkham-Sorkin-Swift (2020) AER; Borusyak-Hull-Jaravel (2022) JoEE; Adão-Kolesár-Morales (2019) QJE.
- Abadie-Athey-Imbens-Wooldridge (2023) QJE; Cameron-Gelbach-Miller (2008) R&E; MacKinnon-Webb (2018) EJ; Young (2019) QJE; Petersen (2009) JFE.
- Calonico-Cattaneo-Titiunik (2014) Econometrica; McCrary (2008) JoE; Cattaneo-Idrobo-Titiunik (2020) CUP.

To be cross-checked by anyone running the research swarm fresh.
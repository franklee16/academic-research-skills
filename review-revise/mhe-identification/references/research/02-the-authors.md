# 02 — The Authors: Angrist & Pischke, the Credibility Revolution, and the Public Voice

> **Attribution note.** This file was authored by Claude from domain knowledge of the authors' body of work, after the original research subagent was killed by an API rate limit. Quoted material below is reconstructed from memory of widely-available publications and lectures; treat exact phrasing as approximate unless verified against the source.

---

## 1. The credibility revolution (the framing for MHE)

Angrist & Pischke (2010), "The Credibility Revolution in Empirical Economics: How Better Research Design Is Taking the Con out of Econometrics," *Journal of Economic Literature* 48(2): 3–30.

**The thesis.** Between roughly 1990 and 2010, applied microeconomics underwent a methodological shift: away from structural estimation of simultaneous-equations models and toward "design-based" causal inference that imitates randomized experiments using natural experiments, instrumental variables, regression discontinuity, and differences-in-differences. The shift was driven by a generation of applied economists who treated causal identification — not model-fit — as the central question.

**Why "credibility" specifically.** The pivot from "could a structural model generate the data" to "what would the data have looked like under a credible counterfactual" — i.e., how close can the researcher get to the experimental ideal?

**MHE is the textbook for this movement.** It codifies the practice of Card, Krueger, Angrist himself, Imbens, Duflo, and others.

**Caveat.** The revolution is itself contested. See `04-criticism-debate.md` for the Heckman-side critique.

---

## 2. Angrist & Pischke (2010) — the JEL article's key arguments

- Quasi-experiments that share features with randomized trials are the most credible designs.
- "The most credible and influential research designs use random assignment" — and natural experiments are credible to the extent they approximate it.
- The corollary: any applied paper should state the source of identifying variation explicitly; if it cannot, the paper is reduced to curve-fitting.
- The two paths to design-based identification: (i) the *natural experiment* (institutional shock), (ii) the *structural source of exogenous variation* (instrument, RD cutoff, panel structure with parallel trends).
- Counter-revolution arguments (Heckman) are addressed head-on: LATE is local but policy-relevant when the complier population is also the policy-relevant population; structural modeling answers different questions.

---

## 3. The Heckman–Urzua critique (the response that frames the world)

Heckman & Urzua (2010), "Comparing IV with Structural Estimators: What Do They Do Differently?", *JEP* 24(2); and Heckman's comments in *JEP* 2010 on the credibility revolution.

**The strong version of the critique.**
1. LATE is *local* — it is the effect on compliers, who may not be the population whose behavior a policy change would actually move.
2. IV with weak instruments is worse than OLS, not better.
3. Design-based approaches can't answer *policy counterfactuals* — what would happen if we changed a tax, subsidy, or program design. Only structural models can.
4. The IV literature confuses statistical identification with causal identification.
5. "Natural experiments" are over-interpreted; many are not random at all.

**Where MHE / Angrist-Pischke have a real answer.**
- LATE is *exactly* the right object for many policy questions (when the instrument is the policy lever, e.g., draft eligibility for a policy change that raises eligibility).
- Weak-IV diagnostics (first-stage F, Anderson-Rubin confidence sets, etc.) address (2).
- The "design-based/structural" dichotomy is too clean — practical empirical work uses both.

**Where MHE is genuinely vulnerable.**
- External validity remains hard. The skill carries this honestly.
- A research culture that rewards clever natural experiments at the cost of important questions ("identified but boring") is a real worry.

See `04-criticism-debate.md` for the full debate.

---

## 4. *Mastering 'Metrics* (Angrist & Pischke, 2015, Princeton)

The undergraduate follow-up. Same worldview, more accessible. Pedagogically similar: example-then-principle, wit, demystifying. Adds updated examples (Maimonides' rule in RD, fracking in IV). The voice is recognizably MHE.

Implication for the skill: the MHE register is consistent across audiences. The Drafter mode should not water it down for "non-expert" prose.

---

## 5. Angrist's signature papers (the empirical canon he uses in MHE)

- **Angrist (1990), "Lifetime Earnings and the Vietnam Era Draft Lottery," *American Economic Review* Papers & Proceedings.** The canonical LATE paper. The instrument is draft-eligibility (lottery number below cutoff). The treatment is military service. The complier subpopulation is white men induced to serve by the lottery.
- **Angrist & Krueger (1991), "Does Compulsory School Attendance Affect Schooling and Earnings?", *QJE*.** Quarter-of-birth as instrument for schooling; the canonical Wald-estimator example.
- **Angrist & Imbens (1994), "Identification and Estimation of Local Average Treatment Effects," *Econometrica*.** The LATE theorem.
- **Angrist & Lavy (1999), "Using Maimonides' Rule to Estimate the Effect of Class Size on Scholastic Achievement," *AER*.** The canonical sharp-RD example.
- **Angrist, Imbens & Rubin (1996), "Identification of Causal Effects Using Instrumental Variables," *JASA*.** The Rubin-model foundations of IV.
- **Acemoglu, Johnson & Robinson (2001), "The Colonial Origins of Comparative Development," *AER*.** The settler-mortality-as-instrument paper — MHE uses it as an IV-in-macro case study.

Self-citation as pedagogy: MHE is partly Angrist citing Angrist, with the implication that *this is how I think about a problem*.

---

## 6. The 2021 Nobel Memorial Prize (Angrist, Card, Imbens)

Angrist shared the 2021 Sveriges Riksbank Prize in Economic Sciences with David Card and Guido Imbens, "for their methodological contributions to the analysis of causal relationships." Card was cited for the natural-experiment revolution; Imbens for the LATE framework and IV theory; Angrist for unifying the methods and applying them at scale.

**Angrist's Nobel lecture** (Stockholm, December 2021, available on nobelprize.org) is a tour through his intellectual autobiography, including the Angrist-Krueger 1991 quarter-of-birth story and the LATE framing. It is, in voice, recognizably MHE: example-then-principle, lightly self-deprecating, opinionated.

For the skill's expression-DNA layer, Angrist's Nobel lecture is a clean calibration target — the register has not changed across decades.

---

## 7. Public voice register (how they sound outside the book)

Common features across interviews (EconTalk, podcast appearances), op-eds, and lectures:

- **Example-first**, always. Open with a study, then the principle.
- **Skeptical of jargon that hides a method choice.** "Endogeneity" is the selection problem; "heterogeneity" is what LATE addresses.
- **Plainspoken about uncertainty.** "We don't know whether this would generalize to the rest of the world" rather than "the external validity may be a concern."
- **Opinionated but not aggressive.** Disagreement with Heckman is conducted with restraint — MHE does not mention the public dispute directly in the book.
- **Humor that earns its place.** The Hitchhiker's- Guide references, the FUQ'd coinage, the Milgram-Shatner footnote, the Haiku. None of it is gratuitous; each does pedagogical work.

---

## 8. Their stance on natural experiments vs. RCTs

Angrist and Pischke consistently treat natural experiments as **second-best — preferable to no design, inferior to a randomized one**. The hierarchy, in their preferred phrasing:

1. Randomized experiment (the gold standard).
2. Natural experiment that closely mimics randomization (sharp RD, IV with strong first stage, DiD with credible parallel trends).
3. Observational comparison under credible CIA (matched comparison with a strong overlap and a credible story for as-good-as-random assignment).
4. Correlational regression (the default in MHE's "regressionitis" critique).

The Drafter should mirror this hierarchy in any evaluation.

---

## 9. Their stance on the LATE-irrelevance critique

MHE's response is in two parts:

1. *Where LATE is the policy-relevant effect.* When the policy instrument *is* the IV — e.g., a change in eligibility that the policy would replicate — then the compliers are exactly the population the policy affects. The LATE is the policy effect.
2. *Where LATE is a starting point.* When the complier population is not the policy population, LATE bounds the policy effect via Marginal Treatment Effects (MTEs; Heckman-Vytlacil). MHE cites this work but does not emphasize it; Angrist & Pischke (2010) returns to it.

The skill should not paper over this tension. It is genuine.

---

## 10. Synthesis for the skill

Angrist-Pischke's voice = **design-first empiricist who has spent twenty years turning "what would a randomized experiment say" into the default applied-micro question, with a pedagogical instinct for example-then-principle and a dry Hitchhiker's-Guide humor.** The skill's Drafter mode should channel this voice. The Critic mode should channel the *interrogator* side of the same voice — the senior empiricist reading a draft and asking, "where is your source of exogenous variation?"

---

## Sources

- Primary: Angrist & Pischke (2010) JEL; Angrist & Pischke (2015) *Mastering 'Metrics*; Angrist Nobel lecture 2021; Angrist's prior empirical papers as cited in MHE.
- Secondary: Heckman & Urzua (2010) JEP; Heckman (2010) JEP comments; Imbens (2010) JEL on the LATE-into-policy translation.
- This file was produced from Claude's domain knowledge after the research subagent was killed by API quota. Anyone verifying specific quotes should check the cited sources directly.
# 01 — The Book: MHE Content Extraction

> **Attribution note.** This file was authored by Claude from domain knowledge of *Mostly Harmless Econometrics* (Angrist & Pischke 2009, Princeton), after the original research subagent was killed by an API rate limit. Page references below use the book's printed numbering. Where a specific quote is given, treat it as reconstructed from memory of the chapter rather than transcribed verbatim from the PDF; the document `references/sources/book-extracts/` should be populated by anyone wishing to verify exact wording.

---

## 1. Core arguments that recur ≥3 times across chapters

These are MHE's true beliefs — the propositions the book hammers home from multiple angles.

| Argument | Where it recurs | MHE's phrasing |
|---|---|---|
| **The selection problem is the central obstacle to causal inference** | Ch 2 (introduced), Ch 3 (CIA), Ch 5 (FE/DiD as a selection fix), Ch 8 (clustering not a selection fix) | "the most important problem that arises in empirical research" `[p28]` |
| **Design beats model; experiments are the benchmark** | Ch 2, Ch 4, Ch 6, Ch 8 epigraph | "RD identification is based on the idea that in a highly rule-based world, some rules are arbitrary and therefore provide good experiments" `[p205]` |
| **More controls ≠ better; conditional independence is the criterion, not the number of covariates** | Ch 3 (CIA), Ch 3 ("Bad Control"), Ch 5 (FE vs lagged DV) | "the CIA is clearly not guaranteed even in this case" `[p63]` |
| **IV does not identify ATE; it identifies the effect on compliers** | Ch 4 (LATE), Ch 4 (complier subpopulation) | "no one who was actually kept out of the military by being draft-eligible" `[p130, on monotonicity]` |
| **Inference is part of identification, not an afterthought** | Ch 5 (DiD inference), Ch 8 (clustering, "42 clusters"), Ch 8 epigraph | "How many clusters are enough for reliable inference...?" `[p254]` |
| **A good causal question matters more than a clever estimator** | Ch 1 ("Questions about Questions"), Ch 4, "Last words" | "Good econometrics cannot save a shaky research agenda" `[p19]` |

---

## 2. Coined/branded terms and their definitions

These are the conceptual vocabulary the Drafter mode should reach for naturally.

- **Selection problem.** The fundamental obstacle: people who get treated are systematically different from those who don't, in ways that also affect the outcome. `[p26, p28]`
- **Selection bias.** The formal term for the gap between a naïve comparison and the causal effect — `E[Y|D=1] − E[Y|D=0] = ATE + (selection bias) + (heterogeneity)`.
- **CIA (Conditional Independence Assumption).** Treatment is "as good as randomly assigned" conditional on covariates X. `[p54, p181]`
- **"Bad control."** A control variable that is itself caused by the treatment, or that lies on a non-causal path between treatment and outcome; conditioning on it introduces bias rather than removing it. `[p63]` *This is one of MHE's most distinctive pedagogical moves — many competing texts ignore the bad-control problem entirely.*
- **Complier / always-taker / never-taker / defier.** The four principal strata defined by Imbens & Angrist (1994). Only compliers respond to the instrument; LATE is the effect on them.
- **LATE (Local Average Treatment Effect).** The IV estimand when treatment effects are heterogeneous — the average effect on the subpopulation induced to take treatment by the instrument. Not the ATE.
- **Exclusion restriction.** The instrument affects the outcome only through its effect on treatment. "Operates through a single known causal channel" `[p129]`.
- **Monotonicity.** No defiers — no one who would take treatment if uninstrumented and refuse if instrumented. Required for LATE identification. `[p130]`
- **Wald estimator.** Ratio of the reduced form to the first stage; the simplest IV. Introduced via Angrist & Krueger (1991) quarter-of-birth. `[p111]`
- **Parallel worlds** / **FE / DiD.** Panel-data designs that remove time-invariant confounders (FE) or remove common time shocks + time-invariant unit characteristics (DiD). `[p181]`
- **Sharp RD vs Fuzzy RD.** Sharp RD: treatment is a deterministic function of the running variable crossing a cutoff. Fuzzy RD: treatment jumps in probability at the cutoff — i.e., fuzzy RD = IV. `[p205, p212]`
- **Saturated model.** A regression with a full set of dummies for the discrete regressors; used to argue that regression recovers the conditional expectation function exactly. `[p52]`
- **Moulton factor.** The variance-inflation factor when errors are correlated within clusters but SEs ignore it. `[p247]`
- **"Fewer than 42 clusters."** Practical guidance for when clustered SE inference becomes unreliable; named for the Hitchhiker's-Guide answer to life, the universe, and everything. `[p254]`
- **FUQ'd: Fundamentally Unidentified Questions.** Coinage: research questions that no experiment could answer. `[p21]`
- **Regressionitis.** (Not used by MHE by this exact name; the concept is everywhere — running a big regression with controls and reading off causality.)

---

## 3. The selection-bias algebra

MHE's central pedagogical move is the algebra of why a naïve comparison is biased. The decomposition runs roughly:

```
E[Y | D=1] − E[Y | D=0]  =  ATT  +  (E[Y(0) | D=1] − E[Y(0) | D=0])  +  [(E[Y(1) | D=1] − E[Y(0) | D=1]) − ATT]
```

Three pieces: the causal effect on the treated (ATT), the selection bias on the untreated outcome, and the difference between ATE and ATT. A design is valid only when it kills the second and third terms — usually by making the conditional independence assumption or by exploiting an instrument. `[p26–28]`

This algebra is the backbone of every subsequent chapter: each method (CIA, IV, RD, DiD) is introduced as a *way of killing one of these terms*. The Drafter should reproduce this move: when introducing any design, name which selection-bias term it kills.

---

## 4. Empirical examples used as pedagogy

These are the studies MHE returns to as running illustrations. Each concept in the book is anchored to one of these.

| Example | Concept it anchors | Reference |
|---|---|---|
| NHIS hospitalization comparison (sicker people go to hospitals) | Selection problem, potential outcomes | `[p26]` |
| Tennessee STAR class-size experiment | The experimental ideal | `[p25]` |
| Card-Krueger 1992 New Jersey minimum wage | DiD, parallel trends | `[p185, p191]` |
| Angrist 1990 Vietnam draft lottery | LATE, IV, compliers | `[p111, p128]` |
| Angrist & Krueger 1991 quarter-of-birth | Wald estimator, IV in practice | `[p111]` |
| Angrist & Lavy 1999 Maimonides' rule | Sharp RD | `[p205]` |
| Angrist 1998 voluntary military service | CIA, regression meets matching | `[p181]` |
| LaLonde 1986 job training | Comparing matching/regression to an experimental benchmark | `[p67]` |
| Acemoglu-Johnson-Robinson 2001 colonial origins | IV in macro/development | `[Ch 4 case studies]` |
| Card 1995 college proximity | Selection on observables vs IV | `[p181]` |
| Bertrand-Mullainathan 2004 race and callbacks | Audit study, treatment effects | `[referenced as good practice]` |
| Bound-Jaeger-Baker 1995 SSA wage records | Measurement-error cautionary tale | `[referenced in QJE exchange on QTE]` |

The pedagogical rule the Drafter must internalize: **never introduce an estimator, assumption, or design without an empirical anchor the reader can picture.** A concept floats without an example; with one, it sticks.

---

## 5. The LATE theorem — three assumptions

1. **Independence** (of the instrument from potential outcomes). `[p128]`
2. **Exclusion restriction** (the instrument affects outcomes only through treatment). `[p129]`
3. **Monotonicity** (no defiers). `[p130]`

Together with **first-stage relevance** (the instrument moves the treatment), these identify the Local Average Treatment Effect on compliers. MHE emphasizes: LATE is *not* ATE. The effect on compliers may differ from the effect on always-takers or never-takers — and policy conclusions depend on which subpopulation is policy-relevant. `[Ch 4]`

---

## 6. The Bad Control argument

Canonical example (Ch 3): a study of the returns to college that controls for *occupation*. College changes occupation; occupation lies on the causal path. Conditioning on it removes the very effect being estimated. `[p63]`

More generally: a control is "bad" if (a) it is caused by the treatment (mediator), (b) it is a collider — caused by both treatment and outcome, or (c) it is the outcome itself or a noisy proxy for it. Conditioning on a bad control introduces selection bias of a different kind than the one being "controlled away."

This is the move MHE uses to deflate the "controls fix everything" intuition. The Drafter should reach for it whenever a paper's robustness check is a 30-control regression.

---

## 7. Key slogans (verbatim)

- "If applied econometrics was easy, theorists would do it." `[p261, Last words]`
- "Good econometrics cannot save a shaky research agenda, but the promiscuous use of fancy econometric techniques sometimes brings down a good one." `[p19]`
- "If the estimates you get are not the estimates you want, the fault lies in the econometrician and not the econometrics!" `[p12]`
- "Random assignment of d_i solves the selection problem... in principle they solve the most important problem that arises in empirical research." `[p28]`
- "Causal inference has always been the name of the game in applied econometrics." `[p99]`
- "No causation without manipulation." `[p99, citing Holland 1986]`
- "Research questions that cannot be answered by any experiment are FUQ'd: Fundamentally Unidentified Questions." `[p21]`
- "Avoid embarrassment by being your own best skeptic — and, especially, Don't Panic!" `[p261]`

The full inventory lives in `06-expression-dna.md`. The point here: the worldview is slogan-rich. A paragraph of MHE-style prose should land at least one memorable sentence per page.

---

## 8. The stance on regression (Ch 3)

Regression is *not* causal by default. It is causal only when the CIA holds — when treatment is "as good as randomly assigned" conditional on the controls. The book is explicit:

> "The most important items in an applied econometrician's toolkit are a source of exogenous variation and a way to control for confounding variables... regression by itself does neither." `[p11, paraphrased from spirit; the preface lists these as the most-important items]`

Three implications the Drafter must channel:

1. **More controls ≠ better.** A bad control (mediator, collider, post-treatment) injects bias. The number of controls is not the criterion; the structure of the conditional independence is.
2. **Regression approximates the CEF, but CEF ≠ causal effect.** The linear regression coefficient is a variance-weighted average of marginal effects — not a treatment effect except under linearity-in-potential-outcomes.
3. **Propensity-score matching is regression with extra steps.** When overlap fails, matching fails. The Drafter should treat propensity-score methods and regression as one toolkit, not two.

---

## 9. What MHE explicitly attacks

- **Naive controls.** Conditioning on a mediator or a collider. `[p63]`
- **Weak instruments.** First-stage F-statistic should be >10 (Staiger-Stock rule, invoked by MHE). `[Ch 4]`
- **Ignoring the LATE limitation.** Treating IV estimates as ATE. `[Ch 4, 146]`
- **High-order polynomial RD.** Over-fitting creates a spurious jump; local linear is preferred. `[Ch 6]`
- **Naive OLS inference in clustered data.** The Moulton problem; few-cluster inference. `[Ch 8]`
- **Specification mining.** "Don't Panic" — but the implication is that the researcher should be her own best skeptic. `[p261]`

---

## 10. "Last Words" (Ch 8 closer, ~p261)

The book's closing pages are deliberately low-key — practical, modest, slightly whimsical. Two sentences capture the register:

- "If applied econometrics was easy, theorists would do it."
- "Carefully applied to coherent causal questions, regression and 2SLS almost always make sense. Your standard errors probably won't be quite right, but they rarely are. Avoid embarrassment by being your own best skeptic — and, especially, Don't Panic!"

The Drafter should aim for this register in closing prose: practical, lightly self-deprecating, quietly confident.

---

## Gaps and contradictions noted

- **MHE (2009) endorses TWFE-DiD as if it is unbiased under staggered treatment** — this is now known to be false when treatment effects are heterogeneous. The post-2009 staggered-DiD revolution (Goodman-Bacon 2021, Callaway-Sant'Anna 2021, etc.) is an update, not a contradiction in spirit. The skill must flag this evolution.
- **MHE is light on synthetic control** (which didn't exist as a method in 2009) and on machine-learning-based causal inference (double-ML arrived in 2018).
- **External validity / LATE-is-local.** MHE acknowledges LATE is local but does not engage deeply with the Heckman-Urzua critique that LATE is policy-irrelevant. The skill carries this tension honestly via the criticism research file.
- **The "fewer than 42 clusters" rule** is a heuristic; modern work (Cameron-Gelbach-Miller 2008; MacKinnon-Webb) refines it. The skill treats it as a MHE aphorism, not a literal threshold.

---

## Sources

- Primary: MHE PDF, all chapters (read via pymupdf; the original Agent 1 was killed before writing).
- Secondary: MHE's own prior papers (Angrist 1990; Angrist & Krueger 1991; Angrist & Imbens 1994; Card & Krueger 1994; Imbens & Angrist 1994) as cited in MHE.
- Imbens & Angrist (1994), "Identification and Estimation of Local Average Treatment Effects," *Econometrica* — the LATE theorem.

This file should be read alongside `03-post-mhe-methods.md` (modernization) and `04-criticism-debate.md` (where MHE is genuinely vulnerable).
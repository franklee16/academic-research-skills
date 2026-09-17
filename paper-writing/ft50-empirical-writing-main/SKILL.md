---
name: ft50-empirical-writing
description: Use when writing or revising empirical research papers targeting FT50 journals across all management disciplines (Accounting, Finance, Management, Marketing, Operations/IS, Economics). Covers the full empirical pipeline — Research Question → Theory → Identification → Data → Results → Robustness → Mechanism → Implications — with discipline-specific journal guidance, identification strategy design, robustness frameworks, mechanism evidence, and writing patterns. Also use when stuck at any stage of an FT50-targeted empirical paper and needing stage-specific guidance.
---

# FT50 Empirical Research Paper Writing

## Overview

The FT50 (Financial Times 50) is the definitive list of 50 premier journals used by the Financial Times to rank business schools globally. Publishing in FT50 journals requires papers to meet the **highest standards of empirical rigor, identification credibility, and theoretical contribution** across all management disciplines.

This skill covers the full empirical pipeline for causal-inference-oriented research: **Research Question → Theory → Identification → Data → Results → Robustness → Mechanism → Economic Significance → Implications**. Unlike MS&E papers that prioritize mathematical modeling or ML papers that emphasize benchmark performance, FT50 empirical papers are evaluated on the **credibility of the causal identification strategy** and the **compelling nature of the research design**.

**Core Principle**: An FT50 empirical paper tells a story of **causal identification**. The reader must be convinced — through a combination of institutional knowledge, theoretical reasoning, and econometric design — that the estimated effect is not merely a correlation but a genuine causal relationship, and that the magnitude is economically meaningful.

---

## When to Use This Skill

- Drafting an empirical paper targeting any FT50 journal across Accounting, Finance, Management, Marketing, Operations/IS, or Economics
- Designing an identification strategy (DID, RDD, IV, RCT, Synthetic Control, matching)
- Building a robustness framework that anticipates reviewer concerns
- Developing mechanism evidence (mediation, moderation, heterogeneity analysis)
- Selecting the right FT50 journal given a research design and contribution profile
- Writing the identification and robustness sections of an empirical paper
- Revising based on reviewer feedback from an FT50 journal (especially on causal claims)
- Converting a working paper or dissertation chapter into an FT50-submittable manuscript
- Assessing whether a research design is strong enough for FT50-level scrutiny

---

## Journal Selection: The FT50 Landscape

### The FT50 List and Discipline Mapping

The FT50 spans six broad management disciplines. Journal selection is a function of your paper's **topic domain**, **identification strategy rigor**, **theoretical contribution type**, and **practical relevance**.

#### Accounting

| Journal | Abbreviation | Core Identity | Emphasis |
|---------|-------------|--------------|----------|
| Journal of Accounting Research | JAR | Archival-empirical, capital markets | Causal identification in accounting settings; disclosure, auditing, regulation |
| Journal of Accounting and Economics | JAE | Positive accounting theory, contracting | Theory-empirical integration; compensation, governance, debt contracting |
| The Accounting Review | TAR | Broad accounting, experimental and archival | Mix of analytical, archival-empirical, and behavioral experimental |
| Contemporary Accounting Research | CAR | Broad international scope | Welcomes non-US settings; diverse methods including qualitative |
| Review of Accounting Studies | RAST | Valuation, disclosure, text analysis | Financially oriented; NLP/textual analysis increasingly common |

**Accounting FT50 Methodology Expectations**: Strong archival-empirical tradition. Panel data with firm and year fixed effects is the baseline. Difference-in-differences and regression discontinuity are standard. IV estimation is expected when endogeneity is a first-order concern. Natural experiments are highly valued. Behavioral experiments accepted at TAR and CAR. Capital market studies require event study methodology with appropriate benchmark models. Standard errors must be clustered at the level of treatment assignment.

#### Finance

| Journal | Abbreviation | Core Identity | Emphasis |
|---------|-------------|--------------|----------|
| Journal of Finance | JF | Top flagship, broad scope | Highest bar for causal identification; asset pricing, corporate finance |
| Journal of Financial Economics | JFE | Corporate finance, governance, contracting | Theory-empirical integration; institutional detail matters |
| Review of Financial Studies | RFS | Asset pricing, fintech, intermediation | Methodological innovation; structural estimation increasingly common |
| Journal of Financial and Quantitative Analysis | JFQA | Quantitative methods, portfolio theory | Methodologically rigorous; welcomes computational methods |

**Finance FT50 Methodology Expectations**: The "identification revolution" has fully arrived. Causal claims demand quasi-experimental or experimental designs. DID with staggered treatment (using Sun & Abraham, Callaway & Sant'Anna, or Borusyak et al. estimators), RDD, IV, and natural experiments. Standard errors clustered at firm or state level. Placebo tests mandatory. Economic magnitude emphasized alongside statistical significance. Matched sample designs common in corporate finance (PSM, CEM, entropy balancing). Event studies must address confounding events and use appropriate estimation windows.

#### Management

| Journal | Abbreviation | Core Identity | Emphasis |
|---------|-------------|--------------|----------|
| Academy of Management Journal | AMJ | Empirical, strong theory, organizational behavior | Compelling stories grounded in rich theory; multi-level research |
| Academy of Management Review | AMR | Pure theory and conceptual development | No empirical data; must propose new theory or substantially extend existing |
| Administrative Science Quarterly | ASQ | Organizational theory, qualitative and quantitative | Deep theoretical contribution; ethnographic, longitudinal, and archival |
| Strategic Management Journal | SMJ | Strategy, competitive advantage, firm performance | Causal identification increasingly required; natural experiments valued |
| Organization Science | OS | Organization theory, formal and informal | Welcomes formal modeling alongside empirical; computational methods |
| Journal of Management | JOM | Broad management, reviews, meta-analyses | Comprehensive reviews with theoretical integration; large-scale empirical |
| Journal of Management Studies | JMS | Broad management, critical and pluralistic | Welcomes heterodox approaches; critical management studies |
| Journal of International Business Studies | JIBS | International business, cross-border strategy | Multi-country empirical designs; comparative institutional analysis |
| Human Relations | HR | Organizational behavior, critical perspectives | Sociologically informed; qualitative and mixed methods valued |
| Human Resource Management | HRM | HR practices, employment relations | Practitioner-relevant but theoretically grounded |
| Leadership Quarterly | LQ | Leadership theory and measurement | Multi-level, multi-source designs; endogeneity addressed in leadership-outcome studies |

**Management FT50 Methodology Expectations**: Methodological pluralism — qualitative (ethnography, grounded theory, multiple case studies), quantitative (survey, archival panel), and mixed methods all accepted. For quantitative studies: multi-level modeling, panel data methods, and increasing demand for causal identification (IV, DID, natural experiments). Survey-based studies must address common method bias, measurement validity (CFA/SEM with appropriate fit indices), and endogeneity. ASQ and AMJ value rich qualitative data and process theorizing. SMJ increasingly requires identification strategies comparable to economics. Theory sections must be extensive and contribute to management theory — purely empirical contributions without theoretical advance are desk-rejected.

#### Marketing

| Journal | Abbreviation | Core Identity | Emphasis |
|---------|-------------|--------------|----------|
| Journal of Marketing | JM | Broad marketing, strategy-focused | Substantive contribution to marketing practice; field experiments valued |
| Journal of Marketing Research | JMR | Quantitative, consumer behavior, methods | Methodologically rigorous; experiments (lab, field, online), econometrics |
| Journal of Consumer Research | JCR | Consumer behavior, psychological foundations | Behavioral experiments; theoretical depth in consumer psychology |
| Marketing Science | MktSci | Quantitative modeling, structural estimation | Analytical models with empirical estimation; structural econometrics |
| Journal of the Academy of Marketing Science | JAMS | Broad marketing, strong theory | Conceptual and empirical; managerial relevance required |
| Journal of Consumer Psychology | JCP | Consumer psychology, experimental | Theory-driven experiments; psychological mechanisms |

**Marketing FT50 Methodology Expectations**: Structural econometric modeling for MktSci (demand estimation with BLP, dynamic structural models). Field and lab experiments for JMR, JCR, JCP. JM values field experiments and large-scale empirical work. JAMS requires strong theoretical contribution with empirical validation. Standard experimental design considerations: power analysis (a priori), randomization checks, manipulation checks, attention checks, demand effects, experimenter bias. Marketing papers must demonstrate both internal validity and external validity (generalizability). Mediation analysis (bootstrapped indirect effects; PROCESS models) is the dominant mechanism-evidence approach in consumer behavior. Moderation analysis to demonstrate boundary conditions is standard. Multi-study packages (3-5 or more studies per paper) are common in JCR and JMR.

#### Operations & Information Systems

| Journal | Abbreviation | Core Identity | Emphasis |
|---------|-------------|--------------|----------|
| Manufacturing & Service Operations Management | M&SOM (MSOM) | Empirical OM, behavioral operations | Data-driven operations; field experiments, structural estimation |
| Operations Research | OR | Mathematical optimization, stochastic models | Proofs, optimality guarantees, computational experiments |
| Information Systems Research | ISR | IS economics, behavioral IS, design science | Econometric identification and analytical modeling both valued |
| MIS Quarterly | MISQ | IS management, digital transformation | Broad IS phenomena; qualitative, quantitative, design science |
| Journal of Operations Management | JOM (Ops) | Empirical OM, supply chain, sustainability | Strong identification, multiple data sources, practice-grounded |
| Production and Operations Management | POM | Broad OM, data-driven, analytics | Empirical, analytical, and behavioral; strong practical relevance |
| Management Science | MS | Broad management science, high rigor | Cross-disciplinary; optimization, econometrics, behavioral experiments |

**Operations & IS FT50 Methodology Expectations**: MS, OR, and MSOM span analytical modeling (optimization, stochastic processes, game theory) and empirical work (DID, IV, structural estimation, field experiments). ISR and MISQ accept econometric identification, analytical modeling, and design science. JOM (Ops) and POM increasingly emphasize empirical identification with multiple data sources, natural experiments, and field experiments. OM empirical papers must demonstrate intimate knowledge of the operational context — "institutional detail" in OM replaces what "theory" does in management. IS papers must address digital technology phenomena with appropriate identification strategies (instrumental variables for endogenous technology adoption, DID for policy/program evaluations). Computational social science and machine learning methods are increasingly accepted in ISR and MISQ.

#### Economics (FT50-listed)

| Journal | Abbreviation | Core Identity | Emphasis |
|---------|-------------|--------------|----------|
| Econometrica | ECTA | Top theory and econometrics | Highest bar for formal theory and methods |
| American Economic Review | AER | Top general interest, short papers | Important, broadly accessible contributions; ~40 page limit in AER |
| Journal of Political Economy | JPE | Chicago tradition, deep theory | Long papers; deep theoretical foundation with empirical validation |
| Quarterly Journal of Economics | QJE | Long empirical papers, applied micro | Institutional detail, natural experiments, credible designs |
| Review of Economic Studies | REStud | Top European-based general interest | Theory and applied work; newer methods welcomed |
| Review of Economics and Statistics | REStat | Applied econometrics, empirical | Methodological innovation in applied settings |
| Journal of Econometrics | JoE | Econometric theory and methods | New estimators, tests, and identification results |
| Journal of Labor Economics | JOLE | Labor economics | Causal identification in labor markets; natural experiments |
| Rand Journal of Economics | RAND | Industrial organization, regulation | IO theory and empirical; structural estimation |
| Journal of Business and Economic Statistics | JBES | Statistical methods for economics | Time series, forecasting, machine learning in economic settings |

**Economics FT50 Methodology Expectations**: The "credibility revolution" originated here. Causal identification is non-negotiable. Papers are evaluated on: (1) identification strategy credibility, (2) institutional detail that motivates the design, and (3) economic significance. Standard designs: DID (with event-study plots showing pre-trends), RDD (with McCrary density tests, donut-hole robustness), IV (with first-stage F-statistic >> 10, plausibly exogenous instruments), RCT (with pre-analysis plan, balance tables, attrition analysis), synthetic control (with in-space placebo tests). Standard errors: cluster-robust at treatment level. Multiple hypothesis testing corrections (Bonferroni, Romano-Wolf, sharpened q-values). P-hacking concerns addressed transparently. Pre-analysis plans and replication packages increasingly required. The QJE event-study plot (coefficient-by-year with confidence intervals) is the gold standard for visualizing DID results.

### Journal Selection Decision Flowchart

```
What is the disciplinary home of your phenomenon?
├── ACCOUNTING (auditing, disclosure, tax, governance, contracting)
│   ├── Strong causal identification + capital markets → JAR, JAE
│   ├── Behavioral/experimental → TAR, CAR
│   ├── International setting → CAR
│   └── Theoretical-empirical integration → JAE, RAST
│
├── FINANCE (asset pricing, corporate, banking, fintech)
│   ├── Top causal identification + broad interest → JF
│   ├── Corporate finance + institutional detail → JFE
│   ├── Asset pricing + structural methods → RFS
│   └── Quantitative/computational methods → JFQA
│
├── MANAGEMENT (strategy, OB, OT, HR, IB, leadership)
│   ├── Strong causal identification + strategy → SMJ
│   ├── Rich theory + quantitative or qualitative → AMJ, ASQ
│   ├── Pure theory (no data) → AMR
│   ├── Formal modeling + empirical → OS
│   ├── Cross-border/cross-cultural → JIBS
│   ├── Leadership focus → LQ
│   └── HR/employment focus → HRM, HR
│
├── MARKETING (strategy, CB, quantitative, advertising)
│   ├── Structural econometric modeling → MktSci
│   ├── Field experiment + strategy → JM
│   ├── Consumer behavior experiments → JCR, JCP
│   ├── Quantitative methods + experiments → JMR
│   └── Conceptual + empirical + managerial → JAMS
│
├── OPERATIONS / IS (supply chain, service ops, digital, analytics)
│   ├── Analytical modeling (optimization/stochastic) → OR, MS
│   ├── Empirical OM (DID, field experiments) → MSOM, JOM (Ops), POM
│   ├── IS economics + econometric identification → ISR
│   ├── IS management + mixed methods → MISQ
│   └── Cross-disciplinary + high rigor → MS
│
└── ECONOMICS (labor, IO, public, development, econometrics)
    ├── Top general interest → AER
    ├── Deep theory + empirical → JPE, ECTA
    ├── Applied micro + natural experiments → QJE, REStud
    ├── Applied econometrics → REStat, JoE, JBES
    ├── Labor → JOLE
    └── IO + regulation → RAND
```

---

## The FT50 Empirical Paper Structure

Unlike the IMRAD format in biomedical sciences or the model-analysis-algorithm structure in MS&E, an FT50 empirical paper follows a **causal-identification-centric** structure:

| Section | Typical Length | Key Content |
|---------|---------------|-------------|
| Abstract | 100-250 words | Research question, identification strategy, key estimate, mechanism, economic significance |
| S1 Introduction | 3-5 pages | Motivating puzzle, research question, institutional context preview, identification approach, preview of findings, contributions (numbered, 3-5) |
| S2 Institutional Background / Theory | 3-6 pages | Institutional details that motivate the design; theoretical framework generating testable predictions; conceptual model |
| S3 Data & Measurement | 3-5 pages | Data sources, sample construction (with attrition table), variable definitions, descriptive statistics, balance/correlation table |
| S4 Identification Strategy / Research Design | 3-6 pages | Identification challenge (endogeneity source), empirical specification (estimating equation), identification assumptions (stated and defended), graphical evidence (reduced-form plots) |
| S5 Main Results | 4-8 pages | Baseline specification results, coefficient of interest interpretation, economic magnitude discussion (back-of-envelope calculations), falsification/placebo tests |
| S6 Robustness | 4-8 pages | Alternative DV, alternative IV, alternative sample, alternative specification, alternative estimator, placebo in time/space, bounding (Oster, Altonji et al.), sensitivity analysis |
| S7 Mechanism Evidence | 2-5 pages | Mediation analysis, moderation analysis, heterogeneity across theoretically motivated dimensions, ruling out alternative mechanisms |
| S8 Discussion & Implications | 2-4 pages | Summary of findings, theoretical contribution, practical/managerial/policy implications, connection to prior literature |
| S9 Conclusion | 0.5-1 page | Summary, limitations, future research directions |
| References | — | 40-80 papers typical for FT50 empirical papers |
| Online Appendix | Unlimited | Additional robustness, alternative specifications, additional mechanism tests, data construction details, replication package |

**Key structural differences from other writing traditions**:

1. **The identification section is the centerpiece.** Reviewers read this before anything else after the introduction. If the identification is not credible, the paper is rejected regardless of the results.
2. **The institutional background section is essential for quasi-experimental designs.** It justifies why the natural experiment or instrumental variable is valid. Without institutional detail, the identification strategy lacks credibility.
3. **Robustness is not an afterthought.** In FT50 papers, the robustness section is often longer than the main results section. It must systematically address every conceivable threat to validity.
4. **Mechanism evidence is increasingly required**, even in papers where the reduced-form relationship is sufficient for policy/practice implications. Knowing *why* an effect exists strengthens causal interpretation.
5. **Economic significance** must be discussed alongside statistical significance. A statistically significant coefficient with a tiny magnitude may not warrant publication.

---

## Identification Strategies

The credibility of the identification strategy is the single most important factor in FT50 empirical papers. Each strategy has specific specification requirements, diagnostic tests, and common pitfalls.

### A. Difference-in-Differences (DID)

#### Specification

The canonical two-way fixed effects (TWFE) specification:

$$Y_{it} = \alpha_i + \lambda_t + \beta \cdot Treat_i \times Post_t + \varepsilon_{it}$$

For staggered treatment timing, the event-study specification:

$$Y_{it} = \alpha_i + \lambda_t + \sum_{k \neq -1} \beta_k \cdot D_{it}^k + \varepsilon_{it}$$

where $D_{it}^k$ are indicators for $k$ periods relative to treatment.

**Modern Staggered DID Estimators** (required for settings with heterogeneous treatment effects and staggered adoption):
- Sun & Abraham (2021): `eventstudyinteract` in Stata, `sunab` 
- Callaway & Sant'Anna (2021): `csdid` in Stata, `did` in R
- Borusyak, Jaravel & Spiess (2024): `did_imputation` in Stata, `didimputation` in R
- de Chaisemartin & D'Haultfœuille (2020): `did_multiplegt` in Stata, `DIDmultiplegt` in R
- Gardner (2022): `did2s` in Stata and R

#### Checklist

- [ ] Event-study plot (coefficient-by-period with 95% CI; reference period at $t=-1$) showing pre-trends
- [ ] No evidence of differential pre-trends (joint F-test of pre-treatment coefficients = 0, with p-value reported)
- [ ] For staggered designs: use at least one modern estimator that is robust to heterogeneous treatment effects
- [ ] Treatment and control groups defined before analysis; no ad-hoc group construction
- [ ] Standard errors clustered at the level of treatment assignment (state, firm, industry)
- [ ] Composition of treatment and control groups stable over time (balanced panel or demonstrate no selective attrition)
- [ ] Parallel trends assumption defended with institutional arguments, not just statistical tests
- [ ] Mean of dependent variable in control group reported (for economic magnitude interpretation)
- [ ] Number of treated and control units reported
- [ ] Never-treated, not-yet-treated, and already-treated clearly distinguished in staggered designs

#### Common Pitfalls

| Pitfall | Consequence | Remedy |
|---------|------------|--------|
| TWFE with staggered heterogeneous effects | Negative weights; biased $\hat{\beta}$ | Use modern staggered DID estimators |
| Clustering at wrong level | Severely understated standard errors | Cluster at treatment assignment level; consider wild cluster bootstrap with few clusters |
| Interpreting pre-trend insignificance as proof of parallel trends | Statistical power issue | Provide economic argument for parallel trends; use pre-trend magnitude relative to treatment effect |
| Selective attrition correlated with treatment | Biased estimates | Show attrition by treatment status; bounding approaches |
| Treatment effect heterogeneity hidden by aggregation | Misleading average effect | Report treatment effect heterogeneity by cohort/duration |
| Event-study with binning of endpoints | Arbitrary endpoint choice | Report full dynamic specification; justify endpoint binning |
| Contamination from other concurrent treatments | Confounded estimates | Document all concurrent policy changes; consider synthetic control as robustness |

### B. Regression Discontinuity Design (RDD)

#### Specification

Sharp RDD:

$$Y_i = \alpha + \beta \cdot D_i + f(X_i - c) + \gamma \cdot D_i \cdot f(X_i - c) + \varepsilon_i$$

where $D_i = \mathbf{1}[X_i \geq c]$, $f(\cdot)$ is a flexible polynomial (linear or quadratic) of the running variable centered at the cutoff $c$, and the interaction allows different slopes on each side.

Fuzzy RDD:

$$D_i = \alpha_1 + \pi \cdot Z_i + f_1(X_i - c) + \nu_i \quad \text{(first stage)}$$
$$Y_i = \alpha_2 + \beta_{FRD} \cdot \widehat{D}_i + f_2(X_i - c) + \varepsilon_i \quad \text{(second stage)}$$

where $Z_i = \mathbf{1}[X_i \geq c]$ is the instrument.

**Bandwidth selection**: MSE-optimal bandwidth (Calonico, Cattaneo & Titiunik, CCT), coverage error rate (CER) optimal bandwidth. Use `rdrobust` in Stata/R.

#### Checklist

- [ ] McCrary (2008) density test: no manipulation of the running variable at the cutoff
- [ ] Baseline covariate balance at the cutoff (regress each predetermined covariate on treatment at the cutoff)
- [ ] Robustness to bandwidth choice: plot $\hat{\beta}$ as a function of bandwidth ($h \in [0.5 h^*, 2 h^*]$)
- [ ] Robustness to polynomial order: linear, quadratic, cubic
- [ ] Donut-hole RDD (excluding observations very close to the cutoff)
- [ ] Placebo cutoffs at other values of the running variable
- [ ] Conventional, bias-corrected, and robust confidence intervals reported (CCT)
- [ ] Optimal bandwidth reported with justification
- [ ] Local-linear specification preferred over higher-order polynomials (Gelman & Imbens, 2019)
- [ ] Number of observations above and below the cutoff reported
- [ ] Graphical evidence: binned scatterplot with global polynomial fit (or local means)

#### Common Pitfalls

| Pitfall | Consequence | Remedy |
|---------|------------|--------|
| High-order global polynomials | Noisy estimates, overfitting | Use local-linear within optimal bandwidth |
| Running variable manipulation | Invalid design | McCrary test; institutional argument why manipulation impossible |
| Donut-hole without justification | Excluding informative observations | Transparently report; justify if heaping at cutoff |
| Inference with discrete running variable | Standard errors incorrect | Use randomization inference with discrete running variable (Cattaneo et al.) |
| Extrapolation: LATE interpretation | Not generalizable | Interpret as LATE at cutoff; caution about external validity |
| Ignoring bandwidth uncertainty | Understated standard errors | Use robust confidence intervals (CCT) |

### C. Instrumental Variables (IV)

#### Specification

First stage: $X_i = \pi_0 + \pi_1 Z_i + \Pi_2 W_i + \nu_i$  

Second stage (structural): $Y_i = \beta_0 + \beta_1 \widehat{X}_i + \beta_2 W_i + \varepsilon_i$

Reduced form: $Y_i = \gamma_0 + \gamma_1 Z_i + \gamma_2 W_i + \eta_i$

Where $Z_i$ is the instrument, $X_i$ is the endogenous regressor, $W_i$ are exogenous controls.

#### Checklist

- [ ] Economic/institutional argument for instrument relevance (not just statistical)
- [ ] Economic/institutional argument for exclusion restriction (why $Z$ affects $Y$ only through $X$)
- [ ] First-stage F-statistic reported: $F > 10$ (Stock & Yogo critical values); Kleibergen-Paap F-statistic for clustered SE
- [ ] First-stage coefficients reported in a table (not just "results available upon request")
- [ ] Reduced-form results reported alongside IV results (transparent: show both)
- [ ] OLS results reported for comparison (bracket the IV estimate)
- [ ] Limited information maximum likelihood (LIML) if weak instruments or many instruments
- [ ] Overidentification test (Sargan-Hansen J-test) if multiple instruments, but acknowledge limitations
- [ ] "Plausibly exogenous" sensitivity analysis (Conley, Hansen & Rossi, 2012) if exclusion restriction is uncertain
- [ ] Interpretation: LATE vs. ATE discussion (whose treatment effect is identified?)
- [ ] Standard errors: cluster-robust if instrument varies at group level

#### Common Pitfalls

| Pitfall | Consequence | Remedy |
|---------|------------|--------|
| Weak instruments ($F < 10$) | Biased IV toward OLS; large SE | Use LIML; report weak-instrument robust CIs (Anderson-Rubin) |
| Exclusion restriction violation | Inconsistent estimates | Plausibly exogenous bounds (Conley et al.); never-happen tests |
| Bad controls in IV | Inconsistent estimates | Controls must be predetermined or exogenous; justify each control |
| Many instruments relative to sample | Overfitting first stage; biased IV | LIML instead of 2SLS; jackknife IV |
| Interpreting LATE as ATE | Overgeneralization | Discuss complier characteristics; compare to full sample |
| Not reporting reduced form | Hides weak/broken instrument story | Always report reduced form alongside IV |
| First-stage with FE and nonlinearity | Incorrect standard errors in manual 2SLS | Use `ivreghdfe` (Stata) or `feols` with IV (R fixest) |

### D. Randomized Controlled Trial (RCT)

#### Specification

Simple comparison of means (ATE):

$$\hat{\tau} = \bar{Y}_T - \bar{Y}_C$$

With covariate adjustment for precision:

$$Y_i = \alpha + \tau \cdot T_i + \beta X_i + \varepsilon_i$$

where $T_i$ is treatment assignment and $X_i$ are pre-specified baseline covariates.

#### Checklist

- [ ] Pre-analysis plan (PAP) registered (AEA RCT Registry, OSF, AsPredicted); link provided
- [ ] Power analysis reported (ex ante minimum detectable effect)
- [ ] Randomization procedure described in detail (stratification, blocking, clustering)
- [ ] Balance table: pre-treatment covariates compared across treatment and control; joint F-test p-value
- [ ] Attrition analysis: differential attrition by treatment status; bounding (Lee bounds) if asymmetric
- [ ] Intention-to-treat (ITT) as primary specification
- [ ] Treatment-on-the-treated (TOT/LATE) as secondary specification if imperfect compliance
- [ ] Multiple hypothesis testing correction (Romano-Wolf stepdown, sharpened q-values, or Westfall-Young)
- [ ] Heterogeneous treatment effects analysis (pre-specified subgroups)
- [ ] Standard errors: robust (HC2/HC3); cluster-robust if randomization is clustered
- [ ] CONSORT diagram (flow of participants through each stage)

#### Common Pitfalls

| Pitfall | Consequence | Remedy |
|---------|------------|--------|
| No pre-analysis plan | p-hacking concerns | Register PAP before data collection or accessing outcome data |
| Differential attrition | Biased ATE | Report attrition by arm; Lee bounds; inverse probability weighting |
| Multiple outcomes without correction | Inflated Type I error | PAP must specify primary outcome; correct for multiple testing |
| Spillovers / SUTVA violation | Biased ATE | Design to minimize spillovers; measure and model if expected |
| Non-compliance ignored | ATE vs. ITT confusion | Report both ITT and TOT; use randomization as instrument |
| Underpowered | Null results uninformative | Ex ante power analysis; report minimum detectable effect ex post |
| Hawthorne / John Henry effects | Reduced external validity | Design placebo arm or measure awareness; discuss limitations |
| Baseline imbalance despite randomization | Reduced credibility | Show balance; adjust with pre-specified covariates (not selected post-hoc) |

### E. Synthetic Control Method (SCM)

#### Specification

The synthetic control is a weighted average of control units:

$$\hat{\tau}_{1t} = Y_{1t} - \sum_{j=2}^{J+1} w_j^* Y_{jt}$$

where $w_j^*$ are weights chosen to minimize the pre-treatment gap in outcomes and predictors between the treated unit and the synthetic control.

#### Checklist

- [ ] Single (or few) treated unit(s) clearly identified (SCM designed for small number of treated units)
- [ ] Donor pool of control units described with inclusion/exclusion rationale
- [ ] Predictor variables listed (pre-treatment outcomes + covariates); their weights reported
- [ ] Unit weights reported in a table (which control units matter and with what weight)
- [ ] Pre-treatment fit visually demonstrated (gap plot); RMSPE reported
- [ ] In-space placebo tests: run SCM for each control unit as if treated; compare treatment effect to placebo distribution
- [ ] Ratio of post/pre RMSPE reported (Abadie, Diamond & Hainmueller, 2010)
- [ ] Leave-one-out robustness (remove each donor unit with positive weight one at a time)
- [ ] Robustness to predictor set (alternative weighting schemes)
- [ ] Inference: p-value from rank of post/pre RMSPE ratio among all units
- [ ] Generalized SCM (Xu, 2017) or matrix completion (Athey et al., 2021) for multiple treated units with staggered adoption

#### Common Pitfalls

| Pitfall | Consequence | Remedy |
|---------|------------|--------|
| Poor pre-treatment fit | Invalid counterfactual | Include more pre-treatment outcomes; expand predictor set; reconsider donor pool |
| Interpolation bias (negative weights) | Biased effect | Use constrained SCM (non-negative weights); check for extrapolation |
| Too few pre-treatment periods | Overfitting; poor fit | Minimum 10+ pre-treatment periods recommended |
| Ignoring aggregate shocks | Biased effect | Use interactive fixed effects / generalized SCM |
| Over-reliance on p-values from small N | Misleading inference | Qualify with N of donor pool; use alternative inference methods |

### F. Matching Methods (PSM, CEM, Entropy Balancing)

#### Specification

Propensity Score Matching (PSM):

1. Estimate propensity score: $p(X_i) = \Pr(T_i = 1 | X_i)$ via logit/probit
2. Match treated to control units on $\hat{p}(X_i)$ (1:1 nearest neighbor, with or without caliper)
3. Estimate ATT: $\hat{\tau}_{ATT} = \frac{1}{N_T} \sum_{i: T_i=1} (Y_i - \sum_{j: T_j=0} w_{ij} Y_j)$

Coarsened Exact Matching (CEM): Temporarily coarsen each variable into bins, exact match on bins, then estimate treatment effect on matched data.

Entropy Balancing: Re-weight control observations to achieve exact balance on specified moments of covariates.

#### Checklist

- [ ] Matching is used as a supplementary method to regression, not as a standalone solution to endogeneity
- [ ] Selection on observables assumption (CIA/unconfoundedness) explicitly stated and defended
- [ ] Variables in the propensity score: only pre-treatment covariates unaffected by treatment
- [ ] Common support demonstrated (overlapping histograms of propensity scores)
- [ ] Covariate balance after matching reported (standardized differences < 0.1 or 0.25; variance ratios near 1)
- [ ] Matching procedure transparently described (algorithm, caliper, replacement, ratio)
- [ ] Outcome analysis on matched sample: standard errors should account for matching uncertainty or use Abadie-Imbens SE
- [ ] Sensitivity to unobserved confounding: Rosenbaum bounds (for continuous outcomes) or Oster/Imbens bounds
- [ ] CEM or entropy balancing preferred over PSM due to reduced researcher degrees of freedom

#### Common Pitfalls

| Pitfall | Consequence | Remedy |
|---------|------------|--------|
| PSM as primary identification strategy | Selection on unobservables remains | Use matching as robustness to parametric assumptions, not for causal identification |
| Post-treatment variables in propensity score | Biased estimates | Only pre-treatment variables; no mediators or outcomes |
| No common support check | Extrapolation bias | Trim observations outside common support; report overlap |
| Ignoring matching uncertainty in SE | Understated standard errors | Use Abadie-Imbens robust SE or bootstrap the entire matching procedure |
| Researcher discretion in matching algorithm | p-hacking | Pre-specify matching approach; report robustness to alternative algorithms |
| Standardized differences not reported | Unverifiable balance | Report love plot or balance table with standardized differences before/after |

---

## Robustness Standards for FT50

FT50 reviewers expect a comprehensive robustness framework that systematically addresses threats to internal validity. Robustness is not a collection of ad-hoc checks — it is an organized, theoretically motivated battery of tests.

### The Robustness Pyramid (Ordered by Priority)

```
Level 5: Sensitivity to Unobservables (Oster Bounds, Rosenbaum Bounds, Imbens Bounds)
    ↑
Level 4: Placebo / Falsification Tests (In-Time, In-Space, In-Group)
    ↑
Level 3: Alternative Specification / Estimator (Poisson, Logit, Quantile, LASSO controls)
    ↑
Level 2: Alternative Sample (Restricted/Balanced Panel, Excluding Outliers, Trimming)
    ↑
Level 1: Alternative DV and IV (Re-measurement, Alternative Operationalizations)
    ↑
Baseline: Main Specification
```

### Robustness Checklist by Level

#### Level 1: Alternative Dependent Variables and Key Independent Variables

- [ ] Alternative measurement of the dependent variable (log vs. level, per-capita vs. total, alternative data source)
- [ ] Alternative measurement of the key independent variable (continuous vs. binary, alternative threshold, alternative source)
- [ ] If using a constructed index: show components separately; demonstrate robustness to index construction method
- [ ] If using a ratio: show numerator and denominator separately; demonstrate relationship is not driven by denominator
- [ ] If using textual/sentiment-based measure: robustness to alternative dictionaries, algorithms, or human-coding validation

#### Level 2: Alternative Sample

- [ ] Restricted sample (e.g., exclude financial crisis years, exclude largest 1% of firms, exclude early/late adopters)
- [ ] Balanced panel (if main sample is unbalanced)
- [ ] Excluding influential observations (DFBETA, Cook's distance; report with and without)
- [ ] Jackknife: exclude one unit/country/industry at a time
- [ ] Sample split by expected effect magnitude (e.g., high vs. low predicted compliance)
- [ ] Winsorization robustness: alternative thresholds (1%/99%, 5%/95%, no winsorization)

#### Level 3: Alternative Specification and Estimator

- [ ] Alternative fixed effects structure (e.g., adding industry×year FE, region×year FE)
- [ ] Alternative functional form (log-linear, linear-log, Poisson pseudo-maximum likelihood for non-negative outcomes)
- [ ] Alternative estimator: OLS vs. Poisson vs. Negative Binomial for count outcomes; linear probability vs. logit/probit for binary outcomes
- [ ] Quantile regression (effect at median, 25th, 75th percentiles)
- [ ] LASSO/post-double-selection for high-dimensional controls (Belloni, Chernozhukov & Hansen)
- [ ] Standard error robustness: cluster at alternative level, Conley spatial SE, wild cluster bootstrap (when clusters < 50)
- [ ] Methods robust to heteroskedasticity: HC2, HC3 standard errors
- [ ] If panel: robustness to including/excluding unit-specific linear time trends

#### Level 4: Placebo and Falsification Tests

- [ ] **In-time placebo**: Move treatment date earlier (e.g., 2, 3, 4 periods before actual treatment); no significant "effect"
- [ ] **In-space placebo**: Assign treatment to units that were never treated; no significant "effect"
- [ ] **In-group placebo**: Test treatment on an outcome that *should not* be affected (theoretical justification required)
- [ ] **Alternative dependent variable that should not be affected**: Demonstrate discriminant validity
- [ ] **Randomization inference**: Shuffle treatment assignment; compare actual estimate to distribution of placebo estimates

#### Level 5: Sensitivity to Unobservables

- [ ] **Oster (2019) bounds**: $\delta$ for $\beta = 0$ — how large must selection on unobservables be relative to selection on observables to nullify the result? Rule of thumb: $\delta > 1$ is reassuring.
- [ ] **Altonji, Elder & Taber (2005) ratio**: Ratio of coefficient movement with and without controls; larger ratio = less sensitivity.
- [ ] **Rosenbaum bounds** (for matching designs): $\Gamma$ — by what factor must the odds of treatment differ between treated and control (due to an unobservable) to change inference? Report $\Gamma$ at which p-value crosses 0.05.
- [ ] **Imbens (2003) / Conley, Hansen & Rossi (2012)**: "Plausibly exogenous" IV bounds; report treatment effect CI under various degrees of exclusion restriction violation.

### Robustness Reporting Standards

| Requirement | Frequency | Journal Types |
|-------------|-----------|--------------|
| Alternative DV | Every paper | All FT50 |
| Alternative sample | Every paper | All FT50 |
| Alternative specification | Every paper | All FT50 |
| Placebo in time | Quasi-experimental | Economics, Finance, Accounting |
| Placebo in space | Quasi-experimental | Economics, Finance, Accounting |
| Oster bounds | Selection-on-observables designs | Management, Marketing, OB |
| Randomization inference | Few clusters | Economics, Finance |
| Multiple hypothesis correction | Multiple outcomes/treatments | Economics, Marketing |
| Pre-analysis plan | RCT | Economics, Marketing, OB |

---

## Mechanism Evidence

FT50 papers increasingly require not just demonstrating *that* X causes Y, but *why* X causes Y. Mechanism evidence strengthens causal interpretation and theoretical contribution.

### Three Types of Mechanism Evidence

#### 1. Mediation Analysis (Causal Pathway)

The classical Baron & Kenny (1986) approach:

1. $Y = \alpha_1 + c X + \varepsilon_1$ — Total effect ($c$ significant)
2. $M = \alpha_2 + a X + \varepsilon_2$ — X affects mediator ($a$ significant)
3. $Y = \alpha_3 + c' X + b M + \varepsilon_3$ — Direct ($c'$) and indirect ($a \times b$) effects

**Modern standards for FT50**:
- Bootstrapped confidence intervals for indirect effect ($a \times b$) with 5,000-10,000 resamples (Preacher & Hayes, 2004, 2008)
- Report bias-corrected and percentile bootstrap CIs; if CI excludes zero, mediation is supported
- For experimental designs: use parallel mediation models (PROCESS macro) or structural equation modeling (SEM)
- For observational designs: Acknowledge that mediators are endogenous; use *causal mediation analysis* (Imai, Keele & Tingley, 2010) or IV-based mediation (Dippel et al., 2020)
- **Key limitation**: Mediation analysis in observational data requires the same identification assumptions for the mediator as for the treatment

#### 2. Moderation Analysis (Boundary Conditions)

Moderation demonstrates *when* or *for whom* the treatment effect varies:

$$Y = \alpha + \beta_1 X + \beta_2 Z + \beta_3 X \times Z + \varepsilon$$

- **Continuous moderator**: Simple slopes analysis at $\pm 1$ SD of $Z$; Johnson-Neyman regions of significance
- **Categorical moderator**: Subgroup analysis with Chow test for difference in coefficients
- **Reporting**: Interaction plot with confidence bands; marginal effects plot
- **Caution**: Subgroup analyses must be pre-specified in PAPs for experimental designs; ex-post subgroup fishing inflates Type I error
- **FT50 expectations**: Moderation results should be theoretically motivated, not data-mined; discuss why the moderator should matter based on theory or institutional context

#### 3. Heterogeneity Analysis (Treatment Effect Heterogeneity)

Heterogeneity analysis examines how treatment effects vary across theoretically relevant dimensions:

$$Y = \alpha + \beta_1 D + \beta_2 D \times Z + \gamma Z + \varepsilon$$

- **Approaches**:
  - Split-sample estimation (by firm size, industry, region, time period)
  - Interaction terms (continuous treatment heterogeneity)
  - Causal forest / generalized random forest (Athey, Tibshirani & Wager, 2019)
  - Quantile treatment effects (effect at different points of the outcome distribution)
- **Levels of heterogeneity relevant by discipline**:
  - Economics: regional, demographic, time period heterogeneity
  - Finance: firm size, leverage, governance quality, institutional ownership
  - Accounting: Big N vs. non-Big N auditors, high vs. low analyst following
  - Management: industry dynamism, firm capabilities, leadership characteristics
  - Marketing: product category, consumer segment, channel type
  - Operations: process type, supply chain complexity, firm size
- **Reporting**: Coefficient plots by subgroup; forest plots; interaction coefficients with confidence intervals

### Mechanism Evidence Best Practices

| Practice | Rationale |
|----------|-----------|
| Pre-register mechanism hypotheses | Prevents HARKing; distinguishes confirmatory from exploratory |
| Report null mechanism results | Counter publication bias; build cumulative knowledge |
| Triangulate with qualitative evidence | Mixed methods strengthens causal narrative |
| Distinguish mediation from confounding | Mediation = causal pathway; confounding = common cause; different remedies |
| Multiple mediators: test simultaneously | Parallel mediation avoids omitted mediator bias |
| Ruling out alternative mechanisms | Strengthen your mechanism by testing—and rejecting—plausible alternatives |

---

## Common FT50 Rejection Reasons

Understanding why FT50 papers are rejected is essential for prevention. The following are based on editorial reports, reviewer comments, and published editorials across FT50 journals.

| Reason | Frequency | Discipline-Specific | Prevention |
|--------|-----------|---------------------|------------|
| **Identification not credible** — endogeneity not adequately addressed; causal claims unsupported | Very High | Economics, Finance, Accounting (critical); Management, Marketing (increasing) | Invest in identification design; use quasi-experimental variation; be honest about what the design can and cannot identify |
| **Insufficient theoretical contribution** — "so what?"; contribution is incremental | Very High | Management (critical: AMJ, ASQ, AMR require theoretical advance); Marketing (JCR, JCP) | Explicitly state contribution to theory; gap table comparing to prior literature on theoretical dimensions |
| **Mechanism not established** — demonstrates correlation but not why the effect exists | High | All disciplines increasingly | Include mediation, moderation, or heterogeneity analysis; rule out alternative mechanisms; contextual qualitative evidence |
| **Robustness insufficient** — reviewer can construct a plausible alternative explanation not addressed | High | Economics, Finance (critical) | Use the Robustness Pyramid; anticipate every reviewer objection; preemptively address concerns |
| **Economic significance negligible** — statistically significant but tiny magnitude | Medium-High | Economics, Finance, Accounting | Report economic magnitude (elasticities, back-of-envelope calculations); benchmark against related estimates |
| **Selection on unobservables not addressed** — in non-experimental designs | High | Management, OB, Marketing (survey-based studies) | Oster bounds, Rosenbaum bounds, Imbens bounds; endogeneity discussion; instrumental variables |
| **Sample construction opaque** — replication impossible; observations lost unexplained | Medium | All FT50 | Attrition table; sample selection criteria documented step-by-step; CONSORT diagram (if applicable) |
| **Multiple hypothesis testing unaddressed** — probability of false positive inflated | Medium | Economics (critical); Marketing, Management (experiments) | Bonferroni, Holm, Romano-Wolf, Benjamini-Hochberg; pre-specify primary outcome |
| **Common method bias** — same source, same method, same time for DV and IV | High | Management, OB, Marketing (survey studies) | Multi-source, multi-wave, multi-method designs; marker variable; procedural and statistical remedies |
| **Poor fit with journal scope** — paper would be fine at a different FT50 journal | Medium | All | Use the Journal Selection guide in this skill |
| **Standard errors incorrectly computed** — clustering, heteroskedasticity, autocorrelation unaddressed | Medium-High | Economics, Finance, Accounting | Cluster at treatment assignment level; report standard error robustness; diagnostic tests |
| **Pre-trends in DID problematic** — differential pre-trends visible but ignored | Medium-High | All (quasi-experimental) | Event-study plot with pre-period coefficients; joint F-test; honest discussion |
| **Instrument validity questionable** — exclusion restriction not defended | High | Economics, Finance | Institutional argument; falsification tests; plausibly exogenous bounds |
| **p-hacking / specification searching** — results not robust to reasonable alternatives | Medium-High | All FT50 | Specification curve analysis; multiverse analysis; pre-registration; transparent robustness reporting |
| **Writing quality / narrative clarity** — paper hard to follow; contribution buried | Medium | All FT50 | Clear motivation (motivating puzzle pattern); signposting; structured writing; see Writing Patterns below |

---

## 0-to-Draft Pipeline: Five-Stage Workflow

This is the core workflow of this skill. Each stage builds on the previous. Stages 1-3 are sequential; Stages 4-5 can partially overlap. At each stage, ask the user for their current materials before proceeding.

---

### Stage 1: Question Formulation & Positioning

**Goal**: Define a compelling research question, identify the identification challenge, establish the theoretical/conceptual framework, select a target FT50 journal, and position the paper's contribution.

**Input needed from user**: Research area, preliminary phenomenon of interest, any existing data access or institutional knowledge, any preliminary literature review.

**Agent actions**:

```
1.1 Understand the phenomenon and research question
    - Ask: What is the economic/managerial phenomenon? What is the outcome of interest?
    - What treatment/policy/shock/variation does the paper exploit?
    - Is the research question causal ("does X cause Y?"), descriptive, or predictive?
    - Clarify: What would ideal identification look like? What is feasible?
    - Output: One-paragraph research question with clear outcome and treatment/variation

1.2 Identify the core endogeneity challenge
    - Omitted variable bias? Simultaneity/reverse causality? Measurement error? Selection?
    - Self-selection into treatment? Policy endogeneity?
    - What confounds the relationship between X and Y?
    - Output: explicit endogeneity diagnosis

1.3 Theoretical / conceptual grounding
    - Does the paper build on an existing theory (agency theory, transaction cost economics, institutional theory, etc.)?
    - Or does it develop a conceptual framework from institutional knowledge?
    - What are the testable predictions?
    - Management field: identify the theoretical conversation the paper joins
    - Economics/Finance: identify the behavioral/institutional mechanism being tested
    - Output: theoretical framework summary with predictions

1.4 Literature gap analysis
    - Search for 15-20 closest papers using paper-lookup or research-lookup
    - Map literature along dimensions: research question, method/identification, data, key finding, theoretical lens
    - Build a structured Gap Table
    - Identify: what does this paper do that no prior paper has done?
    - Output: draft gap table + explicit differentiation statement

1.5 FT50 journal selection
    - Use the Journal Selection guide and Decision Flowchart above
    - Match: disciplinary home + identification strategy + contribution type → journal(s)
    - Consider: Which FT50 journals have recently published on similar topics? What is the "conversation" your paper joins?
    - Output: recommended primary journal + 1-2 fallback options with rationale

1.6 Contribution statement
    - Formulate the one-sentence contribution: "Using [identification strategy] in [empirical context], we find that [treatment] causes [outcome] through [mechanism], contributing to [literature stream(s)]."
    - Draft 3-5 numbered contributions: conceptual/theoretical (1-2), empirical (1-2), practical/managerial (1)
    - Output: contribution list

1.7 Writing plan
    - Outline the paper structure based on the FT50 Empirical Paper Structure (above)
    - Estimate page allocation per section for target journal
    - Identify: what data is needed? what identification strategy? what robustness tests?
    - Output: section-by-section writing plan
```

**Stage 1 exit criteria**: Research question precisely stated, endogeneity challenge identified, theoretical grounding established, gap table completed, target journal chosen, contribution list written, writing plan ready.

---

### Stage 2: Identification Design

**Goal**: Design the identification strategy, select data sources, and plan the empirical framework — the centerpiece of an FT50 empirical paper.

**Input needed from user**: Research question and endogeneity challenge (from Stage 1), data sources (existing or planned), institutional context knowledge.

**Agent actions**:

```
2.1 Identification strategy selection
    - Given the empirical context and data structure, which design is feasible?
    - Match variation type → identification strategy:
        - Policy change over time across units → DID (staggered or classic)
        - Sharp cutoff in assignment rule → RDD
        - Plausibly exogenous variation source → IV
        - Randomized intervention → RCT
        - Single treated unit with many controls → SCM
        - Selection on observables (last resort) → matching + Oster bounds
    - Output: recommended identification strategy with feasibility assessment

2.2 Estimation equation specification
    - Write the formal estimating equation(s)
    - Define: dependent variable, key independent variable, control variables, fixed effects, standard error structure
    - Justify each control variable (predetermined; not "bad controls")
    - Specify standard error clustering level
    - Output: formal empirical specification

2.3 Identification assumptions documentation
    - For each assumption of the chosen strategy, state:
        - What the assumption is (in plain language)
        - Why it is plausible in this setting (institutional argument)
        - How it will be tested/defended (diagnostic test)
        - What happens if it fails (robustness or caveat)
    - Output: identification assumptions table

2.4 Data source assessment
    - Identify data sources: administrative, survey, commercial, scraped, hand-collected
    - Assess: sample size adequacy (power analysis), temporal coverage, unit coverage, variable availability
    - Document: data access, confidentiality, IRB requirements
    - Output: data plan with sources, variables, and coverage

2.5 Sample construction plan
    - Define inclusion/exclusion criteria
    - Plan sample construction flowchart / CONSORT diagram
    - Plan attrition analysis
    - Output: sample construction protocol

2.6 Robustness framework planning
    - Using the Robustness Pyramid, plan robustness tests at each level
    - Identify: which tests are diagnostic for the specific identification strategy?
    - Plan mechanism tests
    - Output: robustness plan document
```

**Stage 2 exit criteria**: Identification strategy selected and justified, estimation equations specified, identification assumptions documented and defended, data sources identified, sample construction planned, robustness framework planned.

---

### Stage 3: Analysis & Results

**Goal**: Execute the analysis, generate results tables and figures, and verify the statistical integrity of all findings.

**Input needed from user**: Data (or data access), identification design (from Stage 2), statistical software.

**Agent actions**:

```
3.1 Data preparation
    - Execute sample construction protocol (from Stage 2.5)
    - Produce attrition table
    - Handle: missing values (document pattern; justify method), outliers (winsorization at defensible thresholds), measurement error
    - Output: final analysis sample + sample construction documentation

3.2 Descriptive evidence
    - Summary statistics table (N, mean, SD, min, max, percentiles)
    - Balance table / correlation table
    - Time series plot of key variables (if time series)
    - Graphical evidence: maps (if geographic), trends, distributions
    - Output: Tables 1-2 + descriptive figures

3.3 Identification diagnostics
    - Execute all diagnostic tests specified in Stage 2.3
    - DID: event-study plot with pre-trends
    - RDD: McCrary density test, covariate balance at cutoff, RD plot
    - IV: first-stage table with F-statistic, reduced form
    - RCT: balance table, attrition by arm
    - SCM: pre-treatment fit plot, unit weight table
    - Matching: standardized differences before/after matching (love plot)
    - Output: identification diagnostics section + diagnostic figures

3.4 Main results estimation
    - Estimate baseline specification
    - For DID: event-study specification (preferred over single Post coefficient)
    - For RDD: local-linear with optimal bandwidth
    - For IV: 2SLS (first stage, reduced form, and structural equation all reported)
    - Report: coefficients, standard errors, p-values, confidence intervals
    - Include control mean of DV (for economic magnitude context)
    - Output: Main results tables + key coefficient plot

3.5 Economic significance interpretation
    - Compute: standardized effect size (Cohen's d or equivalent)
    - Back-of-envelope calculation: what does the coefficient mean in practical terms?
    - Benchmark against related estimates from published literature
    - Output: economic significance discussion

3.6 Full robustness execution
    - Execute all planned robustness tests (Levels 1-5 of Robustness Pyramid)
    - Report robustness results in structured tables or coefficient plots
    - Identify any robustness check where results are fragile; discuss transparently
    - Output: robustness section with tables and figures

3.7 Mechanism analysis
    - Execute mechanism tests: mediation, moderation, heterogeneity
    - For causal mediation: implement Imai et al. (2010) or Dippel et al. (2020) approach
    - Report null results on alternative mechanisms
    - Output: mechanism evidence section

3.8 Results section drafting
    - Write results section following journal conventions
    - Tables: self-contained with clear titles, notes, variable definitions
    - Figures: publication-quality; colorblind-friendly palette; vector format
    - NO interpretation beyond stated results — save for Discussion
    - Output: §4 Results, §5 Robustness, §6 Mechanism sections
```

**Stage 3 exit criteria**: All analyses executed and verified, results tables and figures generated, all diagnostic tests passed, robustness framework complete, mechanism evidence assembled, results sections drafted.

---

### Stage 4: Writing & Assembly

**Goal**: Write the full paper from Introduction through Conclusion; assemble all sections; check cross-section consistency; format for target journal.

**Input needed from user**: All prior stage outputs, target journal selection, any institutional knowledge.

**Agent actions**:

```
4.1 Introduction drafting
    - P1: Motivating puzzle or striking fact (see Writing Pattern 1)
    - P2: Generalize to broader economic/managerial significance; set stakes
    - P3: Institutional context preview — what variation does this paper exploit? (high-level, no detailed specification)
    - P4: Identification challenge — "Identifying the causal effect of X on Y is challenging because..."
    - P5: Our approach — "We overcome this challenge by exploiting [variation] in a [DID/RDD/IV/RCT] design..."
    - P6: Preview of findings — "We find that..." (key coefficient + economic magnitude)
    - P7: Contributions (numbered, 3-5 items)
    - P8: Paper organization
    - Output: §1 Introduction draft

4.2 Institutional background / theory section
    - If quasi-experimental: detailed institutional context that motivates and validates the design
    - Why was the policy/practice adopted? Who was affected? Why might effects be heterogeneous?
    - If theory-driven: develop conceptual framework generating testable predictions
    - Use numbered predictions or hypotheses (H1, H2, H3...)
    - Diagrams: institutional timeline, conceptual framework figure
    - Output: §2 Institutional Background / Theory draft

4.3 Data & measurement section
    - Data sources described with provenance
    - Sample construction: step-by-step with numbers (attrition table)
    - Variable definitions: precise, reproducible
    - Descriptive statistics table
    - Balance / correlation analysis
    - Output: §3 Data & Measurement draft

4.4 Identification / research design section
    - Statement of the identification problem
    - Estimation equation formally presented
    - Identification assumptions: stated, defended, tested
    - Diagnostic evidence (pre-trend plots, balance at cutoff, first-stage table)
    - Why this design is credible in this setting
    - Output: §4 Identification Strategy draft

4.5 Results, robustness, mechanism sections
    - Integrate drafts from Stage 3 into polished sections
    - Ensure flow: main results → robustness confirmation → mechanism revealed
    - Output: §5-7 polished drafts

4.6 Discussion & implications
    - Connect findings back to research question and theoretical framework
    - Discuss: what did we learn that we didn't know before?
    - Theoretical contribution: how does this advance theory?
    - Practical/managerial/policy implications: what should decision-makers do differently?
    - Compare with prior literature: where does this finding sit in the literature?
    - Unexpected findings: acknowledge and interpret
    - Output: §8 Discussion & Implications draft

4.7 Conclusion
    - Summary (2-3 sentences)
    - Limitations (specific, honest)
    - Future research (concrete directions, not vague)
    - Output: §9 Conclusion draft

4.8 Abstract
    - Write LAST
    - Structure: (1) Research question, (2) Identification strategy, (3) Key finding with magnitude, (4) Mechanism, (5) Contribution/Implication
    - Word limit: varies by journal; typically 100-150 for Economics, 150-250 for Management/Marketing
    - Output: Abstract

4.9 Cross-section consistency check
    - Contribution list (Introduction) ↔ Discussion (1:1 mapping)
    - Hypotheses/predictions (Theory) ↔ Results (all tested; all reported)
    - Variables in estimating equation (Identification) ↔ Variables in Results tables
    - Robustness plan (Stage 2) ↔ Robustness section (all executed)
    - All tables/figures referenced in text in numerical order
    - All citations in text appear in References
    - Abstract claims substantiated in body
    - Terminology consistent throughout
    - Output: consistency check report with corrections

4.10 Journal formatting
    - Apply journal-specific page budget and formatting
    - References: journal-specific style
    - Tables: journal-specific format
    - Figures: resolution, format requirements
    - Online appendix: organize supplementary material
    - Output: formatted manuscript
```

**Stage 4 exit criteria**: Full manuscript drafted with all sections, cross-consistency verified, journal formatting applied.

---

### Stage 5: Polish & Pre-Submission Review

**Goal**: Polish language, verify all references, conduct a reviewer-simulation review, and prepare submission package.

**Input needed from user**: Full manuscript (from Stage 4), target journal details.

**Agent actions**:

```
5.1 Language polish
    - Run ppw:polish for overall language quality
    - Check for: jargon, passive voice overuse, sentence length, paragraph flow
    - Verify consistent tense (past for methods/results; present for theory/discussion)
    - Output: polished manuscript

5.2 Reference verification
    - Verify all citations via DOI/Crossref lookup
    - Check: no hallucinated references, correct volume/page numbers, consistent formatting
    - Verify all cited papers actually say what the text claims they say
    - Output: verified reference list

5.3 Reviewer-simulation review
    - Run ppw:reviewer-simulation
    - Identify remaining weaknesses before real submission
    - Strengthen any sections flagged as weak
    - Output: pre-submission review report + revisions

5.4 Submission package preparation
    - Cover letter: tailored to journal, highlights contribution, suggests reviewers
    - Title page: with acknowledgments, funding, conflicts of interest
    - Blinded manuscript: remove all identifying information
    - Supporting information: online appendix, replication package (if required)
    - Response to pre-submission review (if applicable)
    - Output: submission-ready package

5.5 Final checklist
    - Run the Quick Checklist Before Submission (below)
    - Address any remaining items
    - Output: final submission package
```

**Stage 5 exit criteria**: Polished manuscript, verified references, pre-submission review completed, submission package ready.

---

### Pipeline Interaction Protocol

When the user invokes this skill, the agent should:

1. **Determine the current stage**: Ask what the user has so far (idea only? identification designed? data in hand? results available? draft written?)
2. **Start at the appropriate stage**: Don't force users back to Stage 1 if they've already designed their identification
3. **At each stage**: Execute agent actions in order; load relevant reference files as needed
4. **Stage gate**: Confirm with user before proceeding to the next stage
5. **Iterate within stage**: Draft → get feedback → revise until stage exit criteria are met

### Quick-Start Prompts

Users can jump to any stage:

- "I have a phenomenon I want to study. Help me design the identification strategy and pick an FT50 journal." → Stage 1-2
- "I have my data and identification design. Help me run the analysis and robustness checks." → Stage 3
- "I have all my results. Help me write the full paper for [Journal]." → Stage 4
- "I have a full draft. Help me polish it and prepare for submission to [Journal]." → Stage 5
- "My paper was rejected from [Journal]. Help me revise for resubmission to [Alternative Journal]." → Stage 1 (re-position) → Stage 4-5
- "Take me through the full pipeline from scratch." → Stage 1 → 5

---

## Writing Patterns

### Pattern 1: The Motivating Puzzle

Open the introduction with a striking empirical fact, paradox, or puzzle that the paper resolves. The motivating puzzle establishes that the research question is non-obvious and important.

**Template**:
> Despite [conventional wisdom / prior literature suggesting X], we observe that [puzzling empirical fact Y]. This pattern is surprising because [reason Z]. Understanding why [Y occurs] has important implications for [theory, practice, policy].

**Discipline variants**:
- Economics: "A vast literature documents [stylized fact]. Yet causal evidence on its determinants remains scarce..."
- Finance: "Theory predicts that X should lead to Y. However, empirical evidence has been mixed, likely due to..."
- Management: "Although [management practice] is widely adopted, evidence on whether it actually improves performance is limited because..."
- Accounting: "Regulators and standard-setters have long debated whether [accounting policy] affects [outcome]. We provide the first causal evidence on this question by..."
- Marketing: "Firms spend $X billion annually on [marketing activity], yet whether this spending causally affects consumer behavior remains an open question..."

### Pattern 2: The Institutional Detail Paragraph

For quasi-experimental papers, institutional detail transforms a statistical exercise into a credible causal design.

**Template**:
> [Policy/Regulation/Practice] was introduced in [year] by [institution]. Its stated purpose was [goal]. Crucially for our identification strategy, [policy] applied to [treated units] but not to [control units] because [institutional rule]. Moreover, the timing of [policy] was determined by [process], which is plausibly exogenous to [outcome] because [reasoning]. This institutional feature allows us to estimate the causal effect of [treatment] by comparing [treated] to [control] before and after [policy], in a difference-in-differences framework.

### Pattern 3: The Coefficient of Interest Paragraph

The key coefficient must be highlighted and interpreted for economic magnitude — not just statistical significance.

**Template**:
> The coefficient of interest is [β̂] on [variable] in [equation/column]. The estimate is [β̂ = value] (SE = [value]; [p-value or CI]). The magnitude is economically significant: [back-of-envelope interpretation]. To put this in context, [benchmark]. The estimate implies that [practical interpretation of the number in substantive terms]. This [supports / fails to support] our prediction that [theoretical expectation].

### Pattern 4: The Robustness Pyramid Narrative

The robustness section should read as a systematic dismantling of potential concerns, organized from most specific to most general:

**Template**:
> We conduct a series of robustness tests to address potential threats to our identification. **First**, we verify that our results are not driven by [measurement]: using alternative measures of [DV/IV], the estimated effect remains [similar/direction]. **Second**, we examine sample composition: [restricted/balanced/trimmed] samples yield [consistent/similar] results. **Third**, we test the sensitivity of our specification: [alternative FEs / functional forms / estimators] produce [similar estimates]. **Fourth**, we conduct falsification tests: [in-time placebo / in-space placebo / alternative outcome that should not be affected] yields [null result], supporting the validity of our design. **Finally**, we assess sensitivity to unobserved confounding: [Oster δ / Rosenbaum Γ / Imbens bounds] suggest that [interpretation]. Collectively, these tests reinforce our main finding: [restate key result concisely].

### Pattern 5: The Mechanism Cascade

When presenting mechanism evidence, structure the narrative as a cascade from the most theoretically grounded mechanism to supplementary or alternative mechanism tests:

**Template**:
> Having established that [treatment] causally affects [outcome], we next examine **why** this effect occurs. **Theory suggests [mechanism 1]**: if [treatment] operates through [channel], we should observe [mediating variable] responding to [treatment] and in turn affecting [outcome]. [Present mediation results]. **We also examine [mechanism 2]** using a moderation approach: if [theory] is correct, the effect of [treatment] on [outcome] should be stronger for [subgroup] because [theoretical reasoning]. [Present moderation results]. **To rule out alternative mechanisms**, we test whether [treatment] affects [alternative mediating variable], which would be consistent with [alternative theory]. We find no evidence for this alternative channel, suggesting that [mechanism 1] is the primary driver. **Taken together**, the mechanism evidence suggests that [treatment] affects [outcome] primarily through [primary channel], with [secondary channel] playing a [role].

### Pattern 6: The Honest Limitations Paragraph

FT50 reviewers reward honest, specific limitations, not boilerplate.

**Template**:
> Several limitations of our study should be acknowledged. **First**, our identification strategy relies on [key assumption]. While we provide [evidence/test] supporting this assumption, we cannot fully rule out [residual concern]. Future work using [alternative design] in [different context] would strengthen confidence in the causal interpretation. **Second**, our sample is limited to [context/population], which may affect generalizability. [Discussion of whether the direction of bias is predictable; whether the sign or only the magnitude would change in other contexts.] **Third**, while our mechanism evidence points to [mechanism], we cannot definitively rule out [alternative mechanism] without [data/design feature]. Despite these limitations, we believe our paper provides the most credible evidence to date on [research question].

---

## Quick Checklist Before Submission

### Identification Credibility

- [ ] Identification strategy clearly stated in the introduction and detailed in a dedicated section
- [ ] All identification assumptions explicitly stated and defended with institutional arguments
- [ ] Diagnostic tests conducted and passed: pre-trends (DID), density test (RDD), first-stage F > 10 (IV), balance table (RCT, Matching)
- [ ] Standard errors clustered at the level of treatment assignment; justification provided
- [ ] Identification is discussed honestly: what can be identified (LATE, ATT, ATE) and what cannot
- [ ] For staggered DID: at least one modern estimator (Sun-Abraham, Callaway-Sant'Anna, BJS, Gardner) used alongside TWFE

### Robustness

- [ ] Alternative dependent variables tested
- [ ] Alternative independent variable / treatment definitions tested
- [ ] Alternative sample (restricted, balanced, trimmed) tested
- [ ] Alternative specification (FE structure, functional form, estimator) tested
- [ ] Placebo/falsification tests conducted (in-time, in-space, alternative outcome)
- [ ] Sensitivity to unobservables quantified (Oster ð or equivalent)

### Mechanism

- [ ] At least one mechanism channel tested and supported
- [ ] Mediation tested with bootstrapped CIs (if quantitative); moderators tested with interaction terms
- [ ] Alternative mechanisms tested and ruled out (or acknowledged as unresolved)
- [ ] Mechanism evidence connected back to theoretical framework

### Writing & Structure

- [ ] Abstract: question, identification, key estimate with magnitude, mechanism, contribution (within word limit)
- [ ] Introduction: motivating puzzle, institutional preview, identification challenge, findings preview, numbered contributions
- [ ] Institutional background: sufficient detail to justify the identification strategy
- [ ] Identification section: estimation equation, assumptions (stated and defended), diagnostic evidence, credibility argument
- [ ] Results: coefficient of interest interpreted for economic significance alongside statistical significance
- [ ] Robustness: organized pyramid, systematic, not ad-hoc
- [ ] Discussion: theoretical contribution explicit, practical implications grounded in results
- [ ] Conclusion: limitations are specific, future research directions are concrete

### Mechanics

- [ ] All tables self-contained with clear notes and variable definitions
- [ ] All figures publication-quality with clear labels
- [ ] All references verified via DOI lookup (no hallucinated references)
- [ ] Page/word budget within journal limits
- [ ] Journal formatting applied correctly
- [ ] Blinded manuscript prepared (if journal requires double-blind review)
- [ ] Cover letter drafted and tailored to target journal
- [ ] Replication package prepared (data, code, README) if journal requires
- [ ] Pre-analysis plan referenced if RCT or pre-registered design

---

## Cross-Referencing with Other Skills

This skill works with:

- **scientific-writing**: General academic writing principles, IMRAD structure, clarity and conciseness
- **literature-review**: Systematic literature search and synthesis for empirical research topics
- **paper-lookup**: Finding and verifying citations from academic databases
- **research-lookup**: Broader research context and related literature
- **ppw:polish**: English language polishing for non-native speakers
- **ppw:reviewer-simulation**: Simulate peer review before submission to identify weaknesses
- **ppw:abstract**: Generate or optimize abstracts using the Farquhar formula
- **scientific-visualization**: Publication-quality figures (event-study plots, coefficient plots, RD plots, maps)
- **statistical-analysis**: Guided statistical test selection for mechanism and heterogeneity analysis
- **statsmodels** / **scikit-learn**: Implementing statistical models and machine learning methods

---

## References

- [references/ft50-journals.md](references/ft50-journals.md): Complete FT50 journal list with per-journal profiles, editorial preferences, methodology expectations, rejection rates, turnaround times, and published editorial statements
- [references/identification-strategies.md](references/identification-strategies.md): Detailed guidance for each identification strategy — specification templates, diagnostic checklist, Stata/R/Python code examples, common pitfalls, and published examples from FT50 journals
- [references/robustness-framework.md](references/robustness-framework.md): Comprehensive robustness framework — the Robustness Pyramid (5 levels), test-specific guidance, reporting standards, and journal-specific robustness expectations
- [references/writing-patterns.md](references/writing-patterns.md): Reusable writing patterns from published FT50 papers — motivating puzzles, institutional detail paragraphs, coefficient interpretation, robustness narrative, mechanism cascade, and honest limitations
- [references/reviewer-expectations.md](references/reviewer-expectations.md): What reviewers look for in FT50 empirical papers — by discipline, by section, by identification strategy; common reviewer comments and effective rebuttal strategies; revise-and-resubmit response templates

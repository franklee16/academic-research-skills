# 05 — Finance Calibration: How Identification Norms Diverge from MHE's Labor-Micro Context

> **Attribution note.** This file was authored by Claude from domain knowledge of empirical finance practice. The research subagent was killed by an API rate limit; specific quotes should be verified against the cited sources.

---

## 1. Asset pricing has its own identification culture (parallel to MHE, not derived from it)

The MHE playbook — IV, RD, DiD, CIA — was developed in labor and development economics. Asset pricing developed an *independent* identification culture that MHE does not address:

- **Portfolio sorts.** Sort stocks by some characteristic (size, value, momentum, ESG score); compute the spread in returns. The identification claim: the spread is compensation for risk, not a data-mining artifact.
- **Fama-MacBeth regressions.** Cross-sectional regressions of returns on characteristics; the slope is the risk-price. Standard errors adjusted for the cross-sectional correlation induced by shared factor exposure.
- **Factor-model decomposition.** Time-series regression of portfolio returns on factor-mimicking portfolios (Mkt-RF, SMB, HML, RMW, CMA, MOM, etc.); the alpha is the unexplained return, identified as the pricing error.
- **Anomaly zoo.** Hundreds of published predictors. Identification claim: out-of-sample, after multiple-testing correction, after transaction costs, the predictor survives.

**MHE has nothing to say about any of this.** The skill must acknowledge: asset pricing's identification tradition is parallel, not derivative. A pure-MHE lens would reject most anomaly papers ("no source of exogenous variation"); the field has its own defenses (out-of-sample, multiple-testing, transaction costs, economic-magnitude thresholds).

**Key references.**
- Fama & French (1993, 2015); Carhart (1997).
- Harvey, Liu & Zhu (2016), "...and the Cross-Section of Expected Returns," *RFS* — the multiple-testing critique.
- Chen & Zimmermann (2021, 2024) — the anomaly zoo and false-discovery rates.
- Yan & Zheng (2017) — fundamentals-based anomaly selection.

---

## 2. Corporate finance identification (where MHE applies most directly)

**Where the MHE playbook is genuinely useful.**
- Governance: Gompers-Ishii-Metrick (2003) G-index; Bertrand-Mullainathan (2003) on tunneling.
- IV applications: Baker-Wurgler sentiment index as IV for capital structure; Francis-Park for peer effects; a large literature uses plausibly exogenous shocks.
- DiD applications: SOX (2002), Reg FD (2000), exchange deregulation, regulatory changes around accounting standards.
- RD applications: bond rating cutoffs (Baghai-Servaes 2012, the threshold for investment-grade as RD); Dodd-Frank thresholds; margin requirements; class-size cutoffs in labor settings; law changes around 401(k) auto-enrollment.

**Key references.**
- Bertrand & Mullainathan (2003), "Enjoying the Quiet Life? Corporate Governance and Managerial Preferences," *JPE* — DiD on state-level antitakeover laws.
- Baghai-Servaes (2012, JF) — bond-rating RD.
- Baker-Wurgler (2007) sentiment — IV application.
- Gompers-Ishii-Metrick (2003) G-index.

**What JF/RFS referees want.** Source of exogenous variation named explicitly; parallel-trends plot shown; first-stage F reported; complier population discussed; clustering justified (firm + year double-clustering is the default in firm-year panels); placebo/robustness tests run.

---

## 3. ESG-specific endogeneity (the user's area)

ESG is the user's area. Identification is hard because the "treatment" — being a high-ESG firm — is endogenous to firm quality.

**Three core endogeneity threats.**
1. **Selection.** High-quality firms afford ESG; ESG doesn't cause quality. Or: profitable firms attract ESG investor demand; ESG doesn't cause profitability.
2. **Measurement error.** ESG ratings disagree across providers (Berg, Kölbel & Rigobon 2022, *RFS*, "Aggregate Confusion"). The "ESG" variable is partly noise.
3. **Reverse causality.** ESG screens and exclusions are endogenous to past performance.

**Common identification moves.**
- **ESG incidents as shocks.** A scandal or activist event generates plausibly exogenous variation in ESG scores. Examples: Refinitiv/MSCI downgrades; media-driven ESG controversies (e.g., BP Deepwater Horizon, Volkswagen Dieselgate).
- **Regulatory mandates as shocks.** EU SFDR (2019/2020); EU Taxonomy; national carbon taxes; mandatory ESG disclosure. DiD around regulatory events.
- **Index exclusions.** Norges Bank exclusion list (Norway sovereign wealth fund); exclusion announcements as quasi-shocks.
- **Natural experiments.** Russell 1000/2000 index reconstitution (Appel, Gormley & Keim 2018) as the canonical RD; fund-flow shocks around ESG index inclusions.

**Key references.**
- Berg, Kölbel & Rigobon (2022), "Aggregate Confusion," *RFS* — the ESG-ratings-disagreement paper.
- Pedersen, Fitzgibbons & Pomorski (2021) — "Responsible Investing: The ESG-Efficient Frontier."
- Friede, Busch & Bassen (2015), *Journal of Sustainable Finance & Investment* — the meta-analysis.
- Hong & Kacperczyk (2009), "The Price of Sin: Effects of Norm Violations on Stock Returns," *RFS* — the sin-stock/sin-ETF exclusion paper.
- Appel, Gormley & Keim (2018) — Russell 1000/2000 RD.

**What ESG referees expect.**
- A named source of exogenous variation, not just "high-ESG firms outperform."
- Robustness to ratings disagreement (report results across MSCI, Refinitiv, Sustainalytics).
- Reverse-causality check (lag structure; instrumental variable; placebo periods).
- Mechanism (channel): through what does ESG affect returns? Cost of capital? Cash flows? Investor demand?

**The MHE lens applied.** MHE's selection-problem language fits ESG perfectly: "the ESG paper compares high- and low-ESG firms; high-ESG firms are systematically different — larger, more regulated, less levered. The selection bias on the untreated outcome is large and probably not killed by controls." The skill should reach for this vocabulary.

---

## 4. Behavioral finance identification

The user's other area. Behavioral claims — sentiment causes mispricing; arbitrage is limited; investors overreact — must be identified when psychology is not directly observable.

**Common identification moves.**
- Investor sentiment as IV (Baker-Wurgler 2007); sentiment indices constructed from market-wide proxies.
- Shocks to investor attention: weather, daylight, sports outcomes (Hirshleifer & Shumway 2003); media coverage (Tetlock 2007).
- Limits-to-arbitrage tests: Shleifer-Vishny (1997); Pontiff (1996, 2006) on the limits of arbitrage; short-interest as a proxy.
- Natural experiments: market closures (Hong & Yu 2009); trading hours; index additions.

**The MHE lens.** Sentiment is not an instrument in the IV sense — it is itself endogenous to fundamentals. The identification move is to argue that sentiment has components orthogonal to fundamentals (the Baker-Wurgler decomposition). The skill should know this is a contested move.

---

## 5. The high-D FE + double-clustering finance convention

Finance panels are long — decades of stock-month or firm-year data. Standard practice: firm + year FE, double-clustered SEs by firm and time.

**MHE (Ch 8) is skeptical of clustering as a fix-all.** This skepticism is partly right and partly wrong in finance.

**Where the convention is legitimate.**
- Firm FE: removes time-invariant firm characteristics (a partial control for unobserved heterogeneity).
- Year FE: removes common time shocks (macroeconomic conditions).
- Double-clustered SEs: correct standard errors when errors are correlated within firm and within time.

**Where the convention is not legitimate.**
- **Treatment at the firm level.** If treatment varies within firm (firm-by-year ESG score, firm-by-year governance index), then firm-level clustering is wrong — the cluster is firm-year, not firm. The skill should flag this.
- **Treatment at the year level.** If treatment is a year-specific regulatory shock (SOX 2002, Reg FD 2000), then firm-level clustering *over*-states precision because it ignores the year-level correlation induced by the shock. The skill should flag this.
- **Few clusters.** Few industries, few regulators, few states — finance panels can be long but narrow. Few-cluster inference is required.
- **Identified-but-just-a-fixed-effect.** A "firm FE" absorbs a lot of variation, including the treatment, if treatment is slow-moving. A 30-year panel with firm FE and a slow-moving ESG score has the treatment absorbed.

**Key references.**
- Petersen (2009), "Estimating Standard Errors in Finance Panel Data Sets," *Journal of Financial Economics*.
- Thompson (2011), "Simple Formulas for Standard Errors that Cluster by Both Firm and Time," *Journal of Financial Economics*.
- Cameron, Gelbach & Miller (2011), "Robust Inference with Multiway Clustering," *Journal of Business & Economic Statistics*.
- Abadie, Athey, Imbens & Wooldridge (2023), "When Should You Adjust Standard Errors for Clustering?," *QJE* — the modern update.

**The MHE parallel.** MHE's "bad control" applies: if the year FE is correlated with the treatment (e.g., a year-specific regulatory shock), then year FE is not a control but a collinear variable. The skill should reach for this analogy.

---

## 6. How JF/RFS referees differ from QJE/AER referees

A generalization, with exceptions:

| Dimension | QJE/AER referees | JF/RFS/JFE referees |
|---|---|---|
| Identification purity | High — sources of exogenous variation expected | High in corporate finance; looser in asset pricing |
| Economic magnitude | Required but not central | Often central — a 1bp effect is hard to publish even if precisely identified |
| External validity | Often discussed | Often discussed |
| Mechanism | Required when the question is mechanism-uncertain | Required |
| Robustness tables | Extensive | Even more extensive — the "Table 7A of 7B" norm |
| Out-of-sample | Optional | Often required (especially in asset pricing) |
| Multiple-testing correction | Increasingly expected | Always expected in asset pricing |
| Pre-registration | Rare in econ | Rare in finance |
| Data access | Required (AEA data policy) | Required |

**Implication for the skill.** When the skill is reviewing a finance paper, it should weight economic magnitude, multiple-testing correction, and out-of-sample tests more heavily than a pure-MHE lens would. When the paper is asset-pricing, the skill should *not* demand an IV where the field's tradition (sorts + Fama-MacBeth) is the identification move.

---

## 7. Natural experiments common in finance

Finance papers often use plausibly exogenous variation around:

- **Regulatory shocks.** Reg FD (2000), SOX (2002), MiFID II (2018), the 2003 mutual fund trading scandal, decimalization (2001), Reg SHO (2005), Dodd-Frank (2010), Basel III implementation dates.
- **Index events.** Russell 1000/2000 reconstitution (Appel, Gormley & Keim 2018 RD); S&P 500 additions; MSCI EM index inclusions.
- **Credit-rating events.** Baghai-Servaes (2012) investment-grade threshold RD; Moody's/S&P downgrades.
- **Earnings events.** Earnings surprises (analyst forecast error); restatements; 8-K disclosures.
- **Analyst-coverage events.** Analyst drop after M&A (Hong & Kacperczyk); initiation vs. discontinuation.
- **Index-expulsion events.** Norges Bank sovereign wealth fund exclusions; sin-stock ETFs.
- **M&A as shocks.** Bertrand & Mullainathan (2003) antitakeover laws; Agrawal & Tambe (2019) on data and M&A.

**Referee scrutiny in 2026.** Each of these has been criticized in the modern identification literature. E.g., the Russell 1000/2000 RD has been re-examined (Chang, Hong & Tiedmann 2015, *JFE*); natural experiments around regulatory events must address anticipation and confounders.

---

## 8. Synthetic control / staggered-DiD adoption in finance

Slower than in econ. Reasons:
- Asset pricing is dominated by panel methods (sorts, regressions); SC is one-country/state, unusual in finance.
- Corporate finance is catching up on staggered-DiD (Roth-Sant'Anna 2023 synthesis has explicit finance applications).
- The 2018+ methods are entering finance journals by 2022-2025.

**Implication.** A finance paper using TWFE on staggered data in 2026 is increasingly criticized; the skill should know this is now the standard referee complaint.

---

## 9. When MHE skepticism is right vs overzealous in finance

**Right (apply MHE skepticism).**
- ESG: endogeneity is severe; pure correlational claims ("high-ESG firms outperform") should be rejected.
- Sentiment: endogeneity to fundamentals; the identification move must be defended.
- Bond-rating cutoffs: density test (McCrary) must be reported.
- Bartik IV: GP-Sorkin-Swift / BH-Jaravel must be addressed.
- Staggered DiD: must use modern estimators.

**Overzealous (don't apply MHE skepticism).**
- Asset pricing anomaly papers: the identification tradition is sort + Fama-MacBeth + out-of-sample, not IV.
- Portfolio sorts on slow-moving characteristics: the "treatment" is the characteristic itself; the identification move is the out-of-sample and multiple-testing defense.
- Pure correlations with extensive robustness checks: often the best available in finance; do not reject because no IV is available.
- High-D FE panels with double-clustered SEs: legitimate when treatment is at the firm-year level and clustering matches.

**Calibration rule.** The skill should ask: "What is the field's identification culture for this question, and does this paper meet it?" If yes, accept; if no, critique.

---

## 10. What the skill does with this calibration

The skill's Drafter mode, when drafting an ESG or asset-pricing identification section, must:

1. Name the source of variation using the field's vocabulary (incident, regulatory shock, index event) — not just "an instrument."
2. Address reverse causality explicitly. Don't assume the reader will fill it in.
3. Discuss ratings disagreement if relevant.
4. Justify clustering. "We cluster at the firm level because the treatment varies at the firm-year level" — or use the modern clustering literature.
5. Match the field's identification expectation. ESG papers are scrutinized harder than anomaly papers; corporate-finance DiD is scrutinized like econ DiD.

The Critic mode must:

1. Not impose MHE purity where the field has a legitimate alternative tradition.
2. But insist on modern identification when the field expects it (staggered DiD, Bartik IV, ESG endogeneity).
3. Flag high-D FE panels when the treatment may be absorbed or the clustering may be wrong.
4. Push back on marginal results, especially in anomaly or ESG papers where specification mining is plausible.

---

## Sources

This file was authored by Claude from domain knowledge after the research subagent was killed by API quota. Key references (verify against originals):
- Fama-French (1993, 2015); Carhart (1997); Harvey-Liu-Zhu (2016) RFS; Chen-Zimmermann (2021, 2024).
- Gompers-Ishii-Metrick (2003) QJE; Bertrand-Mullainathan (2003) JPE; Baghai-Servaes (2012) JF; Baker-Wurgler (2007) JF.
- Berg-Kölbel-Rigobon (2022) RFS; Pedersen-Fitzgibbons-Pomorski (2021); Friede-Busch-Bassen (2015); Hong-Kacperczyk (2009) RFS; Appel-Gormley-Keim (2018).
- Hirshleifer-Shumway (2003); Tetlock (2007); Shleifer-Vishny (1997); Pontiff (1996, 2006); Hong-Yu (2009).
- Petersen (2009) JFE; Thompson (2011) JFE; Cameron-Gelbach-Miller (2011) JBES; Abadie-Athey-Imbens-Wooldridge (2023) QJE.

To be cross-checked by anyone running the research swarm fresh.
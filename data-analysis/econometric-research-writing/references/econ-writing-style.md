# Economics And Management Writing Style

Use this reference when drafting, restructuring, or polishing economics, finance, management, or applied econometrics prose.

## Style Principles

- Lead with the research question and empirical claim.
- Use precise, bounded causal language.
- Prefer short paragraphs with one job: motivation, design, result, interpretation, or limitation.
- Distinguish evidence from interpretation.
- Report economic magnitudes, not only significance.
- Use active voice for author choices and passive/objective phrasing for estimates.
- Avoid course-answer phrasing such as "I would choose", "better model", or "this proves".

## Section Templates

### Abstract

Use four moves:

1. Research question and setting.
2. Data and method.
3. Main empirical finding with magnitude.
4. Interpretation and limitation.

Avoid literature-review detail and excessive equations.

### Introduction

Use this order:

1. Motivation and economic stakes.
2. Gap or unresolved empirical problem.
3. Research design in one paragraph.
4. Main findings with magnitudes.
5. Contribution and roadmap.

### Data

Include:

- Data source and sample period.
- Unit of observation.
- Outcome, treatment/main regressor, controls.
- Transformations: logs, lags, differences, standardization.
- Sample restrictions and missing-data handling.

### Empirical Strategy

Include:

- Baseline equation.
- Definition of all indices and variables.
- Estimator.
- Identifying or interpretation assumptions.
- Standard errors and fixed effects.
- Threats the design addresses and does not address.

### Results

Write from table to interpretation:

1. "Column (1) reports..."
2. "The coefficient implies..."
3. "Adding controls/fixed effects changes..."
4. "This pattern is consistent with..."
5. "However, this estimate should be interpreted as..."

Every table or figure callout should tell the reader what to look for. Avoid empty callouts such as "see Table 2" without an empirical takeaway.

### Robustness

Do not list checks mechanically. Group them by threat:

- Measurement.
- Sample composition.
- Functional form.
- Timing/dynamics.
- Inference.
- Identification.

### Conclusion

Summarize what the analysis shows, what remains uncertain, and what future data/design would improve.

## Literature And Citation Style

- Default to author-year citations for economics, finance, and management drafts unless the target style requires numeric citations.
- Cite only verified sources. If a paper cannot be verified or does not support the claim, do not cite it as support.
- Use citations to support claims about prior findings, methods, data definitions, institutional facts, and external estimates.
- Do not use citations to mask weak reasoning; the prose should still explain why the cited literature matters for this design.
- When adding literature, organize by argument: substantive setting, identification precedent, measurement/data precedent, and method precedent.
- Keep a claim-to-source ledger for citation-heavy revisions.

## Preferred Wording

Use:

- `The estimates suggest...`
- `The coefficient is consistent with...`
- `Under the maintained assumptions...`
- `The result is robust to...`
- `The evidence points to...`
- `This pattern should be interpreted as an association unless...`

Avoid:

- `This proves...`
- `The model solves endogeneity...`
- `The variable causes...`
- `The best model is...`
- `Obviously...`
- `It is clear that...`

## Method-Specific Language

- FE: "controls for time-invariant unit heterogeneity."
- DiD: "under parallel trends and no differential shocks."
- IV: "local effect for compliers under relevance and exclusion restrictions."
- Granger: "predictive content for future values."
- VAR: "dynamic association among endogenous variables."
- Cointegration: "stable long-run relation."
- Nonparametric/time-varying: "flexible/evolving association."

## Polishing Checklist

- Remove first person unless the venue allows it.
- Replace subjective adjectives with diagnostics.
- Replace "significant" alone with sign, magnitude, and uncertainty.
- Check that every causal verb has a design justification.
- Check consistency of terminology across tables, figures, and prose.
- Keep equations close to the text that explains them.
- Check that every citation-backed sentence has a real, verified source and that every reference-list entry is cited.

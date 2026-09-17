---
name: neishengxing
description: Use when designing, diagnosing, coding, running, or writing an endogeneity section for empirical economics papers, including IV/2SLS/IV-Tobit, leave-one-out peer instruments, weak-IV tests, Oster (2019), Heckman selection, WIT many-IV screening, TSCI/STCI invalid-IV methods, LIML/Fuller fallbacks, and manuscript-ready Chinese or English reporting.
---

# 经济学内生性 Skill

## Core Rule

Treat endogeneity handling as a diagnostic workflow, not a decoration. First identify the threat and data structure, then choose methods that are conceptually applicable, estimable in the user's software, and reportable without overclaiming.

Never claim a method solves endogeneity merely because the coefficient is significant. Always report suitability, identifying assumptions, diagnostics, and residual reviewer risk.

## Intake Checklist

Before coding or writing, collect or infer:

- Outcome type: continuous, binary, count, censored/share in `[0,1]`, panel, survival, or selection-only observed.
- Baseline estimator: OLS for linear continuous outcomes; Tobit or fractional/bounded alternatives for censored shares; logit/probit for binary outcomes; fixed effects or panel models when panel variation exists.
- Suspected threat: omitted variables, reverse causality, self-selection/sample selection, simultaneity, measurement error, weak instruments, invalid instruments.
- Treatment/endogenous variable: binary, continuous, ordered, generated index, or multiple endogenous regressors.
- Data level: individual/household, village/community, county/city, firm, panel, repeated cross-section.
- Available instruments: external historical/geographic/institutional variables, peer leave-one-out instruments, high-dimensional candidate IVs, policy shocks, or no credible IV.
- Software: Stata, R, Python, or mixed workflow; whether packages may be installed.
- Manuscript target: main identification section, robustness subsection, appendix, or reviewer response.

If key information is missing but work can proceed, make a conservative assumption and flag it in the output.

## Method Selection

Use this order unless the user requests a specific method:

1. **Baseline alignment**: ensure the baseline estimator matches the outcome. For shares bounded in `[0,1]`, use Tobit or a bounded-outcome model for direct regressions; keep OLS as a comparability or diagnostic model if needed.
2. **Main IV path**: if credible instruments exist, estimate first stage and second stage. For censored outcomes, consider IV-Tobit or control-function Tobit in addition to 2SLS.
3. **Leave-one-out peer IV**: if no external IV exists and peer environment is defensible, construct same-group excluding-self means for the endogenous variable or digital subindices. Treat this as a reviewer-risk instrument requiring strong exclusion-argument writing.
4. **Weak-IV and overidentification diagnostics**: report first-stage F, KP rk Wald F, Anderson-Rubin, Stock-Wright/CLR when available, underidentification, weak-ID, endogeneity, and Hansen/Sargan overidentification when overidentified.
5. **Oster (2019)**: use coefficient stability to address omitted-variable concerns in OLS-style models. Do not present it as a Tobit replacement.
6. **Heckman**: use only when the outcome is observed for a selected subsample and selection into observation is substantively meaningful. Do not use Heckman merely because the dependent variable has many zeros.
7. **WIT / many-IV screening**: use when there is a genuinely large or mechanically generated candidate IV pool and the method's assumptions are defensible. Treat WIT as candidate-IV screening or many-IV robust identification support, then report the selected/effective IV pool and post-selection estimates/diagnostics.
8. **TSCI / STCI invalid-IV methods**: use only after reading the method reference and checking whether the data satisfy the method's curvature/nonlinearity, invalid-IV structure, and candidate-IV requirements. Do not call it a simple instrument-combination method.
9. **Fallbacks**: use LIML / Fuller-LIML as weak-IV robustness for linear IV settings. They supplement but do not repair an implausible exclusion restriction.

For method details, read `references/method_cards.md`. For paper-facing wording and table checklists, read `references/reporting_templates.md`. If the user needs citations, DOI, literature grounding, or a referee-facing method explanation, read `references/literature.md`.

## Leave-One-Out Peer IV Pattern

Use when the user lacks external IVs but has clustered peer data:

- Define group: village, community, county, city, school, industry, or market.
- For each unit, compute the group mean of the endogenous variable excluding itself.
- Candidate variants: leave-one-out mean of the binary treatment, continuous index, subindices, lagged peer exposure, or peer access/use/finance components.
- Exclusion argument: peer digital environment affects the individual's digital participation through local learning, infrastructure, norms, and service exposure; it should not directly affect the outcome after controlling for own covariates and fixed effects.
- Risk statement: peer IV may violate exclusion through common shocks, reflection, spillovers, or sorting. Always add group controls/fixed effects where feasible and avoid overclaiming.

When coding from tabular data, adapt `scripts/build_leave_one_out_iv.py`.

## Output Contract

For empirical work, deliver:

- A diagnosis paragraph: endogeneity threats and why each selected method fits or does not fit.
- A runnable command file or code block with Chinese comments if the user works in Chinese.
- A results map: main tables, appendix tables, logs, and file paths.
- A reporting checklist: coefficients, standard errors, stars, N, controls, fixed effects, first-stage diagnostics, weak-IV diagnostics, overidentification tests, method-specific assumptions.
- A manuscript paragraph: conservative, journal-style interpretation with no hidden workflow notes.
- A stop/go recommendation: what can enter main text, what belongs in appendix, what should be dropped.

## Red Lines

- Do not hide insignificant, weak, or failed diagnostics in the reasoning. If the user asks not to report a failed result, separate “do not report” from “method not supported.”
- Do not call a weak-IV result “solved identification.”
- Do not use Heckman for true zero outcomes unless there is a separate sample-observation selection process.
- Do not use WIT/TSCI simply because the method sounds advanced; first pass the applicability gate.
- Do not invent external instruments. Ask the user to provide literature or data, or limit work to constructible peer/group instruments.

## Version

Current version: 1.0.0.

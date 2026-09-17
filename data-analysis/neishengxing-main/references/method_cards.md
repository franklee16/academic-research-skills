# Method Cards for Economics Endogeneity Workflows

## 1. Instrumental Variables

Use when an instrument affects the endogenous regressor but affects the outcome only through that regressor.

Core references to cite when needed: Sargan (1958), Hansen (1982), Bound et al. (1995), Staiger and Stock (1997), Stock and Wright (2000), Kleibergen and Paap (2006). See `literature.md`.

Core outputs:

- First-stage coefficient(s) on excluded instruments.
- First-stage F or partial F; robust settings should report Kleibergen-Paap rk Wald F when available.
- Underidentification test if available.
- Weak-IV robust tests such as Anderson-Rubin, Stock-Wright, CLR, or weakiv output when available.
- Second-stage coefficient and standard error.
- Endogeneity test such as Durbin-Wu-Hausman when available.
- Overidentification test such as Hansen J or Sargan when there are more excluded instruments than endogenous regressors.

Model choices:

- OLS baseline with continuous outcome: 2SLS.
- Censored/share outcome: Tobit follows Tobin (1958). IV-Tobit or control-function Tobit can be more aligned with Tobit baseline; also report linear 2SLS as a diagnostic if useful.
- Multiple instruments for one endogenous regressor: standard overidentified IV setting; report overidentification.

## 2. Leave-One-Out Peer Instruments

Use as a constructible fallback when external instruments are unavailable and group peer exposure is defensible.

This is a practical peer-environment construction, not a universally valid off-the-shelf IV. Ask the user to support the exclusion restriction with setting-specific literature whenever the instrument is central to identification.

Formula for group `g` and unit `i`:

`loo_x_i = (sum_{j in g} x_j - x_i) / (n_g - 1)`

Good candidates:

- Same-village excluding-self mean of treatment.
- Same-village excluding-self mean of continuous digital index.
- Same-village excluding-self means of subindices such as access, usage, finance, production, supply-marketing.

Minimum diagnostics:

- First-stage sign and significance.
- First-stage F / KP rk Wald F.
- Weak-IV robust p-values if available.
- Sensitivity to group controls or fixed effects where feasible.
- No overidentification test if exactly identified with one instrument.

Risks to state:

- Common village shocks may directly affect the outcome.
- Peer behavior may reflect local sorting or shared preferences.
- Spillovers from peer treatment to own outcome can violate exclusion.

## 3. Oster (2019)

Use for omitted-variable robustness based on coefficient stability. It is most natural for OLS-style linear models.

Core reference: Oster (2019). See `literature.md`.

Required inputs:

- Short regression coefficient and R-squared: `beta_short`, `R_short`.
- Controlled regression coefficient and R-squared: `beta_full`, `R_full`.
- Assumed maximum R-squared `Rmax`, commonly `1.3 * R_full` or an alternative justified value.
- Selection ratio `delta`, commonly benchmarked at `delta = 1`.

Report:

- `beta_short`, `R_short`, `beta_full`, `R_full`, `Rmax`, `delta`.
- Bias-adjusted coefficient or identified set.
- Whether the identified set excludes zero.

Do not present Oster as replacing IV or Tobit. Use it as omitted-variable sensitivity evidence.

## 4. Heckman Selection

Use only when the outcome is observed only for a selected subsample and the observation process is economically meaningful.

Core reference: Heckman (1979). See `literature.md`.

Appropriate examples:

- Wage observed only for employed individuals.
- Export value observed only for exporters.
- Credit amount observed only for applicants or approved borrowers.

Not appropriate by itself:

- Outcome equals true zero for some units.
- Missing values were recoded to zero without being able to distinguish missingness from true zero.
- The researcher merely wants another robustness test without a credible selection equation.

Report:

- Selection equation variables and exclusion restriction.
- Outcome equation coefficient.
- Inverse Mills ratio / lambda and significance.
- Wald test of independent equations when available.
- A candid statement if selection is not detected.

## 5. WIT / Many-IV Screening

Use when there are many candidate instruments, especially mechanically generated or domain-derived candidate pools, and some may be weak or invalid.

Core reference: Lin et al. (2024). See `literature.md`.

Appropriate settings:

- Mendelian randomization with many SNPs.
- Shift-share or Bartik-style decompositions with many shocks/exposure components.
- Spatial/network/peer IV pools with many candidates created by a transparent rule.

Workflow:

- Build a candidate IV pool from a clear rule.
- Screen or weight candidates using the chosen WIT procedure.
- Report the initial candidate pool, excluded candidates, effective IV pool, and final estimate.
- Add conventional diagnostics where estimable: first-stage strength, overidentification, weak-IV robust tests.

Do not use WIT language for a tiny hand-picked IV set. If the candidate pool is small, describe it as systematic subset screening instead.

## 6. TSCI / STCI Invalid-IV Methods

Use only after reading the relevant paper or package documentation. These methods are not simple “make weak IV strong” tools.

Core reference: Carl et al. (2025). See `literature.md`.

Applicability gate:

- There must be multiple candidate IVs with plausible partial validity or structured invalidity.
- The method's nonlinear/curvature or violation-structure assumptions must be meaningful for the treatment-outcome setting.
- The software implementation must run and produce interpretable diagnostics.
- If the diagnostic gate fails, report it as not supported by the current data rather than as a failed coefficient.

Report when usable:

- Candidate IV pool and construction rule.
- Method-specific validity/curvature diagnostics.
- Selected/effective instruments or weights if the method reports them.
- Estimated treatment effect and uncertainty.
- Comparison with conventional IV and weak-IV robust estimates.

## 7. LIML and Fuller-LIML

Use as weak-IV robustness for linear IV models.

Report:

- 2SLS coefficient.
- LIML coefficient.
- Fuller-LIML coefficient if available.
- First-stage/KP weak-IV diagnostics.
- Whether estimates are close in sign and magnitude.

Interpretation:

- Close LIML/Fuller and 2SLS estimates reduce concern about finite-sample weak-IV bias.
- They do not fix invalid instruments or make a bad exclusion restriction credible.

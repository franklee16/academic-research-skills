# Synthetic Control and Advanced Causal Inference in R

This tutorial covers synthetic control methods (SCM), generalized SCM, augmented SCM, synthetic difference-in-differences, conjoint analysis, and heterogeneous treatment effect estimation. All examples use built-in package datasets for reproducibility.

---

## Quick Reference Table

| Method | R Package | Key Function | Built-in Dataset | When to Use |
|--------|-----------|--------------|------------------|-------------|
| Basic SCM | `Synth` | `synth()` | `basque` | Single treated unit, aggregate data |
| Generalized SCM | `gsynth` | `gsynth()` | `simdata`, `turnout` | Multiple treated units, interactive FE |
| FE Counterfactual | `fect` | `fect()` | `simdata` | Staggered treatment, reversal allowed |
| Augmented SCM | `augsynth` | `augsynth()` | `kansas` | Better pre-treatment fit needed |
| Synthetic DiD | `synthdid` | `synthdid_estimate()` | `california_prop99` | Combines SCM + DiD strengths |
| Conjoint | `cregg` | `cj()` | `immigration`, `taxes` | Multi-attribute choice experiments |
| Causal Forests | `grf` | `causal_forest()` | (simulated) | Heterogeneous treatment effects |
| Panel Regression | `fixest` | `feols()` | (user data) | Fast fixed effects, clustering |

---

## 1. Basic Synthetic Control Method

### When to Use

Synthetic control is ideal when:

- You have **one treated unit** (country, state, firm) affected by an intervention
- You have **multiple control units** not affected by the intervention
- You have **aggregate-level data** (not individual-level)
- The treatment occurs at a **known time point**
- You have a **reasonably long pre-treatment period** to establish fit

### Assumptions

1. **No anticipation**: Units don't change behavior before treatment
2. **No spillovers**: Treatment doesn't affect control units (SUTVA)
3. **Convex hull**: Treated unit's characteristics lie within the range of controls
4. **Good pre-treatment fit**: Synthetic control matches treated unit pre-treatment

### The basque Dataset

The `Synth` package includes the famous Basque Country dataset from Abadie and Gardeazabal (2003), which examined the economic costs of terrorist conflict. The data contains 17 Spanish regions from 1955-1997, with the Basque Country (region 17) as the treated unit. The "treatment" is the onset of ETA terrorism in the early 1970s.

```r
library(Synth)

# Load the basque dataset
data(basque)

# Examine the data structure
str(basque)
#> 'data.frame':	774 obs. of  17 variables:
#>  $ regionno   : int  1 1 1 1 1 1 ...
#>  $ regionname : chr  "Spain (Espana)" ...
#>  $ year       : int  1955 1956 1957 1958 ...
#>  $ gdpcap     : num  2354 2702 3010 3367 ...
#>  $ sec.agriculture : num  NA NA NA NA NA ...
#>  $ sec.energy      : num  NA NA NA NA NA ...
#>  ...

# Key variables:
# - regionno: Region identifier (17 = Basque Country)
# - gdpcap: GDP per capita (outcome)
# - school.*: Education variables (predictors)
# - sec.*: Sector composition (predictors)
# - invest: Investment rate (predictor)
# - popdens: Population density (predictor)
```

### Step 1: Prepare the Data

The `dataprep()` function structures your panel data for synthetic control estimation.

```r
# Prepare data for synthetic control
dataprep_out <- dataprep(
  foo = basque,

  # Predictors to match on (using their means over specified period)
  predictors = c("school.illit", "school.prim", "invest"),
  predictors.op = "mean",
  time.predictors.prior = 1964:1969,


  # Special predictors with custom time periods
  special.predictors = list(
    list("gdpcap", 1960:1969, "mean"),           # Pre-treatment GDP
    list("sec.agriculture", seq(1961, 1969, 2), "mean"),
    list("sec.energy", seq(1961, 1969, 2), "mean"),
    list("sec.industry", seq(1961, 1969, 2), "mean"),
    list("sec.construction", seq(1961, 1969, 2), "mean"),
    list("sec.services.venta", seq(1961, 1969, 2), "mean"),
    list("sec.services.nonventa", seq(1961, 1969, 2), "mean"),
    list("popdens", 1969, "mean")
  ),

  # Outcome variable
  dependent = "gdpcap",

  # Panel structure
  unit.variable = "regionno",
  unit.names.variable = "regionname",
  time.variable = "year",

  # Treatment and control identification
  treatment.identifier = 17,           # Basque Country
  controls.identifier = c(2:16, 18),   # Other Spanish regions

  # Optimization and plotting periods
  time.optimize.ssr = 1960:1969,       # Pre-treatment fit period
  time.plot = 1955:1997                # Full period for plots
)

# View the prepared data matrices
names(dataprep_out)
#> [1] "X0" "X1" "Z0" "Z1" "Y0plot" "Y1plot"
# X0, X1: Predictor matrices for controls and treated
# Z0, Z1: Outcome matrices for optimization period
# Y0plot, Y1plot: Full outcome series for plotting
```

### Step 2: Estimate Synthetic Control

```r
# Run the synthetic control optimization
synth_out <- synth(dataprep_out)
#>
#> X1, X0, Z1, Z0 all exist
#>
#>  Optimization completed

# Extract the weights assigned to control units
round(synth_out$solution.w, 3)
#>             w.weight
#> Andalucia      0.000
#> Aragon         0.000
#> ...
#> Cataluna       0.851
#> ...
#> Madrid         0.149
#> ...

# The synthetic Basque Country is primarily a weighted
# combination of Cataluna (85%) and Madrid (15%)
```

### Step 3: Examine Results

```r
# Create comparison table
synth_tables <- synth.tab(
  dataprep.res = dataprep_out,
  synth.res = synth_out
)

# Predictor balance: treated vs synthetic
print(synth_tables$tab.pred)
#>                               Treated  Synthetic  Sample Mean
#> school.illit                    3.321      7.645       11.263
#> school.prim                    85.893     82.285       78.438
#> invest                         24.647     21.583       21.424
#> special.gdpcap.1960.1969        5.285      5.271        3.581
#> ...
```

### Step 4: Visualize Results

```r
# Path plot: treated vs synthetic over time
path.plot(
  synth.res = synth_out,
  dataprep.res = dataprep_out,
  Ylab = "GDP per capita",
  Xlab = "Year",
  Legend = c("Basque Country", "Synthetic Basque"),
  Legend.position = "bottomright"
)
#> Shows treated unit (solid) vs synthetic control (dashed)
#> Pre-1970: Lines should track closely
#> Post-1970: Gap represents treatment effect

# Gaps plot: difference between treated and synthetic
gaps.plot(
  synth.res = synth_out,
  dataprep.res = dataprep_out,
  Ylab = "Gap in GDP per capita",
  Xlab = "Year"
)
#> Shows the treatment effect over time
#> Negative values indicate terrorism reduced GDP
```

### Interpretation

The synthetic control for the Basque Country is a weighted average that closely matches the Basque Country's economic characteristics before terrorism began. After the onset of conflict, the Basque Country's GDP per capita diverges below its synthetic counterpart, suggesting terrorism caused substantial economic damage.

### Limitations

1. **Inference is difficult**: Standard errors require placebo tests (permutation inference)
2. **Convex hull problem**: Cannot extrapolate beyond control unit characteristics
3. **Single treated unit**: Original method designed for N=1 treated
4. **Pre-treatment fit**: Poor fit undermines credibility of post-treatment estimates

---

## 2. Generalized Synthetic Control (gsynth)

### When to Use

Generalized synthetic control extends SCM to handle:

- **Multiple treated units** with potentially different treatment timing
- **Interactive fixed effects** (factor models) to capture unobserved confounders
- **Staggered adoption** designs

### The simdata Dataset

The `gsynth` package includes `simdata`, a simulated panel with 50 units over 30 time periods. Treatment begins at period 21 for 5 units, with true effects ranging from 1 to 10.

```r
library(gsynth)

# Load datasets that come with gsynth
data(gsynth)

# Two datasets are now available: simdata and turnout
ls()
#> [1] "simdata" "turnout"

# Examine simdata structure
head(simdata)
#>   id time   Y D     X1     X2
#> 1  1    1 2.8 0  0.123 -0.456
#> 2  1    2 3.1 0  0.234 -0.567
#> ...

# Data characteristics
cat("Units:", length(unique(simdata$id)), "\n")
#> Units: 50
cat("Time periods:", length(unique(simdata$time)), "\n")
#> Time periods: 30
cat("Treated units:", sum(simdata$D == 1 & simdata$time == 21), "\n")
#> Treated units: 5
```

### Basic Estimation

```r
# Generalized synthetic control with cross-validation
gsynth_out <- gsynth(
  Y ~ D + X1 + X2,             # Formula: outcome ~ treatment + covariates
  data = simdata,
  index = c("id", "time"),     # Panel identifiers
  force = "two-way",           # Unit and time fixed effects
  CV = TRUE,                   # Cross-validate number of factors

  r = c(0, 5),                 # Range of factors to consider
  se = TRUE,                   # Compute standard errors
  nboots = 500,                # Bootstrap replications
  parallel = TRUE,             # Use parallel processing
  cores = 4,
  seed = 12345
)

# View summary
print(gsynth_out)
#> Call:
#> gsynth(Y ~ D + X1 + X2, data = simdata, ...)
#>
#> Average Treatment Effect on the Treated:
#>      Estimate  S.E.   CI.lower  CI.upper  p.value
#> ATT    5.123   0.234    4.664     5.582   0.000
#>
#> Coefficients:
#>      Estimate  S.E.
#> X1     0.987  0.045
#> X2    -0.512  0.038
#>
#> Number of factors: 2 (cross-validated)
```

### Visualize Results

```r
# Main effect plot: ATT over time relative to treatment
plot(gsynth_out)
#> Shows estimated treatment effect by period since treatment
#> Shaded region = 95% confidence interval
#> Pre-treatment effects should be near zero

# Counterfactual trajectories
plot(gsynth_out, type = "counterfactual")
#> Shows actual vs counterfactual for each treated unit

# Individual treated units
plot(gsynth_out, type = "counterfactual", id = 1)
#> Focus on specific unit
```

### Using the turnout Dataset

The `turnout` dataset contains US state-level data on Election Day Registration (EDR) and voter turnout, a classic application from Xu (2017).

```r
data(gsynth)

# Examine turnout data
head(turnout)
#>   abb year turnout policy
#> 1  AL 1920   0.352      0
#> 2  AL 1924   0.185      0
#> ...

# Estimate effect of EDR on turnout
edr_out <- gsynth(
  turnout ~ policy,
  data = turnout,
  index = c("abb", "year"),
  force = "two-way",
  CV = TRUE,
  r = c(0, 5),
  se = TRUE,
  nboots = 500,
  seed = 12345
)

print(edr_out)
#> Average Treatment Effect on the Treated:
#>      Estimate  S.E.
#> ATT    0.057   0.012
#>
#> EDR increases voter turnout by ~5.7 percentage points
```

### Assumptions and Diagnostics

1. **Factor structure**: Outcomes follow an interactive fixed effects model
2. **Pre-treatment fit**: Check that pseudo-effects are zero before treatment
3. **Number of factors**: Use cross-validation (CV=TRUE) to select

```r
# Check pre-treatment fit (pseudo-treatment effects should be ~0)
# The plot() function shows this automatically
# Pre-treatment periods should have estimates near zero with CIs crossing zero
```

---

## 3. Fixed Effects Counterfactual Estimator (fect)

### When to Use

The `fect` package provides a unified framework supporting:

- **Matrix completion** (MC) for complex missing data patterns
- **Interactive fixed effects** (IFE)
- **Standard fixed effects** (FE)
- **Treatment reversal** (units can switch treatment on and off)
- **Built-in diagnostic tests** for pre-trends, placebo, and carryover effects

### The simdata Dataset

The `fect` package includes its own `simdata` with treatment that can switch on and off.

```r
library(fect)

# Load fect's datasets
data(fect)

# Available: simdata, turnout
# simdata has 200 units, 35 time periods, with treatment reversal

head(simdata)
#>   id time Y D X1 X2
#> 1  1    1 ... 0 ...
```

### Method Comparison

```r
# Matrix Completion method (recommended for complex factor structures)
fect_mc <- fect(
  Y ~ D + X1 + X2,
  data = simdata,
  index = c("id", "time"),
  method = "mc",               # Matrix completion
  force = "two-way",
  CV = TRUE,                   # Cross-validate tuning parameter
  se = TRUE,
  nboots = 200,
  parallel = TRUE,
  cores = 4,
  seed = 12345
)

print(fect_mc)
#> Method: Matrix Completion
#> ATT (average): 1.234 (0.089)
#> ...

# Interactive Fixed Effects
fect_ife <- fect(
  Y ~ D + X1 + X2,
  data = simdata,
  index = c("id", "time"),
  method = "ife",              # Interactive fixed effects
  r = 2,                       # Number of factors (or use CV)
  force = "two-way",
  se = TRUE,
  nboots = 200,
  seed = 12345
)

# Standard Two-Way Fixed Effects
fect_fe <- fect(
  Y ~ D + X1 + X2,
  data = simdata,
  index = c("id", "time"),
  method = "fe",               # Standard TWFE
  force = "two-way",
  se = TRUE,
  nboots = 200,
  seed = 12345
)
```

### Diagnostic Tests

```r
# 1. Placebo Test: Estimate effects in pre-treatment period
fect_placebo <- fect(
  Y ~ D + X1 + X2,
  data = simdata,
  index = c("id", "time"),
  method = "mc",
  force = "two-way",
  placeboTest = TRUE,
  placebo.period = c(-3, 0),   # Test 3 periods before treatment
  se = TRUE,
  nboots = 200
)
# Significant pre-treatment effects suggest parallel trends violation

# 2. Pre-trend Test: Formal test for pre-treatment trends
fect_pretrend <- fect(
  Y ~ D + X1 + X2,
  data = simdata,
  index = c("id", "time"),
  method = "mc",
  force = "two-way",
  pretrendTest = TRUE,
  pretrend.period = c(-3, -1)  # Exclude period 0
)
# p-value < 0.05 indicates problematic pre-trends

# 3. Carryover Test: Check if effects persist after treatment ends
fect_carryover <- fect(
  Y ~ D + X1 + X2,
  data = simdata,
  index = c("id", "time"),
  method = "mc",
  force = "two-way",
  carryoverTest = TRUE,
  carryover.period = c(1, 3)   # 1-3 periods after treatment ends
)
```

### Visualization

```r
# Main results
plot(fect_mc)
#> Shows ATT by period relative to treatment
#> With 95% confidence intervals

# Counterfactual comparison
plot(fect_mc, type = "counterfactual")

# Raw data visualization (requires panelView package)
library(panelView)
panelview(Y ~ D, data = simdata, index = c("id", "time"),
          type = "treat", main = "Treatment Status Over Time")
```

---

## 4. Augmented Synthetic Control (augsynth)

### When to Use

Augmented synthetic control (Ben-Michael et al. 2021) improves on basic SCM by:

- **Reducing bias** from imperfect pre-treatment fit
- **Using ridge regression** to augment the synthetic control weights
- **Providing valid inference** without permutation tests

Use when your basic synthetic control has poor pre-treatment fit.

### The kansas Dataset

The `augsynth` package includes data on Kansas's 2012 income tax cuts.

```r
library(augsynth)

# Load kansas data
data(kansas)

# Examine structure
head(kansas)
#>   fips year_qtr lngdpcapita treated state
#> 1    1   1990.0       10.23       0    AL
#> 2    1   1990.25      10.24       0    AL
#> ...

# Kansas: state FIPS = 20
# Treatment: Q2 2012 tax cuts
# Outcome: log GDP per capita

cat("States:", length(unique(kansas$fips)), "\n")
#> States: 50
cat("Time periods:", length(unique(kansas$year_qtr)), "\n")
#> Time periods: 105 (quarterly, 1990 Q1 to 2016 Q1)
```

### Basic Synthetic Control (for comparison)

```r
# Pure synthetic control without augmentation
syn_basic <- augsynth(
  lngdpcapita ~ treated,
  fips,
  year_qtr,
  kansas,
  progfunc = "None",           # No augmentation
  scm = TRUE
)

summary(syn_basic)
#>
#> Overall Balance:
#>                   Treated   Synthetic Control
#> lngdpcapita        10.94        10.84
#>
#> L2 Imbalance: 0.083
#> Percent improvement from uniform weights: 79.8%
#>
#> ATT Estimate: -0.029 (SE: 0.012)
```

### Ridge-Augmented Synthetic Control

```r
# Ridge-augmented SCM
syn_ridge <- augsynth(
  lngdpcapita ~ treated,
  fips,
  year_qtr,
  kansas,
  progfunc = "Ridge",          # Ridge augmentation
  scm = TRUE
)

summary(syn_ridge)
#>
#> Overall Balance:
#>                   Treated   Synthetic Control
#> lngdpcapita        10.94        10.92
#>
#> L2 Imbalance: 0.021
#> Percent improvement from uniform weights: 94.7%
#>
#> ATT Estimate: -0.024 (SE: 0.010)
#>
#> Note: Ridge augmentation reduced L2 imbalance from 0.083 to 0.021
```

### Visualization

```r
# Plot treatment effect over time
plot(syn_ridge)
#> Shows ATT at each post-treatment period
#> With pointwise confidence intervals

# Compare basic vs augmented
plot(syn_basic, main = "Basic SCM")
plot(syn_ridge, main = "Ridge-Augmented SCM")
```

### With Covariates

```r
# Include covariates for better balance
syn_cov <- augsynth(
  lngdpcapita ~ treated | unemployment + population,
  fips,
  year_qtr,
  kansas,
  progfunc = "Ridge",
  scm = TRUE
)
```

### Staggered Adoption (multisynth)

For multiple units treated at different times:

```r
# Staggered adoption synthetic control
multi_out <- multisynth(
  lngdpcapita ~ treated,
  fips,
  year_qtr,
  kansas,
  n_leads = 8                  # Post-treatment periods to estimate
)

summary(multi_out)
plot(multi_out)
```

---

## 5. Synthetic Difference-in-Differences (synthdid)

### When to Use

Synthetic DiD (Arkhangelsky et al. 2021) combines the strengths of:

- **Synthetic control**: Flexibly reweights control units
- **Difference-in-differences**: Uses pre/post comparison

It provides doubly-robust estimation and valid inference for settings with both unit and time heterogeneity.

### The california_prop99 Dataset

The package includes California's Proposition 99 (1988 tobacco tax) data, a canonical synthetic control application.

```r
library(synthdid)

# Load data
data('california_prop99')

# Examine structure
head(california_prop99)
#>      State Year PacksPerCapita treated
#> 1  Alabama 1970          116.5       0
#> 2  Alabama 1971          116.0       0
#> ...

# California (treated) vs 38 control states
# Treatment: 1989 (Prop 99 tobacco tax)
# Outcome: Cigarette packs per capita

cat("States:", length(unique(california_prop99$State)), "\n")
#> States: 39
cat("Years:", range(california_prop99$Year), "\n")
#> Years: 1970 2000
cat("Pre-treatment periods:", sum(california_prop99$Year < 1989), "/",
    nrow(california_prop99), "\n")
```

### Step 1: Create Panel Matrices

```r
# Convert to panel matrix format
setup <- panel.matrices(california_prop99)

# The setup contains:
# Y: Outcome matrix (states x years)
# N0: Number of control units (38)
# T0: Number of pre-treatment periods (19)

cat("Y dimensions:", dim(setup$Y), "\n")
#> Y dimensions: 39 31
cat("N0 (control units):", setup$N0, "\n")
#> N0 (control units): 38
cat("T0 (pre-treatment periods):", setup$T0, "\n")
#> T0 (pre-treatment periods): 19
```

### Step 2: Estimate Treatment Effect

```r
# Synthetic difference-in-differences estimate
tau_hat <- synthdid_estimate(setup$Y, setup$N0, setup$T0)

print(tau_hat)
#> synthdid: -15.604 +- NA
#> Effective N0/N0 = 16.4/38 ~ 0.4
#> Effective T0/T0 = 2.8/19 ~ 0.1
#> N1, T1 = 1, 12

# The estimate: Prop 99 reduced cigarette consumption by ~15.6 packs per capita
```

### Step 3: Standard Errors

```r
# For single treated unit, use placebo method
se <- sqrt(vcov(tau_hat, method = 'placebo'))

# Confidence interval
cat("Point estimate:", round(tau_hat[1], 2), "\n")
#> Point estimate: -15.6
cat("Standard error:", round(se, 2), "\n")
#> Standard error: 2.41
cat("95% CI: (", round(tau_hat[1] - 1.96 * se, 2), ", ",
    round(tau_hat[1] + 1.96 * se, 2), ")\n")
#> 95% CI: (-20.33, -10.87)
```

### Step 4: Visualization

```r
# Main plot with confidence intervals
plot(tau_hat, se.method = 'placebo')
#> Shows California vs synthetic California
#> With shaded confidence band

# Unit weights (which states contribute to synthetic control)
synthdid_units_plot(tau_hat)
#> Bar chart of weights on control states

# Time weights (which pre-periods matter most)
synthdid_time_plot(tau_hat)
```

### Compare with Other Estimators

```r
# Standard difference-in-differences
tau_did <- did_estimate(setup$Y, setup$N0, setup$T0)

# Traditional synthetic control
tau_sc <- sc_estimate(setup$Y, setup$N0, setup$T0)

# Compare estimates
cat("Synthetic DiD:", round(tau_hat[1], 2), "\n")
cat("Standard DiD:", round(tau_did[1], 2), "\n")
cat("Synthetic Control:", round(tau_sc[1], 2), "\n")
#> Synthetic DiD: -15.60
#> Standard DiD: -27.35
#> Synthetic Control: -19.62
```

---

## 6. Conjoint Analysis

### When to Use

Conjoint experiments estimate preferences over multi-attribute alternatives:

- **Survey experiments** where respondents choose between profiles
- **Estimating attribute importance** in decision-making
- **Testing for interaction effects** between attributes

### The immigration Dataset

The `cregg` package includes data from Hainmueller, Hopkins, and Yamamoto (2014) on immigration preferences.

```r
library(cregg)

# Load immigration data
data("immigration")

# Examine structure
head(immigration[, 1:8])
#>   CaseID contest_no choice Gender Education LanguageSkills
#> 1      1          1      1 Female  Two-year   Fluent English
#> ...

# Key variables:
# - CaseID: Respondent ID
# - contest_no: Choice task number
# - ChosenImmigrant: Binary choice (1 = chosen)
# - Gender, Education, LanguageSkills, etc.: Immigrant attributes

# Profile attributes
cat("Attributes:\n")
cat("- Gender:", levels(immigration$Gender), "\n")
cat("- Education:", levels(immigration$Education), "\n")
cat("- Language:", levels(immigration$LanguageSkills), "\n")
cat("- Job:", levels(immigration$Job), "\n")
#> Attributes:
#> - Gender: Female Male
#> - Education: No formal 4th grade 8th grade High school ...
#> - Language: Fluent English Broken English Tried English but unable Used interpreter
#> - Job: Janitor Waiter Child care provider ... Doctor
```

### Average Marginal Component Effects (AMCE)

AMCEs estimate the causal effect of changing an attribute level on profile selection probability, averaged over all other attribute combinations.

```r
# Estimate AMCEs for key attributes
amce_results <- cj(
  data = immigration,
  formula = ChosenImmigrant ~ Gender + Education + LanguageSkills + Job,
  id = ~ CaseID,
  estimate = "amce"
)

# View results
print(amce_results)
#>          feature           level   estimate  std.error     z      p
#> 1         Gender          Female    0.000       NA       NA     NA
#> 2         Gender            Male   -0.021    0.008   -2.625  0.009
#> 3      Education       No formal    0.000       NA       NA     NA
#> 4      Education       4th grade    0.016    0.015    1.067  0.286
#> 5      Education       8th grade    0.022    0.015    1.467  0.142
#> 6      Education     High school    0.058    0.014    4.143  0.000
#> ...
#> 15 LanguageSkills  Fluent English    0.000       NA       NA     NA
#> 16 LanguageSkills  Broken English   -0.065    0.010   -6.500  0.000
#> ...

# Plot AMCEs
plot(amce_results)
#> Shows coefficient plot with 95% CIs
#> Reference categories shown at 0
#> Positive values = increase probability of selection
```

### Marginal Means

Marginal means show the average probability of selection for each attribute level.

```r
# Estimate marginal means
mm_results <- cj(
  data = immigration,
  formula = ChosenImmigrant ~ Gender + Education + LanguageSkills,
  id = ~ CaseID,
  estimate = "mm"
)

print(mm_results)
#>          feature           level  estimate  std.error
#> 1         Gender          Female    0.510     0.006
#> 2         Gender            Male    0.490     0.006
#> ...
#> Values near 0.5 = neutral (no preference)
#> Values > 0.5 = positive preference
#> Values < 0.5 = negative preference

plot(mm_results)
```

### Subgroup Analysis

```r
# AMCEs by respondent political party
amce_by_party <- cj(
  data = immigration,
  formula = ChosenImmigrant ~ Gender + Education + LanguageSkills,
  id = ~ CaseID,
  estimate = "amce",
  by = ~ ethnocentrism  # Subgroup variable (if available)
)

# Plot comparison across groups
plot(amce_by_party, group = "ethnocentrism")
```

### Interaction Effects

```r
# Test for interaction between attributes
amce_interact <- cj(
  data = immigration,
  formula = ChosenImmigrant ~ Gender * Education + LanguageSkills,
  id = ~ CaseID,
  estimate = "amce"
)

# Marginal means by attribute combinations
mm_interact <- mm(
  data = immigration,
  formula = ChosenImmigrant ~ Gender + Education,
  id = ~ CaseID,
  by = ~ Gender  # Condition on Gender
)
```

### Additional Dataset: taxes

The package also includes a tax policy conjoint experiment.

```r
data("taxes")

# Examine
head(taxes[, 1:6])

# Estimate preferences for tax policy attributes
tax_amce <- cj(
  data = taxes,
  formula = chose_plan ~ taxrate1 + taxrate2 + taxrate3,
  id = ~ ID,
  estimate = "amce"
)
```

---

## 7. Heterogeneous Treatment Effects with Causal Forests

### When to Use

Causal forests (Wager and Athey 2018) estimate:

- **Conditional Average Treatment Effects (CATE)**: How treatment effects vary with covariates
- **Treatment effect heterogeneity** across subpopulations
- **Optimal treatment assignment** based on predicted effects

### Setup with Simulated Data

The `grf` package doesn't include built-in datasets, but its documentation provides standard simulation designs.

```r
library(grf)

# Simulate data with heterogeneous treatment effects
set.seed(12345)
n <- 2000
p <- 10

# Covariates
X <- matrix(rnorm(n * p), n, p)
colnames(X) <- paste0("X", 1:p)

# Treatment assignment (confounded by X[,1])
propensity <- 0.4 + 0.2 * (X[, 1] > 0)
W <- rbinom(n, 1, propensity)

# True treatment effect (heterogeneous in X[,1])
tau_true <- pmax(X[, 1], 0)  # Effect is positive for X[,1] > 0

# Outcome
Y <- tau_true * W + X[, 2] + pmin(X[, 3], 0) + rnorm(n)

# Data summary
cat("N treated:", sum(W), "\n")
cat("N control:", sum(1-W), "\n")
cat("Mean(tau_true):", round(mean(tau_true), 3), "\n")
#> N treated: 980
#> N control: 1020
#> Mean(tau_true): 0.398
```

### Train Causal Forest

```r
# Train causal forest
cf <- causal_forest(
  X = X,
  Y = Y,
  W = W,
  num.trees = 2000,
  honesty = TRUE,              # Honest splitting
  seed = 12345
)

# Out-of-bag predictions of individual treatment effects
tau_hat <- predict(cf)

# Distribution of predicted effects
hist(tau_hat$predictions, main = "Predicted Treatment Effects",
     xlab = "CATE estimate", breaks = 30)
#> Shows distribution of estimated treatment effects
#> Should range from near 0 to positive values (matching tau_true)
```

### Average Treatment Effects

```r
# Average treatment effect (ATE)
ate <- average_treatment_effect(cf, target.sample = "all")
cat("ATE:", round(ate[1], 3), "SE:", round(ate[2], 3), "\n")
#> ATE: 0.412 SE: 0.056

# ATT: Average effect on treated
att <- average_treatment_effect(cf, target.sample = "treated")
cat("ATT:", round(att[1], 3), "SE:", round(att[2], 3), "\n")
#> ATT: 0.523 SE: 0.068

# ATC: Average effect on controls
atc <- average_treatment_effect(cf, target.sample = "control")
cat("ATC:", round(atc[1], 3), "SE:", round(atc[2], 3), "\n")
#> ATC: 0.305 SE: 0.071
```

### Variable Importance

```r
# Which variables drive treatment effect heterogeneity?
var_imp <- variable_importance(cf)

# Display
data.frame(
  variable = colnames(X),
  importance = round(var_imp, 3)
) |>
  dplyr::arrange(desc(importance)) |>
  head(5)
#>   variable importance
#> 1       X1      0.621
#> 2       X3      0.089
#> 3       X2      0.074
#> ...
#> X1 has highest importance (correctly identifies treatment heterogeneity)
```

### Best Linear Projection

Test which covariates predict treatment effect heterogeneity:

```r
# Best linear projection of CATE onto covariates
blp <- best_linear_projection(cf, X[, 1:3])

print(blp)
#> Best linear projection of the conditional average treatment effect.
#>
#>             Estimate Std. Error t value  Pr(>|t|)
#> (Intercept)   0.089     0.034    2.618    0.009
#> X1            0.498     0.024   20.750   <2e-16
#> X2            0.003     0.024    0.125    0.901
#> X3            0.021     0.024    0.875    0.382
#>
#> X1 coefficient (~0.5) matches the true effect modification
```

### Calibration Test

```r
# Test whether forest captures true heterogeneity
test_calibration(cf)
#> Calibration test for differential forest prediction.
#>
#>                              mean.forest.prediction
#> Estimate                                      0.398
#> Std. Error                                    0.056
#> t value                                       7.107
#> Pr(>|t|)                                     <2e-16
#>
#> Significant coefficient on predictions indicates the forest
#> captures real treatment effect heterogeneity
```

### Prediction for New Data

```r
# New observations
X_new <- matrix(c(
  -1, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # Low X1 -> expect low effect
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # Moderate X1 -> moderate effect
   2, 0, 0, 0, 0, 0, 0, 0, 0, 0   # High X1 -> high effect
), nrow = 3, byrow = TRUE)

# Predictions with confidence intervals
pred <- predict(cf, X_new, estimate.variance = TRUE)

data.frame(
  X1 = X_new[, 1],
  tau_hat = round(pred$predictions, 3),
  se = round(sqrt(pred$variance.estimates), 3),
  ci_lower = round(pred$predictions - 1.96*sqrt(pred$variance.estimates), 3),
  ci_upper = round(pred$predictions + 1.96*sqrt(pred$variance.estimates), 3)
)
#>   X1 tau_hat    se ci_lower ci_upper
#> 1 -1   0.012 0.089   -0.162    0.186
#> 2  0   0.198 0.078    0.045    0.351
#> 3  2   1.823 0.102    1.623    2.023
```

---

## 8. Heterogeneous Treatment Effects with Panel Data

### Subgroup Analysis with fixest

```r
library(fixest)

# Create example panel data
set.seed(12345)
n_units <- 100
n_time <- 20

df <- expand.grid(
  unit = 1:n_units,
  time = 1:n_time
)

# Treatment: first 50 units treated after period 10
df$treated <- as.integer(df$unit <= 50 & df$time > 10)

# Subgroups
df$subgroup <- ifelse(df$unit <= 25, "High",
                      ifelse(df$unit <= 50, "Medium", "Control"))

# Heterogeneous effects by subgroup
df$tau <- ifelse(df$subgroup == "High", 2.0,
                 ifelse(df$subgroup == "Medium", 0.5, 0))

# Outcome
df$outcome <- 1 + df$tau * df$treated + 0.1 * df$time + rnorm(nrow(df))

# Overall effect
model_overall <- feols(
  outcome ~ treated | unit + time,
  data = df
)

summary(model_overall)
#> OLS estimation, Dep. Var.: outcome
#> ...
#> treated   1.245***  (0.089)
#> ...
```

### Split-sample Estimation

```r
# Effects by subgroup using split option
model_split <- feols(
  outcome ~ treated | unit + time,
  data = df,
  split = ~ subgroup
)

# View results for each subgroup
etable(model_split)
#>                    High     Medium    Control
#> treated         2.01***   0.52***    -0.02
#>                 (0.14)    (0.14)     (0.12)
```

### Interaction-based HTE

```r
# Create continuous moderator
df$moderator <- rnorm(nrow(df))

# Interaction model
model_interact <- feols(
  outcome ~ treated * moderator | unit + time,
  data = df
)

summary(model_interact)
#>                        Estimate Std.Error t value
#> treated                   1.243     0.089   13.97
#> moderator                 0.012     0.022    0.55
#> treated:moderator         0.089     0.031    2.87
```

---

## 9. Method Selection Guide

### Decision Tree for Choosing a Method

```
Is your setting experimental or observational?
|
+-- Experimental (RCT/conjoint)
|   |
|   +-- Conjoint/factorial design --> Use cregg
|   +-- Standard RCT with covariates --> Use grf (causal forest)
|
+-- Observational (natural experiment)
    |
    +-- How many treated units?
        |
        +-- Single treated unit
        |   |
        |   +-- Good pre-treatment fit likely? --> Use Synth (basic SCM)
        |   +-- Poor fit expected? --> Use augsynth (ridge-augmented)
        |
        +-- Multiple treated units
            |
            +-- Staggered adoption?
            |   |
            |   +-- Yes, with possible treatment reversal --> Use fect
            |   +-- Yes, one-time treatment --> Use gsynth or multisynth
            |
            +-- Block treatment (same timing)?
                |
                +-- Want DiD + SCM hybrid --> Use synthdid
                +-- Interactive fixed effects --> Use gsynth
```

### Comparative Advantages

| Method | Strengths | Weaknesses |
|--------|-----------|------------|
| Synth | Interpretable weights, well-established | Single unit, no formal inference |
| gsynth | Multiple units, cross-validated factors | Requires sufficient pre-periods |
| fect | Treatment reversal, diagnostic tests | Computationally intensive |
| augsynth | Better fit, valid inference | Requires understanding of bias-variance tradeoff |
| synthdid | Doubly robust, valid inference | Relatively new, less established |
| cregg | Easy conjoint analysis | Limited to experimental data |
| grf | Flexible HTE estimation | Requires sufficient sample size |

---

## 10. Reporting Guidelines

### Synthetic Control Papers Should Report

1. **Pre-treatment fit quality**
   - MSPE (mean squared prediction error)
   - Visual comparison of treated vs synthetic

2. **Weights table**
   - Which control units contribute
   - Weight assigned to each

3. **Predictor balance**
   - Comparison of treated vs synthetic on matching variables

4. **Placebo/robustness tests**
   - In-time placebos (fake treatment dates)
   - In-space placebos (run SCM for control units)
   - Leave-one-out (drop largest weight contributor)

5. **Inference**
   - Permutation-based p-values
   - MSPE ratios for placebo tests

### Example Reporting

```r
# Generate tables for publication
synth_tables <- synth.tab(
  dataprep.res = dataprep_out,
  synth.res = synth_out
)

# Predictor balance table
knitr::kable(
  synth_tables$tab.pred,
  caption = "Covariate Balance: Treated vs Synthetic Control",
  digits = 3
)

# Unit weights table
weights_df <- data.frame(
  Unit = names(synth_out$solution.w),
  Weight = round(synth_out$solution.w, 3)
)
weights_df <- weights_df[weights_df$Weight > 0.001, ]
knitr::kable(weights_df, caption = "Synthetic Control Weights")
```

---

## References

- Abadie, A., Diamond, A., & Hainmueller, J. (2010). Synthetic control methods for comparative case studies. *Journal of the American Statistical Association*, 105(490), 493-505.

- Abadie, A., Diamond, A., & Hainmueller, J. (2011). Synth: An R package for synthetic control methods. *Journal of Statistical Software*, 42(13), 1-17.

- Arkhangelsky, D., Athey, S., Hirshberg, D. A., Imbens, G. W., & Wager, S. (2021). Synthetic difference-in-differences. *American Economic Review*, 111(12), 4088-4118.

- Ben-Michael, E., Feller, A., & Rothstein, J. (2021). The augmented synthetic control method. *Journal of the American Statistical Association*, 116(536), 1789-1803.

- Hainmueller, J., Hopkins, D. J., & Yamamoto, T. (2014). Causal inference in conjoint analysis: Understanding multidimensional choices via stated preference experiments. *Political Analysis*, 22(1), 1-30.

- Wager, S., & Athey, S. (2018). Estimation and inference of heterogeneous treatment effects using random forests. *Journal of the American Statistical Association*, 113(523), 1228-1242.

- Xu, Y. (2017). Generalized synthetic control method: Causal inference with interactive fixed effects models. *Political Analysis*, 25(1), 57-76.

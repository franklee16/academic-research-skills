# Synthetic Control Methods in Stata

Synthetic control method for comparative case studies. All code tested on Stata 15+.

---

## 1. Overview

The synthetic control method constructs a weighted combination of control units to serve as a counterfactual for a treated unit. It is designed for:

- Single treated unit
- Aggregate-level data (states, countries, regions)
- Clear treatment timing
- Multiple potential control units

---

## 2. Data Requirements

Panel data structure with:
- Unit identifier
- Time variable
- Outcome variable
- Predictor variables

```stata
* Declare panel structure
tsset unit_id time_var
```

---

## 3. Basic Synthetic Control

```stata
* Install synth package
ssc install synth, replace

* Basic syntax
synth outcome_var predictors, ///
    trunit(#) trperiod(#)
```

### Example with Simulated Data

```stata
clear
set seed 12345
set obs 400

* Create panel: 20 states, 20 years each
gen state = ceil(_n/20)
bysort state: gen year = 1980 + _n

* Outcome variable
gen y = 100 + state*2 + year*0.5 + rnormal(0, 5)

* Treatment: state 1 treated after year 1990
replace y = y - 15 if state == 1 & year >= 1990

* Covariates
gen x1 = rnormal(50, 10)
gen x2 = rnormal(1000, 200)

* Declare panel
tsset state year

* Run synthetic control
synth y x1 x2 y(1985) y(1988), trunit(1) trperiod(1990)
```

---

## 4. Specifying Predictors

### Average of Variable Over Pre-Period

```stata
* x1 averaged over all pre-treatment periods
synth y x1 x2, trunit(1) trperiod(1990)
```

### Specific Year Values

```stata
* y at specific years as predictors
synth y y(1985) y(1988), trunit(1) trperiod(1990)
```

### Range of Years

```stata
* y averaged over 1985-1988
synth y y(1985(1)1988), trunit(1) trperiod(1990)
```

### Combined Predictors

```stata
synth y x1 x2 y(1985) y(1988), trunit(1) trperiod(1990)
```

---

## 5. Output Interpretation

The synth output shows:

### RMSPE (Root Mean Squared Prediction Error)
- Measures pre-treatment fit
- Lower is better

### Unit Weights
- Which control units comprise the synthetic control
- Weights sum to 1

### Predictor Balance
- Compares treated vs synthetic control on predictors
- Should be similar if fit is good

---

## 6. Options

| Option | Purpose |
|--------|---------|
| `trunit(#)` | Treated unit ID |
| `trperiod(#)` | First treatment period |
| `fig` | Display results figure |
| `keep(filename)` | Save results to file |
| `nested` | Use nested optimization |
| `allopt` | Try all optimization methods |

---

## 7. Inference

### Placebo Tests (In-Space)

Run synth for each control unit as if it were treated:

```stata
* Store treated unit result
synth y x1 x2 y(1985) y(1988), trunit(1) trperiod(1990) ///
    keep(synth_treated) replace

* Placebo for control unit 2
synth y x1 x2 y(1985) y(1988), trunit(2) trperiod(1990) ///
    keep(synth_placebo2) replace

* Compare RMSPEs
* Treated effect is significant if RMSPE ratio is large
```

### Placebo Tests (In-Time)

Apply treatment at different (fake) times:

```stata
* True treatment 1990
synth y x1 x2 y(1982) y(1985), trunit(1) trperiod(1990)

* Placebo: treatment at 1985 (before actual treatment)
synth y x1 x2 y(1982), trunit(1) trperiod(1985)
```

---

## 8. Limitations

- Single treated unit (not for multiple treatment)
- Requires good pre-treatment fit
- Sensitive to predictor choice
- No built-in inference (must do placebo tests)
- Cannot extrapolate beyond donor pool characteristics

---

## Quick Reference

### Basic Syntax

```stata
synth outcome predictors, trunit(#) trperiod(#)
```

### Package Installation

```stata
ssc install synth, replace
```

### Key Components

| Component | Description |
|-----------|-------------|
| `outcome` | Dependent variable |
| `predictors` | Variables to match on |
| `trunit()` | ID of treated unit |
| `trperiod()` | First treatment period |

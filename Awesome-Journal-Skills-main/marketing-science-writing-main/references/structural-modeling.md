# Structural Modeling in Marketing

Structural models in marketing combine consumer utility theory, firm behavior, and market equilibrium to answer counterfactual questions.

---

## 1. The BLP Framework (Berry-Levinsohn-Pakes)

The workhorse model for aggregate demand estimation with differentiated products.

### Consumer Utility

$u_{ijt} = \alpha_i p_{jt} + \beta_i x_{jt} + \xi_{jt} + \varepsilon_{ijt}$

- $p_{jt}$: price of product j in market t
- $x_{jt}$: observed product characteristics
- $\xi_{jt}$: unobserved product quality (structural error)
- $\alpha_i = \alpha + \pi y_i + \sigma_\alpha \nu_{i\alpha}$: heterogeneous price sensitivity
- $\beta_i = \beta + \Sigma \nu_{i\beta}$: heterogeneous taste for characteristics
- $\varepsilon_{ijt}$: i.i.d. Type I extreme value (logit error)

### Demand Inversion

Given market shares $s_{jt}$ and parameters $\theta$, the mean utility $\delta_{jt}$ is the unique fixed point of:

$\delta_{jt}^{h+1} = \delta_{jt}^h + \ln s_{jt} - \ln s_{jt}(\delta^h, \theta)$

### Instruments

Standard instruments for price endogeneity:
1. **Cost shifters**: input prices, wage rates in production location
2. **Hausman instruments**: prices in other markets
3. **BLP instruments**: characteristics of competing products (differentiation IVs)
4. **Optimal instruments**: Chamberlain (1987) approach

### Supply Side

Firms set prices to maximize profit under Bertrand-Nash:
$p_{jt} = mc_{jt} + \text{markup}_{jt}(\theta)$

The FOCs provide additional moments for GMM estimation.

---

## 2. Dynamic Structural Models

For intertemporal decisions (brand choice with state dependence, inventory, learning).

### Key Components

- **State variables**: inventory, brand loyalty, advertising goodwill
- **Choice variables**: purchase, consumption
- **State transition**: how choices affect future states
- **Value function**: Bellman equation solved via nested fixed point (Rust 1987) or conditional choice probability (Hotz-Miller)

### CCP Approach (Hotz-Miller)

Avoids solving the dynamic program by estimating conditional choice probabilities from data and inverting to recover value functions.

---

## 3. Counterfactual Simulations

The purpose of structural estimation is to simulate outcomes under alternative policies.

### Standard Counterfactuals

1. **Merger simulation**: change ownership structure, recompute equilibrium
2. **Tax/subsidy**: add per-unit tax on a product, recompute prices and shares
3. **Product removal/introduction**: add or remove products from choice set
4. **Information provision**: change consumer perceptions of attributes

### Reporting Standards

- Present baseline (status quo) and counterfactual side-by-side
- Compute compensating variation for consumer welfare
- Report firm profit changes
- Bootstrap standard errors for counterfactual outcomes

---

## 4. Estimation Diagnostics

| Diagnostic | Purpose | Threshold |
|-----------|---------|-----------|
| First-stage F-statistic | Instrument relevance | F > 10 |
| Hansen J-test | Overidentification | p > 0.10 |
| Price elasticity | Face validity | Negative, reasonable magnitude |
| Markup | Economic plausibility | Positive, industry-reasonable |
| Holdout prediction | External validity | MAPE < 20% preferred |

---

## 5. Common Pitfalls

1. **Weak instruments**: Hausman instruments may be weak in concentrated markets. Use cost shifters.
2. **Ignoring supply side**: Estimating demand without supply moments loses efficiency and may give biased counterfactuals.
3. **Numerical issues**: BLP contraction mapping may not converge with poor starting values. Use tight tolerance and good initialization.
4. **Too many random coefficients**: Overfitting heterogeneity. Parimony; add random coefficients only where economically motivated.
5. **Not reporting own- and cross-price elasticities**: These are the fundamental outputs of demand estimation. Always report a representative subset.

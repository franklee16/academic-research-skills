# Model Primitives

**Date:** 2026-06-14
**Stage:** 4 — Model Primitives

---

## Model Overview

Two children, identical in innate ability θ but differing in hukou registration status τ ∈ {U, R} (urban/rural), each choose how much to invest in education. They face the same cost function and the same ability level, but different expected wage returns: the urban child's wage depends only on (e, θ), while the rural child's wage is penalized by a factor δ ∈ (0,1) except when education is high enough to trigger access to the urban labor market via an "escape route" (e.g., elite university admission) with probability p(e). The model is a static single-agent optimization problem run twice — once per type — and the central object is the investment gap Δe*(θ) = e*_U(θ) − e*_R(θ), whose sign depends on θ relative to a threshold θ̄.

---

## 1. Agents

| Label | Name | Count | Characteristics |
|-------|------|-------|----------------|
| C_U | Urban child | 1 | Hukou τ = U; ability θ; price-taking in labor market |
| C_R | Rural child | 1 | Hukou τ = R; same ability θ; faces hukou wage penalty δ and escape route p(e) |

Both agents are rational and risk-neutral. There is no strategic interaction between them; each solves an independent optimization. The comparison is purely parametric (same θ, different τ).

---

## 2. Timing

1. **Nature** fixes ability θ ∈ Θ = [θ_L, θ_H] ⊂ ℝ₊ and hukou status τ ∈ {U, R} for each child. Both are common knowledge.
2. Each child independently chooses education investment e ∈ [0, ē], paying cost C(e) in period 0.
3. The labor market opens in period 1. Wages are determined by (e, θ, τ) according to the wage function defined below.
4. Each child receives net lifetime payoff V(e; θ, τ) and the game ends.

**Game type:** Static (two-period: invest then earn). No repetition. No strategic interaction.
**Commitment:** The hukou status τ is fixed at birth and cannot be changed except via the escape route. Education e is irreversible once chosen.

---

## 3. Information Structure

**Complete information:** All parameters (θ, τ, w(·), C(·), δ, ê, p(·), r) are common knowledge. There is no private information and no uncertainty about the model structure.

**State variables known by each child:**
- Own ability θ (known)
- Own hukou status τ (known)
- Wage function w(e, θ, τ) (known)
- Cost function C(e) (known)
- Escape-route parameters (ê, p(·)) (known)

**Common knowledge:** All of the above, plus the structure of the two-period model.

*Note:* Ability θ is observable to the labor market (wages reflect θ directly). The model abstracts from signaling; education builds genuine human capital.

---

## 4. Preferences

### Urban child (C_U)
- **Net payoff:** V_U(e; θ) = w(e, θ) / r − C(e)
  where w(e, θ) = A · θ^α · e^β is the competitive urban wage (A > 0, α > 0, β ∈ (0,1)), and r > 0 is the opportunity cost of funds (discount rate). The term w(e,θ)/r is the present value of lifetime earnings (perpetuity normalization).
- **Maximizes:** V_U(e; θ) over e ∈ [0, ē]
- **Risk attitude:** Risk-neutral

### Rural child (C_R)
- **Net payoff:** V_R(e; θ) = W_R(e, θ) / r − C(e)

  where the effective rural wage W_R is:

  **Case 1 — No escape route (e < ê):**
  W_R(e, θ) = δ · w(e, θ),   δ ∈ (0, 1)

  **Case 2 — With escape route (e ≥ ê):**
  W_R(e, θ) = [δ + (1 − δ) · p(e)] · w(e, θ)

  where p: [ê, ē] → [0, 1] is the escape-route probability function, with p(ê) = p₀ > 0, p'(e) ≥ 0, p(ē) ≤ 1.

- **Maximizes:** V_R(e; θ) over e ∈ [0, ē]
- **Risk attitude:** Risk-neutral

**Interpretation of W_R:** The rural child earns the full urban wage w(e,θ) with probability p(e) (escape succeeds) and the discounted rural wage δ·w(e,θ) with probability 1−p(e). The weighted average is W_R(e,θ) = [δ + (1−δ)p(e)]·w(e,θ).

---

## 5. Action and Strategy Spaces

### Urban child
- **Action space:** e_U ∈ [0, ē] (continuous)
- **Strategy:** Choose e_U to maximize V_U(e_U; θ)
- **Constraints:** e_U ≥ 0 (no negative investment); C(e_U) ≤ I_U + L (budget: family income plus loan capacity; relaxed to non-binding in the baseline, binding in the extension)

### Rural child
- **Action space:** e_R ∈ [0, ē] (continuous)
- **Strategy:** Choose e_R to maximize V_R(e_R; θ)
- **Constraints:** Same feasibility constraint; same relaxation in baseline

---

## 6. State Variables and Outcome Space

**State variables:**

| Symbol | Meaning | Domain |
|--------|---------|--------|
| θ | Innate ability | [θ_L, θ_H] ⊂ ℝ₊ |
| τ | Hukou status | {U, R} |
| δ | Hukou wage penalty (rural discount) | (0, 1) |
| ê | Escape-route education threshold | (0, ē) |
| p(e) | Escape-route probability | [0,1], defined on [ê, ē] |
| p₀ | Jump probability at threshold: p(ê) | (0, 1] |
| r | Opportunity cost of funds | ℝ₊₊ |

**Outcome space:** Each child's outcome is an education level e* ∈ [0, ē] and resulting payoff V(e*; θ, τ) ∈ ℝ.

**Central object:** Investment gap Δe*(θ) ≡ e*_U(θ) − e*_R(θ).

**Outcome function:** Strategies (e_U, e_R) map directly to payoffs via V_U and V_R.

---

## 7. Equilibrium Concept Candidates

### Candidate A: Individual Optimality (IO)
- **When appropriate:** Single-agent optimization; no strategic interaction between C_U and C_R; each solves their own problem independently.
- **What it requires:** e* = argmax V(e; θ, τ) subject to e ∈ [0, ē]. First-order condition (when interior): marginal benefit = marginal cost.
- **Potential issues:** The rural child's problem may have a non-interior optimum (corner at ê from above) if the escape-route probability jumps discretely at ê, requiring comparison of the interior FOC solution with the corner solution e = ê.

### Candidate B: Competitive Equilibrium (CE)
- **When appropriate:** If the model is embedded in a general equilibrium where many children of each type make investment decisions and aggregate labor supply affects wages.
- **What it requires:** Market-clearing wage function; aggregate behavior is consistent with individual optimization.
- **Potential issues:** Adds complexity without changing the core individual investment result; appropriate for the GE extension but not the baseline.

### ★ Recommended equilibrium concept: Individual Optimality (IO)
**Justification:** There is no strategic interaction in the baseline model — C_U and C_R solve independent problems, and the wage function w(e, θ) is taken as given (competitive labor market). Individual optimality is the correct concept. The model is a single-agent decision problem run parametrically in (θ, τ); the comparison across types is a comparative statics exercise, not an equilibrium selection problem.

---

## 8. Social Planner Benchmarks

### First-Best (No hukou constraint)
The planner sets δ = 1 and p(e) = 1 for all e (no penalty, no escape needed) and solves for both children identically:

  max_{e} w(e, θ)/r − C(e)

First-order condition: w_e(e^FB, θ)/r = C'(e^FB)

Both children invest e^FB(θ) regardless of hukou status. The first-best investment level is the same for all agents with the same θ.

**Welfare at first-best:** W^FB(θ) = w(e^FB, θ)/r − C(e^FB) for each child.

### Second-Best (Hukou constraint in place, planner chooses e subject to existing labor market segmentation)
With hukou constraint active (δ < 1, escape route available), the planner takes the segmented wage function as given and maximizes aggregate payoff:

  max_{e_U, e_R} [V_U(e_U; θ) + V_R(e_R; θ)]

Since the problems are separable, the constrained planner's solution coincides with the private equilibrium: e*_U = e^FB(θ) and e*_R = argmax V_R(e_R; θ). The constrained efficiency loss is:

  ΔW(θ, δ) = V_U(e^FB, θ) − V_R(e*_R, θ)

which decomposes into the return-channel loss (due to δ < 1) and, if applicable, the escape-route distortion (over-investment cost for high-θ rural children).

---

## 9. Internal Consistency Check

| Check | Status | Notes |
|-------|--------|-------|
| All variables defined before use | ✓ | All symbols appear in Notation Summary below; domains specified |
| Equilibrium concept compatible with action/information space | ✓ | IO is correct for single-agent problems; no game-theoretic structure needed |
| Budget/resource constraints consistent across agents | ✓ | Constraints are per-agent and non-interacting; relaxed to non-binding in baseline |
| Timing internally consistent | ✓ | No agent conditions on future events; e is chosen before wages are realized |
| Model generates the tension from Stage 1 | ✓ | Urban FOC: w_e/r = C'; Rural FOC (e < ê): δ·w_e/r = C' → e*_R < e*_U for same θ. Rural FOC (e near ê): includes escape-route term, potentially reversing sign |
| Existence (preliminary) | ✓ | V_U and V_R are continuous; [0, ē] is compact; maxima exist by Weierstrass. Interior solutions exist under standard Inada conditions on w and C |
| Payoff consistency | ⚠️ | W_R has a potential discontinuity at e = ê if p(e) has a jump at ê (p(ê⁻) = 0, p(ê) = p₀ > 0). This must be handled: either (a) define p as left-continuous with p(ê⁻) = 0 and p(ê) = p₀ (discrete jump → comparison of corner vs. interior), or (b) smooth p near ê (p continuous, p'(ê) large). Both are tractable; (a) is cleaner for the escape-route proposition. |

**Outstanding issues:**
1. The discrete-jump specification of p(e) at ê (Option a) means V_R may be discontinuous at ê from the left, so the argmax may be at e = ê (a kink point) rather than at an interior FOC solution. Stage 5 (Assumption Audit) must specify which case is assumed and prove that the optimal solution is well-characterized.

---

## Notation Summary

| Symbol | Meaning | Domain |
|--------|---------|--------|
| θ | Innate ability | [θ_L, θ_H] ⊂ ℝ₊ |
| τ | Hukou registration status | {U, R} (urban, rural) |
| e | Education investment level | [0, ē] ⊂ ℝ₊ |
| ē | Maximum feasible education | ℝ₊₊ (exogenous) |
| w(e, θ) | Competitive urban wage function | ℝ₊; w_e > 0, w_θ > 0, w_{ee} < 0 |
| A | TFP parameter in wage function | ℝ₊₊ |
| α | Ability elasticity of wages | (0, 1) |
| β | Education elasticity of wages | (0, 1) |
| C(e) | Cost of education | ℝ₊; C' > 0, C'' > 0, C(0) = 0 |
| r | Opportunity cost of funds | ℝ₊₊ |
| δ | Hukou wage penalty (rural discount) | (0, 1); δ = 1 ↔ no penalty |
| ê | Escape-route education threshold | (0, ē) |
| p(e) | Escape-route access probability | [0,1]; p(e) = 0 for e < ê; p(ê) = p₀ > 0; p'(e) ≥ 0 for e ≥ ê |
| p₀ | Jump size at escape threshold | (0, 1] |
| W_R(e,θ) | Effective rural wage | [δ·w(e,θ), w(e,θ)]; equals δ·w for e < ê |
| V_U(e;θ) | Urban child net payoff | w(e,θ)/r − C(e) |
| V_R(e;θ) | Rural child net payoff | W_R(e,θ)/r − C(e) |
| e*_U(θ) | Urban child optimal investment | argmax V_U |
| e*_R(θ) | Rural child optimal investment | argmax V_R |
| Δe*(θ) | Investment gap (urban minus rural) | e*_U(θ) − e*_R(θ) |
| θ̄ | Ability threshold above which Δe* < 0 | To be characterized in Stage 6 |
| e^FB(θ) | First-best investment (no hukou) | argmax w(e,θ)/r − C(e) |
| ΔW(θ,δ) | Welfare loss due to hukou | V_U(e^FB,θ) − V_R(e*_R,θ) |

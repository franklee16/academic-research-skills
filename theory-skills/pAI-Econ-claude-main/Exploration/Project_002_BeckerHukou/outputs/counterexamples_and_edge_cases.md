# Counterexamples and Edge Cases

**Date:** 2026-06-14
**Stage:** 8 — Counterexample Finder

---

## Summary Table

| Proposition | Attempts | Breaks Found | Max Severity | Status |
|------------|---------|-------------|------------|--------|
| P_E1 | 6 | 2 (boundary) | LOW | CONDITIONAL |
| P_C1 | 5 | 1 (HIGH) + 1 (LOW) | HIGH | NEEDS FIX |
| P_C2 | 8 | 0 | — | ROBUST |
| P_C3 | 6 | 1 (MEDIUM) | MEDIUM | NEEDS FIX |
| P_W1 | 5 | 0 | — | ROBUST |
| P_W2 | 4 | 0 | — | ROBUST |
| P_B1 | 3 | 0 | — | ROBUST |

---

## [P_E1] — Counterexample Analysis

### Attempt 1: Two-Type Reduction
**Tried:** θ ∈ {θ_L, θ_H}, binary action space {0, ê}. Does a maximum exist and is it unique?
**Result:** SURVIVES — With finite action space, the maximum is attained at {0} or {ê} (no interior FOC needed). With continuous action space [0,ē] and two types, the argument goes through unchanged. Existence and uniqueness follow from strict concavity at each θ.

### Attempt 2: Extreme Parameter Values — β → 1
**Tried:** Wage function w = Aθ^αe^β with β → 1 (wages become approximately linear in e).
**Result:**
```
⚠️  BREAKS (boundary) — Extreme parameter value
Counterexample: β = 1. Then w(e,θ) = Aθ^αe. V_U(e;θ) = Aθ^α·e/r − C(e). V_U''(e) = w_{ee}/r − C'' = 0 − C''(e) < 0 — wait, V_U'' = −C''(e) < 0, so V_U is still strictly concave if C'' > 0. However, the FOC becomes Aθ^α/r = C'(e*_U), which has a unique solution. P_E1 SURVIVES for β = 1 if C'' > 0.
```
Re-evaluation: **SURVIVES** — The strict concavity of V_U = w/r − C requires w_{ee} < 0 OR C'' > 0 (or both). For β = 1, w_{ee} = 0, but C'' > 0 (A6) is sufficient. P_E1's concavity argument relies on C'' > 0 alone being sufficient. Mark as SURVIVES.

### Attempt 3: Relaxing A6 — C Affine
**Tried:** Replace A6 (C strictly convex) with C(e) = c·e (linear cost, C'' = 0).
**Result:**
```
⚠️  BREAKS (uniqueness part) — Assumption relaxation
Counterexample: C(e) = c·e, w = Aθ^αe^β (β < 1). V_U''(e) = β(β−1)Aθ^αe^{β−2}/r < 0 — still strictly concave in e. Actually V_U is strictly concave because w_{ee} < 0 even if C'' = 0.
```
Re-evaluation: **SURVIVES** — For Cobb-Douglas w with β < 1, w_{ee} < 0 is sufficient for strict concavity of V_U even when C'' = 0. A6 (C strictly convex) is only needed to ensure the FOC is strictly decreasing when w_{ee} is not sufficient.

### Attempt 4: Corner Solution — Inada Condition Failure
**Tried:** Suppose C'(0) > 0 (positive marginal cost at zero). Then as e → 0, V_U'(e) = w_e/r − C'(e) = +∞ − C'(0) → could still be positive. But suppose C'(0) > lim_{e→0} w_e(e,θ)/r for some θ.
**Result:**
```
⚠️  BREAKS (interior characterization) — Corner solution
Counterexample: If C'(0) > βAθ_L^α · 0^{β−1}/r (which is +∞ as e → 0 for β < 1, so this doesn't bind under Cobb-Douglas). 
But if ē is very small: if C'(ē) < w_e(ē,θ)/r, then e*_U = ē (upper corner). The interior FOC characterization in P_E1 does not cover this.
```
**Severity:** LOW (boundary case; fix is to add a parameter condition)
**Fix options:**
  Option A: Add Inada-type assumption: ∃ θ_L, θ_H such that for all θ ∈ [θ_L, θ_H]: C'(ē) > w_e(ē,θ)/r (interior solution exists strictly below ē). [This is the condition A18 / Inada condition noted in Gate 4]

### Attempt 5: Degenerate Distribution (Homogeneous Types)
**Tried:** All children have the same type θ_0. Does P_E1 hold?
**Result:** SURVIVES — P_E1 is a statement about a single agent's optimization given θ; it makes no distributional assumption. Works for any fixed θ.

### Attempt 6: Existence Failure for Rural Child's Two-Regime Problem
**Tried:** What if V_R^{high}(ê; θ) > V_R^{low}(e*_int; θ) is violated for all θ (i.e., rural child always prefers the interior low solution to the escape route)? Is e*_R still well-defined?
**Result:** SURVIVES — The two-regime comparison is always well-defined: e*_R = argmax{V_R^{low}(e*_int;θ), V_R^{high}(ê;θ)}. Both regime optima exist by steps 3 and 6 of P_E1 proof sketch. Even if V_R^{high}(ê) < V_R^{low}(e*_int) for all θ, e*_R = e*_int is well-defined.

**P_E1 Overall verdict:** CONDITIONAL (survives all attempts except the corner-solution edge case at upper boundary ē, which requires an explicit Inada condition on C)

---

## [P_C1] — Counterexample Analysis

### Attempt 1: Two-Type Reduction
**Tried:** Two types θ_L < θ_H, single period, multiplicative penalty δ. For each type, is e*_int(θ) < e*_U(θ)?
**Result:** SURVIVES — The single-crossing argument works at each fixed θ independently of the type distribution.

### Attempt 2: Relaxing A7 — Additive Penalty

```
⚠️  BREAKS (HIGH) — Assumption relaxation
Counterexample: Replace W_R(e,θ) = δ·w(e,θ) with W_R(e,θ) = w(e,θ) − d for e < ê (additive wage penalty d > 0).
What fails: The FOC for the rural child in the low regime becomes w_e(e,θ)/r = C'(e) — identical to the urban FOC. Hence e*_int(θ; additive) = e*_U(θ) for all θ. The investment gap Δe*(θ) = 0 for all θ in the under-investment regime.
Severity: HIGH — The core under-investment result fails entirely under the additive formulation.
Fix options:
  Option A: Keep A7 (multiplicative penalty) as a BINDING assumption; add explicitly to P_C1 statement: "Under the multiplicative penalty specification (A7)..."
  Option B: P_C1 can be restated as: "The under-investment result is special to multiplicative penalties; additive penalties generate zero investment distortion in the low regime." Convert this to a comparative remark rather than a standalone proposition.
```

**Note:** This break is already anticipated in the assumption audit (A7 labeled BINDING). What is new here is the explicit confirmation: additive penalty is not merely an alternative — it is a proposition-killing alternative for P_C1.

### Attempt 3: Extreme Parameter — δ → 0
**Tried:** δ → 0: the rural wage in the low regime → 0. Does e*_int → 0? Does P_C1 still hold?
**Result:** SURVIVES — As δ → 0: the rural child's low-regime problem becomes max [0·w(e)/r − C(e)], with solution e*_int = 0 (since −C(e) is maximized at e = 0 given C is increasing). And e*_U > 0 (assuming interior solution). So e*_int = 0 < e*_U. The under-investment result holds maximally. This is the limit P_B1(iii).

### Attempt 4: Corner Solution — e*_int = 0
**Tried:** What if δ is very small and θ is very small, so e*_int = 0? Is the proposition still meaningful?
**Result:**
```
⚠️  BREAKS (LOW) — Corner solution
Counterexample: For sufficiently small δ·θ, the FOC δ·w_e(e,θ)/r = C'(e) has solution e*_int = 0 (corner, if the FOC is violated at all interior points). At e = 0: C'(0) = 0, but w_e(0,θ) = βAθ^α·0^{β−1} = +∞ → FOC cannot be satisfied at 0 → still forces interior solution.
Re-evaluation: Under Cobb-Douglas with β < 1, lim_{e→0} w_e(e,θ) = +∞ for all θ > 0 (Inada). So e*_int > 0 always as long as θ > 0. Corner solution at e*_int = 0 requires either θ = 0 (degenerate) or Inada fails.
```
**Re-evaluation:** SURVIVES under Cobb-Douglas — The Inada-like property of Cobb-Douglas wages (marginal product → ∞ at e = 0) ensures e*_int > 0 for any θ > 0 and any δ > 0. Corner at e = 0 only at θ = 0 (boundary of type space).

### Attempt 5: Strategic Manipulation
**Tried:** Can the rural child manipulate her way into the "urban" wage classification by choosing e ≥ ê even when it's not optimal?
**Result:** SURVIVES — In the IO equilibrium, the rural child maximizes her own payoff. If she chooses e ≥ ê for strategic reasons (e.g., to influence the wage function), this is ruled out by the IO solution concept (she is already optimizing her own payoff, which includes the escape route benefit). There is no additional manipulation possible within the IO framework.

**P_C1 Overall verdict:** NEEDS FIX — Breaks under additive penalty (HIGH severity). Fix: explicitly restrict the proposition to multiplicative penalty (A7) and add a remark that the additive-penalty model yields zero investment distortion in the low regime.

---

## [P_C2] — Counterexample Analysis

### Attempt 1: Two-Type Reduction
**Tried:** Two types: θ_L < θ_H = θ̄ (so e*_U(θ_H) = ê). Rural child at θ_H: does e*_R = ê?
**Result:** SURVIVES — At θ = θ_H, the condition for over-investment is F(θ_H) = V_R^{high}(ê;θ_H) − V_R^{low}(e*_int;θ_H) > 0, which requires p₀ ≥ p₀*(δ, ê, θ_H). For p₀ large enough, this holds. The two-type case captures the essence of the claim.

### Attempt 2: Relaxing A7 — Additive Penalty
**Tried:** Replace multiplicative penalty with additive: W_R = w − d for e < ê.
**Result:** SURVIVES — As established in the P_C1 adversarial check: with additive penalty, e*_int = e*_U. Then F(θ) = V_U(ê;θ) − V_U(e*_U;θ) + d/r. At θ = θ̄ (where e*_U(θ̄) = ê): F(θ̄) = 0 + d/r = d/r > 0. By continuity, ∃ θ̃ < θ̄ with F(θ̃) = 0. So P_C2 **holds under additive penalty** as well. The escape-route over-investment mechanism is more robust than P_C1.

**Implication:** P_C2 is NOT contingent on A7 (multiplicative penalty). The key assumption is A9 (discrete jump in p at ê) and A17 (p₀ > 0). This robustness should be noted explicitly in the paper — the headline result holds under either penalty specification.

### Attempt 3: p₀ → 0 (No Escape Route Benefit)
**Tried:** p₀ → 0: the escape probability at ê goes to zero.
**Result:** SURVIVES (degenerates gracefully) — As p₀ → 0, the escape premium (1−δ)p₀·w(ê,θ)/r → 0 and p₀* → 0 as well (the threshold also falls to 0 from above). The over-investment range (θ̃, θ̄) → ∅ (collapses to a single point). The proposition's sufficient condition p₀ ≥ p₀* is satisfied vacuously at p₀ = 0 = p₀*(0,...), but the range is empty. This is the limit P_B1(ii): the claim is vacuously true with an empty over-investment interval. The proposition correctly requires p₀ > 0 as a non-trivial condition.

### Attempt 4: δ → 1 (Hukou Removed Before Reform)
**Tried:** δ → 1 with fixed p₀ > 0.
**Result:** SURVIVES (degenerates gracefully) — As δ → 1: (1−δ)p₀·w(ê,θ)/r → 0, so the escape premium → 0. The threshold p₀*(δ,ê,θ̄) → ∞ (since the denominator (1−δ)·w → 0 but the numerator stays positive). For fixed p₀ < ∞, p₀ < p₀* → over-investment range collapses. Consistent with the proposition's sufficient condition: for δ close to 1, the condition p₀ ≥ p₀* fails for any finite p₀. The claim is vacuously true with empty interval. Graceful.

### Attempt 5: ê → ē (Elite Threshold at Maximum)
**Tried:** ê → ē (the elite university threshold equals the maximum feasible investment).
**Result:** SURVIVES — As ê → ē: the over-investment threshold θ̄ satisfies e*_U(θ̄) = ê → ē. For θ < θ̄: e*_U(θ) < ē = ê. The over-investment range (θ̃, θ̄) is still non-empty as long as F(θ̄) > 0 (requires p₀ ≥ p₀*(δ, ē, θ̄)). Since ê = ē is in the model's action space [0, ē], this is a valid limit. However, the rural child faces the maximum possible investment — empirically, ê → ē may be implausible (Gaokao threshold is well below maximum educational investment). This is an EDGE CASE to discuss.

### Attempt 6: Continuous p(e) — Removing A9
**Tried:** Replace discrete jump A9 with p(e) smooth and strictly increasing for e ≥ ê.
**Result:** SURVIVES (with modification) — With smooth p(e) increasing from 0 at ê to p₀ at ê+ε: the payoff V_R is now smooth (no jump at ê). The over-investment result still holds but the mechanism changes: the rural child now has a smooth upward-sloping marginal benefit in [ê, ē] from the increasing escape probability. The corner solution at ê may or may not be the optimum — it depends on whether V_R^{high}'(ê) > 0. If p'(ê) > 0 (smooth), the rural child may invest e > ê. The proposition should be refined: "e*_R ≥ ê > e*_U" rather than "e*_R = ê exactly" for smooth p. The strict over-investment remains, but the investment level is ê (corner) only in the discrete-jump case.

**Severity:** LOW — The direction of the effect is unchanged; only the exact level of over-investment changes from ê to some e*_R > e*_U.

### Attempt 7: Existence Failure — p₀ < p₀*
**Tried:** Parameterize so that p₀ < p₀*(δ, ê, θ̄). Does the proposition claim existence that fails?
**Result:** SURVIVES — The proposition correctly includes the sufficient condition p₀ ≥ p₀* as part of the claim statement. When p₀ < p₀*, the proposition's conclusion does not apply (no over-investment range). This is NOT a break of the proposition — it is a correctly bounded claim.

### Attempt 8: Multiple Escape Thresholds
**Tried:** Suppose there are two elite thresholds ê₁ < ê₂, each with its own escape probability p₀₁ and p₀₂. Does P_C2 still hold?
**Result:** INCONCLUSIVE — With two thresholds, the rural child has a three-regime problem. Each threshold generates its own potential over-investment incentive. P_C2 as stated applies to a single threshold. An extension to multiple thresholds is possible but requires re-deriving the comparison conditions. Not a break of the existing claim; an extension question.

**P_C2 Overall verdict:** ROBUST — No break found under any attack. The proposition is robust to: additive vs. multiplicative penalty; removal of p₀; degenerate limits; continuous p(e); existence conditions. The only refinement needed is for the continuous-p case (investment is ≥ ê rather than exactly = ê).

---

## [P_C3] — Counterexample Analysis

### Attempt 1: Two-Type Reduction
**Tried:** Comparative statics with two discrete types. Does ∂Δe*/∂δ < 0 hold?
**Result:** SURVIVES — In the two-type case, we can compute e*_int(θ;δ) and e*_U(θ) explicitly for each θ ∈ {θ_L, θ_H} and verify that increasing δ reduces the gap at each type. The IFT argument works at each fixed θ.

### Attempt 2: Sign of ∂θ̃/∂δ — Parameter Dependence

```
⚠️  BREAKS (MEDIUM) — FALSE_RISK confirmed as an actual break
Counterexample: Take δ close to 1 (mild hukou), p₀ small, and e*_int close to ê. Then (1−p₀)·ê^β − (e*_int)^β is small, and the sign of ∂F/∂δ is uncertain. Specifically:
- If ê/e*_int ≤ (1−p₀)^{−1/β}: ∂F/∂δ ≤ 0 → ∂θ̃/∂δ ≥ 0 (stricter hukou shrinks the over-investment range).
- If ê/e*_int > (1−p₀)^{−1/β}: ∂F/∂δ > 0 → ∂θ̃/∂δ < 0 (stricter hukou expands the over-investment range).
What fails: The claim that the over-investment range width θ̄ − θ̃ is monotone in δ is FALSE in general; it depends on the ratio ê/e*_int relative to (1−p₀)^{−1/β}.
Severity: MEDIUM — P_C3(iii) as stated requires revision. Parts (i) and (ii) are unaffected.
Fix options:
  Option A: State P_C3(iii) as a CONDITIONAL result: "When ê/e*_int(θ̃) > (1−p₀)^{−1/β}, the over-investment range expands as δ decreases (hukou tightens). The condition holds in the empirically relevant case where ê >> e*_int (large gap between urban and rural schooling levels)."
  Option B: Drop P_C3(iii) from the main proposition list; move to a Remark ("the effect of δ on the over-investment range width depends on the ratio of elite to interior investment levels").
  Option C: Restrict to δ close to 0 (tight hukou regime): in this range, ê >> e*_int and the condition ê/e*_int > (1−p₀)^{−1/β} holds, so ∂θ̃/∂δ < 0 is guaranteed.
```

### Attempt 3: Extreme Parameter — β → 0 (Investment Barely Matters)
**Tried:** β → 0: wages become approximately independent of education (only ability matters). Does comparative statics still hold?
**Result:** SURVIVES (degenerates gracefully) — As β → 0: w(e,θ) → Aθ^α (flat in e). Then w_e → 0 for all e. The FOC δ·w_e/r = C' becomes 0 = C'(e*_int), which forces e*_int = 0 (since C'(0) = 0 by Inada). Similarly e*_U → 0. All investment goes to zero and the gap Δe* → 0. P_C3(i) says ∂Δe*/∂δ < 0; in the limit Δe* = 0 for all δ, so ∂Δe*/∂δ = 0. The result holds weakly (= 0) at the boundary. Not a proper break.

### Attempt 4: Degenerate p — p₀ = 1 (Certain Escape)
**Tried:** p₀ = 1: reaching ê guarantees urban status with certainty.
**Result:** SURVIVES — With p₀ = 1: p₀*(δ, ê, θ̄) = [V_R^{low}(e*_int;θ̄) − V_R^{low}(ê;θ̄)] / [(1−δ)·w(ê,θ̄)/r]. At p₀ = 1 ≥ p₀*, the sufficient condition is easily satisfied. P_C3(ii) says θ̄ − θ̃ is increasing in p₀; at the maximum p₀ = 1, the over-investment range is widest. Consistent.

### Attempt 5: Alternative Equilibrium — No IO Assumption
**Tried:** Suppose both rural children observe each other's investment and play a Nash equilibrium. Can competitive investment-as-signaling destroy P_C3?
**Result:** SURVIVES (condition) — This is outside the model's scope (IO equilibrium with no strategic interaction between rural children). A13 rules out signaling; since there are only two agents (τ = U and τ = R), and they do not interact strategically, this is not applicable within the model. In a macro version with a continuum of rural children, aggregate investment patterns may feed back through labor demand, potentially altering wages — but this is a general equilibrium extension outside the model's scope.

### Attempt 6: Non-Monotone e*_U in θ
**Tried:** Can e*_U(θ) be non-monotone in θ if w_{eθ} < 0 for some e?
**Result:**
```
⚠️  BREAKS (MEDIUM) — Assumption on w structure
Counterexample: If w(e,θ) = Aθ^α·e^β − B(θ)·e^γ with B'(θ) > 0 (higher ability leads to lower return at high education levels), then w_{eθ} could be negative at some e. This would make e*_U(θ) non-monotone, destroying the existence of θ̄ (the ability at which e*_U(θ̄) = ê).
What fails: θ̄ need not exist or be unique; P_C2 and hence P_C3(ii) lose their foundation.
Severity: MEDIUM — The result depends critically on w_{eθ} > 0 everywhere (supermodularity of w in e and θ).
Fix options:
  Option A: Add supermodularity of w as explicit maintained assumption A_SM: w_{eθ}(e,θ) > 0 for all (e,θ). Under Cobb-Douglas, this holds: w_{eθ} = αβAθ^{α−1}e^{β−1} > 0. State this as a binding assumption.
```

**P_C3 Overall verdict:** NEEDS FIX — Two issues: (1) P_C3(iii) sign of ∂θ̃/∂δ is parameter-dependent (revise to conditional claim); (2) θ̄ existence requires supermodularity of w (add as explicit assumption A_SM).

---

## [P_W1] — Counterexample Analysis

### Attempt 1: ΔW < 0 — Can Welfare Loss Be Negative?
**Tried:** Is there any scenario where the rural child is better off than the urban child (ΔW < 0)?
**Result:** SURVIVES — V_U(e^{FB};θ) = max_e [w(e,θ)/r − C(e)]. V_R(e*_R;θ) = max_e [W_R(e,θ)/r − C(e)] ≤ max_e [w(e,θ)/r − C(e)] = V_U(e^{FB};θ), since W_R(e,θ) ≤ w(e,θ) for all e (because δ+(1−δ)p(e) ≤ 1 for all e when p(e) ≤ 1). Therefore ΔW ≥ 0 always. Equality (ΔW = 0) only when p₀ = 1 AND δ = 1 (no penalty, certain escape). This result is fully rigorous and requires only A7 and p₀ ≤ 1.

### Attempt 2: Non-Monotone ΔW — Does ΔW Always Have a Local Max Near θ̃?
**Tried:** Is it possible for ΔW to be strictly monotone in θ (no local max)?
**Result:** SURVIVES (with clarification) — ΔW(θ) exhibits a local maximum near θ̃ because of the payoff jump at θ̃: just below θ̃, rural child invests e*_int < ê with increasing ΔW(θ) (P_W1, step 4); just above θ̃, rural child switches to e = ê (a discrete jump), immediately reducing the welfare loss because the escape route provides positive value. The "local max" is actually a left-hand limit (ΔW is right-discontinuous at θ̃ in the discrete-jump p(e) case). With smooth p(e), the jump is smoothed out but the local maximum still exists by continuity. This is a correct characterization of the non-monotone profile.

### Attempt 3: ΔW Increasing Everywhere (No Non-Monotonicity)
**Tried:** Can ΔW(θ) be strictly increasing in θ everywhere, with no local maximum?
**Result:** SURVIVES (claim holds) — ΔW is NOT monotone: for θ > θ̄ (high regime), ΔW has coefficient [1 − (δ+(1−δ)p₀)] > 0 but smaller than [1−δ] in the low regime. So the slope of ΔW in the high regime is smaller than in the low regime. Whether there is a local max or only a slope change depends on the discontinuity at θ̃. The non-monotone profile (slope change, not necessarily a strict local max) is correctly documented.

### Attempt 4: Additive Penalty — Does ΔW Change Sign?
**Tried:** With additive penalty d: ΔW = V_U(e^{FB};θ) − V_R(e*_R;θ). Is ΔW > 0?
**Result:** SURVIVES — Same argument: V_R^{additive}(e;θ) = V_U(e;θ) − d/r (for e < ê). So max V_R^{additive,low} = max V_U − d/r = V_U(e*_U;θ) − d/r. V_R(e*_R;θ) ≤ max{V_U(e*_U;θ) − d/r, V_U(ê;θ)} ≤ V_U(e*_U;θ). So ΔW ≥ 0 even with additive penalty.

### Attempt 5: Degenerate p — p₀ = 0 Everywhere
**Tried:** p₀ = 0: no escape route. Does ΔW simplify?
**Result:** SURVIVES — With p₀ = 0: V_R = δ·w(e*_int)/r − C(e*_int). ΔW = V_U(e^{FB}) − V_R(e*_int). Positive since δ < 1 and e*_int < e^{FB} (P_C1 under-investment). This is the Arrow (1973) welfare loss, which is well-known to be positive.

**P_W1 Overall verdict:** ROBUST — ΔW > 0 is fully rigorous and holds under all parameter variations. The non-monotone θ-profile is correctly characterized under the discrete-jump specification.

---

## [P_W2] — Counterexample Analysis

### Attempt 1: Reform Does Not Eliminate Welfare Loss
**Tried:** Does δ → 1 always eliminate ΔW? What if p(e) ≡ 0 for all e (no escape route even post-reform)?
**Result:** SURVIVES — Post-reform δ = 1: W_R(e,θ) = [1+(1−1)p(e)]·w(e,θ) = w(e,θ). Regardless of p(e), the rural child's effective wage equals the urban wage. Welfare loss disappears by definition.

### Attempt 2: Can the Reform INCREASE Investment for θ ∈ (θ̃, θ̄)?
**Tried:** Can the pre-reform rural child be investing less than e*_U(θ) in the over-investment range (making P_W2(iii) vacuously correct with no investment reduction)?
**Result:** SURVIVES — In the over-investment range (θ̃, θ̄), P_C2 establishes e*_R(θ) = ê > e*_U(θ) (rural child over-invests). Post-reform: e*_R(θ; δ=1) = e*_U(θ) < ê. Reform strictly reduces investment. P_C2 is the foundation for P_W2(iii); given P_C2 holds, P_W2(iii) is immediate.

### Attempt 3: Can Welfare Fall Post-Reform?
**Tried:** Is it possible that hukou reform (δ → 1) reduces welfare for some θ?
**Result:** SURVIVES — Pre-reform welfare: V_R(e*_R; θ, δ*) = max_e W_R(e;δ*)/r − C(e) ≤ max_e w(e;1)/r − C(e) = V_R(e*_R; θ, 1) [post-reform welfare]. Since W_R(e;δ) ≤ w(e;1) for any δ < 1 and the maximum over e can only increase when the objective function increases, post-reform welfare is always weakly higher. Welfare cannot fall post-reform.

### Attempt 4: Extreme Parameter — δ = 0 (Complete Exclusion)
**Tried:** δ = 0: rural child earns zero wage unless they escape. Does P_W2 apply?
**Result:** SURVIVES — With δ = 0: W_R(e;0) = p(e)·w(e,θ) for e ≥ ê, and 0 for e < ê. All rural children invest exactly ê (assuming p₀ > 0) or invest 0 (if p₀ too small to justify cost). Post-reform δ = 1: all rural children invest e*_U(θ), which is less than ê for θ < θ̄. P_W2 still holds (reform reduces investment for θ < θ̄ and improves welfare).

**P_W2 Overall verdict:** ROBUST — The proof is essentially watertight given P_C2. No counterexample found.

---

## [P_B1] — Counterexample Analysis

### Attempt 1: Continuity in δ Fails
**Tried:** Can e*_int(θ;δ) be discontinuous in δ at some interior point?
**Result:** SURVIVES — By the IFT on δ·w_e(e,θ)/r = C'(e): since the LHS and RHS are both C¹ functions and the denominator of the IFT expression (C'' − δ·w_{ee}/r) ≠ 0 at any interior solution, e*_int(θ;δ) is C¹ in δ (and hence continuous). No discontinuity is possible in the interior.

### Attempt 2: p₀ → 0 Limit — Does (θ̃, θ̄) Collapse Correctly?
**Tried:** Verify that as p₀ → 0, the interval (θ̃, θ̄) collapses to ∅.
**Result:** SURVIVES — F(θ̃; p₀) = 0 and F(θ̄; p₀) = [V_R^{low}(e*_int;θ̄) − V_R^{low}(ê;θ̄)] (negative) + (1−δ)p₀·w(ê,θ̄)/r. As p₀ → 0: F(θ̄) → [negative term] < 0. The indifference condition F(θ̃) = 0 requires θ̃ → θ̄ (since F is negative everywhere when p₀ = 0, there is no θ with F = 0 except at the limit). The interval collapses to ∅.

### Attempt 3: δ → 0 — Does e*_int Really → 0?
**Tried:** Verify e*_int → 0 as δ → 0 under Cobb-Douglas.
**Result:** SURVIVES — e*_int satisfies δ·βAθ^α·(e*_int)^{β−1}/r = C'(e*_int). As δ → 0: LHS → 0 for any fixed e*_int > 0 (while RHS remains positive). The only way for equilibrium to hold is e*_int → 0 (so both sides approach 0 simultaneously by Inada conditions on C). Confirmed.

**P_B1 Overall verdict:** ROBUST — All three limit results hold rigorously.

---

## Consolidated Fixes Required

| # | Counterexample | Affected Proposition | Recommended Fix | Fix Type |
|---|---------------|---------------------|----------------|---------|
| CE1 | Additive penalty: P_C1 FOC equals urban FOC → Δe* = 0 | P_C1 | Add "under multiplicative penalty (A7)" explicitly to P_C1 statement; add Remark noting additive penalty gives zero distortion in low regime | CLAIM SCOPE |
| CE2 | P_C3(iii): sign of ∂θ̃/∂δ is parameter-dependent (breaks for ê/e*_int ≤ (1−p₀)^{−1/β}) | P_C3 | Revise P_C3(iii) to conditional statement: "when ê >> e*_int, stricter hukou expands the over-investment range"; OR drop to a Remark | CLAIM REVISION |
| CE3 | Non-monotone e*_U(θ) if w_{eθ} < 0 at some (e,θ) → θ̄ may not exist | P_C2, P_C3 | Add supermodularity assumption A_SM: w_{eθ}(e,θ) > 0 for all (e,θ) | ASSUMPTION |
| CE4 | Corner solution at ē: if C'(ē) < w_e(ē,θ)/r, interior P_E1 characterization fails | P_E1 | Add Inada upper bound on C (already flagged as A18 in Gate 4) | ASSUMPTION |

---

## Edge Cases to Document in the Paper

| # | Edge Case | Proposition | How to Handle |
|---|-----------|------------|--------------|
| EC1 | P_C2 holds under ADDITIVE penalty (more robust than assumed) | P_C2 | Add Remark: "The over-investment result does not require multiplicative penalties; it holds as long as the escape route generates a discrete payoff jump at ê." |
| EC2 | Over-investment range collapses when p₀ → 0 or δ → 1 | P_C2 | Explicitly state these boundary conditions in the proposition; treat as limits (P_B1) |
| EC3 | Smooth p(e) vs. discrete jump: investment level is ê (exactly) only in the discrete-jump case; with smooth p(e), investment is ≥ ê | P_C2 | Add a Remark: "Under a continuous escape-probability schedule p(e) increasing from 0, rural children invest e*_R > ê (above the elite threshold) rather than exactly at ê. The main result (over-investment relative to urban child) still holds; the discrete specification is a simplification." |
| EC4 | Welfare loss ΔW at the boundary θ̃ has a discrete jump (discontinuity in θ) | P_W1 | State in paper: "the welfare profile has a downward jump at θ̃ due to the discrete escape probability; this jump is an artifact of the discrete p(e) specification and disappears with smooth p(e)." |
| EC5 | Multiple escape thresholds (ê₁ < ê₂) — extension question | P_C2, P_C3 | Note in the conclusion as a direction for future work; do not incorporate into the main model. |
| EC6 | General equilibrium feedback: if enough rural children invest at ê, urban-rural wage differential may adjust endogenously | All | The model is partial equilibrium (A3); acknowledge as a maintained assumption and note that GE extensions are outside scope. |

---

## Robustness Summary

**Overall robustness assessment:** MODERATE-STRONG

The headline propositions (P_C2, P_W1, P_W2, P_B1) are robust — no adversarial construction broke them. The most vulnerable result is **P_C1** (under-investment benchmark), which fails entirely under additive penalties; this was already flagged in the assumption audit but is now formally confirmed as a proposition-killing construction. Four targeted fixes are required: (i) scope P_C1 to multiplicative penalties explicitly; (ii) revise P_C3(iii) to a conditional claim; (iii) add supermodularity (A_SM) as an explicit assumption; (iv) add the Inada upper bound on C (A18). Critically, **P_C2's robustness to additive penalties** is an unexpected positive finding — the escape-route over-investment mechanism is more general than the proof strategy required, strengthening the paper's claims against referee objections.

# Proof Sketches

**Date:** 2026-06-14
**Stage:** 7 — Proof Sketches

---

## [P_E1] — Proof Sketch: Existence and Characterization

**Claim (restated):**
> Under Assumptions A1, A3, A5, A6, A9: (i) e*_U(θ) is the unique interior solution to β·A·θ^α·(e*_U)^{β−1}/r = C'(e*_U). (ii) e*_R(θ) = argmax over two regimes, characterized by direct payoff comparison of V_R^{low} and V_R^{high} optima.

**Proof strategy:** Weierstrass maximum theorem for existence; strict concavity for uniqueness within each regime.

**Proof sketch:**

1. **Continuity of payoff functions** [SOLID]
   V_U(e; θ) = w(e,θ)/r − C(e) is continuous on [0, ē]: w = Aθ^αe^β is continuous; C is continuous by A6. Same for V_R^{low} and V_R^{high} on their respective domains. [A5, A6]

2. **Compactness of action space** [SOLID]
   [0, ē] is compact. Each regime domain [0, ê) and [ê, ē] is bounded, and the closure [0, ê] is compact.

3. **Existence by Weierstrass** [SOLID] [CITE: Weierstrass / Berge Maximum Theorem]
   A continuous function on a compact set attains its maximum. Hence e*_U exists on [0, ē]; e*_R,low exists on [0, ê]; e*_R,high exists on [ê, ē].

4. **Strict concavity of V_U** [SOLID]
   V_U''(e) = w_{ee}/r − C''(e). Since w_{ee} = β(β−1)Aθ^αe^{β−2} < 0 (β < 1) and C'' > 0 (A6), V_U'' < 0. Hence V_U is strictly concave → unique interior maximizer e*_U characterized by the FOC: β·A·θ^α·(e*_U)^{β−1}/r = C'(e*_U).

5. **Existence of interior solution (Inada condition)** [PLAUSIBLE]
   As e → 0: w_e/r = βAθ^α·e^{β−1}/r → +∞ (since β−1 < 0); and C'(0) = 0 (assuming C'(0) = 0 or C'(0) < +∞ with C'(0) < lim w_e/r). As e → ē: assume C'(ē) > w_e(ē,θ)/r. By IVT on FOC, an interior solution exists. [A8]

6. **Rural child's two-regime problem** [SOLID]
   V_R^{low} is strictly concave on [0, ê) (same argument as step 4 with δ < 1 rescaling); unique maximizer e*_int(θ) or corner at ê if the unconstrained optimum exceeds ê. V_R^{high} is strictly concave on [ê, ē] when p(e) = p₀ (constant) since [δ+(1−δ)p₀] < 1 gives same concavity argument. [A7, A9]

7. **Global optimum via payoff comparison** [SOLID]
   e*_R(θ) = argmax{V_R^{low}(e*_int, θ), V_R^{high}(e*_high, θ)}. Both candidates exist by steps 3–6. The global maximizer is the one with higher value; tie-broken by choosing ê (Lemma H1). [A9, H1]

**Additional lemmas needed:**
- **Lemma on e*_U monotonicity:** e*_U(θ) is strictly increasing in θ [needed for P_C2; follows from supermodularity w_{eθ} > 0 and IFT on FOC].
- **Lemma H1 (Tie-breaking):** Stated as assumption; no proof required.

**Hardest step:** Step 5 — the Inada condition requires careful parameter specification; formally, need C'(ē) > βAθ_H^α·ē^{β−1}/r for the interior solution to exist within [0, ē].

**Rigor summary:** MOSTLY SOLID
**To complete:** Verify step 5 formally; state Inada conditions on C explicitly.

---

## [P_C1] — Proof Sketch: Under-Investment Benchmark

**Claim (restated):**
> Under A1, A3, A5–A7, A10, A13, A16: if e*_R(θ) < ê, then e*_R(θ) < e*_U(θ) for all θ.

**Proof strategy:** Single-crossing argument comparing FOCs.

**Proof sketch:**

1. **Urban FOC at e*_U** [SOLID]
   e*_U satisfies: w_e(e*_U, θ)/r = C'(e*_U). [A5, A6]

2. **Rural (low-regime) FOC at e*_int = e*_R** [SOLID]
   e*_int satisfies: δ·w_e(e*_int, θ)/r = C'(e*_int). [A7]

3. **Urban marginal benefit at e*_int exceeds marginal cost** [SOLID]
   At e = e*_int: w_e(e*_int, θ)/r = C'(e*_int)/δ > C'(e*_int) since δ < 1 and C' > 0. So the urban child's marginal return exceeds marginal cost at e*_int → the urban child wishes to invest more than e*_int. [A7: δ < 1]

4. **Unique crossing + conclusion** [SOLID]
   Define g(e) = w_e(e,θ)/r − C'(e). g is strictly decreasing (w_{ee} < 0, C'' > 0). g(e*_U) = 0 by step 1. g(e*_int) = C'(e*_int)/δ − C'(e*_int) = C'(e*_int)·(1−δ)/δ > 0. Since g is strictly decreasing and g(e*_int) > 0 = g(e*_U), we have e*_int < e*_U. [A5, A6, A7]

5. **Remark on Arrow lineage** [SOLID]
   This result is the Becker-framework restatement of Arrow (1973, Theorem 1). The multiplicative penalty δ shifts the rural child's marginal benefit schedule down proportionally, giving a lower interior optimum. An additive penalty W_R = w − d would not affect the FOC, so e*_int = e*_U (no investment distortion). [A7: multiplicative is essential]

**Additional lemmas needed:** None beyond P_E1.

**Hardest step:** Step 3 is the key algebraic insight; the rest is immediate. No hard steps.

**Rigor summary:** NEAR-COMPLETE
**To complete:** None — this proof is essentially complete under the stated assumptions.

---

## [P_C2] — Proof Sketch: Escape-Route Over-Investment ★ HEADLINE

**Claim (restated):**
> Under all model assumptions and p₀ ≥ p₀*(δ, ê, θ̄), ∃ non-empty interval (θ̃, θ̄) such that for θ ∈ (θ̃, θ̄): e*_R(θ) = ê > e*_U(θ).

**Proof strategy:** (1) Define θ̄ via IVT on e*_U(θ). (2) Evaluate sign of F(θ) := V_R^{high}(ê; θ) − V_R^{low}(e*_int(θ); θ) at endpoints θ̄ and θ_L. (3) Apply IVT to define θ̃. (4) Show F is strictly increasing on (θ̃, θ̄) using Cobb-Douglas structure.

**Proof sketch:**

1. **θ̄ is well-defined** [PLAUSIBLE]
   e*_U(θ) is strictly increasing in θ: by IFT on FOC w_e(e*_U,θ)/r = C'(e*_U), differentiating: ∂e*_U/∂θ = −(w_{eθ}/r) / (w_{ee}/r − C'') = w_{eθ}/r / (C'' − w_{ee}/r) > 0 since w_{eθ} = αβAθ^{α−1}e^{β−1} > 0. So e*_U is strictly increasing. By IVT, ∃ unique θ̄ with e*_U(θ̄) = ê, provided ê ∈ (e*_U(θ_L), e*_U(θ_H)). [A5; requires parameter calibration that ê is in the range of e*_U]

2. **F is negative at θ_L** [PLAUSIBLE]
   F(θ) = [δ+(1−δ)p₀]·w(ê,θ)/r − C(ê) − [δ·w(e*_int,θ)/r − C(e*_int)]. As θ → 0: w(e,θ) → 0 for all e; both V_R^{high}(ê;θ) → −C(ê) and V_R^{low}(e*_int;θ) → −C(0) = 0 (since e*_int → 0 as θ → 0 and C(0) = 0). So F(θ) → −C(ê) < 0. Hence F(θ_L) < 0 for θ_L small enough. [A6: C(ê) > 0; requires θ_L small enough]

3. **F is positive at θ̄ when p₀ ≥ p₀*** [PLAUSIBLE]
   F(θ̄) = [V_R^{low}(ê; θ̄) − V_R^{low}(e*_int; θ̄)] + (1−δ)p₀·w(ê,θ̄)/r.
   The first bracketed term is strictly negative (V_R^{low} is strictly concave with max at e*_int < ê; so moving to ê decreases V_R^{low}). The second term is strictly positive. Define p₀* := [V_R^{low}(e*_int;θ̄) − V_R^{low}(ê;θ̄)] / [(1−δ)·w(ê,θ̄)/r] > 0. For p₀ > p₀*, F(θ̄) > 0. [A7, A9, A17: p₀ > 0; requires p₀ > p₀* which is an explicit sufficient condition]

4. **θ̃ < θ̄ exists by IVT** [SOLID]
   F is continuous in θ (V_R and e*_int(θ) are continuous). F(θ_L) < 0 and F(θ̄) > 0. By IVT, ∃ θ̃ ∈ (θ_L, θ̄) with F(θ̃) = 0. [Steps 2, 3]

5. **F is strictly increasing on (θ_L, θ̄) — single-crossing** [PLAUSIBLE]
   ∂F/∂θ = [δ+(1−δ)p₀]·w_θ(ê,θ)/r − δ·w_θ(e*_int,θ)/r [by envelope theorem: ∂V_R^{low}/∂θ|_{e=e*_int} = δ·w_θ(e*_int,θ)/r].
   With Cobb-Douglas: w_θ(e,θ) = αAθ^{α−1}e^β. So ∂F/∂θ proportional to [δ+(1−δ)p₀]·ê^β − δ·(e*_int)^β. Since ê > e*_int and [δ+(1−δ)p₀] > δ: both terms favor ê, so ∂F/∂θ > 0. [A5 (Cobb-Douglas); PLAUSIBLE under general w with w_{eθ} > 0 and ê > e*_int, but not fully general]

6. **Uniqueness of θ̃ and F > 0 on (θ̃, θ̄)** [PLAUSIBLE]
   Given step 5 (F strictly increasing), F has a unique zero at θ̃, and F(θ) > 0 for all θ ∈ (θ̃, θ̄). [Follows from strict monotonicity; PLAUSIBLE conditional on step 5]

7. **e*_R(θ) = ê for θ ∈ (θ̃, θ̄)** [SOLID given steps 4–6]
   F(θ) > 0 means V_R^{high}(ê; θ) > V_R^{low}(e*_int; θ) → rural child prefers high regime at ê. In the high regime (p₀ constant), e*_R,high(θ) = ê if e*_R,high,unconstrained < ê (which holds for θ < θ̄ since the high-regime coefficient [δ+(1−δ)p₀] < 1 < coefficient driving e*_U, and e*_U(θ) < ê for θ < θ̄). [PLAUSIBLE: need to verify that the high-regime unconstrained optimum is below ê for θ < θ̄]

8. **e*_U(θ) < ê for θ ∈ (θ̃, θ̄)** [SOLID]
   Since θ < θ̄ and e*_U is strictly increasing: e*_U(θ) < e*_U(θ̄) = ê. [Step 1]

9. **Conclusion: e*_R(θ) = ê > e*_U(θ) for θ ∈ (θ̃, θ̄)** [SOLID given steps 7–8]

**Additional lemmas needed:**
- **Lemma A (Monotonicity of e*_U):** e*_U is strictly increasing in θ. [SOLID by IFT; step 1]
- **Lemma B (Monotonicity of e*_int):** e*_int(θ) is strictly increasing in θ. [PLAUSIBLE by same IFT argument with δ scaling]
- **Lemma C (High-regime unconstrained optimum below ê for θ < θ̄):** When p(e) = p₀ constant, the high-regime unconstrained optimum e*_R,high(θ) satisfies [δ+(1−δ)p₀]·w_e(e*_R,high,θ)/r = C'(e*_R,high). Since [δ+(1−δ)p₀] < 1, by the same argument as P_C1: e*_R,high(θ) < e*_U(θ). So for θ < θ̄: e*_R,high(θ) < e*_U(θ) < ê → high-regime optimum is below ê → corner solution at ê. [PLAUSIBLE]

**Hardest step:** Step 5 — monotonicity of F in θ. Under general w (beyond Cobb-Douglas), ∂F/∂θ > 0 requires w_{eθ} > 0 (supermodularity of w in e and θ) and ê > e*_int. This is a maintained assumption (A5 plus the result of P_C1), but the formal verification requires showing ∂F/∂θ > 0 rigorously for general w satisfying the stated conditions. This is PLAUSIBLE but not proven in full generality.

**Rigor summary:** SKETCH
**To complete this proof, one would need to:**
- Verify step 5 (F strictly increasing) rigorously for general w satisfying w_{eθ} > 0, w_{ee} < 0
- Verify step 7 (high-regime corner at ê) using Lemma C
- State the parameter condition on ê (that ê is in the interior of the range of e*_U) explicitly
- Verify step 2 (F negative at θ_L) for a finite θ_L, not just the limit

---

## [P_C3] — Proof Sketch: Comparative Statics on the Investment Gap

**Claim (restated):**
> (i) In under-investment regime: ∂Δe*/∂δ < 0. (ii) Width of over-investment range θ̄ − θ̃ is increasing in p₀. (iii) Effect of δ on θ̃ is parameter-dependent. (iv) Aggregate gap is non-monotone in δ.

**Proof strategy:** Implicit function theorem applied to each FOC and to F(θ̃; δ, p₀) = 0.

**Proof sketch:**

1. **∂e*_int/∂δ > 0 [Part (i) numerator]** [SOLID]
   Differentiate δ·w_e(e*_int, θ)/r = C'(e*_int) implicitly w.r.t. δ:
   w_e(e*_int,θ)/r + δ·w_{ee}·(∂e*_int/∂δ)/r = C''·(∂e*_int/∂δ).
   → ∂e*_int/∂δ = (w_e/r) / (C'' − δ·w_{ee}/r) > 0 [numerator w_e > 0; denominator > 0 since C'' > 0, w_{ee} < 0]. [A5, A6, A7]

2. **e*_U is independent of δ** [SOLID]
   Urban child's FOC w_e(e*_U,θ)/r = C'(e*_U) does not involve δ → ∂e*_U/∂δ = 0. [A7 only applies to rural]

3. **∂Δe*/∂δ = −∂e*_int/∂δ < 0 [Part (i) conclusion]** [SOLID]
   Δe*(θ) = e*_U(θ) − e*_int(θ). ∂Δe*/∂δ = 0 − ∂e*_int/∂δ < 0 by step 1. So as δ increases (hukou relaxed), the gap shrinks. Conversely, as δ decreases (stricter hukou), the gap widens. [Steps 1, 2]

4. **∂θ̄/∂p₀ = 0 [Preparation for Part (ii)]** [SOLID]
   θ̄ defined by e*_U(θ̄) = ê. Since e*_U does not depend on p₀, θ̄ is independent of p₀.

5. **∂θ̃/∂p₀ < 0 [Part (ii) key step]** [SOLID]
   F(θ̃; p₀) = 0. By IFT: ∂θ̃/∂p₀ = −(∂F/∂p₀)/(∂F/∂θ).
   ∂F/∂p₀ = (1−δ)·w(ê,θ̃)/r > 0 [the escape premium increases in p₀].
   ∂F/∂θ > 0 [from P_C2, step 5].
   → ∂θ̃/∂p₀ = −positive/positive < 0. As p₀ increases, θ̃ decreases.
   Combined with ∂θ̄/∂p₀ = 0: the over-investment range width θ̄ − θ̃ strictly increases in p₀. [A17, P_C2]

6. **∂θ̃/∂δ: ambiguous sign [Part (iii)]** [PLAUSIBLE]
   By IFT: ∂θ̃/∂δ = −(∂F/∂δ)/(∂F/∂θ).
   ∂F/∂δ = (1−p₀)·w(ê,θ̃)/r − w(e*_int(θ̃),θ̃)/r [envelope theorem on each regime].
   With Cobb-Douglas: ∂F/∂δ ∝ (1−p₀)·ê^β − (e*_int)^β.
   Sign: positive iff (1−p₀)·ê^β > (e*_int)^β, i.e., ê/e*_int > (1−p₀)^{−1/β}.
   This holds when ê is substantially larger than e*_int and p₀ is moderate. When positive: ∂θ̃/∂δ < 0 [as δ rises (hukou relaxed), θ̃ falls, expanding the over-investment range]. The sign can be negative (∂θ̃/∂δ > 0, over-investment range shrinks as hukou relaxes) if ê/e*_int is small. [FALSE_RISK: the sign of ∂F/∂δ is parameter-dependent and may differ from what P_C3(iii) claims]

7. **Non-monotone aggregate gap [Part (iv)]** [PLAUSIBLE]
   ∫Δe*(θ)f(θ)dθ. For θ < θ̃: Δe*(θ) = e*_U − e*_int > 0 (under-investment). For θ ∈ (θ̃,θ̄): Δe*(θ) = e*_U − ê < 0 (over-investment, negative gap). For θ > θ̄: Δe*(θ) = e*_U − e*_R,high > 0 (under-investment again). As δ decreases: under-investment component increases (step 3); over-investment range may expand (step 6, parameter-dependent). Net effect on the integral is ambiguous → confirmed non-monotone. [PLAUSIBLE: formal demonstration requires specific distributional assumptions on f(θ)]

**Additional lemmas needed:**
- **Lemma E (Envelope for V_R at fixed e = ê):** ∂/∂δ [V_R^{high}(ê;θ)] = (1−p₀)·w(ê,θ)/r. [Straightforward differentiation; SOLID]
- **Lemma F (Envelope for V_R^{low} at e*_int):** ∂/∂δ [V_R^{low}(e*_int(δ);θ)] = w(e*_int,θ)/r [by envelope theorem]. [SOLID]

**Hardest step:** Step 6 — the sign of ∂F/∂δ is not uniformly determined; the FALSE_RISK in step 6 means P_C3(iii) as stated may need revision. The statement should be: "under the sufficient condition (1−p₀)·ê^β > (e*_int)^β, ∂θ̃/∂δ < 0" rather than asserting it holds in general.

**Rigor summary:** MOSTLY SOLID for parts (i) and (ii); SKETCH for parts (iii) and (iv).
**To complete:** Clarify P_C3(iii) as a conditional result; formalize part (iv) with specific distributional assumption on f(θ).

---

## [P_W1] — Proof Sketch: Welfare Loss Characterization

**Claim (restated):**
> ΔW(θ) := V_U(e^{FB}(θ);θ) − V_R(e*_R(θ);θ) > 0 for all θ, δ ∈ (0,1); ΔW is non-monotone in θ with a local maximum near θ̃.

**Proof strategy:** Direct comparison of V_U at first-best vs. V_R at constrained optimum; envelope argument for monotonicity.

**Proof sketch:**

1. **ΔW(θ) > 0: Step 1 — First-best exceeds constrained rural payoff** [SOLID]
   e^{FB}(θ) = e*_U(θ) (since the first-best solves max w(e,θ)/r − C(e), same problem as urban child). So V_U(e^{FB};θ) = V_U(e*_U;θ) is the global maximum of w(e,θ)/r − C(e).
   V_R(e*_R;θ) ≤ W_R(e*_R,θ)/r − C(e*_R) ≤ max_e [W_R(e,θ)/r − C(e)].
   Since W_R(e,θ) = [δ+(1−δ)p₀]·w(e,θ) ≤ w(e,θ) for all e (as δ+(1−δ)p₀ ≤ 1 since p₀ ≤ 1 and δ < 1 → δ+(1−δ)p₀ < 1 unless p₀ = 1):
   max_e [W_R·/r − C] < max_e [w/r − C] = V_U(e*_U;θ). → ΔW > 0. [A7, A17]

2. **ΔW(θ) → 0 as δ → 1** [SOLID]
   As δ → 1: W_R(e,θ) → w(e,θ) → e*_R → e*_U → ΔW → 0. [A7]

3. **ΔW is strictly decreasing in δ** [SOLID]
   ∂ΔW/∂δ = −∂V_R(e*_R;θ)/∂δ. By envelope theorem: ∂V_R/∂δ = ∂W_R/∂δ · 1/r. Since ∂W_R/∂δ > 0 (relaxing hukou raises the rural wage), ∂V_R/∂δ > 0 → ∂ΔW/∂δ < 0. Stricter hukou → larger welfare loss. [A7, Envelope theorem]

4. **ΔW is non-monotone in θ: behavior in under-investment regime** [PLAUSIBLE]
   For θ < θ̃: e*_R = e*_int(θ) < e^{FB}(θ). ΔW(θ) = V_U(e^{FB};θ) − V_R(e*_int;θ). Both V_U and V_R^{low} increase in θ (higher ability → higher payoff for both). The difference ΔW may increase or decrease as θ increases; it depends on the relative rate of increase. For Cobb-Douglas: V_U(e^{FB};θ) ∝ θ^{α/(1−β)} (standard computation); V_R^{low}(e*_int;θ) ∝ δ^{β/(1−β)}·θ^{α/(1−β)}. So ΔW ∝ (1 − δ^{β/(1−β)})·θ^{α/(1−β)}, which is strictly increasing in θ for δ < 1. [PLAUSIBLE — specific to Cobb-Douglas; under general w, sign requires checking]

5. **ΔW has a local maximum near θ̃** [PLAUSIBLE]
   At θ = θ̃: e*_R jumps from e*_int(θ̃) to ê (the rural child switches regimes). This jump has two effects: (a) e*_R increases discontinuously → V_R increases (since ê is above e*_int) → ΔW falls discontinuously. (b) After the jump, e*_R = ê while e^{FB}(θ) = e*_U(θ) < ê (for θ just above θ̃): the rural child over-invests relative to first-best, incurring the cost C(ê) − C(e^{FB}) > 0. So ΔW remains positive but may be smaller than just below θ̃. The local maximum occurs just below θ̃ (end of the under-investment regime, where ΔW is increasing by step 4). [FALSE_RISK: the jump argument assumes a discrete transition at θ̃ due to the discrete-jump specification of p; with smooth p, the transition is smooth and the local maximum may not be sharp]

6. **ΔW behavior above θ̄** [PLAUSIBLE]
   For θ > θ̄: e*_R = e*_R,high(θ) < e*_U(θ) (under-investment in high regime, by P_C1 logic with [δ+(1−δ)p₀] < 1). ΔW is again positive and increasing in θ (same logic as step 4 with coefficient [δ+(1−δ)p₀] replacing δ). [PLAUSIBLE]

**Additional lemmas needed:**
- **Lemma G (Cobb-Douglas welfare formula):** Under w = Aθ^αe^β and C(e) = γ·e^k (k > 1), derive closed-form ΔW(θ) in each regime for explicit computation. [SOLID — standard calculus]

**Hardest step:** Step 5 — the non-monotone profile argument requires careful tracking of what happens at θ̃. The FALSE_RISK step is contained (it only affects the characterization of the local maximum, not the existence of non-monotonicity).

**Rigor summary:** MOSTLY SOLID for ΔW > 0 and monotonicity in δ; SKETCH for the non-monotone θ-profile.
**To complete:** Derive closed-form ΔW for Cobb-Douglas case; verify step 4 for general w; characterize the local maximum more carefully.

---

## [P_W2] — Proof Sketch: Unintended Consequence of Hukou Reform

**Claim (restated):**
> Reform setting δ' = 1: (i) eliminates welfare loss; (ii) increases investment for θ < θ̃(δ*); (iii) DECREASES investment for θ ∈ (θ̃(δ*), θ̄).

**Proof strategy:** Direct comparison of pre- and post-reform equilibria; straightforward given P_E1 and P_C2.

**Proof sketch:**

1. **Post-reform (δ = 1): both children solve identical problem** [SOLID]
   With δ = 1: W_R(e,θ) = [1+(1−1)p₀]·w(e,θ) = w(e,θ). The rural child's payoff V_R = w/r − C = V_U. The two problems are identical → e*_R(θ; δ=1) = e*_U(θ) = e^{FB}(θ). Welfare loss ΔW = V_U(e^{FB}) − V_R(e^{FB}) = 0. [A7: multiplicative penalty; δ = 1 → no penalty]

2. **Under-investment regime θ < θ̃(δ*): reform increases investment** [SOLID]
   Pre-reform: e*_R(θ; δ*) = e*_int(θ; δ*) < e*_U(θ) [by P_C1].
   Post-reform: e*_R(θ; 1) = e*_U(θ).
   Hence reform raises investment: e*_U(θ) > e*_int(θ; δ*). [P_C1, step 1]

3. **Over-investment regime θ ∈ (θ̃(δ*), θ̄): reform DECREASES investment** [SOLID given P_C2]
   Pre-reform: e*_R(θ; δ*) = ê [by P_C2].
   Post-reform: e*_R(θ; 1) = e*_U(θ) < ê [since θ < θ̄ → e*_U(θ) < ê by definition of θ̄].
   Hence reform reduces investment from ê to e*_U(θ) < ê. [P_C2, step 8]

4. **Welfare improves despite lower investment** [SOLID]
   Pre-reform welfare: V_R(ê; θ, δ*) = [δ*+(1−δ*)p₀]·w(ê,θ)/r − C(ê) < w(e*_U,θ)/r − C(e*_U) = V_R(e*_U; θ, 1).
   The first inequality: W_R(ê;δ*) < w(ê;1) = w(ê) and e*_U is the first-best optimum for e*_U < ê, so V_U(e*_U) > V_U(ê) > W_R(ê)/r − C(ê) [since W_R < w and e*_U is the urban optimum]. [Step 1 of P_W1; A7]

5. **The paradox** [SOLID given steps 3–4]
   For θ ∈ (θ̃, θ̄): reform both (a) reduces educational investment (step 3) and (b) increases welfare (step 4). This is the unintended consequence: policymakers tracking educational attainment as a reform indicator would observe a fall in attainment for this group, even though welfare is improving. The over-investment pre-reform was a distortion — its elimination is welfare-improving even though it appears to be "less education."

**Additional lemmas needed:** None beyond P_E1 and P_C2.

**Hardest step:** Step 4 — the welfare comparison requires showing V_U(e*_U;θ) > V_R(ê;θ,δ*). This follows from W_R ≤ w and optimality of e*_U, but the formal chain is a one-line argument once the notation is set up correctly. Not hard.

**Rigor summary:** NEAR-COMPLETE
**To complete:** Verify the chain in step 4 formally; state the proof for θ > θ̄ (residual under-investment) analogously to step 2 for completeness.

---

## [P_B1] — Proof Sketch: Boundary and Limit Results

**Claim (restated):**
> (i) δ → 1: e*_R → e*_U; Δe* → 0. (ii) p₀ → 0: over-investment range collapses; model → Arrow (1973). (iii) δ → 0: e*_low → 0.

**Proof strategy:** Direct computation using FOC formulas.

**Proof sketch:**

1. **δ → 1: e*_int → e*_U** [SOLID]
   e*_int satisfies δ·w_e(e*_int)/r = C'(e*_int). As δ → 1: this approaches w_e/r = C', the urban FOC. By continuity of the implicit solution in δ (IFT applies): e*_int(θ;δ) → e*_U(θ). [A5, A6, A7; IFT]

2. **p₀ → 0: F(θ̃; p₀) = 0 → θ̃ → θ̄** [SOLID]
   F(θ̃; p₀) = V_R^{high}(ê;θ̃,p₀) − V_R^{low}(e*_int;θ̃). As p₀ → 0: V_R^{high}(ê;p₀=0) = δ·w(ê)/r − C(ê) = V_R^{low}(ê;θ̃) < V_R^{low}(e*_int;θ̃) [since V_R^{low} is maximized at e*_int < ê]. So F → negative → the indifference condition F = 0 requires θ̃ → θ̄ (where F barely reaches zero, with vanishing escape premium). The over-investment range (θ̃, θ̄) → ∅. [A9, A17 → 0]

3. **δ → 0: e*_int → 0** [SOLID]
   e*_int satisfies δ·w_e(e*_int)/r = C'(e*_int). As δ → 0: the LHS → 0 for any fixed e > 0, while the RHS C'(e) > 0. The equation can only hold if e*_int → 0 (where C'(0) = 0). [A5, A6]

**Additional lemmas needed:** None.

**Hardest step:** None — all steps are straightforward limits of continuous functions.

**Rigor summary:** NEAR-COMPLETE
**To complete:** State formally that the implicit functions are continuous in their parameters (which follows from the IFT, already established in the comparative statics proofs).

---

## Overall Proof Landscape

| Proposition | Rigor Level | Hardest Step | Lemmas Needed |
|------------|------------|-------------|--------------|
| P_E1 | MOSTLY SOLID | Step 5 (Inada condition) | 2 (monotonicity, tie-breaking) |
| P_C1 | NEAR-COMPLETE | None | 0 |
| P_C2 | SKETCH | Step 5 (F strictly increasing) | 3 (Lemmas A, B, C) |
| P_C3 | MOSTLY SOLID (parts i,ii) / SKETCH (parts iii,iv) | Step 6 (∂F/∂δ sign) | 2 (Lemmas E, F) |
| P_W1 | MOSTLY SOLID (ΔW>0, δ-monotone) / SKETCH (θ-profile) | Step 5 (non-monotone θ-profile) | 1 (Lemma G) |
| P_W2 | NEAR-COMPLETE | Step 4 (welfare comparison chain) | 0 (beyond P_E1, P_C2) |
| P_B1 | NEAR-COMPLETE | None | 0 |

**Most vulnerable proposition:** P_C3(iii) — the sign of ∂θ̃/∂δ contains a FALSE_RISK step; the effect of the penalty parameter on the over-investment range width is not uniformly signed and the original proposition statement may need revision.

**Most complete proof:** P_C1 and P_W2 — both are NEAR-COMPLETE with essentially rigorous arguments.

**Priority for formalization:**
1. **P_C2 first** — the headline result. The key GAP (step 5, F strictly increasing) is the most important to resolve; it determines whether the over-investment range is non-empty and unique. Formalize using supermodularity of w and careful case analysis.
2. **P_W2 second** — follows immediately from P_C2 once it is established; clean and policy-relevant.
3. **P_C3(iii) revision** — revise the claim so that the sign of ∂θ̃/∂δ is stated as parameter-dependent with an explicit sufficient condition, rather than as a uniform result.

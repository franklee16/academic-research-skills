# Gate 4: Proof Integrity Gate — Verdict

**Date:** 2026-06-14
**Stage:** Post-Stage-7

---

## Evaluation Rubric

For each proposition, score on 6 checks (PASS / CONDITIONAL / FAIL):

- **Check 1 — Assumptions sufficient:** All assumptions required by the proof are stated explicitly in Stage 5.
- **Check 2 — Argument is valid:** Each step follows from the previous ones without logical gap.
- **Check 3 — Key lemmas stated:** Required auxiliary results are identified (even if not proven).
- **Check 4 — Mathematical objects are well-defined:** All objects (e*_R, ê, θ̃, p₀*, F, Δe*) exist and are unambiguous at each step.
- **Check 5 — No circular reasoning:** Propositions do not rely on each other in a cycle.
- **Check 6 — Negative results:** FALSE_RISK and GAP steps are explicitly flagged and contained.

---

## Per-Proposition Assessment

### P_E1 — Existence and Characterization

| Check | Status | Notes |
|-------|--------|-------|
| 1 — Assumptions sufficient | PASS | A1, A3, A5, A6, A8, A9, H1 all stated in Stage 5 |
| 2 — Argument valid | CONDITIONAL | Step 5 (interior solution existence) requires explicit Inada specification on C not yet stated |
| 3 — Lemmas stated | PASS | Monotonicity of e*_U, tie-breaking at ê flagged as needed |
| 4 — Objects well-defined | PASS | e*_U unique by strict concavity (step 4); e*_R defined as max of two regime optima |
| 5 — No circularity | PASS | P_E1 is the base lemma; nothing here depends on later propositions |
| 6 — FALSE_RISK / GAP flagged | PASS | Step 5 Inada condition flagged as PLAUSIBLE |

**Verdict: CONDITIONAL PASS**
**Condition:** Specify explicitly that C'(0) ≥ 0, C'(ē) > lim_{e→ē} w_e(e,θ)/r for all θ, and that C(0) = 0. These Inada-type conditions ensure interior solution existence in [0, ē].

---

### P_C1 — Under-Investment Benchmark

| Check | Status | Notes |
|-------|--------|-------|
| 1 — Assumptions sufficient | PASS | A5, A6, A7 (multiplicative penalty) sufficient; all stated in Stage 5 |
| 2 — Argument valid | PASS | Single-crossing argument is airtight (steps 1–4); the algebraic chain is complete |
| 3 — Lemmas stated | PASS | No additional lemmas beyond P_E1 required |
| 4 — Objects well-defined | PASS | e*_int well-defined by P_E1; g(e) = w_e/r − C' is well-defined and strictly decreasing |
| 5 — No circularity | PASS | P_C1 uses P_E1 only |
| 6 — FALSE_RISK / GAP flagged | PASS | Step 5 correctly identifies Arrow (1973) lineage; no FALSE_RISK steps in the proof itself |

**Verdict: PASS**
**Note:** This proof is essentially complete. The only remaining item is to formalize P_C1 within a full-paper appendix, where it would occupy half a page.

---

### P_C2 — Escape-Route Over-Investment ★ HEADLINE

| Check | Status | Notes |
|-------|--------|-------|
| 1 — Assumptions sufficient | CONDITIONAL | Steps 1, 3, and 7 each require conditions not listed verbatim in A1–A17: (a) ê ∈ range of e*_U requires calibration assumption on ê; (b) high-regime unconstrained optimum below ê for θ < θ̄ requires Lemma C (derived but not stated); (c) p₀ ≥ p₀* must be listed as an assumption or treated as a sufficient condition |
| 2 — Argument valid | CONDITIONAL | Steps 1–4 and 6–9 follow; step 5 (F strictly increasing) is PLAUSIBLE under Cobb-Douglas w_{eθ} > 0 but not proven for general w satisfying A5 |
| 3 — Lemmas stated | PASS | Three supporting lemmas (A, B, C) explicitly identified in proof sketch |
| 4 — Objects well-defined | PASS | F(θ) is explicitly defined; θ̄ and θ̃ are defined constructively; p₀* is given an explicit formula |
| 5 — No circularity | PASS | P_C2 uses P_E1 (existence) and P_C1 (e*_int < ê); neither uses P_C2 |
| 6 — FALSE_RISK / GAP flagged | PASS | Step 5 explicitly flagged as PLAUSIBLE (not SOLID); the critical gap is clearly identified |

**Verdict: CONDITIONAL PASS**
**Conditions (3):**
1. **Add calibration assumption** (A18): ê ∈ int(range(e*_U)), i.e., θ_L is small enough that e*_U(θ_L) < ê and θ_H is large enough that e*_U(θ_H) > ê. This ensures θ̄ exists and is in the interior of [θ_L, θ_H].
2. **Prove Lemma A** (e*_U strictly increasing in θ) and **Lemma C** (high-regime unconstrained optimum < e*_U(θ)) — both are short IFT arguments.
3. **Resolve the GAP in step 5**: Prove F strictly increasing using the supermodularity of w [w_{eθ} > 0, a consequence of A5 under Cobb-Douglas; must be stated as a maintained assumption for general w].

---

### P_C3 — Comparative Statics on the Investment Gap

| Check | Status | Notes |
|-------|--------|-------|
| 1 — Assumptions sufficient | PASS | Parts (i, ii) use only A5–A7, P_E1, P_C2 FOC; all available |
| 2 — Argument valid | PASS (parts i, ii) / CONDITIONAL (parts iii, iv) | Parts (i, ii): IFT arguments are valid and complete. Part (iii): ∂F/∂δ sign is parameter-dependent; the claim as stated in P_C3 may be incorrect in generality |
| 3 — Lemmas stated | PASS | Envelope Lemmas E and F identified |
| 4 — Objects well-defined | PASS | ∂Δe*/∂δ, ∂θ̃/∂p₀, and ∂θ̃/∂δ defined via IFT wherever the implicit functions are C¹ |
| 5 — No circularity | PASS | P_C3 uses P_C1 (interior solution), P_C2 (θ̃ and θ̄ existence) |
| 6 — FALSE_RISK / GAP flagged | CONDITIONAL | FALSE_RISK in step 6 (∂θ̃/∂δ sign) is flagged, but the proposition statement (P_C3 in candidate_propositions.md) may not reflect this ambiguity |

**Verdict: CONDITIONAL PASS**
**Conditions (2):**
1. **Revise P_C3(iii):** Change the unconditional claim about sign of ∂θ̃/∂δ to a conditional statement: "When (1−p₀)·ê^β > (e*_int(θ̃))^β, ∂θ̃/∂δ < 0 [stricter hukou expands the over-investment range]. The reverse holds when this condition fails." Add this as a parameter condition to the proposition statement.
2. **Formalize P_C3(iv):** Provide a specific example (e.g., uniform f(θ)) under which the aggregate gap is verified to be non-monotone in δ.

---

### P_W1 — Welfare Loss Characterization

| Check | Status | Notes |
|-------|--------|-------|
| 1 — Assumptions sufficient | PASS | All steps use A5–A7; step 4 uses Cobb-Douglas (A5 specific form) |
| 2 — Argument valid | PASS (steps 1–3) / CONDITIONAL (steps 4–6) | Steps 1–3 (ΔW > 0 and monotone in δ) are rigorous; step 4 (ΔW increasing in θ for under-investment regime) is Cobb-Douglas-specific; step 5 (local max near θ̃) uses the discrete-jump structure and is correctly flagged as FALSE_RISK for smooth p |
| 3 — Lemmas stated | PASS | Lemma G (Cobb-Douglas welfare formula) identified |
| 4 — Objects well-defined | PASS | ΔW(θ) is defined as V_U(e^{FB};θ) − V_R(e*_R;θ); both terms are well-defined by P_E1 |
| 5 — No circularity | PASS | P_W1 uses P_E1 (first-best), P_C1, P_C2 (for regime identification); none of these uses P_W1 |
| 6 — FALSE_RISK / GAP flagged | PASS | Step 5 flagged as FALSE_RISK for smooth p(e) case; correctly bounded |

**Verdict: CONDITIONAL PASS**
**Conditions (2):**
1. **Derive Lemma G** explicitly: Under w = Aθ^αe^β and C(e) = γe^k, derive closed-form e^{FB}(θ), V_U(e^{FB};θ), and V_R^{low}(e*_int;θ) to verify ΔW monotone in θ under-investment regime.
2. **Boundary of the non-monotone profile:** The FALSE_RISK (step 5) is contained — it affects the characterization of the local max near θ̃, not the existence of a local max. Statement should specify "the profile has a local maximum below or near θ̃" rather than asserting a sharp discontinuous jump.

---

### P_W2 — Unintended Consequence of Hukou Reform

| Check | Status | Notes |
|-------|--------|-------|
| 1 — Assumptions sufficient | PASS | All steps use only A7 (multiplicative penalty, δ = 1 eliminates it) and results from P_E1, P_C2 |
| 2 — Argument valid | PASS | Steps 1–5 form a complete, rigorous argument; the logic is clean |
| 3 — Lemmas stated | PASS | No new lemmas needed beyond P_E1 and P_C2 |
| 4 — Objects well-defined | PASS | Pre- and post-reform equilibria are well-defined; the reform is a parameter change δ: δ* → 1 |
| 5 — No circularity | PASS | P_W2 uses P_E1, P_C2; the dependency chain is acyclic |
| 6 — FALSE_RISK / GAP flagged | PASS | No FALSE_RISK steps; the proof is conceptually transparent |

**Verdict: PASS**
**Note:** This is the cleanest proof in the set. Given P_C2, P_W2 requires only three lines: (1) δ=1 eliminates the penalty; (2) pre-reform rural child over-invests (e*_R = ê > e*_U); (3) reform moves e*_R from ê to e*_U < ê. Done.

---

### P_B1 — Boundary and Limit Results

| Check | Status | Notes |
|-------|--------|-------|
| 1 — Assumptions sufficient | PASS | A5, A6, A7; no additional assumptions |
| 2 — Argument valid | PASS | Direct applications of IFT and continuity of implicit functions in parameters |
| 3 — Lemmas stated | PASS | No new lemmas; continuity in parameters inherited from P_C1 and P_C3 arguments |
| 4 — Objects well-defined | PASS | All limits exist (by step 1 of P_C3 for δ→1; by step 5 of P_B1 sketch for δ→0 and p₀→0) |
| 5 — No circularity | PASS | P_B1 uses P_C1 (δ→1 limit), P_C2 (p₀→0 limit) |
| 6 — FALSE_RISK / GAP flagged | PASS | No gaps or false risks in any step |

**Verdict: PASS**

---

## Summary Table

| Proposition | Gate 4 Verdict | Blocking Issues |
|------------|---------------|----------------|
| P_E1 | CONDITIONAL PASS | Specify Inada conditions on C |
| P_C1 | **PASS** | None |
| P_C2 | CONDITIONAL PASS | Add A18 (ê in range); prove Lemmas A+C; resolve GAP in step 5 |
| P_C3 | CONDITIONAL PASS | Revise P_C3(iii) to conditional; formalize P_C3(iv) |
| P_W1 | CONDITIONAL PASS | Derive Lemma G; refine characterization of local max |
| P_W2 | **PASS** | None |
| P_B1 | **PASS** | None |

**Overall Gate 4 Verdict: CONDITIONAL PASS**

**Summary of conditions to address before Stage 9:**
1. **A18 (new assumption):** ê ∈ int(range of e*_U over θ ∈ [θ_L, θ_H]).
2. **Three lemmas to prove:** Lemma A (e*_U monotone in θ), Lemma C (high-regime optimum below ê), Lemma G (Cobb-Douglas welfare formula).
3. **One claim to revise:** P_C3(iii) sign of ∂θ̃/∂δ — state as conditional.
4. **Inada conditions on C:** State C'(0) = 0 and appropriate upper bound.
5. **Supermodularity of w:** Add explicitly as a maintained assumption or verify it follows from Cobb-Douglas A5.

**Action for pipeline:** All conditions are of the "add an explicit assumption / prove a supporting lemma" type. None require discarding a proposition or fundamentally restructuring the model. Proceed to Stage 8 with these conditions noted as required for final manuscript.

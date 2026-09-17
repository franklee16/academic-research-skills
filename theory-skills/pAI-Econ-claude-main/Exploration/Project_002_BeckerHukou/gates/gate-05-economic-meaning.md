# Gate 5: Economic Meaning Gate — Verdict

**Verdict:** PASS

**Per-proposition check summary:**

| Proposition | Check 1 (Overreach) | Check 2 (Underreach) | Check 3 (CE Consistency) | Check 4 (Scope) | Check 6 (So What?) |
|------------|--------------------|--------------------|------------------------|----------------|-------------------|
| P_E1 | ✓ | ✓ | ✓ | ✓ | N/A (Supporting) |
| P_C1 | ✓ | ✓ | ✓ (CE1 acknowledged) | ✓ | ✓ |
| P_C2 ★ | ✓ | ✓ | ✓ (CE robustness noted) | ✓ | ✓ |
| P_C3 | ⚠️ | ✓ | ✓ (CE2 conditional acknowledged) | ✓ | ✓ |
| P_W1 | ✓ | ✓ | ✓ | ✓ | ✓ |
| P_W2 ★ | ✓ | ✓ | ✓ | ✓ | ✓ |
| P_B1 | ✓ | ✓ | ✓ | ✓ | N/A (Supporting) |

**Cross-proposition narrative (Check 5):** ✓ — The Cross-Proposition Narrative section is coherent and complete; it weaves all four core propositions into a single story (non-monotone investment pattern, welfare loss profile, reform paradox) with a clear central message.

---

## Check 1 — No Overreach: Detailed Notes

**P_C3 (⚠️ WARNING):** The "So What?" paragraph for P_C3 states "stricter enforcement can expand the population of rural students who over-invest" without explicitly noting the parameter condition (ê/e*_int > threshold) established in CE2-A. The main text of the P_C3 interpretation and Limitations do acknowledge the condition, but the "So What?" paragraph presents the result as if it holds generally. Minor language clarification recommended (add "under the empirically plausible condition that the elite threshold substantially exceeds the interior optimum").

All other CORE propositions (P_C2, P_W1, P_W2): ✓ No overreach detected.
- P_C2 correctly uses "for rural children of intermediate ability" (scoped to (θ̃, θ̄))
- P_W1 correctly uses "is largest for intermediate-ability rural children near the threshold" (not "all")
- P_W2 correctly uses "the most motivated intermediate-ability rural students" and carefully distinguishes welfare from investment outcomes
- P_B1 correctly uses "confirms that the model's novel predictions arise from..." (scope-appropriate)
- P_C1 correctly notes that the result is restricted to multiplicative penalties (CE1-A applied)

---

## Check 2 — No Underreach: Detailed Notes

All CORE propositions provide:
- A causal-chain mechanism in "When → → → outcome" format ✓
- An intuition section explaining why the result holds ✓
- A "Why it would have been non-obvious" subsection ✓
- A "So What?" paragraph ✓

P_W2 is particularly strong: the "So What?" paragraph is suitable for use in a paper's introduction verbatim, with the concrete example (numerical illustration with δ = 0.7, p₀ = 0.3) making the mechanism tangible. ✓

P_C3 provides a clear mechanism for all three sub-results. ✓

---

## Check 3 — Counterexample Consistency: Detailed Notes

- **CE1 (HIGH severity: P_C1 breaks under additive penalty):** Acknowledged in P_C1 Limitations: "the additive-penalty version of the model gives the same result. It does not — with an additive penalty, this proposition fails entirely." ✓ Also noted in the Remark added to the formal statement. ✓
- **CE2 (MEDIUM: P_C3(iii) sign is parameter-dependent):** Acknowledged in P_C3 Limitations: "The sign of the effect of δ on the over-investment range width depends on the ratio ê/e*_int relative to a parameter-dependent threshold." ✓ Also noted the condition in the "So What?" wording (though the WARNING in Check 1 applies to the "So What?" paragraph).
- **CE3 (MEDIUM: supermodularity required):** Added as A_SM; P_C2 interpretation correctly says "for rural children of intermediate ability" without claiming it holds generally when A_SM fails. ✓
- **CE4 (LOW: corner solution):** Acknowledged in P_E1 Limitations. ✓
- **P_C2 robustness to additive penalty:** Correctly noted as a positive robustness finding in P_C2 Limitations: "the under-investment direction is fragile to the penalty form, while the over-investment direction is robust." ✓

---

## Check 4 — Scope Honesty: Detailed Notes

All CORE propositions have explicit Limitations sections with 3+ items each. ✓

Notable strong scope acknowledgments:
- P_C2: "The model is not the world" language; notes partial equilibrium scope; notes the result applies to any "escape-route discrimination regime" beyond China.
- P_W1: Notes welfare is measured in model units, not monetary, requiring calibration.
- P_W2: Explicitly states "the result is about the interpretation of investment data post-reform, not about the desirability of reform itself." ✓

---

## Check 6 — "So What?" Clarity: Detailed Notes

All four CORE propositions have "So What?" paragraphs that:
- Use no unexplained mathematical notation ✓
- Explain the core economic finding to a non-specialist ✓
- Are 3–5 sentences, suitable for use in an introduction ✓

Best "So What?" paragraph: **P_W2** — it sets up the paradox ("the decline in investment is precisely the efficiency gain from removing the distortion"), explains the policy misinterpretation risk, and gives a clear take-away. Publication-ready.

---

## Total Warning Count: 1 (P_C3 "So What?" paragraph overstates generality)

**Threshold for PASS:** ≤ 2 WARNINGs. Actual: 1. ✓

---

## Critical Issues (FAILs)

**None.** No CORE proposition fails any check.

---

## Corrections Required

**1 correction (not blocking; to be made before manuscript submission):**

**P_C3 "So What?" paragraph — add conditional language:**

Current text: "...stricter enforcement can expand the population of rural students who over-invest in education by making the escape-route prize more valuable."

Revised text: "...stricter enforcement can expand the population of rural students who over-invest in education by making the escape-route prize more valuable — a prediction that holds when the elite admission threshold is substantially above rural students' unconstrained optimal investment (the empirically plausible case in China, where Gaokao elite scores substantially exceed typical rural schooling levels)."

This change is minor and does not alter the economic message; it simply closes the scope gap.

---

## Recommended Action

**Proceed to Stage 10 (Manuscript Skeleton)** with the following note for the manuscript drafting stage: apply the P_C3 "So What?" language correction above when writing the introduction or abstract.

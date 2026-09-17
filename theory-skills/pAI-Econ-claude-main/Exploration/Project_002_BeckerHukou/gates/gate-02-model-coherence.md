# Gate 2: Model Coherence Gate — Verdict

**Verdict:** CONDITIONAL PASS

**Check results:**
| Check | Status | Notes |
|-------|--------|-------|
| 1 — Variable Completeness | ✓ | All symbols defined with domains in Notation Summary; θ̄ noted as TBD in Stage 6 (acceptable forward reference) |
| 2 — Equilibrium Concept Compatibility | ✓ | Individual Optimality is correct for independent single-agent problems; no strategic interaction; complete information; compact action space |
| 3 — Budget/Resource Consistency | ✓ | Constraints are per-agent and non-interacting; baseline relaxes budget to non-binding; extension adds credit constraint cleanly |
| 4 — Timing Consistency | ✓ | Period-0 decision conditions only on known parameters; period-1 wages are deterministic given e; no future-event conditioning |
| 5 — Tension Generation | ✓ | Urban FOC: w_e/r = C'. Rural FOC (e < ê): δ·w_e/r = C'. Since δ < 1, rural child's FOC is satisfied at lower e → Δe* > 0. Near ê: escape-probability term enters rural MB, potentially making MB_rural > MB_urban for high θ → Δe* < 0. Both sides of the tension are generated. |
| 6 — Existence (Preliminary) | ✓ | V_U strictly concave → unique interior maximum. V_R continuous on [0,ē] (piecewise, with possible jump at ê) → maximum exists by Weierstrass; may be at corner e = ê |
| 7 — Payoff Consistency | ⚠️ | W_R(e,θ) is discontinuous from the left at e = ê when p(e) has a discrete jump (p(ê⁻) = 0, p(ê) = p₀ > 0). V_R is therefore left-discontinuous at ê. The maximum still exists but the FOC may not characterize it at ê; requires explicit comparison of interior solution vs. corner solution e = ê. Must be addressed in Stage 5 (Assumption Audit). |

**Critical issues (FAIL checks):** None.

**Issues to address (WARNING checks):**
- Check 7: Specify in Stage 5 whether p(e) is treated as (a) discrete jump at ê (clean for the escape-route proposition; requires corner-solution comparison) or (b) smooth approximation near ê (interior FOC applies everywhere; smoother algebra). Recommended: adopt specification (a) — discrete jump — for the main proposition, since the threshold interpretation is economically precise and the corner-solution comparison is standard.

**Recommended action:** Proceed to HiL-4 with the payoff-discontinuity issue to be resolved in Stage 5 (Assumption Audit) by committing to the discrete-jump specification of p(e) and stating the comparison-of-regimes approach explicitly.

# Assumption Audit

**Date:** 2026-06-14
**Stage:** 5 — Assumption Audit

---

## Extracted Assumptions

### [A1] Equal Ability Across Types
**Statement:** Both children have the same innate ability θ ∈ [θ_L, θ_H]; the comparison is parametric in τ, holding θ fixed.
**Where used:** Agents (§1); Central object Δe*(θ) (§6)

**Q1 — Necessity:** NECESSARY
**Justification:** The entire research question is about isolating the institutional effect (hukou) from ability differences. Without this, the investment gap could be explained by ability alone.

**Q2 — Economic motivation:** STRONG MOTIVATION
**Real-world counterpart:** Standard ceteris paribus design; used in every discrimination study to isolate the group-status effect.

**Q3 — Standard:** STANDARD

**Q4 — What breaks if relaxed:** If ability θ correlates positively with urban hukou (e.g., higher-ability parents more likely to hold urban hukou), the observed investment gap conflates the institutional effect with the ability-transmission effect. The clean attribution to the return channel requires θ to be orthogonal to τ in the thought experiment.

**Referee risk:** LOW | **Binding:** YES

---

### [A2] Risk Neutrality
**Statement:** Both children maximize expected net payoff V = W/r − C(e) with no concavity in income.
**Where used:** Preferences (§4)

**Q1 — Necessity:** PROBABLY NECESSARY for closed-form solutions; qualitative under-investment result likely survives under risk aversion.
**Justification:** The over-investment result (escape route) relies on a comparison of expected payoffs from two regimes; with risk aversion the escape-route lottery is worth less, potentially weakening the over-investment.

**Q2 — Economic motivation:** WEAK MOTIVATION
**Real-world counterpart:** Households making education decisions for children face genuine income uncertainty (especially rural households). Risk neutrality is a modelling convenience.

**Q3 — Standard:** STANDARD in baseline theory models.

**Q4 — What breaks if relaxed:** Under risk aversion (concave utility), the escape-route lottery (earn urban wage with probability p, rural wage with 1−p) carries a risk premium cost. The over-investment result survives only if the expected gain from the escape route exceeds the risk premium. For sufficiently high risk aversion, the escape-route incentive could vanish. The under-investment result is robust.

**Referee risk:** MEDIUM | **Binding:** NO (for under-investment); PROBABLY NECESSARY (for escape-route sharpness)

---

### [A3] No Strategic Interaction
**Statement:** C_U and C_R solve independent optimization problems; neither child's payoff depends on the other's action.
**Where used:** Model overview; §3 timing

**Q1 — Necessity:** NECESSARY for the Individual Optimality equilibrium concept.
**Justification:** The model is a comparative statics exercise, not a game.

**Q2 — Economic motivation:** STRONG MOTIVATION
**Real-world counterpart:** Education investment decisions at the household level are not strategic — children are not choosing investment to outcompete each other directly.

**Q3 — Standard:** STANDARD

**Q4 — What breaks if relaxed:** With peer effects or congestion in the escape-route (e.g., if the escape-route probability p(e) is a function of the aggregate investment of rural children, not just own e), the problem becomes a game and the equilibrium concept must change. The escape-route may be rationed.

**Referee risk:** LOW | **Binding:** YES (defines model class)

---

### [A4] Complete Information
**Statement:** All parameters (θ, δ, ê, p₀, r, A, α, β) are common knowledge; no private information and no uncertainty about the model structure.
**Where used:** §3 Information Structure

**Q1 — Necessity:** PROBABLY NECESSARY for tractability.
**Justification:** Uncertainty about δ or p₀ would introduce risk management into the decision; tractable but adds complexity. Uncertainty about θ (own ability) would introduce self-selection on ability — a different model.

**Q2 — Economic motivation:** WEAK MOTIVATION
**Real-world counterpart:** Rural children may not know the precise hukou wage penalty or the escape-route probability. Complete information is a modelling convention.

**Q3 — Standard:** STANDARD for a first model.

**Q4 — What breaks if relaxed:** If δ or p₀ are uncertain (rural children don't know the exact penalty or escape probability), the investment decision involves expected return calculations under uncertainty. The qualitative results likely survive (lower expected return → lower expected investment), but the comparative statics on δ and p₀ would need to account for variance as well as mean effects.

**Referee risk:** MEDIUM | **Binding:** NO (qualitatively); YES (for clean comparative statics)

---

### [A5] Cobb-Douglas Wage Function: w(e,θ) = A·θ^α·e^β
**Statement:** The competitive urban wage is w(e,θ) = A·θ^α·e^β with A > 0, α ∈ (0,1), β ∈ (0,1).
**Where used:** §4 Preferences

**Q1 — Necessity:** LIKELY DISPENSABLE for qualitative results; needed for closed-form comparative statics.
**Justification:** The main results require only: w_e > 0, w_{ee} < 0 (concave in e), w_θ > 0. Any function satisfying these gives the same qualitative results. Cobb-Douglas yields clean formulas.

**Q2 — Economic motivation:** WEAK MOTIVATION
**Real-world counterpart:** Cobb-Douglas is a mathematical convenience; the Mincer earnings function (log-linear in education) would be more empirically grounded but is less tractable for comparative statics on δ.

**Q3 — Standard:** STANDARD in theoretical labor economics.

**Q4 — What breaks if relaxed:** Under a general concave increasing w(e,θ), all qualitative results survive. Specific comparative statics formulas would change form but not sign. The paper could state results for general w and specialize to Cobb-Douglas for explicit solutions.

**Referee risk:** LOW | **Binding:** NO (for qualitative results); YES (for closed-form solutions)

---

### [A6] Strictly Convex Cost Function
**Statement:** C: [0,ē] → ℝ₊ satisfies C(0) = 0, C'(e) > 0, C''(e) > 0 for all e ∈ (0,ē).
**Where used:** §4 Preferences; §9 Consistency

**Q1 — Necessity:** NECESSARY for interior solutions to exist and be unique.
**Justification:** With C'' = 0 (linear cost), the objective V(e) = W(e,θ)/r − C(e) may not be globally concave, and the argmax may be a corner.

**Q2 — Economic motivation:** STRONG MOTIVATION
**Real-world counterpart:** Education has increasing marginal cost: time cost, foregone earnings, tuition — all increase with years of schooling. Standard in the literature.

**Q3 — Standard:** STANDARD

**Q4 — What breaks if relaxed:** Linear cost creates corner solutions (e* = 0 or e* = ē). The continuous comparative statics framework breaks down; analysis shifts to a discrete comparison.

**Referee risk:** LOW | **Binding:** YES (for interior solutions)

---

### [A7] Multiplicative Hukou Wage Penalty
**Statement:** For e < ê, the rural child's effective wage is W_R(e,θ) = δ·w(e,θ), where δ ∈ (0,1) is a constant multiplicative factor.
**Where used:** §4 Preferences (rural child)

**Q1 — Necessity:** NECESSARY in its multiplicative form for the under-investment result.
**Justification:** Under an additive penalty W_R = w(e,θ) − d (constant d > 0), the marginal return to education for the rural child is w_e(e,θ)/r — identical to the urban child. An additive penalty does not affect the optimal investment level (only the payoff level). Therefore, the multiplicative form is essential for the under-investment result; an additive form destroys it.

**Q2 — Economic motivation:** STRONG MOTIVATION
**Real-world counterpart:** A rural hukou holder in the urban labor market earns a proportionally lower wage (e.g., 60–80% of urban wage for the same education and ability), not a fixed absolute difference. Empirical evidence on the hukou wage gap supports a proportional penalty.

**Q3 — Standard:** COMMON — Arrow (1973) uses a similar proportional penalty; wage discrimination models typically use multiplicative factors.

**Q4 — What breaks if relaxed:** Additive penalty → no investment distortion at the margin → main under-investment result (P_C1) fails. **However, P_C2 (escape-route over-investment) survives under additive penalty** — the discrete jump at ê still creates an incentive to over-invest relative to the first-best and the urban child. This asymmetry is itself a result: the under-investment direction is fragile to the penalty form, while the over-investment direction is robust. This is the single most critical functional form choice for P_C1; P_C2 is robust to it.

**Referee risk:** MEDIUM (needs empirical motivation for multiplicative vs. additive) | **Binding:** YES (for P_C1); NO (for P_C2)

---

### [A8] Interior Solution (Inada-type Conditions)
**Statement:** w_e(0,θ)/r → ∞ as e → 0 (or equivalently, marginal return to first unit of education is unbounded) and C'(ē) > w_e(ē,θ)/r, ensuring the urban child's optimum is interior: e*_U ∈ (0,ē).
**Where used:** Implicit in §7 (existence)

**Q1 — Necessity:** PROBABLY NECESSARY for interior solutions; qualitative results survive with corner solutions but characterization is messier.

**Q2 — Economic motivation:** TECHNICAL ONLY
**Real-world counterpart:** A technical regularity condition.

**Q3 — Standard:** STANDARD

**Q4 — What breaks if relaxed:** If the urban child invests e*_U = ē (corner), the comparison Δe*(θ) = ē − e*_R(θ) is trivially positive for all θ; the escape-route result cannot reverse the sign.

**Referee risk:** LOW | **Binding:** NO (qualitative); YES (for characterization)

---

### [A9] Discrete Jump in Escape-Route Probability
**Statement:** p(e) = 0 for e < ê; p(ê) = p₀ > 0; p is non-decreasing for e ≥ ê. (Addressed directly from Gate 2 WARNING.)
**Where used:** §4 Preferences (rural child, e ≥ ê)

**Q1 — Necessity:** PROBABLY NECESSARY for the sharp threshold interpretation; a smooth specification gives the same qualitative result.
**Justification:** The discrete jump corresponds to China's Gaokao-based university tier system — crossing the admission cutoff for a national-key university creates a discrete change in labor market access, not a continuous improvement.

**Q2 — Economic motivation:** STRONG MOTIVATION
**Real-world counterpart:** Gaokao admission thresholds are genuinely discrete (cutoff scores determine tier of university, which affects urban registration access). The jump is institutionally grounded.

**Q3 — Standard:** NON-STANDARD in theory models; discrete jumps complicate analysis.

**Q4 — What breaks if relaxed:** Smooth p(e) near ê (continuous, with p(ê⁻) = 0 and steep p'(ê)) gives the same qualitative escape-route result but allows standard FOC analysis everywhere (no corner solution at ê). The smooth version is easier to work with mathematically and should be offered as a robustness check. The discrete-jump version is the main specification for institutional motivation.

**Referee risk:** HIGH — non-standard; requires comparison-of-regimes analysis; referee may prefer smooth version. | **Binding:** YES (for the specific threshold proposition)

**Resolution of Gate 2 WARNING:** Adopt specification (a) — discrete jump — as the main case; offer smooth-p robustness in an appendix. Characterize e*_R by comparing V_R at interior solution vs. at e = ê explicitly.

---

### [A10] Exogenous Hukou Status
**Statement:** τ ∈ {U, R} is assigned at birth and cannot be changed except via the escape route at e = ê.
**Where used:** §1 Agents; §2 Timing

**Q1 — Necessity:** NECESSARY for the model's structure.
**Justification:** If hukou could be purchased or changed independently of education, the investment decision would include a hukou-acquisition option that is orthogonal to education.

**Q2 — Economic motivation:** STRONG MOTIVATION
**Real-world counterpart:** China's hukou system does not allow free conversion; the main legitimate path to urban hukou for rural-origin individuals is high-education-based migration (including university admission).

**Q3 — Standard:** STANDARD for institutional economics.

**Q4 — What breaks if relaxed:** With purchasable hukou (e.g., via points-based migration systems being piloted in some Chinese cities since 2014), the model needs an additional option — buy urban hukou directly — and the return to education would be reduced because the hukou escape is no longer the only path to urban wages.

**Referee risk:** LOW | **Binding:** YES

---

### [A11] Competitive Labor Market
**Statement:** Both children are price-takers in the labor market; wages equal the marginal product, which is given by the hukou-segmented wage function.
**Where used:** §7 Equilibrium Concept

**Q1 — Necessity:** PROBABLY NECESSARY for the clean wage-equals-marginal-product structure.

**Q2 — Economic motivation:** STRONG for rural labor markets; WEAK for urban (some monopsony possible in concentrated urban labor markets).

**Q3 — Standard:** STANDARD

**Q4 — What breaks if relaxed:** Monopsony in the urban market would compress the urban wage below w(e,θ); the hukou penalty would be smaller than the competitive model predicts. The qualitative results survive but the magnitude of δ is understated.

**Referee risk:** LOW | **Binding:** NO

---

### [A12] Two-Period (Static) Model
**Statement:** Education investment is a once-for-all decision in period 0; period 1 is the entire working life.
**Where used:** §2 Timing

**Q1 — Necessity:** PROBABLY NECESSARY for tractability in a first model.

**Q2 — Economic motivation:** WEAK MOTIVATION — education decisions extend over many years in practice.

**Q3 — Standard:** STANDARD for first-cut analysis.

**Q4 — What breaks if relaxed:** A Ben-Porath dynamic extension would allow continued investment after initial education (on-the-job training). The hukou constraint might interact with on-the-job training: rural workers in urban areas (post-escape) may invest in further human capital, partially offsetting the initial under-investment.

**Referee risk:** MEDIUM | **Binding:** NO (qualitative results survive in a lifecycle extension)

---

### [A13] Ability Observable to Labor Market (No Signaling)
**Statement:** The wage w(e,θ) depends on both e and θ, where θ is observed directly by employers. Education builds productive human capital, not a signal.
**Where used:** §3 Information Structure; §4 Preferences

**Q1 — Necessity:** NECESSARY to remain in the human capital (Becker) paradigm.
**Justification:** Allowing education to function as a signal (Spence) would change the model class entirely; the investment choice would then reflect signaling incentives, not just return-maximization.

**Q2 — Economic motivation:** WEAK MOTIVATION
**Real-world counterpart:** In practice, employers in China use education credentials as signals of ability, not just as direct measures of productivity. The Gaokao score itself is a signal.

**Q3 — Standard:** STANDARD within the human capital tradition; NON-STANDARD if compared to the signaling literature.

**Q4 — What breaks if relaxed:** With signaling, the rural child may invest in education to signal high ability to escape the hukou stigma — creating a "double signaling" problem. The model would need to characterize a separating equilibrium where education signals both ability AND the willingness to escape hukou. This is a fundamentally different and more complex model.

**Referee risk:** HIGH — A referee familiar with China's education context may argue that the Gaokao is primarily a signaling mechanism, not a productivity-building one. The paper must defend the productive human capital interpretation explicitly. | **Binding:** YES

---

### [A14] Non-Binding Budget Constraint (Baseline)
**Statement:** Both children can finance any e ∈ [0,ē] without binding credit constraints in the baseline model.
**Where used:** §5 Action Spaces; §8 Benchmarks

**Q1 — Necessity:** LIKELY DISPENSABLE for the qualitative under-investment result; needed to isolate the return-side channel.

**Q2 — Economic motivation:** WEAK as empirical claim (rural households in China do face credit constraints for education); STRONG as a modelling strategy (isolates the return-side effect).

**Q3 — Standard:** STANDARD to start without credit constraints.

**Q4 — What breaks if relaxed:** Adding a binding credit constraint C(e) ≤ y (family income) creates a second channel for rural under-investment. The welfare decomposition extension (planned) will add this. In the baseline, ruling it out is necessary to cleanly attribute the investment gap to the return channel.

**Referee risk:** MEDIUM | **Binding:** NO (qualitatively); YES (for attribution of the investment gap to the return channel)

---

### [A16] Identical Cost Function Across Types
**Statement:** Both children face the same cost function C(e); there is no school quality differential between urban and rural education.
**Where used:** §4 Preferences

**Q1 — Necessity:** PROBABLY NECESSARY for isolating the return-side effect.
**Justification:** If C_R(e) > C_U(e) (rural schools are worse, making producing e more costly), the investment gap would reflect both higher costs and lower returns for rural children, making the attribution ambiguous.

**Q2 — Economic motivation:** WEAK MOTIVATION
**Real-world counterpart:** Rural schools in China are empirically worse than urban schools. Holding C equal abstracts from this, which is a significant simplification.

**Q3 — Standard:** STANDARD for isolating one channel.

**Q4 — What breaks if relaxed:** If C_R > C_U, the under-investment result is reinforced. The escape-route result is potentially weakened (higher cost makes over-investment near ê less attractive for rural children). The welfare decomposition would need three components: return-side loss, cost-side loss (credit), and school quality loss.

**Referee risk:** HIGH — The Brutal Skeptic (Stage 3) and Economic Intuition Referee both flagged that school quality may be the dominant channel. The paper must explicitly defend abstracting from school quality by arguing that (a) it isolates the return channel and (b) the return channel has independent policy relevance (return equalization via hukou reform vs. cost equalization via school quality investment are different policy instruments). | **Binding:** PROBABLY NECESSARY (for clean attribution)

---

### [A17] Positive Escape-Route Probability: p₀ > 0
**Statement:** p(ê) = p₀ > 0; at the threshold education level ê, the rural child has a strictly positive probability of accessing the urban labor market.
**Where used:** §4 Preferences; §6 State Variables

**Q1 — Necessity:** NECESSARY for the escape-route result to exist.
**Justification:** If p₀ = 0 (no escape route), the model collapses to Arrow (1973) restated in Becker's framework. The irreducibility condition from Gate 2c requires p₀ > 0.

**Q2 — Economic motivation:** STRONG MOTIVATION
**Real-world counterpart:** Elite university admission in China does provide substantially better labor market access in urban areas for rural-hukou graduates. The probability is positive (though small for typical students).

**Q3 — Standard:** NON-STANDARD (specific institutional feature)

**Q4 — What breaks if relaxed:** As p₀ → 0, the escape-route incentive vanishes and the paper's headline result disappears. The under-investment result survives. The paper's novelty claim collapses to Arrow (1973).

**Referee risk:** LOW (institutionally grounded) | **Binding:** YES (irreducibility condition)

---

### [A_SM] Supermodularity of Wage in (e, θ)
**Statement:** w_{eθ}(e,θ) > 0 for all (e,θ) ∈ (0,ē) × (θ_L,θ_H): higher ability increases the marginal return to education.
**Where used:** P_C2 (existence of θ̄ via monotonicity of e*_U); P_C3 (comparative statics); proof sketch step 5 (F strictly increasing in θ)

**Q1 — Necessity:** NECESSARY for e*_U(θ) to be strictly increasing in θ (by IFT on the FOC), which is required to establish θ̄ uniquely.
**Justification:** Supermodularity of w ensures higher-ability children have higher marginal return to investment, hence invest more. Without it, e*_U could be non-monotone and θ̄ might not exist.

**Q2 — Economic motivation:** STRONG MOTIVATION
**Real-world counterpart:** Ability and education are complementary: ability amplifies the return to education investment. Cobb-Douglas satisfies this automatically: w_{eθ} = αβAθ^{α−1}e^{β−1} > 0.

**Q3 — Standard:** STANDARD in human capital models.

**Q4 — What breaks if relaxed:** If w_{eθ} < 0 somewhere, higher-ability children might invest less, making e*_U non-monotone in θ. Then θ̄ (defined by e*_U(θ̄) = ê) may not be unique or may not exist, undermining P_C2's proof structure.

**Referee risk:** LOW (Cobb-Douglas satisfies it; standard assumption) | **Binding:** YES (for P_C2 and P_C3)
**Added:** Stage 8 fix CE3-A

---

### [A18] Inada Upper Bound — Elite Threshold in Interior of e*_U Range
**Statement:** The parameters are calibrated so that: (a) C'(ē) > w_e(ē, θ_H)/r, ensuring e*_U(θ) < ē for all θ; (b) ê ∈ (e*_U(θ_L), e*_U(θ_H)), ensuring the elite threshold lies in the interior of the range of urban optima.
**Where used:** P_E1 (interior characterization); P_C2 (existence of θ̄ via IVT)

**Q1 — Necessity:** NECESSARY for the interior characterization in P_E1 and for θ̄ to exist in (θ_L, θ_H).

**Q2 — Economic motivation:** TECHNICAL — ensures the elite threshold is within the economically relevant range of ability, not so low that all children over-invest or so high that no one can reach it.

**Q3 — Standard:** STANDARD Inada-type parameter condition.

**Q4 — What breaks if relaxed:** If ê > e*_U(θ_H): no child ever finds it optimal to invest at ê even without hukou → the over-investment result is vacuous. If ê < e*_U(θ_L): all children would have invested above ê anyway → the threshold is not binding.

**Referee risk:** LOW (calibration condition, not an economic assumption) | **Binding:** YES (for P_C2's non-triviality)
**Added:** Stage 8 fix CE4-A

---

## Binding Assumptions Summary

| Label | Assumption | Binding Reason |
|-------|-----------|----------------|
| A1 | Equal ability across types | Defines the research question; without it, the gap reflects ability, not institutions |
| A3 | No strategic interaction | Defines the model class (single-agent IO) |
| A6 | Strictly convex cost | Required for interior solutions to exist |
| A7 | Multiplicative hukou penalty | Additive penalty eliminates marginal distortion and destroys P_C1; P_C2 is robust to this |
| A10 | Exogenous hukou status | Defines the institutional constraint being modeled |
| A13 | Ability observable (no signaling) | Keeps model in Becker paradigm; signaling changes model class |
| A15 (= A1) | Equal ability in comparison | See A1 |
| A16 | Identical cost functions | Required to attribute the investment gap cleanly to the return channel |
| A17 | p₀ > 0 | Irreducibility condition: required for the escape-route result |
| A_SM | Supermodularity: w_{eθ} > 0 | Required for e*_U monotone in θ; hence for θ̄ to exist (P_C2, P_C3) |
| A18 | ê ∈ interior of range of e*_U | Calibration condition ensuring θ̄ ∈ (θ_L, θ_H) is non-trivial |

---

## High Referee-Risk Assumptions

| Label | Assumption | Likely Objection | Suggested Response |
|-------|-----------|-----------------|-------------------|
| A7 | Multiplicative penalty | "Why multiplicative, not additive? The results are entirely driven by this choice." | Provide empirical evidence that the hukou wage gap is proportional (e.g., the coefficient on rural hukou in a Mincer regression is proportional to education). Note that additive penalty is a special case that eliminates the margin — itself an interesting null result. |
| A9 | Discrete jump in p(e) | "The discontinuous payoff function is non-standard and the results may be artifact of the discontinuity." | Provide a smooth-p robustness appendix; show that the qualitative results survive for any p with p'(ê) sufficiently large. The discrete jump is just the limit of smooth functions with large slope at ê. |
| A13 | No signaling | "In the Chinese context, the Gaokao is primarily a signaling device. This assumption misrepresents the actual role of education." | Argue that the paper isolates the productive human capital channel, which is relevant for policy evaluation of human capital accumulation. Signaling and productive HC are complementary explanations; this paper focuses on the latter as a tractable first step. Cite evidence that education in China raises productivity (not just signals). |
| A16 | Same cost function | "This is the most unrealistic assumption. Rural schools are much worse. The paper might be explaining the wrong thing." | Argue that school quality differences and return differences are empirically separable policy levers. Hukou reform (equalization of returns) is a different policy from school quality investment. The paper isolates the policy-relevant return channel. Future work should add the cost channel (welfare decomposition extension). |

---

## Hidden Assumptions Found

| Label | Hidden Assumption | Where It Matters |
|-------|------------------|-----------------|
| H1 | Tie-breaking at e = ê | When V_R(interior optimum) = V_R(ê), a tie-breaking rule is needed. Standard choice: if indifferent, choose the higher education level (ê), or specify that V_R is strictly higher at ê when the over-investment result holds. Must be made explicit in Stage 6. |
| H2 | Escape route applies only to rural children | p(e) = 1 for urban children for all e (they already have full urban access). This is implied but not stated; make explicit in Stage 6. |
| H3 | Uniqueness of e*_R | The rural child's problem may have two local optima (interior e*_R < ê and corner at ê). The paper implicitly assumes the global maximum is characterized — which requires explicitly comparing V_R at both candidates. Must be stated as part of the proposition structure in Stage 6. |
| H4 | School quality embedded in w, not C | The assumption that C(e) is the same for both children implicitly assumes school quality differences, if any, are already factored into the wage function through the ability parameter θ. This conflation should be explicitly acknowledged and separated. |

**Recommendation:** Make H1–H4 explicit in Stage 6 (Proposition Generator) as conditions or lemmas.

---

## Assumption Stacking Assessment

**Total explicit assumptions:** 16 (A1–A17, excluding A15 = A1)
**Total binding assumptions:** 8
**Assumption stacking risk:** MEDIUM

The model has a moderate number of assumptions, which is typical for a theory paper in this tradition. The risk is manageable because most assumptions are STANDARD or well-motivated. The two high-risk functional form assumptions (A7 multiplicative, A9 discrete jump) are the ones most likely to trigger referee concerns, and both have clear robustness checks available. The combination of A13 (no signaling) + A16 (same cost) + A7 (multiplicative penalty) together defines the specific channel the paper studies. A referee who is skeptical of any one of these three could challenge the paper's conclusions, so the paper must defend all three jointly in the introduction.

---

## Recommendations for Stage 6

1. **Make the comparison-of-regimes structure explicit:** Proposition 1 should state the under-investment result for e*_R < ê (the Arrow-type benchmark). Proposition 2 (headline) should characterize the conditions under which e*_R = ê (escape-route over-investment) — including explicitly comparing V_R(e*_int) vs. V_R(ê) and characterizing the θ-threshold θ̄ above which over-investment occurs.

2. **State Hidden Assumptions H1–H3 as formal conditions:** Before Proposition 2, state explicitly: (a) tie-breaking rule at ê; (b) that the urban child's escape probability is 1 for all e; (c) that the rural child's global optimum is characterized by comparing two candidates.

3. **Defend A7 (multiplicative) early:** In Proposition 1's proof sketch, include a remark noting that an additive penalty would not generate the investment gap — this makes the multiplicative assumption earn its keep visibly.

4. **Flag A16 (same cost) explicitly in scope:** At the top of the propositions section, state the scope: "We isolate the return-side distortion by holding C(e) equal across types. The cost-side extension (school quality differential and credit constraints) is addressed in Section [X]."

# Candidate Propositions

**Date:** 2026-06-14
**Stage:** 6 — Proposition Generator

---

## Proposition Summary Table

| ID | Type | One-line statement | Role | Difficulty | Novelty |
|----|----|---|---|---|---|
| P_E1 | Existence | Optimal investments exist and are uniquely characterized for both children | SUPPORTING | EASY | LOW |
| P_C1 | Comp. Statics | Under-investment benchmark: e*_R(θ) < e*_U(θ) when rural child's optimum is below escape threshold | SUPPORTING | EASY | LOW (Arrow-type) |
| P_C2 | Comp. Statics | Escape-route over-investment: for θ ∈ (θ̃, θ̄) the rural child invests strictly MORE than the equally-able urban child | **CORE** | MEDIUM | HIGH |
| P_C3 | Comp. Statics | Comparative statics on the investment gap Δe*(θ) w.r.t. hukou penalty δ and escape probability p₀ | **CORE** | MEDIUM | MEDIUM |
| P_W1 | Welfare | Total welfare loss ΔW(θ) > 0 for all δ ∈ (0,1); non-monotone in θ with a local maximum at the boundary of the over-investment region | **CORE** | MEDIUM | MEDIUM |
| P_W2 | Welfare | Unintended consequence: hukou reform (δ → 1) eliminates welfare losses but reduces educational attainment for intermediate-ability rural children | **CORE** | MEDIUM | HIGH |
| P_B1 | Boundary | Limit results: δ → 1 collapses the gap; p₀ → 0 collapses the escape-route to Arrow (1973) | SUPPORTING | EASY | LOW |

---

## Dependency Graph

```
P_E1 (Existence + Characterization)
├── P_C1 (Under-investment benchmark, depends on P_E1 and δ < 1)
├── P_C2 (Over-investment headline, depends on P_E1, δ < 1, p₀ > 0)
│   └── P_C3 (Comparative statics on gap, depends on P_C2)
│       └── P_W1 (Welfare loss, depends on P_C1 + P_C2)
│           └── P_W2 (Reform consequence, depends on P_W1 + P_C2)
└── P_B1 (Boundary limits, depends on P_C1 + P_C2; checks P_B1 independently)
```

---

## Detailed Proposition Statements

---

### [P_E1] — Existence and Characterization of Optimal Investments

**Statement:**
> Under assumptions A1, A3, A6 (convex cost), and A5 (or any concave increasing wage function), there exists a unique optimal investment e*_U(θ) for the urban child and a globally optimal investment e*_R(θ) for the rural child. The urban child's optimum is characterized by the first-order condition. The rural child's optimum is the global maximizer over a two-regime problem: an interior optimum in [0, ê) and a regime optimum in [ê, ē], with the global choice determined by direct payoff comparison.

**Formal statement:**
```
\begin{lemma}[Existence and Characterization]
Under Assumptions A1, A3, A5, A6, and A9:
(i) The urban child's optimum e^*_U(\theta) \in (0, \bar{e}) is the unique solution to:
    \frac{\beta A \theta^\alpha (e^*_U)^{\beta-1}}{r} = C'(e^*_U).
(ii) The rural child's optimum satisfies:
    e^*_R(\theta) \in \arg\max\!\Big\{
        \max_{e \in [0,\hat{e})} V_R^{low}(e;\theta),\;
        \max_{e \in [\hat{e},\bar{e}]} V_R^{high}(e;\theta)
    \Big\}
where V_R^{low}(e;\theta) = \delta w(e,\theta)/r - C(e)
  and V_R^{high}(e;\theta) = [\delta + (1-\delta)p(e)] w(e,\theta)/r - C(e).
\end{lemma}
```

**Required assumptions:** A1, A3, A5, A6, A8 (interior for urban), A9, A18 (Inada upper bound: C'(ē) > w_e(ē,θ_H)/r ensures interior solution below ē)
**Expected proof technique:** Weierstrass theorem (existence); strict concavity of V_U and V_R^{low}, V_R^{high} on respective domains (uniqueness within each regime); direct comparison for global optimum of rural child.
**Proof difficulty:** EASY
**Novelty:** LOW (standard existence result)
**Role:** SUPPORTING

**Economic content:** Establishes the well-posedness of the two-regime optimization and provides the foundation for comparing e*_U and e*_R.

---

### [P_C1] — Under-Investment Benchmark (Arrow-Type)

**Statement:**
> Under assumptions A1–A7 and A10, A13, A16, if the rural child's optimum lies in the low regime (e*_R(θ) ∈ (0, ê)), then e*_R(θ) < e*_U(θ). Specifically, e*_R(θ) is the unique solution to δ·w_e(e,θ)/r = C'(e), and since δ < 1 and w is strictly concave in e, we have e*_R(θ) < e*_U(θ) for all θ ∈ [θ_L, θ_H].

**Formal statement:**
```
\begin{proposition}[Under-Investment Benchmark]
\label{prop:underinvestment}
Under Assumptions A1, A3, A5--A7, A10, A13, A16, and the
multiplicative-penalty specification (A7), suppose the rural child's
optimal investment satisfies e^*_R(\theta) < \hat{e}.
Then e^*_R(\theta) < e^*_U(\theta) for all \theta \in [\theta_L, \theta_H].
Moreover, the investment gap \Delta e^*(\theta) := e^*_U(\theta) - e^*_R(\theta) > 0
satisfies: \Delta e^*(\theta) = 0 when \delta = 1 (no hukou penalty).
\end{proposition}

\begin{remark}[Scope of P_C1]
The under-investment result is specific to the multiplicative penalty
specification (A7). Under an additive penalty W_R(e,\theta) = w(e,\theta) - d,
the rural child's marginal return is w_e(e,\theta)/r — identical to the
urban child's — so e^*_R(\theta) = e^*_U(\theta) and the investment gap
vanishes. The multiplicative form is not merely a convenience: it is
the mechanism through which the institutional penalty distorts the
education investment margin.
\end{remark}
```

**Required assumptions:** A1, A3, A5, A6, A7 (multiplicative penalty — essential; additive penalty destroys this result), A10, A13, A16
**Expected proof technique:** Compare FOCs: urban FOC gives w_e(e*_U)/r = C'(e*_U); rural FOC gives δ·w_e(e*_R)/r = C'(e*_R). Since δ < 1 and w is strictly concave (w_{ee} < 0) while C is strictly convex (C'' > 0), the solution to δ·w_e/r = C' is strictly smaller than the solution to w_e/r = C'. This is a standard single-crossing argument.
**Proof difficulty:** EASY
**Novelty:** LOW — this is Arrow (1973) restated in the Becker framework; stated as benchmark, not as main contribution.
**Role:** SUPPORTING

**Economic content:** Confirms that the hukou wage penalty causes the rural child to under-invest relative to an equally-able urban child. This result follows immediately from the multiplicative penalty structure; its purpose is to establish the benchmark against which the over-investment result (P_C2) is contrasted.

**Note:** This proposition must be presented in the paper as "Proposition 1 (Benchmark)" with a remark explicitly acknowledging that this follows from Arrow (1973) applied to the Becker framework. It is NOT the paper's main contribution.

---

### [P_C2] — Escape-Route Over-Investment ★ HEADLINE

**Statement:**
> Under all model assumptions, there exist non-empty intervals of ability θ for which the rural child's optimal investment strictly exceeds that of the equally-able urban child — the opposite direction from the benchmark under-investment. Specifically, define:
> - θ̄ as the ability level at which e*_U(θ̄) = ê (the urban child's optimum equals the escape threshold)
> - θ̃ as the ability level at which the rural child is indifferent between the low-regime interior optimum and investing at ê
> Then for θ ∈ (θ̃, θ̄): e*_R(θ) = ê > e*_U(θ), i.e., the rural child over-invests relative to the urban child. The interval (θ̃, θ̄) is non-empty if and only if p₀ ≥ p₀*(δ, ê, θ̄).

**Formal statement:**
```
\begin{proposition}[Escape-Route Over-Investment]
\label{prop:overinvestment}
Under Assumptions A1--A10, A13, A16--A17, define:
    \bar\theta: e^*_U(\bar\theta) = \hat{e}
    \tilde\theta: V_R^{low}(e^*_{int}(\tilde\theta);\tilde\theta)
               = V_R^{high}(\hat{e};\tilde\theta)
where e^*_{int}(\theta) is the low-regime interior optimum.
If p_0 \geq p_0^*(\delta,\hat{e},\bar\theta) [defined in the proof],
then \tilde\theta < \bar\theta and for all \theta \in (\tilde\theta, \bar\theta):
    e^*_R(\theta) = \hat{e} > e^*_U(\theta).
That is, the rural child of ability \theta \in (\tilde\theta, \bar\theta) invests
strictly more in education than the equally-able urban child.
\end{proposition}
```

**Required assumptions:** A1, A3, A5, A6, A7 (multiplicative), A9 (discrete jump), A10, A13, A16, A17 (p₀ > 0), A_SM (supermodularity: w_{eθ} > 0), A18 (ê ∈ interior of range of e*_U)
**Expected proof technique:**
1. Show θ̄ is well-defined by the intermediate value theorem (e*_U is continuous and strictly increasing in θ by A_SM; e*_U(θ_L) < ê < e*_U(θ_H) by A18).
2. Show θ̃ is well-defined: evaluate V_R(ê; θ̄) − V_R(e*_int(θ̄); θ̄). At θ = θ̄, the jump at ê delivers V_R(ê; θ̄) > V_R(e*_int(θ̄); θ̄) iff (1−δ)p₀·w(ê,θ̄)/r > [C(ê)−C(e*_int)] − δ[w(ê,θ̄)−w(e*_int,θ̄)]/r (the escape premium exceeds the net cost of over-investing). This defines p₀*.
3. By continuity, θ̃ < θ̄ if p₀ > p₀*.
4. For θ ∈ (θ̃, θ̄): rural child chooses ê (high-regime corner); urban child's optimum e*_U(θ) < ê (since θ < θ̄). Hence e*_R(θ) = ê > e*_U(θ). QED.

**Proof difficulty:** MEDIUM
**Novelty:** HIGH — this result does not appear in Arrow (1973) or any standard human capital / discrimination model
**Role:** CORE

**Economic content:** The hukou escape route creates a perverse over-investment incentive for intermediate-ability rural children. These children invest at the threshold ê even though, absent the hukou barrier, they would optimally invest less. The institutional barrier does not merely suppress investment for the disadvantaged group — for the most motivated subset, it forces excess investment, a second-best distortion in the opposite direction.

---

### [P_C3] — Comparative Statics on the Investment Gap

**Statement:**
> (i) In the under-investment regime (θ < θ̃): the investment gap Δe*(θ) = e*_U(θ) − e*_R(θ) is strictly decreasing in δ (relaxing the hukou penalty closes the gap) and independent of p₀ (escape probability does not affect behavior below θ̃).
> (ii) The over-investment range (θ̃, θ̄): the width θ̄ − θ̃ is increasing in p₀ (higher escape probability expands the range) and non-monotone in δ (stricter hukou makes escape more valuable, potentially expanding the range, but also shifts θ̃ and θ̄).
> (iii) The investment gap at the threshold θ̄: Δe*(θ̄) = 0 − (e*_R(θ̄) − ê) > 0 [the rural child over-invests relative to urban at θ̄]; the over-investment magnitude |Δe*(θ)| for θ ∈ (θ̃, θ̄) is increasing in the ability gap θ̄ − θ (rural child at lower ability over-invests more).

**Formal statement:**
```
\begin{proposition}[Comparative Statics on the Investment Gap]
\label{prop:comparativestatics}
Under all model assumptions:
(i) \frac{\partial \Delta e^*(\theta)}{\partial \delta} < 0
    for \theta \in [\theta_L, \tilde\theta) (under-investment regime).
(ii) \frac{\partial (\bar\theta - \tilde\theta)}{\partial p_0} > 0:
    a higher escape probability expands the over-investment ability range.
(iii) When \hat{e}/e^*_{int}(\tilde\theta) > (1-p_0)^{-1/\beta}
    (empirically satisfied when the elite threshold substantially exceeds
    the interior optimum):
    \frac{\partial \tilde\theta}{\partial \delta} < 0,
    so a stricter hukou penalty (lower \delta) lowers the threshold \tilde\theta,
    expanding the set of rural children who find it optimal to invest at \hat{e}.
    The condition holds in the empirically relevant regime (\hat{e} \gg e^*_{int}).
    When the condition fails (elite and interior thresholds are close), the
    effect of \delta on the over-investment range is ambiguous.
(iv) The aggregate investment gap integrating over \theta:
    \int_{\theta_L}^{\theta_H} \Delta e^*(\theta) f(\theta) d\theta
    is non-monotone in \delta: starting from \delta = 1 (no gap),
    as \delta decreases the aggregate gap first increases (from under-investment),
    then may decrease if the over-investment range expands sufficiently.
\end{proposition}
```

**Required assumptions:** A1, A3, A5, A6, A7, A9, A10, A13, A16, A17; plus a distribution F(θ) on [θ_L, θ_H] for part (iv)
**Expected proof technique:** Implicit function theorem applied to the FOC (for parts i, iii); direct differentiation of θ̄ − θ̃ w.r.t. p₀ using the definition of θ̃ (for part ii); envelope theorem for payoff comparisons. Part (iv) requires integration and may require a sign condition on f(θ) near the over-investment range.
**Proof difficulty:** MEDIUM
**Novelty:** MEDIUM — direction of gap under under-investment is standard; parts (ii)–(iv) on the over-investment range are new.
**Role:** CORE

**Economic content:** The comparative statics reveal a key policy paradox: stricter hukou enforcement (lower δ) both increases under-investment among low-ability rural children AND expands the over-investment incentive among intermediate-ability rural children. These are competing effects on aggregate human capital, and the net effect on total investment is ambiguous — a result with direct policy relevance for China's ongoing hukou reform.

---

### [P_W1] — Welfare Loss Characterization

**Statement:**
> The total welfare loss from the hukou constraint is ΔW(θ) := V_U(e^FB(θ); θ) − V_R(e*_R(θ); θ) > 0 for all θ ∈ [θ_L, θ_H] and δ ∈ (0,1). The welfare loss is non-monotone in θ: it is hump-shaped, with a local maximum near the boundary of the over-investment region (θ ≈ θ̃), where the rural child transitions from under-investing to over-investing and the distance from the first-best is largest.

**Formal statement:**
```
\begin{proposition}[Welfare Loss]
\label{prop:welfare}
Under all model assumptions, for all \theta \in [\theta_L, \theta_H] and \delta \in (0,1):
(i) \Delta W(\theta) := V_U(e^{FB}(\theta);\theta) - V_R(e^*_R(\theta);\theta) > 0.
(ii) \Delta W(\theta) is strictly decreasing in \delta:
    \frac{\partial \Delta W(\theta)}{\partial \delta} < 0
    (relaxing the hukou penalty reduces welfare loss).
(iii) \Delta W(\theta) is non-monotone in \theta. Specifically,
    there exists \theta^{max} \approx \tilde\theta such that
    \Delta W(\theta) achieves a local maximum at \theta^{max},
    reflecting the largest distance from first-best occurring at the
    threshold between the under- and over-investment regimes.
\end{proposition}
```

**Required assumptions:** A1, A3, A5–A7, A9, A10, A13, A16, A17; plus the first-best benchmark (δ = 1, p ≡ 1)
**Expected proof technique:**
- Part (i): V_R ≤ V_U always (since W_R(e,θ) ≤ w(e,θ) for all e and δ < 1), and e*_R ≠ e^FB; direct substitution.
- Part (ii): Envelope theorem on V_R w.r.t. δ: ∂V_R/∂δ > 0 (higher δ = better terms for rural child → higher payoff → smaller gap from first-best).
- Part (iii): At θ < θ̃ (under-investment), ΔW increases as θ approaches θ̃ (the rural child is increasingly far from the first-best as the penalty pushes e*_R further below e^FB). At θ > θ̃ (over-investment), the rural child invests ê which may be closer to e^FB than e*_low was. The welfare loss profile is characterized by direct computation.

**Proof difficulty:** MEDIUM
**Novelty:** MEDIUM — welfare loss analysis in discrimination models is standard; the non-monotone profile with a maximum at the regime boundary is new.
**Role:** CORE

**Economic content:** The welfare loss from the hukou constraint is not uniform across ability levels — it is largest for the intermediate-ability rural children who are closest to the escape-route threshold. These are exactly the students for whom the institutional distortion is most severe: they are forced to over-invest at ê, bearing the cost of excess education, while still not achieving the first-best (since even with p₀ > 0, they earn less than urban children in expectation due to δ < 1). This generates a policy targeting implication: hukou reform would benefit intermediate-ability rural children the most.

---

### [P_W2] — Unintended Consequence of Hukou Reform ★ POLICY RESULT

**Statement:**
> When the hukou barrier is removed (δ → 1 with p₀ ≥ p₀* maintained, or equivalently p₀ → 0 making the escape route accessible to all), the welfare loss ΔW(θ) → 0 for all θ. However, the effect on educational attainment is non-monotone: for rural children in the over-investment range (θ ∈ (θ̃, θ̄)), the removal of the hukou constraint strictly reduces their educational investment from ê to e*_U(θ) < ê. Thus, hukou reform that eliminates the barrier simultaneously improves welfare for all ability levels AND reduces observed educational investment among the most incentivized intermediate-ability rural students. This is an unintended consequence: policymakers who use educational attainment as an indicator of reform success may observe an unexpected decrease in investment among the most motivated rural students.

**Formal statement:**
```
\begin{proposition}[Unintended Consequence of Hukou Reform]
\label{prop:reform}
Let \delta^* \in (0,1) be the status-quo hukou penalty. Under all model
assumptions, a reform that sets \delta' = 1 (full return equalization):
(i) Eliminates welfare loss: \Delta W(\theta; \delta') = 0 for all \theta.
(ii) Increases investment for \theta \in [\theta_L, \tilde\theta(\delta^*)]:
    e^*_R(\theta; \delta') = e^*_U(\theta) > e^*_R(\theta; \delta^*).
(iii) DECREASES investment for \theta \in (\tilde\theta(\delta^*), \bar\theta):
    e^*_R(\theta; \delta') = e^*_U(\theta) < \hat{e} = e^*_R(\theta; \delta^*).
    The reform reduces educational attainment for intermediate-ability
    rural children even as it improves their welfare.
\end{proposition}
```

**Required assumptions:** A1–A10, A13, A16, A17; plus the reform experiment (δ changing from δ* to 1)
**Expected proof technique:** Direct computation. Post-reform (δ = 1): both children solve the same problem; e*_R = e*_U = e^FB. Pre-reform: e*_R(θ) = ê for θ ∈ (θ̃, θ̄) and ê > e*_U(θ). So reform reduces investment from ê to e*_U(θ) < ê for θ in this range.
**Proof difficulty:** EASY (given P_C2)
**Novelty:** HIGH — counter-intuitive; not present in any discrimination or human capital model that we are aware of. Policy-relevant for the ongoing hukou reform debate in China.
**Role:** CORE

**Economic content:** Hukou reform is unambiguously welfare-improving, but it has an unintended consequence for observable educational attainment: the most incentivized intermediate-ability rural students will rationally invest less in education once the escape-route incentive is removed. This is a new theoretical prediction that could be tested using China's hukou reform episodes since 2014. It also suggests that policymakers should not interpret reduced educational attainment among motivated rural students as a sign that reform has failed — it is, paradoxically, a sign that the distortionary over-investment incentive has been eliminated.

---

### [P_B1] — Boundary and Limit Results

**Statement:**
> (i) As δ → 1: e*_R(θ) → e*_U(θ) = e^FB(θ) for all θ; Δe*(θ) → 0; ΔW(θ) → 0. The urban-rural investment gap vanishes continuously.
> (ii) As p₀ → 0: the over-investment range (θ̃, θ̄) → ∅ (collapses to empty); e*_R(θ) → δ-Becker interior solution for all θ; the model converges to Arrow (1973) restated in Becker's framework.
> (iii) As δ → 0: e*_R(θ) → 0 for θ in the low regime; the over-investment range expands; the escape-route becomes the dominant investment incentive. In the limit, only students above θ̃(δ→0) invest any positive amount.

**Formal statement:**
```
\begin{proposition}[Boundary Cases]
\label{prop:boundary}
Under all model assumptions:
(i) \lim_{\delta \to 1} e^*_R(\theta) = e^*_U(\theta) \text{ for all } \theta.
(ii) \lim_{p_0 \to 0} e^*_R(\theta) = \text{Arrow solution: }
    e_A(\theta) \text{ s.t. } \delta w_e(e_A;\theta)/r = C'(e_A),
    \text{ and the over-investment range collapses: }
    \lim_{p_0 \to 0} (\bar\theta - \tilde\theta) = 0.
(iii) \lim_{\delta \to 0} e^*_{low}(\theta) = 0 \text{ for all } \theta;
    the escape route is the only incentive to invest.
\end{proposition}
```

**Required assumptions:** A1–A10, A13, A16, A17
**Expected proof technique:** Direct computation using the explicit FOC solutions and the definition of θ̃(δ, p₀). Limit (ii) uses the fact that as p₀ → 0, V_R(ê; θ) → V_R(e*_int; θ) from above, so the indifference condition V_R(ê; θ̃) = V_R(e*_int; θ̃) requires θ̃ → θ̄.
**Proof difficulty:** EASY
**Novelty:** LOW (verification of model behavior at extremes)
**Role:** SUPPORTING

**Economic content:** The boundary results confirm the model's theoretical coherence and establish the relationship to Arrow (1973) as the limiting case (p₀ → 0). They also give testable predictions: as China's hukou system is relaxed (δ → 1 partially), we should see the investment gap shrinking continuously — a prediction that could be tested using reform intensity data.

---

## Hidden Assumption Propositions (from Stage 5)

The following conditions are elevated from hidden assumptions (H1–H3) to formal lemma status, to be stated before Proposition P_C2:

**Lemma H1 (Tie-breaking):** If V_R(e*_int(θ̃); θ̃) = V_R(ê; θ̃), the rural child is assumed to invest at ê (tie-breaking toward the higher education level). This is without loss of generality since indifference is a measure-zero event.

**Lemma H3 (Uniqueness of e*_R):** The rural child's problem has a unique global maximum. The proof distinguishes two cases: (a) θ < θ̃: unique low-regime interior solution; (b) θ > θ̃: unique choice ê (or interior high-regime solution for θ above the region where high-regime optimum exceeds ê).

---

## What the Model CANNOT Establish

The following claims are OUT OF SCOPE for this model:
1. **Empirical magnitudes:** The model cannot say how large the investment gap is in Chinese data (requires calibration and empirical estimation).
2. **General equilibrium effects:** Aggregate labor supply effects on wages are not modeled; the competitive wage function is taken as given.
3. **Dynamic lifecycle effects:** The model is two-period; long-run career effects of the initial investment choice are abstracted away.
4. **Signaling equilibria:** If education is also a signal of ability, the investment decisions would reflect signaling incentives (Spence structure) in addition to productive returns. The model cannot speak to this.
5. **School quality effects:** The model abstracts from differential school quality (same C for both types); results about the school-quality channel cannot be derived from this model.
6. **Political economy of hukou reform:** Why the hukou system exists and persists is not modeled (τ is exogenous).

---

## Contribution Assessment

**Core propositions count:** 4 (P_C2, P_C3, P_W1, P_W2)
**Overall strength of contribution:** MODERATE–STRONG

The proposition set constitutes a publishable contribution at the *Journal of Development Economics* level and has a viable path to *AEJ:Applied Economics*. The core results — over-investment for intermediate-ability rural children (P_C2) and the unintended consequence of reform (P_W2) — are genuinely new and carry policy relevance for an ongoing debate. The comparative statics (P_C3) and welfare analysis (P_W1) strengthen the contribution beyond the headline result. The under-investment benchmark (P_C1) is acknowledged as an Arrow (1973) corollary, not as a novel contribution.

**What would strengthen the contribution:**
- An empirical section or calibrated numerical illustration of the over-investment range for specific Chinese parameters (δ, p₀, ê), to demonstrate the quantitative relevance of P_C2
- A formal welfare decomposition separating the return-channel loss from the school-quality channel loss (credit constraint extension), addressing Referee Concern 3 from Stage 3

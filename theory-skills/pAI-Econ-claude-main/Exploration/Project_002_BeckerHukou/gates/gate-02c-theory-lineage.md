# Gate 2c: Theory Lineage Gate — Verdict

**Date:** 2026-06-14
**Runs after:** Stage 3b (Canonical Model Matching)

---

## Theory Lineage Statement

```
THEORY LINEAGE STATEMENT
========================
Closest canonical ancestors:
  (1) Becker, G.S. (1964). Human Capital. University of Chicago Press.
      [Structural basis: single-agent education investment optimization]
  (2) Arrow, K.J. (1973). "The Theory of Discrimination." In Ashenfelter
      and Rees (eds.), Discrimination in Labor Markets. Princeton UP.
      [Mechanism basis: group-specific wage penalty → investment divergence
      for equal-ability agents]

What is inherited from the ancestors:
  From Becker (1964):
  1. Single-agent optimization: individual with innate ability θ chooses
     education investment level e ∈ [0, ē] to maximize net present value
     of lifetime earnings net of education costs
  2. Two-period timing: period 0 (education decision), period 1 (labor
     market participation at wages determined by education and ability)
  3. Equilibrium concept: individual optimality under competitive wages;
     wage = marginal product of human capital in the labor market
  4. First-order condition structure: invest until marginal return to
     education = marginal cost of funds (opportunity cost r)
  5. General human capital framing: education is portable across employers;
     the worker captures the full return to general training

  From Arrow (1973):
  6. Two-group structure: agents with identical ability θ but different
     institutional status (urban hukou vs. rural hukou, analogous to
     Arrow's majority vs. minority group)
  7. Group-specific wage penalty: disadvantaged group (rural) receives a
     fraction δ ∈ (0,1) of the wage earned by the advantaged group
     (urban) for the same education and ability
  8. Investment divergence result (benchmark): lower return → lower
     optimal investment for equal-ability agents in the disadvantaged
     group (this is the under-investment proposition, held as benchmark)

What is changed from the ancestors:
  Change 1 — Source of the return differential:
    Arrow's wage penalty arises from employer taste-based discrimination
    (an equilibrium outcome of prejudiced employer preferences). The hukou
    penalty arises from a codified administrative-legal rule that restricts
    rural workers' access to urban labor markets. Structurally: Arrow's δ
    is an endogenous equilibrium object (a function of employer preferences
    and labor market competition); the hukou δ is an exogenous policy
    parameter directly manipulable by the government. This changes the
    welfare and policy analysis completely: Arrow's remedy requires
    changing employer preferences; the hukou remedy requires a legal
    reform of a specific institutional parameter.

  Change 2 — Shape of the return function for the disadvantaged group:
    Arrow assumes a smooth, monotone, proportional wage penalty: rural
    wage = δ × urban wage for ALL education levels e. The proposed
    model adds a threshold structure: at a critical education level ê
    (e.g., admission to an elite university), rural agents gain access
    to the urban labor market with probability p(e; ê) ∈ [0,1], making
    the effective return function non-monotone for rural agents.

What new economic mechanism is added:
  The escape-route threshold mechanism: when a rural agent's education
  level e reaches ê (the critical threshold at which elite university
  admission grants access to urban labor markets), the probability of
  accessing the full urban wage jumps from 0 to p(ê) > 0. For e > ê,
  p(e; ê) is increasing in e. This makes the marginal benefit schedule
  for rural agents non-monotone:
    MB_rural(e) = δ × w_e(e, θ)                               for e < ê
    MB_rural(e) = [δ + (1−δ)p(e;ê)] × w_e(e,θ)
                  + (1−δ) × p_e(e;ê) × w(e,θ)                for e ≥ ê
  The second term in the e ≥ ê expression, (1−δ) × p_e(e;ê) × w(e,θ),
  is positive and represents the marginal return from improving the escape
  probability. For agents with high θ (high w(e,θ)), this term can exceed
  the urban child's marginal benefit δ × w_e(e,θ) near ê, causing
  MB_rural(e) > MB_urban(e) in a neighborhood above ê. As a result,
  the optimal investment of a high-θ rural agent exceeds that of an
  equally-able urban agent: e*_rural(θ) > e*_urban(θ) for θ above a
  threshold θ̄(ê, p, δ). This is the paper's headline result: hukou
  barriers can cause OVER-investment by the most talented rural children,
  not just under-investment — a prediction Arrow (1973) cannot generate.

Where the novelty lies:
  [x] New primitives (escape-route threshold ê and probability function
      p(e; ê) not present in Arrow or Becker)
  [ ] Modified information structure
  [ ] Different equilibrium concept
  [x] New comparative statics direction (sign of the investment gap
      reverses for high-θ agents — not a monotone result)
  [x] New welfare implication (over-investment at the escape route is a
      second-best distortion in the opposite direction from Arrow)
  [x] New policy interpretation (hukou reform may reduce investment by
      high-ability rural children — an unintended consequence not in
      Arrow's or Becker's welfare analysis)
  [ ] Extension to a broader class of environments

This paper would NOT reduce to the Arrow-in-Becker ancestor model if:
  The irreducibility condition is: there exists an interior escape-route
  threshold ê ∈ (0, ē) at which rural agents access the urban labor
  market with strictly positive probability, p(ê) > 0.
  
  Formally: the paper differs from Arrow (1973) restated in Becker's
  framework if and only if ∃ ê ∈ (0, ē) such that p(ê) > 0. If no
  such ê exists (p ≡ 0 everywhere, or ê = ē — escape only possible
  at maximum investment), the non-monotone marginal benefit schedule
  collapses to Arrow's smooth penalty, and the paper produces only
  the under-investment result already known from Arrow. The escape-route
  mechanism is therefore the paper's irreducible contribution.
```

---

## Check-by-Check Results

| Check | Verdict | Reason |
|-------|---------|--------|
| Check 1 — Ancestor Identification | PASS | Two specific papers named: Becker (1964) *Human Capital* and Arrow (1973) "The Theory of Discrimination." Both identifications are credible and appropriate. |
| Check 2 — Inheritance Completeness | PASS | Eight specific inherited elements listed (5 from Becker, 3 from Arrow), covering primitives, timing, equilibrium concept, FOC structure, and the investment divergence mechanism. Sufficient for a referee to verify which parts are standard. |
| Check 3 — Genuine Change | PASS | Two substantive changes identified: (1) source of the return differential changes from endogenous equilibrium object (Arrow) to exogenous policy parameter (hukou) — this is a structural change that alters the welfare and policy analysis; (2) the shape of the return function changes from smooth monotone to non-monotone with threshold — this generates new equilibrium behavior not present in Arrow. Neither change is notational. |
| Check 4 — New Mechanism Specificity | PASS | Complete causal chain provided: [escape-route threshold ê with p(ê) > 0] → [MB_rural(e) becomes non-monotone above ê; escape-probability term dominates for high-θ agents] → [e*_rural(θ) > e*_urban(θ) for θ > θ̄, reversing the under-investment prediction]. The mechanism includes specific functional form characterization of MB_rural(e). |
| Check 5 — Irreducibility | PASS | Specific, non-trivial irreducibility condition stated: ∃ ê ∈ (0, ē) with p(ê) > 0. The condition can fail (e.g., if the government fully restricts university-based hukou conversion), in which case the paper collapses to Arrow. The condition is empirically verifiable and not tautologically true. |

---

## Overall Gate Verdict: **PASS**

Theory lineage is complete. The paper inherits from Becker (1964) and Arrow (1973), makes two genuine substantive changes, and adds a non-trivial escape-route mechanism with a complete causal chain. The irreducibility condition (escape-route threshold at interior education level with p(ê) > 0) is clearly stated. Stage 4 (Model Primitives) may proceed with the confirmed lineage.

# Canonical Model Match

**Date:** 2026-06-14
**Stage:** 3b — Canonical Model Matching

---

## Research Puzzle Summary

Two children of identical innate ability (θ) but different hukou registration status (urban vs. rural) face different expected marginal returns to education because China's hukou system segments the labor market. In an extended Becker human capital investment model, this return differential causes them to choose different optimal education investment levels even when costs are held equal. The paper's headline result (directed by the Persona Council) is that high-ability rural children may invest *more* than equally-able urban peers when hukou can be escaped via elite university admission — a counter-intuitive over-investment distortion that distinguishes this paper from Arrow (1973). The under-investment result for low-to-middle ability rural children follows as a corollary.

---

## Candidate Model Families

### Candidate 1: Becker Human Capital Investment Model
- **Fit rationale:** The model library entry's "When to Use" section lists "When studying the economics of education investment" as the primary use case. The research puzzle is precisely about the education investment decision. The Becker model's core structure — agent invests until marginal return equals marginal cost of funds — is the explicit framework named in the research hypothesis.
- **Key structural match:**
  - *Friction type:* Institutional return segmentation (hukou wage penalty) maps to the "How to Extend the Model" section's "Credit-constrained workers" entry — both shift the effective return/cost balance away from first-best. Here the distortion is on the return side (not the cost side), which is structurally analogous.
  - *Agent structure:* Worker chooses education investment level; competitive labor market (modified by hukou segmentation) determines return. This matches the Becker general human capital timing exactly.
  - *Equilibrium concept:* Individual optimality (not strategic interaction); agent solves a single-agent optimization. Matches "Competitive equilibrium" in Becker general HC.
  - *Key result type:* Comparative statics on optimal investment as a function of a return-side parameter. Matches "Comparative Statics Usually Available" in the Becker library entry.
- **Potential gap:** The Becker model library entry does not accommodate group-specific return functions; the hukou modification must be introduced as a new element. The "escape route" threshold (top university admission grants urban hukou) creates a non-monotone marginal benefit schedule that has no counterpart in the standard Becker setup.
- **Closest canonical ancestor:** Becker (1964) general human capital model, specifically the setup where the worker chooses how much to invest in education (continuous choice) and the return is determined by the competitive labor market wage for human capital.
- **Fit score: HIGH**

---

### Candidate 2: Education Under Credit Constraints
- **Fit rationale:** The library entry's "When to Use" section lists "When decomposing the correlation between parental income and children's education into a 'pure income constraint' effect versus a 'returns to education' effect." This is directly relevant to the welfare decomposition (N3), which requires separating the return-side effect (hukou wage penalty) from the cost-side effect (borrowing constraints rural children may also face). The credit constraint model provides the formal apparatus for the cost-side welfare accounting.
- **Key structural match:**
  - *Friction type:* Credit constraint (cost-side distortion) is the mirror image of the hukou penalty (return-side distortion). The welfare decomposition requires both to be modeled.
  - *Agent heterogeneity:* The library entry explicitly has "Heterogeneity in ability θ: determines the return R(θ) to education" alongside "Heterogeneity in family income y" — exactly the two dimensions of heterogeneity in the proposed model (ability θ and hukou status τ).
  - *Main mechanism:* The credit constraint library entry's "Main Mechanism" section shows how to derive underinvestment analytically: agents invest H=1 iff R(θ) ≥ 0 AND cost ≤ budget. The proposed paper can analogously derive: agent invests e* iff marginal return (hukou-adjusted) equals marginal cost.
- **Potential gap:** The credit constraint model is typically discrete (invest or not), whereas the Becker investment problem is continuous (how much to invest). The continuous Becker framework is the better baseline; the credit constraint model is best used as a welfare accounting complement.
- **Closest canonical ancestor:** Galor-Zeira (1993) — the library entry lists this as the canonical predecessor for investment divergence among equal-ability individuals facing different institutional environments.
- **Fit score: MODERATE**

---

### Candidate 3: Occupational Choice / Roy Model (Comparative Advantage)
- **Fit rationale:** The library entry's description of workers sorting across sectors based on comparative advantage, with institutional barriers potentially preventing efficient sorting, is partially relevant. The hukou system is a barrier to rural workers sorting into urban occupations. The Roy model's self-selection structure is present: rural workers choose between (a) investing heavily in education to access urban labor markets and (b) investing less and remaining in rural employment.
- **Key structural match:**
  - *Two-sector structure:* Urban sector (high wage, high return to education) and rural sector (low wage, lower return to education) maps to the Roy two-sector setup.
  - *Institutional barrier:* The hukou restriction prevents free sorting into the urban sector, distorting the competitive equilibrium allocation.
- **Potential gap:** The Roy model takes skills/human capital as given and analyzes sector selection. The proposed research takes sector access (as mediated by hukou) as given (or parametric) and analyzes the investment decision. The Roy model does not model the endogenous human capital investment choice. This is a fundamental mismatch.
- **Closest canonical ancestor:** Harris-Todaro (1970) — expected income model of migration with an urban sector barrier to entry.
- **Fit score: MODERATE (structural relevance for the two-sector framing; but investment is not modeled)**

---

### Candidate 4: Intergenerational Transmission of Human Capital
- **Fit rationale:** The library entry's framing of parental investment in children's education with credit constraints, and the decomposition of the intergenerational income correlation into channels, is partially relevant. The proposed research studies children's education decisions, and the hukou barrier is a policy-created environmental factor analogous to "school quality E_g" in the intergenerational transmission model's HC technology.
- **Key structural match:**
  - *Parental investment structure:* The library entry's timing (parent chooses I_g; child's HC forms; child earns adult income) maps naturally to the proposed setup (household/parent decides on child's education investment).
  - *Environmental input:* Hukou status functions like "educational environment E_g" — it is an institutional complement to investment that determines the return per unit invested.
- **Potential gap:** The intergenerational model focuses on cross-generation dynamics and the IGE — not on the within-generation investment decision. The proposed paper is static (or at most two-period: invest then earn) and focuses on optimal investment for given hukou status, not on intergenerational persistence. This model family would be an extension, not the baseline.
- **Closest canonical ancestor:** Becker-Tomes (1986) with credit constraints.
- **Fit score: MODERATE (good for extensions; wrong temporal focus for the baseline)**

---

## Recommended Baseline Model

**Recommended Baseline: Becker Human Capital Investment Model**

**Primary justification:**
The research hypothesis explicitly invokes Becker's human capital framework and the research puzzle is stated directly in terms of that framework's core objects (marginal return vs. marginal cost of education investment). The Becker general human capital model provides the correct equilibrium concept (individual optimality under competitive wages), the correct agent structure (single decision-maker choosing education investment level), and the correct timing (invest, then work at wages determined by education and the labor market). The hukou modification is then a clean, minimal extension that introduces a hukou-type parameter τ into the wage function, shifting the marginal benefit schedule for rural agents. This minimal modification preserves all the tractability of the Becker framework while creating the investment-gap result. The Persona Council's directive to make the escape-route non-monotonicity the headline result can be implemented by specifying the wage function with a threshold at a high education level — still within the Becker framework but with a non-standard (non-monotone) return schedule for rural agents.

**Canonical baseline setup (from library entry):**
- Agent: worker with innate ability θ; chooses education level e ∈ [0, ē] (continuous)
- Return function: competitive wage = w(e, θ) — marginal product of labor with human capital (e, θ)
- Cost: C(e) — increasing and convex (cost of obtaining education e); discount rate r
- Optimization: choose e* to maximize V(e) = w(e, θ) − C(e)/(1+r) (present value of lifetime earnings net of education cost)
- First-order condition: w_e(e*, θ) = C'(e*) · r (marginal return = marginal cost of funds)
- Equilibrium concept: individual optimality (no strategic interaction; competitive wages)

**Inheritance list (to hand off to Stage 4):**
- Agents: single household/child with innate ability θ, choosing education investment e ∈ [0, ē]
- Timing: two-period — period 0: education investment decision; period 1: labor market participation at wages determined by e, θ, and hukou status τ
- Information structure: perfect information about own θ, τ, and the wage function w(e, θ, τ); no information asymmetry
- Equilibrium concept: individual optimality (single-agent optimization; competitive labor market)
- Key constraint: individual rationality (invest iff V_rural(e*, θ, τ=rural) ≥ V(0) = outside option); optionally, borrowing constraint C(e) ≤ income + loan capacity

**What must be added or modified:**
1. *Hukou-augmented wage function:* Replace w(e, θ) with w(e, θ, τ) where τ ∈ {urban, rural} is the agent's registration type. For τ = rural, the wage is scaled down by a hukou penalty parameter: w(e, θ, rural) = δ · w(e, θ, urban) with δ ∈ (0, 1). This is the core modification.
2. *Escape-route threshold structure:* For rural agents, include a threshold education level ê(τ=rural) such that if e ≥ ê, the agent can access urban labor markets with probability p ∈ (0, 1], potentially earning w(e, θ, urban). This makes the marginal return schedule for rural agents non-monotone — decreasing for e < ê (hukou penalty applies), then jumping upward at e = ê (escape probability p applies). This generates the headline escape-route over-investment result.

---

## Recommended Extensions

**Recommended Extension 1: Education Under Credit Constraints**
- **Why natural:** Once the baseline Becker model with hukou returns is established, the welfare decomposition (N3) requires formally separating the return-side distortion (hukou wage penalty) from the cost-side distortion (borrowing constraints rural households face). The credit constraint model provides the formal apparatus for this decomposition.
- **What it adds:** Introduces a borrowing constraint C(e) ≤ y_rural (rural household income) for rural children. Then the total welfare loss from the first-best is decomposable: ΔW = ΔW_return (due to hukou wage penalty δ) + ΔW_cost (due to credit constraint). Policy implication: the relative magnitude of ΔW_return vs. ΔW_cost determines whether hukou reform or credit market development is the higher-priority policy instrument.
- **When to pursue:** After the baseline characterization (Propositions 1–3 on the investment gap and escape-route) is complete. The credit constraint extension forms the welfare decomposition section (Stage 9) of the paper.

**Recommended Extension 2: Intergenerational Transmission**
- **Why natural:** The paper's policy relevance is enhanced by asking: if hukou creates under-investment in the current generation of rural children, how does this compound across generations? The intergenerational transmission model provides a natural framework for this: under-investment by parents reduces child's inherited human capital, amplifying the hukou distortion across generations.
- **What it adds:** A two-generation extension showing that the urban-rural education gap Δe*(θ) generates a diverging human capital stock across generations, with the rate of divergence determined by the hukou barrier parameter δ and the intergenerational skill transmission parameter α. This converts the paper's single-period comparative statics into a long-run policy argument.
- **When to pursue:** Only after the baseline paper is complete. This extension is suited for a follow-on paper or a final section of the manuscript if length allows.

---

## Excluded Families

- **Roy Model / Occupational Choice:** Excluded as baseline because it takes human capital as given and analyzes sector selection; the proposed research takes sector access as given and analyzes investment. The Roy model is the sector-choice stage that follows the education investment stage — not the correct baseline.
- **Intergenerational Transmission:** Excluded as baseline because the research focuses on the static (or two-period) individual investment decision, not on intergenerational income dynamics. The IGE is not the target object of this paper.
- **Moral Hazard / Principal-Agent:** Excluded — there is no information asymmetry or hidden action in the basic model; education investment is observable and ability is parametric.
- **Signaling (Spence):** Excluded — the model explicitly treats education as building human capital (true productivity), not as a signal. Including signaling would require a separate information structure not in scope.
- **Screening:** Excluded — there is no mechanism designer choosing an allocation rule; the question is about an individual's optimal investment given a labor market return function.
- **Disclosure / Persuasion:** Excluded — no information transmission between agents; not relevant.
- **Mechanism Design:** Excluded — no designer in the model; policy analysis is comparative statics on the hukou parameter, not an optimal mechanism problem.

---

## Relabeling Check

**Is the proposed model a superficial relabeling of a classic model?**

**PARTIAL RELABELING FLAG — with important qualifications:**

The under-investment result — "lower expected returns → lower optimal investment for equal-ability agents" — IS a direct application of Arrow (1973) pre-market discrimination to the Chinese hukou context. Applying a group-specific wage penalty to the Becker framework and deriving Δe*(θ) > 0 requires no modification to the Arrow mechanism; it only relabels "minority group membership" as "rural hukou status." The Brutal Skeptic's concern from Stage 3 is confirmed: the main under-investment proposition, stated alone, is a superficial relabeling of Arrow (1973) in the Becker framework.

**However, the following elements are NOT present in Arrow (1973) and constitute the original contribution:**

1. **The escape-route non-monotonicity (N2):** Arrow (1973) assumes a smooth, uniform wage penalty for the disadvantaged group. The hukou system has a specific institutional feature — education above a threshold (elite university admission) can confer urban labor market access with probability p. This generates a non-monotone marginal benefit schedule for rural agents that does not exist in Arrow's setup. The result that high-ability rural agents may invest MORE than equally-able urban agents is not derivable from Arrow; it is a genuine new result.

2. **The welfare decomposition by channel (N3):** Arrow (1973) characterizes the return differential as a market failure caused by employer discrimination. In the hukou model, the barrier is an institutional parameter δ that is (a) directly policy-manipulable, and (b) potentially commingled with a credit market failure affecting rural households. Decomposing the total welfare loss into return-side (δ) and cost-side (credit constraint) components, and characterizing their relative magnitudes, has no counterpart in Arrow.

3. **The hukou barrier as a structural policy parameter (N5):** Arrow's wage penalty is an equilibrium outcome of employer preferences and cannot be directly parameterized for reform analysis. The hukou penalty δ is a legal-administrative parameter that can be set by policy — which enables a different type of welfare analysis (reform comparative statics on δ).

**Conclusion:** The paper must be structured so that the relabeled result (under-investment for low-to-middle ability rural children) is presented as a benchmark proposition — straightforwardly derived and not claimed as the novel contribution — and the escape-route non-monotonicity is the paper's headline result.

---

## Primitives Inheritance Handoff to Stage 4

```
CANONICAL MODEL MATCH HANDOFF TO STAGE 4
==========================================
Baseline model family:    Becker Human Capital Investment Model
Canonical ancestor:       Becker (1964) general human capital; the
                          individual education investment problem

Inherit from the canonical model:
  - Agents:               Single individual (child/household) with innate
                          ability θ ∈ [0, ∞), choosing education investment
                          e ∈ [0, ē] (continuous)
  - Timing:               Two-period: (0) education investment decision;
                          (1) labor market entry with wages determined by
                          (e, θ, τ)
  - Information structure: Perfect and complete — agent knows own θ, τ,
                           and the wage function w(e, θ, τ) for all e
  - Equilibrium concept:  Individual optimality (single-agent);
                          competitive labor market (wages = marginal
                          product conditional on registration status)
  - Key constraint type:  Individual rationality (IR): invest iff
                          V(e*, θ, τ) ≥ V(0, θ, τ) = outside option

Modify from the canonical model:
  - Wage function: Replace uniform w(e, θ) with hukou-segmented
    w(e, θ, τ): for τ = urban, w(e, θ, urban) = standard Becker return;
    for τ = rural, w(e, θ, rural) = δ · w(e, θ, urban) + escape(e, θ)
    where δ ∈ (0, 1) is the hukou penalty parameter and escape(e, θ)
    is the escape-route term (see New Element 1 below).
  - Agent types: Two types τ ∈ {urban, rural} with identical ability θ
    and identical cost function C(e). Type is exogenous and unalterable
    except through the escape route.

New elements not in the canonical model:
  - Element 1 — Escape-route threshold: For rural agents only, define
    a threshold education level ê such that e ≥ ê triggers access to
    urban labor market with probability p(e; ê) ∈ [0, 1] (increasing
    in e for e ≥ ê). The rural agent's effective wage becomes:
    w(e, θ, rural) = [1 − p(e; ê)] · δ · w(e, θ) + p(e; ê) · w(e, θ)
                   = [δ + (1−δ) · p(e; ê)] · w(e, θ)
    This makes the marginal benefit schedule non-monotone for rural
    agents: MB_rural decreases (due to δ < 1) for e < ê, then jumps
    at ê due to p(ê) > 0. This generates the headline over-investment
    result for high-θ rural agents.
  - Element 2 — Dual-type comparative statics: The paper introduces
    a type-comparison operator: for given θ, compare e*_urban(θ) vs.
    e*_rural(θ). The sign and magnitude of Δe*(θ) = e*_urban − e*_rural
    is the core object of analysis, as a function of (δ, ê, p, θ, C).

Confirmed NOT a superficial relabeling: PARTIAL — the under-investment
  result (Δe*(θ) > 0 for low/mid θ) is a direct application of Arrow
  (1973) and must be framed as a benchmark, not the main contribution.
  The escape-route non-monotonicity (Δe*(θ) < 0 for high θ near ê)
  and the welfare decomposition are NOT in Arrow and are the genuine
  original contributions of this paper.
```

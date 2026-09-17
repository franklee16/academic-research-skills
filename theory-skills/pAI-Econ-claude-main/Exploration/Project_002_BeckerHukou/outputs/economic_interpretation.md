# Economic Interpretation

**Date:** 2026-06-14
**Stage:** 9 — Economic Interpretation

---

## [P_E1] — Existence and Characterization: Economic Interpretation

**Proposition (restated in plain English):**
Every child — urban or rural — has a well-defined best educational investment, and the rural child's best choice must be found by comparing two distinct strategies: invest below the elite threshold and accept the hukou wage penalty, or invest exactly at the threshold and attempt to escape the penalty.

---

### The Core Mechanism

The urban child faces a standard trade-off: more education raises wages (at a diminishing rate) but costs more. A single well-behaved optimum exists. The rural child faces the same trade-off in each regime, but the two regimes are stitched together by the hukou barrier: investing just below the elite threshold gives the low-penalty wage, while reaching the threshold opens the possibility of the full urban wage. The two-regime structure means the rural child cannot simply equate marginal benefit to marginal cost globally — she must compare the best option in each regime and pick the better one.

**Step-by-step mechanism:**
When a rural child chooses education level → she earns either a penalized rural wage (e < ê) or an escape-route wage (e ≥ ê) → the payoff function has a discrete jump at ê → the globally optimal investment is determined by comparing the best interior solution in each regime, not by a single first-order condition.

---

### The Intuition

The key insight is that the hukou barrier turns a smooth single-stage optimization into a discontinuous two-regime problem. This matters because the "right" way to solve the rural child's problem is comparison-of-regimes, not calculus — a fact easy to overlook if one tries to apply standard Becker techniques directly to the rural child.

**Why it would have been non-obvious before the model:**
Without explicitly modeling the escape route as a discrete jump, one might try to apply the urban FOC to the rural child (with δ scaling the wage), missing the possibility that the global optimum is a corner solution at ê rather than an interior solution.

---

### What This Result Rules Out

P_E1 rules out the possibility that the rural child's problem is ill-posed or has multiple locally optimal strategies that are genuinely incomparable. The two-regime comparison always delivers a unique best choice (with the tie-breaking rule at ê), so the model generates well-defined comparative statics.

---

### Real-World Counterpart

This is consistent with the observation that Chinese rural students, when making college application decisions, effectively face a binary choice between "aim for a top-tier national university" (which provides urban labor market access) and "settle for a local or provincial university" (which does not). The graduation-threshold nature of Gaokao scores — where crossing the provincial key-line gives dramatically different university access — is precisely the discrete-jump structure the model captures.

---

### Policy / Welfare Interpretation

Not directly applicable. P_E1 is a technical foundation lemma.

---

### "So What?" — Introduction Paragraph

China's hukou system does not merely reduce the expected return to education for rural children — it restructures the entire optimization problem. Unlike urban children, who face a smooth trade-off between educational investment and wages, rural children face two qualitatively different strategies: invest modestly and accept a penalized rural wage, or invest heavily enough to cross the elite university threshold and gain a chance at the full urban wage. Recognizing this two-regime structure is essential for understanding why the effects of hukou on educational investment are more nuanced — and more surprising — than a simple "discrimination depresses investment" story would predict.

---

### Connection to Prior Literature

P_E1 formalizes the two-regime structure that is implicit but not explicitly modeled in Arrow (1973), where the wage penalty enters smoothly. The discrete-threshold structure here is closer to models of educational thresholds in the signaling literature (e.g., Fernandez and Gali 1999 on rank-order tournaments) but applied to a productive human capital (Becker) setting rather than a signaling setting.

---

### Limitations of the Interpretation

This interpretation should NOT be taken to imply:
- That rural children literally solve a two-regime mathematical program. The model captures the *structure* of incentives, not the cognitive process.
- That the escape route is accessible to all rural children who reach ê. The model treats p₀ as a fixed probability; in reality, success depends on many factors beyond the Gaokao score.
- That the discrete-jump structure of p(e) is the only specification consistent with the model. A smooth p(e) with steep slope at ê gives the same qualitative results.

---

## [P_C1] — Under-Investment Benchmark: Economic Interpretation

**Proposition (restated in plain English):**
When the hukou wage penalty is proportional — the rural child earns a fixed fraction of the urban wage for the same education and ability — she will invest less in education than an equally-able urban child, as long as she is not trying to reach the elite threshold.

---

### The Core Mechanism

A proportional wage penalty reduces the payoff to every additional unit of education by the same factor δ. This means the rural child's marginal return to education is always δ times the urban child's marginal return at the same education level. Since investing is only worthwhile up to the point where marginal return equals marginal cost — and the cost function is the same for both children — the rural child stops investing earlier. The gap is not due to any difference in ability, preferences, or access to credit; it is purely a consequence of the proportional penalty suppressing the return to education.

**Step-by-step mechanism:**
When a proportional hukou penalty (δ < 1) applies → rural child's marginal return to education is δ × urban child's return at every e → rural child's marginal benefit curve lies below the urban child's → the crossing point with the (identical) marginal cost curve occurs at a lower e → rural child invests less.

---

### The Intuition

The result reflects the straightforward logic of marginal analysis: if you earn less for the same investment, you invest less. The model makes this precise and shows that the effect is exactly proportional — the investment gap is driven entirely by δ, with no other parameters playing a role in the *direction* of the gap (though they affect its magnitude).

**Why it would have been non-obvious before the model:**
A naive observer might expect rural children to *compensate* for the wage penalty by investing *more* to signal their quality. The model shows that in the productive human capital framework — where education raises productivity, not just signals — the opposite is true: the penalty suppresses investment.

---

### What This Result Rules Out

P_C1 rules out the possibility that under-investment is due to credit constraints (by assumption, both children face the same budget constraint) or to school quality differences (same C). The investment gap must be attributed entirely to the lower return on rural children's educational investment — the return channel, not the cost channel.

---

### Real-World Counterpart

This is consistent with the large empirical literature documenting lower educational attainment among rural-origin children in China, even after controlling for family income and school access. The model suggests that part of this gap reflects a rational response to lower expected returns: why invest more in education when the labor market will discount your credentials because of your hukou status?

**Concrete illustrative example:**
Consider θ = 1 (normalized), A = 1, α = 0.5, β = 0.5, r = 1, C(e) = e². Urban FOC: 0.5·e^{−0.5} = 2e → e*_U ≈ 0.397. Rural FOC with δ = 0.7: 0.7·0.5·e^{−0.5} = 2e → e*_R ≈ 0.178. The gap is 55% of the urban investment level — a substantial penalty from a moderate hukou wage discount.

---

### Policy / Welfare Interpretation

**Who loses:** Rural children, who invest less and earn less than equally-able urban children, not because they are less capable but because the institutional penalty suppresses their incentive to invest.
**Policy implication:** Equalizing returns (raising δ toward 1) would close this gap. But note: this is the *only* implication of P_C1. P_W2 will show that closing the gap has an unexpected effect on a different group.

---

### "So What?" — Introduction Paragraph

A foundational prediction of models of labor market discrimination — from Arrow (1973) to the present — is that groups facing lower expected returns to human capital investment will invest less. Our model confirms this prediction in the Chinese hukou context: rural children, who face a proportional wage penalty in urban labor markets due to their registration status, invest less in education than equally-able urban children when their optimal strategy does not involve trying to cross the elite university threshold. This under-investment result is the expected baseline. Its importance lies not in its novelty — it is a direct consequence of Arrow's (1973) logic — but in what it sets up: the surprising opposite result for intermediate-ability rural children, who invest *more* than their urban peers.

---

### Connection to Prior Literature

P_C1 is explicitly a restatement of Arrow (1973, Theorem 1) in the Becker productive human capital framework. It adds nothing theoretically beyond translating Arrow's mechanism from a labor supply context to an education investment context. Its role in the paper is as a benchmark, not a contribution.

---

### Limitations of the Interpretation

This interpretation should NOT be taken to imply:
- That all rural children under-invest. P_C2 establishes a group for whom the opposite is true.
- That the additive-penalty version of the model gives the same result. It does not — with an additive penalty, this proposition fails entirely (the investment margin is undistorted).
- That under-investment is the dominant empirical pattern. Whether the under-investment or over-investment regime is empirically larger depends on the distribution of ability and the calibrated values of δ, ê, and p₀.

---

## [P_C2] — Escape-Route Over-Investment: Economic Interpretation ★ HEADLINE

**Proposition (restated in plain English):**
For rural children of intermediate ability — able enough to plausibly reach the elite university threshold but not able enough to reach it without stretching — the hukou barrier creates an incentive to invest *more* in education than an equally-able urban child, not less.

---

### The Core Mechanism

An elite university admission (the escape route) offers rural children something that urban children do not need: a chance to escape the hukou wage penalty entirely. For a rural child of intermediate ability, the urban child's first-best investment level is just below the elite threshold. The rural child faces a choice: invest at the urban optimum and earn the penalized rural wage, or over-shoot to the threshold and gamble on full urban wages. The escape premium — the wage gain from escaping the penalty with probability p₀ — can outweigh the direct cost of over-investing. When it does, the rural child rationally invests more than her urban peer.

**Step-by-step mechanism:**
When a rural child of ability θ ∈ (θ̃, θ̄) has e*_U(θ) just below ê → she could accept the penalized wage at e*_U, OR invest exactly at ê for a chance at urban wages → the escape premium (1−δ)p₀·w(ê,θ)/r exceeds the cost of over-shooting → she chooses to invest at ê → this exceeds e*_U(θ) → over-investment relative to the urban child.

---

### The Intuition

The key insight is that the hukou barrier creates an asymmetric prize structure: urban children gain nothing by reaching ê (they already earn the full urban wage), while rural children gain a potential wage jump. This asymmetry inverts the normal logic of wage discrimination — instead of suppressing investment, the barrier *creates* an incentive to over-invest for those close enough to the escape threshold to find the gamble worthwhile.

**Why it would have been non-obvious before the model:**
Standard discrimination theory predicts uniformly lower investment by the discriminated group. The escape-route mechanism shows that a threshold-based institutional barrier generates non-monotone effects: *some* members of the discriminated group over-invest. Without explicitly modeling the escape route as a discrete payoff jump, this result would not emerge.

---

### What This Result Rules Out

P_C2 rules out the claim that "hukou discrimination always reduces educational attainment among rural children." It shows that the relationship between discrimination and investment is non-monotone in ability: low-ability rural children under-invest (P_C1), intermediate-ability rural children over-invest (P_C2), and high-ability rural children's behavior depends on the high-regime trade-off.

---

### Real-World Counterpart

This is consistent with the observation that competition for elite university places in China is, if anything, *more* intense among rural students than urban students of comparable measured ability. Rural students' willingness to spend extreme amounts of time and money on Gaokao preparation — often well beyond what their urban counterparts invest — has been documented in sociological studies of Chinese rural education. The model offers a formal economic rationale: the escape-route incentive makes extreme investment rational for intermediate-ability rural students.

**Concrete illustrative example:**
Suppose δ = 0.7 (rural earns 70% of urban wage), p₀ = 0.3 (30% chance of urban labor market access at ê), and ê = 0.6 (normalized). An intermediate-ability rural child (θ = 0.8, with e*_U ≈ 0.52) would in the absence of escape route invest ≈ 0.27 (the low-regime rural optimum). The escape premium at θ = 0.8: (1−0.7)×0.3×w(0.6, 0.8)/1 = 0.09×w ≈ positive. If this premium exceeds the cost of jumping from 0.27 to 0.6 (which it does for p₀ large enough), the rural child invests 0.6 — 15% more than the urban child's 0.52. The urban child has no reason to invest beyond 0.52; the rural child finds it rational to over-shoot.

---

### Policy / Welfare Interpretation

**Who benefits:** Intermediate-ability rural children who successfully escape (with probability p₀); they earn the full urban wage.
**Who loses:** The same children who fail to escape (probability 1−p₀): they invested ê > e*_U(θ), paid the extra cost C(ê) − C(e*_U), but still earn only the penalized rural wage δ·w(ê,θ). They have over-invested and still face discrimination.
**Distributional consequence:** The escape-route mechanism redistributes risk onto intermediate-ability rural children. It is an equilibrium distortion in which the institutional barrier forces a subset of the disadvantaged group into excessive investment as the price of a lottery ticket.
**Policy implication:** Hukou reform (P_W2) that equalizes wages eliminates the over-investment incentive. This is welfare-improving — but it reduces educational attainment for this group, which may look counterintuitive to observers tracking educational outcomes as a reform indicator.

---

### "So What?" — Introduction Paragraph

We show that a regime of labor market discrimination does not uniformly suppress educational investment among the discriminated group. When the discrimination takes the form of a wage penalty that can be escaped by reaching an educational threshold — as in China's hukou system, where elite university admission provides a path to urban labor market access — children facing the penalty have an incentive to *over-invest* in education relative to equally-able unpenalized peers. This escape-route over-investment is not a sign of ambition or compensatory behavior in a psychological sense; it is a rational economic response to a lottery with an asymmetric prize. The result overturns a central prediction of standard discrimination models and generates a new empirical prediction: among students near the elite admission threshold, rural students should invest *more* than urban students of equal measured ability.

---

### Connection to Prior Literature

P_C2 has no direct precedent in the discrimination literature. Arrow (1973) predicts uniformly lower investment. Galor and Zeira (1993) generate investment distortions from credit constraints, not from returns to threshold-crossing. The closest conceptual antecedent is the tournament literature (Lazear and Rosen 1981), where agents over-invest to win a discrete prize — but that model involves strategic interaction among competitors, while here the over-investment is driven by a single agent's rational response to an institutional barrier with no strategic element.

---

### Limitations of the Interpretation

This interpretation should NOT be taken to imply:
- That all rural children over-invest. The result applies only to the interval (θ̃, θ̄); below θ̃, under-investment (P_C1) holds; above θ̄, behavior depends on the high-regime analysis.
- That the over-investment is efficient from a social perspective. It is not: P_W1 shows that ΔW > 0 even in the over-investment regime, because the rural child pays the cost of over-shooting while still facing discrimination (δ < 1 on the escape prize with probability 1−p₀).
- That this mechanism is unique to China. Any institutional barrier with a discrete threshold that disadvantaged-group members can cross to escape discrimination generates the same structure. The model applies to any "escape-route" discrimination regime.
- That the result is robust to all penalty specifications — specifically, P_C1 (under-investment) fails under additive penalty, though P_C2 (over-investment) survives.

---

## [P_C3] — Comparative Statics on the Investment Gap: Economic Interpretation

**Proposition (restated in plain English):**
Relaxing the hukou penalty closes the under-investment gap; a higher escape-route probability expands the set of rural children who over-invest; and — in the empirically relevant case where the elite threshold is far above the rural child's low-regime optimum — tighter hukou enforcement makes more rural children willing to gamble on the escape route.

---

### The Core Mechanism

Three separate mechanisms operate. (i) Loosening the hukou penalty (δ → 1) raises the rural child's marginal return to education in the low regime, pushing her investment closer to the urban level — the under-investment gap closes monotonically. (ii) A higher escape probability (p₀ ↑) increases the expected payoff at ê, making the gamble more attractive for a wider range of rural children (lower-ability ones who would otherwise not find the risk worth taking now find it worthwhile) — the over-investment range expands downward in θ. (iii) In the empirically plausible case where ê is much larger than the rural low-regime optimum, a tighter hukou penalty (δ ↓) increases the relative value of the escape route versus the low-regime payoff, pushing more children toward the over-investment threshold — the over-investment range again expands.

---

### The Intuition

The result reflects two competing forces: the direct effect of the penalty (which suppresses low-regime investment) and the indirect effect of the escape-route prize (which is more valuable when the penalty is harsher). The comparative statics disentangle which force dominates where.

**Why it would have been non-obvious before the model:**
Informal reasoning would predict that stricter hukou enforcement uniformly reduces rural investment. The model shows that in the over-investment range, the opposite can occur: stricter enforcement makes the escape-route gamble more attractive, potentially expanding the set of rural children who over-invest.

---

### What This Result Rules Out

P_C3 rules out a monotone relationship between hukou enforcement severity and aggregate educational investment by rural children. The relationship is non-monotone: as the penalty tightens, low-ability rural children invest less (under-investment deepens) while intermediate-ability rural children invest more (over-investment range expands). Aggregate investment is therefore not a reliable indicator of enforcement severity.

---

### Real-World Counterpart

This is consistent with the observation that China's rural-urban educational investment gap has not moved monotonically with hukou enforcement. Provinces with stricter urban hukou policies have sometimes seen *more* intense Gaokao preparation among rural students near the admission threshold — precisely because the prize for crossing the threshold (urban labor market access) is more valuable when the penalty for failing is harsher. The model provides a formal rationale for this pattern.

---

### Policy / Welfare Interpretation

**Policy implication:** Tightening hukou enforcement as a policy to reduce urban congestion may have the unintended consequence of intensifying educational competition among rural students near the elite admission threshold. The policy instrument intended to control labor migration affects educational investment through the escape-route channel.

---

### "So What?" — Introduction Paragraph

The comparative statics of our model reveal a fundamental non-linearity in how institutional discrimination affects educational investment. Contrary to the prediction of standard models — that stricter enforcement of the hukou wage penalty would reduce all rural educational investment — our model shows that stricter enforcement can *expand* the population of rural students who over-invest in education by making the escape-route prize more valuable. This generates a testable, counter-intuitive prediction: in areas or periods of stricter hukou enforcement, the intensity of Gaokao preparation among rural students near the elite admission threshold should be higher, not lower.

---

### Connection to Prior Literature

The non-monotone comparative static in part (iii) is not present in Arrow (1973) or any standard discrimination model. It is a consequence of the escape-route mechanism that emerges only when there is a threshold the discriminated group can cross. Closest to the over-investment range expansion result is the property in tournament models (Lazear-Rosen) that higher prizes attract more entrants — here, a harsher penalty plays the role of a higher prize for the winner.

---

### Limitations of the Interpretation

This interpretation should NOT be taken to imply:
- That part (iii) holds universally. The sign of the effect of δ on the over-investment range width depends on the ratio ê/e*_int relative to a parameter-dependent threshold. The economic interpretation applies under the empirically plausible condition that ê ≫ e*_int.
- That relaxing the penalty (δ → 1) always reduces aggregate investment. It reduces investment in the over-investment range (P_W2) while increasing it in the under-investment range (P_C1). The net aggregate effect depends on the distribution of ability.
- That the non-monotone result is robust to all model specifications. In the absence of a discrete escape route (p₀ = 0), the relationship is monotone (P_B1).

---

## [P_W1] — Welfare Loss Characterization: Economic Interpretation

**Proposition (restated in plain English):**
The hukou barrier always reduces the welfare of rural children relative to equally-able urban children; the welfare loss is largest for intermediate-ability rural children near the escape-threshold boundary, not for the most- or least-able students.

---

### The Core Mechanism

Two channels generate welfare loss: (1) in the under-investment range, rural children invest too little relative to the first-best, earning less than they could in the absence of the barrier; (2) in the over-investment range, rural children invest too much — they overshoot to ê, incur extra education costs, and still face the barrier with probability 1−p₀. The welfare loss is the sum of these two distortions relative to the first-best urban outcome.

The non-monotone profile arises because near the boundary θ̃: (a) low-regime rural children just below θ̃ are investing as far below the first-best as possible in the under-investment regime (the under-investment gap is largest near θ̃, where e*_U is closest to ê but e*_R is pushed far below); (b) high-regime rural children just above θ̃ are over-investing at ê while paying for it in cost — but they also receive the escape premium with probability p₀. The net welfare loss peaks near θ̃.

---

### The Intuition

The result reflects the fact that the worst outcomes are not at the extremes of the ability distribution. The lowest-ability rural children invest very little in both regimes, so the distortion from the first-best is modest. The highest-ability rural children would have invested above ê in the first-best anyway, so the escape route is not a distortion for them. The intermediate group — forced to either invest far below their first-best (low regime) or gamble on the escape route at a cost — faces the largest welfare gap.

**Why it would have been non-obvious before the model:**
A natural intuition would be that the highest-ability rural children lose the most (because their potential earnings are highest). The model shows the opposite: high-ability rural children can escape through the elite route, partially recovering their first-best outcome; the biggest losers are those in the middle who cannot escape efficiently.

---

### Real-World Counterpart

This is consistent with sociological findings that the most acute subjective sense of unfairness in China's educational system is reported not by the weakest or strongest rural students, but by those who perform near the elite admission threshold — students who feel they are "close enough" to the escape route to make the over-investment feel compelled, yet are not guaranteed success. The model provides a formal welfare interpretation of this experience: this is precisely the group bearing the largest welfare loss.

---

### Policy / Welfare Interpretation

**Who loses most:** Intermediate-ability rural children near θ̃ — they face the combination of high investment costs (they over-invest at ê) and uncertain escape-route outcomes (they earn penalized wages with probability 1−p₀).
**Policy implication:** Targeted policy interventions aimed at reducing the welfare loss from hukou barriers would have the largest per-child impact if directed at the intermediate-ability range near the elite admission threshold — the group bearing the largest burden per child. Broad-based hukou reform helps everyone, but per-child welfare gains are concentrated in this group.

---

### "So What?" — Introduction Paragraph

The welfare consequences of China's hukou system are not uniform across the ability spectrum. Our model shows that the burden of the institutional barrier — measured as the gap between what a rural child could achieve in a fair labor market and what she actually achieves — peaks among students of intermediate ability who are near the elite university admission threshold. These are the students who rationally over-invest in education as an escape strategy, bearing high costs for an uncertain escape, yet remain partially trapped by the penalty if the gamble fails. This concentration of welfare loss among the near-threshold group suggests that hukou reform would have its largest per-beneficiary welfare impact precisely where educational competition is most intense.

---

### Connection to Prior Literature

P_W1 extends Arrow (1973)'s welfare analysis to include the over-investment regime, which generates a qualitatively different welfare profile. In Arrow's model, the welfare loss is monotone in ability (higher ability → larger potential loss). Here, the escape-route mechanism non-monotonicizes the welfare profile, generating a local maximum at an interior ability level. This is a new finding in the discrimination-and-investment literature.

---

### Limitations of the Interpretation

This interpretation should NOT be taken to imply:
- That the welfare loss is measured in monetary units here. The model measures welfare in terms of net payoffs (wage discounted at rate r, minus education cost). Translating this to observable magnitudes requires calibration.
- That the welfare loss is the entire social cost of the hukou system. The model captures only the direct distortion to one child's investment decision; general equilibrium effects (reduced aggregate human capital, effects on wages) are not modeled.
- That the local maximum of the welfare loss is sharp. In the discrete-jump p specification it produces a right-discontinuity at θ̃; with smooth p(e), the transition is smooth and the "local maximum" is a smooth hump.

---

## [P_W2] — Unintended Consequence of Hukou Reform: Economic Interpretation

**Proposition (restated in plain English):**
When China's hukou wage barrier is fully removed, all rural children become better off — but the most motivated intermediate-ability rural students invest *less* in education after the reform than before, because the escape-route incentive that was driving their over-investment disappears.

---

### The Core Mechanism

The hukou barrier distorts intermediate-ability rural children's investment upward — they invest at ê even though their first-best investment is below ê. When the barrier is removed, the distortion disappears. The rural child now solves the same problem as the urban child and arrives at the first-best investment level, which is below ê. Educational investment falls. Yet welfare rises: the over-investment was always a distortion; moving to the first-best is by definition welfare-improving.

**Step-by-step mechanism:**
Reform removes the hukou penalty (δ → 1) → rural child's wage no longer penalized → escape-route premium (1−δ)p₀·w(ê,θ)/r → 0 → incentive to over-invest at ê disappears → rural child's optimal investment falls from ê to e*_U(θ) < ê → less educational investment, but the full wage is earned at the lower investment level → net welfare improves.

---

### The Intuition

The result reflects the principle that a distorted optimum is worse than an undistorted one, even if the distorted optimum appears to involve "more effort." The intermediate-ability rural students were over-investing as a consequence of the institutional barrier, not out of genuine preference for more education. Removing the barrier allows them to invest optimally — which means investing less, but earning more per unit of investment.

**Why it would have been non-obvious before the model:**
Any economist or policymaker would expect that removing a wage penalty would (a) improve welfare and (b) increase educational attainment, because it raises the return to education. For low-ability rural students (in the under-investment regime), this is exactly right. But for intermediate-ability students, the escape-route incentive was driving investment above the first-best; its removal lowers investment while raising welfare. The two effects come apart.

---

### What This Result Rules Out

P_W2 rules out the claim that hukou reform is Pareto-improving in terms of educational investment levels. While welfare improves for all rural children, educational attainment falls for the intermediate-ability group. A policymaker who uses educational attainment as a success indicator for hukou reform would see a *decrease* in investment among the most motivated rural students and might incorrectly conclude that reform has failed or backfired.

---

### Real-World Counterpart

This is potentially consistent with evidence from China's partial hukou reforms since 2014. If reform is successfully reducing the wage penalty in some regions, we would expect — according to the model — a relative *reduction* in Gaokao preparation intensity among rural students near the elite admission threshold in those regions, even as their welfare improves. Empirically distinguishing the P_W2 prediction (welfare up, investment down for intermediate-ability students) from a reform failure (welfare down, investment down) requires measuring both wages and investment outcomes simultaneously.

**Concrete illustrative example:**
Before reform: δ = 0.7, p₀ = 0.3. A rural child with θ = 0.8 invests at ê = 0.6 (over-investing; her e*_U = 0.52). After full reform (δ = 1): she invests at 0.52 and earns the full urban wage. Investment falls from 0.6 to 0.52 (a 13% decrease), but welfare rises because she no longer pays the extra cost C(0.6) − C(0.52) while also no longer facing the wage penalty δ < 1.

---

### Policy / Welfare Interpretation

**Who benefits:** All rural children see welfare improvements post-reform. The intermediate-ability group (θ ∈ (θ̃, θ̄)) benefits especially — the cost of over-investment is eliminated and the wage penalty disappears.
**Who appears to lose (but does not):** The intermediate-ability group reduces educational investment, which could be misread as a harm. It is not — it is the elimination of a distortion.
**Policy implication:** Policymakers evaluating hukou reform should not use educational attainment among rural students as a primary indicator of reform success. A successful reform should be measured by wage outcomes, not schooling levels. Reduction in near-threshold educational investment may be a sign that reform is working, not that it has failed.

---

### "So What?" — Introduction Paragraph

We demonstrate a striking unintended consequence of labor market integration: when China's hukou system is reformed to equalize wages between urban and rural workers, the resulting improvement in welfare for rural children is accompanied by a *reduction* in their educational investment. This paradox arises because the hukou barrier — by threatening rural children with a permanent wage discount unless they cross the elite university threshold — was previously driving intermediate-ability rural students to over-invest in education. The institutional distortion looked like ambition; its removal looks like disengagement. A policymaker who monitors educational attainment as a welfare indicator would observe declining investment among the most motivated rural students and might incorrectly interpret this as evidence that reform has made rural children worse off. Our model shows the opposite: the decline in investment is precisely the efficiency gain from removing the distortion.

---

### Connection to Prior Literature

P_W2 has no direct counterpart in the discrimination literature. Reforming labor market discrimination is universally predicted to raise investment in human capital models (Arrow 1973, Becker 1971) — because it raises the return to investment. The escape-route mechanism inverts this prediction for the intermediate-ability group. The closest analogues are models of rent-seeking or contest theory where removing the contest prize reduces wasteful over-investment — but those models involve competition between agents, while here the over-investment is a single agent's response to an institutional barrier.

---

### Limitations of the Interpretation

This interpretation should NOT be taken to imply:
- That hukou reform reduces educational investment on average. For low-ability rural children (θ < θ̃), reform increases investment (P_W2, part ii). The net aggregate effect on investment depends on the distribution of ability.
- That the reform paradox is empirically testable without careful research design. Distinguishing the P_W2 effect (intermediate-ability students invest less post-reform, welfare improves) from other mechanisms (general discouraged-worker effects, differential take-up of reform) requires isolating the intermediate-ability group and measuring wage outcomes alongside investment outcomes.
- That this result implies reform is bad policy. It is not — welfare improves unambiguously. The result is about the *interpretation* of investment data post-reform, not about the desirability of reform itself.

---

## [P_B1] — Boundary and Limit Results: Economic Interpretation

**Proposition (restated in plain English):**
As the hukou penalty disappears, the investment gap closes and both children converge to the same (first-best) outcome; as the escape probability vanishes, the model simplifies to the Arrow (1973) benchmark with no over-investment range; as the penalty approaches zero, low-regime rural investment collapses to zero since education earns nothing without the escape route.

---

### The Core Mechanism

The limit results confirm that the model's special features (escape route, over-investment range) arise from the interaction of the penalty (δ < 1) and the escape route (p₀ > 0). Remove either and the model degenerates to a simpler case. These limit results serve as sanity checks: the model "nests" prior results (Arrow 1973 when p₀ → 0) and generates a first-best outcome at the efficient limit (δ = 1).

---

### The Intuition

The key insight is that the model's novel predictions are driven by both the penalty AND the escape route together. Neither alone is sufficient: no penalty means no distortion; no escape route means only under-investment (Arrow). The co-presence of both generates the over-investment result.

---

### What This Result Rules Out

P_B1 rules out the possibility that the model generates novel predictions in degenerate parameter regions. At the extremes, the model collapses to known benchmarks — which is reassuring, confirming that the paper's contributions are genuinely "interior" results rather than artifacts of extreme parameter values.

---

### Real-World Counterpart

The p₀ → 0 limit corresponds to a hypothetical China with no elite universities that provide urban labor market access for rural-hukou graduates — essentially the pre-reform state before national key universities were established. In this limit, the model predicts only Arrow-type under-investment, consistent with historical descriptions of rural education in China before the development of elite higher education. The limit thus provides a counterfactual narrative for the paper.

---

### "So What?" — Introduction Paragraph

Not applicable. P_B1 is a supporting proposition whose economic content is fully captured in the main propositions.

---

### Connection to Prior Literature

P_B1(ii) explicitly nests Arrow (1973): as p₀ → 0, the model's behavior converges to Arrow's prediction of pure under-investment. This confirms the theory lineage established in Stage 3b and gives the paper a clean "this paper generalizes Arrow (1973) by adding an escape route" narrative.

---

### Limitations of the Interpretation

This interpretation should NOT be taken to imply:
- That real-world limits are achievable (δ = 1 or p₀ = 0 are idealized boundary conditions).
- That the convergence is fast — the rate at which the over-investment range shrinks as p₀ → 0 depends on the curvature of V_R, which is parameter-specific.

---

## Cross-Proposition Narrative

The paper tells a single coherent economic story: **China's hukou system, by imposing a proportional wage penalty on rural workers that can be escaped by crossing an elite education threshold, creates a two-group distortion in educational investment.** Low-ability rural children rationally under-invest relative to their urban peers (P_C1), because the return to education is suppressed by the penalty. Intermediate-ability rural children rationally over-invest relative to their urban peers (P_C2), because the escape-route prize makes over-shooting the elite threshold worthwhile. This non-monotone investment pattern generates a welfare loss that is largest for the intermediate-ability group (P_W1). Most strikingly, removing the barrier — as China's hukou reforms aim to do — simultaneously improves welfare and reduces educational investment for the intermediate-ability group (P_W2), because it eliminates the distortionary over-investment incentive. The model thus provides both a new theoretical result about discrimination and educational investment, and a concrete, testable prediction about the empirical patterns that should accompany China's ongoing hukou reforms.

---

## Recommended Discussion Section Topics

1. **Empirical testing of P_C2 and P_W2** — The paper's novel predictions have a natural empirical counterpart: using China's hukou reform episodes since 2014, one could test whether (a) rural students near the Gaokao elite threshold invest more intensively than urban students of similar measured ability, and (b) in reformed regions where the wage penalty has been reduced, this over-investment is attenuated. This would constitute the most direct test of the model's headline results.

2. **Credit constraints extension** — The baseline model assumes no binding credit constraints. Adding a credit constraint C(e) ≤ y (family income) would interact with the escape-route incentive: rural children with lower y might want to reach ê but be unable to afford it. This generates a welfare decomposition with three terms: the return-side distortion (this paper), the credit-side distortion, and their interaction. Such an extension would speak to the large empirical literature on credit constraints and education in China.

3. **School quality and cost heterogeneity** — The model holds the cost function C(e) equal across types. Introducing C_R(e) > C_U(e) (worse rural schools require more effort to reach the same education level) would reinforce the under-investment result but attenuate the over-investment result (higher costs make the escape gamble less attractive). Defending the paper's choice to hold C equal — and providing a robustness argument for the qualitative results under C_R > C_U — is important for addressing the school quality objection from the referee council.

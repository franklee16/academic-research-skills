# Identification for Asset Pricing Writing Style

**Source Papers:** Kelly & Ljungqvist ("Asymmetric Information"), Chang et al. ("Testing Disagreement Models")
**Typical Journals:** Journal of Finance, Journal of Financial Economics, Review of Financial Studies, Journal of Financial Economics
**Field Code:** `identification`

---

## Core Blueprint for Causal Identification

Both source papers share a common rhetorical and structural blueprint for establishing causality. Every identification paper must follow these six steps:

1. **State the Identification Problem Upfront:** Acknowledge endogeneity issues (omitted variables, reverse causality)
2. **Introduce the "Shock" as a Solution:** Present a specific, exogenous event as a "natural experiment"
3. **Argue for Exogeneity:** Provide institutional detail and empirical tests to prove the shock is unrelated to firm fundamentals
4. **Use a Clean Empirical Design:** DiD with matched controls, event studies, or IV to isolate the treatment effect
5. **Validate the Channel:** Show the shock affects the proposed mechanism before showing it affects the final outcome
6. **Rule Out Alternatives:** Test for and dismiss other potential explanations

---

## Two Complementary Voices

### Voice 1: Authoritative & Direct (Kelly & Ljungqvist Style)

Confident, declarative, economically precise. Focuses heavily on institutional details to build narrative.

**Framing the problem:**
> "Testing if and how information asymmetry affects asset pricing poses a tricky identification challenge... To overcome such problems of simultaneity, we need a source of exogenous variation."

**Presenting the solution:**
> "We identify three natural experiments that affect information asymmetry through their effect on the extent of research coverage by sell-side equity analysts."

**Arguing for exogeneity (two-pronged attack):**
1. **Plausibility from institutional details:** Quote press releases, describe the real-world event that makes the shock clearly exogenous
2. **Empirical validation:** Directly test and report: "Closure-induced terminations are neither economically nor statistically related to subsequent earnings surprises (p-value = .965). This is consistent with closure-induced terminations being uninformative about future performance and thus plausibly exogenous."

**Handling threats to validity:**
> "Of course, each of the forty-three brokerage closures results in multiple terminations on the same day, which could cause cross-sectional dependence... A popular way to adjust... is to estimate standard errors by using a block bootstrap."

### Voice 2: Methodologically Meticulous & Cautious (Chang et al. Style)

Written for an audience deeply concerned with econometric validity. Self-conscious about assumptions. Uses "plausibly exogenous" and "clean controls."

**Framing the problem:**
> "Prior empirical studies typically explore cross-sectional correlations... A clean identification strategy requires a randomly assigned shock to investor disagreement."

**Presenting the solution (staggered rollout):**
> "We exploit the staggered implementation of the EDGAR system by the SEC as a shock to investor disagreement... Helpfully, for identification purposes, the SEC randomly assigned firms to 1 of 10 implementation waves."

**Arguing for exogeneity (design-based):**
> "Conditionally random assignments and staggered implementation significantly reduce endogeneity concerns... a firm's inclusion in EDGAR can be viewed as a surprise, reducing concerns that firms, analysts, or investors altered their behavior in anticipation."

**Addressing modern DiD concerns:**
> "To avoid biases that can arise in staggered DD approaches with time-varying treatments and treatment effect heterogeneity (Baker, Larcker, and Wang (2021)), we select 'clean' control firms... our research design is equivalent to Cengiz et al.'s (2019) stacked-regression estimator."

**Defending the exclusion restriction:**
> "A causal interpretation of these findings requires that [shock] affects [outcome] only through its effect on [channel] and not directly or through another channel... We investigate the plausibility of this identifying assumption through the lens of the leading alternative explanation..."

---

## The Barbell Style (Synthesis)

The most powerful approach combines both voices:

1. **Start with the direct, confident claim** (Kelly & Ljungqvist voice):
   > "We provide evidence for the importance of X by using a natural experiment..."

2. **Immediately follow with meticulous, cautious defense** (Chang et al. voice):
   > "Our identification strategy exploits the staggered implementation of Y, which provides conditionally random variation..."

---

## Three-Part Identification Section Structure

### Part 1: Confident Claim
State what you do and why it works, in clear declarative sentences.

### Part 2: Meticulous Defense
Walk through every assumption. Show balance tables. Test parallel trends. Report exogeneity tests. Address modern econometric concerns (staggered DiD, heterogeneous treatment effects).

### Part 3: Active Ruling-Out of Alternatives
Do not just list control variables. Dedicate a paragraph or subsection to explicitly test AGAINST a rival hypothesis. Show "no evidence" for alternative channels.

---

## Key Phrase Bank

### From Kelly & Ljungqvist:
- "Our identification strategy requires that..."
- "A necessary condition for this to hold is that..."
- "Consistent with the notion that the [shock] was unanticipated..."
- "This provides indirect support for our identification strategy."
- "To the extent that... this biases our tests against finding any effects."

### From Chang et al.:
- "Our aim is to provide plausibly identified evidence for..."
- "We take this into account by matching on [variable] when selecting control firms."
- "The identifying assumption in the context of a DD design is, as always, parallel trends, which we can evaluate directly..."
- "While it is never possible to 'prove' that an instrument satisfies the exclusion restriction, we investigate potential violations through the lens of..."
- "Given quasi-random assignment, staggered implementation, and the absence of diverging pretrends, the findings in Table V permit the plausibly causal interpretation that..."

### Universal Identification Phrases:
- "plausibly exogenous"
- "conditionall random variation"
- "clean identification"
- "sharp and sudden change"
- "as good as random"
- "the exclusion restriction is satisfied if..."

---

## Modern DiD Awareness Checklist

- [ ] Address staggered treatment timing concerns (Baker, Larcker, and Wang 2022)
- [ ] Use stacked regression or Callaway-Sant'Anna estimator if treatment timing varies
- [ ] Show formal parallel trends tests with event-study plots
- [ ] Report "clean" control selection criteria
- [ ] Test for anticipation effects
- [ ] Discuss heterogeneous treatment effects if using two-way fixed effects
- [ ] Report first-stage F-statistic if using IV
- [ ] Test and report results for exclusion restriction violations

---

## Checklist for Identification Style

- [ ] Identification problem stated upfront (endogeneity acknowledged)
- [ ] "Natural experiment" or "quasi-random variation" introduced as solution
- [ ] Exogeneity argued both with institutional detail AND empirical tests
- [ ] Balance/pre-trends shown in a table or figure
- [ ] Channel validated before final outcome tested
- [ ] Alternative explanations actively ruled out (dedicated subsection)
- [ ] "Plausibly exogenous" used (not "exogenous" without qualification)
- [ ] Modern DiD concerns addressed if using staggered design
- [ ] Exclusion restriction discussed and tested
- [ ] Both voices used: confident claim + meticulous defense

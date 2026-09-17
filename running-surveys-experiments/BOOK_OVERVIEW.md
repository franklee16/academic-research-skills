# Survey Curious? Start-Up Guide and Best Practices — Whole-book reading (Stage 0 output)

> Whole-book reading distilled by book2skill. Every downstream extractor and skill takes this file as global context.

## Basic info

- **Book title**: Survey Curious? Start-Up Guide and Best Practices For Running Surveys and Experiments Online
- **Authors**: Abigail Bergman, Alex Chinko, Samuel M. Hartzmark, Abigail B. Sussman (all Chicago Booth / NBER)
- **Year**: 2020 (Oct 5)
- **Source file**: `Best Practices For Running Surveys.pdf` (35 pages, SSRN 3701330)
- **Distillation date**: 2026-08-19

---

## 1. Structural

### Type

**Practical methodology manual + start-up guide** — written for empirical finance/economics researchers who want to run a survey but don't know how. Hybrid: §2 is a compact survey-design best-practice review; §3 is a best-practices playbook for running studies online; §4+Appendices are platform walkthroughs (Qualtrics, MTurk, CloudResearch, Prolific, Lucid).

### One-sentence thesis

A credible online survey experiment requires three layers of work stacked on top of each other — (a) **question design** that elicits answers respondents can and will give honestly, (b) **execution hygiene** (pilots, attention checks, screening, attrition checks) that protects data quality before full launch, (c) **platform fit** (MTurk / CloudResearch / Prolific / Lucid) matched to your target population and ethical constraints.

### Skeleton (main arguments and how they relate)

1. **Survey design (§2)** — *Layer 1, what to ask and how to ask it.* Seven subsections stacked by issue: ability & willingness (2.1), relative vs. absolute interpretation (2.2), converging evidence (2.3), clarity/concreteness/simplicity (2.4), avoiding leading questions (2.5), ceiling/floor/order effects (2.6), attention & motivation (2.7). All of §2 is **a checklist of pitfalls** rather than a positive design system — the author's stance is that respondents default to giving you junk unless each pitfall is actively blocked.
2. **Online execution (§3)** — *Layer 2, how to run it.* Piloting (3.1), attention/comprehension/manipulation checks (3.2), screening (3.3), reputation management (3.4), timing (3.5). These are **operational defenses against the same junk-data threats** §2 warns about, deployed at the workflow level rather than question level.
3. **Platform & population (§4)** — *Layer 3, who's answering and where.* Workflow (4.1), Qualtrics (4.2), recruitment platforms (4.3: MTurk / CloudResearch / Prolific / Lucid), the typical MTurk respondent (4.4). This is the **logistics layer**.
4. **Appendices A & B** — click-by-click recipes for Qualtrics + MTurk, plus a real Qualtrics QSF file (Chinco et al. baseline survey).

**Argument relationship**: §2 (questions) → §3 (operations) → §4 (platforms). Each layer assumes the previous one. A great §2 design can still fail at §3; a perfect §3 can still get wrong population at §4. Tiers of fail.

### Author's core problem

Finance and economics PhDs and faculty are trained on archival data and structural models, not on participant research. The practical knowledge of online surveys lives only in informal networks (lab mates, advisors' Slack groups), so first-time researchers pay huge start-up costs. The paper exists to lower that cost and push survey methods into economics mainstream.

---

## 2. Interpretive

### Key terms (author's usage)

| Term | Author's definition | Different from common usage |
|------|-----|-----|
| **Meaningful response** | One that would convince a critical reader familiar with survey methods that the hypothesis is/isn't supported (§2 intro). | ≠ "any response". Tied to the *evidentiary standard* of the field, not the respondent's effort. |
| **Converging evidence** | Asking the same hypothesis in 2+ question forms (state vs. action; stated preference vs. revealed), so inconsistent answers can be triangulated (§2.3). | ≠ "multiple data points". Requires *cross-validation across question types for the same construct*. |
| **Attribute substitution** | Respondent answers a *simpler* question than what was asked — the classic example "Do you consider factor X in allocation?" elicits "Does X *sound like* something I should care about?" (§2.4, Kahneman & Frederick). | ≠ "misreading". The respondent *is* trying to answer accurately, but substitutes a heuristic. |
| **Order effects** | Answer to Q1 changes answer to Q2 via anchoring, consistency-seeking, or different recall framing (§2.6, 2.7). | ≠ "fatigue". Includes *priming* and *anchoring*, which fatigue doesn't. |
| **Ceiling / floor effect** | Constrained response scale misses at one extreme — too many people pile up at "strongly agree" or "strongly disagree" (§2.6). | ≠ "low variance". Scale is *systematically truncated*, not just noisy. |
| **Selective attrition** | Differential drop-out or check-failure rates across experimental conditions — produces a treatment-vs-control comparison that's confounded with respondent types (§3.2, citing Zhou & Fishbach). | ≠ "drop-out" generally. Requires *across-condition asymmetry*. |
| **Attention check** | A question not relevant to the research question used to flag participants who aren't reading carefully (§2.7, §3.2). | ≠ "manipulation check". Attention check = are you paying attention? Manipulation check = did the *treatment* land? |
| **Manipulation check** | A question testing whether the experimental manipulation created the intended difference across conditions (§3.2). | ≠ "attention check". Manipulation check ≠ "do you read carefully", it asks "did you notice the difference between conditions?". |
| **Comprehension check** | A question testing whether the participant understood the instructions (§3.2). | ≠ "attention check". Comprehension can fail even when attention doesn't (e.g., instructions are unclear). |
| **Experimenter demand** | Respondent answers the question they think the researcher wants (§2.5). | ≠ "social desirability" (which is about self-image vs. outsider, not researcher-influence). Often overlap in practice. |
| **Social desirability bias** | Respondent answers the way they want to be seen, especially on sensitive topics ("Have you ever engaged in insider trading?" — always "no") (§2.5). | ≠ "lying". The respondent may *believe* their answer is virtuous, not recognize it as false. |
| **Relative vs. absolute level** | Surveys reliably estimate *comparisons* (Stock A vs. B) but levels (probability of buying Stock XYZ) are contaminated by question framing (§2.2). | ≠ "ordinal vs. cardinal". This is about *question-form sensitivity*, not measurement scale. |
| **Satisficing** | Respondent takes the path of least cognitive effort — picking the right-most option, always "yes", random clicking (§2.7). | ≠ "low motivation". It's the *mechanism* that motivation-deficit produces. |

### Core claims (in my own words)

1. **A respondent's answer is constrained by what they can recall, are willing to reveal, and can interpret** — fine-grained dollar amounts, distant memories, and introspective questions on decision context all systematically fail. (§2.1)
2. **Levels are fragile; comparisons are robust.** Asking "what's the probability you'll buy XYZ?" gives framing-dependent junk; asking "compare XYZ to ABC" gives something usable — as long as framing is held constant. (§2.2)
3. **Always triangulate.** A single survey item on a hypothesis is rarely credible. The same construct should be measured by ≥2 different question types. (§2.3)
4. **Clarity is anti-substitution.** When a question is ambiguous, respondents don't say "I don't know" — they substitute a related-but-different judgment. The fix is concreteness (named indexes, date ranges, exact denominators), not "make it simpler in general". (§2.4)
5. **Leading questions are everywhere.** Both social desirability bias and experimenter demand pollute responses; removing the *first half* of leading prompts ("Academics consider X important — to what extent do you consider X important?") eliminates the demand effect, but you should also include factors you expect to be irrelevant to catch consistency-bias. (§2.5)
6. **Yes-saying is the default.** Acquiescence biases raw agreement scales upward; asking "Was anything confusing?" instead of "Did you understand?" is a cheap fix. (§2.5)
7. **Pretest everything with non-economists, then pilot with 50–100 before the full 500.** Two layers of testing because the bugs you find in pilot are bugs your friends couldn't catch. (§3.1)
8. **Attention checks have diminishing-and-then-negative returns.** One or two are useful; piling them in selects for survey-savvy respondents and biases the sample. (§3.2, §3.3)
9. **Selective attrition is a quietly fatal confound.** If your treatment condition has more dropouts or more attention-check failures than control, your comparison is no longer random. (§3.2)
10. **Online surveys are not anonymous to participants.** Turker review sites (Turkerview) and reputation matter for getting usable data. (§3.4)
11. **MTurk ≠ MTurk-via-CloudResearch ≠ Prolific.** They're different populations with different pay expectations. Picking the wrong one can invalidate inferences about the population the researcher actually wants. (§4.3, §4.4)
12. **MTurk samples are convenience samples, not representative.** Better than undergrads in many applied-finance questions, worse for general-population inference. Pick based on research goal. (§4.4)

### Argument chain

The paper doesn't construct a tight deductive argument — it's an enumeration. Each section is its own micro-best-practice supported by 3-8 cited empirical findings from psychology/political-science survey literature (Krosnick, Schwarz, Oppenheimer, Bradburn, Tourangeau, etc.). The implicit chain is:

> **Premise**: Survey respondents are not the rational agents that economist models assume.
> **Consequence 1**: Many natural-sounding questions produce garbage.
> **Consequence 2**: Even well-designed garbage-detection requires operational discipline (pilots, checks, attrition audits).
> **Consequence 3**: Even with that discipline, platform choice determines the population you get, which may not be your target population.
> **Bottom line**: A good survey requires all three layers, and shortcuts at any layer compromise the others.

---

## 3. Critical ★

### Era limitations

- **2020 data-quality landscape is stale.** The paper notes a COVID-era decline in MTurk data quality and says "may or may not persist" (§4.3). It persists. As of 2024-2026, MTurk bot/server-farm issues are first-order — `bots vs. humans` is now a baseline screening question, not an afterthought.
- **Bot detection section is too optimistic.** "At the time of writing, bot-driven results are not a first order concern" (§4.4) — no longer true. CloudResearch's bot-detection tooling is the de facto standard now.
- **Pay rates quoted ($3.13–$3.48/hour on MTurk) are below current Prolific floor.** The paper positions these as baselines; in 2026, Prolific enforces ~$6.50/hr minimum and academic-best-practice is ≈$15/hr across platforms.
- **No mention of LLM/AI-driven response contamination.** Surveys in 2026 must worry about participants using ChatGPT to answer open-ended questions en masse.

### Author position blind spots

- **Booth/NBER finance perspective dominates.** Authors all write household finance / asset pricing. The paper silently assumes the reader wants to study finance/financial-decision-making. General-purpose survey concerns for marketing, public policy, health, or political behavior are under-treated.
- **US/UK centric.** MTurk (US/India), Prolific (US/UK), Lucid (US). No guidance for non-Western populations or for cross-cultural survey design (translation equivalence, response style differences like acquiescence in East Asian samples).
- **Lab-style vs. field-study continuum is missing.** The paper assumes convenience-sample online experiments. Doesn't address probability sampling, address-based sampling, or hybrid designs.
- **Underplays ethics.** IRB approval is relegated to footnote 5. Consent procedures, data-privacy (GDPR/CCPA), debriefing — all barely mentioned.
- **Status-of-respondent hide.** Doesn't dwell much on the *moral economy* of paying participants ($0.15 + $0.85 for 6 min of real effort) — yet the paper itself flags reputation and "do not stiff the participants". A more candid author would warn that ethically minimum-pays risk producing bad data precisely because they select for income-motivated respondents.

### Unproven assumptions

- **That the *practical knowledge* the authors document is best-practice and not just shared-routine.** Several recommendations are presented as "this is what people do" rather than "this is what works". E.g., 50–100 pilot sample size is standard but the paper doesn't show simulation-based support for that specific number.
- **That converging evidence always strengthens a finding.** Triangulation helps if the auxiliary items measure something correlated with the construct. Multiple correlated-confounded measurements don't help; the paper doesn't make this caveat.
- **That pay-rate-as-quality-knob is monotonic.** More pay → better data is a folk theorem in the literature; the paper endorses it implicitly but evidence is mixed (high pay also draws professional survey-takers who game).

### Strongest counter-argument

> The paper's *under-specification* of design (Section 2) and *over-confidence* in mechanical pilots/checks (Section 3) masks the **fundamental problem that survey-response validity is construct-specific and field-specific**. A checklist of 7 design pitfalls (the paper's own §2 structure) flattens what is actually a hierarchy — for some constructs (risk preference), no online survey of laypeople will produce defensible data, regardless of how many attention checks you stack. The honest move is to say "use a different method here", not to add another §2.7 pitfall.

This pushback comes from the limits of self-report on constructs (Kahneman's distinction between experiencing vs. remembering utility; Hauser et al. on validity of stated vs. revealed preferences in finance). The paper does not engage with these well.

> **Above critiques will feed into the Boundary (B) field of every downstream skill.**

---

## 4. Applicability

### Content that can be skill-ified

- Question-design heuristics (clarity, concreteness, avoiding leading questions, order/ceiling/floor effects) — these are the most "always applicable" and the least platform-dependent.
- Operational discipline (pilots, attention checks, attrition audits, screening payment) — works on every platform.
- Platform-selection decision tree (MTurk vs. CloudResearch vs. Prolific vs. Lucid) — concrete, actionable, and doesn't go stale quickly.
- Relative-vs-absolute interpretation — a constant mindset any economist running surveys needs.
- Converging evidence — the survey-design analogy of robustness checks.

### Content that should NOT be skill-ified alone

- Appendices A & B (click-by-click for Qualtrics, MTurk) — these are platform tutorials that go stale quarterly. Better to link to current Qualtrics/MTurk docs than to maintain a skill.
- The §4.4 demographic profile of MTurkers — accurate as of 2018 data; not skill material.
- The reference list — link to it, don't reproduce.

### Estimated skill count

**8-12 atomic skills** expected. Let me list them provisionally (will be tightened by Stage 1.5 verification):

1. **claude-skill: survey-question-design** — the umbrella "before you write a question, run this checklist" skill
2. **claude-skill: clarity-concreteness-substitution** — anti-attribute-substitution heuristics (§2.4)
3. **claude-skill: avoid-leading-questions** — social-desirability / experimenter-demand awareness (§2.5)
4. **claude-skill: relative-vs-absolute** — interpreting levels vs. comparisons (§2.2)
5. **claude-skill: converging-evidence** — design with multiple items per construct (§2.3)
6. **claude-skill: pretest-then-pilot** — two-stage field-test protocol (§3.1)
7. **claude-skill: quality-checks** — attention vs. comprehension vs. manipulation — when to use which (§2.7, §3.2)
8. **claude-skill: selective-attrition-audit** — diagnosing condition-asymmetric drop-out (§3.2)
9. **claude-skill: platform-selection** — MTurk vs. CloudResearch vs. Prolific vs. Lucid (§4.3)
10. **claude-skill: participant-payment** — fair-compensation norms & reputation (§3.3, §3.4)
11. **claude-skill: mturk-representativeness** — what's actually in the MTurk pool (§4.4)

### Priority ranking (most-empowers-a-normal-user first)

1. **survey-question-design** (umbrella; gets used every time)
2. **clarity-concreteness-substitution** (single highest-impact design fix)
3. **pretest-then-pilot** (single highest-impact operational fix)
4. **platform-selection** (single highest-impact logistics fix)
5. **avoid-leading-questions**
6. **quality-checks** (attention vs. comprehension vs. manipulation)
7. **converging-evidence**
8. **relative-vs-absolute**
9. **selective-attrition-audit**
10. **participant-payment**
11. **mturk-representativeness**

---

## ✅ Quality-gate check

- [x] One-sentence thesis
- [x] Skeleton: 4 main argument layers + cross-layer relationship described
- [x] Glossary: 12 key terms with author-specific definitions
- [x] Critical stage: 3 era limits, 5 author blind spots, 3 unproven assumptions, 1 strong counter-argument (≥3 limits ✓)
- [ ] **Pending user sign-off before proceeding to Stage 1**

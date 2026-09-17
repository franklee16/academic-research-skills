# Candidate Cases (author's worked examples)

> Extracted from Survey Curious? Bergman, Chinco, Hartzmark, Sussman (2020).
> Each case is bound to a methodology theme it illustrates.

---

- id: c01
  title: Chinco et al. (2020) — risk-factor correlations study with benchmark items
  type: case
  source_chapter: §2.2
  source_quote: |
    "For example, in Chinco et al. (2020), we are interested in learning whether participants care about risk-factor correlations. We include questions asking about the relevance of means and volatility in addition to risk-factor correlations. If we were to see that people did not report caring about any of the three items, this would lead to concerns that there were underlying problems with the survey. However, we see instead that people do report caring about means and volatility, but not about risk-factor correlations. Consequently, we can interpret this null result as meaningful in both relative and absolute terms."
  summary: |
    The authors wanted to test whether laypeople consider risk-factor correlations when investing. They included benchmark items (means, volatility) that should clearly register if the survey instrument is functioning. Result: respondents did claim to consider means and volatility but not correlations. Because the benchmarks registered, the null on correlations is interpretable in *absolute* terms, not just relative.
  bound_to:
    - "relative-vs-absolute"
    - "converging-evidence"
  outcome: |
    Authors were able to claim a meaningful absence-of-result rather than a "the survey didn't catch it" outcome.
  tags: [case, benchmark-items, absolute-interpretation]

---

- id: c02
  title: Chinco et al. — stated strategies vs. revealed allocation decisions
  type: case
  source_chapter: §2.3
  source_quote: |
    "in Chinco et al. (2020), we include questions asking participants to state their strategies for making allocation decisions. To provide converging evidence, we also include questions asking participants to make allocation decisions. We can then compare how the same person says they made decisions with the strategy they say they implement."
  summary: |
    Same construct — how an investor makes allocation decisions — measured with two question types: a stated-preference version (describe your strategy) and a revealed-choice version (now make allocations). Stated-revealed gap is itself the finding; either alone would have missed it.
  bound_to:
    - "converging-evidence"
    - "stated-vs-revealed"
  outcome: |
    Two question types per hypothesis gave authors the ability to cross-validate. Inconsistent respondents (state X, choose Y) become a *finding* about the construct, not noise.
  tags: [case, triangulation, stated-vs-revealed]

---

- id: c03
  title: Replacement of "How will the market perform short-term?"
  type: case
  source_chapter: §2.4
  source_quote: |
    "For example, if you ask: 'How do you think that the market will perform in the short-term?' participants may have different interpretations of both 'market' and 'the short-term'. Instead, a better way to ask the question would be: 'The S&P index's current value is $XX. What do you think the change in the S&P 500 index's value will be between today and one month from today (DD/MM/YY)?' and allow for responses as percentage changes."
  summary: |
    Authors replace "How will the market perform?" (vague on both market and horizon) with a named, dated, numerically-specifiable item ("S&P 500 from today to one month from today, in percent"). The latter is unambiguous; respondents cannot plausibly interpret "market" as their own portfolio.
  bound_to:
    - "clarity-concreteness-substitution"
    - "ambiguity-driven-substitution"
  outcome: |
    Concrete wording enabled clear interpretation of results, especially relative to other similar items.
  tags: [case, clarity, concreteness]

---

- id: c04
  title: Fair screening pay — split into 2-part design
  type: case
  source_chapter: §3.3
  source_quote: |
    "the best practice is to launch a short screener survey first that pays everyone a small amount. Then, invite only workers who 'pass' the screener to complete a second (main) study. Alternatively, you could launch a survey with 2 parts (and say so explicitly in the instructions). Then, you could allow only those who passed the first part to participate in the second, paying a bonus to all those who completed part 2. Here is some example wording: 'The first part will take about 1 minute and will pay everyone $0.15. Workers who qualify will be directed to the second part which takes about 5 minutes and will pay a bonus of $0.85.'"
  summary: |
    The author's literal split-payment wording: 1-minute screener at $0.15 universal pay, then 5-minute main at $0.85 bonus for qualifiers. Both groups are paid; qualifiers get more; nobody is stiffed.
  bound_to:
    - "fair-pay"
    - "screener-design"
    - "reputation-management"
  outcome: |
    Screener participants (even those who don't qualify) are compensated; main survey uses only pre-qualified respondents.
  tags: [case, payment-design, screening, fair-pay]

---

- id: c05
  title: Pilot protocol — small wave first, bug-check, then full launch
  type: case
  source_chapter: §3.1
  source_quote: |
    "If you are aiming to get 500 participants, run an initial survey experiment involving only 50−100 participants. Don't analyze the data to see if responses are in-line with your hypothesis, but do check that the data is interpretable. [...] It is also helpful to include free response questions at the end of the survey experiment that allow participants to offer their thoughts [...] A quick skim of these responses can alert a researcher to unanticipated issues — i.e., things only a survey taker would notice."
  summary: |
    The recommended discipline for any new survey: pretend you want 500, actually collect only 50-100 first, *don't run the hypothesis test* on that subsample, only check for instrument bugs and skim open-ended responses. Once clean, launch to remaining participants.
  bound_to:
    - "pilot-study-design"
    - "two-stage-testing"
  outcome: |
    Bugs visible only at scale (broken randomizations, condition-asymmetric drop-out) are caught at small cost before committing to a full sample.
  tags: [case, pilot, methodology]

---

- id: c06
  title: Sample-composition timing — Arechar et al. on MTurk daytime vs. weekend
  type: case
  source_chapter: §3.5
  source_quote: |
    "Studies have examined MTurker participation during the day vs. at night as well as on weekdays vs. over the weekend and found a lack of evidence for differences in incentivized behavior — i.e., participants are not responding differently. However, studies have found significant differences in character traits between participants who complete studies at different times — i.e., participants do look different."
  summary: |
    Arechar, Kraft-Todd, & Rand (2017) showed: MTurkers answering at night vs. day, weekday vs. weekend, give similar *behavior* responses but differ in *person traits*. Same people behave similarly; different people are at the keyboard.
  bound_to:
    - "platform-population-choice"
    - "timing-as-sample-selection"
  outcome: |
    Researchers can treat behavior data as roughly comparable across times, but cannot treat *demographics* as comparable across times.
  tags: [case, timing, MTurk-samples]

---

- id: c07
  title: Bot-detection result — Moss & CloudResearch
  type: case
  source_chapter: §4.4
  source_quote: |
    "Research completed using MTurk by researchers at the CloudResearch survey platform found no evidence of bots. But, they did find some evidence of data coming from workers using server farms to mask their location, allowing them to complete the same survey experiment several times."
  summary: |
    In their sampling window, CloudResearch did *not* find bot-driven responses on MTurk but *did* find server-farm workers (location-masked, repeating). The fix is geolocation-blocking and duplicate-IP screening.
  bound_to:
    - "platform-selection"
    - "data-quality-screening"
  outcome: |
    Authors suggest geolocation and IP screening, not bot-detection filters, as the relevant defenses — note: this 2020 finding is partially dated; bot-detection is now a first-order concern.
  tags: [case, bots, server-farm, MTurk]

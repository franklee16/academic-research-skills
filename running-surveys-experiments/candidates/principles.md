# Candidate Principles (rules / heuristics / checklists)

> Extracted from Survey Curious? Bergman, Chinco, Hartzmark, Sussman (2020).

---

- id: p01
  title: Privacy prohibits precise dollar questions
  type: principle
  source_chapter: §2.1
  source_quote: |
    "if you ask detailed questions about participants' personal finances asking for an exact dollar amount, participants may be unwilling to answer truthfully as a result of privacy considerations [...] A researcher would often be better served by asking less detailed questions, which could be accomplished by allowing participants to respond in ranges"
  summary: |
    Never ask for an exact dollar amount on personal finance. Use bracketed ranges ($0, $0-10k, $10k-50k, $50k-100k, >$100k). Applies to income, net worth, holdings, salary, debt amounts — anything that's "a stranger would want to know".
  tags: [principle, privacy, sensitive-questions, bracketing]

---

- id: p02
  title: Shorten the recall window when you must ask about past behavior
  type: principle
  source_chapter: §2.1
  source_quote: |
    "if you ask detailed questions about behavior over an extended period [...] people may be unable to answer accurately as a result of memory limitations [...] shortening the time horizon would make it more likely that participants recall and report a meaningful result"
  summary: |
    Don't ask "how many times in the last year did you check your portfolio?" — ask "in the last week". Memory decays fast; one-week recall is reliable; one-year recall is mostly fabrication. When in doubt, switch from "habit over time" to "specific last-N-days".
  tags: [principle, memory, time-horizon, behavior]

---

- id: p03
  title: Make the abstract concrete — name the index, name the date
  type: principle
  source_chapter: §2.4
  source_quote: |
    "if you ask: 'How do you think that the market will perform in the short-term?' participants may have different interpretations of both 'market' and 'the short-term'. Instead, a better way to ask the question would be: 'The S&P index's current value is $XX. What do you think the change in the S&P 500 index's value will be between today and one month from today (DD/MM/YY)?'"
  summary: |
    Replace every abstract word in a survey question with a named concrete reference. "Market" → "S&P 500". "Short-term" → "today to one month from today". "Important factor" → "factor X for decision Y". If a word can be replaced by a specific example, replace it.
  tags: [principle, concreteness, wording]

---

- id: p04
  title: Strip evaluative framing from the front of your question
  type: principle
  source_chapter: §2.5
  source_quote: |
    "asking: 'Academics consider X factor to be very important in investment decisions. To what extent do you consider X in your own investment decisions?' can suggest that the researchers believe that factor X is important [...] Eliminating the first part of that question would largely address this issue."
  summary: |
    Phrases like "Experts say…" / "Most people think…" / "Researchers have shown…" before a question induce experimenter-demand bias. Strip the leading sentence; ask the question directly. Bonus: include factor items you expect to be irrelevant to catch the same participant who is just answering what they think you want.
  tags: [principle, leading-questions, experimenter-demand]

---

- id: p05
  title: Replace "Did you understand?" with "What was confusing?"
  type: principle
  source_chapter: §2.5
  source_quote: |
    "if you want to know whether people understand a particular question in your survey, or if they are confused, a question asking: 'Do you understand the instructions?' is likely to bias participants towards saying that they do understand in order to seem intelligent. Instead, rephrasing the question as: 'Was anything confusing in these instructions? Please explain if so.'"
  summary: |
    Yes/no confirmation questions are saturated by social-desirability bias. To get real signal on comprehension, ask open-ended "what was confusing?" with an empty text box. Same fix applies to "did you have any issues?" — replace yes/no with open-text.
  tags: [principle, acquiescence, comprehension-checks, open-ended]

---

- id: p06
  title: Counterbalance order, randomize items, separate pages
  type: principle
  source_chapter: §2.6
  source_quote: |
    "Consider the possibility of order effects when determining question order and counterbalance items (e.g., randomize whether participants see question A before vs. after B) when possible. Also consider page spacing [...] If two questions appear on the same page, an earlier question may be more likely to influence a later question"
  summary: |
    Three rules for ordering:
    (a) Randomize which participant sees A-before-B vs. B-before-A when the items are comparable.
    (b) Put likely-influencing and likely-influenced items on separate pages.
    (c) Drop "huge grids" — they fatigue attention and increase the chance that the late-row response was anchored by the early-row.
  tags: [principle, order-effects, randomization, counterbalancing]

---

- id: p07
  title: One or two attention checks; more is worse
  type: principle
  source_chapter: §3.2
  source_quote: |
    "it is important to recognize that there can be downsides to introducing an excessive number of attention checks. It is possible that going overboard in this direction can actually reduce the quality of your data by introducing bias [...] some seasoned survey-takers may anticipate these attention checks and be more likely to pass them"
  summary: |
    A few well-placed attention checks filter out inattentive respondents without biasing the sample. Pile them in and you select for "people who know what attention checks look like" — which correlates with professional survey-takers who game your survey. Quality of attention checks (clear, not trick-question, not impossible) matters more than quantity.
  tags: [principle, attention-checks, satisficing, selection-bias]

---

- id: p08
  title: Always include an open-ended "what was confusing?" at end of pilot
  type: principle
  source_chapter: §3.1
  source_quote: |
    "It is also helpful to include free response questions at the end of the survey experiment that allow participants to offer their thoughts (e.g., 'Do you have any questions about this survey? Did you find anything confusing?'). A quick skim of these responses can alert a researcher to unanticipated issues — i.e., things only a survey taker would notice."
  summary: |
    End every pilot with a free-text "what was confusing / questions / anything to flag" — read every response. Survey designers are blind to their own bugs; the taker sees them in 10 seconds. The cost is one optional text box.
  tags: [principle, pilot, free-text, bug-discovery]

---

- id: p09
  title: Pay screeners even if they're rejected
  type: principle
  source_chapter: §3.3
  source_quote: |
    "be sure to offer some compensation to participants who do not pass the screening step. The best practice is to launch a short screener survey first that pays everyone a small amount. Then, invite only workers who 'pass' the screener to complete a second (main) study."
  summary: |
    Screened-out participants must be paid. Two-step design: a short screener that pays a small amount to everyone, then invite only passers to the main survey which pays a bonus. Never stiff the screen — it both creates an ethical breach and damages your reputation on Turker-review sites.
  tags: [principle, screening, fair-pay, ethics]

---

- id: p10
  title: Direct questions on insider trading, illegal sex, drug use → expect a "no" floor
  type: principle
  source_chapter: §2.5
  source_quote: |
    "if you were to ask: 'Have you ever engaged in insider trading?' most people would answer that they have not, irrespective of the truth."
  summary: |
    Direct questions on socially-deviant behaviors (insider trading, illegal drug use, undeclared income, affair) yield a "no" floor that's mostly artifact. Methods to break: list experiments, randomized response, indirect elicitation, behavioral measures, or — better — skip self-report entirely and use admin or audit data. A confirmed "no rate of 95%" on a sensitive question rarely means 95% didn't do it.
  tags: [principle, sensitive-questions, social-desirability, list-experiment]

---

- id: p11
  title: Don't analyze pilot data on the target hypothesis; only check the instrument
  type: principle
  source_chapter: §3.1
  source_quote: |
    "Don't analyze the data to see if responses are in-line with your hypothesis, but do check that the data is interpretable. You will be surprised at how often you will find bugs in the survey design even after initial testing phases."
  summary: |
    Pilot's job is to detect *instrument* bugs (broken skips, missing response options, scale saturation, condition-imbalance), not to do a hypothesis check. If you analyze the pilot for hypothesis results, you'll be tempted to ship early or hand-pick modifications that confirm what you want to see.
  tags: [principle, pilot, separation-of-concerns, bias-prevention]

---

- id: p12
  title: Match pay rate to platform norms — underpay drives away good respondents
  type: principle
  source_chapter: §3.4
  source_quote: |
    "pay attention to any changes in the standard pay rates that participants expect. These may be different across different crowdsourcing platforms. e.g., participants on Prolific will not be happy with standard MTurker pay."
  summary: |
    Each platform has a social norm of "fair pay". On Prolific, the floor is ≈$6.50/hour and ethics-friendly is ≈$15/hour. On MTurk, ≈$7.50/hour is competitive. Picking the wrong pay for your platform → professional-survey-takers avoid your study and your sample composition silently worsens. Check platform-specific recent rate guides before posting.
  tags: [principle, fair-pay, platform-norms, data-quality]

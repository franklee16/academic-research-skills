# Candidate Counter-Examples (failure modes / warnings)

> Extracted from Survey Curious? Bergman, Chinco, Hartzmark, Sussman (2020).
> Each counter-example feeds the B (Boundary) section of downstream skills.

---

- id: ce01
  title: Asking exact dollar amounts on personal finance
  failure_mode: |
    Respondent refuses to answer, gives random number, or abandons survey. Even when they answer, social desirability bias distorts toward under-reporting of wealth and over-reporting of virtue-signaling categories (giving, savings rate).
  mechanism: |
    Privacy considerations. Sensitive questions get a floor of refusal or low-effort answers (Cho & LaRose 1999; Duncan 1996).
  warning_signs:
    - High skip rate on the question
    - Spikes at round numbers ($50,000, $100,000)
    - Heaping at $0
  bound_to: limits-survey-of-personal-finance-detail
  source_chapter: §2.1
  source_quote: |
    "if you ask detailed questions about participants' personal finances asking for an exact dollar amount, participants may be unwilling to answer truthfully as a result of privacy considerations"
  tags: [counter-example, sensitive-questions, privacy, financial-data]

---

- id: ce02
  title: Year-scale recall of behavior
  failure_mode: |
    Respondent reports a plausible-sounding number that's mostly reconstructed/imputed, not remembered. Numbers converge to heuristics (mental "typical" estimates) rather than actual counts.
  mechanism: |
    Memory decays non-linearly; aggregate periods are filled in by cognitive interpolation (Bradburn et al. 1987).
  warning_signs:
    - Implausible uniformity (everyone says "12-15 times")
    - Sharp round-number preferences
    - Low correlation with shorter-window recall on same topic
  bound_to: limits-survey-of-infrequent-behavior
  source_chapter: §2.1
  source_quote: |
    "if you ask detailed questions about behavior over an extended period [...] people may be unable to answer accurately as a result of memory limitations"
  tags: [counter-example, memory, time-horizon]

---

- id: ce03
  title: Asking why someone made a particular decision
  failure_mode: |
    Respondent gives a confident-sounding narrative that's correlated with the actual decision only weakly. Often the answer is a post-hoc rationalization matching what the respondent wishes had been the reason, not what actually was.
  mechanism: |
    Introspection-illusion: people don't have direct access to their decision processes (Nisbett & Wilson 1977).
  warning_signs:
    - High consistency across respondents suggesting a social-desirable template
    - Long, fluent answers to questions about decisions a year ago
  bound_to: limits-introspection-surveys
  source_chapter: §2.1
  source_quote: |
    "if you ask a question about how context affected a decision-making process [...] participants are unlikely to be able to access the relevance of the context and therefore will be unable to report it to you"
  tags: [counter-example, introspection, decision-process]

---

- id: ce04
  title: Asking "Will you buy Stock XYZ next week?" with probability scale
  failure_mode: |
    The probability is contaminated by anchoring (the prior question), by frame ("next week" ranges 1-12 vs. 5-10 workweek days), and by the respondent's failure to interpret probabilities literally.
  mechanism: |
    Anchoring + framing + probability-literacy gap (Tversky & Kahneman 1974; Schwarz 2007).
  warning_signs:
    - Masses pile at 0%, 50%, 100%
    - Different probability scale (0-100 vs. 1-10) changes the distribution
    - Order-effects change the answer materially
  bound_to: limits-survey-of-probabilistic-intentions
  source_chapter: §2.2
  source_quote: |
    "What is the probability that you will purchase Stock XYZ next week? [...] psychological processes such as anchoring [...] may influence participants' responses to the target question."
  tags: [counter-example, probability, anchoring, intentions-vs-actions]

---

- id: ce05
  title: Asking "Did you understand the instructions?" (yes/no)
  failure_mode: |
    Yields an empty "yes" floor. Respondents don't want to look stupid, so they answer "yes" even when they didn't understand.
  mechanism: |
    Social desirability + desire to appear competent.
  warning_signs:
    - 99% "yes" rate
    - Free-text responses later reveal confusion the "yes" hid
  bound_to: limits-yes-no-comprehension-checks
  source_chapter: §2.5
  source_quote: |
    "a question asking: 'Do you understand the instructions?' is likely to bias participants towards saying that they do understand in order to seem intelligent."
  tags: [counter-example, acquiescence, comprehension-checks]

---

- id: ce06
  title: Pile-in attention checks
  failure_mode: |
    Survey-savvy workers (who know what attention checks look like) pass them and dominate the sample. Naive workers (who would have given genuine effort) drop out or are filtered. Net data quality is *worse* not better.
  mechanism: |
    Differential non-response / selection by sophistication. See Vannette 2017; Casler et al. 2013.
  warning_signs:
    - "Other: read" pattern selected for in every attention check
    - Sample is dominated by repeat MTurk/Prolific veterans
    - Free-text responses are unusually polished and short
  bound_to: limits-too-many-attention-checks
  source_chapter: §3.2
  source_quote: |
    "it is important to recognize that there can be downsides to introducing an excessive number of attention checks. It is possible that going overboard in this direction can actually reduce the quality of your data by introducing bias"
  tags: [counter-example, attention-checks, selection]

---

- id: ce07
  title: Survey too long for the pay
  failure_mode: |
    Random-responding kicks in. Specifically, response quality degrades visibly from the first 5 minutes to the last 5 minutes. Mid-survey, respondents start picking the right-most option, or always "agree".
  mechanism: |
    Survey fatigue — cognitive load exceeds motivation (Krosnick 1991; Dolnicar & Rossiter 2008; Wu et al. 2014).
  warning_signs:
    - Latency drops in second half of survey
    - Right-most-option pileups on later pages
    - Drop-offs clusters in last 20% of length
  bound_to: limits-survey-length-vs-pay
  source_chapter: §2.7, §3.3
  source_quote: |
    "Online participants are typically being paid relatively small amounts to complete a survey. Even if you were to increase this amount substantially and include incentives for correct responses, participants are likely to lose interest in a study that is too long or poorly designed. [...] Or alternatively, participants may choose a particular response (e.g., the right-most option available) and be more likely to select that response for everything."
  tags: [counter-example, fatigue, satisficing, response-quality]

---

- id: ce08
  title: Directly asking about socially-deviant behavior
  failure_mode: |
    Yields a 0-1% "yes" rate regardless of actual prevalence. The number is not interpretable.
  mechanism: |
    Strong social desirability bias on face-valid illegal/immoral questions (Krumpal 2013).
  warning_signs:
    - Self-reported rate much lower than external prevalence data
    - Skew toward extreme-virtuous demographic
  bound_to: limits-survey-of-sensitive-behavior
  source_chapter: §2.5
  source_quote: |
    "if you were to ask: 'Have you ever engaged in insider trading?' most people would answer that they have not, irrespective of the truth."
  tags: [counter-example, insider-trading, drug-use, sensitive-topics]

---

- id: ce09
  title: Differential drop-out across experimental conditions
  failure_mode: |
    Your treatment arm has, e.g., 20% drop-out and your control arm has 8%. The remaining respondents in your treatment arm are systematically different (more patient, more pro-research, less time-pressured) than those in control. Your treatment-vs-control estimate is now confounded with respondent type.
  mechanism: |
    Differential attrition (Zhou & Fishbach 2016).
  warning_signs:
    - Completion-time / completion-rate asymmetry across conditions
    - Different attention-check pass-rate across conditions
    - Different demographic distribution across conditions
  bound_to: limits-condition-symmetric-attrition
  source_chapter: §3.2
  source_quote: |
    "beware of selective attrition. When analyzing responses, check to see whether the pass-rate on checks, as well as the completion rate for the survey, is consistent across experimental conditions"
  tags: [counter-example, attrition, internal-validity]

---

- id: ce10
  title: Asking about transaction-criterion stocks (XYZ) one-by-one
  failure_mode: |
    Each subsequent probability rating is anchored on the previous. Independent ratings are not independent.
  mechanism: |
    Anchoring + comparative judgment (respondents compare within the page rather than to a personal standard).
  warning_signs:
    - Strong correlation between adjacent ratings that exceeds true correlation
    - Distribution shapes nearly identical across items
  bound_to: limits-cross-item-anchoring
  source_chapter: §2.2, §2.6
  source_quote: |
    "if the response were dependent on question order [...] asking about the probability of purchasing stock ABC or DEF [...] may influence participants' responses to the target question"
  tags: [counter-example, anchoring, cross-item-effects]

---

- id: ce11
  title: Trusting MTurk sample as US-general-population-representative
  failure_mode: |
    MTurk samples skew younger, more educated, more female, more US-India, more "prolific survey takers" than US general population. Inference to "Americans" or "investors" is unsupported.
  mechanism: |
    Convenience sampling on a self-selected platform (Paolacci et al. 2010; Huff & Tingley 2015).
  warning_signs:
    - Demographic comparison with US Census shows age/education gaps
    - Comparing responses to probability-sampled panels shows gaps
  bound_to: limits-mturk-representativeness
  source_chapter: §4.4
  source_quote: |
    "MTurk samples can be considered convenience samples. They are not representative of the general population."
  tags: [counter-example, sample, representativeness]

---

- id: ce12
  title: Stiffing screeners — not paying failed-screen respondents
  failure_mode: |
    Reputation damage on Turker review sites. Future respondents avoid your studies. Your sample becomes the desperate/low-effort tail of the platform.
  mechanism: |
    Worker coalition penalties; review economy.
  warning_signs:
    - Review scores dropping
    - Higher-than-average drop-out on launches
  bound_to: limits-payment-toward-screeners
  source_chapter: §3.3, §3.4
  source_quote: |
    "be sure to offer some compensation to participants who do not pass the screening step [...] it is important that you do not stiff the participants who only make it to part one"
  tags: [counter-example, fair-pay, reputation]

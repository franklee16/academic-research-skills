# Candidate Glossary (author-specific terminology)

> Shared glossary for all downstream skills. Each entry flags what's specific to this paper vs. common usage.

---

- id: g01
  term: Meaningful response
  type: term
  author_definition: |
    "we refer to meaningful responses as those that would be likely to convince critical readers who are knowledgeable about survey methods that your hypothesis either is or is not correct." (§2 intro)
  key_distinction: |
    ≠ "any answer the respondent gave". Tied to evidentiary standard of the field, not the respondent's effort or honesty.
  why_it_matters: |
    Downstream skills should not optimize for respondent engagement or honesty; they optimize for "would a critical reviewer trust this answer?". Engagement and honesty are necessary but not sufficient.
  tags: [term, core-concept]

---

- id: g02
  term: Converging evidence
  type: term
  author_definition: |
    "multiple question types that can be compared against one another [...] That way, if there are concerns about a specific question type (e.g., question framing), an alternative question type (e.g., with a different question framing) testing the same hypothesis can be used to provide additional support for the overall results." (§2.3)
  key_distinction: |
    ≠ "piling more items". The items must test the *same construct* using *different methods* (state vs. choose, recall vs. infer). Two correlated items testing the same construct via the same method = redundancy, not convergence.
  why_it_matters: |
    This is the survey-design analog of robustness checks. Most published survey papers have a single item per construct; downstream skills should push researchers toward ≥2 items using different elicitation methods.
  tags: [term, core-concept, robustness]

---

- id: g03
  term: Attribute substitution
  type: term
  author_definition: |
    "people reply to a complicated question with the answer to a simpler one." (§2.4, citing Kahneman & Frederick 2002)
  key_distinction: |
    ≠ "not understanding the question". The respondent *is* trying to answer accurately; they substitute a heuristically-easier related judgment. Their answer is sincere but about the wrong construct.
  why_it_matters: |
    This is the central mechanism that concreteness rules counter. Without naming this mechanism, "be clearer about your questions" sounds like a stylistic instruction; with it, "be clearer" becomes a construct-validity intervention.
  tags: [term, mechanism]

---

- id: g04
  term: Social desirability bias
  type: term
  author_definition: |
    "people want to answer your survey in a way that is socially acceptable, even when this response is not truthful." (§2.5, citing Grimm 2010; Krumpal 2013)
  key_distinction: |
    ≠ "experimenter demand". Social desirability is about self-image vs. an imagined social audience. Experimenter demand is about the respondent reading the researcher's intent.
  why_it_matters: |
    Methods to address them are different. Social desirability → list experiments, randomized response, indirect elicitation. Experimenter demand → strip the leading sentence, include irrelevant factors to test consistency.
  tags: [term, bias]

---

- id: g05
  term: Experimenter demand
  type: term
  author_definition: |
    "participants will try to understand the answer the researcher wanted them to give and be more likely to give that answer." (§2.5, citing Mummolo & Peterson 2019; Orne 1962; Sears 1986; Zizzo 2010)
  key_distinction: |
    ≠ social desirability (see above). ≠ priming (priming ≠ demand awareness).
  why_it_matters: |
    The fix is *stripping the framing sentence* (e.g., "Academics consider X important — to what extent do you consider X important?" → "To what extent do you consider X important?"). The fix is *not* deception about hypotheses — IRB would flag that.
  tags: [term, bias]

---

- id: g06
  term: Order effects (incl. anchoring, consistency-seeking)
  type: term
  author_definition: |
    "questions occurring early in a study may influence later responses. This can occur because participants anchor on response to earlier questions, because a particular question early on influences interpretation of a later question, elicits different relevant characteristics from memory, or because participants often aim to be consistent." (§2.6, multiple citations)
  key_distinction: |
    ≠ survey fatigue (which is response-degradation, not response-direction-shift). ≠ common-method-variance (a measurement-model concept).
  why_it_matters: |
    Order effects can flip a treatment effect's sign. Counterbalancing across participants (not just across surveys) is the standard mitigation.
  tags: [term, design-effect]

---

- id: g07
  term: Ceiling / floor effect
  type: term
  author_definition: |
    "For questions where participants are able to respond within a constricted range, carefully consider what range of options are available to avoid ceiling or floor effects. [...] If you have a high proportion of participants responding at either end of the scale, you should probably adjust the scale." (§2.6, citing Masino & Lam 2014; Streiner et al. 2015)
  key_distinction: |
    ≠ "low variance". The variance isn't low — it's truncated at the scale boundary. ≠ "everyone agrees". They could disagree at the unmeasured level.
  why_it_matters: |
    Pretests that show 40%+ of responses piled at "5 of 5" mean the scale is structurally inadequate, not that the construct is uniform.
  tags: [term, scale-design]

---

- id: g08
  term: Satisficing
  type: term
  author_definition: |
    "participants might simplify the process, for example by choosing randomly or always selecting the right-most option." (§2.7, citing Krosnick 1991; Krosnick et al. 1996)
  key_distinction: |
    ≠ "low motivation". Satisficing is the *mechanism* by which low motivation produces junk data — heuristic-based answering rather than effortful processing.
  why_it_matters: |
    Interventions: shorten survey, raise pay, vary question types, reduce grids, embed attention checks. The right intervention depends on the satisficing mode (random vs. straight-line vs. acquiescence).
  tags: [term, mechanism]

---

- id: g09
  term: Attention check
  type: term
  author_definition: |
    "questions that are not directly relevant to your research question, but can be used to identify if participants are paying attention to your survey (e.g., 'If you are reading carefully, please select the Other option and enter the word read in the space provided')." (§2.7)
  key_distinction: |
    ≠ manipulation check (below). ≠ comprehension check (below).
  why_it_matters: |
    Attention checks filter inattentive respondents, not the design. They're a necessary diagnostic but not a substitute for clear design — and overuse biases the sample.
  tags: [term, instrument]

---

- id: g10
  term: Manipulation check
  type: term
  author_definition: |
    "[a question that] can help test whether a given experimental manipulation worked as intended (e.g., participants noticed differences across experimental conditions)." (§3.2)
  key_distinction: |
    ≠ attention check (where failure = respondent issue). ≠ comprehension check (where failure = instructions issue).
  why_it_matters: |
    A high-quality experiment can still fail the manipulation check if the treatment is too subtle. A failed manipulation check is a treatment-validity problem, not a respondent or design problem.
  tags: [term, instrument]

---

- id: g11
  term: Comprehension check
  type: term
  author_definition: |
    "Reading comprehension checks can help test whether participants are reading carefully and understand key points from the survey questions and instructions." (§3.2)
  key_distinction: |
    ≠ attention check. Attention + comprehension can both pass or independently fail.
  why_it_matters: |
    A respondent passing the attention check but failing the comprehension check means instructions are unclear — rewrite the instructions, not exclude the respondent.
  tags: [term, instrument]

---

- id: g12
  term: Selective attrition
  type: term
  author_definition: |
    "When filtering participants for any reason (or when participants drop out of the survey on their own), beware of selective attrition. When analyzing responses, check to see whether the pass-rate on checks, as well as the completion rate for the survey, is consistent across experimental conditions." (§3.2, citing Zhou & Fishbach 2016)
  key_distinction: |
    ≠ "drop-out" generally. Selective attrition is drop-out that's *systematically different across conditions*.
  why_it_matters: |
    This is the rarely-discussed failure mode that kills internal validity. Even clean design and clean checks can't save a study where condition-A lost the most-procrastinating respondents and condition-B kept them.
  tags: [term, internal-validity]

---

- id: g13
  term: Relative vs. absolute level
  type: term
  author_definition: |
    "surveys are often most useful in determining relative, but not absolute, levels." (§2.2, citing Hinkin 1998; Jolliffe 2001)
  key_distinction: |
    ≠ "ordinal vs. cardinal measurement scale". This distinction is about *question-form sensitivity*, not the response scale you coded.
  why_it_matters: |
    Conclusions that depend on the *number* (e.g., "X is the modal response") require benchmark items to upgrade relative-to-absolute. Conclusions that depend on the *comparison* (X > Y) are usually safe across framings.
  tags: [term, interpretation]

---

- id: g14
  term: Selective (vs. compensating) screening
  type: term
  author_definition: |
    "researchers [screen] to select participants with specific characteristics, or to check for comprehension or attention. However, be sure to offer some compensation to participants who do not pass the screening step." (§3.3)
  key_distinction: |
    ≠ "selective" in the statistical sense (sample selection). Here "selective" refers to the platform-level decision to *include or exclude* based on a screener.
  why_it_matters: |
    Every exclusion has a fairness cost — compensate the excluded or accept the reputation damage downstream.
  tags: [term, ethics]

---

- id: g15
  term: Convenience sample (MTurk)
  type: term
  author_definition: |
    "MTurk samples can be considered convenience samples. They are not representative of the general population." (§4.4)
  key_distinction: |
    ≠ "biased sample" generally. *Every* sample is biased in some way. The point is that the biases are *known* (younger, US/India, more educated) and you have to design the study around them.
  why_it_matters: |
    The right move is not "find a representative sample" (impossible at this price point) but "match the sample to the research question" — MTurk is fine for many applied-finance questions even though it isn't representative.
  tags: [term, sample-design]

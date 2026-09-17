# Candidate Frameworks (decision frameworks / mental models)

> Extracted from Survey Curious? Bergman, Chinco, Hartzmark, Sussman (2020).

---

- id: f01
  title: Three-layer survey integrity (questions → operations → platform)
  type: framework
  source_chapter: §2-4
  source_quote: |
    "Section 2 provides a non-comprehensive list of some of the most critical points to keep in mind when designing a survey. [...] Section 3 provides similar guidance around the practice of running surveys online by offering advice on best practices to follow when running studies online. Section 4 focuses on the practical issues associated with how to interact with popular software [...]" (§2 intro)
  summary: |
    The whole paper is structured as three stacked layers — first *what* to ask (question design, §2), then *how* to defend the response (operations, §3), then *who* you're surveying (platform & population, §4). A quality break at any layer invalidates the next; design brilliance can't save poor recruitment, perfect recruitment can't save leading questions.
  tags: [framework, survey-design, layers]

---

- id: f02
  title: Respondent's answer = function of their ability × willingness × interpretation
  type: framework
  source_chapter: §2.1
  source_quote: |
    "The key is to ask questions that participants are able and willing to answer. Obstacles to doing so include participants' preferences for privacy, limited memory, and limited ability to access their thoughts on certain topics."
  summary: |
    A response is the *triple intersection* of (i) the participant's ability to recall or introspect on the construct, (ii) their willingness to disclose honestly given social/privacy cost, (iii) their interpretation given the question's wording. Question design's job is to keep all three satisfied at once. A model-perfect economist question fails on (ii) for a private finance fact, (i) for a year-old behavior, and (iii) for any abstract construct.
  tags: [framework, respondent-constraints]

---

- id: f03
  title: Levels vs. comparisons — what's actually defensible from a survey
  type: framework
  source_chapter: §2.2
  source_quote: |
    "Thus, surveys are often most useful in determining relative, but not absolute, levels."
  summary: |
    When you ask for a *level* (probability of buying Stock XYZ), framing and order effects can move the answer materially. When you ask for a *comparison* (XYZ vs. ABC), systematic randomization of order/framing preserves the relative signal even if absolute levels are wrong. So conclusions should be drawn about ranked items or contrasts, not about magnitudes. To upgrade comparisons to level claims, add benchmark items you expect to register clearly.
  tags: [framework, interpretation, relative-vs-absolute]

---

- id: f04
  title: Converging evidence as cross-question triangulation
  type: framework
  source_chapter: §2.3
  source_quote: |
    "When possible, survey experiments can be designed more effectively when there are multiple question types that can be compared against one another. That way, if there are concerns about a specific question type (e.g., question framing), an alternative question type (e.g., with a different question framing) testing the same hypothesis can be used to provide additional support for the overall results."
  summary: |
    Don't trust a single survey item per construct. Always measure the same construct with at least two question types (state vs. choose, recall vs. infer, abstract vs. concrete). Cross-question agreement is the survey-design analog of robustness checks. If only one item, any bias in that item is your entire result.
  tags: [framework, robustness, triangulation]

---

- id: f05
  title: Question clarity as anti-attribute-substitution
  type: framework
  source_chapter: §2.4
  source_quote: |
    "In cases where participants do not understand the question, but try to answer accurately, they may engage in attribute substitution. This occurs when people reply to a complicated question with the answer to a simpler one."
  summary: |
    When a question is abstract or ambiguous, respondents try to be helpful by answering the *clearest* similar question they can extract — not the one you asked. The asker thinks they got a sincere opinion; they got a sincere opinion about a different construct. Fix: concreteness — name the index, name the dates, name the alternatives. Ambiguity is not okay; it converts your question into a different question invisibly.
  tags: [framework, question-design, attribute-substitution]

---

- id: f06
  title: Two-stage field test — pretetest with non-economists, then pilot 50-100
  type: framework
  source_chapter: §3.1
  source_quote: |
    "Before doing that, test it out yourself. Have a friend or two (ideally someone who is not an academic or at least not trained in economics) take the survey [...] do not launch the entire survey experiment all at once. If you are aiming to get 500 participants, run an initial survey experiment involving only 50−100 participants."
  summary: |
    One pilot is not enough — you need two stages. First, get non-economists to take it (they catch wording bugs you can't, because you can't unsee your own model). Second, run 50-100 real respondents before committing to full scale. The bugs found in pilot are bugs your first-stage test couldn't see — survey-instrument bugs only surface when respondents vary in reading speed, attention, and goal-orientation.
  tags: [framework, pilot, pretest, methodology]

---

- id: f07
  title: Three different "checks" — attention, comprehension, manipulation
  type: framework
  source_chapter: §3.2
  source_quote: |
    "Reading comprehension checks and manipulation checks can help you confirm whether your survey is being read and interpreted as intended. Reading comprehension checks can help test whether participants are reading carefully and understand key points from the survey questions and instructions. Manipulation checks can help test whether a given experimental manipulation worked as intended."
  summary: |
    Three diagnostic instruments get conflated but answer different questions:
    - **Attention check**: Are you paying attention at all? (Most basic)
    - **Comprehension check**: Are you understanding the question we asked? (Test your wording, not the respondent)
    - **Manipulation check**: Did your experimental treatment land? (Test the treatment, not the wording or respondent)
    High failure on attention → respondent-quality problem. High failure on comprehension → design problem. High failure on manipulation → treatment problem. They're not interchangeable, and the fix differs.
  tags: [framework, quality-checks, attention, comprehension, manipulation]

---

- id: f08
  title: Selective attrition as quietly fatal confound
  type: framework
  source_chapter: §3.2
  source_quote: |
    "When filtering participants for any reason (or when participants drop out of the survey on their own), beware of selective attrition. When analyzing responses, check to see whether the pass-rate on checks, as well as the completion rate for the survey, is consistent across experimental conditions."
  summary: |
    Drop-out is not random. If your treatment condition has higher drop-out, lower attention-pass rate, or higher comprehension-check failure, the remaining sample is *not* comparable to the control sample. Your treatment-vs-control comparison is now confounded with respondent type. The standard diagnostic: report pass-rate and completion-rate *per condition* and reject the study if they differ.
  tags: [framework, attrition, selection, internal-validity]

---

- id: f09
  title: Platform as implicit population choice
  type: framework
  source_chapter: §4.3, §4.4
  source_quote: |
    "MTurk samples can be considered convenience samples. They are not representative of the general population. [...] it is important for researchers to consider who they want their survey to be a representative sample of, and this will depend on your research goals. [...] College students are unlikely to have full-time jobs or be managing their finances in ways similar to adults outside of college. Thus, if your research question involves applied questions about financial management, MTurk might represent a more relevant population than an in-person survey experiment at a college campus."
  summary: |
    Choosing a recruitment platform is choosing a population. MTurk ≈ young, US/India, educated, web-savvy. Prolific ≈ US/UK, pre-screened, ethical-pay expectations. Lucid Theory/Marketplace ≈ US quota samples or specifically-targeted populations. The same survey on MTurk and Prolific isn't measuring "the same population" — it could be measuring two different things. Your *research question*, not your convenience, should drive this choice.
  tags: [framework, platform-selection, population, external-validity]

---

- id: f10
  title: Reputation as data-quality investment
  type: framework
  source_chapter: §3.4
  source_quote: |
    "You are not an anonymous requester. You have a reputation. And, you should aim to maintain a good one (e.g., by paying participants promptly and fairly). [...] There are many online blogs, such as https://turkerview.com/, that workers use to review requesters."
  summary: |
    Requesters on crowdsourcing platforms are visible to workers via Turker-review sites. Bad reputation → professional-survey-takers avoid your study → your respondent pool becomes only inexperienced/casual workers → data quality collapses silently. The investment: separate email, prompt payment, fair pay, monitoring of public reviews. This isn't PR — it's upstream of data quality.
  tags: [framework, reputation, fair-pay, data-quality]

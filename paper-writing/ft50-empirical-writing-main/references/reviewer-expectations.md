# Reviewer Expectations for FT50 Empirical Papers

This reference provides a structured guide to the expectations, critiques, and evaluation frameworks that reviewers apply to empirical papers submitted to FT50 journals. Understanding the reviewer's priors, heuristics, and typical concerns is essential for writing a paper that survives the review process.

---

## 1. The Identification-First Review Paradigm

### 1.1 The Centrality of Causal Identification

For any empirical paper in an FT50 journal, the reviewer's first and most important question is:

> **"Why should I believe that the estimated coefficient has a causal interpretation?"**

This question is asked before any consideration of contribution, novelty, or practical importance. A paper with questionable causal identification is typically rejected regardless of how interesting the research question is.

### 1.2 The Reviewer's Mental Checklist

Every FT50 reviewer evaluates an empirical paper against this implicit hierarchy:

1. **Identification credibility** (is the causal claim believable?)
2. **Robustness** (does the result survive reasonable perturbations?)
3. **Economic significance** (is the magnitude meaningful, not just statistically significant?)
4. **Mechanism evidence** (is there evidence for *why* the effect occurs?)
5. **Contribution** (does this advance knowledge beyond existing work?)
6. **Writing clarity** (is the argument accessible and well-structured?)

Note that contribution — the thing authors spend the most time developing — is evaluated *fifth*. The first four items are methodological and empirical gatekeepers.

### 1.3 The "One Fatal Flaw" Heuristic

Reviewers typically search for one fatal flaw that justifies rejection. If they find it, the rest of the paper's strengths become irrelevant. The most common fatal flaws by design:

| Design | Common Fatal Flaw |
|--------|-------------------|
| DID | Non-parallel pre-trends or TWFE with staggered treatment |
| RDD | McCrary test failure; bandwidth manipulation |
| IV | Weak instrument (F < 10); exclusion restriction implausible |
| RCT | Differential attrition; selective reporting of outcomes |
| Matching | Poor balance after matching; selection on unobservables ignored |
| Panel FE | No correction for serial correlation; endogenous selection into sample |
| Cross-section | No credible source of exogenous variation |

**The corollary for authors:** Your primary job is to make the fatal flaw unfindable. This means anticipating what the reviewer will look for and either (a) addressing it directly in the paper, or (b) acknowledging it honestly and bounding its consequences.

---

## 2. Discipline-Specific Reviewer Profiles

### 2.1 Finance (JF, JFE, RFS)

**Typical Reviewer Background:** Empirical corporate finance or asset pricing researcher. Strong econometrics training. Computational proficiency. Values identification rigour above all else.

**What Finance Reviewers Look For:**

1. **The "first stage" of identification:** For any treatment variable, the reviewer asks: "What determines the variation in this variable?" If the answer is not exogenous, the paper is in trouble. The reviewer will mentally construct an omitted variable that could generate the observed correlation and ask whether the author has ruled it out.

2. **Multiple identification strategies:** Finance reviewers are impressed by papers that identify the same effect using fundamentally different sources of variation. A paper that uses both a DID design (exploiting a regulatory change) and an IV design (exploiting a different source of variation) is substantially stronger than either alone.

3. **Clustering sophistication:** Finance data have complex dependence structures (firms over time, firms within industries, firms within states). Reviewers will ask: "What is the right level of clustering?" and expect the answer to be at least at the treatment assignment level. Double-clustering (firm × year) is increasingly the norm.

4. **Economic magnitude:** Finance reviewers care deeply about whether the coefficient is economically meaningful. An effect that is statistically significant but economically trivial (e.g., 2 basis points on ROA) will be dismissed. Always contextualise magnitudes: "A one-standard-deviation increase in X is associated with a Y% increase in firm value relative to the sample mean."

**The Five Most Common Criticisms in Finance Reviews:**

| Criticism | Frequency | Preemptive Response |
|-----------|-----------|---------------------|
| "Identification is not credible" | Very High | Multiple identification strategies; institutional detail; falsification tests |
| "Standard errors are not clustered correctly" | High | Cluster at treatment level; double-cluster; wild bootstrap with few clusters |
| "The instrument is not exogenous" | High | Detailed institutional argument for exclusion; Conley bounds; reduced-form emphasis |
| "Results are not economically significant" | Moderate | Standardise coefficients; compare to benchmark elasticities; cost-benefit calculation |
| "The mechanism is unclear" | Moderate | Cross-sectional heterogeneity; mediator analysis; qualitative evidence |

### 2.2 Accounting (JAR, JAE, TAR)

**Typical Reviewer Background:** Archival accounting researcher. Expert in financial reporting and disclosure. Comfortable with large-sample econometrics. Values construct validity and institutional detail.

**What Accounting Reviewers Look For:**

1. **Construct validity:** Accounting reviewers care enormously about whether the empirical proxy matches the theoretical construct. If you claim to measure "earnings quality," you must justify why discretionary accruals, restatements, or meets-or-beats captures the concept — and test alternatives. A table of pairwise correlations between alternative measures of the same construct is highly valued.

2. **Institutional context:** Accounting reviewers are domain experts in regulatory and reporting environments. They will question whether the institutional feature you exploit actually works the way you claim. Detailed institutional background, ideally with direct evidence (regulatory filings, FASB statements, SEC guidance), is essential.

3. **Alternative explanations from accounting theory:** Accounting reviewers will propose alternative explanations grounded in accounting mechanisms. If you find that firms increase disclosure after regulation X, the reviewer will ask: "Is this increased disclosure or just mechanical compliance? Is it informative disclosure or boilerplate?" Test these alternative interpretations.

4. **Measurement timing:** Accounting data are reported at discrete intervals with known lags. A common criticism: "The treatment variable and outcome variable are measured over different windows that overlap in ways that could induce mechanical correlation." Be precise about measurement timing.

**The Five Most Common Criticisms in Accounting Reviews:**

| Criticism | Frequency | Preemptive Response |
|-----------|-----------|---------------------|
| "The measure does not capture the construct" | Very High | Multiple measures; correlations; validation against known benchmarks |
| "Institutional feature is misinterpreted" | High | Detailed regulatory background; legal analysis; practitioner input |
| "Result is mechanical, not behavioural" | Moderate | Accounting identity decomposition; alternative mechanical benchmarks |
| "Sample selection is non-random" | Moderate | Heckman correction; sample selection discussion; comparison to population |
| "Magnitude is not practically important" | Moderate | Materiality thresholds; analyst/investor relevance; market reaction evidence |

### 2.3 Management (AMJ, SMJ, OS)

**Typical Reviewer Background:** Management or strategy scholar. Mixed methods comfort — some accept pure econometrics, others prefer qualitative triangulation. Values theoretical contribution and construct novelty.

**What Management Reviewers Look For:**

1. **Theoretical contribution:** Unlike finance and accounting, management reviewers place near-equal weight on theoretical contribution and empirical execution. A paper with mediocre identification but a genuinely new theoretical insight can be published. A paper with perfect identification but no theoretical novelty will be rejected. The theoretical contribution must be stated explicitly and early.

2. **Construct novelty:** Management values new constructs. If your independent variable is a new measure of "CEO humility" or "strategic agility," the reviewer will focus on construct validation — discriminant validity, convergent validity, nomological validity. A multi-trait multi-method (MTMM) matrix or at least a careful discussion of construct validity is expected.

3. **Endogeneity acknowledgement and remediation:** Management reviewers are aware of endogeneity concerns but are often more accepting of careful acknowledgement than of technically dubious instrumentation. A thoughtful discussion of why endogeneity is unlikely to be fatal, combined with at least two empirical approaches, is the norm.

4. **Generalisability:** Management reviewers care about boundary conditions. "Under what conditions does this effect hold?" is a standard question. Heterogeneous treatment effects across industries, firm sizes, and time periods are valued.

**The Five Most Common Criticisms in Management Reviews:**

| Criticism | Frequency | Preemptive Response |
|-----------|-----------|---------------------|
| "The theoretical contribution is unclear" | Very High | Explicit statement of contribution in introduction; contrast with existing theory |
| "Endogeneity is not adequately addressed" | High | At least two identification strategies; qualitative evidence; honest limitations |
| "The construct is not validated" | High | Convergent/discriminant validity evidence; multiple measures; qualitative validation |
| "Results may not generalise" | Moderate | Multi-industry, multi-country sample; heterogeneity analysis; boundary conditions |
| "Mechanism is not tested" | Moderate | Mediation analysis; qualitative process evidence; moderators as mechanism tests |

### 2.4 Marketing (JM, JMR, MkSci)

**Typical Reviewer Background:** Quantitative marketing researcher. Expert in consumer behaviour, demand estimation, or marketing strategy. Values external validity and practical relevance.

**What Marketing Reviewers Look For:**

1. **External validity:** Marketing reviewers place unusually high weight on whether the results generalise beyond the specific study context. A field experiment with one firm in one category will be asked: "Does this generalise to other categories? Other firms? Other customer segments?" These questions are not optional — they expect evidence or at least compelling arguments.

2. **Practical significance for managers:** Marketing reviewers expect a clear statement of what a marketing manager should do differently based on the results. This is not optional window-dressing — it is a core element of the review. "So what should a CMO do?" is a question every marketing paper must answer.

3. **Consumer heterogeneity:** Aggregate effects that mask substantial consumer-level heterogeneity are viewed sceptically. Marketing reviewers expect distributional analysis — who benefits, who is unaffected, who responds negatively. Quantile treatment effects and latent class models are valued.

4. **Replication across methods:** Marketing reviewers value multi-method packages: field experiment + lab experiment + observational data. No single method is fully convincing; the convergence of evidence across methods is.

**The Five Most Common Criticisms in Marketing Reviews:**

| Criticism | Frequency | Preemptive Response |
|-----------|-----------|---------------------|
| "External validity is limited" | Very High | Multi-category, multi-firm evidence; boundary condition discussion |
| "Managerial implications are unclear" | High | Explicit "what managers should do" paragraph; ROI calculation |
| "Consumer heterogeneity is ignored" | High | Quantile regressions; latent class analysis; segment-specific effects |
| "Demand-side mechanism is not identified" | Moderate | Mediation; process measures; qualitative consumer interviews |
| "Endogeneity is not addressed" | Moderate | Field experiment; IV; panel data with consumer FE |

### 2.5 Operations Management (MSOM, POM)

**Typical Reviewer Background:** Operations management or management science researcher. Values analytical rigour. Comfortable with structural models. Increasingly values empirical work with clean identification.

**What Operations Reviewers Look For:**

1. **Link to operational practice:** Operations reviewers care about whether the empirical finding translates into operational decisions — inventory policy, capacity planning, quality control, supply chain design. The paper must connect the empirical estimate to an operational decision variable.

2. **Structural vs. reduced-form:** Many operations reviewers are trained in structural modelling and may prefer a structural interpretation. If using reduced-form methods, be explicit about how the reduced-form parameter maps to the structural parameter of interest.

3. **Process-level evidence:** Operations reviewers want to see the mechanism at the operational level. It is not enough to show that lean manufacturing improves financial performance — show that it reduces defect rates, decreases lead times, or increases capacity utilisation.

4. **Robustness to operational context:** Results should be robust to different operational environments — different production technologies, different demand patterns, different supply chain configurations.

**The Five Most Common Criticisms in Operations Reviews:**

| Criticism | Frequency | Preemptive Response |
|-----------|-----------|---------------------|
| "The link to operational practice is unclear" | High | Explicit operational decision variable; managerial levers identified |
| "The mechanism is not shown at the operational level" | High | Process-level data; operational intermediate outcomes |
| "Endogeneity is not addressed" | Moderate | Natural experiment; IV using operational shocks |
| "Results depend on specific operational context" | Moderate | Multi-plant, multi-firm evidence; contextual robustness |
| "The empirical estimate is not connected to a decision model" | Moderate | Structural interpretation of reduced-form estimates; counterfactual simulations |

### 2.6 Economics (AER, Econometrica, QJE, REStud)

**Typical Reviewer Background:** Academic economist. World-class econometrics training. Values formal identification arguments, methodological novelty, and theoretical microfoundations.

**What Economics Reviewers Look For:**

1. **Formal identification argument:** Economics reviewers expect a formal statement of the identifying assumptions and the conditions under which the estimator recovers the causal parameter of interest. A section titled "Identification" or "Econometric Framework" is standard. Hand-waving about "exogenous variation" without a formal argument is met with scepticism.

2. **Methodological contribution:** The top economics journals (Econometrica, QJE) expect a methodological contribution alongside the empirical one. A new estimator, a new identification approach, or a new method for testing assumptions is expected. The AER and REStud are somewhat more accepting of purely empirical contributions with strong identification.

3. **Power and inference:** Economics reviewers scrutinise power calculations, pre-analysis plans, and multiple testing adjustments. If the experiment is underpowered, the reviewer will note that the confidence intervals are too wide to distinguish the estimated effect from economically meaningful alternatives.

4. **External validity through theory:** Rather than demanding multi-context empirical evidence, economics reviewers prefer a theoretical model that clarifies the conditions under which the result generalises. The model defines the scope of external validity.

**The Five Most Common Criticisms in Economics Reviews:**

| Criticism | Frequency | Preemptive Response |
|-----------|-----------|---------------------|
| "The identifying assumptions are not credible" | Very High | Formal identification argument; multiple estimators; sensitivity analysis |
| "The econometric method is not appropriate" | High | Derive the estimator; show its properties; compare to alternatives |
| "The confidence intervals are too wide to be informative" | Moderate | Power analysis; pre-registration; honest inference |
| "There is no formal model" | Moderate | Theoretical framework section; microfoundations for reduced-form specification |
| "The contribution is incremental" | Moderate | Clear contrast with prior work; explicit statement of what is new |

---

## 3. Common Criticisms by Section and How to Preempt

### 3.1 Introduction

| Criticism | Preemption |
|-----------|------------|
| "The research question is not motivated" | First paragraph: empirical puzzle or theoretical tension. Second paragraph: why it matters. Third: what you do. |
| "The contribution is unclear" | An explicit contribution paragraph: "We contribute to three literatures. First,... Second,... Third,..." |
| "The paper overclaims" | Use precise language: "suggestive evidence," "consistent with," "we estimate." Avoid "prove," "demonstrate conclusively," "establish." |

### 3.2 Institutional Background / Theory

| Criticism | Preemption |
|-----------|------------|
| "The institutional detail is incorrect" | Cite primary sources (regulations, laws, policy documents). Include dates, thresholds, and precise eligibility criteria. |
| "The theoretical framework is disconnected from the empirics" | End the theory section with testable predictions that map to specific regression coefficients. |
| "The hypothesis is obvious / tautological" | Distinguish between "what we expect" and "what is not obvious." The hypothesis should be in doubt ex ante. |

### 3.3 Data and Sample

| Criticism | Preemption |
|-----------|------------|
| "Sample selection is not transparent" | Include a sample selection flowchart (CRSP → Compustat merge → filter steps → final sample). Report observations lost at each step. |
| "Measurement is not valid" | Validate measures against known benchmarks. Report correlations with related constructs. |
| "The sample is not representative" | Compare sample characteristics to population characteristics. Discuss external validity honestly. |

### 3.4 Empirical Design / Identification

| Criticism | Preemption |
|-----------|------------|
| "The source of variation is not exogenous" | Provide institutional detail about what causes variation in the treatment. Document that pre-treatment covariates do not predict treatment. |
| "The parallel trends assumption is violated" | Event study plot with pre-trend coefficients. Joint F-test. Rambachan & Roth (2023) sensitivity. |
| "The design is underpowered" | Ex ante power calculation. Ex post minimum detectable effect. Discuss whether the detected effect is economically meaningful. |

### 3.5 Results

| Criticism | Preemption |
|-----------|------------|
| "The table does not convey information clearly" | Use the Coefficient of Interest pattern (see Writing Patterns reference). Stars, standard errors, and sample sizes are essential. |
| "The coefficient sign is counterintuitive" | Acknowledge explicitly. Offer possible explanations. Do not ignore. |
| "The effect is statistically significant but economically trivial" | Standardise coefficients. Compare to benchmark elasticities. Contextualise with descriptive statistics. |

### 3.6 Robustness

| Criticism | Preemption |
|-----------|------------|
| "Robustness checks are selective" | Organise by the five-level pyramid. Address all five levels. If a level is not applicable, explain why. |
| "The robustness checks are perfunctory" | Each check should address a specific threat. Name the threat. Explain how the check addresses it. |
| "Oster delta is not reported" | Report Oster (2019) delta for $R_{max}$ at 1.0×, 1.3×, and 2.2×. Discuss interpretation. |

### 3.7 Mechanisms / Channels

| Criticism | Preemption |
|-----------|------------|
| "Correlation is not mechanism" | Distinguish between "consistent with the mechanism" and "the mechanism is identified." Acknowledge that alternative mechanisms are possible. |
| "The mechanism test is endogenous" | Acknowledge that the mediator is likely endogenous. Use qualitative evidence, heterogeneity patterns, or instrumental variables for the mediator. |
| "There are too many mechanisms and no clear test" | Focus on 1–2 mechanisms. Design tests that distinguish between them. Avoid laundry lists. |

### 3.8 Conclusion

| Criticism | Preemption |
|-----------|------------|
| "The conclusion just restates the results" | Discuss implications for theory, practice, and policy. Suggest future research that follows naturally. |
| "The limitations are omitted or minimised" | Include an Honest Limitation section (see Writing Patterns). Acknowledge what the paper cannot do. |
| "The implications overreach" | Use conditional language: "If our estimates are causal, then..." Distinguish between what is established and what is suggestive. |

---

## 4. The Review Report Structure

### 4.1 Anatomy of a Typical Review

Most FT50 reviews follow a predictable structure. Understanding this structure helps authors preempt criticisms before they are written.

**Section 1: Summary (1 paragraph)**
> "This paper examines [research question] using [method] on [data]. The authors find that [main result]. The paper addresses [literature] and contributes by [contribution]."

This is the reviewer demonstrating they understood the paper. If they mischaracterise it, the authors have failed to communicate clearly.

**Section 2: Overall Assessment (1–2 paragraphs)**
> "The paper tackles an [important / timely / interesting] question. The identification strategy is [credible / creative / concerning]. The contribution to the literature is [substantial / incremental / unclear]."

This is where the reviewer's decision is foreshadowed. "Important question" + "credible identification" + "substantial contribution" = likely accept. Combinations of these with negative qualifiers = likely reject.

**Section 3: Major Concerns (numbered list, 3–6 items)**

The meat of the review. Each major concern typically has this structure:
1. Statement of the concern
2. Why it matters for interpretation
3. What the reviewer wants to see

Example: "My primary concern is with the parallel trends assumption. Figure 2 shows that treated and control firms follow different trajectories even before the policy change. The joint F-test of pre-treatment coefficients has a p-value of 0.07, which, while not significant at the 5% level, suggests potential violations. I would like to see: (a) a discussion of why firms with different pre-trends might have been differentially affected by other contemporaneous shocks, (b) Rambachan & Roth (2023) honest confidence sets, and (c) the inclusion of unit-specific linear trends as a robustness check."

**Section 4: Minor Concerns (numbered list, 3–8 items)**

These are typically about exposition, table formatting, or interpretation. They are easy to address but should be taken seriously — failing to address minor concerns signals carelessness.

**Section 5: Recommendation**

Reject, Major Revision, Minor Revision, or Accept. The actual recommendation matters less than the tone of the preceding sections — a "Major Revision" with solvable concerns is better than a "Minor Revision" that masks fundamental scepticism.

### 4.2 How Reviewers Are Selected

Understanding the reviewer selection process helps authors anticipate the reviewer's priors:

1. The editor identifies potential reviewers based on the paper's references, keywords, and the editor's knowledge of the field.
2. Reviewers typically come from the literature the paper cites (either authors cited or authors who cite the same literature).
3. This means: **every person you cite substantively is a potential reviewer.** Do not mischaracterise their work. Do not dismiss their contribution. Do not claim novelty that they might dispute.

---

## 5. Rebuttal Strategies for Empirical Papers

### 5.1 Structure of an Effective Rebuttal Letter

A rebuttal letter is a persuasive document. It should be organised as follows:

1. **Opening paragraph:** Thank the editor and reviewers. State that you have addressed all concerns. Summarise the key changes.

2. **Major changes overview:** Bullet-point list of 3–6 substantive changes made in response to reviewer feedback. This demonstrates responsiveness before the reviewer reads the detailed response.

3. **Point-by-point response:** For each reviewer comment:
   - Quote the comment (in *italics*)
   - State your response ("We agree and have..." or "We respectfully disagree because...")
   - Describe the change made to the paper (with page/line numbers)
   - Quote the new text if it is important

4. **Closing:** Restate gratitude. Indicate willingness to make further changes.

### 5.2 Hierarchy of Responses

| Reviewer Concern | Recommended Response |
|------------------|---------------------|
| Factual error | Apologise, correct, thank reviewer |
| Omitted analysis they request | Do the analysis. Add it to the paper or appendix. |
| Interpretation they disagree with | Clarify. If genuinely disagree, provide evidence for your interpretation. Acknowledge theirs as a possible alternative. |
| They want a fundamentally different paper | Politely explain that this is beyond scope. Note that the suggested analysis would be valuable for future work. |
| They misunderstand the paper | Rewrite the unclear section. Do not blame the reviewer for misunderstanding. |

### 5.3 The "One-Table Standard"

For empirical complaints, the most convincing response is: **show the result in a table.** A new table that directly addresses the reviewer's concern is worth more than paragraphs of argument. The implicit message is: "We heard your concern, we took it seriously, we did the work, and here is the evidence."

### 5.4 When to Push Back

It is acceptable (and sometimes necessary) to push back against reviewer requests when:

| Situation | Strategy |
|-----------|----------|
| Request requires data you do not have and cannot obtain | Explain why the data are unavailable. Acknowledge the limitation. Explain why the existing evidence is still informative. |
| Request would change the paper's contribution fundamentally | Politely decline. Note that the current framing has been validated by other reviewers and the editor. |
| Request is internally inconsistent | Point out the inconsistency gently. Propose a resolution. |
| Request is methodologically incorrect (rare) | Cite the methodological literature. Be deferential but correct. "We understand the intuition behind this concern, but the recent econometric literature (cite) shows that..." |

### 5.5 Common Rebuttal Mistakes

| Mistake | Why It Hurts |
|---------|-------------|
| Defensiveness / hostility | Reviewers are volunteers. Hostility ensures rejection. |
| Ignoring minor concerns | Signals carelessness. Address every concern, even if briefly. |
| Promising changes that do not appear in the revised manuscript | Reviewer will check. Broken promises destroy credibility. |
| Overclaiming in response ("This completely addresses the concern") | Respectful language: "We believe this addresses the concern" or "This evidence is consistent with..." |
| Adding robustness checks without discussing them in the text | Tables without narrative are not convincing. Integrate new results into the discussion. |
| Failing to track changes | Always provide both a clean version and a tracked-changes version. |

---

## 6. What Separates Accept from Reject at FT50 Journals

### 6.1 The Implicit Decision Criteria

Based on patterns across thousands of editorial decisions, the following factors distinguish accepted from rejected papers:

| Factor | Accept | Reject |
|--------|--------|--------|
| **Identification** | Clean, credible, multiple strategies | Questionable, single strategy, acknowledged weakness |
| **Contribution** | Novel question or novel answer to old question | Incremental contribution to narrow literature |
| **Robustness** | Comprehensive, anticipates all reasonable concerns | Perfunctory, addresses only obvious concerns |
| **Writing** | Clear narrative arc, motivation → method → results → implication | Disjointed, defensive, technically dense without narrative |
| **Tables** | Informative, well-formatted, self-contained | Cluttered, poorly labelled, require text to interpret |
| **Response to review** | Comprehensive, respectful, new evidence provided | Defensive, argumentative, minimal changes |

### 6.2 The Editor's Perspective

Editors at FT50 journals are overloaded. They receive 5–10× more submissions than they can publish. Their default mode is to search for reasons to reject. Your paper must make rejection difficult.

**What editors want:**
- A paper that reviewers will find easy to evaluate (clear research design → clear results → clear contribution)
- A paper unlikely to generate a split decision (one accept, one reject) — these consume excessive editorial time
- A paper that fits the journal's identity and readership
- A paper that will be cited (this matters more than editors admit)

**What editors avoid:**
- Papers where the editor cannot determine the contribution from the first two pages
- Papers where the identification is obviously flawed (editor has enough training to spot this)
- Papers where the writing is impenetrable (editor must understand the paper to assign reviewers)
- Papers that are likely to provoke hostile reviews (editor does not want to manage conflict)

### 6.3 The Desk Rejection Criteria

Approximately 30–50% of FT50 submissions are desk-rejected (rejected by the editor without review). Common reasons:

1. **No fit:** The paper does not match the journal's scope or audience.
2. **No contribution:** The editor cannot identify what is new.
3. **Fatal identification flaw:** The editor can see the identification problem immediately.
4. **Incremental extension:** The paper adds a minor twist to a well-known result.
5. **Poor writing:** The editor cannot understand the contribution or method.
6. **Wrong format:** The paper does not follow the journal's submission guidelines.

---

## 7. Journal-Specific Reviewer Quirks

### 7.1 Journal of Finance (JF)

- Expects a clear "takeaway" that can be summarised in one sentence for practitioners
- Values simplicity over complexity — a clean DID is preferred to a messy structural model
- Internet Appendix is unlimited; put everything there and keep the main paper tight
- Will desk-reject if the paper has no obvious connection to financial markets, institutions, or corporate decisions

### 7.2 Journal of Financial Economics (JFE)

- More tolerant of corporate finance topics that JF might find too narrow
- Expects extensive robustness — JFE papers often have 15+ tables in the main text
- Values economic mechanisms — "why" the effect occurs matters as much as "whether" it occurs
- Contracting, governance, and ownership structure are core topic areas

### 7.3 Review of Financial Studies (RFS)

- Most open to methodological innovation among the top three finance journals
- Values interdisciplinary approaches (finance + accounting, finance + law, finance + macro)
- More tolerant of longer papers with detailed institutional analysis
- Strong preference for papers that multiple subfields will cite

### 7.4 Academy of Management Journal (AMJ)

- Heavy emphasis on theoretical contribution — empirical execution is secondary
- Values qualitative and mixed-methods work alongside quantitative
- Requires explicit discussion of "practical implications for managers"
- Rejections often cite "insufficient theoretical contribution" even when empirics are strong

### 7.5 Strategic Management Journal (SMJ)

- Strategy-focused: the paper must speak to strategic management questions
- Values novel data — hand-collected datasets, surveys, proprietary data
- Tolerant of endogeneity concerns if the contribution is high and the limitation is acknowledged
- Expects discussion of boundary conditions and generalisability

### 7.6 American Economic Review (AER)

- Extremely competitive; acceptance rate ~5–8%
- Requires both a novel contribution and credible identification
- Papers with both theory and empirics are preferred to purely empirical papers
- The introduction must hook the reader in the first paragraph — reviewers read it first and form initial impressions

### 7.7 Review of Economic Studies (REStud)

- Values methodological innovation alongside empirical contribution
- More tolerant of structural approaches than AER
- Shorter papers (typically 40–45 pages) with tight arguments preferred
- Restudies (re-examinations of important prior results) are accepted if they substantially change the interpretation

---

## 8. Pre-submission Self-Audit Checklist

Before submitting to an FT50 journal, complete this audit:

### Identification

- [ ] Can I state the source of identifying variation in one sentence?
- [ ] Would a sceptical reader believe that this variation is exogenous? What evidence do I provide?
- [ ] Have I tested the key identifying assumptions (parallel trends, exclusion restriction, density continuity, etc.)?
- [ ] Have I used at least one robustness estimator for the chosen design?
- [ ] If using fixed effects: can I justify the level at which effects are absorbed?

### Contribution

- [ ] Can I state the contribution in one sentence without using "contributes to the literature by"?
- [ ] Have I contrasted my findings with the most closely related papers explicitly?
- [ ] Would my paper change how researchers in this field think about the phenomenon?
- [ ] Would my paper change how practitioners behave?

### Robustness

- [ ] Have I addressed all five levels of the robustness pyramid (or explained why a level is not applicable)?
- [ ] Have I reported Oster (2019) bounds for selection on unobservables?
- [ ] Have I tested alternative measures, samples, and specifications?
- [ ] Have I included at least one falsification or placebo test?

### Writing

- [ ] Does the introduction motivate the question, state the approach, preview the findings, and articulate the contribution — all within 3 pages?
- [ ] Can a reader understand the main result from the abstract alone?
- [ ] Are all tables self-contained (notes explain variables, sources, and sample)?
- [ ] Are figure axes clearly labelled with readable font sizes?
- [ ] Have I proofread for typos, inconsistent formatting, and missing references?

### Mechanics

- [ ] Does the paper follow the journal's submission guidelines (length, format, anonymisation)?
- [ ] Is the Internet Appendix or Online Supplement organised and referenced in the main text?
- [ ] Are all data sources documented and accessible (or is an exemption explained)?
- [ ] Is the code repository ready for submission (if required by the journal's data policy)?

---

## References

- Angrist, J. D., & Pischke, J.-S. (2009). *Mostly Harmless Econometrics*. Princeton University Press.
- Angrist, J. D., & Pischke, J.-S. (2014). *Mastering 'Metrics*. Princeton University Press.
- Bettis, R. A., Ethiraj, S., Gambardella, A., Helfat, C., & Mitchell, W. (2016). Creating repeatable cumulative knowledge in strategic management. *Strategic Management Journal*, 37(2), 257-261.
- Harvey, C. R. (2017). Presidential address: The scientific outlook in financial economics. *Journal of Finance*, 72(4), 1399-1440.
- Rynes, S. L. (2007). Editor's afterword: Let's create a tipping point: What academics and practitioners can do, alone and together. *Academy of Management Journal*, 50(5), 1046-1054.
- Zellner, A. (2007). Some aspects of the history of the causal order, identification, and exogeneity in econometrics. *Journal of Econometrics*, 137(2), 461-488.

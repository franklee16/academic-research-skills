# Empirical Corporate Finance Writing Style

**Source Papers:** Giroud (2013), Giroud & Mueller (2019)
**Typical Journals:** Journal of Finance, Journal of Financial Economics, Review of Financial Studies, Quarterly Journal of Economics, American Economic Review
**Field Code:** `ecf`

---

## 1. Tone and Voice

- **Confident but not arrogant.** Assertive but always supported by evidence. Avoid excessive hedging after results are established, but acknowledge limitations.
- **Precise and economical.** Every word serves a purpose. Concrete descriptions, not flowery language.
- **Reader-friendly.** Complex ideas introduced gently with simple examples or step-by-step buildup.
- **Authorial voice.** "We" for multiple authors, "I" for single author. Never "you" or "one." Present but modest.

---

## 2. Paper Structure

### Introduction
1. **Opening hook:** Broad, interesting observation or provocative quote (e.g., Williamson 1975)
2. **Problem statement:** What we don't know and why it matters
3. **This paper in a nutshell:** Approach, data, main findings — without burying reader in details
4. **Preview of identification strategy:** Key source of variation and intuition for why it works
5. **Results summary:** Quantitative estimates early (e.g., "an increase in plant-level investment of 8% to 9%")
6. **Roadmap:** Short paragraph at end

### Body Sections
- **Conceptual Framework / Model** (optional): Simple, minimal jargon, directly linked to empirical predictions
- **Data and Variables:** Sources, sample construction, summary statistics table early, variable definitions before results
- **Main Results:** Visual first (bin scatterplot) → regression tables with progressive buildup (simple → controls → fixed effects)
- **Identification and Robustness:** THE HEART. Anticipate every challenge. Each threat gets its own subsection. Mix of placebo tests, alternative samples, alternative fixed effects, direct controls.
- **Heterogeneity / Extensions:** Interaction terms, split-sample analyses supporting the mechanism
- **Aggregate Implications** (if applicable): County-level or higher-level analysis

### Conclusion
Short. Summarize contributions. No new results. Policy or welfare implications if appropriate.

---

## 3. Paragraph and Sentence Construction

### Paragraphs
- One main idea per paragraph
- First sentence states the point, rest supports it
- Moderate length (6-7 sentences max; short paragraphs for emphasis)
- Logical flow with transitions: "That being said," "By contrast," "Similarly," "To see this," "Formally," "Intuitively"

### Sentences
- Clear subject-verb-object structure
- Passive voice only for data/procedures ("are obtained," "is constructed")
- Active voice for interpreting results
- Short, punchy sentences for emphasis ("Both are intuitive.")
- Parallel structure when comparing: "While these shocks may directly affect X, they should not directly affect Y."

---

## 4. Explaining Identification: The Detective Story

**Key principle:** Make the reader feel smart by walking them through logic step by step.

### Step 1: Use a Concrete Example
> "Consider a company headquartered in Boston with a plant in Memphis. In 1985, the fastest way to travel from Boston to Memphis was an indirect flight with one stopover in Atlanta. In 1986, Northwest Airlines opened a new hub in Memphis..."

### Step 2: State the Threat Clearly
> "An important concern is that local shocks in the plant's vicinity could be driving both the introduction of new airline routes and plant-level investment."

### Step 3: Explain How You Address It
> "I can control for such local shocks by including MSA-year controls..."

### Step 4: Show the Result of the Fix
> "As is shown, the coefficient on... remains virtually unchanged."

### Step 5: Acknowledge Remaining Concerns
> "A potential concern is that regional shocks may differentially affect establishments even within a given 4-digit NAICS code industry..."

---

## 5. Presenting Results

### Tables
- Clean, clear variable names
- Self-contained notes describing all variables and specification completely
- Standard errors in parentheses; clustering explicitly stated
- Significance stars used, but main text reports coefficient AND economic magnitude
- Placebo tests alongside main results

### Figures
- Scatterplots or bin scatterplots for visual first impression
- Figure notes describe exactly what is plotted and how residuals are computed
- Slope reported directly on figure

### In-Text Interpretation Formula
**statistical significance + economic magnitude + real-world equivalent**

> "The coefficient is statistically highly significant. It is also economically significant. Given that the sample mean of plant-level investment is 0.10, an increase of 0.8 percentage points implies that investment increases by 8%, corresponding to an increase in capital expenditures of $158,000."

---

## 6. Handling Literature

- **Integrated into introduction and motivation**, not ghettoized into a separate section
- **No laundry lists.** Each cited paper tied to a specific point
- **Contrast clearly.** "By contrast, little is known about whether and how..."
- **Never:** "A large literature has studied... (see X, Y, Z for a survey)."
- **Instead:** "Prior research has shown that... (Author, Year)."

---

## 7. Common Phrases and Constructions

| Function | Phrase |
|----------|--------|
| Introducing a point | "A prominent feature of..." / "A defining feature of..." |
| Referring to evidence | "Consistent with this prediction, we find..." / "As prior research has shown..." |
| Presenting a result | "As is shown, the coefficient..." / "We find that..." / "The results suggest that..." |
| Acknowledging a concern | "An important concern is..." / "A potential concern is..." / "One might worry that..." |
| Addressing a concern | "To account for this possibility..." / "To assess this concern..." / "We address this issue by..." |
| Emphasizing robustness | "The results are virtually identical if..." / "All our results are similar if..." |
| Qualifying a statement | "That being said," / "Although this is of course speculative," / "Arguably," |
| Explaining intuition | "Intuitively," / "The idea is that..." / "To see this,..." |
| Smooth transitions | "Let us briefly comment on..." / "We proceed analogously in panel B..." / "Two robustness checks deserve special mention." |
| Concluding | "Overall, these results suggest that..." / "We may thus conclude that..." |

---

## 8. The Ideal First Two Pages

1. **Broad motivation (1-2 sentences).** Connect to big idea or famous quote.
2. **What we know / don't know (2-3 sentences).** Briefly summarize prior research and gap.
3. **This paper's approach (2-3 sentences).** Data, setting, key source of variation.
4. **Main results (1-2 sentences).** Quantitative findings upfront.
5. **Why identification is credible (1-2 sentences).** Hint at methods (fixed effects, natural experiment).
6. **Additional results / contributions (1-2 sentences).** Mechanism tests or aggregate implications.
7. **Roadmap (1 sentence).** "The rest of this paper is organized as follows."

---

## Checklist for ECF Style

- [ ] Introduction grabs attention and states contribution immediately
- [ ] All empirical challenges anticipated and addressed with concrete examples
- [ ] Coefficients interpreted in both statistical AND economic terms (with dollar-equivalent)
- [ ] Tables and figures have self-contained notes
- [ ] Sentences clear, direct, free of unnecessary jargon
- [ ] Identification told like a detective story: threat → solution → result
- [ ] Placebo tests central, not afterthought
- [ ] Paper modular (reader can skip intro → conclusion and get main message)
- [ ] Literature integrated, not listed
- [ ] Conclusion avoids repeating all results; focuses on implications

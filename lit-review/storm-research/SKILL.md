---
name: storm-research
description: >
  Conduct Stanford STORM-style deep research: multi-perspective exploration, structured Wikipedia-style
  reports with citations. Use when the user wants thorough research on any topic, a literature review,
  comprehensive analysis, topic primer, or Wikipedia-quality report. Triggers include: "research X",
  "tell me about X", "write a report on X", "deep dive into X", "comprehensive analysis of X",
  "literature review on X", "what is X", "how does X work", "explore X", "investigate X",
  "understand X", "explain X", "give me the full picture on X". This skill uses Tavily Search
  for research-grounded responses with inline citations. Inspired by Stanford OVAL's STORM
  (Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking).
compatibility: Tavily MCP (mcp__tavily__tavily-search, mcp__tavily__tavily-extract)
---

# Storm Research Skill

Conduct thorough, multi-perspective research inspired by Stanford OVAL's STORM methodology and produce Wikipedia-quality reports with citations.

## The STORM Philosophy

STORM (Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking) breaks research into two stages:

1. **Pre-writing stage**: Research from multiple angles, generate outline
2. **Writing stage**: Produce structured article with citations

The core insight: **good research comes from asking good questions from multiple perspectives.**

## Research Workflow

### Phase 1: Topic Decomposition

When given a topic, break it down:

```
Topic: [given topic]

Main Question: What is [topic] and what are its key aspects?

Perspectives to Explore:
1. [Definition/Core concepts] - What is it fundamentally?
2. [History/Origin] - How did it develop?
3. [Mechanism/How it works] - What are the key components?
4. [Applications/Uses] - How is it applied in practice?
5. [Evidence/Research] - What does the evidence say?
6. [Debates/Criticisms] - What are the limitations or controversies?
7. [Recent developments] - What's new in the field?
```

### Phase 2: Multi-Perspective Research

For each perspective, formulate specific questions and search for answers.

#### Question Types to Ask

| Perspective | Questions to Generate |
|-------------|----------------------|
| **Definition** | What is X? What are the key definitions? How is it defined by different sources? |
| **History** | When did X emerge? What was the context? Who were the key figures? |
| **Mechanism** | How does X work? What are the components? What is the process? |
| **Evidence** | What research supports X? What are the key studies? What evidence exists? |
| **Applications** | How is X used? What are the practical applications? |
| **Criticisms** | What are the limitations? What criticisms exist? What are the debates? |
| **Recent** | What are the latest developments? What has changed recently? |

### Phase 3: Source Collection

Use Tavily Search for grounded research. Conduct **MULTIPLE search rounds** to maximize citation coverage:

#### Round 1: Overview (3-5 searches)
```
- "[topic] overview"
- "[topic] introduction guide"
- "what is [topic]"
- "[topic] definition"
```

#### Round 2: Academic/Research (3-5 searches)
```
- "[topic] research study"
- "[topic] academic paper"
- "[topic] evidence statistics"
- "[topic] key findings"
```

#### Round 3: Platform/Application Specific (2-3 searches)
```
- "[specific platform] [topic]"
- "[topic] industry applications"
- "[topic] case study"
```

#### Round 4: Critical/Alternative View (3-5 searches)
```
- "[topic] problems limitations"
- "[topic] criticism debates"
- "[topic] challenges"
- "[topic] vs alternatives"
- "[topic] comparison"
```

#### Round 5: Current/Recent (2-3 searches)
```
- "[topic] latest developments 2025 2026"
- "[topic] recent news"
- "[topic] future trends"
```

**CRITICAL: Track your sources!** Create a running list as you research:
```
Sources found:
1. [Title](URL) - Brief description
2. [Title](URL) - Brief description
...
```

Aim for 20-30 unique sources. Use tavily-extract on the most promising URLs to get detailed content.

### Phase 4: Outline Generation

Based on collected information, create a structured outline with **AT LEAST 10 sections**:

```markdown
# [Topic] - Research Outline

## I. Executive Summary
   A. Brief overview of topic
   B. Key findings
   C. Main conclusions

## II. Introduction
   A. Background and context
   B. Why this topic matters
   C. Scope of this report

## III. Definition and Core Concepts
   A. What is [topic]
   B. Key terminology
   C. Fundamental principles

## IV. How It Works/Mechanism
   A. Technical explanation
   B. Key components/process
   C. Supporting theory

## V. Applications and Use Cases
   A. [Application area 1 with examples]
   B. [Application area 2 with examples]
   C. [Application area 3 with examples]

## VI. Evidence and Research
   A. [Key study 1 with statistics]
   B. [Key study 2 with statistics]
   C. [Key study 3 with statistics]

## VII. Comparison with Alternatives
   A. [Alternative method 1] vs [topic]
   B. [Alternative method 2] vs [topic]
   C. [Quantitative comparison table if possible]

## VIII. Regulatory/Legal Considerations
   A. Current regulatory framework
   B. Legal issues
   C. Compliance considerations

## IX. Challenges and Limitations
   A. [Limitation/criticism 1]
   B. [Limitation/criticism 2]
   C. [Potential solutions]

## X. Current Developments
   A. Recent news/events
   B. Emerging trends
   C. Future directions

## XI. Key Takeaways
   A. [Main finding 1]
   B. [Main finding 2]
   C. [Main finding 3]

## XII. Conclusion
   A. Summary
   B. Implications
   C. Next steps/recommendations
```

### Phase 5: Article Generation

Write the full report following the outline, with:

- **Inline citations**: `[Source Name](URL)` for every factual claim
- **Specific facts**: Names, dates, figures, statistics (with sources!)
- **Balanced coverage**: Different perspectives acknowledged
- **Clear structure**: Headings, subheadings, logical flow
- **Comparison tables**: Include tables comparing alternatives when relevant
- **Alternative coverage**: Always include a section comparing to similar platforms/methods
- **Statistics with context**: Every percentage/stat should have comparison to baseline

## Citation Format

Use inline parenthetical citations:

```markdown
According to Smith et al. (2023), the effectiveness of X is well-documented
([Smith et al., 2023](https://example.com/source)).

For a comprehensive overview, see the [Wikipedia article on Topic X](https://en.wikipedia.org/wiki/Topic_X).
```

Or footnote-style:

```markdown
This claim is supported by multiple sources.[^1][^2]

[^1]: Author Name, "Article Title," Publication, Year. URL
[^2]: Another Source, "Another Article," Year. URL
```

## Output Structure

### Full Report Format

**TARGET: 10+ sections, 20-30 citations**

```markdown
# [Topic] - Comprehensive Research Report

**Research Date:** [Date]
**Sources:** [Number] sources consulted (aim for 20-30)
**Perspectives Covered:** [List of angles explored]

---

## Executive Summary
[2-3 paragraph overview of the topic, key findings, and conclusions]

---

## 1. Introduction
[Background on why this topic matters, scope of this report]

## 2. Definition and Core Concepts
[What the topic is, key definitions, fundamental principles]

## 3. Historical Context
[Origins, key milestones, evolution of the topic]

## 4. How It Works/Mechanisms
[Technical details, process explanations, key components]

## 5. Applications and Use Cases
[Practical applications, real-world examples with specific companies/institutions]

## 6. Evidence and Research
[Key studies, findings, with specific statistics and comparisons]

## 7. Comparison with Alternatives
[Compare to similar methods/platforms. Include comparison table where relevant]

## 8. Regulatory/Legal Considerations
[Legal framework, compliance issues, regulatory landscape]

## 9. Challenges and Limitations
[Problems, criticisms, potential solutions]

## 10. Current Developments
[Recent news, emerging trends, future directions]

## 11. Key Takeaways
[Bullet point summary of 5-7 main findings]

## 12. Conclusion
[Summary of key takeaways, implications, recommendations]

---

## References

1. [Source Title](URL) - Brief description of this source
2. [Source Title](URL) - Brief description of this source
[... aim for 20-30 total references]
```

## Quality Standards

### Citation Requirements (MINIMUM 15 citations)
- **Target 20-30 inline citations** per report - this is a key quality indicator
- Every factual claim must have a source
- Include academic papers (SSRN, journals), industry reports, reputable news
- Cite specific studies with authors and years
- Include URLs for all sources for verification
- At least 3-5 academic/research citations for credibility

### Section Requirements (MINIMUM 10 sections)
Ensure your report includes ALL of the following sections:

1. **Executive Summary** - 2-3 paragraph overview
2. **Introduction** - Background and scope
3. **Definition/Core Concepts** - What the topic is
4. **Mechanism/How It Works** - Technical explanation
5. **Applications/Use Cases** - Practical examples
6. **Evidence/Research** - Key studies and findings with specific statistics
7. **Comparison with Alternatives** - Compare to existing methods/competitors
8. **Regulatory/Legal Considerations** - Legal framework, compliance issues
9. **Challenges/Limitations** - Problems and criticisms
10. **Current Developments** - Recent news and trends
11. **Key Takeaways** - Bullet point summary of main findings
12. **References** - Full citation list with URLs

## Handling Different Topic Types

### For ALL Topics - Include These Elements

Regardless of topic type, ALWAYS include:
- **Comparison section**: Compare to at least 2-3 alternatives
- **Regulatory section**: Legal/regulatory considerations (even if brief)
- **Comparison table**: When comparing platforms/services, include a markdown table
- **Statistics with baselines**: When citing accuracy/effectiveness, compare to baselines

### Academic/Research Topics
- Include theoretical frameworks
- Cite peer-reviewed sources (aim for 5+ academic citations)
- Cover seminal papers with authors and years
- Note methodological debates
- Include comparison with other research approaches

### Technical/How-To Topics
- Clear step-by-step explanations
- Prerequisites noted
- Variations/alternatives covered
- Common pitfalls listed
- Include comparison with alternative tools/methods

### Current Events/News
- Timeline of events
- Multiple stakeholder perspectives
- Data and statistics where available
- Acknowledge evolving information
- Compare to similar past events

### Explainer/Definition Topics
- Clear definitions first
- Build complexity gradually
- Use analogies for clarity
- Include examples
- Compare to related concepts

### Platform/Service Research (e.g., Polymarket, Kalshi)
- Always include: What are the alternatives? How do they compare?
- Regulatory status comparison
- Feature comparison table
- Market share/usage comparison
- Pros/cons for each platform

## Comparison Tables

When your report covers multiple platforms, services, or methods, **INCLUDE A COMPARISON TABLE**:

```markdown
| Feature | Platform A | Platform B | Platform C |
|---------|------------|------------|------------|
| Focus Area | ... | ... | ... |
| Regulation | ... | ... | ... |
| User Base | ... | ... | ... |
| Key Feature 1 | ... | ... | ... |
| Key Feature 2 | ... | ... | ... |
| Pricing | ... | ... | ... |
```

This is especially important for:
- Technology platform comparisons
- Service/product comparisons
- Method comparison (prediction markets vs polls vs analyst forecasts)
- Country/region comparisons

## Example Research Session

**User:** "Research prediction markets for corporate earnings forecasting"

**Claude's approach:**

1. **Topic decomposition**: Break into perspectives (definition, mechanism, platforms, accuracy evidence, comparisons, limitations, regulations)

2. **Multi-round searches** (15-25 total):
   - Round 1: Overview (3 searches)
   - Round 2: Academic/research (4 searches)
   - Round 3: Platform specific (3 searches - Polymarket, Kalshi, alternatives)
   - Round 4: Critical view (3 searches)
   - Round 5: Current news (2-3 searches)

3. **Extract from key sources**: Get full content from 5-8 most promising URLs

4. **Outline creation** (12 sections):
   - Executive Summary
   - Introduction
   - Definition/Core Concepts
   - How It Works
   - Applications (with examples)
   - Evidence/Research (with stats)
   - **Comparison with Alternatives** (table comparing Polymarket, Kalshi, Metaculus)
   - Regulatory Considerations
   - Challenges/Limitations
   - Current Developments
   - **Key Takeaways** (bullet points)
   - Conclusion
   - References (20-30 citations)

5. **Report writing**: With citations inline, comparison table, specific statistics

6. **Output**: Comprehensive markdown report saved to file

## Tavily MCP Integration

### Search Tool Usage

**IMPORTANT: Do multiple search rounds!** Don't just search once. Each round should target a different angle.

```javascript
// Round 1: Overview searches (3-5 queries)
// Round 2: Academic/research searches (3-5 queries)
// Round 3: Platform/application specific (2-3 queries)
// Round 4: Critical views (3-5 queries)
// Round 5: Recent news (2-3 queries)

// Example: Overview search
mcp__tavily__tavily-search({
  query: "[topic] overview",
  max_results: 5,
  search_depth: "basic"
})

// Example: Academic research search
mcp__tavily__tavily-search({
  query: "[topic] research study paper statistics",
  max_results: 8,
  search_depth: "advanced"
})

// Example: Critical/debates search
mcp__tavily__tavily-search({
  query: "[topic] problems limitations criticism",
  max_results: 8,
  search_depth: "advanced"
})

// Extract full content from top sources (use 3-5 times per report)
mcp__tavily__tavily-extract({
  urls: ["https://example.com/key-source-1", "https://example.com/key-source-2"],
  extract_depth: "advanced"
})
```

### Target: 20-30 Citations

For a comprehensive report, you should:
- Run 15-25 Tavily searches across all rounds
- Extract content from 5-10 key URLs
- Cite at least 20-30 sources in the final report
- Include 3-5 academic/research citations (papers, journals)

### Search Query Strategies

| Research Goal | Query Strategy |
|--------------|----------------|
| Basic understanding | "[topic] what is", "[topic] guide" |
| Academic depth | "[topic] research study", "[topic] paper" |
| Technical details | "[topic] how it works", "[topic] mechanism" |
| Current state | "[topic] latest", "[topic] 2025 2026" |
| Practical use | "[topic] applications", "[topic] use cases" |
| Critical view | "[topic] problems", "[topic] criticism" |

## After Research

When research is complete:

1. **Offer to save**: "Should I save this as a markdown file?"
2. **Suggest follow-up**: "Would you like me to research [related topic]?"
3. **Note gaps**: "There are some areas I'd need to research further if you need more detail on [specific aspect]."
4. **Ask for focus**: "Would you like me to expand on any particular section?"

## Skill Invocation Tips

When this skill is triggered:
1. Acknowledge the research goal
2. Mention you'll use multi-perspective research with citations
3. Optionally clarify scope if very broad
4. Execute research workflow
5. Deliver structured report
6. Offer next steps

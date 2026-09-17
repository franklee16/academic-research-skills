# Writing Style for Empirical Finance

## Table of Contents

1. [Core Principles](#core-principles)
2. [Voice and Tense](#voice-and-tense)
3. [Sentence Structure](#sentence-structure)
4. [Paragraphs](#paragraphs)
5. [Words and Phrases to Avoid](#words-and-phrases-to-avoid)
6. [Finance-Specific Style](#finance-specific-style)
7. [Common Pitfalls](#common-pitfalls)

---

## Core Principles

**Be precise.** Choose words carefully so you say what you mean. Replace "performance" with "monthly return," "accuracy" with "R-squared," "significant" with the actual t-statistic.

**Be concise.** After writing initial text, try to delete one-third of the words. Most first drafts are 30-50% too long.

**Be simple.** English is not the first language for many readers of finance journals. Avoid rare words or jargon when plain language works.

**Be consistent.** Use the same term for the same concept throughout the paper. No synonyms for key variables or concepts.

## Voice and Tense

### Active vs. Passive Voice

**Default: use active voice.** It is clearer and more direct.

| Avoid (passive) | Prefer (active) |
|-----------------|-----------------|
| "It is found that DS Score predicts returns" | "We find that DS Score predicts returns" |
| "The data were collected from CSMAR" | "We collect data from CSMAR" |
| "It has been shown by [Author] that..." | "[Author] shows that..." |

**Exception: passive voice is acceptable in data and methodology sections** where the actor is obvious and emphasis should be on the process:
- "Returns are computed using daily closing prices"
- "Standard errors are clustered by firm and month"
- "Firms are excluded if they have fewer than 24 months of coverage"

### Tense Conventions

| Section | Tense | Example |
|---------|-------|---------|
| Related work | Present or past | "[Author] finds / found that..." |
| Data / Methods | Past | "We collected..." / "We estimated..." |
| Results | Past for what you did, present for what it means | "The coefficient was 0.23 (t = 3.41). This suggests that..." |
| Conclusion | Present | "Our results suggest..." |

## Sentence Structure

**Put the verb early.** Early verbs make sentences easier to parse.

| Avoid | Prefer |
|-------|--------|
| "The relationship between analyst text quality and subsequent stock returns, controlling for firm size and book-to-market, is positive and significant" | "Analyst text quality positively predicts subsequent stock returns, controlling for firm size and book-to-market" |

**One idea per sentence.** If a sentence has two ideas, split it.

| Avoid | Prefer |
|-------|--------|
| "DS Score predicts returns and this effect is stronger for small firms" | "DS Score predicts returns. This effect is stronger for small firms." |

**Long sentences are fine if the words are simple.** A sentence with 30 common words is better than a sentence with 15 rare words.

## Paragraphs

- **Lead with a strong topic sentence.** The reader should know what the paragraph is about from the first sentence.
- **End with a strong closing sentence.** Middle sentences are for elaboration.
- **Every sentence should add information.** If a sentence merely restates the previous one, delete it.
- Ask about every word: "Is this necessary?" Ask about every sentence: "Can I phrase this more simply?"

## Words and Phrases to Avoid

### Remove These

| Remove | Why |
|--------|-----|
| "actually" | Adds nothing |
| "a bit" | Imprecise |
| "very", "really", "extremely" | If you need these, your evidence is not strong enough |
| "to our knowledge" | If you are not sure, search harder |
| "note that", "observe that" | Just state the fact |
| "try to" | Either you did it or you did not |
| "it is worth noting that" | If it is worth noting, just note it |
| "in order to" | Just "to" |
| "the fact that" | Usually deletable |

### Replace These

| Replace | With |
|---------|------|
| "want to", "hope to" | "aim to" |
| "performance" | The specific metric (returns, alpha, R-squared) |
| "good", "bad", "nice" | The specific quality you mean |
| "a number of" | The specific number, or "several" |
| "in the context of" | Just name the context |
| "in this paper, we" | "We" |

### Hedging

**Social science requires some hedging, but stack hedging is a red flag.**

| Avoid (stacked) | Acceptable |
|-----------------|------------|
| "It may perhaps potentially suggest that text might have some predictive power" | "Our results suggest that text has predictive power" |
| "We somewhat find evidence that could indicate..." | "We find evidence that..." |

**Rule:** Use at most one hedge word per claim. Choose the strongest hedge your evidence supports:
- "proves" -- almost never appropriate
- "demonstrates" -- strong, requires clean identification
- "shows" -- standard for well-supported claims
- "suggests" -- for correlational or suggestive evidence
- "is consistent with" -- for mechanism tests

### Other Style Points

- **Minimize pronouns.** If you use "this," make it an adjective: "this result," "this specification"
- **Do not start every sentence with "We."** Vary sentence openings, but not at the cost of clarity
- **"On the other hand" requires "On the one hand"** first, or use a different transition
- **Never use a comparative without specifying both sides:** "returns are higher" -> "returns are higher than for the low-score quintile"
- **Cite any claim not supported by your own evidence**
- **Avoid grandiose language.** "This paper makes a groundbreaking contribution" -- no, just state what you did

## Finance-Specific Style

### Reporting Numbers

- Always report t-statistics in parentheses below coefficients
- Use asterisks consistently: * p<0.10, ** p<0.05, *** p<0.01
- Report economic magnitudes alongside statistical significance
- Round appropriately: 1.33% per month, not 1.32847% per month
- Use consistent decimal places within a table

### Variable Names in Text

- First mention: full name followed by abbreviation in parentheses -- "DeepSeek Score (DS Score)"
- Subsequent mentions: abbreviation only -- "DS Score"
- Never redefine or use synonyms once introduced

### Cross-Referencing Results

- Reference tables and figures by number: "Table 3 reports..." not "the following table shows..."
- Use present tense for discussing your own tables: "Table 3 shows..." not "Table 3 showed..."

## Common Pitfalls

### The Illusion of Transparency

You have spent months on this project. The reader has 10 minutes. Things that feel obvious to you are not obvious to the reader.

- Address likely misconceptions proactively
- Provide context before introducing new concepts
- Define notation before using it

### Overclaiming

The temptation to make work sound maximally exciting is dangerous. Competent researchers see through this.

- Let the evidence speak for itself
- Clearly acknowledge limitations
- State what you show, not what you wish you showed

### Unnecessary Complexity

If readers do not understand your paper, they will not cite it.

- Use precise language, but within that constraint be as simple and possible
- You get credit for quality insights, not for sounding fancy
- A simple specification that makes the point clearly beats a complex one that obscures it

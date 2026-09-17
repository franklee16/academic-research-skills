# Empirical Asset Pricing Writing Style

**Source Papers:** Cohen & Frazzini (2008), Cohen & Lou (2012), and related top-tier empirical asset pricing papers.
**Typical Journals:** Journal of Finance, Journal of Financial Economics, Review of Financial Studies, Review of Financial Studies
**Field Code:** `eap`

---

## The Narrative Arc

Top EAP papers follow a classic arc: **Puzzle → Mechanism → Test → Resolution**.

### 1. The Hook (Introduction)
Do NOT start with dry methodology. Start with an observation or a gap in the literature.

- **Good:** "Firms do not exist as independent entities, but are linked..." (Start broad, then narrow)
- **Good:** Use a real-world vignette (like the Callaway/Coastcast story in Cohen & Frazzini) to humanize abstract concepts like "limited attention"
- **Bad:** "Financial economists have long wondered..." / "The literature has been interested in..."

### 2. The Mechanism (Theory/Hypothesis)
Explicitly define the economic mechanism (e.g., "Limited Attention," "Complicated Processing").
Use a concrete example to illustrate intuition BEFORE diving into math.

### 3. The Suspense (Results)
Present results in a logical sequence:
1. "Horse race" (raw returns) first
2. Risk-adjusted returns (alphas) second
3. Alternative explanations last

**Do not bury the lead.** State the magnitude early: "150 basis points per month."

### 4. The Defense (Robustness)
Anticipate referee skepticism. Dedicate a section to "Alternative Explanations" or "Robustness Checks."
Systematically dismantle counter-arguments (liquidity, industry momentum, firm characteristics).

---

## Voice of Authority

### Active vs. Passive
Use active constructions to assign credit and causality:
- **Do:** "We conjecture that...", "We exploit a novel setting..."
- **Don't:** "It is conjectured that...", "It is exploited..."

### Hedging Language
Use "suggest," "indicate," "consistent with" when discussing results.
Be definitive when stating the contribution. Avoid over-hedging (makes paper seem weak).

### Economy of Language
Every sentence serves a purpose. No fluff. If a sentence does not advance the hypothesis, provide a definition, or summarize a result — cut it.

### Transitions
Use strong transitional phrases: "Turning to," "In contrast," "To better understand," "Finally."

---

## Vocabulary Replacement Table

| Function | Use This (Authoritative) | Avoid This (Amateur) |
|----------|--------------------------|---------------------|
| Introducing the idea | posits, conjecture, exploit, novel, mechanism | think, believe, new idea, way |
| Presenting results | yields, generates, monotonically, induce, robust | gives, makes, goes up, causes, strong |
| Discussing mechanics | impound, underreaction, diffusion, constraints, salient | put in, overreaction, spread, limits, important |
| Defending the result | spurious, artifacts, driven by, controlling for, exposure | fake, caused by, with, looking at |
| Tone | objective, precise, authoritative, concise | emotional, vague, apologetic, wordy |

---

## Structural Template (Cohen & Frazzini / Cohen & Lou)

### A. Introduction
1. **The Hook:** Start broad, then narrow to the specific puzzle
2. **The Gap:** "While X theory suggests Y, we observe Z..."
3. **The Mechanism:** "We posit that [Mechanism] leads to [Prediction]."
4. **Summary of Results:** "We find that [Strategy] yields [X%] per month. This result is robust to..."
5. **The Roadmap:** "The remainder of the paper is organized as follows..."

### B. Body
- **Literature Review:** Be selective. Only cite directly relevant papers. Synthesize, don't list.
- **Data & Construction:** Meticulous. Explain source (CRSP/Compustat), sample period, variable construction.
- **Empirical Strategy:**
  - Portfolio tests: "We sort stocks into deciles based on..."
  - Regression: "We use a Fama-MacBeth cross-sectional regression approach..."
- **Results:** Do not just repeat table numbers. Interpret: "As shown in Table III, the alpha is positive and significant, supporting our hypothesis."
- **Robustness:** "One might argue that our results are driven by [Alternative X]. To test this, we do [Test Y]. The results, shown in Table IV, reject this alternative."

### C. Conclusion
Briefly summarize contribution and suggest future research. No new results.

---

## Sentence Patterns

### The "Although" Structure (for Robustness)
> "Although the customer momentum total abnormal return is roughly the same in large and small cap securities, prices tend to converge faster for large cap stocks."

Pattern: "Although [Standard Risk Factor] suggests [X], our results show [Y] even after controlling for [Z]."

### The "Hedging" Structure (for Nuance)
> "While it could certainly be that both explanations are present, in this section, we present a test that helps distinguish between the two."

Pattern: "While it could be the case that [Alternative Theory], we show that [Our Theory] is more consistent with the data because [Reason]."

---

## Table Presentation Rules

- **Table Title:** Must be fully descriptive and stand alone. Example: "Table III: Customer Momentum Strategy, Abnormal Returns 1981-2004."
- **In-text Reference:** Do not say "Look at Table 3." Summarize the table's conclusion and cite it.
- **Writing Style:** "Consistent with the customer momentum results being driven by investor inattention, varying inattention... significantly varies the returns."

---

## Checklist for EAP Style

- [ ] Introduction hooks with a puzzle or real-world vignette
- [ ] Mechanism is named and illustrated with a concrete example
- [ ] Main result magnitude stated early (basis points per month)
- [ ] Results sequence: raw returns → alphas → alternatives
- [ ] Vocabulary uses "yields," "exploits," "monotonically" (not "gives," "uses," "goes up")
- [ ] Active voice dominates
- [ ] Tables have self-contained titles
- [ ] Alternative explanations section systematically addresses counter-arguments
- [ ] No throat-clearing in introduction
- [ ] Literature review synthesizes, doesn't list

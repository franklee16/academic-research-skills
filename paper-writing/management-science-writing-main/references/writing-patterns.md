# Writing Patterns from Published MS&E Papers

This reference catalogues four reusable writing patterns distilled from published papers in top MS&E journals. Each pattern includes: when to use it, structural template, and a concrete published example.

---

## Pattern 1: The Motivating Example Opening

**Best for**: MS, MSOM, OMEGA, POM
**Purpose**: Ground an abstract model in a concrete, real-world problem from the first paragraph.

### Structure

```
Paragraph 1: The real-world setting
  - Name a specific company or industry
  - Cite a specific number or statistic
  - Describe a concrete dilemma faced by managers

Paragraph 2: Generalization
  - "This problem is not unique to [company]. Firms across [industry] face..."
  - Provide broader industry evidence

Paragraph 3: The academic gap
  - "Despite its practical importance, the academic literature has largely ignored..."
  - Cite 2-3 key references that come closest but fall short

Paragraph 4: Our approach
  - "In this paper, we develop a model that..."
  - State the main contribution in one sentence

Paragraph 5: Contributions (numbered)
  - 3-5 numbered contributions
```

### Example Template

```latex
\section{Introduction}

In 2023, Amazon spent \$12.7 billion on inbound logistics to move products 
from suppliers to its fulfillment centers, while simultaneously managing 
over 2 million active seller accounts with varying lead time reliability 
(Amazon Annual Report, 2023). Amazon's logistics managers face a persistent 
challenge: how much inventory to hold at each fulfillment center when lead 
times vary unpredictably across suppliers?

This challenge extends far beyond Amazon. A 2024 survey by the Council of 
Supply Chain Management Professionals found that 73\% of retailers cite 
supplier lead time variability as their top inventory management challenge, 
with poor lead time performance causing an estimated \$1.2 trillion in excess 
inventory globally (CSCMP, 2024).

Despite the practical importance of managing inventory under stochastic lead 
times, the academic literature has focused predominantly on demand uncertainty 
while treating lead times as deterministic or exponentially distributed...
```

---

## Pattern 2: The Gap Table

**Best for**: All journals, especially MS, OR, EJOR
**Purpose**: Visually demonstrate your contribution relative to the existing literature.

### Structure

A comparison table with:
- **Rows**: 8-12 key references
- **Columns**: 5-8 methodological dimensions with which you differentiate
- **Your row**: Marked in bold, with a ✓ in every column (because your paper does everything)

### Template

```latex
\begin{table}[htbp]
\centering
\caption{Positioning of This Paper in the Literature}
\label{tab:literature}
\footnotesize
\begin{tabular}{@{}lccccccc@{}}
\toprule
\textbf{Paper} & \textbf{Stochastic} & \textbf{Multi-} & \textbf{Capacity} & \textbf{Closed-} & \textbf{Numerical} & \textbf{Managerial} \\
               & \textbf{Demand}     & \textbf{Product} & \textbf{Constraints} & \textbf{Form} & \textbf{Study} & \textbf{Insights} \\
\midrule
Smith (2018)   & \checkmark & — & — & \checkmark & — & — \\
Jones (2019)   & \checkmark & \checkmark & — & — & \checkmark & — \\
Lee (2020)     & \checkmark & — & \checkmark & — & \checkmark & \checkmark \\
Chen (2021)    & — & \checkmark & \checkmark & \checkmark & — & — \\
\midrule
\textbf{This paper} & \textbf{\checkmark} & \textbf{\checkmark} & \textbf{\checkmark} & \textbf{\checkmark} & \textbf{\checkmark} & \textbf{\checkmark} \\
\bottomrule
\end{tabular}
\end{table}
```

### Placement
- Immediately after the literature review
- Often in the introduction (smaller version) AND in the literature review section (expanded version)
- Reference the table in text: "Table~\ref{tab:literature} positions our work relative to the existing literature."

---

## Pattern 3: The Assumption-Relaxation Ladder

**Best for**: MS, OR (primary); MSOM, POM (secondary)
**Purpose**: Demonstrate that your core insight is robust to model assumptions.

### Structure

```
§3. Base Model
  - Simplest version of the problem
  - 3-4 key assumptions that enable clean analytical results
  - Derive the main structural insight
  
§4. Extensions
  §4.1 Relaxing Assumption 1
    - What changes: [specific modification to the model]
    - What stays the same: "The structural insight from Theorem 1 is preserved..."
    - What changes: "However, the threshold level shifts from X to X'..."
  
  §4.2 Relaxing Assumption 2
    [Same structure]
  
  §4.3 Joint Relaxation (optional)
    - "When both Assumption 1 and 2 are relaxed simultaneously, ..."
```

### Narrative Pattern for Each Extension

```
"In the base model, we assumed [Assumption X] for analytical tractability. 
We now relax this assumption to examine whether our main insight is 
robust. Specifically, we now allow [new, more general condition]."

[Model reformulation]

[Analysis]

"As Proposition Y shows, the qualitative insight from Theorem 1 is preserved 
under this relaxation. Specifically, [restatement of insight]. However, 
the magnitude of the effect is attenuated: [quantitative difference from 
base model]. This suggests that managers in settings where [Assumption X 
is violated] should [adjusted recommendation]."
```

---

## Pattern 4: The Dual-Track Literature Review

**Best for**: MS, MSOM, POM — papers at the intersection of two literature streams.
**Purpose**: Organize a literature review that spans two distinct research traditions.

### Structure

```
§2. Literature Review

§2.1 [Stream A]: The Operations Perspective
  - 5-8 papers from OM/OR literature
  - Organize by modeling approach
  - End with: what Stream A has accomplished, and what it hasn't

§2.2 [Stream B]: The [Economics/Marketing/Strategy] Perspective
  - 5-8 papers from the other discipline
  - Organize by research question
  - End with: what Stream B has accomplished, and what it hasn't

§2.3 Our Positioning
  - Synthesis: "Stream A studies X but ignores Y. Stream B studies Y but ignores X."
  - Gap: "No paper studies X and Y jointly."
  - Our contribution: "We bridge these two streams by..."
  - Reference the gap table
```

---

## Pattern 5: The Result-Intuition-Proof Triplet

**Best for**: All analytical papers
**Purpose**: Make mathematical results accessible without sacrificing rigor.

### Structure

```
1. INTUITION (1-2 sentences before the formal statement)
   "Before presenting the formal result, we provide the intuition. 
   When holding costs increase, the firm has a stronger incentive to 
   reduce inventory. However, because of the fixed ordering cost, the 
   firm cannot reduce inventory continuously — it must do so in discrete 
   jumps by increasing the time between orders. This creates a tension 
   between the continuous holding cost pressure and the discrete ordering 
   frequency."

2. THEOREM (formal statement)
   \begin{theorem}[Optimal Reorder Interval]
   Under Assumptions 1-3, the optimal reorder interval T* satisfies:
   \begin{equation}
   T^* = \sqrt{\frac{2K}{h\lambda}}
   \end{equation}
   \end{theorem}

3. PROOF or PROOF SKETCH
   \begin{proof}
   The total cost per unit time is C(T) = K/T + h\lambda T/2...
   \end{proof}

4. DISCUSSION (1-2 sentences after the proof)
   "Equation (X) reveals that the optimal reorder interval scales with 
   the square root of the fixed cost-to-holding cost ratio. This implies 
   that a 4x increase in fixed ordering cost only doubles the optimal 
   interval — a useful rule of thumb for managers calibrating order 
   frequencies."
```

---

## Pattern 6: The Counterintuitive Result Highlight

**Best for**: MS, OR, MSOM — especially for papers seeking high-impact publication.
**Purpose**: Signal to reviewers and readers that your result is non-obvious.

### Structure

```
Opening signal phrase:
  "Surprisingly, we find that..."
  "Counterintuitively, our analysis reveals that..."
  "In contrast to conventional wisdom, ..."

Statement of conventional wisdom:
  "Conventional wisdom suggests that increasing product variety always 
   increases operational costs due to greater complexity."

Your counterintuitive finding:
  "However, we find that introducing modular product architecture can 
   reduce total costs by up to 18% when variety is increased from 10 to 
   50 product variants, despite the increase in variety."

Mechanism explanation:
  "The mechanism is [risk pooling / economies of scale / substitution effect]: 
   modular designs allow the firm to pool demand uncertainty at the component 
   level, which more than offsets the increased complexity at the finished 
   good level."

Boundary condition:
  "This benefit is most pronounced when demand across variants is negatively 
   correlated (enabling stronger pooling benefits) and diminishes when 
   correlation exceeds 0.6."
```

---

## Pattern Considerations

### When NOT to use each pattern

| Pattern | Don't Use When |
|---------|---------------|
| Motivating Example | Your problem is primarily theoretical with no natural industry connection |
| Gap Table | The literature is too sparse to fill a meaningful table (< 5 relevant papers) |
| Assumption-Relaxation | Your model is already complex; adding extensions would bloat the paper |
| Dual-Track Review | Your paper fits cleanly within a single literature stream |
| Result-Intuition-Proof | The result is a simple algebraic derivation that doesn't need intuition |
| Counterintuitive Highlight | Your result is expected/unsurprising — don't force it |

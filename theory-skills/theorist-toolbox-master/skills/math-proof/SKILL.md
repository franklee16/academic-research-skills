---
name: math-proof
description: Write clear, detailed mathematical proofs for academic papers. Use when
  the user asks to prove a result, derive an equation, justify a claim analytically,
  or expand a proof sketch into a full proof. Also trigger on "prove", "show analytically",
  "derive", "justify mathematically", or "write a proof".
author: Moran Koren <korenmor@bgu.ac.il> (Ben-Gurion University of the Negev)
---

> **Author:** Moran Koren, Ben-Gurion University of the Negev (korenmor@bgu.ac.il). Part of the [Theorist Toolbox](https://github.com/morankor/theorist-toolbox).


# Math proof

Write rigorous mathematical proofs suitable for peer-reviewed academic papers. Every step should be explicit enough that a reader can verify it without filling in gaps. The proof must be a complete proof, not a proof outline — each step should be carefully explained and documented.

## Trigger phrases

- `/math-proof`
- "prove this"
- "show analytically"
- "derive this result"
- "justify mathematically"
- "write a proof"
- "expand this proof"

## Core principles

### No gaps between steps

Every transition from one equation to the next must be justified. If you use the quotient rule, say so. If you substitute a definition, point to which definition. If a sign is negative, explain why. The reader should never need to work out an intermediate step on their own.

**Bad:**
$$\frac{d}{d\rho}\frac{n_G}{n_B} = \frac{2q-1}{n_B^2} > 0.$$

**Good:**
We compute $\frac{d}{d\rho}(n_G/n_B)$ using the quotient rule. First, the derivatives:
$$\frac{dn_G}{d\rho} = q, \qquad \frac{dn_B}{d\rho} = 1-q.$$
Applying the quotient rule:
$$\frac{d}{d\rho}\frac{n_G}{n_B} = \frac{q \cdot n_B - (1-q) \cdot n_G}{n_B^2}.$$
Expanding the numerator:
$$q[\rho + (1-\rho)q] - (1-q)[\rho + (1-\rho)(1-q)] = \rho(2q-1) + (1-\rho)(2q-1) = 2q-1.$$
Since $q > 1/2$, this is positive.

### State what you want to show before showing it

Open each step with a sentence explaining the goal: "We want to show that $t$ decreases with $\rho$." Then deliver the proof. The reader should know where you are headed before wading into algebra.

### Sign every term

When a derivative or expression appears, immediately state its sign and why. Do not leave sign determination as an exercise. If a quantity is negative because it is a log of a number less than 1, say so explicitly.

### Bridge definitions to usage

When you define a quantity (like a threshold $t$) and then use it in a derivative, explain the connection. Do not jump from "$Y \geq$ [some expression]" to "$t(K,\rho) =$ [formula]" without a sentence like: "Define $t(K,\rho)$ as the minimum number of yes votes required for allocation, i.e., the smallest integer $Y$ satisfying this inequality."

### Show intermediate algebra

Expand products, collect terms, cancel factors. Do not skip from a quotient rule setup to a simplified final form. Show at least one intermediate line where terms are expanded but not yet simplified.

### Explain why results are intuitive

After a formal derivation, add one sentence of economic or mathematical intuition. "The threshold drops because no votes carry less information, so fewer yes votes suffice to outweigh them." This helps the reader connect the math to the model.

### Self-contained proofs

The proof must be self-contained. Only cite well-known theorems — as a rule of thumb, a theorem must be famous enough to have a Wikipedia page or be taught in standard undergraduate courses. Do not invoke obscure or non-existent results. If you need a non-standard lemma, prove it inline.

### Prove the general case, not examples

Never prove a claim only for specific cases or small examples and then assert it holds in general. If you verify a property for $n=1,2,3$, that is evidence, not a proof. You must provide an argument that covers the full generality of the claim. If the general proof is beyond reach, state this explicitly: "We have verified this for $n \leq 5$; the general case remains open."

## Proof structure

### 1. Setup section

- Define all notation up front
- State the model primitives (distributions, parameters, decision rules)
- Write the key quantities as explicit functions of the parameters

### 2. Numbered steps

Each step should:
- **Open** with a plain-language statement of what will be shown
- **Derive** the result with full intermediate algebra
- **Sign** every derivative and explain the sign
- **Close** with boundary values or limiting cases where helpful

### 3. Connecting steps

When one step feeds into the next, say so explicitly: "Substituting the result from Step 1 into the expression for $c_K$..." Do not assume the reader tracks which results carry forward.

### 4. Edge cases and case analysis

Enumerate all cases explicitly. If you claim a result holds "for all $x > 0$", check boundary behavior at $x = 0$ and $x \to \infty$. Do not silently assume non-degeneracy. If the proof requires case splits (e.g., $n$ even vs odd, or an angle acute vs obtuse), handle every case — do not prove one case and assert "the other case is similar" unless the symmetry is genuinely obvious and you state the symmetry.

### 5. QED

End with $\square$ and optionally a one-sentence summary of the full result.

## Common patterns

### Differentiating a ratio $f/g$

Always use the quotient rule explicitly:
$$\frac{d}{dx}\frac{f}{g} = \frac{f'g - fg'}{g^2}.$$
Compute $f'$ and $g'$ separately first, then substitute.

### Signing a log

If $\beta = \log(a/b)$ and you claim $\beta < 0$, show that $a < b$ first with an explicit inequality.

### Chain rule through a CDF

When differentiating $P(Y \geq t(\rho))$ where both $t$ and the distribution parameter depend on $\rho$:
$$\frac{d}{d\rho}P(Y \geq t) = \frac{\partial P}{\partial t}\cdot\frac{dt}{d\rho} + \frac{\partial P}{\partial p}\cdot\frac{dp}{d\rho}.$$
Sign each term separately, then discuss which dominates.

### Discrete vs continuous

When a threshold must be an integer but you differentiate as if it were continuous, flag this: "Treating $t$ as continuous for tractability. In practice, $t$ is an integer, so small changes in $\rho$ can cause discrete jumps in $t$."

### Inequality manipulation

When manipulating inequalities, explicitly justify every direction change. Common errors include: reversing inequality signs when multiplying by a negative quantity without noting it, flipping bounds when taking reciprocals without checking sign, and applying Jensen's inequality in the wrong direction (convex vs concave). After each inequality transformation, re-state which direction the inequality points and why.

### Induction

When using induction, state the base case, the inductive hypothesis, and the inductive step separately. In the inductive step, explicitly mark where the inductive hypothesis is applied. Do not conflate "holds for $n = k$" (hypothesis) with "holds for $n = k+1$" (what you are proving).

## Format

- Use `$$` for display equations, `$` for inline
- Use `\triangleq` for definitions, `=` for equalities
- Label equations only if referenced later
- Use `\text{}` for words inside math mode
- Separate steps with `##` headings
- Write in markdown with LaTeX math
- Do not use unicode symbols for math — use LaTeX commands

## What NOT to do

- Do not write "it is easy to see" or "it follows trivially" — if a step is truly trivial, prove it anyway; a reader or reviewer will assume you cannot explain what you cannot be bothered to write
- Do not skip sign justifications
- Do not introduce shorthand notation mid-proof without defining it (e.g., writing $b$ for $|\beta|$ without warning)
- Do not combine multiple algebraic manipulations into one line
- Do not end a step by restating the setup of the next step
- Do not use "clearly" or "obviously"
- Do not assert that one effect "dominates" another without proving it. If the comparison is ambiguous, say so. If you claim A > B, show A > B with an inequality, not with an intuitive argument about where distributions "concentrate"
- Do not claim a monotonicity direction without either a derivative computation or a discrete comparison that establishes the sign
- Distinguish between what is proved and what is conjectured. If a step relies on a plausible but unproved claim, flag it explicitly: "We conjecture that..." or "Numerical evidence suggests..."
- Do not overgeneralize from examples. Proving a statement for specific values ($n = 1, 2, 3$) does not constitute a proof for all $n$ — it is evidence at best. If you cannot prove the general case, say so
- Do not cite theorems or results that are not well-known. If a result would not be taught in a standard undergraduate course and does not have a Wikipedia article, either prove it from scratch or explicitly provide a verifiable reference. Fabricating citations is worse than having a longer proof
- Do not silently omit edge cases or degenerate configurations. If your proof assumes $x \neq 0$ or a matrix is invertible, state and justify the assumption
- If you are uncertain about a step, say so explicitly rather than producing a confident-sounding but potentially wrong argument. "We believe this holds because... but a complete proof requires..." is far better than a flawed claim presented as fact

## Workflow

1. Read the claim to be proved
2. Identify the key quantities and their dependencies on parameters
3. Plan the proof structure: what needs to be shown in what order
4. Write the Setup section with all definitions
5. Write each step with full algebra, signing every term
6. Check that no step references a result not yet established
7. Add intuition sentences after key derivations
8. Verify boundary cases, edge cases, and limiting behavior
9. Self-check: re-read the proof looking for gaps, unjustified sign claims, overgeneralizations from examples, and cited results that need verification. If the proof sketch came from the user, translate intuitions into precise statements — do not merely restate the sketch in fancier notation

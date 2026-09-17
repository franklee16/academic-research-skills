# Proof and Derivation Guide for MS&E Papers

Mathematical proofs are the engine of analytical MS&E papers. This guide covers proof structure, journal-specific standards, common proof techniques, and the critical distinction between what goes in the body and what goes in the appendix.

---

## 1. Proof Hierarchy

MS&E papers follow a structured hierarchy of mathematical statements:

```
Definition  →  Precise meaning of a concept
    ↓
Lemma  →  Technical auxiliary result, used to prove something larger
    ↓
Proposition  →  Structural property of the model (secondary result)
    ↓
Theorem  →  Main result of the paper (the headline finding)
    ↓
Corollary  →  Special case or immediate consequence of a theorem
```

### Hierarchy Usage by Journal

| Journal | Typical Proof Structure |
|---------|------------------------|
| MS | 1-2 Theorems + 2-4 Propositions + 1-3 Lemmas |
| OR | 2-3 Theorems + 3-6 Propositions + multiple Lemmas |
| MSOM | 1 Theorem + 2-3 Propositions (proofs often in appendix) |
| POM | 1 Theorem + 1-2 Propositions |
| TS/TRB | 2-3 Theorems + multiple Propositions |
| EJOR | 1-2 Theorems + 2-4 Propositions |
| IJPE/IJPR | 1 Theorem + 1-2 Propositions (often proof sketches) |
| C&IE | Minimal formal proofs; computational validation preferred |

---

## 2. Proof Placement: Body vs. Appendix

This is the most important formatting decision in an MS&E paper. The rule of thumb:

| Proof Length | Placement |
|-------------|-----------|
| < 0.5 page | Body |
| 0.5 - 1.5 pages | Body if central result; Appendix if technical |
| > 1.5 pages | Appendix (or Online Supplement) |

### Journal-Specific Rules

#### MS, OR
- Short, elegant proofs in body
- Long technical proofs in appendix
- Body must contain the **statement** of every result, even if proof is in appendix
- Provide a **proof sketch** in body for appendix-deferred proofs

#### MSOM, POM
- Most proofs in appendix (these journals prioritize empirical content)
- Body: theorem statement + intuition + proof sketch
- Appendix: full algebraic derivation

#### EJOR
- Complete proofs expected somewhere (body or appendix)
- More tolerant of long proofs in body than MS
- Appendices are considered part of the reviewed paper

#### C&IE, IJPR
- Minimal proofs in body
- If the method is heuristic/computational, convergence behavior shown numerically is sufficient
- "Proof" may be replaced by "Derivation" or "Computational Validation"

---

## 3. Proof Presentation Template

```latex
\begin{theorem}[Structural Properties of the Optimal Policy]
\label{thm:optimal_policy}
Under Assumptions~\ref{ass:linear_cost}--\ref{ass:backlogging}, the optimal 
inventory policy is a state-dependent base-stock policy with level $S_t^*$, 
where $S_t^*$ is decreasing in the holding cost $h$ and increasing in the 
backlogging penalty $\pi$.
\end{theorem}

\begin{proof}[Proof Sketch]
The proof proceeds in three steps. First, we establish that the cost-to-go 
function $V_t(\cdot)$ is convex in the inventory level (Lemma~\ref{lem:convexity}). 
Second, we characterize the first-order condition of $V_t$ to derive the 
threshold structure. Third, we apply the implicit function theorem to 
establish monotonicity of $S_t^*$ in $h$ and $\pi$. The full algebraic 
derivation is provided in Appendix~\ref{app:proof_thm1}.
\end{proof}
```

### Proof Writing Conventions

1. **Always state the result before proving it.** The reader should know what you are about to establish.

2. **Name your proof technique** in the first sentence:
   - "By induction on $n$..."
   - "We construct a coupling between process A and process B..."
   - "Assume, for contradiction, that..."
   - "By backward induction on the value function..."
   - "We apply the KKT conditions to..."

3. **Provide intuition before the formal proof**: "The intuition is that higher holding costs make the firm less willing to carry inventory, which lowers the target stock level. The proof formalizes this monotonicity."

4. **End every proof with a clear marker**: `\hfill \blacksquare` or `\hfill \square` or `\qedhere`.

5. **Number all equations within proofs**: Use `\begin{align}...\end{align}` with `\tag` or `\label` for referencing.

---

## 4. Common Proof Techniques in MS&E

### Convexity / Concavity Proofs
The most common technique. Used to establish that an optimization problem is well-behaved.

**Pattern**:
1. Show the feasible set is convex
2. Show the objective function is convex (usually by verifying the Hessian is PSD)
3. Conclude that KKT conditions are necessary and sufficient
4. Characterize the optimal solution via KKT

### Sample Path / Coupling Arguments
Used in stochastic models to compare systems without computing expectations.

**Pattern**:
1. Construct two systems on the same probability space
2. Show that system A dominates system B on every sample path
3. Conclude stochastic ordering (e.g., $\leq_{st}$, $\leq_{cx}$)

### Induction (on time horizon or problem size)
Used in dynamic programming and finite-horizon problems.

**Pattern**:
1. Base case: verify the property holds for the last period / smallest instance
2. Inductive hypothesis: assume property holds for period $t+1$
3. Inductive step: show property holds for period $t$ using the Bellman equation

### Supermodularity / Lattice Arguments
Used to establish monotone comparative statics without differentiability.

**Pattern**:
1. Show the objective function is supermodular/submodular in the relevant variables
2. Apply Topkis's theorem to establish monotonicity of the optimal solution

---

## 5. Derivations vs. Proofs

A **derivation** shows how to obtain a result through algebraic manipulation. A **proof** establishes that the result is **true** under the stated assumptions.

| | Derivation | Proof |
|---|-----------|-------|
| Purpose | "Here is how we got this expression" | "This statement is mathematically true" |
| Typical content | Algebraic steps, simplifications | Logical argument, lemma applications |
| Required rigor | Each step should be clear | Each inference must be justified |
| Common in | Algorithm development, closed-form solutions | Structural results, optimality guarantees |

Most MS&E papers need **both**: derivations to get closed-form expressions, and proofs to establish that those expressions are correct/optimal.

---

## 6. Handling Proofs in Revisions

When a reviewer identifies a gap or error in a proof:

1. **Acknowledge explicitly**: "We thank the reviewer for identifying an oversight in the proof of Theorem 1."
2. **Fix the proof completely**: A partial fix that creates new gaps is worse than acknowledging the limitation
3. **If unfixable**: Restate the result as a conjecture, provide numerical evidence, and weaken the claim
4. **Add robustness**: If a proof relies on a restrictive assumption, add a discussion of what happens if the assumption fails

---

## 7. Proof Checklist Before Submission

- [ ] Every theorem/proposition/lemma is **stated** (even if proof is in appendix)
- [ ] Every statement has a **proof or proof sketch** somewhere in the paper
- [ ] Proofs are **self-contained**: all referenced lemmas are proved or cited
- [ ] Proof technique is stated in the first sentence of each proof
- [ ] All equations within proofs are numbered and referenced correctly
- [ ] Every proof ends with a clear marker
- [ ] For appendix proofs: body contains a proof sketch or intuition
- [ ] "Proof" claims are verified: do not claim to "prove" a conjecture
- [ ] All assumptions used in each proof are explicitly referenced
- [ ] Edge cases (zero, infinity, boundary) are checked

---

## 8. Journal-Specific Proof Dos and Don'ts

### MS — Do:
- Keep body proofs short and elegant
- Provide proof sketches for complex proofs moved to appendix
- Emphasize the **intuition** behind every proof
- Use lemmas to modularize long proofs

### MS — Don't:
- Include 3-page algebraic derivations in the body
- Skip the intuition behind a proof
- Assume the reader will fill in "obvious" steps

### OR — Do:
- Provide complete, rigorous proofs
- State all technical conditions (regularity, differentiability, etc.)
- Include a section on "Preliminaries" if using specialized mathematics

### OR — Don't:
- Hand-wave over technical details
- Claim optimality without verifying constraint qualifications

### EJOR — Do:
- Provide complete proofs (in body or appendix)
- Support theoretical results with numerical validation
- Include both derivation and proof where applicable

### C&IE — Do:
- Focus on algorithmic correctness rather than formal optimality proofs
- Validate heuristics computationally (benchmark comparison, convergence plots)
- Replace "Theorem" with "Result" or "Finding" if not formally proved

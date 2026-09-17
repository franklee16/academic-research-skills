# Algorithm and Solution Method Presentation in MS&E Papers

This guide covers how to present algorithms, heuristics, and solution methods in MS&E papers — a component that distinguishes MS&E from pure theory or pure empirical fields.

---

## 1. When an Algorithm Section Is Needed

Include a dedicated algorithm/solution section when:

| Condition | Example |
|-----------|---------|
| The model cannot be solved analytically | Large-scale IP, non-convex NLP |
| You propose a new algorithm | Exact method, approximation algorithm, heuristic |
| The solution method is a contribution | Novel decomposition, custom B&B, metaheuristic |
| Readers need implementation guidance | Industry-oriented paper (IJPE, IJPR, C&IE) |

**Skip or minimize** when:
- The model has a closed-form solution (just state it)
- You use an off-the-shelf solver with no customization
- The solution method is standard (e.g., "We solve the LP using Gurobi")

---

## 2. Algorithm vs. Heuristic: Labeling Convention

| Label | Definition | Guarantee Required |
|-------|-----------|-------------------|
| **Algorithm** | Method with provable optimality or approximation bound | Yes — optimality proof or approximation ratio |
| **Heuristic** | Method with no theoretical guarantee | No — validated numerically |
| **Solution Procedure** | Multi-step approach mixing exact and heuristic | Partial |
| **Approximation Algorithm** | Method with provable worst-case ratio | Yes — ratio + tightness proof |

### Journal Sensitivity to Labeling

| Journal | Tolerance for "Algorithm" without Proof | Expectation |
|---------|---------------------------------------|-------------|
| MS, OR | None | Every "Algorithm" must have a proof |
| MSOM, POM | Low | Prefer provable methods; accept well-validated heuristics |
| EJOR | Moderate | Heuristics accepted if thoroughly tested |
| C&IE, IJPR | High | Most papers propose heuristics; numerical validation is sufficient |

---

## 3. Pseudocode Standards

### LaTeX Package

Use `algorithm2e` (preferred for EJOR, IJPE, C&IE) or `algorithmicx` (preferred for MS, OR).

```latex
\usepackage[lined,linesnumbered,ruled,vlined]{algorithm2e}
```

### Pseudocode Template

```latex
\begin{algorithm}[htbp]
\caption{Adaptive Large Neighborhood Search (ALNS)}
\label{alg:alns}
\SetKwInOut{Input}{Input}
\SetKwInOut{Output}{Output}

\Input{Instance data $\mathcal{D}$, parameters $\rho, \sigma, \tau$}
\Output{Best found solution $s^*$}

\BlankLine
Initialize solution $s \leftarrow$ \texttt{ConstructInitialSolution}($\mathcal{D}$)\;
$s^* \leftarrow s$\;
\For{$i \leftarrow 1$ \KwTo $\mathit{maxIterations}$}{
    Choose destroy operator $d \in \mathcal{D}$ and repair operator $r \in \mathcal{R}$ 
    using adaptive weights $\mathbf{w}$\;
    $s' \leftarrow r(d(s))$\;
    \If{$\texttt{Accept}(s', s, T)$}{
        $s \leftarrow s'$\;
    }
    \If{$f(s') < f(s^*)$}{
        $s^* \leftarrow s'$\;
    }
    Update weights $\mathbf{w}$ based on operator performance\;
    Update temperature $T \leftarrow \rho \cdot T$\;
}
\Return{$s^*$}\;
\end{algorithm}
```

### Pseudocode Dos and Don'ts

**DO**:
- Number every line for easy reviewer reference
- State Input and Output explicitly
- Use descriptive function names (`ConstructInitialSolution` not `Init`)
- Keep each line to one logical operation
- Use mathematical notation consistent with the model section

**DON'T**:
- Include lines of pure code (e.g., `for i in range(n):`)
- Use language-specific syntax (`list.append()`, `std::vector`)
- Skip error handling unless it's algorithmically relevant
- Omit the stopping criterion

---

## 4. Complexity Analysis

Every algorithm must report computational complexity. The level of detail depends on the journal.

### Required Components

```
✓ Worst-case time complexity: O(f(n))
✓ Space complexity: O(g(n))
✓ Key parameters: n (problem size), m (number of constraints), etc.
✓ Derivation sketch: 1-2 sentences justifying the bound
```

### Example

```latex
\textbf{Computational Complexity.} Algorithm~\ref{alg:main} has worst-case 
time complexity $O(n^2 \log n)$ and space complexity $O(n^2)$, where $n$ 
is the number of customers. The dominant operation is the distance matrix 
computation in Line~4, which requires $O(n^2)$ operations, followed by 
$O(n \log n)$ for sorting in Line~7. The algorithm performs at most $n$ 
iterations of the main loop, yielding the overall $O(n^2 \log n)$ bound.
```

### Complexity Reporting by Journal

| Journal | Time Complexity | Space Complexity | Derivation | Empirical Runtime |
|---------|----------------|-----------------|------------|-------------------|
| MS | Required | Preferred | Brief | Required |
| OR | Required | Required | Detailed | Required |
| EJOR | Required | Preferred | Brief | Required |
| C&IE | Required | Optional | Optional | Required |

---

## 5. Approximation Guarantees

If you claim your method is an approximation algorithm, you must provide:

1. **Approximation ratio**: $\alpha$ such that $f(\text{algorithm}) \leq \alpha \cdot f(\text{optimal})$ for minimization
2. **Proof of the ratio**: Complete derivation
3. **Tightness**: An example showing the bound is achievable (or a proof that it is tight)
4. **Complexity**: The running time of the approximation algorithm

### Template

```latex
\begin{theorem}[Approximation Guarantee]
Algorithm~\ref{alg:approx} is a $(2 - 1/n)$-approximation algorithm for 
Problem~$\mathcal{P}$ and runs in $O(n^3)$ time.
\end{theorem}

\begin{proof}
[Proof sketch in body; full proof in appendix]
\end{proof}

\begin{remark}
The bound is tight: consider the instance with $n$ facilities located at 
vertices of a regular simplex...
\end{remark}
```

---

## 6. Heuristic Validation

For heuristic methods without theoretical guarantees, the burden of proof shifts to computational validation:

### Required Validation Components

| Component | Description |
|-----------|-------------|
| **Benchmark comparison** | Compare against exact solutions (small instances) or best-known solutions (large instances) |
| **Optimality gap** | For small instances: % deviation from optimal |
| **Multiple instance sets** | At least 2-3 different benchmark sets |
| **Statistical testing** | Paired tests across instances |
| **Convergence analysis** | Show how solution quality improves with runtime |
| **Parameter sensitivity** | How heuristic performance varies with its own parameters |

### Heuristic Performance Table

```latex
\begin{table}[htbp]
\centering
\caption{Heuristic Performance on Standard Benchmark Instances}
\label{tab:heuristic}
\begin{tabular}{@{}lcccccc@{}}
\toprule
\textbf{Instance} & \textbf{n} & \textbf{Best Known} & \textbf{Our Heuristic} & \textbf{Gap (\%)} & \textbf{CPU (s)} & \textbf{Best Found} \\
\midrule
Set A-1  & 50  & 524.3 & 528.1 & 0.72 & 2.3  & 8/10 \\
Set A-2  & 50  & 687.2 & 689.8 & 0.38 & 2.8  & 6/10 \\
Set B-1  & 100 & 1,045.8 & 1,062.3 & 1.58 & 8.4  & 3/10 \\
Set B-2  & 100 & 1,201.4 & 1,218.9 & 1.46 & 9.1  & 4/10 \\
Set C-1  & 200 & 2,104.6 & 2,153.8 & 2.34 & 25.7 & 1/10 \\
\bottomrule
\multicolumn{7}{@{}l}{\footnotesize Gap = (Heuristic - Best Known)/Best Known $\times$ 100\%. `Best Found' = \# instances where our heuristic matched or improved the best known.} \\
\end{tabular}
\end{table}
```

---

## 7. Parameter Calibration for Heuristics

Every heuristic has parameters (population size, mutation rate, cooling rate, etc.). You must explain how you chose them.

### Calibration Methods (in order of rigor)

1. **iRace or SMAC** (automated algorithm configuration) — preferred by OR, EJOR
2. **Full factorial design** — test all combinations of parameter values on a tuning set
3. **One-at-a-time tuning** — vary one parameter, fix others; iterate
4. **Literature values** — "Following [citation], we set population size = 100"
5. **Arbitrary** — not acceptable at any top journal

### Calibration Reporting

```latex
\subsection{Parameter Calibration}

We calibrated the five parameters of ALNS ($\rho$, $\sigma$, $\tau$, $p_d$, $p_r$) 
using the iRace package~\citep{lopez2016irace} with a budget of 5,000 
evaluations. The tuning was performed on a separate set of 30 instances not 
used in the final experimental evaluation. The calibrated values are:

\begin{itemize}
    \item $\rho = 0.9975$ (cooling rate): near-1.0 values performed best, 
          suggesting slow cooling is beneficial for this problem class
    \item $\sigma = 25$ (segment size): smaller segments led to more targeted 
          search but slower convergence
    \item $\tau = 0.1$ (reaction factor): rapid weight adaptation improved 
          performance on heterogeneous instances
\end{itemize}
```

---

## 8. Solution Method Section Structure

```
§X. Solution Method

  §X.1 Problem Complexity
      - Prove NP-hardness (if applicable) or state complexity class
      - "Problem P is NP-hard, as it contains the [Knapsack / TSP / etc.] 
         as a special case when [parameter] = 0."
      - If polynomial, state the complexity bound
  
  §X.2 Exact Solution Method (if applicable)
      - Mathematical programming formulation (MIP, CP, DP)
      - Decomposition approach (Benders, column generation, Lagrangian)
      - Custom valid inequalities / cuts
      - Branching and search strategies
  
  §X.3 Heuristic / Approximation Method
      - Algorithm pseudocode
      - Complexity analysis
      - Approximation guarantee (if applicable)
      - Intuitive explanation of why it works
  
  §X.4 Implementation Details
      - Preprocessing steps
      - Warm-start strategies
      - Numerical stability considerations
      - Solver parameters (if using commercial solver)
```

---

## 9. Common Mistakes

1. **Calling a heuristic an algorithm**: If you cannot prove optimality or an approximation guarantee, it's a heuristic. Label it correctly.

2. **No complexity analysis**: Even heuristic papers should state time complexity (at least empirically).

3. **Missing stopping criterion**: "Repeat until convergence" — what is convergence? Define it: "Stop when the improvement in the best solution over the last 100 iterations is less than 0.01\%."

4. **Unreproducible pseudocode**: If a reader cannot implement your method from the pseudocode, it's insufficient. Include all parameter values and subroutines.

5. **No comparison to exact solutions**: Even for heuristic papers targeting large instances, show on small instances that the heuristic is close to optimal.

6. **Tuning on test instances**: Parameter calibration must use a separate tuning set. Tuning on test instances and reporting results is data leakage.

7. **Ignoring solver defaults**: If you changed Gurobi/CPLEX parameters from defaults, list all changes and explain why.

8. **Single run per instance**: For stochastic heuristics, report results averaged over multiple runs (minimum 10) with standard deviations.

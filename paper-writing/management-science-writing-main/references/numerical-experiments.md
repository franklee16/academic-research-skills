# Numerical Experiment Design for MS&E Papers

Numerical experiments in MS&E papers serve a different purpose than in ML papers. They are **not** the primary contribution — they **validate** and **illustrate** the analytical results. This guide covers experiment structure, parameter calibration, sensitivity analysis, and journal-specific expectations.

---

## 1. The Purpose of Numerical Experiments

In MS&E, numerical experiments serve four purposes:

| Purpose | Description | Required By |
|---------|-------------|-------------|
| **Validation** | Confirm that analytical results hold and algorithms work | All journals |
| **Illustration** | Show how the model behaves concretely | MS, MSOM, POM |
| **Comparison** | Benchmark against existing methods | All journals |
| **Insight** | Generate managerial recommendations beyond what analytics can provide | MS, MSOM, OMEGA |
| **Robustness** | Demonstrate that insights survive parameter variation | MS, OR, EJOR |

---

## 2. Standard Experiment Section Structure

```
§X. Numerical Experiments
  §X.1 Experimental Setup
      - Hardware: CPU model, RAM, OS
      - Software: Solver (Gurobi 11.0, CPLEX 22.1), language (Python 3.11)
      - Implementation details: any preprocessing, warm-start strategies
      - Random seed(s) for replicability
  
  §X.2 Parameter Settings
      - Comprehensive table of all parameter values
      - Justification for each value (from literature, industry, calibration)
      - Default/base case values highlighted
  
  §X.3 Benchmark Instances
      - Data source: real data (cite), generated (describe method), literature instances (cite)
      - Instance sizes: small (n=10-50), medium (n=50-200), large (n=200-1000)
      - Number of instances per size category (minimum 10 per category)
  
  §X.4 Main Results
      - Performance comparison tables
      - Optimality gap for heuristics: (UB-LB)/UB × 100%
      - CPU time (seconds) for each method
      - Statistical significance tests where applicable
  
  §X.5 Sensitivity Analysis
      - Vary one parameter at a time around the base case
      - Show how key metrics (objective value, solution structure) change
      - Often presented as line plots or heatmaps
  
  §X.6 Managerial Implications of Experiments (optional)
      - What the numbers mean for practice
      - Actionable recommendations derived from experimental results
```

---

## 3. Parameter Tables

The parameter table is the most important element of the experimental setup. Every journal expects it.

### Required Columns

| Column | Example | Notes |
|--------|---------|-------|
| Parameter | $h$ (holding cost) | Use the same symbol as in the model section |
| Description | Unit holding cost per period | Brief verbal description |
| Base Value | 5 | The value used in the default scenario |
| Range | {1, 3, 5, 7, 10} | Values tested in sensitivity analysis |
| Source | Industry report (2023) | Where the value comes from |

### Parameter Table Template

```latex
\begin{table}[htbp]
\centering
\caption{Parameter Settings for Numerical Experiments}
\label{tab:parameters}
\begin{tabular}{@{}lllll@{}}
\toprule
\textbf{Parameter} & \textbf{Description} & \textbf{Base Value} & \textbf{Range} & \textbf{Source} \\
\midrule
$h$    & Holding cost per unit per period   & 5    & $\{1,3,5,7,10\}$           & Industry report \\
$\pi$  & Backlogging penalty per unit       & 20   & $\{10,15,20,25,30\}$       & Calibrated \\
$K$    & Fixed ordering cost                & 100  & $\{50,100,200,500\}$       & Literature \\
$\lambda$ & Demand rate (Poisson)           & 8    & $\{2,4,8,12,16\}$          & Data-driven \\
\bottomrule
\end{tabular}
\end{table}
```

### Parameter Justification Requirements

| Journal | Required Justification Level |
|---------|------------------------------|
| MS | Full justification: each parameter must cite a literature precedent or industry calibration |
| OR | Parameter values from literature or standard test instances |
| MSOM | Parameters preferably from real data; calibration method described |
| POM | Real data preferred; literature values acceptable |
| EJOR | Literature values acceptable; sensitivity analysis compensates |
| C&IE | Parameter values from standard benchmark sets |

---

## 4. Benchmark Instances

### Types of Instances

1. **Real-world data**: Best for MSOM, POM, IJPE. Must cite the data source. Describe any preprocessing (outlier removal, aggregation).

2. **Literature instances**: Standard test problems from published papers. Common in OR, TS, TRB, C&IE. Cite the originating paper.

3. **Randomly generated**: Default for most analytical papers. Must describe:
   - Distribution of each parameter (e.g., $c_i \sim U[10, 100]$)
   - Generation algorithm
   - Number of instances: at least 10 per size category (30+ total)

4. **Hybrid**: Some parameters from data, others randomized. Increasingly common in EJOR, IJPE.

### Instance Size Requirements

| Journal | Small | Medium | Large | Extra Large |
|---------|-------|--------|-------|-------------|
| MS | ✓ | ✓ | Preferred | —
| OR | ✓ | ✓ | ✓ | Preferred for algorithmic papers |
| MSOM | ✓ | ✓ | Preferred | —
| EJOR | ✓ | ✓ | ✓ | Required for heuristic papers |
| C&IE | — | ✓ | ✓ | Required |

---

## 5. Results Presentation

### Performance Comparison Table

```latex
\begin{table}[htbp]
\centering
\caption{Performance Comparison: $n=100$, 30 instances}
\label{tab:results}
\begin{tabular}{@{}lcccc@{}}
\toprule
\textbf{Method} & \textbf{Obj. Value} & \textbf{Gap (\%)} & \textbf{CPU (s)} & \textbf{Solved (\%)} \\
\midrule
Exact (Gurobi)    & 1,245.3 & —     & 45.2  & 100 \\
Heuristic-A       & 1,267.8 & 1.81  & 2.1   & 100 \\
Heuristic-B       & 1,252.1 & 0.55  & 8.7   & 100 \\
Literature benchmark~\cite{ref} & 1,310.5 & 5.24 & 12.3 & 100 \\
\bottomrule
\multicolumn{5}{@{}l}{\footnotesize Gap = (Heuristic - Exact)/Exact $\times$ 100\%. CPU times are averages over 30 instances.} \\
\end{tabular}
\end{table}
```

### Key Metrics to Report

| Metric | When to Use |
|--------|-------------|
| **Objective value** | Always |
| **Optimality gap** | For heuristics vs. exact |
| **CPU time** | For algorithmic papers |
| **% instances solved** | For exact methods with time limits |
| **# iterations** | For iterative methods |
| **Solution quality metrics** | e.g., service level, fill rate, utilization |

### Statistical Reporting

- Report **averages** with **standard deviations** (not just means)
- For comparisons: use paired t-tests or Wilcoxon signed-rank tests
- For multiple comparisons: apply Bonferroni correction
- Report **confidence intervals** at 95% level where informative
- Indicate **statistically significant** differences with asterisks (* p<0.05, ** p<0.01, *** p<0.001)

---

## 6. Sensitivity Analysis

### One-at-a-Time (OAT) Sensitivity

The standard approach: vary one parameter while holding others at base values.

```
Parameter h (holding cost):
Base = 5, Range = {1, 3, 5, 7, 10}

Result:
h=1:  Total cost = 980,  Avg inventory = 45.2
h=3:  Total cost = 1,120, Avg inventory = 32.1
h=5:  Total cost = 1,245, Avg inventory = 25.3  ← Base
h=7:  Total cost = 1,360, Avg inventory = 20.8
h=10: Total cost = 1,520, Avg inventory = 15.4

Finding: Total cost increases and inventory decreases monotonically with h. 
The relationship is approximately linear, with each unit increase in h 
reducing average inventory by ~4.5 units.
```

### Factorial Design (for multiple parameters)

For papers investigating interaction effects between 2-3 key parameters, use a full or fractional factorial design.

### Sensitivity Analysis Requirements by Journal

| Journal | OAT | Factorial | Robustness to Distribution | Scenario Analysis |
|---------|-----|-----------|---------------------------|-------------------|
| MS | Required | Preferred | Preferred | Preferred |
| OR | Required | Preferred | Preferred | Optional |
| MSOM | Required | Required | Required | Required |
| POM | Required | Required | Required | Preferred |
| EJOR | Required | Optional | Preferred | Optional |
| C&IE | Preferred | Optional | Optional | Optional |

---

## 7. Computing and Reproducibility

### Required Disclosures

```
✓ Solver: Gurobi 11.0.1 with default settings (or list all non-default parameters)
✓ Hardware: Intel Core i9-13900K, 64GB RAM, Windows 11
✓ Language: Python 3.11.5 with gurobipy 11.0.1
✓ Time limit: 3600 seconds per instance (if applicable)
✓ Optimality tolerance: 0.01% (Gurobi default)
✓ Random seed: numpy.random.seed(42)
✓ Code availability: [GitHub repository link] (MS requires this)
```

### MS Data Policy

Management Science requires authors to provide data, code, and materials sufficient for replication. The Data Editor may verify reproducibility.

---

## 8. Common Mistakes in Numerical Experiments

1. **Arbitrary parameter values**: "We set h=5." Why? What does 5 mean? A dollar amount? A percentage? Always provide units and justification.

2. **Too few instances**: 5 instances at n=100 is not enough. Minimum 10 per category; 30+ total.

3. **No sensitivity analysis**: Showing only base-case results. All top journals expect sensitivity analysis.

4. **Missing statistical tests**: Comparing methods by raw numbers without testing for significance.

5. **No convergence check**: For heuristics, how do you know it converged? Show convergence plots or stopping criteria.

6. **Cherry-picked results**: Showing only the instances where your method wins. Report all instances.

7. **Ignoring computational limits**: Reporting a 0.00% optimality gap when the solver hit the time limit at 1.5% gap.

8. **No connection to analytical results**: The experiments section should explicitly reference which theorem/proposition each experiment validates. "Consistent with Proposition 2, we observe..."

9. **Managerial insights in the experiments section without connection to model**: Each insight should be linked to a specific analytical or numerical result.

10. **Unclear comparison baseline**: What is the "current practice" benchmark? Define it explicitly.

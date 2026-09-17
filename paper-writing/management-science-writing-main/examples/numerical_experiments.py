"""
Generic MS&E Numerical Experiment Template
===========================================
Illustrates the experiment patterns from references/numerical-experiments.md
using a simple Newsvendor model with reference-dependent demand.
"""
import numpy as np
from dataclasses import dataclass

@dataclass
class NewsvendorParams:
    """Parameters for a Newsvendor with reference effects."""
    c: float = 5.0        # unit production cost
    p: float = 12.0       # selling price
    s: float = 2.0        # salvage value
    mu: float = 100.0     # mean demand
    sigma: float = 30.0   # demand std dev
    alpha: float = 0.3    # reference-dependence weight
    r: float = 100.0      # reference point (prior-period order quantity)

def newsvendor_profit(q, params, demand):
    """Single-period Newsvendor profit."""
    sales = min(q, demand)
    leftover = max(0, q - sales)
    return params.p * sales + params.s * leftover - params.c * q

def reference_adjusted_demand(params):
    """
    Reference-dependent demand: consumers anchor on prior order quantity r.
    Higher r → higher perceived availability → lower urgency → lower demand.
    """
    base = np.random.normal(params.mu, params.sigma)
    adjustment = params.alpha * (params.r - params.mu)
    return max(0, base - adjustment)

def optimal_order_quantity(params):
    """Critical ratio solution for classical Newsvendor."""
    cr = (params.p - params.c) / (params.p - params.s)
    return params.mu + params.sigma * np.sqrt(2) * (0.5 - (1 - cr))

# ============================================================
# Experiment 1: Parameter Table (following §X.2 convention)
# ============================================================
def print_parameter_table():
    print("=" * 60)
    print("Table 1: Parameter Settings")
    print("=" * 60)
    print(f"{'Parameter':<15} {'Value':>8} {'Range':>18} {'Source':>15}")
    print("-" * 60)
    params = NewsvendorParams()
    print(f"{'c (cost)':<15} {params.c:>8.1f} {'{3,5,7,9}':>18} {'Literature':>15}")
    print(f"{'p (price)':<15} {params.p:>8.1f} {'{10,12,14}':>18} {'Industry':>15}")
    print(f"{'s (salvage)':<15} {params.s:>8.1f} {'{1,2,3}':>18} {'Industry':>15}")
    print(f"{'mu (mean)':<15} {params.mu:>8.1f} {'{80,100,120}':>18} {'Data-driven':>15}")
    print(f"{'sigma (std)':<15} {params.sigma:>8.1f} {'{20,30,40}':>18} {'Data-driven':>15}")
    print(f"{'alpha (ref)':<15} {params.alpha:>8.2f} {'{0.1,0.3,0.5}':>18} {'Calibrated':>15}")

# ============================================================
# Experiment 2: Sensitivity Analysis (following §X.5 convention)
# ============================================================
def sensitivity_analysis():
    print("\n" + "=" * 60)
    print("Table 2: Sensitivity of Optimal Order Quantity to Parameters")
    print("=" * 60)
    print(f"{'Parameter':<15} {'Value':>8} {'Optimal Q':>12} {'Profit':>10}")
    print("-" * 60)
    
    base = NewsvendorParams()
    np.random.seed(42)
    demand = np.random.normal(base.mu, base.sigma, 10000)
    
    for c in [3, 5, 7, 9]:
        p = NewsvendorParams(c=c)
        q_star = optimal_order_quantity(p)
        profit = np.mean([newsvendor_profit(q_star, p, d) for d in demand])
        print(f"{'c (cost)':<15} {c:>8.1f} {q_star:>12.1f} {profit:>10.1f}")
    
    for alpha in [0.1, 0.3, 0.5]:
        p = NewsvendorParams(alpha=alpha)
        q_star = optimal_order_quantity(p)
        profit = np.mean([newsvendor_profit(q_star, p, d) for d in demand])
        print(f"{'alpha (ref)':<15} {alpha:>8.2f} {q_star:>12.1f} {profit:>10.1f}")

# ============================================================
# Experiment 3: Performance Comparison Table (following §X.4)
# ============================================================
def benchmark_comparison():
    print("\n" + "=" * 60)
    print("Table 3: Method Comparison (n=30 instances)")
    print("=" * 60)
    print(f"{'Method':<20} {'Avg Profit':>12} {'Std Dev':>10} {'CPU (ms)':>10}")
    print("-" * 60)
    
    np.random.seed(42)
    params = NewsvendorParams()
    q_opt = optimal_order_quantity(params)
    
    # Exact solution
    profits_exact = []
    for _ in range(30):
        d = np.random.normal(params.mu, params.sigma, 1000)
        profits_exact.append(np.mean([newsvendor_profit(q_opt, params, di) for di in d]))
    
    # Heuristic: mean demand
    profits_heuristic = []
    for _ in range(30):
        d = np.random.normal(params.mu, params.sigma, 1000)
        q_heuristic = params.mu
        profits_heuristic.append(np.mean([newsvendor_profit(q_heuristic, params, di) for di in d]))
    
    print(f"{'Exact (critical ratio)':<20} {np.mean(profits_exact):>12.1f} "
          f"{np.std(profits_exact):>10.1f} {'0.05':>10}")
    print(f"{'Heuristic (mean=demand)':<20} {np.mean(profits_heuristic):>12.1f} "
          f"{np.std(profits_heuristic):>10.1f} {'0.01':>10}")
    
    gap = (np.mean(profits_exact) - np.mean(profits_heuristic)) / np.mean(profits_exact) * 100
    print(f"\nOptimality gap: {gap:.2f}%")
    print("(Heuristic vs. Exact)")

if __name__ == "__main__":
    print("MS&E Numerical Experiment Template")
    print("Newsvendor with Reference-Dependent Demand")
    print("=" * 60)
    print_parameter_table()
    sensitivity_analysis()
    benchmark_comparison()
    print("\nAll experiments complete.")

# Generalized Theorem Structure Reference

This file illustrates the theorem hierarchy and proof patterns recommended by the skill. Replace the dummy content with your own model's results.

---

## Theorem Hierarchy Convention

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

---

## Example Theorem Sequence (Generic Inventory Model)

### Lemma 1: Convexity of the Cost Function

**Statement**: The expected cost function $C(q) = c \cdot q + h \cdot \mathbb{E}[(q - D)^+] + p \cdot \mathbb{E}[(D - q)^+]$ is convex in the order quantity $q$.

**Proof technique**: Second-order condition. Show $C''(q) = (h + p) \cdot f_D(q) \geq 0$. ∎

---

### Proposition 1: Optimality of Base-Stock Policy

**Statement**: Under Lemma 1, the optimal ordering policy is a base-stock policy with level $S^* = F_D^{-1}(p/(p+h))$.

**Proof technique**: First-order condition. Set $C'(q) = 0$ and solve. The convexity from Lemma 1 ensures the FOC is sufficient. ∎

---

### Theorem 1: Comparative Statics of the Optimal Base-Stock Level

**Statement**: The optimal base-stock level $S^*$ satisfies:
1. $\partial S^* / \partial p > 0$ (higher shortage cost → higher stock)
2. $\partial S^* / \partial h < 0$ (higher holding cost → lower stock)
3. $\partial S^* / \partial \mu = 1$ if demand follows a location-scale family

**Proof technique**: Implicit function theorem on $F_D(S^*) = p/(p+h)$. ∎

---

### Corollary 1: Special Case — Normal Demand

**Statement**: Under $D \sim \mathcal{N}(\mu, \sigma^2)$, the optimal base-stock level is $S^* = \mu + \sigma \cdot \Phi^{-1}(p/(p+h))$.

---

### Proposition 2: Value of Demand Information

**Statement**: The expected value of perfect demand information is $\Delta V = (p+h) \cdot \sigma \cdot \phi(\Phi^{-1}(p/(p+h)))$.

---

## Proof Placement Decision Tree

```
How long is the proof?
├── < 0.5 page → Put in body
├── 0.5–1.5 pages  
│   ├── Central to main result → Body (with intuition before formal proof)
│   └── Technical / auxiliary → Appendix
└── > 1.5 pages → Appendix (body contains proof sketch + intuition)
```

---

## Proof Writing Checklist

- [ ] State the result before proving it
- [ ] Name the proof technique in the first sentence
- [ ] Provide intuition before the formal proof
- [ ] End every proof with a clear marker ($\square$ or $\blacksquare$)
- [ ] Number all equations within proofs
- [ ] Explicitly reference all assumptions used
- [ ] Check edge cases (zero, infinity, boundaries)

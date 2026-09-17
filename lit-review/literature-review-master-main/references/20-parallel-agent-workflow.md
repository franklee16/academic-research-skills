# Parallel Agent Workflow

## Purpose

Some literature tasks require several agents to work in parallel. If real parallel execution is unavailable, run labelled agents sequentially in the same response and then integrate their outputs.

## Common parallel bundles

### Mode B idea validation

```text
Search Query Architect Agent
Killer Paper Agent
Corpus Triage Agent
Deep Reading Agent
Gap Hunter Agent
No-Data Viability Agent
Equilibrium Agent when game-theoretic
Integration Editor Agent
```

### Mode C project foundation

```text
Corpus Triage Agent
Deep Reading Agent
Journal Scope Agent
Gap Hunter Agent
Related Work Writer Agent
Integration Editor Agent
```

### Mode D manuscript support

```text
Related Work Writer Agent
Journal Scope Agent
Claim Extraction Agent
Evidence Gate Agent
Integration Editor Agent
```

### Mode E citation and evidence verification

```text
Claim Extraction Agent
Citation Verification Agent
Evidence Gate Agent
Numerical and Table Verification Agent
Source-Only Verification Agent when a fixed corpus is supplied
Integration Editor Agent
```

## Integration rules

1. All agents must use the same shared research contract.
2. The Integration Editor resolves conflicts explicitly.
3. If an agent's output is provisional, label it as provisional.
4. Do not merge unsupported claims into manuscript prose.
5. Do not promise background execution or future delivery.


## Mode E parallel workflow

Mode E can be decomposed into parallel specialist checks after the claim inventory is fixed.

```text
Claim Extraction Agent creates the fixed claim inventory.
Citation Verification Agent checks source existence, metadata, versions and retraction status.
Evidence Gate Agent checks whether each source supports each claim.
Numerical and Table Verification Agent checks figures, tables, simulations, units and rounding.
Source-Only Verification Agent checks traceability when a fixed corpus is used.
Integration Editor Agent merges statuses and produces manuscript fixes.
```

Do not let agents rewrite claims independently. Any rewritten claim must be re-entered into the claim inventory before final verification.


## Mode E specialist sequence

When Mode E is active, use this sequence.

```text
Claim Extraction Agent
Citation Verification Agent
Evidence Gate Agent
Numerical and Table Verification Agent
Integration Editor Agent
```

Do not let the Citation Verification Agent rewrite claims. The claim list must be fixed before evidence verification begins.

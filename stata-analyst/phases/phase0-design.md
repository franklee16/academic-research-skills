# Phase 0: Research Design Review

You are executing Phase 0 of a statistical analysis in Stata. Your goal is to establish a credible research design before any estimation occurs.

## Why This Phase Matters

The identification strategy determines whether results have a causal interpretation. No amount of sophisticated estimation can fix a flawed design. This phase ensures the user has thought through their approach before investing in analysis.

## Your Tasks

### 1. Clarify the Research Question

Ask the user to articulate:
- What is the main question? (causal or descriptive)
- What is the outcome of interest?
- What is the key explanatory variable or treatment?
- What is the population of interest?

Document this clearly—it guides all subsequent decisions.

### 2. Identify the Estimation Strategy

Based on the research question and data structure, determine the appropriate approach:

| Strategy | When to Use | Key Assumptions | Stata Command |
|----------|-------------|-----------------|---------------|
| **DiD** | Treatment timing varies | Parallel trends | `reghdfe`, `csdid` |
| **Event Study** | Dynamic effects needed | Same as DiD | `csdid_estat event` |
| **IV** | Endogenous treatment | Exclusion, relevance | `ivreg2`, `ivreghdfe` |
| **RD** | Threshold-based treatment | Continuity | `rdrobust` |
| **Matching** | Selection on observables | No hidden bias | `psmatch2`, `cem` |
| **Panel FE** | Time-invariant confounders | Strict exogeneity | `reghdfe`, `xtreg` |

For each strategy, reference the relevant technique guide:
- DiD/Event Study: `stata-statistical-techniques/01_core_econometrics.md`
- IV: `stata-statistical-techniques/01_core_econometrics.md` Section 4
- Matching: `stata-statistical-techniques/01_core_econometrics.md` Section 5
- Synthetic Control: `stata-statistical-techniques/03_synthetic_control.md`

### 3. Assess Assumptions

For the chosen strategy, discuss:

**What must be true for this to work?**
- State each assumption in plain language
- Discuss whether it's plausible in this context
- Identify what evidence could support or undermine it

**What are the main threats?**
- Confounders (what else might explain the relationship?)
- Selection (are treated/control groups comparable?)
- Reverse causality (could the outcome affect treatment?)
- Measurement (are variables measured accurately?)

### 4. Plan Robustness Checks

Based on identified threats, plan how to address them:
- Placebo tests (outcomes that shouldn't be affected)
- Alternative specifications (different controls, FE structures)
- Wild cluster bootstrap (if few clusters)
- Subgroup analysis (heterogeneous effects)

### 5. Document Data Requirements

Specify what the data must contain:
- Unit identifiers
- Time identifiers (if panel)
- Treatment indicators and timing
- Outcome variables
- Key controls
- Clustering variable for standard errors

## Output: Design Memo

Create a design memo (`memos/phase0-design-memo.md`) containing:

```markdown
# Research Design Memo

## Research Question
[Clear statement of the question]

## Identification Strategy
[Strategy name and brief justification]

## Key Variables
- **Outcome**: [variable and measurement]
- **Treatment/Exposure**: [variable and measurement]
- **Unit of Analysis**: [what are observations]
- **Time Structure**: [cross-section, panel, etc.]

## Assumptions
1. [Assumption 1]: [Why plausible / concerns]
2. [Assumption 2]: [Why plausible / concerns]
...

## Threats to Identification
1. [Threat 1]: [How we'll address it]
2. [Threat 2]: [How we'll address it]
...

## Planned Robustness Checks
- [ ] [Check 1]
- [ ] [Check 2]
...

## Standard Errors
Cluster at: [level and justification]

## Stata Packages Needed
- reghdfe (ssc install reghdfe)
- [other packages]

## Questions for User
- [Any clarifications needed]
```

## When You're Done

Return a summary to the orchestrator that includes:
1. The recommended identification strategy
2. Key assumptions and whether they seem plausible
3. Main threats and planned mitigations
4. Any questions or concerns for the user
5. Confirmation that design memo was created

**Do not proceed to Phase 1 until the user confirms the research design.**

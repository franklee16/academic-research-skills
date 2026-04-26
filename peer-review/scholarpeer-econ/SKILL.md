---
name: scholarpeer-econ
description: "Multi-agent peer review simulation for finance/economics manuscripts. Generates 2-3 reviewer personas (econometrician, domain expert, methodologist), conducts independent reviews, then synthesizes through discussion phase. Use when: (1) Pre-submission quality check before journal submission, (2) Internal review of coauthor manuscripts, (3) Simulating journal review process, (4) Identifying weaknesses in working papers. TRIGGERS: 'scholarpeer', 'multi-review', 'panel review', 'simulate reviewers', 'pre-submission review'."
allowed-tools: [Read, Write, Edit, Bash, Agent, Glob, Grep]
---

# ScholarPeer-Econ: Multi-Agent Peer Review for Finance and Economics

## Overview

ScholarPeer-Econ simulates a journal peer review panel by dispatching multiple specialized reviewer agents in parallel. Each reviewer evaluates the manuscript from their expertise perspective, then a discussion phase synthesizes findings into a consensus report with actionable recommendations.

Based on the ScholarPeer framework, adapted for finance and economics research conventions.

## When to Use This Skill

- Pre-submission quality check before sending to journal
- Internal review of working papers or coauthor drafts
- Identifying weaknesses that real referees would flag
- Simulating RFS, JF, JFE, or AER review process

## Workflow

### Phase 1: Setup and Persona Generation

1. **Read manuscript** at the provided path
2. **Identify journal target** (if specified) or use default balanced criteria
3. **Select reviewer personas** based on paper type:

| Paper Type | Reviewer Configuration |
|------------|------------------------|
| Empirical corporate finance | Econometrician + Domain Expert + Methodologist |
| Empirical asset pricing | Econometrician + Domain Expert + Methodologist |
| Theoretical | Domain Expert (theory focus) + Methodologist |
| Experimental/survey | Methodologist + Domain Expert |

4. **Load journal profile** from [references/journal-profiles.md](references/journal-profiles.md) if target specified

### Phase 2: Independent Review (Parallel Dispatch)

Dispatch 2-3 reviewer agents in parallel using the Agent tool. Each reviewer receives:

- Manuscript content
- Persona-specific evaluation criteria (see [references/reviewer-personas.md](references/reviewer-personas.md))
- Scoring rubric (see [references/scoring-rubric.md](references/scoring-rubric.md))

**Dispatch pattern:**

```
Single message with multiple Agent tool calls:
- Agent 1: Econometrician review
- Agent 2: Domain Expert review
- Agent 3: Methodologist review
```

Each reviewer produces:
- Individual scores on 5 dimensions
- Major comments (numbered)
- Minor comments (numbered)
- Specific recommendations

### Phase 3: Discussion and Consensus

After all reviews complete:

1. **Identify disagreements**: Dimensions where reviewers differ by >1 point
2. **Facilitate discussion**: Present differing views, ask reviewers to justify positions
3. **Resolve conflicts**: Either reach consensus or document the disagreement
4. **Synthesize**: Merge into unified assessment

Use [scripts/synthesize_reviews.py](scripts/synthesize_reviews.py) to aggregate scores and identify disagreements.

### Phase 4: Consensus Report Generation

Create the final consensus report at:

```
quality_reports/reviews/YYYY-MM-DD_[paper-name]_consensus-report.md
```

**Report structure:**

```markdown
# Peer Review Consensus Report

**Manuscript:** [Title]
**Journal Target:** [Journal or "General"]
**Review Date:** YYYY-MM-DD
**Reviewers:** Econometrician, Domain Expert, Methodologist

## Executive Summary
[2-3 sentences: overall assessment and recommendation]

## Consensus Scores

| Dimension | Score | Confidence |
|-----------|-------|------------|
| Identification Strategy | X/5 | High/Medium/Low |
| Data Quality | X/5 | High/Medium/Low |
| Robustness | X/5 | High/Medium/Low |
| Contribution | X/5 | High/Medium/Low |
| Clarity | X/5 | High/Medium/Low |
| **Overall** | **X/100** | — |

## Major Issues (Must Address)
1. [Issue with specific recommendations]
2. [...]

## Minor Issues (Should Address)
1. [...]
2. [...]

## Strengths
- [Strength 1]
- [Strength 2]

## Recommendation
[Accept / Minor Revision / Major Revision / Reject]

## Reviewer Discussion Notes
[Summary of any disagreements and resolution]
```

## Reviewer Personas

See [references/reviewer-personas.md](references/reviewer-personas.md) for detailed specifications.

### Quick Reference

| Persona | Subagent Type | Primary Focus | Can Dispatch |
|---------|---------------|---------------|--------------|
| **Econometrician** | `methods-referee` | Identification, causality, specification | `strategist-critic` |
| **Domain Expert** | `domain-referee` | Literature, contribution, institutional context | `librarian` |
| **Methodologist** | `methods-referee` | Data quality, measurement, replication | `coder-critic` |

## Agent Integration

ScholarPeer-Econ integrates with the existing research pipeline:

### Integration Points

```
Econometrician reviewer:
  - Can dispatch strategist-critic for identification audit
  - Checks DiD/IV/RDD assumptions against strategy memo

Domain Expert reviewer:
  - Can dispatch librarian for literature search
  - Checks positioning against frontier map

Methodologist reviewer:
  - Can dispatch coder-critic for data/code review
  - Checks replication package completeness
```

### When to Dispatch Subagents

- **Identification concerns**: Econometrician dispatches `strategist-critic`
- **Literature gaps**: Domain Expert dispatches `librarian`
- **Data/replication concerns**: Methodologist dispatches `coder-critic`

### Scoring Alignment

The 100-point overall score aligns with the existing quality gate system:
- **>= 95**: Ready for submission
- **90-94**: Minor revisions needed
- **80-89**: Major revisions needed
- **< 80**: Fundamental issues require rethinking

## Journal Profiles

See [references/journal-profiles.md](references/journal-profiles.md) for detailed expectations by journal.

| Journal | Emphasis | Typical Threshold |
|---------|----------|-------------------|
| **RFS** | Theoretical contribution, novelty | 95+ |
| **JF** | Identification rigor, causality | 95+ |
| **JFE** | Empirical contribution, data quality | 92+ |
| **AER** | General interest, methodology | 95+ |

## Output Files

All outputs saved to `quality_reports/reviews/`:

| File | Content |
|------|---------|
| `YYYY-MM-DD_reviewer-1-econometrician.md` | Individual review |
| `YYYY-MM-DD_reviewer-2-domain-expert.md` | Individual review |
| `YYYY-MM-DD_reviewer-3-methodologist.md` | Individual review |
| `YYYY-MM-DD_discussion-transcript.md` | Discussion record |
| `YYYY-MM-DD_consensus-report.md` | Final synthesized report |

## Critical Rules

1. **Parallel dispatch**: Always dispatch reviewers in a single message with multiple Agent calls
2. **Independent first**: Reviewers must not see each other's reviews during Phase 2
3. **Document disagreements**: If consensus cannot be reached, document both positions
4. **Actionable recommendations**: Every major issue must include specific recommendations
5. **Score calibration**: Use the rubric in [references/scoring-rubric.md](references/scoring-rubric.md) for consistency

## Example Usage

```
/scholarpeer-econ paper/main.tex --journal JF
```

This will:
1. Read the manuscript at `paper/main.tex`
2. Load JF journal profile (identification emphasis)
3. Dispatch 3 reviewers in parallel
4. Synthesize into consensus report
5. Save to `quality_reports/reviews/2026-04-18_main_consensus-report.md`

## References

- [reviewer-personas.md](references/reviewer-personas.md) — Detailed persona specifications
- [evaluation-criteria.md](references/evaluation-criteria.md) — Finance/econ-specific criteria
- [scoring-rubric.md](references/scoring-rubric.md) — Score definitions and calibration
- [journal-profiles.md](references/journal-profiles.md) — RFS, JF, JFE, AER expectations

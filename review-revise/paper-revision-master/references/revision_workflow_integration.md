# Revision Workflow Integration

This document explains how this paper-revision skill integrates with the existing revision-protocol.md and multi-agent system.

---

## Two Complementary Systems

### This Skill (paper-revision)

**Purpose:** Comprehensive end-to-end R&R workflow

**When to use:** 
- Starting a new R&R cycle from scratch
- Need systematic tracking of all comments
- Want guided workflow through all 10 steps
- First time handling R&R or want structured approach

**What it provides:**
- 10-step revision process
- Revision tracking spreadsheet
- Response letter templates
- Comment classification and routing
- Integration with LaTeX manuscript editing

### revision-protocol.md

**Purpose:** Targeted agent dispatch for specific comment types

**When to use:**
- Already have a revision plan and need to route specific comments
- Targeted re-entry (e.g., just need NEW ANALYSIS work done)
- Want agent-based quality control for specific tasks

**What it provides:**
- Agent routing rules (NEW ANALYSIS → coder, CLARIFICATION → writer)
- Worker-critic pairing system
- Three-strikes escalation protocol
- Quality scoring and thresholds

---

## Integration Points

### Same Classification System

Both systems use identical comment classifications:
- **NEW ANALYSIS** → Requires new empirical work
- **CLARIFICATION** → Text revision sufficient
- **DISAGREE** → Diplomatic pushback needed
- **MINOR** → Typos, formatting, small corrections

### When to Use Each

**Use paper-revision skill when:**
1. You receive an R&R decision and need to start from the beginning
2. You want a comprehensive tracking system for all comments
3. You prefer a guided workflow through all revision steps
4. This is your first R&R with Claude

**Use revision-protocol.md when:**
1. You've already extracted and organized comments
2. You need targeted work on specific comment types
3. You want agent-based quality control with critic reviews
4. You're doing mid-pipeline re-entry (e.g., a referee asks for additional analysis after you've already responded)

### Workflow Transitions

**From paper-revision skill to revision-protocol.md:**

After using this skill to extract and classify comments (steps 1-5), you can transition to revision-protocol.md's agent routing for execution:

```
paper-revision skill: Extract comments → Classify → Plan responses
                              ↓
revision-protocol.md: Route each classification to appropriate agent
```

**Example transition:**
- Use this skill to create revision tracker with all comments classified
- Then invoke revision-protocol.md's orchestrator to dispatch:
  - All NEW ANALYSIS comments → coder + coder-critic
  - All CLARIFICATION comments → writer + writer-critic
  - All DISAGREE comments → User review

---

## Agent Dispatch Rules

When using revision-protocol.md agent routing after planning with this skill:

| Classification | Agent Dispatched | Critic Review |
|---------------|------------------|---------------|
| NEW ANALYSIS | coder | coder-critic |
| CLARIFICATION | writer | writer-critic |
| DISAGREE | User (not an agent) | N/A |
| MINOR | writer | None (too minor) |

### Quality Gates

When using revision-protocol.md, each agent pair must achieve:
- **Score >= 80** for the component to advance
- **Score >= 95** overall for submission readiness
- **Max 3 rounds** of worker-critic iteration before escalation

---

## Recommended Workflow

### For First-Time R&R or Comprehensive Revision

1. **Invoke this skill** (`/paper-revision`) to:
   - Extract and organize all comments
   - Create revision tracker
   - Classify each comment
   - Plan responses

2. **Transition to revision-protocol.md** for execution:
   - Let orchestrator dispatch worker-critic pairs
   - Quality gates ensure high standard
   - Escalation if disagreements arise

3. **Return to this skill** for:
   - Drafting response letter
   - Final double-check
   - Re-submission preparation

### For Targeted Mid-Pipeline Work

1. **Invoke revision-protocol.md directly** to:
   - Route specific comment types to appropriate agents
   - Get quality-controlled execution
   - Handle just NEW ANALYSIS or just CLARIFICATION

2. **Skip this skill** because you already have the tracking and classification done

---

## Practical Examples

### Example 1: Comprehensive R&R (First Pass)

**Scenario:** You receive an R&R decision with 3 referee reports.

**Workflow:**
1. Use `/paper-revision` to:
   - Parse all 3 referee reports
   - Extract 25 comments total
   - Classify: 5 NEW ANALYSIS, 12 CLARIFICATION, 2 DISAGREE, 6 MINOR
   - Create revision tracker

2. Transition to revision-protocol.md:
   - Orchestrator dispatches coder for 5 NEW ANALYSIS comments
   - coder-critic reviews (score: 85/100 - pass)
   - Orchestrator dispatches writer for 12 CLARIFICATION comments
   - writer-critic reviews (score: 90/100 - pass)
   - 2 DISAGREE flagged for user review

3. Return to `/paper-revision`:
   - Draft response letter using completed tracker
   - Double-check all comments addressed
   - Final read of manuscript

### Example 2: Targeted Re-Entry (After Initial Submission)

**Scenario:** You submitted revisions, but one referee asks for additional robustness tests.

**Workflow:**
1. Skip `/paper-revision` (you already have the system set up)

2. Use revision-protocol.md directly:
   - Classify the new request as NEW ANALYSIS
   - Orchestrator dispatches coder + coder-critic
   - New robustness tests completed and reviewed
   - Writer updates manuscript section

3. Update your existing revision tracker:
   - Add the new comment
   - Mark as completed

---

## Tool Integration

### LaTeX Paper Editing

**Within this skill:**
- Read and edit .tex files directly
- Use writer agent for section revisions
- Track changes in revision tracker

**Within revision-protocol.md:**
- writer agent handles all CLARIFICATION revisions
- writer-critic ensures quality
- Integration with working-paper-format.md standards

### Excel/CSV Tracking

**This skill provides:**
- Template for revision tracking
- Structured format for comment extraction

**Manual work:**
- User fills in responses in the tracker
- Claude reads tracker to generate response letter

---

## Decision Matrix

| Your Situation | Use This Skill? | Use revision-protocol.md? |
|----------------|-----------------|--------------------------|
| First R&R ever | YES (full workflow) | AFTER this skill |
| Complex multi-referee R&R | YES (organization) | YES (quality control) |
| Single minor revision | YES (quick tracking) | NO (overkill) |
| Mid-pipeline additional analysis | NO (already organized) | YES (targeted dispatch) |
| Just need response letter template | YES (templates only) | NO |

---

## Key Principle

**This skill is the comprehensive workflow. revision-protocol.md is the targeted agent dispatcher.**

- Use this skill for **planning and organization**
- Use revision-protocol.md for **execution with quality control**
- They work together but serve different phases of the revision process

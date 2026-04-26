# Phase 3: Integration Review

## Why This Phase Matters

Revising sections individually can introduce incoherence. A strengthened theory section may now use different language than the findings. A restructured intro may no longer set up the conclusion's callbacks. This phase ensures the revised manuscript works as a whole.

## Integration Checks

### Check 1: Cluster Coherence

Do intro, theory, and conclusion share the same cluster type?

| Section | Cluster | Match? |
|---------|---------|--------|
| Introduction | [cluster] | — |
| Theory | [cluster] | ✓/✗ |
| Conclusion | [cluster] | ✓/✗ |

**If mismatch detected**:
- Usually the theory cluster is authoritative (it reflects the actual contribution)
- Intro and conclusion should be adjusted to match theory
- Use interview-bookends Phase 3 (coherence) to realign

### Check 2: Promise-Delivery Alignment

Does the intro promise what the findings deliver?

**Extract from intro**:
- What puzzle/question does intro pose?
- What is the promised contribution?
- What empirical context is set up?

**Extract from findings**:
- What does the paper actually deliver?
- What claims are actually made?
- What empirical context is actually covered?

**Common mismatches**:

| Mismatch Type | Example | Resolution |
|---------------|---------|------------|
| Scope mismatch | Intro promises general theory; findings are case-specific | Narrow intro OR broaden discussion implications |
| Emphasis mismatch | Intro emphasizes X; findings emphasize Y | Rebalance intro or add Y to intro framing |
| Missing delivery | Intro promises Z; findings never address Z | Either deliver Z or remove promise |

### Check 3: Theory → Findings Language

Do the theoretical concepts from the revised theory section appear in the findings?

**Concept inventory**:
| Concept (from theory) | Appears in Findings? | Location |
|----------------------|---------------------|----------|
| [concept 1] | Yes/No | [para/page] |
| [concept 2] | Yes/No | [para/page] |
| [concept 3] | Yes/No | [para/page] |

**If concepts missing from findings**:
- Either the findings don't actually engage the theory (substantive problem)
- Or the terminology shifted during revision (fixable with word changes)

**If findings use concepts not in theory**:
- Either theory section needs to introduce them
- Or findings should use theory's terminology instead

### Check 4: Conclusion Callbacks

Does the conclusion reference specific language/concepts from the intro?

**Callback inventory**:
| Intro Element | Callback in Conclusion? | Quote/Location |
|---------------|------------------------|----------------|
| Opening hook/puzzle | Yes/No | |
| Central question | Yes/No | |
| Key phrase | Yes/No | |
| Promise | Yes/No | |

**Interview-bookends benchmark**: 100% of strong conclusions have callbacks.

**If callbacks missing**:
- Identify 2-3 specific intro phrases that can be echoed
- Add explicit references in conclusion (not repetition, but resonance)
- Use interview-bookends Phase 3 specifically for this

### Check 5: Methods → Findings Alignment

Do the methods described support the claims made in findings?

**Check for**:
- If findings claim saturation, does methods mention saturation?
- If findings report precise counts, does methods explain counting procedure?
- If findings discuss negative cases, does methods explain how they were identified?

### Check 6: Terminology Consistency

Are key terms used consistently throughout?

**Build a terminology table**:
| Term | Definition Location | Consistent Use? | Variants Found |
|------|--------------------|-----------------| ---------------|
| [key term 1] | Theory, para X | Yes/No | [list variants] |
| [key term 2] | Theory, para Y | Yes/No | [list variants] |

**Common problems**:
- Term defined in theory, synonym used in findings
- Term used before it's defined
- Term definition shifts between sections

### Check 7: Citation Consistency

Are the same sources cited consistently?

**Check for**:
- Same author cited differently (Smith 2020 vs. Smith 2019)
- In-text citations that don't appear in references
- References that are never cited in-text

## Integration Repair Protocol

For each integration issue detected:

1. **Classify severity**:
   - **Minor**: Terminology inconsistency, missing callback (easy fix)
   - **Moderate**: Promise-delivery mismatch requiring section adjustment
   - **Major**: Cluster mismatch requiring re-revision

2. **Document the issue**:
   ```markdown
   ### Integration Issue: [Name]

   **Type**: [Cluster / Promise-Delivery / Terminology / Callback / Citation]
   **Severity**: [Minor / Moderate / Major]
   **Sections affected**: [list]

   **Description**:
   [What's inconsistent and where]

   **Proposed resolution**:
   [How to fix]

   **Action**:
   - [ ] Direct fix (can do now)
   - [ ] Requires skill re-dispatch
   - [ ] Requires user decision
   ```

3. **Make repairs**:
   - Minor issues: Fix directly
   - Moderate issues: May require skill re-dispatch (back to Phase 2)
   - Major issues: Flag for user decision

## Cross-Section Coherence Matrix

Create a summary matrix:

```markdown
## Coherence Matrix

| Check | Status | Notes |
|-------|--------|-------|
| Cluster coherence | ✓/✗ | [notes] |
| Promise-delivery | ✓/✗ | [notes] |
| Theory→Findings language | ✓/✗ | [notes] |
| Conclusion callbacks | ✓/✗ | [notes] |
| Methods→Findings | ✓/✗ | [notes] |
| Terminology | ✓/✗ | [notes] |
| Citations | ✓/✗ | [notes] |

### Issues Requiring Attention
1. [Issue 1 — severity, resolution]
2. [Issue 2 — severity, resolution]
```

## Special Case: Cascading Changes

Sometimes fixing one integration issue creates another. For example:
- Fixing promise-delivery mismatch by changing intro → breaks conclusion callbacks
- Fixing terminology in theory → requires updates in findings AND discussion

**Handle cascading changes by**:
1. Identifying the full cascade before making changes
2. Making changes in dependency order (upstream → downstream)
3. Re-checking after each change

## Output Files

Update in `revision/` directory:
- `revision-map.md` — Add integration findings section
- `integration-report.md` — Detailed coherence analysis (optional)

## When You're Done

Summarize for the orchestrator:
- Integration checks passed/failed
- Issues detected and resolved
- Any issues requiring user decision
- Recommendation: ready for Phase 4 or needs more work

**Example summary**:
> Integration review complete. 5/7 checks passed.
>
> Issues detected:
> 1. Conclusion callbacks: Missing reference to intro's "dispersal" framing — FIXED (added callback in conclusion para 2)
> 2. Terminology: "Organizational absorption" used inconsistently (sometimes "total institution") — FIXED (standardized to "organizational absorption" throughout)
>
> Remaining:
> - Cluster coherence: ✓
> - Promise-delivery: ✓ (intro now matches revised findings emphasis)
> - Theory→Findings: ✓
> - Methods→Findings: ✓
> - Citations: ✓
>
> Ready for Phase 4 verification.

Then proceed to Phase 4.

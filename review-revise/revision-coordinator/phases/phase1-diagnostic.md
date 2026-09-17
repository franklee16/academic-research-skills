# Phase 1: Diagnostic Assessment

## Why This Phase Matters

Before revising, you need to know *what kind* of revision each section needs. A section might need:
- Complete restructuring (wrong cluster/pathway)
- Targeted fixes (right structure, specific gaps)
- Calibration only (right approach, wrong execution)

This phase runs each section through its skill's diagnostic lens to determine the entry point for revision.

## Your Tasks

### Task 1: Diagnostic Protocol by Skill

For each section routed to a specialized skill, run the appropriate diagnostic:

---

#### Interview-Bookends Diagnostic (Intro/Conclusion)

**Cluster identification** — Which of the 5 clusters does this intro/conclusion match?

| Cluster | Frequency | Key Signal |
|---------|-----------|------------|
| Gap-Filler | 38.8% | Opens with puzzle/contradiction, explicit "gap" language |
| Theory-Extension | 22.5% | Opens with theoretical concept, aims to extend/refine |
| Concept-Building | 15% | Opens with phenomenon, aims to develop new concept |
| Synthesis | 17.5% | Opens with multiple literatures, aims to integrate |
| Problem-Driven | 15% | Opens with social problem, aims at practical implications |

**Benchmark check** — Does the intro/conclusion meet cluster targets?

| Metric | Target |
|--------|--------|
| Intro:Conclusion ratio | ~1.67x (intro longer) |
| Opening move | Matches cluster |
| Callbacks in conclusion | Required (100% of benchmarks have them) |
| Contribution clarity | Explicit claim |

**Issue classification**:
- **Cluster mismatch**: Intro written in Gap-Filler style but paper is Theory-Extension → restructure
- **Calibration issue**: Right cluster, wrong execution (e.g., missing callback) → targeted fix
- **Coherence issue**: Intro and conclusion don't match → Phase 3 coordination

---

#### Lit-Writeup Diagnostic (Theory Section)

**Cluster identification** — Which of the 5 clusters?

| Cluster | Frequency | Key Signal |
|---------|-----------|------------|
| Gap-Filler | 27.5% | Identifies absence in literature |
| Theory-Extender | 22.5% | Refines/extends existing theory |
| Concept-Builder | 15% | Develops new concept from phenomenon |
| Synthesis | 18.8% | Integrates multiple literatures |
| Problem-Driven | 16.3% | Addresses debate/applied problem |

**Benchmark check**:

| Metric | Target |
|--------|--------|
| Word count | 1145-1744 (median 1525) |
| Citation density | ~24 per 1000 words |
| Subsections | 2-4 typical |
| Turn clarity | Gap → contribution pivot is explicit |
| Turn position | Near end of section, not buried |

**Issue classification**:
- **Architecture issue**: Wrong number of subsections, wrong arc → Phase 1 restart
- **Turn weakness**: Gap isn't clear or contribution is vague → Phase 4 focus
- **Calibration issue**: Right structure, prose needs polish → Phase 5 only

---

#### Methods-Writer Diagnostic (Methods Section)

**Pathway identification** — Which of the 3 pathways?

| Pathway | Frequency | When Used |
|---------|-----------|-----------|
| Efficient | 10% | Simple design, space-constrained, low vulnerability |
| Standard | 61% | Typical qualitative study |
| Detailed | 23% | High vulnerability, novel methods, replication concern |

Selection criteria:
- Vulnerable population? → Detailed
- Novel/unusual methods? → Detailed
- Severe space constraints? → Efficient
- Otherwise → Standard

**Benchmark check**:

| Metric | Efficient | Standard | Detailed |
|--------|-----------|----------|----------|
| Word count | 600-900 | 1200-1500 | 2000-3000 |
| Table | Rare | Optional | Common |
| Positionality | Brief | If triggered | Extended |
| Saturation | Stated | Stated + numbers | Stated + defense |

**Issue classification**:
- **Pathway mismatch**: Using Efficient when Detailed is appropriate → redraft
- **Component gap**: Missing required element (e.g., no saturation statement) → targeted addition
- **Calibration issue**: Right pathway, word count off → trim/expand

---

#### Case-Justification Diagnostic

**Cluster identification** — Which of the 5 clusters?

| Cluster | Frequency | When Used |
|---------|-----------|-----------|
| Minimal | 16% | Familiar, single site, straightforward |
| Standard | 34% | Typical qualitative case |
| Deep Historical | 16% | Historical significance central |
| Comparative | 22% | Multiple sites |
| Policy-Driven | 13% | Policy precedent matters |

**Position check**:
- Policy-Driven cluster → BEFORE theory section
- All other clusters → AFTER theory section

**Benchmark check**:

| Cluster | Word Count | Opening Move |
|---------|------------|--------------|
| Minimal | 300-500 | Site intro → access → brief justification |
| Standard | 700-1000 | Phenomenon-site link (50%) |
| Deep Historical | 1500-2500 | Historical arc |
| Comparative | 1000-1500 | Comparison logic |
| Policy-Driven | 650-900 | Policy context |

**Issue classification**:
- **Cluster mismatch**: Wrong cluster for case type → restructure
- **Position error**: Policy-Driven placed after theory → move
- **Component gap**: Missing required element → targeted addition

---

### Task 2: Run Diagnostics for Each Section

For each section with feedback items, document:

```markdown
## Diagnostic: [Section Name]

### Skill: [skill name]

### Current State
- Word count: X
- Subsections: [list]
- Opening move: [describe]

### Cluster/Pathway Identified
[Cluster name] because [reasons]

### Benchmark Comparison
| Metric | Target | Actual | Gap |
|--------|--------|--------|-----|
| Word count | X | Y | +/- Z |
| [other metrics] | | | |

### Issues Detected
1. [Issue 1 — from feedback + diagnostic]
2. [Issue 2]

### Recommended Entry Point
- [ ] Complete restructure (Phase X of skill)
- [ ] Targeted revision (Phase Y of skill)
- [ ] Calibration only (Phase Z of skill)
- [ ] Direct revision (no skill needed)

### Notes
[Any additional observations]
```

### Task 3: Synthesize Across Sections

After running diagnostics for all sections, look for patterns:

1. **Cluster coherence**: Do intro, theory, and conclusion share the same cluster type? (They should!)
   - If intro is Gap-Filler but theory is Theory-Extender, there's a framing mismatch

2. **Severity distribution**: How many sections need restructuring vs. targeted fixes?
   - If most sections need restructuring, this is closer to a rewrite than a revision

3. **Dependency implications**: Do any diagnostics reveal new dependencies?
   - E.g., theory cluster changed → intro and conclusion need to match

### Task 4: Update the Revision Map

Add diagnostic findings to `revision-map.md`:

```markdown
---

## Phase 1 Diagnostics

### Section: Introduction
- **Cluster**: Gap-Filler
- **Key issues**: Two intros (structural), too long (calibration)
- **Entry point**: interview-bookends Phase 1 (redraft intro)

### Section: Theory
- **Cluster**: Gap-Filler (matches intro)
- **Key issues**: Repetitive with intro, turn is weak
- **Entry point**: lit-writeup Phase 5 (revision) with focus on turn

### Section: Methods
- **Pathway**: Standard (should be Detailed given vulnerability)
- **Key issues**: Missing credibility detail, pathway mismatch
- **Entry point**: methods-writer Phase 1 (redraft with Detailed pathway)

[Continue for each section...]

---

## Coherence Check

- Intro cluster: Gap-Filler ✓
- Theory cluster: Gap-Filler ✓
- Conclusion cluster: [to check after theory revised]
- Cross-cluster alignment: OK / MISMATCH

---

## Revised Sequence

Based on diagnostics:
1. Theory (Phase 5) — foundation, needs turn strengthening
2. Methods (Phase 1) — pathway change needed
3. Introduction (Phase 1) — restructure to eliminate repetition
4. [etc.]
```

## Issue Severity Classification

| Severity | Definition | Action |
|----------|------------|--------|
| **Critical** | Wrong cluster/pathway, structural misalignment | Full skill workflow |
| **Major** | Right structure, significant gaps | Targeted phases (Turn, Architecture) |
| **Minor** | Calibration issues only | Final phase or direct revision |

## Common Diagnostic Findings

### "Two Intros" Pattern
**Symptom**: Introduction and first section of lit review cover similar ground
**Diagnosis**: Usually a structural issue—no clear division between intro (puzzle + roadmap) and theory (literature engagement)
**Resolution**: Keep ONE intro; convert the other to proper theory section with lit-writeup guidance

### "Weak Turn" Pattern
**Symptom**: Feedback says gap is unclear or contribution is vague
**Diagnosis**: Turn exists but is buried, generic, or too brief
**Resolution**: lit-writeup Phase 4 focus—make turn explicit, position it correctly, sharpen language

### "Methods Credibility Gap" Pattern
**Symptom**: Feedback asks for more detail on coding, reliability, or process
**Diagnosis**: Often a pathway mismatch—using Efficient or Standard when Detailed is warranted
**Resolution**: methods-writer rediagnosis; may need pathway upgrade

### "Promise-Delivery Mismatch" Pattern
**Symptom**: Feedback says intro promises don't match findings
**Diagnosis**: Coherence issue—intro may have been written before findings were finalized
**Resolution**: Decide which is authoritative (usually findings); revise intro to match; check conclusion callbacks

## Output Files

Update in `revision/` directory:
- `revision-map.md` — add Phase 1 diagnostics section

Optionally create:
- `diagnostics/intro-diagnostic.md`
- `diagnostics/theory-diagnostic.md`
- etc.

## When You're Done

Summarize for the orchestrator:
- Diagnostic findings per section
- Entry points recommended
- Any cluster/coherence mismatches discovered
- Revised sequencing if needed

**Example summary**:
> Diagnostics complete. Theory section is Gap-Filler cluster, word count high (+200), turn needs strengthening → lit-writeup Phase 5. Methods currently Standard but should be Detailed given vulnerable population → methods-writer Phase 1 for pathway change. Introduction has two-intros problem → interview-bookends Phase 1 after theory settled. No cluster mismatches detected. Revised sequence: Theory → Methods → Intro → Conclusion.

Then pause for user confirmation before proceeding to Phase 2.

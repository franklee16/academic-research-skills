# Management Science & Engineering Academic Writing Skill

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

A comprehensive OpenCode/Claude Code/Codex skill for writing management science and operations research papers — from topic selection through modeling, derivation, numerical experiments, to a complete first draft.

Covers 13 flagship MS&E journals across two tiers: **MS, OR, MSOM, POM** (UTD-24) and **TS, TRB, DS, OMEGA, TRE, EJOR, IJPE, IJPR, C&IE**.

## What This Skill Does

This skill guides AI coding agents through the full **0-to-Draft Pipeline** for MS&E papers:

| Stage | What It Produces | Key Output |
|-------|-----------------|------------|
| **Stage 1**: Topic Positioning | Gap table, journal recommendation, contribution statement | Which journal + what's new |
| **Stage 2**: Model Building | Notation system, assumption framework, mathematical formulation | §3 Model section draft |
| **Stage 3**: Derivation & Analysis | Lemma→Theorem→Corollary proof chain, comparative statics | §4 Analysis section draft |
| **Stage 4**: Numerical Experiments | Parameter calibration, sensitivity analysis, counterfactuals | §5-6 Experiments draft |
| **Stage 5**: Writing & Assembly | Introduction, Lit Review, Managerial Insights, Abstract, formatting | Complete first draft |

The skill is **domain-specific**: it encodes the conventions, expectations, and stylistic norms of MS&E journals that generic writing skills (like `scientific-writing`) do not cover — such as model-presentation structure, proof hierarchy, managerial insight SAR framework, and journal-specific reviewer expectations.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/liyuanbo1024/management-science-writing.git
```

### 2. Install for Your AI Agent

Choose your platform below.

#### OpenCode

Copy the skill directory to your OpenCode skills folder:

```bash
# Linux/macOS
cp -r management-science-writing ~/.config/opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse management-science-writing "$env:USERPROFILE\.config\opencode\skills\"
```

Or register a custom skills path in `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.config/opencode/skills",
      "/path/to/your/cloned/management-science-writing"
    ]
  }
}
```

Then trigger with: `/management-science-writing` or just describe your task naturally ("I need to write an MSOM paper on...").

#### Claude Code (Anthropic)

```bash
# Linux/macOS
cp -r management-science-writing ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse management-science-writing "$env:USERPROFILE\.claude\skills\"
```

Claude Code auto-discovers skills in `~/.claude/skills/`. The skill activates when you mention:
- Writing for MS, OR, MSOM, POM, EJOR, or any covered journal
- MS&E modeling, proof writing, numerical experiments, managerial insights
- Any phrase matching the skill description triggers

#### Codex (OpenAI)

```bash
# Linux/macOS
cp -r management-science-writing ~/.agents/skills/

# Windows (PowerShell)
Copy-Item -Recurse management-science-writing "$env:USERPROFILE\.agents\skills\"
```

#### Cursor / Windsurf

These editors use the same skill format. Copy to your configured skills directory, typically:

```bash
# Cursor
cp -r management-science-writing ~/.cursor/skills/

# Windsurf
cp -r management-science-writing ~/.windsurf/skills/
```

#### Manual (Any Agent)

If your agent supports custom markdown-based skills, you can:

1. Point the agent's skills path to the cloned directory
2. Or directly reference `SKILL.md` in your agent's configuration
3. Or concatenate `SKILL.md` + relevant reference files into a single prompt

The skill format follows the [agentskills.io specification](https://agentskills.io/specification) with YAML frontmatter (`name` + `description` fields).

---

## How to Use

### Quick Start

Once installed, trigger the skill by describing your task naturally. The agent will detect the skill automatically. Examples:

```
"I'm writing a paper on dynamic pricing with consumer loyalty.
Help me position the contribution and choose a journal."

"My duopoly model is set up. Help me derive the MPE and prove
structural properties."

"I have all my theorems. Design numerical experiments calibrated
to industry data."

"Write the full paper draft for MSOM submission."
```

### Pipeline Mode

For a complete 0-to-draft workflow, say:

```
"Take me through the full MS&E pipeline. My topic is [describe your topic]."
```

The agent will:
1. Load the skill and assess your current stage
2. Execute Stage 1 (positioning) → get confirmation
3. Proceed to Stage 2 (modeling) → get confirmation
4. Continue through Stage 5 (full draft)
5. Output a complete LaTeX manuscript with INFORMS formatting

### Stage-Specific Mode

Jump to any stage:

| Trigger Phrase | Stage |
|---------------|-------|
| "I have a research idea about..." | Stage 1: Positioning |
| "Help me design the mathematical model" | Stage 2: Modeling |
| "I need to derive/prove..." | Stage 3: Derivation |
| "Design my numerical experiments" | Stage 4: Experiments |
| "Write the full paper" | Stage 5: Assembly |

### Reference-Only Mode

The skill also works as a passive reference. Just ask:

```
"What are MS's reviewer expectations for proof completeness?"
"How should I structure the managerial insights for an EJOR submission?"
"What's the standard notation convention for inventory models?"
```

---

## File Structure

```
management-science-writing/
├── SKILL.md                              # Main skill file (578 lines)
│   ├── Journal Selection Quick Reference
│   ├── 0-to-Draft Pipeline (5 stages)
│   ├── Rejection Reasons Checklist
│   └── Cross-References to all reference files
│
├── references/
│   ├── journal-characteristics.md        # 13 journals: detailed profiles
│   ├── modeling-conventions.md           # Notation, assumptions, model types
│   ├── proof-derivation-guide.md         # Proof hierarchy, placement, techniques
│   ├── algorithm-solving-guide.md        # Pseudocode, complexity, heuristics
│   ├── numerical-experiments.md          # Experiment design, calibration
│   ├── managerial-insights.md            # SAR framework, MI writing patterns
│   ├── reviewer-expectations.md          # What reviewers look for, rebuttal tips
│   └── writing-patterns.md               # 6 reusable writing patterns
│
├── assets/
│   └── theorem-structure-reference.md    # Generic theorem hierarchy example
│
├── examples/
│   ├── manuscript_template.tex           # INFORMS-style LaTeX template
│   └── numerical_experiments.py          # Newsvendor experiment template
│
├── README.md                             # This file
└── LICENSE                               # MIT License
```

---

## Covered Journals

### Tier 1 (UTD-24)

| Journal | Abbreviation | Focus |
|---------|-------------|-------|
| Management Science | MS | Broad management, high rigor, significant contribution |
| Operations Research | OR | Methodological depth, optimization focus |
| M&SOM | MSOM | Empirical OM, behavioral operations |
| Production & Oper. Mgmt | POM | Data-driven, broad OM scope |

### Tier 2 (Strong Field Journals)

| Journal | Focus |
|---------|-------|
| Transportation Science (TS) | Transportation systems, network models |
| Transportation Research B (TRB) | Transportation methodology |
| Decision Sciences (DS) | Decision-making, MCDM |
| OMEGA | Concise, high-impact, managerial |
| Transportation Research E (TRE) | Logistics & transportation |
| European J. Operational Research (EJOR) | Broad methodology, inclusive |
| Int. J. Production Economics (IJPE) | Production economics, supply chain |
| Int. J. Production Research (IJPR) | Production engineering |
| Computers & Industrial Eng. (C&IE) | Computational methods, IE |

---

## Customization

### Adding a Journal

Edit `references/journal-characteristics.md` and add a new section following the template:

```markdown
### Your Journal Name

**Publisher**: ...
**Focus**: ...
**Key characteristics**:
- ...
**Paper structure**: ...
**What it values most**:
1. ...
```

### Adjusting Parameter Defaults

The numerical experiments use `Parameters` dataclass defaults. Modify in `examples/numerical_experiments.py`:

```python
@dataclass
class Parameters:
    tau: float = 0.60    # Adjust to your domain
    c: float = 5.0       # Unit cost
    # ... etc
```

### Creating a New Paper Template

1. Copy `examples/manuscript.tex` as your starting point
2. Replace the title, author, and abstract
3. Fill in your model, theorems, and experiments
4. Compile with: `xelatex manuscript.tex` (two passes)

---

## Example Output

The `examples/` directory contains two reference files:

1. **`manuscript_template.tex`**: A clean INFORMS-style LaTeX template with placeholder sections following the MS&E paper structure (Model → Analysis → Experiments → Managerial Insights). Start here when writing a new paper.

2. **`numerical_experiments.py`**: A runnable Python template illustrating the numerical experiment conventions from `references/numerical-experiments.md`—parameter tables, sensitivity analysis, benchmark comparisons. Uses a simple Newsvendor model so you can run it immediately.

The `assets/` directory contains `theorem-structure-reference.md`, a generic guide to the theorem hierarchy (Lemma → Proposition → Theorem → Corollary) with proof-writing conventions.

---

## Requirements

- **AI Agent**: OpenCode, Claude Code, Codex, Cursor, Windsurf, or any agent supporting the agentskills.io format
- **For LaTeX compilation** (examples): XeLaTeX or pdfLaTeX with `amsmath`, `booktabs`, `natbib`, `geometry`, `setspace`, `enumitem`, `hyperref`, `caption`
- **For numerical experiments** (examples): Python 3.10+ with `numpy`

---

## Contributing

Contributions are welcome. Areas where help is especially valuable:

- **Journal profiles**: Detailed editorial statements and reviewer expectations for journals not yet covered
- **Writing patterns**: Additional reusable patterns distilled from published MS&E papers
- **LaTeX templates**: Official style files for specific journals
- **Calibration examples**: Numerical experiments calibrated to different industries/markets
- **Multi-language support**: Chinese/Korean/Japanese MS&E writing conventions

Please open an issue or pull request on GitHub.

---

## License

MIT License — see [LICENSE](LICENSE) file.

---

## Acknowledgments

Built using the [agentskills.io](https://agentskills.io) specification and the skill authoring methodology from [OpenCode](https://github.com/anomalyco/opencode). The MS&E domain knowledge draws on editorial statements from INFORMS journals (MS, OR, MSOM, TS) and published style guides from the operations research community.

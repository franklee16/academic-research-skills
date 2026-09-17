# FT50 Empirical Academic Writing Skill

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

A comprehensive OpenCode/Claude Code/Codex skill for writing empirical research papers targeting the Financial Times 50 (FT50) journals — from research question formulation through theory, identification, results, robustness, mechanism analysis, to a complete first draft.

Covers all 50 FT50 journals across six disciplines: **Accounting, Finance, Management, Marketing, Operations/IS, and Economics**.

## What This Skill Does

This skill guides AI coding agents through the full **0-to-Draft Pipeline** for empirical management papers:

| Stage | What It Produces | Key Output |
|-------|-----------------|------------|
| **Stage 1**: Research Question & Positioning | Gap table, journal recommendation, contribution statement | Which journal + what's new |
| **Stage 2**: Theory & Hypotheses | Theoretical framework, conceptual model, testable hypotheses | §2 Theory & Hypotheses draft |
| **Stage 3**: Identification & Research Design | Identification strategy (DID/RDD/IV/RCT/Synthetic Control), data description | §3-4 Research Design draft |
| **Stage 4**: Results & Robustness | Main results, robustness pyramid, Oster bounds, mechanism analysis | §5-6 Results & Robustness draft |
| **Stage 5**: Writing & Assembly | Introduction, Literature Review, Discussion, Implications, Abstract | Complete first draft |

The skill is **domain-specific**: it encodes the conventions, expectations, and methodological norms of FT50 empirical research that generic writing skills do not cover — such as identification strategy design, the robustness pyramid, Oster bounds for selection on unobservables, mechanism analysis frameworks, and journal-specific reviewer expectations across six management disciplines.

### Key Features

- **Identification strategies**: DID (staggered, continuous), RDD (sharp, fuzzy), IV (2SLS, Bartik, shift-share), RCT, Synthetic Control, event study
- **Robustness pyramid**: Coefficient stability plots, Oster bounds, alternative specifications, falsification tests, sample restrictions
- **Mechanism analysis**: Mediation vs. moderation, cross-sectional heterogeneity, structural estimation
- **Journal-specific guidance**: Distinct conventions for Accounting (TAR, JAE, JAR, CAR, RAST), Finance (JF, JFE, RFS, JFQA, RF), Management (AMJ, AMR, ASQ, OS, SMJ, JOM, JMS, JIBS), Marketing (MktSci, JMR, JM, JCR), Operations/IS (MS, OR, MSOM, ISR), and Economics (AER, ECMA, JPE, QJE, REStud)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/liyuanbo1024/ft50-empirical-writing.git
```

### 2. Install for Your AI Agent

Choose your platform below.

#### OpenCode

Copy the skill directory to your OpenCode skills folder:

```bash
# Linux/macOS
cp -r ft50-empirical-writing ~/.config/opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse ft50-empirical-writing "$env:USERPROFILE\.config\opencode\skills\"
```

Or register a custom skills path in `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.config/opencode/skills",
      "/path/to/your/cloned/ft50-empirical-writing"
    ]
  }
}
```

Then trigger with: `/ft50-empirical-writing` or just describe your task naturally ("I need to write a JF paper on...").

#### Claude Code (Anthropic)

```bash
# Linux/macOS
cp -r ft50-empirical-writing ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse ft50-empirical-writing "$env:USERPROFILE\.claude\skills\"
```

Claude Code auto-discovers skills in `~/.claude/skills/`. The skill activates when you mention:

- Writing for any FT50 journal (JF, JFE, AMJ, AER, etc.)
- DID, RDD, IV, RCT, Synthetic Control, event study designs
- Robustness checks, Oster bounds, mechanism analysis
- Any phrase matching the skill description triggers

#### Codex (OpenAI)

```bash
# Linux/macOS
cp -r ft50-empirical-writing ~/.agents/skills/

# Windows (PowerShell)
Copy-Item -Recurse ft50-empirical-writing "$env:USERPROFILE\.agents\skills\"
```

#### Cursor / Windsurf

These editors use the same skill format. Copy to your configured skills directory, typically:

```bash
# Cursor
cp -r ft50-empirical-writing ~/.cursor/skills/

# Windsurf
cp -r ft50-empirical-writing ~/.windsurf/skills/
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
"I'm writing a paper on the effect of minimum wage on employment
using a border-discontinuity design. Help me position the
contribution and pick a journal."

"My theory framework is ready. Help me design the identification
strategy with staggered DID and address the Bacon decomposition."

"I have my baseline results. Help me build the robustness pyramid
with Oster bounds and alternative specifications."

"Write the full paper draft for Journal of Finance."
```

### Pipeline Mode

For a complete 0-to-draft workflow, say:

```
"Take me through the full FT50 empirical pipeline. My topic is [describe your topic]."
```

The agent will:

1. Load the skill and assess your current stage
2. Execute Stage 1 (positioning) → get confirmation
3. Proceed to Stage 2 (theory) → get confirmation
4. Continue through Stage 5 (full draft)
5. Output a complete LaTeX manuscript with journal-specific formatting

### Stage-Specific Mode

Jump to any stage:

| Trigger Phrase | Stage |
|---------------|-------|
| "I have a research idea about..." | Stage 1: Positioning |
| "Help me develop the theoretical framework" | Stage 2: Theory |
| "I need to design an identification strategy" | Stage 3: Identification |
| "Analyze my results / build robustness checks" | Stage 4: Results |
| "Write the full paper" | Stage 5: Assembly |

### Reference-Only Mode

The skill also works as a passive reference. Just ask:

```
"What are JF's reviewer expectations for identification?"
"How should I implement Oster bounds for selection on unobservables?"
"What's the standard mechanism analysis framework for management journals?"
```

---

## File Structure

```
ft50-empirical-writing/
├── SKILL.md                              # Main skill file
│   ├── FT50 Journal Quick Reference
│   ├── 0-to-Draft Pipeline (5 stages)
│   ├── Identification Strategy Guide
│   ├── Robustness Pyramid Framework
│   └── Cross-References to all reference files
│
├── references/
│   ├── journal-characteristics.md        # 50 FT50 journals: detailed profiles by discipline
│   ├── identification-strategies.md      # DID, RDD, IV, RCT, Synthetic Control, event study
│   ├── theory-hypothesis-guide.md        # Theory framing, hypothesis formulation, conceptual models
│   ├── robustness-oster-guide.md         # Robustness pyramid, Oster bounds, falsification tests
│   ├── mechanism-analysis.md             # Mediation, moderation, heterogeneity, structural
│   ├── data-results-presentation.md      # Summary statistics, result tables, visualization
│   ├── reviewer-expectations.md          # What FT50 reviewers look for by discipline
│   └── writing-patterns.md               # Reusable writing patterns from published FT50 papers
│
├── assets/
│   └── regression-table-template.md      # Standard regression table conventions
│
├── examples/
│   ├── manuscript_template.tex           # Journal-style LaTeX template
│   └── empirical_analysis.py             # DID + Oster bounds analysis template
│
├── README.md                             # This file
└── LICENSE                               # MIT License
```

---

## Covered Journals

### Accounting

| Journal | Abbreviation |
|---------|-------------|
| The Accounting Review | TAR |
| Journal of Accounting and Economics | JAE |
| Journal of Accounting Research | JAR |
| Contemporary Accounting Research | CAR |
| Review of Accounting Studies | RAST |

### Finance

| Journal | Abbreviation |
|---------|-------------|
| Journal of Finance | JF |
| Journal of Financial Economics | JFE |
| Review of Financial Studies | RFS |
| Journal of Financial and Quantitative Analysis | JFQA |
| Review of Finance | RF |

### Management

| Journal | Abbreviation |
|---------|-------------|
| Academy of Management Journal | AMJ |
| Academy of Management Review | AMR |
| Administrative Science Quarterly | ASQ |
| Organization Science | OS |
| Strategic Management Journal | SMJ |
| Journal of Management | JOM |
| Journal of Management Studies | JMS |
| Journal of International Business Studies | JIBS |

### Marketing

| Journal | Abbreviation |
|---------|-------------|
| Marketing Science | MktSci |
| Journal of Marketing Research | JMR |
| Journal of Marketing | JM |
| Journal of Consumer Research | JCR |

### Operations & Information Systems

| Journal | Abbreviation |
|---------|-------------|
| Management Science | MS |
| Operations Research | OR |
| Manufacturing & Service Operations Management | MSOM |
| Information Systems Research | ISR |

### Economics

| Journal | Abbreviation |
|---------|-------------|
| American Economic Review | AER |
| Econometrica | ECMA |
| Journal of Political Economy | JPE |
| Quarterly Journal of Economics | QJE |
| Review of Economic Studies | REStud |

---

## Customization

### Adding a Journal

Edit `references/journal-characteristics.md` and add a new section following the template:

```
### Your Journal Name

**Discipline**: ...
**Publisher**: ...
**Key characteristics**:
- ...
**Identification expectations**: ...
**What it values most**:
1. ...
```

### Adjusting Empirical Defaults

The analysis template uses parameter dataclasses. Modify in `examples/empirical_analysis.py`:

```python
@dataclass
class EmpiricalConfig:
    cluster_se: str = "state"   # Cluster standard errors by
    fe_absorb: str = "firm"     # Fixed effects absorption
    oster_delta: float = 1.0    # Oster delta for bounds
    # ... etc
```

### Creating a New Paper Template

1. Copy `examples/manuscript_template.tex` as your starting point
2. Replace the title, author, and abstract
3. Fill in your theory, identification, results, and robustness
4. Compile with: `xelatex manuscript.tex` (two passes)

---

## Example Output

The `examples/` directory contains two reference files:

1. **`manuscript_template.tex`**: A clean journal-style LaTeX template with placeholder sections following the empirical paper structure (Introduction → Theory → Identification → Results → Robustness → Mechanism → Implications). Start here when writing a new paper.

2. **`empirical_analysis.py`**: A runnable Python template illustrating the empirical analysis conventions — staggered DID estimation, event study plots, Bacon decomposition, Oster bounds, and robustness checks. Uses a synthetic dataset so you can run it immediately.

The `assets/` directory contains `regression-table-template.md`, a guide to standard regression table conventions (coefficients, standard errors, significance stars, fixed effects notation, clustering).

---

## Requirements

- **AI Agent**: OpenCode, Claude Code, Codex, Cursor, Windsurf, or any agent supporting the agentskills.io format
- **For LaTeX compilation** (examples): XeLaTeX or pdfLaTeX with `amsmath`, `booktabs`, `natbib`, `geometry`, `setspace`, `enumitem`, `hyperref`, `caption`
- **For empirical analysis** (examples): Python 3.10+ with `numpy`, `pandas`, `statsmodels`, `linearmodels`

---

## Contributing

Contributions are welcome. Areas where help is especially valuable:

- **Journal profiles**: Detailed editorial statements and reviewer expectations for journals not yet covered
- **Writing patterns**: Additional reusable patterns distilled from published FT50 papers
- **LaTeX templates**: Official style files for specific journals
- **Identification examples**: Worked examples of DID, RDD, IV, RCT, Synthetic Control designs
- **Multi-language support**: Chinese/Korean/Japanese empirical writing conventions

Please open an issue or pull request on GitHub.

---

## License

MIT License — see [LICENSE](LICENSE) file.

---

## Acknowledgments

Built using the [agentskills.io](https://agentskills.io) specification and the skill authoring methodology from [OpenCode](https://github.com/anomalyco/opencode). The FT50 domain knowledge draws on editorial statements from the Financial Times Top 50 journals and published methodological guides from the empirical management research community.

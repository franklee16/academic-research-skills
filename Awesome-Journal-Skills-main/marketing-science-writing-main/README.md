# Marketing Science Academic Writing Skill

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

A comprehensive OpenCode/Claude Code/Codex skill for writing marketing science papers — from topic selection through consumer utility modeling, identification design, structural estimation, counterfactual simulations, to a complete first draft.

Covers 8 flagship marketing journals across two tiers: **Marketing Science, JMR, JM, JCR** (UTD-24) and **JAMS, IJRM, QME, Marketing Letters**.

## What This Skill Does

This skill guides AI coding agents through the full **0-to-Draft Pipeline** for marketing science papers:

| Stage | What It Produces | Key Output |
|-------|-----------------|------------|
| **Stage 1**: Topic Positioning | Gap table, journal recommendation, contribution statement | Which journal + what's new |
| **Stage 2**: Consumer Utility Model | Notation system, utility specification, demand derivation | §3 Model section draft |
| **Stage 3**: Identification & Estimation | Identification strategy (DID/RDD/IV), estimation method, specification tests | §4 Method section draft |
| **Stage 4**: Counterfactuals & Experiments | Counterfactual design, conjoint analysis, field/lab experiment design | §5-6 Results section draft |
| **Stage 5**: Writing & Assembly | Introduction, Lit Review, Marketing Implications, Abstract, formatting | Complete first draft |

The skill is **domain-specific**: it encodes the conventions, expectations, and stylistic norms of marketing journals that generic writing skills (like `scientific-writing`) do not cover — such as consumer utility model structure, identification strategy justification (DID, RDD, IV, regression discontinuity), structural estimation (BLP, GMM), conjoint analysis design, counterfactual simulation workflows, and journal-specific reviewer expectations.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/liyuanbo1024/marketing-science-writing.git
```

### 2. Install for Your AI Agent

Choose your platform below.

#### OpenCode

Copy the skill directory to your OpenCode skills folder:

```bash
# Linux/macOS
cp -r marketing-science-writing ~/.config/opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse marketing-science-writing "$env:USERPROFILE\.config\opencode\skills\"
```

Or register a custom skills path in `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.config/opencode/skills",
      "/path/to/your/cloned/marketing-science-writing"
    ]
  }
}
```

Then trigger with: `/marketing-science-writing` or just describe your task naturally ("I need to write a Marketing Science paper on...").

#### Claude Code (Anthropic)

```bash
# Linux/macOS
cp -r marketing-science-writing ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse marketing-science-writing "$env:USERPROFILE\.claude\skills\"
```

Claude Code auto-discovers skills in `~/.claude/skills/`. The skill activates when you mention:
- Writing for Marketing Science, JMR, JM, JCR, or any covered journal
- Structural modeling, causal identification, conjoint analysis, counterfactual simulations
- Any phrase matching the skill description triggers

#### Codex (OpenAI)

```bash
# Linux/macOS
cp -r marketing-science-writing ~/.agents/skills/

# Windows (PowerShell)
Copy-Item -Recurse marketing-science-writing "$env:USERPROFILE\.agents\skills\"
```

#### Cursor / Windsurf

These editors use the same skill format. Copy to your configured skills directory, typically:

```bash
# Cursor
cp -r marketing-science-writing ~/.cursor/skills/

# Windsurf
cp -r marketing-science-writing ~/.windsurf/skills/
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
"I'm writing a paper on BLP demand estimation for the smartphone market.
Help me position the contribution and choose a journal."

"My consumer utility model is set up. Help me design the identification
strategy with instrumental variables."

"I have my structural estimates. Design counterfactual simulations
for a merger analysis."

"Write the full paper draft for Marketing Science submission."
```

### Pipeline Mode

For a complete 0-to-draft workflow, say:

```
"Take me through the full marketing science pipeline. My topic is [describe your topic]."
```

The agent will:
1. Load the skill and assess your current stage
2. Execute Stage 1 (positioning) → get confirmation
3. Proceed to Stage 2 (consumer utility modeling) → get confirmation
4. Continue through Stage 5 (full draft)
5. Output a complete LaTeX manuscript with INFORMS formatting

### Stage-Specific Mode

Jump to any stage:

| Trigger Phrase | Stage |
|---------------|-------|
| "I have a research idea about..." | Stage 1: Positioning |
| "Help me design the consumer utility model" | Stage 2: Modeling |
| "I need to design the identification strategy" | Stage 3: Identification & Estimation |
| "Design my counterfactual simulations" | Stage 4: Counterfactuals & Experiments |
| "Write the full paper" | Stage 5: Assembly |

### Reference-Only Mode

The skill also works as a passive reference. Just ask:

```
"What are Marketing Science's reviewer expectations for identification?"
"How should I structure the conjoint analysis for a JMR submission?"
"What's the standard utility specification for differentiated goods markets?"
"How do I present a BLP model's micro moments?"
```

---

## File Structure

```
marketing-science-writing/
├── SKILL.md                              # Main skill file
│   ├── Journal Selection Quick Reference
│   ├── 0-to-Draft Pipeline (5 stages)
│   ├── Rejection Reasons Checklist
│   └── Cross-References to all reference files
│
├── references/
│   ├── journal-characteristics.md        # 8 journals: detailed profiles
│   ├── modeling-conventions.md           # Utility models, demand systems, choice models
│   ├── identification-guide.md           # DID, RDD, IV, structural identification
│   ├── estimation-guide.md               # BLP, GMM, MLE, Bayesian estimation
│   ├── counterfactual-guide.md           # Counterfactual simulation design
│   ├── conjoint-analysis.md              # Conjoint design, WTP estimation
│   ├── field-experiments.md              # Field experiment design and analysis
│   ├── marketing-implications.md         # Actionable marketing implications framework
│   ├── reviewer-expectations.md          # What reviewers look for, rebuttal tips
│   └── writing-patterns.md               # Reusable writing patterns
│
├── assets/
│   └── demand-model-reference.md         # Generic demand model structures
│
├── examples/
│   ├── manuscript_template.tex           # INFORMS-style LaTeX template
│   └── blp_estimation_example.py         # BLP estimation Python template
│
├── README.md                             # This file
├── README.zh-CN.md                       # Chinese
├── README.ja.md                          # Japanese
├── README.ko.md                          # Korean
└── LICENSE                               # MIT License
```

---

## Covered Journals

### Tier 1 (UTD-24)

| Journal | Abbreviation | Focus |
|---------|-------------|-------|
| Marketing Science | MktSci | Quantitative marketing, structural models, analytical rigor |
| Journal of Marketing Research | JMR | Empirical marketing, experiments, behavioral research |
| Journal of Marketing | JM | Broad marketing strategy, substantive contributions |
| Journal of Consumer Research | JCR | Consumer behavior, psychological foundations |

### Tier 2 (Strong Field Journals)

| Journal | Abbreviation | Focus |
|---------|-------------|-------|
| Journal of the Academy of Marketing Science | JAMS | Broad marketing science, conceptual and empirical |
| International Journal of Research in Marketing | IJRM | European marketing research, diverse methodologies |
| Quantitative Marketing and Economics | QME | Structural econometrics, IO approach to marketing |
| Marketing Letters | ML | Concise, sharp empirical and methodological advances |

---

## Key Methodological Pillars

This skill specifically encodes conventions for the four pillars of modern quantitative marketing:

### 1. Structural Modeling (BLP)

Consumer utility micro-foundations → aggregate demand via random coefficients logit → supply-side pricing game → BLP/GMM estimation. The skill guides you through utility specification (endogenous price, exogenous product characteristics, random coefficients), moment construction (demand-side and supply-side moments, micro moments), and the GMM objective function with optimal weighting matrix.

### 2. Causal Inference (DID / RDD / IV)

Natural experiments, quasi-experimental designs, and instrumental variable strategies for identifying causal effects in marketing. Covers difference-in-differences with staggered adoption, regression discontinuity in marketing contexts (e.g., policy thresholds, ranking cutoffs), and IV construction (Hausman instruments, BLP instruments, cost shifters).

### 3. Field Experiments

Design and analysis of randomized field experiments in marketing — digital A/B testing, offline store experiments, pricing experiments. Includes power analysis, randomization checks, treatment effect estimation with heterogeneous effects, and the connection to structural models.

### 4. Counterfactual Simulations

After estimating a structural model: predict outcomes under counterfactual scenarios (merger simulation, price discrimination ban, new product introduction, advertising cap). The skill guides you through equilibrium computation in counterfactual worlds, welfare analysis (consumer surplus, producer profit, total welfare), and connecting counterfactual results to managerial/marketing implications.

---

## 0-to-Draft Pipeline: Five-Stage Workflow

Below is the core workflow. Each stage builds on the previous. Stages 1-3 are sequential; Stages 4-5 can partially overlap. At each stage, ask the user for their current materials before proceeding.

### Stage 1: Topic Positioning & Journal Selection

**Goal**: Define the paper's contribution gap, select a target journal, and establish the writing plan.

**Agent actions**:
- Understand the substantive marketing problem
- Search for 8-12 closest papers; build a Gap Table
- Match paper profile to journal identity (Marketing Science vs. JMR vs. JCR vs. JM)
- Formulate 3-5 numbered contributions
- Outline section-by-section writing plan

**Exit criteria**: Target journal chosen, gap table drafted, contribution list written.

### Stage 2: Consumer Utility Model

**Goal**: Build the micro-founded demand model — the backbone of the paper.

**Agent actions**:
- Formalize consumer utility specification (indirect utility, random coefficients)
- Design notation system, state and defend assumptions
- Specify demand system: logit, nested logit, random coefficients logit
- Derive choice probabilities and aggregate demand
- Supply-side specification (pricing game, marginal cost structure)

**Exit criteria**: Complete model section with utility specification, notation table, and demand derivation.

### Stage 3: Identification & Estimation

**Goal**: Design the identification strategy, specify the estimator, and validate model fit.

**Agent actions**:
- Articulate the endogeneity problem (price-quality correlation)
- Design identification: instrumental variables, DID, or RDD strategy
- Construct moments (demand-side, supply-side, micro moments)
- Specify estimator (BLP/GMM, MLE, Bayesian) and optimization approach
- Plan specification tests and robustness checks

**Exit criteria**: Complete method section with identification argument and estimation details.

### Stage 4: Counterfactuals & Experiments

**Goal**: Design counterfactual simulations and/or experiments, generate results.

**Agent actions**:
- Design counterfactual scenarios with policy relevance
- Compute post-counterfactual equilibria
- Welfare analysis (consumer surplus, profits, total welfare)
- If applicable: conjoint analysis design, field experiment protocols
- Present results in structured tables and figures

**Exit criteria**: Complete counterfactual/experimental results with welfare analysis.

### Stage 5: Writing & Assembly

**Goal**: Write the full paper, assemble all sections, polish for submission.

**Agent actions**:
- Introduction: motivating example, gap, contributions, road map
- Literature review: organized by stream, explicit differentiation
- Marketing/managerial implications: actionable, traceable to results
- Conclusion: summary, limitations, future research
- Abstract (write last): problem, approach, key result
- Cross-section consistency check, formatting, citation verification

**Exit criteria**: Complete first draft, within page budget, all sections consistent.

---

## Common Rejection Reasons in Marketing Journals

| Reason | Frequency | Prevention |
|--------|-----------|------------|
| Weak identification strategy | Very High | Explicit justification of instruments or natural experiment |
| Endogeneity unaddressed | Very High | Always address price endogeneity in demand estimation |
| Insufficient contribution over existing literature | High | Explicit gap table in introduction |
| Counterfactual scenarios not policy-relevant | High | Ground counterfactuals in real marketing decisions |
| Marketing implications too generic | High | Specific, numbered, traceable to structural estimates |
| Sample / data insufficient for method | Medium | Match method complexity to data richness |
| Wrong journal fit | Medium | Use the journal selection guide above |

---

## Customization

### Adding a Journal

Edit `references/journal-characteristics.md` and add a new section following the template.

### Adjusting BLP Estimation Parameters

The estimation example uses configurable parameters. Modify in `examples/blp_estimation_example.py`.

### Creating a New Paper Template

1. Copy `examples/manuscript_template.tex` as your starting point
2. Replace the title, author, and abstract
3. Fill in your model, estimation, counterfactuals
4. Compile with: `xelatex manuscript.tex` (two passes)

---

## Requirements

- **AI Agent**: OpenCode, Claude Code, Codex, Cursor, Windsurf, or any agent supporting the agentskills.io format
- **For LaTeX compilation** (examples): XeLaTeX or pdfLaTeX with `amsmath`, `booktabs`, `natbib`, `geometry`, `setspace`, `enumitem`, `hyperref`, `caption`
- **For estimation examples**: Python 3.10+ with `numpy`, `scipy`, `pandas`

---

## Contributing

Contributions are welcome. Areas where help is especially valuable:

- **Journal profiles**: Detailed editorial statements and reviewer expectations for journals not yet covered
- **Writing patterns**: Additional reusable patterns distilled from published marketing papers
- **LaTeX templates**: Official style files for specific journals
- **Estimation examples**: Replication code for classic marketing papers (BLP, Petrin, etc.)
- **Multi-language support**: Chinese/Korean/Japanese marketing writing conventions

Please open an issue or pull request on GitHub.

---

## License

MIT License — see [LICENSE](LICENSE) file.

---

## Acknowledgments

Built using the [agentskills.io](https://agentskills.io) specification and the skill authoring methodology from [OpenCode](https://github.com/anomalyco/opencode). The marketing science domain knowledge draws on editorial statements from INFORMS (Marketing Science) and the published standards of the quantitative marketing community including BLP (1995), Berry, Levinsohn, and Pakes; Petrin (2002); and the broader structural IO-marketing literature.

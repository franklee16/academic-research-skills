# Diagrams: paper figures + generated Mermaid

Two kinds of visuals: the paper's own figures (already extracted) and Mermaid diagrams you add.

## Paper figures

`extract.py` extracts them (PDF: PyMuPDF `cluster_drawings`; arXiv: HTML scrape, images load remotely). You curate into `paper_figures`.

Pick figures by usefulness, not by quota:

- Read the surrounding paper text and inspect the image before selecting it.
- Put a figure in the section whose concept it explains. A benchmark plot belongs in Experiments, not Core Method, even if the method section needs a visual.
- **The paper's overall-architecture figure uses `anchor_section: "architecture"`.** It opens Core Method as the data-flow map. Do not put architecture or method-flow diagrams in `overview` or `motivation`; those sections should first explain the problem and the paper's move.
- Do not relabel a non-architecture plot as an architecture diagram. If the paper has no architecture figure, add a faithful Mermaid schematic or skip the visual.
- Do not include visually duplicate figures unless each adds a distinct condition, metric, or viewpoint.
- If the paper figure is dense but relevant, keep it and add a simpler Mermaid diagram nearby. If the paper figure is irrelevant to the current paragraph, do not use it there.
- Prefer no paper figure over a misleading figure.

When you rename curated figures, make the filename explain where the image belongs:

```text
{section-number}-{role}-{short-name}.png
```

Use roles such as `architecture`, `mechanism`, `result`, `ablation`, or `comparison`.

Examples:

- `03-architecture-transformer-stack.png`
- `04-mechanism-attention-scores.png`
- `06-result-bleu-vs-training-cost.png`

Shape, caption format, keep/skip rules, and `anchor_section` placement: `SKILL.md` -> `analysis.json` Contract -> Figures.

## Mermaid diagrams

Use Mermaid when a simple schematic makes the method easier to follow. A small flowchart often beats a long step-by-step paragraph.

**Generate when the paper has:**

| Pattern | Diagram |
|---|---|
| A pipeline / staged training (stage 1 → 2 → 3 → 4) | `flowchart LR` |
| A multi-component architecture with data flow (VAE encoder → MMDiT → VAE decoder) | `flowchart LR` |
| An algorithm with a conditional branch (denoise vs. decode) | `flowchart TD` |
| A producer/consumer or distributed setup | `flowchart LR` + `subgraph` |
| A parallel / tree reduction (block-wide sum, log-tree across N elements) | `graph TD` |
| Memory-hierarchy data flow (registers ↔ SMEM ↔ HBM, kernel staging) | `flowchart LR` + `subgraph` |
| A recurrence or update rule unrolled across iterations (e.g. \((m, d)\) at step S-1 → S) | `flowchart LR` |
| Backward / gradient flow across the computational graph | `flowchart RL` |
| A taxonomy of related methods | `graph TD` |

**Skip when:**
- It would need > 15 nodes (unreadable).
- You'd have to invent structure the paper doesn't state. A confident-but-wrong diagram is worse than none.

**Placement:** put diagrams inside the section they explain. Architecture and data-flow diagrams belong at the start of Core Method, before formulas and implementation details. Result plots belong in Experiments. Comparison diagrams belong in Comparison or Related Work.

**Decision rule.** Add a Mermaid diagram when the reader must track several moving parts: modules, tensors, stages, loop states, branches, or memory movement. Skip it when prose is clearer or when the diagram would invent structure the paper does not state. Mermaid may restate a dense paper figure when a simpler schematic teaches faster. Keep the paper figure too when it carries evidence, labels, axes, or visual detail Mermaid cannot reproduce.

### Markup

The inner element MUST be `<pre class="mermaid">`. `assemble.py` only un-escapes Mermaid's `-->` and `<br/>` syntax inside that tag, so a `<div>` renders broken. Wrap it in a `<figure>` for the caption:

```html
<figure class="mermaid-figure">
  <pre class="mermaid">
flowchart LR
    A[Tokens s] --> B[T5 encoder]
    B --> C["Clean embedding x"]
    C --> D{"random branch"}
    D -- denoise --> E[Noise corruption z_t]
    D -- decode --> F[Token corruption z̃]
  </pre>
  <figcaption>The ELF training step (Alg. 1): one network, two modes, branched by a coin flip.</figcaption>
</figure>
```

The caption should say what the diagram shows. `assemble.py` initializes Mermaid and `styles.css` styles `.mermaid-figure`; you only write the block.

### Templates

Adapt these to the paper; don't paste verbatim.

Multi-component architecture (most common). `classDef` + `class` highlights the main contribution in the accent color:

```
flowchart LR
    INPUT["Input (text / image)"] --> ENC["Encoder<br/>(e.g. Qwen2.5-VL)"]
    INPUT2[Image] --> VAE[VAE encoder]
    ENC --> MMDIT[MMDiT<br/>20B params]
    VAE --> MMDIT
    MMDIT --> DECODE[VAE decoder]
    DECODE --> OUTPUT[Generated image]
    classDef big fill:#fff,stroke:#b8462e,stroke-width:2px
    class MMDIT big
```

Staged training / curriculum:

```
flowchart LR
    S1["Stage 1<br/>No text"] --> S2["Stage 2<br/>Simple text"]
    S2 --> S3["Stage 3<br/>Multi-line"] --> S4["Stage 4<br/>Complex layouts"]
```

Algorithm branch:

```
flowchart TD
    START([Sample batch]) --> COND{"rand &lt; threshold?"}
    COND -- yes --> DEN[Denoising branch<br/>MSE loss]
    COND -- no --> DEC[Decoding branch<br/>CE loss]
    DEN --> COMBINE([Combined loss])
    DEC --> COMBINE
```

For producer/consumer or distributed setups, box nodes with `subgraph X[Label] … end`; for a Related-Work taxonomy use `graph TD` + `classDef ours`.

### Syntax pitfalls

Mermaid syntax is fragile. These patterns avoid common parse errors:

- **Don't nest `[...]` inside labels.** Mermaid reads `[` and `]` as node-shape delimiters. `A["state [m,d]"]` breaks; use `A["state (m,d)"]` instead. For exact notation like `[m_1, d_1]`, put it in the caption or surrounding prose as KaTeX (`\([m_1,d_1]\)`).
- **Use the pipe form for edge labels, not the quoted form.** Write `A -->|yes| B`, not `A -- "yes" --> B`. The quoted form parses fine for simple words but breaks the moment the label contains punctuation, escaped HTML entities, or comparison operators. The pipe form is the canonical Mermaid 10.x syntax and survives all of these.
- **No `<` or `>` in labels, even escaped.** Mermaid 10.x still chokes on `&lt;` inside both quoted node labels and arrow labels — the HTML decode happens before the Mermaid parser sees the text, and the bare `<` then looks like the start of an arrow. Spell comparisons in words instead: `|less than|`, `|equal|`, `|greater than|`. Same rule for `≤` / `≥`: write `|leq|` or `|at most|`. Put the exact symbol in the surrounding KaTeX prose, not in the diagram.
- **Don't quote subgraph titles.** Mermaid 10.x accepts `subgraph K` (bare id) and `subgraph K [Display Title]` (square-bracket form), but `subgraph K["Display Title"]` is a parse error. If the title needs spaces or punctuation, use the bracket form without quotes; if you need a colon or paren, drop the title and rely on a surrounding `<p>` caption.
- **Edge labels need spaces around `--`**: `A -- yes --> B`, not `A--yes-->B`. (This is for the quoted form; pipe form `A -->|yes| B` doesn't have this issue.)
- **Quote any node label containing punctuation:** `A["Encoder (Qwen2.5-VL)"]`. Bare `A[Encoder (Qwen2.5-VL)]` is fragile.
- **`<br/>` inside quoted labels** is the line break. Use as needed.
- **When in doubt, simplify aggressively.** Mermaid's error message is always the same opaque "Syntax error in text" with a version banner; it never points at the offending character. The fastest path back to a rendering diagram is to halve the node label lengths and replace every special character with a plain word.

Style preferences:

- Keep node IDs short and scannable: `A`, `ENC`, `REDUCE1`.
- For dense math or code-like notation, prefer KaTeX in prose around the diagram rather than long labels — labels work best for short conceptual names.

### Caveats

- Mermaid loads from a CDN. Offline, diagrams show raw `<pre class="mermaid">` source instead of rendering.
- If a diagram is wrong, the user can spot it but can't fix it without a re-run. When in doubt, write the relationship in prose instead.

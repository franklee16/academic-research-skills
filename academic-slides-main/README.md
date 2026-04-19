# Academic Slides

A Claude Code skill for creating publication-quality academic presentations with LaTeX/Beamer-inspired typography, theorem environments, and equation rendering — all in a single, zero-dependency HTML file.

## What This Does

**Academic Slides** helps researchers, educators, and students create professional academic presentations without wrestling with LaTeX compilation or PowerPoint formatting. It uses a "show, don't tell" approach: instead of asking you to describe aesthetic preferences in words, it generates visual theme previews and lets you pick what fits your work.

### Key Features

- **Zero Build Dependencies** — Single HTML files with inline CSS/JS. KaTeX loaded via CDN for equations.
- **Beamer-Inspired Themes** — 12 academic themes based on classic Beamer aesthetics (Madrid, Berlin, Copenhagen, Metropolis, etc.)
- **Theorem Environments** — Semantic `.theorem-box`, `.proof-box`, `.definition-box`, `.lemma-box`, `.corollary-box`, `.example-box` with proper styling and QED markers.
- **Equation Rendering** — KaTeX for inline ($...$) and display ($$...$$) mathematics.
- **Academic Typography** — Computer Modern, Latin Modern, STIX Two, EB Garamond, Source Serif — real academic fonts, not web-design fonts.
- **Progressive Disclosure** — Beamer `\pause` equivalent: reveal content step-by-step within a frame.
- **Frame Numbering** — Beamer-style header/footer bars with section titles, author, and "Frame X of Y."
- **Visual Theme Discovery** — Can't choose? Generate 3 theme previews and pick your favorite.
- **PPT Conversion** — Convert existing PowerPoint files to web presentations preserving content.
- **Production Quality** — Accessible, responsive, well-commented code.

## Installation

### For Claude Code Users

Copy the skill files to your Claude Code skills directory:

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/academic-slides

# Copy the files (or download from this repo)
cp SKILL.md ~/.claude/skills/academic-slides/
cp STYLE_PRESETS.md ~/.claude/skills/academic-slides/
```

Then use it by typing `/academic-slides` in Claude Code.

### Manual Download

1. Download `SKILL.md` and `STYLE_PRESETS.md` from this repo
2. Place them in `~/.claude/skills/academic-slides/`
3. Restart Claude Code

## Usage

### Create a New Presentation

```
/academic-slides
> "I need slides for my ICML 2026 talk on attention mechanisms"
```

The skill will:
1. Ask about your content (theorems, equations, algorithms, citations)
2. Ask about your presentation context (conference, lecture, seminar, defense)
3. Generate 3 Beamer-inspired theme previews
4. Create the full presentation with theorem environments and equation support
5. Open it in your browser

### More Examples

```
/academic-slides
> "Create lecture slides for my algorithms course on graph theory"
```

```
/academic-slides
> "Convert my research-talk.pptx to web slides with proper math rendering"
```

## Included Styles

### Classic Beamer Themes
- **Madrid** — Classic Beamer, blue header/footer bars, serif fonts
- **Berlin** — Sidebar navigation, structured sections
- **Copenhagen** — Clean minimal header, professional
- **Warsaw** — Bold gradient bars, authoritative

### Modern Academic
- **Metropolis** — Modern sans-serif, orange accent (mtheme-inspired)
- **Technical Report** — Engineering/CS style, compact, blue accent

### Traditional/Formal
- **Classic Serif** — Pure LaTeX Computer Modern look, minimal chrome
- **Cambridge** — University formal, forest green + gold
- **Thesis Defense** — Dark navy, institution-ready
- **Journal Article** — Paper-style, black + white, AMS feel

### Pedagogical
- **Lecture Notes** — Warm, approachable, large fonts
- **Seminar** — Informal, relaxed, discussion-oriented

## Output Example

Each presentation is a single, self-contained HTML file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- KaTeX for equations, Computer Modern fonts -->
</head>
<body>
    <header class="frame-header">
        <span class="short-title">Attention Mechanisms</span>
        <span class="section-title">Main Results</span>
    </header>

    <section class="frame title-frame">
        <div class="frame-content">
            <h1 class="reveal">On the Convergence of Transformer Attention</h1>
            <p class="reveal subtitle">ICML 2026</p>
            <div class="author-block reveal">
                <p class="author">Jane Smith</p>
                <p class="institute">MIT CSAIL</p>
                <p class="date">July 2026</p>
            </div>
        </div>
    </section>

    <section class="frame">
        <div class="frame-content">
            <h2 class="reveal">Main Theorem</h2>
            <div class="theorem-box reveal">
                <span class="env-title">Theorem 1 (Convergence)</span>
                <p>For attention weights $\alpha_{ij} = \text{softmax}(q_i^\top k_j / \sqrt{d})$,
                the output converges as $$\lim_{d \to \infty} \text{Attn}(Q,K,V) = V^*$$</p>
            </div>
            <div class="proof-box reveal">
                <span class="env-title">Proof sketch.</span>
                <p>By concentration of measure on the unit sphere...</p>
            </div>
        </div>
    </section>

    <footer class="frame-footer">
        <span class="author-short">J. Smith</span>
        <span class="title-short">Transformer Convergence</span>
        <span class="frame-number">7 / 23</span>
    </footer>

    <script>
        // AcademicPresentation: keyboard nav, frame counter,
        // progressive disclosure (pause), KaTeX auto-render
    </script>
</body>
</html>
```

Features included:
- Keyboard navigation (arrows, space)
- Touch/swipe support
- Frame numbering and progress bar
- KaTeX equation rendering (inline and display)
- Theorem/proof/definition environments
- Progressive disclosure (Beamer \pause equivalent)
- Responsive design with viewport fitting
- Reduced motion support
- Beamer-style header/footer bars

## Philosophy

1. **Academic rigor comes first.** Beautiful slides don't make bad research good, but sloppy formatting undermines credible work.

2. **Content over flash.** Slides support your talk, not distract from it. Clean typography and minimal animation.

3. **You don't need to be a typographer.** Beamer-inspired themes are opinionated so you can focus on theorems and equations, not CSS.

4. **Zero friction.** Single HTML file. No LaTeX compilation. Open in browser, present anywhere.

5. **Comments are kindness.** Code explains how to customize colors, fonts, and theorem styling.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill instructions for Claude Code |
| `STYLE_PRESETS.md` | Reference file with 12 curated academic themes |

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- For PPT conversion: Python with `python-pptx` library
- KaTeX loaded automatically via CDN in generated HTML

## Credits

Inspired by [frontend-slides](https://github.com/zarazhangrui/frontend-slides) by [@zarazhangrui](https://github.com/zarazhangrui).

Built on top of the Beamer LaTeX package philosophy — because academic presentations deserve proper typesetting even outside LaTeX.

## License

MIT — Use it, modify it, share it.

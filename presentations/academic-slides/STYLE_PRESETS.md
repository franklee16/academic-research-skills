# Style Presets Reference

Curated Beamer-inspired academic themes for Academic Slides. Each preset is modeled after real LaTeX/Beamer presentation themes used in mathematics, computer science, and engineering talks. **Structural chrome and theorem environments only — no decorative illustrations.**

---

## CRITICAL: Viewport Fitting (Non-Negotiable)

**Every frame MUST fit exactly in the viewport. No scrolling within frames, ever.**

### Content Density Limits Per Frame

| Frame Type | Maximum Content |
|------------|-----------------|
| Title Frame | 1 title + 1 subtitle + author/institute/date block |
| Content Frame | 1 heading + 4-5 bullet points OR 1 heading + 2 short paragraphs |
| Theorem/Proof Frame | 1 theorem box (max 4 lines) + 1 proof sketch (max 5 lines) |
| Equation Frame | 1 heading + 1-3 display equations with optional annotation |
| Algorithm Frame | 1 heading + max 12 lines of pseudocode |
| Definition Frame | 1 heading + 1-2 definition boxes (max 3 lines each) |
| Citation/References Frame | 1 heading + max 8 reference entries |
| Section Divider Frame | 1 section number + 1 section title + optional outline |

**Too much content? Split into multiple frames. Never scroll.**

### Required Base CSS (Include in ALL Presentations)

```css
/* ===========================================
   VIEWPORT FITTING: MANDATORY
   Copy this entire block into every presentation
   =========================================== */

/* 1. Lock document to viewport */
html, body {
    height: 100%;
    overflow-x: hidden;
}

html {
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}

/* 2. Each frame = exact viewport height */
.frame {
    width: 100vw;
    height: 100vh;
    height: 100dvh; /* Dynamic viewport for mobile */
    overflow: hidden; /* CRITICAL: No overflow ever */
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    position: relative;
}

/* 3. Content wrapper */
.frame-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-height: 100%;
    overflow: hidden;
    padding: var(--frame-padding);
}

/* 4. ALL sizes use clamp() - scales with viewport */
:root {
    /* Typography */
    --title-size: clamp(1.5rem, 5vw, 4rem);
    --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
    --h3-size: clamp(1rem, 2.5vw, 1.75rem);
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --small-size: clamp(0.65rem, 1vw, 0.875rem);

    /* Spacing */
    --frame-padding: clamp(1rem, 4vw, 4rem);
    --content-gap: clamp(0.5rem, 2vw, 2rem);
    --element-gap: clamp(0.25rem, 1vw, 1rem);

    /* Fonts (override per theme) */
    --font-heading: 'STIX Two Text', 'Georgia', serif;
    --font-body: 'Source Serif 4', 'Georgia', serif;
    --font-mono: 'Source Code Pro', 'Courier New', monospace;
}

/* 5. Cards/containers use viewport-relative max sizes */
.card, .container, .content-box {
    max-width: min(90vw, 1000px);
    max-height: min(80vh, 700px);
}

/* 6. Lists auto-scale with viewport */
.item-list, .enum-list {
    gap: clamp(0.4rem, 1vh, 1rem);
}

.item-list li, .enum-list li {
    font-size: var(--body-size);
    line-height: 1.4;
}

/* 7. Images constrained */
img {
    max-width: 100%;
    max-height: min(50vh, 400px);
    object-fit: contain;
}

/* ===========================================
   THEOREM ENVIRONMENTS: MANDATORY
   Academic content boxes for formal material
   =========================================== */

/* Theorem, definition, example, lemma, corollary */
.theorem-box, .definition-box, .example-box, .lemma-box, .corollary-box {
    border-left: 4px solid var(--theorem-border);
    background: var(--theorem-bg);
    padding: clamp(0.5rem, 1.5vw, 1rem) clamp(0.75rem, 2vw, 1.5rem);
    margin: clamp(0.25rem, 0.5vw, 0.5rem) 0;
    max-height: min(40vh, 350px);
    overflow: hidden;
}

/* Definition boxes use their own color when defined */
.definition-box {
    border-left-color: var(--definition-border, var(--theorem-border));
    background: var(--definition-bg, var(--theorem-bg));
}

/* Example boxes use their own color when defined */
.example-box {
    border-left-color: var(--example-border, var(--theorem-border));
    background: var(--example-bg, var(--theorem-bg));
}

/* Proof environment */
.proof-box {
    border-left: 2px solid var(--proof-border);
    background: var(--proof-bg);
    padding: clamp(0.4rem, 1vw, 0.75rem) clamp(0.75rem, 2vw, 1.5rem);
    font-style: italic;
}

.proof-box::after {
    content: '\25A1';
    float: right;
    font-style: normal;
}

/* Algorithm environment */
.algorithm-box {
    border: 1px solid var(--theorem-border);
    background: var(--proof-bg);
    padding: clamp(0.5rem, 1.5vw, 1rem);
    font-family: var(--font-mono);
    font-size: var(--small-size);
    line-height: 1.6;
}

/* Equation block */
.equation-block {
    text-align: center;
    padding: clamp(0.5rem, 1.5vw, 1rem) 0;
    font-size: var(--h3-size);
}

/* Citation block */
.citation-block {
    font-size: var(--small-size);
    line-height: 1.5;
    padding-left: 2em;
    text-indent: -2em;
}

/* Environment titles */
.theorem-box .env-title,
.definition-box .env-title,
.example-box .env-title,
.lemma-box .env-title,
.corollary-box .env-title {
    font-weight: 700;
    font-size: var(--body-size);
    color: var(--theorem-border);
    margin-bottom: clamp(0.2rem, 0.5vw, 0.5rem);
}

.definition-box .env-title {
    color: var(--definition-border);
}

.example-box .env-title {
    color: var(--example-border);
}

/* ===========================================
   FRAME CHROME: HEADER/FOOTER BARS
   Beamer-style structural chrome
   =========================================== */

.frame-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: var(--chrome-height-top, 0);
    background: var(--header-bg);
    color: var(--header-fg);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 var(--frame-padding);
    font-size: var(--small-size);
    z-index: 100;
}

.frame-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: var(--chrome-height-bottom, 0);
    background: var(--footer-bg);
    color: var(--footer-fg);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 var(--frame-padding);
    font-size: var(--small-size);
    z-index: 100;
}

/* ===========================================
   TWO-COLUMN LAYOUT
   Academic-style side-by-side content
   =========================================== */

.columns {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    gap: clamp(1rem, 3vw, 2.5rem);
    max-height: min(75vh, 600px);
    overflow: hidden;
}

/* Sidebar layout (Berlin theme) */
.frame--sidebar {
    flex-direction: row;
}

.frame--sidebar .sidebar {
    width: var(--chrome-width-sidebar, 0);
    flex-shrink: 0;
    overflow: hidden;
    background: var(--header-bg);
    color: var(--header-fg);
}

.frame--sidebar .frame-content {
    flex: 1;
    width: calc(100% - var(--chrome-width-sidebar, 0));
}

/* ===========================================
   RESPONSIVE BREAKPOINTS - Height-based
   =========================================== */

/* Short screens (< 700px height) */
@media (max-height: 700px) {
    :root {
        --frame-padding: clamp(0.75rem, 3vw, 2rem);
        --content-gap: clamp(0.4rem, 1.5vw, 1rem);
        --title-size: clamp(1.25rem, 4.5vw, 2.5rem);
        --h2-size: clamp(1rem, 3vw, 1.75rem);
    }
}

/* Very short (< 600px height) */
@media (max-height: 600px) {
    :root {
        --frame-padding: clamp(0.5rem, 2.5vw, 1.5rem);
        --content-gap: clamp(0.3rem, 1vw, 0.75rem);
        --title-size: clamp(1.1rem, 4vw, 2rem);
        --body-size: clamp(0.7rem, 1.2vw, 0.95rem);
    }

    /* .decorative is a hook for implementers to hide optional ornamental elements */
    .frame-nav, .keyboard-hint, .decorative {
        display: none;
    }
}

/* Extremely short - landscape phones (< 500px) */
@media (max-height: 500px) {
    :root {
        --frame-padding: clamp(0.4rem, 2vw, 1rem);
        --title-size: clamp(1rem, 3.5vw, 1.5rem);
        --h2-size: clamp(0.9rem, 2.5vw, 1.25rem);
        --body-size: clamp(0.65rem, 1vw, 0.85rem);
    }
}

/* Narrow screens */
@media (max-width: 600px) {
    :root {
        --title-size: clamp(1.25rem, 7vw, 2.5rem);
    }

    .columns {
        grid-template-columns: 1fr;
    }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.2s !important;
    }

    html {
        scroll-behavior: auto;
    }
}
```

### Viewport Fitting Checklist

Before finalizing any presentation, verify:

- [ ] Every `.frame` has `height: 100vh; height: 100dvh; overflow: hidden;`
- [ ] All font sizes use `clamp(min, preferred, max)`
- [ ] All spacing uses `clamp()` or viewport units
- [ ] Breakpoints exist for heights: 700px, 600px, 500px
- [ ] Content respects density limits (max 5 bullets, max 4-line theorem, max 3 equations)
- [ ] No fixed pixel heights on content elements
- [ ] Theorem/definition boxes have `max-height: min(40vh, 350px)`
- [ ] Images have `max-height` constraints
- [ ] Frame header/footer heights use `clamp()`
- [ ] Sidebar width (Berlin) uses `clamp()` and content area accounts for it

---

## Beamer-Inspired Themes

### 1. Madrid

**Vibe:** Classic, trustworthy, formal — the default Beamer look

**Layout:** Blue header bar with section title, blue footer bar with author/title/frame number. Content centered.

**Typography:**
- Heading: `STIX Two Text` (700)
- Body: `STIX Two Text` (400)
- Mono: `Source Code Pro` (400)

**Colors:**
```css
:root {
    --bg-primary: #ffffff;
    --header-bg: #2c3e7b;
    --footer-bg: #2c3e7b;
    --header-fg: #ffffff;
    --footer-fg: #ffffff;
    --text-primary: #1a1a2e;
    --text-secondary: #4a5568;
    --theorem-bg: #e8eef8;
    --theorem-border: #2c3e7b;
    --definition-bg: #fdf2e9;
    --definition-border: #d4740e;
    --proof-bg: #f8f8f8;
    --proof-border: #95a5a6;
    --example-bg: #eafaf1;
    --example-border: #27ae60;
    --chrome-height-top: clamp(2.5rem, 5vh, 3.5rem);
    --chrome-height-bottom: clamp(1.5rem, 3vh, 2.5rem);
}
```

**Signature Elements:**
- Blue header/footer bars (classic Beamer Madrid)
- Section navigation indicators in header
- Frame number "X / Y" in footer right
- Author short name in footer left
- Short title in footer center

---

### 2. Berlin

**Vibe:** Structured, organized, navigation-focused

**Layout:** Sidebar on left with section navigation, main content right. Mini header bar.

**Typography:**
- Heading: `Source Serif 4` (600)
- Body: `Source Serif 4` (400)
- Mono: `Source Code Pro` (400)

**Colors:**
```css
:root {
    --bg-primary: #ffffff;
    --header-bg: #1a365d;
    --header-fg: #ffffff;
    --footer-bg: transparent;
    --footer-fg: #718096;
    --text-primary: #1a202c;
    --text-secondary: #4a5568;
    --theorem-bg: #ebf8ff;
    --theorem-border: #2b6cb0;
    --definition-bg: #fefce8;
    --definition-border: #a16207;
    --proof-bg: #f8f8f8;
    --proof-border: #94a3b8;
    --example-bg: #f0fdf4;
    --example-border: #15803d;
    --chrome-width-sidebar: clamp(10rem, 18vw, 14rem);
    --chrome-height-top: clamp(2rem, 4vh, 3rem);
    --chrome-height-bottom: 0;
}
```

**Signature Elements:**
- Left sidebar with section titles (vertical navigation)
- Active section highlighted
- Compact header with frame title
- No footer bar (sidebar serves as navigation)
- Section numbers in sidebar

---

### 3. Copenhagen

**Vibe:** Clean, minimal, professional

**Layout:** Small rounded header block with section name, clean content area, subtle footer.

**Typography:**
- Heading: `EB Garamond` (600)
- Body: `EB Garamond` (400)
- Mono: `Source Code Pro` (400)

**Colors:**
```css
:root {
    --bg-primary: #ffffff;
    --header-bg: #2d4a7a;
    --header-fg: #ffffff;
    --footer-bg: transparent;
    --footer-fg: #718096;
    --text-primary: #1a202c;
    --text-secondary: #4a5568;
    --theorem-bg: #f0f5ff;
    --theorem-border: #2d4a7a;
    --definition-bg: #fef3c7;
    --definition-border: #b45309;
    --proof-bg: #fafafa;
    --proof-border: #9ca3af;
    --example-bg: #ecfdf5;
    --example-border: #059669;
    --chrome-height-top: clamp(2rem, 4vh, 3rem);
    --chrome-height-bottom: clamp(1.2rem, 2.5vh, 2rem);
}
```

**Signature Elements:**
- Compact rounded header with section title
- Thin rule below header
- Clean, generous whitespace
- Subtle frame number in bottom-right

---

### 4. Warsaw

**Vibe:** Bold, authoritative, high-impact

**Layout:** Full-width gradient header bar, bold section markers, prominent footer.

**Typography:**
- Heading: `STIX Two Text` (700)
- Body: `Source Serif 4` (400)
- Mono: `Source Code Pro` (400)

**Colors:**
```css
:root {
    --bg-primary: #ffffff;
    --header-bg: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
    --footer-bg: #1a365d;
    --header-fg: #ffffff;
    --footer-fg: #ffffff;
    --text-primary: #1a202c;
    --text-secondary: #4a5568;
    --theorem-bg: #e8eef8;
    --theorem-border: #1a365d;
    --definition-bg: #fef9c3;
    --definition-border: #a16207;
    --proof-bg: #f8f8f8;
    --proof-border: #94a3b8;
    --example-bg: #dcfce7;
    --example-border: #16a34a;
    --accent: #c53030;
    --chrome-height-top: clamp(3rem, 6vh, 4.5rem);
    --chrome-height-bottom: clamp(1.5rem, 3vh, 2.5rem);
}
```

**Signature Elements:**
- Gradient header bar (navy to blue)
- Section title prominently displayed in header
- Bold separator between header and content
- Navigation dots in footer
- Red accent for alerts/emphasis

---

### 5. Metropolis

**Vibe:** Modern, clean, contemporary academic — inspired by the Metropolis (mtheme) Beamer theme

**Layout:** Dark header bar, clean sans-serif throughout, orange progress indicator.

**Typography:**
- Heading: `Fira Sans` (600)
- Body: `Fira Sans` (400)
- Mono: `Fira Code` (400)

**Colors:**
```css
:root {
    --bg-primary: #fafafa;
    --header-bg: #23373b;
    --footer-bg: #23373b;
    --header-fg: #fafafa;
    --footer-fg: #fafafa;
    --text-primary: #23373b;
    --text-secondary: #5a6872;
    --accent: #eb811b;
    --theorem-bg: #f5f0eb;
    --theorem-border: #eb811b;
    --definition-bg: #ebf5f0;
    --definition-border: #23373b;
    --proof-bg: #f5f5f5;
    --proof-border: #8a9ba5;
    --example-bg: #fdf6ec;
    --example-border: #eb811b;
    --chrome-height-top: clamp(2.5rem, 5vh, 3.5rem);
    --chrome-height-bottom: clamp(1.2rem, 2.5vh, 2rem);
}
```

**Signature Elements:**
- Dark teal header/footer bars
- Orange accent color (signature Metropolis)
- Fira Sans typography (matches the real Metropolis)
- Orange progress bar at top
- Clean, modern feel distinct from traditional Beamer

---

### 6. Classic Serif

**Vibe:** Traditional LaTeX, pure academic, mathematical

**Layout:** No chrome bars — pure content. Thin horizontal rules only. Centered frame titles.

**Typography:**
- Heading: `CMU Serif` / Latin Modern Roman (via CDN)
- Body: `CMU Serif` / Latin Modern Roman
- Mono: `CMU Typewriter Text` / Latin Modern Mono
- Font URL: `https://cdn.jsdelivr.net/npm/computer-modern@0.1.2/cmu-serif.css`

**Colors:**
```css
:root {
    --bg-primary: #fffff8;
    --header-bg: transparent;
    --header-fg: #111111;
    --footer-bg: transparent;
    --footer-fg: #666666;
    --text-primary: #111111;
    --text-secondary: #444444;
    --theorem-bg: #f5f5f0;
    --theorem-border: #333333;
    --definition-bg: #f0f5f0;
    --definition-border: #2e5c3f;
    --proof-bg: transparent;
    --proof-border: #888888;
    --example-bg: #f5f0f0;
    --example-border: #5c2e2e;
    --chrome-height-top: 0;
    --chrome-height-bottom: clamp(1rem, 2vh, 1.5rem);
}
```

**Signature Elements:**
- Computer Modern / Latin Modern fonts (authentic LaTeX typography)
- No header bar — frame title serves as header
- Thin horizontal rules as separators
- Minimal frame number in bottom-right
- Cream/off-white background for paper-like feel
- This is the most "LaTeX-like" theme

---

### 7. Cambridge

**Vibe:** University formal, prestigious, ceremonial

**Layout:** Green header bar with university-style crest area, gold accents.

**Typography:**
- Heading: `EB Garamond` (700)
- Body: `Source Serif 4` (400)
- Mono: `Source Code Pro` (400)

**Colors:**
```css
:root {
    --bg-primary: #fffdf7;
    --header-bg: #1e3a2f;
    --footer-bg: #1e3a2f;
    --header-fg: #d4af37;
    --footer-fg: #d4af37;
    --text-primary: #1a1a2e;
    --text-secondary: #4a5568;
    --accent: #d4af37;
    --theorem-bg: #f0f5f2;
    --theorem-border: #1e3a2f;
    --definition-bg: #fdf8e8;
    --definition-border: #8b6914;
    --proof-bg: #f8f8f5;
    --proof-border: #7a8a7f;
    --example-bg: #eef5f0;
    --example-border: #2d5a3f;
    --chrome-height-top: clamp(2.5rem, 5vh, 4rem);
    --chrome-height-bottom: clamp(1.5rem, 3vh, 2.5rem);
}
```

**Signature Elements:**
- Forest green + gold color scheme
- Space for university crest/logo in header
- Gold accent lines
- Formal, serif-heavy typography
- Appropriate for thesis defense, inaugural lectures

---

### 8. Lecture Notes

**Vibe:** Warm, approachable, pedagogical — like a professor's well-organized notes

**Layout:** Warm background, generous spacing, large fonts for readability.

**Typography:**
- Heading: `Source Serif 4` (700)
- Body: `Source Serif 4` (400)
- Mono: `Source Code Pro` (400)

**Colors:**
```css
:root {
    --bg-primary: #faf6f0;
    --header-bg: transparent;
    --header-fg: #2d2d2d;
    --footer-bg: transparent;
    --footer-fg: #6b5b4f;
    --text-primary: #2d2d2d;
    --text-secondary: #6b5b4f;
    --accent: #c0392b;
    --theorem-bg: #fff8e1;
    --theorem-border: #c0392b;
    --definition-bg: #e8f5e9;
    --definition-border: #2e7d32;
    --proof-bg: #faf6f0;
    --proof-border: #a0937e;
    --example-bg: #e3f2fd;
    --example-border: #1565c0;
    --chrome-height-top: 0;
    --chrome-height-bottom: clamp(1rem, 2vh, 1.5rem);
}
```

**Signature Elements:**
- Warm, parchment-like background
- No header bar — open, spacious feel
- Red accent for emphasis (like a professor's red pen)
- Larger font sizes than other themes
- Theorem boxes with warm yellow background
- Friendly, inviting aesthetic for students

---

### 9. Technical Report

**Vibe:** Dense, precise, engineering-focused

**Layout:** Compact header, two-column-friendly, monospace accents.

**Typography:**
- Heading: `Source Serif 4` (600)
- Body: `Source Serif 4` (400)
- Mono: `Source Code Pro` (400)

**Colors:**
```css
:root {
    --bg-primary: #ffffff;
    --header-bg: #2d3748;
    --footer-bg: #2d3748;
    --header-fg: #e2e8f0;
    --footer-fg: #e2e8f0;
    --text-primary: #1a202c;
    --text-secondary: #4a5568;
    --accent: #3182ce;
    --theorem-bg: #ebf8ff;
    --theorem-border: #3182ce;
    --definition-bg: #fefce8;
    --definition-border: #a16207;
    --proof-bg: #f7fafc;
    --proof-border: #a0aec0;
    --example-bg: #f0fff4;
    --example-border: #38a169;
    --chrome-height-top: clamp(2rem, 4vh, 3rem);
    --chrome-height-bottom: clamp(1.2rem, 2.5vh, 2rem);
}
```

**Signature Elements:**
- Compact layout maximizing content density
- Blue accent color (IEEE/ACM style)
- Monospace elements for code/algorithm emphasis
- Two-column layout support (`.columns` class)
- Good for data-heavy technical presentations

---

### 10. Thesis Defense

**Vibe:** Formal, authoritative, institution-ready

**Layout:** Dark navy header with institution name, structured frame layout.

**Typography:**
- Heading: `STIX Two Text` (700)
- Body: `Source Serif 4` (400)
- Mono: `Source Code Pro` (400)

**Colors:**
```css
:root {
    --bg-primary: #ffffff;
    --header-bg: #0d1b2a;
    --footer-bg: #0d1b2a;
    --header-fg: #e0e7ff;
    --footer-fg: #e0e7ff;
    --text-primary: #0d1b2a;
    --text-secondary: #334155;
    --accent: #1d4ed8;
    --theorem-bg: #eff6ff;
    --theorem-border: #1d4ed8;
    --definition-bg: #fefce8;
    --definition-border: #a16207;
    --proof-bg: #f8fafc;
    --proof-border: #94a3b8;
    --example-bg: #f0fdf4;
    --example-border: #16a34a;
    --chrome-height-top: clamp(3rem, 6vh, 4.5rem);
    --chrome-height-bottom: clamp(1.5rem, 3vh, 2.5rem);
}
```

**Signature Elements:**
- Dark navy bars (authority, formality)
- Space for institution logo in header
- Committee-friendly: clear frame structure
- Prominent frame numbering
- Blue accent throughout

---

### 11. Seminar

**Vibe:** Informal, relaxed, discussion-oriented

**Layout:** Minimal chrome, light background, emphasis on readability.

**Typography:**
- Heading: `EB Garamond` (500 italic)
- Body: `EB Garamond` (400)
- Mono: `Source Code Pro` (400)

**Colors:**
```css
:root {
    --bg-primary: #fafaf8;
    --header-bg: transparent;
    --header-fg: #2d3436;
    --footer-bg: transparent;
    --footer-fg: #636e72;
    --text-primary: #2d3436;
    --text-secondary: #636e72;
    --accent: #6c5ce7;
    --theorem-bg: #f3f0ff;
    --theorem-border: #6c5ce7;
    --definition-bg: #fef3f2;
    --definition-border: #b91c1c;
    --proof-bg: transparent;
    --proof-border: #a1a1aa;
    --example-bg: #f0f9ff;
    --example-border: #0284c7;
    --chrome-height-top: 0;
    --chrome-height-bottom: clamp(0.8rem, 1.5vh, 1.2rem);
}
```

**Signature Elements:**
- No header bar — casual, open feel
- Italic display headings (conversational)
- Purple accent (informal, creative)
- Minimal decoration
- Very small footer with just frame number
- Good for lab meetings, reading groups

---

### 12. Journal Article

**Vibe:** Paper-like, mathematical, publication-quality

**Layout:** Two-column support, centered theorems, paper-like margins.

**Typography:**
- Heading: `STIX Two Text` (600)
- Body: `Source Serif 4` (400)
- Mono: `Source Code Pro` (400)

**Colors:**
```css
:root {
    --bg-primary: #ffffff;
    --header-bg: transparent;
    --header-fg: #000000;
    --footer-bg: transparent;
    --footer-fg: #666666;
    --text-primary: #000000;
    --text-secondary: #333333;
    --theorem-bg: #f8f8f8;
    --theorem-border: #000000;
    --definition-bg: #f0f0f0;
    --definition-border: #333333;
    --proof-bg: transparent;
    --proof-border: #666666;
    --example-bg: #f5f5f5;
    --example-border: #444444;
    --chrome-height-top: 0;
    --chrome-height-bottom: clamp(1rem, 2vh, 1.5rem);
}
```

**Signature Elements:**
- Pure black + white (journal paper aesthetic)
- Strong horizontal rules between sections
- Two-column layout support
- Centered, numbered theorem environments
- Minimal — content is the design
- AMS/Springer journal feel

---

## Font Pairing Quick Reference

| Preset | Heading Font | Body Font | Mono Font | Source |
|--------|-------------|-----------|-----------|--------|
| Madrid | STIX Two Text (700) | STIX Two Text (400) | Source Code Pro | Google Fonts |
| Berlin | Source Serif 4 (600) | Source Serif 4 (400) | Source Code Pro | Google Fonts |
| Copenhagen | EB Garamond (600) | EB Garamond (400) | Source Code Pro | Google Fonts |
| Warsaw | STIX Two Text (700) | Source Serif 4 (400) | Source Code Pro | Google Fonts |
| Metropolis | Fira Sans (600) | Fira Sans (400) | Fira Code | Google Fonts |
| Classic Serif | CMU Serif | CMU Serif | CMU Typewriter Text | jsDelivr CDN |
| Cambridge | EB Garamond (700) | Source Serif 4 (400) | Source Code Pro | Google Fonts |
| Lecture Notes | Source Serif 4 (700) | Source Serif 4 (400) | Source Code Pro | Google Fonts |
| Technical Report | Source Serif 4 (600) | Source Serif 4 (400) | Source Code Pro | Google Fonts |
| Thesis Defense | STIX Two Text (700) | Source Serif 4 (400) | Source Code Pro | Google Fonts |
| Seminar | EB Garamond (500i) | EB Garamond (400) | Source Code Pro | Google Fonts |
| Journal Article | STIX Two Text (600) | Source Serif 4 (400) | Source Code Pro | Google Fonts |

---

## DO NOT USE (Generic / Non-Academic Patterns)

**Fonts:** Calibri, Arial, Comic Sans, display/decorative fonts (Archivo Black, Syne, Clash Display). No sans-serif as the sole body font except in Metropolis.

**Colors:** Neon accents (#00ffcc, #d4ff00, #ff00aa), pure saturated backgrounds, electric blue (#0066ff), gradient meshes.

**Layouts:** Centered-only with no frame structure. Floating abstract blobs. Asymmetric "creative" layouts. Everything on dark backgrounds (except Lecture Notes optional dark mode).

**Animations:** Scale transitions, slide-from-left/right, blur effects, particle systems, 3D tilt, custom cursors. Academic slides use opacity fade ONLY (200-300ms).

**Decorations:** Abstract gradient shapes, halftone textures, neon glow box-shadows, noise textures. Academic slides use horizontal rules, theorem box borders, and structural chrome only.

---

## Troubleshooting

### KaTeX Equations Not Rendering

**Symptoms:** Raw LaTeX source visible instead of rendered math.

**Solutions:**
1. Verify KaTeX CSS and JS CDN links are included in `<head>`
2. Check delimiter configuration (`$...$` for inline, `$$...$$` for display)
3. Ensure KaTeX auto-render script runs after DOM load
4. Verify no CSP (Content Security Policy) blocks the CDN

### Computer Modern Fonts Not Loading

**Symptoms:** Fallback serif font (Georgia/Times) appears instead of CMU Serif.

**Solutions:**
1. Check jsDelivr CDN link: `https://cdn.jsdelivr.net/npm/computer-modern@0.1.2/cmu-serif.css`
2. Add fallback chain: `font-family: 'CMU Serif', 'Latin Modern Roman', 'Georgia', serif;`
3. Test with browser DevTools Network tab to confirm font files load
4. If CDN is blocked, consider self-hosting the WOFF2 files

### Theorem Box Overflows Frame

**Symptoms:** Theorem or proof content extends beyond the frame boundary.

**Solutions:**
1. Reduce content within the box (max 4 lines for theorem, 5 for proof)
2. Split into multiple frames: "Theorem" frame + "Proof" frame
3. Verify `max-height: min(40vh, 350px)` is set on theorem boxes
4. Check that `overflow: hidden` is on the `.frame` element

### Frame Numbering Incorrect

**Symptoms:** Frame counter shows wrong numbers or does not update.

**Solutions:**
1. Check JS frame counter initialization (should count `.frame` elements)
2. Verify `querySelectorAll('.frame')` matches all frame sections
3. Ensure the counter updates on scroll/navigation events
4. Check for duplicate frame IDs or missing frame elements

### Header/Footer Bars Overlapping Content

**Symptoms:** Frame chrome covers frame content text.

**Solutions:**
1. Verify `--chrome-height-top` and `--chrome-height-bottom` variables match actual bar heights
2. Add matching `padding-top` / `padding-bottom` to `.frame-content`
3. For Berlin sidebar: ensure content area has `margin-left: var(--chrome-width-sidebar)`
4. Test at multiple viewport heights — chrome heights should use `clamp()`

### Two-Column Layout Collapsing

**Symptoms:** `.columns` layout stacks vertically on wider screens or overflows.

**Solutions:**
1. Check `min-width` on column children is not too large
2. Verify the 600px responsive breakpoint is present
3. Ensure `.columns` has `gap` using `clamp()` not fixed pixels
4. Test with varying content lengths in both columns

### Text Too Small on Mobile / Too Large on Desktop

**Symptoms:** Unreadable text on phones, oversized text on big screens.

**Solutions:**
```css
/* Use clamp with viewport-relative middle value */
font-size: clamp(1rem, 3vw, 2.5rem);
/*              ^       ^      ^
            minimum  scales  maximum */
```

### Content Doesn't Fill Short Screens

**Symptoms:** Excessive whitespace on landscape phones or short browser windows.

**Solutions:**
1. Add `@media (max-height: 600px)` and `(max-height: 500px)` breakpoints
2. Reduce padding at smaller heights
3. Hide non-essential chrome (`display: none` on `.frame-nav`, `.decorative`)
4. Verify frame header/footer bars shrink appropriately via `clamp()`

### Testing Recommendations

Test at these viewport sizes:
- **Desktop:** 1920x1080, 1440x900, 1280x720
- **Tablet:** 1024x768 (landscape), 768x1024 (portrait)
- **Mobile:** 375x667 (iPhone SE), 414x896 (iPhone 11)
- **Landscape phone:** 667x375, 896x414

Use browser DevTools responsive mode to quickly test multiple sizes.

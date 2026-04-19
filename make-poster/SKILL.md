---
name: make-poster
description: Generate an HTML conference poster from a paper and project website, printable to PDF
argument-hint: <any formatting notes, conference name, or instructions URL>
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, Agent
---

# Conference Poster Generator (HTML)

Generate a professional HTML poster. User notes: $ARGUMENTS

The poster is a **React-based interactive editor** — a single self-contained HTML file in the `poster/` directory. No build step needed (React/Babel loaded via CDN). The user can visually adjust the layout in their browser, then export the config back to Claude for further changes.

## Project folder structure

```
<project>/
├── overleaf/              # Paper source from Overleaf
│   ├── paper.tex
│   ├── figures/
│   └── ...
├── references/            # Reference posters for style matching
│   └── (any format: pdf, png, jpg, html, pptx, ...)
├── poster/                # GENERATED: self-contained poster website
│   ├── index.html         # The poster (React app)
│   ├── poster-config.json # Layout config (columns, card order, heights, font scale)
│   ├── logos/             # Institution logos
│   ├── teaser.png         # Copied/converted figures
│   ├── qr.png             # Project page QR code
│   ├── qr-posterskill.png # Posterskill QR code
│   └── ...
└── .claude/skills/make-poster/
```

- **`overleaf/`** contains the paper source. Read the main `.tex` file and any files it `\input{}`s.
- **`references/`** contains example posters showing the user's preferred visual style. Read/view ALL files in this folder to match their design language.
- **`poster/`** is the generated output — a self-contained website. All figures and assets live alongside `index.html` so relative paths just work.

## Inputs

1. **Paper source** - Located in `overleaf/`. Ask the user which `.tex` file is the main one to read (e.g., `paper.tex`, `main.tex`). Then read it and any files it `\input{}`s.
2. **Project website** - Ask the user for the URL if not already known. Fetch with WebFetch to extract author info, hosted images, and links.
3. **Reference posters** - Auto-discovered from `references/`. View all files there and match their style.
4. **Author website** (optional) - Fetch with WebFetch and extract design signals (color palette, typography, logos). Download institutional logos from the author's site using Playwright (curl may fail due to redirects): `page.request.get(url)` to download the raw bytes.
5. **Formatting requirements** - Ask for poster dimensions, orientation, number of columns.
6. **Git repo** (optional) - Ask the user if they have a GitHub repo to push the poster to.

If the user doesn't specify formatting, ask them before proceeding. Don't assume defaults for dimensions, orientation, or column count.

## Process

### Step 0: Analyze style references
Look in `references/` for any PDF, PNG, or image files. Convert PDFs to PNGs (`sips -s format png` on macOS). View each one and note the visual style — layout, colors, typography, card styles, figure placement. **Match the reference style** — don't default to a dark theme if the reference is light, etc.

### Step 1: Extract content from paper source
Ask the user which `.tex` file to read. Extract: title, authors, affiliations, abstract (2-3 sentences), key method, results (tables + figures), key equations (1-2 max), conclusion.

### Step 2: Fetch the project website
Use WebFetch to get author names, affiliations, figure URLs, project URL for QR, links to code/arxiv/video.

### Step 3: Gather assets into `poster/`

**Figures:** Copy from `overleaf/figures/`, converting PDFs to PNGs at high resolution:
```bash
sips -s format png input.pdf --out poster/output.png -Z 3000
```

**Website images:** Download higher-quality images from the project website using Playwright (not curl — many sites redirect):
```python
resp = page.request.get(url)
with open('poster/filename.png', 'wb') as f:
    f.write(resp.body())
```

**Logos:** Download institutional logos from the author's personal website using Playwright. Save to `poster/logos/`. The template auto-inverts them to white for the header.

**QR codes:** Generate and save:
```bash
curl -sL -o poster/qr.png "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=PROJECT_URL"
curl -sL -o poster/qr-posterskill.png "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=https://github.com/ethanweber/posterskill"
```

### Step 4: Measure image aspect ratios
**This is critical for eliminating whitespace.** Measure every image:
```bash
sips -g pixelWidth -g pixelHeight poster/*.png poster/*.jpg
```

Then assign images to columns based on aspect ratio:
- **Wide images** (>2:1 ratio, e.g. teaser, architecture): put in the widest column
- **Square images** (~1:1 ratio): put in narrow columns
- **Portrait images** (<1:1 ratio): put in the narrowest column

This prevents the #1 whitespace problem: wide images in narrow cells (or vice versa) leaving huge gaps.

### Step 5: Generate the poster HTML

Use the template at `${{CLAUDE_SKILL_DIR}}/template.html` as a starting point. The template is a React app with:

**Architecture:**
- `CARD_REGISTRY` — defines each card's content (title, color, JSX body)
- `DEFAULT_LAYOUT` — defines column structure and card ordering
- `DEFAULT_LOGOS` — institutional logos for the header
- React state manages layout, with localStorage persistence
- `window.posterAPI` exposes functions for programmatic control

**Key things to customize:**
1. Update `CARD_REGISTRY` with the paper's content (each section is a card)
2. Update `DEFAULT_LAYOUT` with the aspect-ratio-optimized column assignments
3. Update `DEFAULT_LOGOS` with the user's institutional logos
4. Update `DEFAULT_FONT_SCALE` (start at 1.3, user can adjust with A-/A+ buttons)
5. Update the header (title, authors, affiliations, conference badge, QR codes)
6. Update `@page { size: WIDTHmm HEIGHTmm; }` and `body { width: WIDTHmm; height: HEIGHTmm; }` for the poster dimensions
7. Update `posterAPI` fit() function with the same dimensions

**Card content patterns:**
- Figure card: `<div className="fig"><div className="fig-wrap"><img src="file.png" alt="..." /></div><div className="cap"><b>Caption title.</b> Description.</div></div>`
- Text card: `<div className="hl"><p>Highlight text</p></div><ul><li>Point 1</li></ul>`
- Table card: `<table><thead>...</thead><tbody>...</tbody></table>` with `className="best"` on winning cells
- Equation card: `<div className="eq">{'$LaTeX equation$'}</div>` (escape backslashes in JSX)

**Critical CSS rules for zero whitespace:**
- Images MUST use `width:100%; height:100%; object-fit:contain` (NOT max-width/max-height — those prevent upscaling)
- Each column must always have one card with `grow: true` (flex:1) that fills remaining space
- The `isCardGrow()` function ensures this automatically — if no card has grow, the last card gets it

**Viewport scaling:**
- Use `translate() + scale()` on body to center and fit the poster to any browser viewport
- `transform-origin: top left` is critical
- `@media print` must set `transform: none !important` for correct print resolution
- `getBoundingClientRect()` returns SCALED values — always divide by `currentScaleRef.current` in resize handlers

### Step 6: Auto-optimize layout with Playwright

After generating, use Playwright to measure whitespace and find optimal column widths:

```python
from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 3200, 'height': 2260})
    page.goto('file://' + os.path.abspath('poster/index.html'))
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    # Measure whitespace
    waste = page.evaluate('window.posterAPI.getWaste()')
    print(f"Total waste: {waste['total']}px")
    for d in waste['details']:
        print(f"  {d['card']}: H={d['wasteH']} W={d['wasteW']} ({d['pct']}%)")

    # Try different column widths to minimize waste
    best_waste = waste['total']
    best_c1, best_c3 = 300, 230
    for c1 in range(200, 350, 10):
        for c3 in range(160, 280, 10):
            page.evaluate(f'window.posterAPI.setColumnWidth("col1", {c1})')
            page.evaluate(f'window.posterAPI.setColumnWidth("col3", {c3})')
            page.wait_for_timeout(30)
            w = page.evaluate('window.posterAPI.getWaste().total')
            if w < best_waste:
                best_waste = w
                best_c1, best_c3 = c1, c3

    # Apply best and screenshot
    page.evaluate(f'window.posterAPI.setColumnWidth("col1", {best_c1})')
    page.evaluate(f'window.posterAPI.setColumnWidth("col3", {best_c3})')
    page.wait_for_timeout(500)
    page.screenshot(path='/tmp/poster_screenshot.png')

    # Also try swapping cards between columns
    page.evaluate('window.posterAPI.swapCards("cardA", "cardB")')
    # ... measure waste again ...

    browser.close()
```

Then read `/tmp/poster_screenshot.png` to visually inspect. **Iterate multiple times** — take screenshots, fix issues, re-screenshot until the poster has minimal blank space.

After finding optimal values, bake them into `DEFAULT_LAYOUT`, `DEFAULT_CARD_HEIGHTS`, etc. in the HTML.

### Step 7: Generate PDF and verify

```python
page.pdf(
    path='poster/poster.pdf',
    width='841mm', height='594mm',  # match poster dimensions
    margin={'top':'0','right':'0','bottom':'0','left':'0'},
    print_background=True
)
```

Convert the PDF to PNG and read it to verify it renders at full resolution:
```bash
sips -s format png poster/poster.pdf --out /tmp/poster_pdf_check.png -Z 3000
```

### Step 8: Open and iterate with user

Open the poster in the browser:
```bash
open poster/index.html
```

**Explain the editing controls to the user:**
- **Preview** — toggle edit UI off to see exactly how it will print
- **A-/A+** — adjust font size globally
- **Drag column dividers** (vertical blue bars) — resize columns left/right
- **Drag row dividers** (horizontal blue bars) — resize cards up/down within columns
- **Click-to-swap** — click one card's diamond handle (turns orange), then click another's to swap them
- **Move/insert** — click a card's handle, then click a dashed orange drop zone to move it there
- **Save** — downloads `poster-config.json`
- **Copy Config** — copies layout JSON to clipboard
- **Reset** — restore defaults

**Proactively suggest improvements:** After showing the first draft, suggest specific changes:
- "The model architecture card has some whitespace — try dragging the row divider above it down to give it less space"
- "The completion figure might look better in column 2 since it's wider — try clicking its diamond, then clicking a drop zone in column 2"
- "You might want to bump the font size with A+ a few times"

**Encourage the feedback loop:** Tell the user:
> Try rearranging the poster in your browser! When you're happy with the layout, click **Copy Config** in the top-right toolbar and paste it here — I'll bake those changes into the defaults so they persist.
- **Save** — download `poster-config.json`
- **Copy Config** — copy layout JSON to clipboard to paste to Claude
- **Reset** — restore defaults

When the user pastes a config JSON, update `DEFAULT_LAYOUT`, `DEFAULT_CARD_HEIGHTS`, `DEFAULT_FONT_SCALE`, and `DEFAULT_LOGOS` in the HTML to match. Also write it to `poster-config.json`.

### Step 9: Push to GitHub (optional)

If the user provides a GitHub repo URL:
```bash
cd poster
git init
git remote add origin <REPO_URL>
git add .
git commit -m "Poster: <paper title>"
git push -u origin main
```

## Important guidelines

- **No blank space.** This is the #1 priority. Use aspect-ratio-aware column assignment, `width:100%; height:100%; object-fit:contain` on images, auto-grow cards, and the Playwright optimizer. Iterate until waste is minimal.
- **Keep text minimal.** Posters are visual — bullet points, not paragraphs. 2-minute understanding.
- **Match the reference style.** If the reference poster is light/clean, don't use a dark theme. Match the overall aesthetic.
- **Font scaling.** All text sizes use `calc(Xpt * var(--font-scale))` so the A-/A+ buttons work. Start with `--font-scale: 1.3` and let the user adjust.
- **Print-optimized CSS.** `@media print` hides all edit UI and sets `transform: none !important`. `@page` sets exact dimensions.
- **Posterskill QR.** Always include a QR code linking to `https://github.com/ethanweber/posterskill` in the header with the label "Poster made with my Claude skill".
- **No acknowledgements footer.** Keep the poster clean — no footer by default.
- **Logos in header.** Download institutional logos from the author's website, save to `poster/logos/`, and list them in `DEFAULT_LOGOS`. They're auto-inverted to white via CSS filter.
- **Self-contained.** No build step, no npm, no server. Single HTML file with CDN dependencies. Works when opened directly as `file://`.
- **Equations.** Use KaTeX (loaded via CDN). Escape backslashes in JSX strings: `{'$\\mathcal{E}$'}`.

## Figure handling
- Always copy needed figures into `poster/` — don't reference `overleaf/` paths in the HTML.
- Convert PDFs to PNGs at high resolution: `sips -s format png input.pdf --out poster/output.png -Z 3000`
- Download website images via Playwright's `page.request.get()` (not curl — websites often redirect).
- Measure aspect ratios with `sips -g pixelWidth -g pixelHeight` and assign to columns accordingly.

## User workflow for config updates

The user can adjust the poster in their browser and share changes back:
1. User clicks "Copy Config" in the toolbar
2. User pastes the JSON in chat
3. Claude updates `DEFAULT_LAYOUT`, `DEFAULT_CARD_HEIGHTS`, `DEFAULT_FONT_SCALE`, `DEFAULT_LOGOS` in `index.html` to match
4. Claude also writes the config to `poster-config.json`
5. User refreshes and clicks "Reset" to load new defaults

## Programmatic API (window.posterAPI)

Available in the browser console or via Playwright:
- `swapCards(id1, id2)` — swap two cards (works across columns)
- `moveCard(cardId, targetColId, position)` — move a card to a specific position
- `setColumnWidth(colId, widthMm)` — set column width (null for flex)
- `setCardHeight(cardId, heightMm)` — set explicit card height (null to reset)
- `setFontScale(scale)` — set global font scale
- `getWaste()` — measure total whitespace in figure containers
- `getLayout()` — get current layout with rendered dimensions
- `getConfig()` — get full serializable config
- `resetLayout()` — restore defaults
- `saveConfig()` — trigger download of poster-config.json
- `copyConfig()` — copy config JSON to clipboard

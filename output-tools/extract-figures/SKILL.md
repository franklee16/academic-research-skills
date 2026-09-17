---
name: extract-figures
description: Extract all embedded figures, charts, diagrams, and images from a Word (.docx) document into a subfolder, converting vector formats (EMF/WMF) to LaTeX-ready 300 DPI PNGs, and produce a README with a ready-to-paste LaTeX snippet. Use this skill whenever the user asks to extract, pull, export, or get figures, images, charts, diagrams, plots, or graphics out of a .docx file. Also trigger on phrases like "get the figures from this Word doc", "pull images out of this manuscript", "extract the charts", or any request to make figures from a .docx usable in LaTeX, slides, or other documents. Trigger even when the user doesn't explicitly say "extract" — any request to get figures out of a Word document for downstream use qualifies. Make sure to use this skill whenever the user mentions figures, images, charts, diagrams, plots, graphics, or visual content from a Word document, even if they don't explicitly say "extract".
---

# Extract Figures from DOCX to LaTeX-Ready PNGs

Pulls every embedded image out of a Word document, converts vector formats to high-resolution PNG, determines document structure from surrounding captions, verifies visual content, and produces a mapping document with a ready-to-paste LaTeX snippet.

## Why This Skill Exists

DOCX figure extraction is full of invisible traps that produce silently wrong outputs:

1. **rId order is meaningless.** Inside a .docx, images are stored as `image1.emf`, `image2.emf`, etc. These numbers are assigned arbitrarily by Word at save time. Naming files based on this number will scramble the panel order of multi-panel figures.
2. **Body XML order is not always visual order.** Within a table or floating layout, the XML traversal order may differ from left-to-right reading order. Two images inside the same paragraph or table cell can appear in the opposite of the visual order.
3. **EMF is Word's default vector format.** Charts, Stata graphs, and most diagrams are stored as EMF (Enhanced Metafile). LaTeX cannot include EMF directly; you need PNG or PDF. 300 DPI PNG is sufficient for journal submissions.
4. **No external tools needed.** Pillow's image library reads EMF directly via its WMF reader. You do not need LibreOffice, Inkscape, or ImageMagick.
5. **Captures live in surrounding paragraphs.** "Figure 1. Title" text is in paragraphs near the image, not metadata. To understand figure structure, you must parse the document body XML and read the text around each image.

The correct approach: extract all media, convert vectors to PNG, walk the document body XML to locate each image and its caption, and **verify visual content by viewing the images** — especially for multi-panel figures — before assigning meaningful names.

## Prerequisites

- Python with `python-docx` and `Pillow` installed (`pip install python-docx Pillow`)
- UTF-8 output encoding (Windows defaults to GBK on Chinese locales — the bundled script sets it explicitly)

## Process

### Step 1: Verify the source document

Use Glob to confirm the `.docx` exists. If the user gives a relative path, resolve it from the project root.

Default output folder: a `figures/` subdirectory next to the source document (e.g., `Draft/CBAM.docx` → `Draft/figures/`). If the user specifies a different folder, respect it.

### Step 2: Run the extraction script

Execute the bundled script:

```bash
python scripts/extract_figures.py "<absolute_path_to_docx>" ["<output_dir>"]
```

The script:

1. Opens the .docx as a ZIP archive and extracts every file from `word/media/`
2. Converts EMF/WMF/EMZ/WMZ to PNG at 300 DPI using Pillow
3. Keeps PNG/JPG/GIF/BMP as-is (also copied to output dir)
4. Parses `word/_rels/document.xml.rels` for rId → media mappings
5. Walks `word/document.xml` body, finding every image reference (`<a:blip r:embed="rId..."/>`) and its body XML position
6. Detects "Figure N" captions by looking at surrounding paragraphs (regex on text or Caption paragraph style)
7. Assigns each image to its closest figure caption, then sorts by body XML order within each figure
8. Saves output as `img_001.png`, `img_002.png`, ... in document body order
9. Writes `_manifest.json` containing the full mapping (filename, original, rId, body position, figure number, position in figure, caption text)
10. Writes `_readme_draft.md` with a basic mapping table

**Important:** The script produces *position-based* filenames (`img_001.png`). It does **not** attempt content-aware naming. That step is done by the LLM in Step 3 because it requires visual verification.

### Step 3: Verify visual content and rename

Read `_manifest.json` to understand which images belong to which figures.

If any figure has more than one panel (i.e., any `fig_num` appears more than once in the manifest), **view every PNG in that figure with the Read tool** to confirm visual content.

What to look for:

- Chart titles or axis labels embedded in the image
- Sub-panel labels visible in the figure ("(a)", "Panel A", etc.)
- Any text that distinguishes one panel from another (e.g., `pct_eu_newsupplier` in a Stata graph title)

If body XML order matches visual order, great. If not (e.g., a "drop supplier" panel appears before a "new supplier" panel in the XML but after it visually), **rename the files** to match visual content. Use temp filenames to avoid collisions during swaps:

```python
import shutil, os

# To swap a.png and b.png:
os.rename("a.png", "tmp_a.png")
os.rename("b.png", "a.png")
os.rename("tmp_a.png", "b.png")
```

Then update the `_manifest.json` `filename` fields to reflect the new names.

### Step 4: Write the final README

Rename `_readme_draft.md` to `README.md` and fill in the verified content.

The README should contain:

1. **Header** — total figure count and total panel images
2. **Source** — extraction date, source format, conversion method
3. **Files table** — columns: output filename, content description (one line), original media file, rId, body position, figure number
4. **Captions** — full caption text for each figure, copied from the document
5. **LaTeX Usage** — ready-to-paste snippet using `subcaption` for multi-panel figures or plain `\includegraphics` for single images

For multi-panel figures with 2 columns, use this template:

```latex
\begin{figure}[H]
\centering
\caption{<figure title>}
\label{fig:<short-id>}

\textbf{Panel A: <panel A title>}\\[0.5em]
\begin{subfigure}{0.48\textwidth}
  \includegraphics[width=\linewidth]{figures/<file>.png}
  \caption{<sub-caption>}
\end{subfigure}
\hfill
\begin{subfigure}{0.48\textwidth}
  \includegraphics[width=\linewidth]{figures/<file>.png}
  \caption{<sub-caption>}
\end{subfigure}

\vspace{1em}
\textbf{Panel B: <panel B title>}\\[0.5em]
\begin{subfigure}{0.48\textwidth}
  \includegraphics[width=\linewidth]{figures/<file>.png}
  \caption{<sub-caption>}
\end{subfigure}
\hfill
\begin{subfigure}{0.48\textwidth}
  \includegraphics[width=\linewidth]{figures/<file>.png}
  \caption{<sub-caption>}
\end{subfigure}

\begin{tablenotes}
\footnotesize
\item <full caption from document>
\end{tablenotes}
\end{figure}
```

For single-image figures:

```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{figures/<file>.png}
\caption{<figure title>}
\label{fig:<short-id>}
\end{figure}
```

### Step 5: Report to the user

Summarize:

- N figures extracted, M total panel images
- Output folder path
- Any ambiguities flagged (e.g., "Figure 3 has 4 panels; I renamed them after viewing content, but double-check against the document")
- Pointer to the README for full mapping and LaTeX snippet

## Bundled Script Details

The extraction script is bundled at `scripts/extract_figures.py`. It is self-contained (no external dependencies besides Pillow) and handles:

- ZIP extraction of `word/media/`
- EMF/WMF → PNG conversion at 300 DPI
- Body XML parsing for figure structure
- Caption detection via "Figure N" regex and paragraph style inspection
- JSON manifest generation

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Panels swapped left/right | Trusting rId order or even body XML order for multi-panel figures | View each PNG to verify visual content; rename to match |
| Empty/black PNG output | EMF parse failed silently | Check Pillow version (≥9.5). Some complex EMFs may need LibreOffice headless fallback |
| Figures missing entirely | Image was a SmartArt or Office chart object (not embedded media) | These don't appear in `word/media/`. Render the whole document via LibreOffice or extract from `word/charts/` |
| Filenames collide on rename | Renaming `a.png` to `b.png` while `b.png` exists | Use temp filename during swap (`a` → `tmp_a`, then `b` → `a`, then `tmp_a` → `b`) |
| UnicodeEncodeError on Windows | Default GBK encoding in Python stdout | Script sets `sys.stdout` to UTF-8 wrapper; verify `chcp 65001` if running manually |
| `pip install svglib` is unnecessary | Trying to convert EMF without checking Pillow first | Pillow reads EMF natively as WMF format |
| `2>$null` in Bash | PowerShell redirect used in a Bash command | Use `2>nul` (Windows cmd), `2>/dev/null` (Unix), or switch to the PowerShell tool |
| `2>$null` in PowerShell | Bash redirect used in PowerShell | Use `2>$null` correctly in PowerShell (the `$` goes before `null`) |

## Output Format

Final layout in the output folder:

```
figures/
├── README.md              # Verified mapping + LaTeX snippet
├── _manifest.json         # Machine-readable mapping
├── fig1_eu_new_supplier.png   # Renamed after visual verification
├── fig1_eu_drop_supplier.png
├── fig1_neu_new_supplier.png
├── fig1_neu_drop_supplier.png
├── image1.emf             # Originals preserved
├── image2.emf
├── image3.emf
└── image4.emf
```

The script initially produces `img_001.png`, `img_002.png`, etc. The LLM then renames them to content-aware names (e.g., `fig1_eu_new_supplier.png`) after viewing the images. This two-step approach prevents the rId-order trap.

## Output README Structure

```markdown
# Figures Extracted from <filename>

Total figures: N (M panels)

## Source

Extracted from `<path>` on YYYY-MM-DD. Original images were embedded as EMF (Enhanced Metafile) format. Each EMF was converted to PNG at 300 DPI for LaTeX use.

## Files

| File | Content | Original | rId | Position |
|------|---------|----------|-----|----------|
| ...  | ...     | ...      | ... | ...      |

## Figure 1 Caption (from document)

> <full caption text>

## LaTeX Usage

```latex
<ready-to-paste snippet>
```
```

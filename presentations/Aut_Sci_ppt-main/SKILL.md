---
name: aut-sci-ppt
description: Use when converting academic paper PDFs or structured text into professional, high-standard PowerPoint (PPTX) presentations for defense or seminars.
---

# Aut_Sci_PPt (Academic Auto-PPT Agent)

A specialized tool for generating professional academic presentations directly from paper content or structured outlines.

## Core Behavioral Rules (The 13 Laws)

1. **Format**: Use `1. Title` for chapters and `- Point` for bullets.
2. **Markdown**: 🚫 DO NOT use `##` for slide titles; it is not recognized by the parser.
3. **Innovation**: Identify the core innovation of the paper and highlight it in **Red**.
4. **Imagery**: Use HD extraction (600 DPI) for figures; minimum width >= 300px.
5. **No Scrapping**: 🚫 PROHIBITED to scrap low-quality bitmaps from PDF streams.
6. **Formulas**: Render LaTeX formulas as high-quality transparent PNGs.
7. **Transparency**: All generated formula/media assets must have transparent backgrounds.
8. **Feedback**: Inform the user if an operation (like PDF parsing) will take >10 seconds.
9. **Final Output**: 🚫 DO NOT output intermediate Markdown; generate and provide the `.pptx` directly.
10. **Colors**: Use `#1E3A5F` (Primary Blue) and `#EE0000` (Highlight Red).
11. **Layout**: Ensure zero text-overflow or figure-text overlap.
12. **Professionalism**: Keep communication brief and technical; skip AI pleasantries.

## Usage

### Simple Text Input
```python
from aut_sci_ppt import create_ppt

create_ppt("""
主题：[Title]
申请人：[Name]
1. [Section Title]
- [Content]
""", "output.pptx")
```

### PDF to PPT (Academic Workflow)
```python
from aut_sci_ppt import PaperWorkflow

workflow = PaperWorkflow()
workflow.process_pdf("paper.pdf", output_pptx="seminar.pptx")
```

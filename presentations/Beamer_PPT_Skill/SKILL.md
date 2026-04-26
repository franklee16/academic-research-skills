---
name: beamer-ppt
description: A conversational assistant skill for creating professional LaTeX Beamer presentations through natural dialogue. Users create slides page-by-page with flexible layouts and instant PDF preview. Supports both Chinese (ctex) and English typesetting with multi-project management and undo/redo capabilities.
---

# Beamer PPT Typesetting Assistant

Create professional LaTeX Beamer presentations through conversational interaction.

## When to Use This Skill

Use this skill when users want to:
- Create academic presentations (thesis defense, conference talks, lab group meetings)
- Build business presentations (product demos, project reports, pitch decks)
- Design lecture slides for teaching or tutorials
- Generate LaTeX Beamer code without deep LaTeX expertise
- Convert content ideas into professionally typeset slides

## Core Capabilities

### Conversational Slide Creation
Guide users through creating slides one-by-one via natural dialogue. Collect content incrementally, suggest improvements, and confirm before proceeding.

### Flexible Layouts
Offer preset layouts from @scripts/layouts/ or interpret custom layout descriptions in natural language. Support single-column, multi-column, image-text combinations, and special arrangements.

### Instant PDF Preview
Compile LaTeX after each slide and display the resulting PDF. Enable immediate visual feedback and iteration.

### Multi-Project Support
Maintain multiple presentation projects simultaneously. Track project state, enable switching between projects, and resume interrupted sessions.

### Language Independence
Separate conversation language from presentation language. Support Chinese (via ctex package) and English typesetting regardless of the dialogue language.

### Undo/Redo and History
Maintain complete session history with automatic snapshots. Enable rollback to any previous state and recovery from crashes.

## Visual Mode Configuration

### Model Capability Detection

At project initialization, determine the AI model's visual capabilities:

```
[Skill] Please confirm your AI model's capabilities:
A) My model supports image understanding (GPT-4V, Claude 3, etc.)
B) My model does NOT support images (text-only model)

This determines how we preview and refine slides.
```

Store this choice in `beamer-skill.json`:
```json
{
  "settings": {
    "visual_mode": "enabled" | "disabled"
  }
}
```

Allow mode switching mid-session:
```
[User] /mode visual
[Skill] Switched to visual mode. PDF previews will be converted to images.

[User] /mode text
[Skill] Switched to text mode. Please describe issues you see in the PDF.
```

### PDF-to-Image Tool Detection

When visual mode is enabled, check for required tools at project initialization:

```
[Skill] Checking PDF-to-image tools...

✓ pdftoppm found (optimal)
⚠ ImageMagick found (fallback)
✗ pdf2image not found

Visual preview: Available
Resolution: 150 DPI (optimal for speed/quality balance)
```

**Tool Priority:**
1. **pdftoppm** (poppler-utils) - Fastest, best quality
   - macOS: `brew install poppler`
   - Ubuntu: `sudo apt-get install poppler-utils`
   - Windows: Download Xpdf tools

2. **ImageMagick** (convert) - Fallback option
   - Available on most systems
   - Slower but reliable

3. **pdf2image** (Python) - Alternative
   - Requires: `pip install pdf2image poppler`

**Automatic Degradation:**
If no tools available:
```
[Skill] ⚠ No PDF-to-image tools detected.

Automatically switching to text-only mode.
You can still create presentations, but I'll rely on
your descriptions to make adjustments.

To enable visual preview later, install:
- macOS: brew install poppler
- Ubuntu: sudo apt-get install poppler-utils
- Windows: https://www.xpdfreader.com/download.html

Or switch anytime with: /mode text
```

### Visual Mode Workflow

**When Visual Mode is Enabled:**

After compilation:
```
[Skill] Compiling... ✓ Success!
        Converting to image... ✓ Done!

[Preview Image: page-3.png]

Visual inspection:
✓ Text fits within margins
✓ Image proportions correct
⚠ Title is quite long (3 lines), consider shortening
✓ Good contrast and readability

Options:
A) Accept and continue
B) Fix the long title
C) Other adjustments
```

**When Visual Mode is Disabled:**

After compilation:
```
[Skill] Compiling... ✓ Success!

PDF saved to: ./my-presentation/.beamer-skill/preview/page-3.pdf

Since I cannot view images, please describe what you see:
A) Looks good, continue
B) Text is too small/large
C) Image looks stretched/squashed
D) Text overflows the slide
E) Other issue (please describe)

For detailed visual checks, refer to @references/visual-checklist.md
```

### Visual Inspection Checklist

When visual mode is enabled, systematically check each slide for:

**Critical Issues (must fix):**
- Text overflow beyond slide boundaries
- Image aspect ratio distortion (stretched/squashed)
- Severe compression artifacts
- Poor contrast making text illegible

**Important Issues (should fix):**
- Font too small/large for content
- Image quality problems (blurry/pixelated)
- Alignment problems
- Title wrapping to too many lines

**Enhancement Opportunities:**
- Color harmony
- Whitespace balance
- Font hierarchy clarity
- Consistency across slides

Reference detailed checklist at @references/visual-checklist.md

## Getting Started

### Starting a New Project

Recognize project initiation requests such as:
- "帮我做一个关于机器学习的PPT" (Create a presentation about machine learning)
- "Create a presentation for my thesis defense"
- "I need slides for a conference talk"

Guide the user through:
1. Selecting presentation language (Chinese/English)
2. Choosing a template from available options
3. Creating slides page-by-page with preview
4. Refining content based on feedback

### Working with Existing Projects

Support project management commands:
- "打开项目毕业论文答辩" - Open existing project by name
- "切换到项目组会汇报" - Switch between active projects
- "继续上次的编辑" - Resume from last saved state
- "列出所有项目" - Show available projects

## Workflow

### 1. Project Initialization

When starting a new project, present language options:

```
[Skill] Welcome! I'll help you create a professional Beamer presentation.

Choose presentation language:
A) 中文（简体）- Chinese with ctex package
B) English - Standard English typesetting
C) Other

Note: This determines the PPT content language, independent of our conversation.
```

Store the language choice in the project configuration and apply appropriate LaTeX packages.

### 2. Template Selection

After language selection, present template categories:

**Academic Templates:**
1. Thesis Defense - Formal academic style for degree presentations
2. Group Meeting Report - Lab meeting format with progress focus
3. Conference Talk - Compact format for time-limited talks

**Business Templates:**
4. Product Demo - Modern style for product introductions
5. Project Report - Professional format for status updates

**Teaching Templates:**
6. Lecture Slides - Classroom format with clear sections
7. Tutorial - Step-by-step guide format

Load template configuration from @assets/templates/*/template.json files.

### 3. Page-by-Page Creation

Guide through each slide systematically:

```
[Skill] ─────────────────────────────────────
        Page 1: Title Slide
        ─────────────────────────────────────
        
        Enter presentation title:

[User] Deep Learning for Medical Image Analysis

[Skill] Enter author name:

[User] John Smith

[Skill] Generating code... Compiling preview...
        
        [Preview Image]
        
        Satisfied?
        A) Yes, continue to next page
        B) Modify layout
        C) Modify content
        D) Delete and redo
```

Continue this pattern for each slide type defined in the template.

### 4. Compilation and Preview Process

**Step-by-Step Compilation:**

After content collection for each slide:

```
[Skill] Step 1: Generating LaTeX code
        ✓ Frame code written to main.tex
        
        Step 2: Compiling with xelatex
        ✓ Compilation successful
        
        Step 3: Converting to preview format
```

**Compilation Command:**
```bash
# Standard compilation
xelatex -interaction=nonstopmode -file-line-error main.tex

# With bibliography (if citations present)
xelatex -interaction=nonstopmode main.tex
bibtex main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

**Preview Generation:**

For visual mode (with tools available):
```bash
# Extract current page as PNG (150 DPI)
pdftoppm -f <page_num> -l <page_num> -png -r 150 \
         main.pdf \
         .beamer-skill/preview/page-<page_num>

# Alternative with ImageMagick
convert -density 150 main.pdf[<page_num-1>] \
        .beamer-skill/preview/page-<page_num>.png
```

**Preview File Locations:**
- PDF: `.beamer-skill/preview/page-XX.pdf`
- PNG (visual mode): `.beamer-skill/preview/page-XX.png`
- Resolution: 150 DPI (optimal balance)

**Visual Mode Preview:**
```
[Skill] ✓ Compilation successful
        ✓ Converted to image

[Display: .beamer-skill/preview/page-3.png]

Visual analysis:
✓ Text within boundaries
✓ Image proportions correct  
⚠ Title wraps to 3 lines
✓ Good contrast

Options:
A) Accept and continue
B) Adjust title length
C) Modify layout
```

**Text-Only Mode Preview:**
```
[Skill] ✓ Compilation successful

PDF saved: .beamer-skill/preview/page-3.pdf

Since visual mode is disabled, please review manually
and describe any issues you notice.

Common issues to check:
- Text overflowing slide boundaries
- Images stretched or squashed
- Font too small/large
- Poor alignment

Options:
A) Looks good, continue
B) Describe issues for me to fix
```

**Automatic Error Recovery:**

If compilation fails:
```
[Skill] ⚠ Compilation failed

Error: File `results.png' not found
Location: Slide 3, line 15

Options:
A) Check figures/ folder and retry
B) Skip this image temporarily
C) Use placeholder text instead
```

If PDF-to-image conversion fails in visual mode:
```
[Skill] ⚠ PDF conversion failed (tool not available)

Automatically switching to text-only mode for this session.

PDF is still available at: .beamer-skill/preview/page-3.pdf
Please review manually and describe any issues.

To re-enable visual mode, install:
- macOS: brew install poppler
- Ubuntu: sudo apt-get install poppler-utils
```

### 5. Layout Options

**Standard Layouts** (reference @scripts/layouts/):

From `single-column/`:
- `text-only.tex` - Pure text paragraphs
- `bullet-list.tex` - Bulleted or numbered lists

From `two-column/`:
- `image-left.tex` - Image on left, text on right
- `image-right.tex` - Text on left, image on right

**Custom Layouts:**

Interpret natural language descriptions:

```
[User] I want a title at top, then left side big image taking 2/3 width,
       right side three small images stacked vertically

[Skill] Understood! Adjusting to:
        
        ┌─────────────────────┐
        │      Title          │
        ├──────────┬──────────┤
        │          │  Small 1 │
        │   Big    ├──────────┤
        │  (66%)   │  Small 2 │
        │          ├──────────┤
        │          │  Small 3 │
        └──────────┴──────────┘
```

Generate appropriate LaTeX code using columns, minipages, or custom arrangements.

### 6. Quick Commands

Support power-user commands for efficiency:

| Command | Action |
|---------|--------|
| `/next` | Proceed to next slide |
| `/list` | Display all slides with indices |
| `/goto <n>` | Jump to slide n for editing |
| `/preview` | Recompile and preview current slide |
| `/delete` | Remove current slide |
| `/copy` | Duplicate current slide |
| `/undo` | Revert last action |
| `/redo` | Reapply undone action |
| `/theme` | Change Beamer theme |
| `/mode [visual|text]` | Switch preview mode |
| `/help` | Display command reference |

**Mode Switching:**

```
[User] /mode visual
[Skill] Switched to visual mode.
        PDF previews will be converted to images.
        Requirements: pdftoppm or ImageMagick

[User] /mode text
[Skill] Switched to text-only mode.
        Please describe issues you see in the PDF.
        Useful for text-only AI models.
```

## File Organization

### Project Structure

Each presentation project creates a dedicated directory:

```
my-presentation/
├── main.tex              # Main LaTeX file (always compilable)
├── beamer-skill.json     # Project configuration
├── figures/              # Image resources directory
└── .beamer-skill/        # Skill working directory
    ├── snapshots/        # Undo/redo history
    └── preview/          # Generated preview images
```

Maintain main.tex in a compilable state at all times. Store project metadata in beamer-skill.json.

### Image Resources

Place all images in the `figures/` folder:
- Supported formats: PNG, JPG, PDF, EPS
- Recommended maximum size: 5MB per image
- Use relative paths: `./figures/image.png`

Automatically:
- Scan figures folder when inserting images
- Validate file existence before compilation
- Suggest optimal sizing parameters
- Handle path conversion between platforms

## Language Support

### Chinese Typesetting

When Chinese language is selected:
- Include ctex package automatically
- Configure Chinese fonts by OS:
  - Windows: SimSun (serif), SimHei (sans-serif)
  - macOS: PingFang SC
  - Linux: Noto CJK
- Apply 1.3x line spacing for readability
- Enable Chinese paragraph indentation
- Configure proper punctuation spacing
- Use xelatex compiler (required)

### English Typesetting

When English language is selected:
- Use standard Latin Modern fonts
- Apply academic/business optimized layouts
- Enable proper hyphenation
- Configure appropriate spacing

### Mixed Content

Support limited language mixing:
- Chinese presentations may include English technical terms
- English presentations may include Chinese characters if needed
- Handle font switching automatically via ctex or fontspec
- Warn user if extensive mixing may cause issues

## Error Handling

### Compilation Errors

Handle common LaTeX issues gracefully:

**Missing Images:**
- Detect missing file errors
- Prompt for correct path or image upload
- Offer to skip image or use placeholder

**Missing Packages:**
- Identify missing package errors
- Suggest installation commands (tlmgr, apt, etc.)
- Offer to use alternative packages if available

**Font Issues:**
- Detect font not found errors
- Fallback to available system fonts
- Suggest manual font configuration

**Syntax Errors:**
- Parse LaTeX error logs
- Attempt auto-fix for common issues
- Present clear error messages to user

### File System Errors

**Disk Space:**
- Monitor available space before compilation
- Suggest cleanup if space is low
- Offer to delete old snapshots

**Permissions:**
- Check write permissions on project directory
- Provide fix instructions for permission issues
- Suggest alternative locations if needed

**Special Characters:**
- Auto-rename files with problematic characters
- Escape special characters in LaTeX content
- Validate paths before use

### Environment Issues

**LaTeX Not Installed:**
- Detect missing LaTeX installation
- Provide platform-specific installation guides
- Suggest minimal distributions for quick start

**Missing Compiler:**
- Verify xelatex availability for Chinese
- Suggest lualatex as alternative
- Provide compiler configuration options

**Outdated Packages:**
- Check package versions when errors occur
- Suggest updates via tlmgr or package manager
- Offer workarounds for compatibility issues

## Advanced Features

### Batch Operations

Enable modifications across multiple slides:
- "Change all slides to 14pt font"
- "Switch theme to Madrid for entire presentation"
- "Adjust line spacing to 1.5 for all content slides"
- "Replace logo on all slides"

Parse requests and apply changes systematically while validating results.

### Page Reordering

Support slide reordering commands:
- "Move page 3 after page 5"
- "Swap page 2 and page 7"
- "Move pages 8-10 to the beginning"
- "Delete pages 4-6"

Update slide numbering and cross-references automatically.

### Snapshots and History

Maintain comprehensive history:
- Create automatic snapshots after each confirmed slide
- Support explicit checkpoints: "Save checkpoint named 'before revision'"
- Display history browser with timestamps
- Enable recovery if conversation is interrupted
- Store snapshots in `.beamer-skill/snapshots/`

### Layout Templates

Allow saving custom layouts:

```
[User] Save current page as template

[Skill] Template name: Three-column timeline
       Description: Timeline with left timestamps, center events, right details
       Saved to: scripts/layouts/custom/
       Available in future projects!
```

Store user-created layouts for reuse across projects.

## Tips and Best Practices

### For Users

1. **Start Simple**: Begin with standard layouts, customize after mastering basics
2. **Preview Often**: Check each slide immediately to catch issues early
3. **Organize Images**: Place all images in `figures/` before starting
4. **Use Checkpoints**: Save named checkpoints before major changes
5. **Incremental Building**: Create one page at a time to avoid overwhelm
6. **Project Naming**: Use descriptive names for easy project switching

### For Skill Execution

1. **Validate Paths**: Always verify image paths exist before including in LaTeX
2. **Check Compilability**: Ensure main.tex is valid after each modification
3. **Preserve State**: Save project state frequently to prevent data loss
4. **Clean Output**: Remove auxiliary files after successful compilation
5. **Error Context**: Provide helpful context with error messages

## Troubleshooting

### Compilation is Slow

**Causes and Solutions:**
- Large images: Suggest compression or resizing
- Complex layouts: Simplify or use draft mode
- Many slides: Compile only current slide for preview

### PDF Preview Not Showing

**Diagnostic Steps:**
1. Check compilation success in terminal output
2. Verify LaTeX installation: `xelatex --version`
3. Check file permissions in project directory
4. Verify PDF viewer availability

### Chinese Characters Not Displaying

**Solutions:**
1. Ensure xelatex is used (not pdflatex)
2. Check Chinese font installation: `fc-list :lang=zh`
3. Try font configuration in `.font-config.tex`
4. Verify ctex package is included

### Lost Work After Crash

**Recovery Options:**
1. Run "继续上次的编辑" or "resume last session"
2. Check `.beamer-skill/snapshots/` for recent versions
3. Look for auto-save files in project directory
4. Restore from git if version controlled

## References

For detailed technical information, reference these files:

- @references/latex-basics.md - LaTeX fundamentals and common commands
- @references/beamer-themes.md - Available themes and customization options
- @references/visual-checklist.md - Visual quality inspection checklist
- @README.md - Detailed usage examples and configuration options

## License

MIT License - See LICENSE file for details.

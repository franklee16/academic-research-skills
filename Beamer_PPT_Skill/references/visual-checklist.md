# Visual Checklist for Beamer Slides

This reference provides a comprehensive checklist for visual quality inspection of Beamer presentation slides.

## Overview

When reviewing a slide visually, check the following categories:
1. Text readability and overflow
2. Image quality and positioning
3. Layout alignment and spacing
4. Overall visual balance

---

## Text Issues

### 1. Text Overflow (Critical)

**Check:** Does any text extend beyond the slide boundaries?

**Signs:**
- Words cut off at edges
- Text extending into margins
- Bullet points truncated
- Long words not hyphenated properly

**Common Causes:**
- Font size too large for content amount
- Too much text on one slide
- Table columns too wide
- Image taking too much space

**Solutions:**
- Reduce font size
- Split content across multiple slides
- Adjust column widths
- Shorten text

### 2. Font Size Issues

**Too Small:**
- Body text below 10pt (hard to read when projected)
- Bullet points illegible from back of room
- Footnotes microscopic

**Too Large:**
- Headlines wrapping awkwardly
- Only 2-3 words per line
- Excessive whitespace

**Recommended Sizes:**
- Title: 18-24pt
- Frame title: 14-18pt
- Body text: 11-14pt
- Footnotes: 8-10pt

### 3. Line Spacing (Leading)

**Too Tight:**
- Lines touching or overlapping
- Descenders hitting ascenders
- Dense, hard-to-read blocks

**Too Loose:**
- Excessive white space between lines
- Text appears fragmented
- Wastes vertical space

**Optimal:**
- 1.2-1.5x line spacing for body text
- 1.0x for compact lists
- Beamer default is usually good

### 4. Text-Background Contrast

**Poor Contrast:**
- Light gray on white
- Dark blue on black
- Yellow on white
- Red on blue (vibration)

**Good Contrast:**
- Black on white (maximum)
- White on dark backgrounds
- Dark colors on light backgrounds
- Avoid pure white on pure black (harsh)

### 5. Title Issues

**Too Long:**
- Title wraps to 3+ lines
- Title font reduced automatically
- Overwhelms the slide

**Too Short:**
- Vague one-word titles
- Doesn't describe content

**Best Practice:**
- 1-2 lines maximum
- Concise but descriptive
- 6-10 words ideal

### 6. Bullet Point Hierarchy

**Unclear Levels:**
- All bullets look identical
- Can't distinguish main vs. sub points
- Inconsistent indentation

**Fixes:**
- Use different bullet styles (• → ○ → ▪)
- Ensure consistent indentation (2em per level)
- Limit to 2-3 levels deep

---

## Image Issues

### 1. Compression Artifacts (Critical)

**Signs:**
- Blocky patterns in smooth areas
- Color banding in gradients
- JPEG artifacts around edges
- Loss of fine detail

**Solutions:**
- Use PNG for diagrams/screenshots
- Use JPEG quality 90+ for photos
- Use PDF for vector graphics
- Avoid re-saving JPEGs multiple times

### 2. Aspect Ratio Distortion (Critical)

**Signs:**
- Circles appear as ovals
- Squares appear as rectangles
- People look stretched/squashed
- Text in images distorted

**Causes:**
- Width specified without height
- Different aspect ratio forced
- `keepaspectratio=false`

**Fix:**
```latex
% Good - maintains aspect ratio
\includegraphics[width=0.5\textwidth]{image.png}

% Bad - may distort
\includegraphics[width=0.5\textwidth,height=5cm]{image.png}

% Good - explicit keepaspectratio
\includegraphics[width=0.5\textwidth,height=5cm,keepaspectratio]{image.png}
```

### 3. Image Quality

**Blurry:**
- Resolution too low for display size
- Upscaling small images
- Compression artifacts

**Pixelated:**
- Image resolution too low
- Excessive zoom
- Wrong format for content type

**Solutions:**
- Use images at least 150 DPI for target display size
- For full-screen images: 1920x1080 minimum
- Vector formats (PDF, SVG, EPS) for diagrams
- High-resolution PNG for screenshots

### 4. Image Positioning

**Overlapping Text:**
- Image covers bullet points
- Caption overlapped
- Title obscured

**Poor Placement:**
- Image floating in whitespace
- Not aligned with text
- Too small/large relative to text

**Fixes:**
- Use `columns` environment for side-by-side
- Adjust image size to fit available space
- Ensure adequate margins

### 5. Image-Text Balance

**Image Dominates:**
- Image takes 80%+ of slide
- Text squeezed to small area
- Looks like just an image

**Text Dominates:**
- Tiny image in corner
- Image not noticeable
- Might as well be text-only

**Optimal:**
- 40-60% split for two-column layouts
- Full-screen images only when appropriate
- Text should complement image, not compete

---

## Layout Issues

### 1. Alignment

**Left/Right Misalignment:**
- Images not aligned with text blocks
- Multiple items at different horizontal positions
- Inconsistent margins

**Vertical Misalignment:**
- Top of image not aligned with top of text
- Baselines of text don't match
- Columns start at different heights

**Fix:**
```latex
% Use [T] for top alignment
\begin{columns}[T]
\column{0.5\textwidth}
\column{0.5\textwidth}
\end{columns}
```

### 2. Margins

**Too Small:**
- Text right against edge
- Looks cramped
- Risk of being cut off when printed

**Too Large:**
- Wasted space
- Content too small
- Looks unprofessional

**Beamer Defaults:**
- Usually appropriate
- Can adjust with `\setbeamersize`

### 3. Column Spacing

**Too Narrow:**
- Columns touching
- No visual separation
- Confusing to read

**Too Wide:**
- Excessive white space
- Columns feel disconnected
- Wastes horizontal space

**Standard:**
- Beamer's `columns` environment handles this well
- Default spacing usually good

### 4. Centering

**Off-Center:**
- Content visibly not centered
- Asymmetric whitespace
- Looks unbalanced

**Should Be Left-Aligned:**
- Body text should be left-aligned (not centered)
- Centered text harder to read
- Reserve centering for titles/special emphasis

### 5. Whitespace

**Too Crowded:**
- No breathing room
- Text right against images
- Margins too small
- Looks amateur

**Too Sparse:**
- Excessive empty space
- Content looks lost
- Suggests incomplete slide

**Optimal:**
- Adequate margins around all elements
- Consistent spacing
- Visual hierarchy clear

---

## Overall Visual Issues

### 1. Color Harmony

**Clashing Colors:**
- Red text on green background (Christmas effect)
- Bright colors fighting for attention
- Background and text too similar

**Monotonous:**
- Everything same color
- No visual hierarchy
- Boring to look at

**Best Practices:**
- Use theme colors consistently
- Limit palette to 3-4 main colors
- Ensure sufficient contrast
- Test on projector (colors differ from screen)

### 2. Font Hierarchy

**Flat:**
- Everything same size/weight
- No distinction between title/body
- Hard to parse visually

**Too Many Fonts:**
- Mixing 3+ font families
- Inconsistent styling
- Looks unprofessional

**Optimal:**
- Clear size progression: Title > Heading > Body > Footnote
- Bold for emphasis
- Italic for definitions/terms
- One font family (Beamer handles this)

### 3. Page Balance

**Top-Heavy:**
- Everything crammed at top
- Bottom empty
- Feels unstable

**Bottom-Heavy:**
- Content at bottom
- Top empty
- Unusual, distracting

**Left-Heavy (for LTR languages):**
- All content on left
- Right side empty
- Wastes space

**Optimal:**
- Visual weight distributed
- Follow reading pattern (top-to-bottom, left-to-right)
- Use columns for horizontal balance

### 4. Consistency

**Inconsistent:**
- Different bullet styles
- Varying image sizes
- Mix of centered and left-aligned
- Changing font sizes arbitrarily

**Importance:**
- Professional look
- Easier to follow
- Predictable layout

**Fix:**
- Use same layout patterns
- Define styles and stick to them
- Let Beamer themes handle consistency

### 5. Content Density

**Overcrowded:**
- 10+ bullet points
- Multiple images + text
- Font reduced to fit
- Audience can't process

**Underutilized:**
- Single sentence
- One small image
- Could be combined with next slide
- Wastes opportunity

**Sweet Spot:**
- 3-5 main points per slide
- One main concept per slide
- Room to breathe
- Amplifies spoken content

---

## Quick Reference: Priority Levels

### 🔴 Critical (Must Fix)
1. Text overflow/cutoff
2. Aspect ratio distortion
3. Compression artifacts
4. Poor contrast (illegible)

### 🟡 Important (Should Fix)
5. Font size issues
6. Image quality problems
7. Alignment problems
8. Title too long

### 🟢 Nice to Have (Fix if Time)
9. Color harmony
10. Whitespace balance
11. Font hierarchy refinement
12. Consistency improvements

---

## Review Process

**For Each Slide:**
1. 🔍 First glance: Overall impression
2. 📐 Check layout: Alignment, spacing, balance
3. 📝 Check text: Overflow, size, contrast, title
4. 🖼️ Check images: Quality, aspect ratio, position
5. 🎨 Check visuals: Color, hierarchy, consistency

**Common Fixes:**
- Reduce text
- Increase font size
- Check image aspect ratio
- Adjust column widths
- Shorten title
- Add whitespace

---

## Platform-Specific Notes

### Projectors vs. Screens
- Projectors have lower contrast
- Colors appear washed out
- Text needs to be larger
- Test on actual projector if possible

### Printouts
- May cut off edges
- Color rendering different
- Higher resolution needed
- Check margins

### Digital Distribution
- Viewers may zoom in
- Ensure text legible at 100%
- High-res images important
- PDF quality matters

---

## Tools for Checking

### Manual Review
- View at 100% zoom
- Check at presentation resolution
- View from distance (simulates projector)
- Print and review

### Automated (Limited)
- Text overflow detection
- Color contrast checkers
- Resolution analysis
- No replacement for human eye

---

## Summary

**Remember:**
- Content readability is paramount
- Consistency creates professionalism
- White space is your friend
- Less is usually more
- Test on actual presentation equipment

**When in Doubt:**
- Simplify
- Enlarge
- Add space
- Reduce text
- Prioritize clarity over decoration

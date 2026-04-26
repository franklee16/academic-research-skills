# Beamer Themes Reference

Complete reference guide for Beamer themes, color schemes, and customization options.

## Built-in Themes

### Modern Themes

#### metropolis (Recommended)
Clean, modern design suitable for academic and business presentations.

```latex
\usetheme{metropolis}
\metroset{
    background=light,      % light or dark
    titleformat=regular,   % regular, smallcaps, etc.
    sectionpage=progressbar % Shows progress bar on section pages
}
```

**Features:**
- Minimal design with focus on content
- Modern typography (Fira fonts)
- Progress bar support
- Highly customizable
- Works well with both light and dark backgrounds

**Best for:** Academic talks, conference presentations, business pitches

---

#### Madrid (Classic Academic)
Traditional academic look with navigation bars.

```latex
\usetheme{Madrid}
\usecolortheme{whale}  % or beaver, dolphin, etc.
```

**Features:**
- Navigation bars at top and bottom
- Section and subsection indicators
- Author and title in header
- Page numbers in footer

**Best for:** Formal academic presentations, thesis defenses

---

#### Berlin
Tree-like navigation structure ideal for long presentations.

```latex
\usetheme{Berlin}
```

**Features:**
- Hierarchical navigation showing all sections
- Mini frames for slide navigation
- Good for presentations with many sections

**Best for:** Long presentations, tutorials with multiple parts

---

#### CambridgeUS
Clean academic style without navigation bars.

```latex
\usetheme{CambridgeUS}
```

**Features:**
- Simple header with title and date
- Clean footer with frame numbers
- No side navigation (maximizes content space)
- Professional academic appearance

**Best for:** Conference talks, research presentations

---

### Simple Themes

#### default
Minimal styling - good starting point for custom themes.

```latex
\usetheme{default}
```

**Features:**
- Basic frame layout
- Minimal styling
- Maximum flexibility for customization

**Best for:** Custom theme development

---

#### boxes
Boxed layout with clean appearance.

```latex
\usetheme{boxes}
\usecolortheme{seahorse}
```

**Features:**
- Content in framed boxes
- Clean separation between sections
- Good for structured content

**Best for:** Technical documentation, structured presentations

---

#### Pittsburgh
Very minimal theme with just frame title.

```latex
\usetheme{Pittsburgh}
```

**Features:**
- No headers or footers
- Just frame title
- Maximum content space

**Best for:** Maximum content visibility, custom styling

---

### Additional Themes

#### Copenhagen
Navigation bars with sections and subsections.

```latex
\usetheme{Copenhagen}
```

#### Darmstadt
Shadow-based design with smooth gradients.

```latex
\usetheme{Darmstadt}
```

#### Dresden
Similar to Darmstadt but without shadows.

```latex
\usetheme{Dresden}
```

#### Frankfurt
Navigation at top with sections.

```latex
\usetheme{Frankfurt}
```

#### Ilmenau
Combination of Darmstadt and tree navigation.

```latex
\usetheme{Ilmenau}
```

#### Luebeck
Tree navigation with circles.

```latex
\usetheme{Luebeck}
```

#### Malmoe
Minimal design with navigation.

```latex
\usetheme{Malmoe}
```

#### Montpellier
Clean design with navigation tree.

```latex
\usetheme{Montpellier}
```

#### PaloAlto
Sidebar with table of contents.

```latex
\usetheme{PaloAlto}
```

#### Rochester
Minimal theme with square corners.

```latex
\usetheme{Rochester}
```

#### Singapore
Table of contents in headline.

```latex
\usetheme{Singapore}
```

#### Szeged
Navigation bars with heavy lines.

```latex
\usetheme{Szeged}
```

#### Warsaw
Shadowed navigation bars.

```latex
\usetheme{Warsaw}
```

---

## Color Themes

### Built-in Color Themes

```latex
\usecolortheme{default}      % Blue-based (standard)
\usecolortheme{albatross}    % Dark blue background
\usecolortheme{beaver}       % Red-based
\usecolortheme{beetle}       % Gray with black structure
\usecolortheme{crane}        % Orange-based
\usecolortheme{dolphin}      % Blue-green contrast
\usecolortheme{dove}         % Grayscale
\usecolortheme{fly}          % Dark gray background
\usecolortheme{lily}         % White with structure color
\usecolortheme{monarca}      % Yellow-brown (bee colors)
\usecolortheme{orchid}       % Dark with structure color
\usecolortheme{rose}         % Light with structure color
\usecolortheme{seagull}      % Light grayscale
\usecolortheme{seahorse}     % Light blue-green
\usecolortheme{sidebartab}   % Enhanced sidebar colors
\usecolortheme{spruce}       % Green-based
\usecolortheme{structure}    % Use structure color
\usecolortheme{whale}        % Deep blue
\usecolortheme{wolverine}    % Yellow-brown (Michigan colors)
```

### Color Theme Descriptions

| Theme | Primary Colors | Best For |
|-------|---------------|----------|
| default | Blue | General purpose |
| albatross | Dark blue | Dark presentations |
| beaver | Red | Attention-grabbing |
| crane | Orange | Energetic presentations |
| dolphin | Blue-green | Professional, calm |
| dove | Gray | Minimal, serious |
| seahorse | Light blue | Academic, clean |
| spruce | Green | Nature, environmental |
| whale | Deep blue | Corporate, formal |
| wolverine | Yellow-brown | Distinctive branding |

---

## Font Themes

### Available Font Themes

```latex
\usefonttheme{default}              % sans-serif (default)
\usefonttheme{professionalfonts}    % Use package fonts (no changes)
\usefonttheme{serif}                % Serif fonts
\usefonttheme{structurebold}        % Bold titles
\usefonttheme{structureitalicserif} % Italic serif structure
\usefonttheme{structuresmallcapsserif} % Small caps for structure
```

### Font Theme Features

**default:**
- Uses sans-serif fonts
- Modern appearance
- Good for presentations

**serif:**
- Uses serif fonts (like Times)
- Traditional, academic look
- Good for text-heavy slides

**professionalfonts:**
- Does not change fonts
- Allows manual font configuration
- Use with font packages

**structurebold:**
- Bold structure elements
- Strong visual hierarchy
- Good for emphasizing sections

---

## Inner Themes (Frame Layout)

Inner themes control the appearance of frame contents.

```latex
\useinnertheme{default}     % Standard bullets and blocks
\useinnertheme{circles}     % Circular bullets
\useinnertheme{rectangles}  % Square/rectangular bullets
\useinnertheme{rounded}     % Rounded boxes and shadows
\useinnertheme{inmargin}    % Items in margin
```

### Inner Theme Features

**default:**
- Triangular bullets
- Standard blocks
- Simple enumeration

**circles:**
- Circular bullets
- Modern appearance
- Good with metropolis

**rectangles:**
- Square bullets
- Clean, structured look
- Works with most themes

**rounded:**
- Rounded corners on blocks
- Shadows for depth
- Soft, modern appearance

**inmargin:**
- Items placed in margins
- Unique layout
- Good for specific designs

---

## Outer Themes (Navigation)

Outer themes control headers, footers, and sidebars.

```latex
\useoutertheme{default}     % No navigation
\useoutertheme{infolines}   % Title + author + page info
\useoutertheme{miniframes}  % Mini frame navigation
\useoutertheme{smoothbars}  % Smooth navigation bars
\useoutertheme{sidebar}     % Sidebar navigation
\useoutertheme{split}       % Split header/footer
\useoutertheme{shadow}      % Shadow boxes
\useoutertheme{tree}        % Tree navigation (sections/subsections)
\useoutertheme{smoothtree}  % Smooth tree navigation
```

### Outer Theme Features

**default:**
- No navigation elements
- Just frame title
- Maximum content space

**infolines:**
- Shows author, title, date in header
- Shows page numbers in footer
- Good for short presentations

**miniframes:**
- Mini navigation circles
- Shows current position
- Good for long presentations

**sidebar:**
- Left or right sidebar
- Shows sections
- Good for navigation

**split:**
- Header shows sections
- Footer shows title/page
- Clean separation

---

## Theme Combinations

### Academic Presentation
Classic academic look with clean colors.

```latex
\usetheme{Madrid}
\usecolortheme{seahorse}
\usefonttheme{professionalfonts}
\useinnertheme{circles}
```

**Characteristics:**
- Professional academic appearance
- Blue-green color scheme
- Clean navigation
- Good for conferences

---

### Business Presentation
Modern dark theme for business pitches.

```latex
\usetheme{metropolis}
\metroset{background=dark}
\usecolortheme{default}
\usefonttheme{default}
```

**Characteristics:**
- Dark background (focus on content)
- Modern typography
- Professional appearance
- Good for product demos

---

### Minimal Presentation
Maximum content space with minimal decoration.

```latex
\usetheme{default}
\usecolortheme{dove}
\useoutertheme{infolines}
\useinnertheme{rectangles}
```

**Characteristics:**
- Minimal styling
- Grayscale colors
- Clean and serious
- Good for technical talks

---

### Colorful Presentation
Vibrant colors for engaging presentations.

```latex
\usetheme{CambridgeUS}
\usecolortheme{dolphin}
\useinnertheme{circles}
\usefonttheme{structurebold}
```

**Characteristics:**
- Blue-green color scheme
- Bold structure
- Eye-catching but professional
- Good for teaching

---

### Corporate Presentation
Professional look for company presentations.

```latex
\usetheme{Madrid}
\usecolortheme{whale}
\usefonttheme{serif}
\useoutertheme{infolines}
```

**Characteristics:**
- Deep blue colors
- Serif fonts for authority
- Clean navigation
- Good for business reports

---

### Creative Presentation
Modern and distinctive for creative industries.

```latex
\usetheme{metropolis}
\metroset{background=light}
\usecolortheme{crane}
\useinnertheme{rounded}
```

**Characteristics:**
- Light background
- Orange accents
- Rounded elements
- Good for creative portfolios

---

## Customization

### Custom Colors

Define and use custom colors:

```latex
% RGB colors
\definecolor{myblue}{RGB}{0, 102, 204}
\definecolor{myred}{RGB}{204, 51, 51}
\definecolor{mygreen}{RGB}{51, 153, 102}

% HTML colors (hex)
\definecolor{myorange}{HTML}{FF6600}
\definecolor{mypurple}{HTML}{663399}

% Apply to theme elements
\setbeamercolor{title}{fg=myblue}
\setbeamercolor{frametitle}{fg=myblue,bg=white}
\setbeamercolor{structure}{fg=myblue}
\setbeamercolor{block title}{bg=myblue,fg=white}
\setbeamercolor{block body}{bg=myblue!10,fg=black}
```

### Hide Navigation Symbols

Remove navigation icons from PDF:

```latex
\beamertemplatenavigationsymbolsempty
```

Or in preamble:

```latex
\setbeamertemplate{navigation symbols}{}
```

### Custom Footer

Customize footer content:

```latex
% Simple page numbers
\setbeamertemplate{footline}{
    \hfill\insertframenumber/\inserttotalframenumber\hspace{2em}\vspace{1em}
}

% Footer with author and title
\setbeamertemplate{footline}{
    \leavevmode%
    \hbox{%
    \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,center]{author in head/foot}%
        \usebeamerfont{author in head/foot}\insertshortauthor
    \end{beamercolorbox}%
    \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,center]{title in head/foot}%
        \usebeamerfont{title in head/foot}\insertshorttitle
    \end{beamercolorbox}%
    \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,right]{date in head/foot}%
        \usebeamerfont{date in head/foot}\insertshortdate{}\hspace*{2em}
        \insertframenumber{} / \inserttotalframenumber\hspace*{2ex} 
    \end{beamercolorbox}}%
    \vskip0pt%
}
```

### Custom Itemize Styles

Change bullet point styles:

```latex
% Different bullet shapes
\setbeamertemplate{itemize items}[default]  % Triangle
\setbeamertemplate{itemize items}[circle]   % Circle
\setbeamertemplate{itemize items}[square]   % Square
\setbeamertemplate{itemize items}[ball]     % Ball

% Sub-item styles
\setbeamertemplate{itemize subitem}[circle]
\setbeamertemplate{itemize subsubitem}[square]
```

### Custom Enumerate Styles

Change numbering styles:

```latex
\setbeamertemplate{enumerate items}[default]     % 1, 2, 3
\setbeamertemplate{enumerate items}[circle]      % Circled numbers
\setbeamertemplate{enumerate items}[square]      % Boxed numbers
\setbeamertemplate{enumerate items}[ball]        % Balls with numbers
```

### Background Image

Add background image to all frames:

```latex
\setbeamertemplate{background}{
    \includegraphics[width=\paperwidth,height=\paperheight]{background.png}
}

% Or for specific frames only
{
\setbeamertemplate{background}{\includegraphics[width=\paperwidth]{bg.png}}
\begin{frame}
    % Content with background
\end{frame}
}
```

### Transparency/Overlay Effects

```latex
% Semi-transparent overlays
\setbeamercovered{transparent}

% Invisible overlays (default)
\setbeamercovered{invisible}

% Dynamic with high contrast
\setbeamercovered{dynamic}
```

---

## Aspect Ratios

Beamer supports multiple aspect ratios:

```latex
\documentclass[aspectratio=169]{beamer}  % 16:9 (modern widescreen)
\documentclass[aspectratio=43]{beamer}   % 4:3 (standard)
\documentclass[aspectratio=1610]{beamer} % 16:10 (common laptops)
\documentclass[aspectratio=149]{beamer}  % 14:9
\documentclass[aspectratio=141]{beamer}  % 1.41:1 (sqrt(2))
\documentclass[aspectratio=54]{beamer}   % 5:4
\documentclass[aspectratio=32]{beamer}   % 3:2
```

### Aspect Ratio Recommendations

| Ratio | Use Case | Notes |
|-------|----------|-------|
| 16:9 | Modern displays, projectors | Recommended for most presentations |
| 4:3 | Older projectors, conference rooms | Still widely used |
| 16:10 | Laptops, tablets | Good for screen sharing |
| 3:2 | Photography presentations | Matches camera sensors |

---

## Usage Recommendations

### By Presentation Type

**Academic Conference Talk:**
- Theme: metropolis or Madrid
- Color: seahorse or dolphin
- Font: professionalfonts
- Aspect: 16:9

**Thesis Defense:**
- Theme: CambridgeUS or Madrid
- Color: whale or seahorse
- Font: serif
- Aspect: 4:3 (traditional)

**Business Pitch:**
- Theme: metropolis
- Color: default or custom corporate colors
- Font: default
- Aspect: 16:9

**Teaching/Lecture:**
- Theme: CambridgeUS or Berlin
- Color: dolphin or spruce
- Font: structurebold
- Aspect: 16:9

**Product Demo:**
- Theme: metropolis
- Color: crane or custom brand colors
- Font: default
- Aspect: 16:9

### By Audience

**Technical Audience:**
- Clean, minimal themes
- dove or seagull colors
- Maximum content space

**Executive/Business:**
- Professional themes (Madrid, metropolis)
- whale or custom corporate colors
- Clear navigation

**Students/Education:**
- Colorful but not distracting
- dolphin or crane
- Good navigation for reference

**General Public:**
- Accessible, high contrast
- Avoid dark backgrounds
- Clear, large fonts

### Quick Selection Guide

**I want something modern and clean:**
```latex
\usetheme{metropolis}
\metroset{background=light}
```

**I need traditional academic:**
```latex
\usetheme{Madrid}
\usecolortheme{seahorse}
```

**I want maximum space for content:**
```latex
\usetheme{default}
\useoutertheme{infolines}
\beamertemplatenavigationsymbolsempty
```

**I'm doing a dark presentation:**
```latex
\usetheme{metropolis}
\metroset{background=dark}
```

**I need good navigation for long talks:**
```latex
\usetheme{Berlin}
\useoutertheme{miniframes}
```

---

## Complete Examples

### Example 1: Academic Conference

```latex
\documentclass[aspectratio=169,11pt]{beamer}

\usetheme{metropolis}
\metroset{
    background=light,
    titleformat=regular,
    sectionpage=progressbar
}
\usecolortheme{seahorse}
\usefonttheme{professionalfonts}

% Custom footer
\setbeamertemplate{footline}{
    \hfill\insertframenumber/\inserttotalframenumber\hspace{2em}\vskip2ex
}

\title{Deep Learning for Medical Image Analysis}
\author{John Smith}
\institute{University of Science}
\date{2026}

\begin{document}

\frame{\titlepage}

\begin{frame}{Outline}
\tableofcontents
\end{frame}

\section{Introduction}
\begin{frame}{Background}
\begin{itemize}
    \item Medical imaging generates vast amounts of data
    \item Manual analysis is time-consuming
    \item Deep learning offers automated solutions
\end{itemize}
\end{frame}

\end{document}
```

### Example 2: Business Presentation

```latex
\documentclass[aspectratio=169,12pt]{beamer}

\usetheme{Madrid}
\usecolortheme{whale}
\usefonttheme{structurebold}

% Custom colors
\definecolor{companyblue}{RGB}{0, 82, 165}
\setbeamercolor{structure}{fg=companyblue}
\setbeamercolor{block title}{bg=companyblue}

% Hide navigation
\beamertemplatenavigationsymbolsempty

\title{Product Launch Strategy}
\author{Marketing Team}
\institute{TechCorp Inc.}
\date{March 2026}

\begin{document}

\frame{\titlepage}

\begin{frame}{Market Overview}
\begin{columns}
\column{0.5\textwidth}
\begin{block}{Target Market}
\begin{itemize}
    \item Enterprise customers
    \item SMB segment
    \item Individual professionals
\end{itemize}
\end{block}

\column{0.5\textwidth}
\begin{alertblock}{Key Challenge}
    Intense competition from established players
\end{alertblock}
\end{columns}
\end{frame}

\end{document}
```

### Example 3: Minimal Presentation

```latex
\documentclass[aspectratio=43,11pt]{beamer}

\usetheme{default}
\usecolortheme{dove}
\useoutertheme{infolines}
\useinnertheme{rectangles}

% Minimal footer
\setbeamertemplate{footline}{
    \hfill\insertframenumber\hspace{2em}\vskip2ex
}

\beamertemplatenavigationsymbolsempty

\title{Algorithm Analysis}
\author{Research Team}
\date{\today}

\begin{document}

\frame{\titlepage}

\begin{frame}{Complexity Analysis}
\begin{block}{Time Complexity}
    $O(n \log n)$ for sorting phase
\end{block}

\begin{block}{Space Complexity}
    $O(n)$ additional space required
\end{block}
\end{frame}

\end{document}
```

---

## Tips and Best Practices

1. **Test on target display:** Always test your theme on the actual projector/screen you'll use

2. **Consider contrast:** Ensure text is readable from the back of the room

3. **Be consistent:** Use the same theme throughout your presentation

4. **Don't over-customize:** Too many custom colors can look unprofessional

5. **Check printing:** If handouts are needed, test how the theme prints

6. **Font sizes:** Larger fonts (11pt-14pt) are better for presentations

7. **Background images:** Keep them subtle if used at all

8. **Navigation:** Include navigation for long presentations, remove for short ones

9. **Color blindness:** Avoid red-green combinations

10. **Backup plan:** Have a plain version ready in case of technical issues

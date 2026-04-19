# Beamer PPT Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a comprehensive Beamer PPT typesetting skill that helps users create professional LaTeX Beamer presentations through conversational interaction, with support for multiple languages and reusable layout templates.

**Architecture:** The skill consists of SKILL.md (main instructions), README docs, reference materials for LaTeX/Beamer knowledge, template assets, and a library of reusable LaTeX layout scripts to save tokens during execution.

**Tech Stack:** Markdown documentation, LaTeX/Beamer templates, JSON configuration, YAML frontmatter

**Reference Design:** `docs/superpowers/specs/2026-03-22-beamer-ppt-skill-design.md`

---

## File Structure Overview

```
beamer-skill/
├── SKILL.md                     # Main skill file (required)
├── README.md                    # English documentation
├── README_zh.md                 # Chinese documentation
├── references/
│   ├── latex-basics.md         # LaTeX fundamentals
│   ├── beamer-themes.md        # Beamer theme reference
│   ├── layout-patterns.md      # Layout pattern library
│   └── chinese-typesetting.md  # Chinese typesetting guide
├── assets/
│   ├── templates/
│   │   ├── academic-thesis/
│   │   ├── business-report/
│   │   ├── course-lecture/
│   │   └── conference-talk/
│   └── examples/
│       ├── example-academic/
│       └── example-business/
└── scripts/
    └── layouts/                # Reusable LaTeX layout scripts
        ├── single-column/
        ├── two-column/
        ├── three-column/
        └── special/
```

---

## Phase 1: Core Skill File (SKILL.md)

### Task 1: Create SKILL.md with YAML Frontmatter

**Files:**
- Create: `SKILL.md`

- [ ] **Step 1: Create SKILL.md with proper YAML frontmatter**

```markdown
---
name: beamer-ppt
description: A conversational assistant skill for creating professional LaTeX Beamer presentations. Users can create slides page-by-page with flexible layouts, preview PDFs immediately, and manage multiple projects. Supports both Chinese and English with automatic typesetting optimization.
license: MIT
---

# Beamer PPT Typesetting Assistant

This skill helps you create professional LaTeX Beamer presentations through natural conversation.

## When to Use This Skill

Use this skill when you want to:
- Create academic presentations (thesis defense, conference talks, group meetings)
- Build business presentations (product demos, project reports)
- Design lecture slides for teaching
- Generate LaTeX Beamer code without deep LaTeX knowledge

## Core Capabilities

1. **Conversational Slide Creation**: Create slides one-by-one through guided conversation
2. **Flexible Layouts**: Choose from preset layouts or describe custom layouts in natural language
3. **Instant PDF Preview**: Compile and preview each slide immediately after creation
4. **Multi-Project Support**: Manage multiple presentation projects simultaneously
5. **Language Independence**: Choose PPT language (Chinese/English) separately from conversation language
6. **Undo/Redo**: Full session history with snapshots for easy rollback

## Getting Started

### Starting a New Project

Simply say something like:
- "帮我做一个关于机器学习的PPT" (I'll create Chinese or English based on your choice)
- "Create a presentation for my thesis defense"
- "I need slides for a conference talk"

The skill will guide you through:
1. Choosing the presentation language (Chinese/English)
2. Selecting a template (academic/business/teaching)
3. Creating slides page-by-page
4. Previewing and refining each page

### Working with Existing Projects

- "打开项目毕业论文答辩" - Open existing project
- "切换到项目组会汇报" - Switch between projects
- "继续上次的编辑" - Resume from last session

## Workflow

### 1. Project Initialization

When starting a new project:

```
[Skill] Welcome! I'll help you create a professional Beamer presentation.

Choose presentation language:
A) 中文（简体）- Chinese with ctex package
B) English - Standard English typesetting
C) Other

Note: This determines the PPT content language, independent of our conversation.
```

### 2. Template Selection

After choosing language:

```
[Skill] Select a template:

Academic:
1) Thesis Defense - For degree thesis presentations
2) Group Meeting Report - For lab group meetings
3) Conference Talk - For academic conferences

Business:
4) Product Demo - For product introductions
5) Project Report - For project presentations

Teaching:
6) Lecture Slides - For classroom teaching
7) Tutorial - For step-by-step guides
```

### 3. Page-by-Page Creation

The skill will guide you through each slide:

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
```

### 4. Layout Options

**Standard Layouts:**
- Single column (text, bullet list, numbered list)
- Two column (image left/right, two text blocks, two images)
- Three column (three images, mixed content)
- Special (full image, centered focus)

**Custom Layouts:**
Describe what you want in natural language:

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

### 5. Quick Commands

For experienced users:

| Command | Action |
|---------|--------|
| `/next` | Go to next slide creation |
| `/list` | Show all slides |
| `/goto <n>` | Jump to slide n |
| `/preview` | Recompile and preview current slide |
| `/delete` | Delete current slide |
| `/copy` | Copy current slide |
| `/undo` | Undo last action |
| `/redo` | Redo |
| `/theme` | Change theme |
| `/help` | Show help |

## File Organization

### Project Structure

Each project creates a directory:

```
my-presentation/
├── main.tex              # Main LaTeX file (always compilable)
├── beamer-skill.json     # Project configuration
├── figures/              # Put your images here
└── .beamer-skill/        # Skill working files
    ├── snapshots/        # Undo/redo history
    └── preview/          # Preview images
```

### Image Resources

Place all images in the `figures/` folder:
- Supported formats: PNG, JPG, PDF, EPS
- Recommended size: < 5MB per image
- Use relative paths: `./figures/image.png`

The skill will automatically:
- Scan the figures folder when inserting images
- Handle path conversion
- Suggest optimal image sizes

## Language Support

### Chinese Typesetting

When Chinese is selected:
- Automatic ctex package inclusion
- Chinese font configuration (SimSun/SimHei on Windows, PingFang on macOS, Noto on Linux)
- Optimized line spacing (1.3x)
- Chinese paragraph indentation
- Proper punctuation spacing

### English Typesetting

When English is selected:
- Standard Latin Modern fonts
- Academic/business optimized layouts
- Proper hyphenation and spacing

### Mixed Content

Even with a single language selection, limited mixing is supported:
- Chinese PPTs can include English terms
- English PPTs can include Chinese if needed
- The skill will handle font switching automatically

## Error Handling

The skill handles common issues:

**Compilation Errors:**
- Missing images → Prompt for correct path
- Missing packages → Suggest installation command
- Font issues → Fallback to available fonts
- Syntax errors → Attempt auto-fix

**File System Errors:**
- Disk space full → Suggest cleanup
- Permission denied → Provide fix instructions
- Special characters in filenames → Auto-rename

**Environment Issues:**
- LaTeX not installed → Provide installation guide
- Missing compiler → Suggest alternatives
- Outdated packages → Update suggestions

## Advanced Features

### Batch Operations

Modify multiple slides at once:
- "Change all slides to 14pt font"
- "Switch theme to Madrid for entire presentation"
- "Adjust line spacing to 1.5 for all content slides"

### Page Reordering

- "Move page 3 after page 5"
- "Swap page 2 and page 7"
- "Move pages 8-10 to the beginning"

### Snapshots and History

- Automatic snapshots after each confirmed page
- Explicit checkpoints: "Save checkpoint named 'before revision'"
- Full history browser with timestamps
- Cross-session recovery if conversation is interrupted

### Layout Templates

Save custom layouts for reuse:

```
[User] Save current page as template

[Skill] Template name: Three-column timeline
       Description: Timeline with left timestamps, center events, right details
       Saved to: scripts/layouts/custom/
       Available in future projects!
```

## Tips and Best Practices

1. **Start Simple**: Begin with standard layouts, customize later
2. **Preview Often**: Check each slide immediately to catch issues early
3. **Organize Images**: Put all images in `figures/` before starting
4. **Use Checkpoints**: Save named checkpoints before major changes
5. **Incremental Building**: One page at a time prevents overwhelm
6. **Project Naming**: Use descriptive names for easy switching

## Troubleshooting

**Compilation is slow:**
- Check image sizes (compress if > 5MB)
- Reduce number of complex layouts
- Use draft mode for previews

**PDF preview not showing:**
- Check if compilation succeeded (view logs)
- Verify LaTeX installation: `xelatex --version`
- Check file permissions in project directory

**Chinese characters not displaying:**
- Ensure xelatex is used (not pdflatex)
- Check if Chinese fonts are installed
- Try font configuration in `.font-config.tex`

**Lost work after crash:****
- Run "继续上次的编辑" to recover
- Check `.beamer-skill/snapshots/` for recent versions

## References

For detailed technical information:
- @references/latex-basics.md - LaTeX fundamentals
- @references/beamer-themes.md - Available themes and customization
- @references/layout-patterns.md - Layout pattern library
- @references/chinese-typesetting.md - Chinese typesetting details

## License

MIT License - See LICENSE file for details
```

- [ ] **Step 2: Verify SKILL.md format**

Run: `head -20 SKILL.md`
Expected: YAML frontmatter with `name:` and `description:` fields

- [ ] **Step 3: Commit SKILL.md**

```bash
git add SKILL.md
git commit -m "feat: create main SKILL.md with complete instructions"
```

---

## Phase 2: README Documentation

### Task 2: Create English README.md

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write comprehensive English README**

```markdown
# Beamer PPT Skill

A conversational AI skill for creating professional LaTeX Beamer presentations through natural dialogue.

## Features

- **Conversational Interface**: Create slides by talking naturally with AI
- **Flexible Layouts**: Choose from presets or describe custom layouts
- **Instant Preview**: Compile and view PDF immediately after each slide
- **Multi-Language Support**: Chinese (ctex) and English typesetting
- **Multi-Project**: Manage multiple presentations simultaneously
- **Undo/Redo**: Full session history with snapshots
- **Layout Templates**: Reusable LaTeX scripts for common layouts

## Quick Start

### Requirements

- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- xelatex compiler (for Chinese support)
- Python 3.7+ (optional, for helper scripts)

### Installation

1. Install this skill to your AI assistant's skill directory
2. Ensure LaTeX is installed on your system
3. Start creating presentations!

### Basic Usage

Simply start a conversation:
```
User: Help me create a presentation about machine learning

AI: Welcome! I'll help you create a professional Beamer presentation.
     
     Choose presentation language:
     A) Chinese (Simplified)  B) English  C) Other
     
     (This determines PPT content language, independent of our conversation)
```

## Project Structure

When you create a presentation, the skill generates:

```
my-presentation/
├── main.tex          # Main LaTeX file (always compilable)
├── beamer-skill.json # Project configuration
├── figures/          # Your images go here
└── .beamer-skill/    # Working files (snapshots, previews)
```

## Layout Scripts

The skill includes pre-built LaTeX layout templates in `scripts/layouts/`:

- **single-column/**: Text, bullet lists
- **two-column/**: Image left/right, two text blocks
- **three-column/**: Three images, mixed content
- **special/**: Full image, centered focus

These templates save tokens and ensure consistent, error-free code.

## Commands

Quick commands for power users:

| Command | Description |
|---------|-------------|
| `/next` | Continue to next slide |
| `/list` | List all slides |
| `/goto N` | Jump to slide N |
| `/preview` | Recompile current slide |
| `/undo` | Undo last action |
| `/help` | Show all commands |

## Examples

### Academic Presentation

```
User: Create a thesis defense presentation

AI: Choose language:
    A) Chinese  B) English

User: B

AI: Select template:
    1) Thesis Defense (formal academic)
    2) Conference Talk (shorter format)
    
User: 1

AI: [Guides through title, outline, chapters, content pages]
```

### Business Presentation

```
User: 帮我做一个产品介绍的PPT

AI: 请选择语言：A) 中文  B) English

User: A

AI: 选择模板：
    1) 产品发布会  2) 项目汇报  3) 培训课程
    
[Guides through creation in Chinese]
```

### Mixed Language Scenario

```
User: I need an English presentation for an international conference
       (我可以中文和你交流吗？)

AI: Of course! You can communicate in Chinese, and I'll generate English content.
     
     Selected: English presentation
     
     Enter title in English or Chinese (I'll translate):
     
User: 基于深度学习的图像识别

AI: Translated: "Image Recognition Based on Deep Learning"
     
     Continue in Chinese for all inputs...
```

## Configuration

### LaTeX Compiler

Default: `xelatex` (required for Chinese)

To use different compiler, specify during project creation or in `beamer-skill.json`:
```json
{
  "settings": {
    "compiler": "lualatex"
  }
}
```

### Chinese Fonts

Fonts are auto-detected by OS:
- **Windows**: SimSun (serif), SimHei (sans-serif)
- **macOS**: PingFang SC
- **Linux**: Noto CJK

Override by creating `.font-config.tex` in project root.

### Themes

Built-in Beamer themes supported:
- metropolis (modern, recommended)
- Madrid (classic academic)
- Berlin (navigation bars)
- CambridgeUS (clean academic)
- And more...

## Troubleshooting

### LaTeX Not Found

```bash
# macOS
brew install --cask mactex

# Ubuntu/Debian
sudo apt-get install texlive-full

# Windows
# Download from https://tug.org/texlive/
```

### Chinese Display Issues

1. Ensure xelatex is installed: `xelatex --version`
2. Check Chinese fonts: `fc-list :lang=zh`
3. Try manual font config in `.font-config.tex`

### Compilation Errors

Common fixes:
- Missing images → Check `figures/` folder
- Package not found → Run `tlmgr install <package>`
- Font issues → Use fallback fonts

## Development

### Project Structure

```
beamer-skill/
├── SKILL.md              # Main skill instructions
├── README.md             # This file
├── README_zh.md          # Chinese documentation
├── references/           # Technical references
│   ├── latex-basics.md
│   ├── beamer-themes.md
│   ├── layout-patterns.md
│   └── chinese-typesetting.md
├── assets/               # Templates and examples
│   ├── templates/
│   └── examples/
└── scripts/              # Reusable layout scripts
    └── layouts/
```

### Adding Layout Scripts

To add custom layouts:

1. Create `.tex` file in `scripts/layouts/custom/`
2. Use placeholders: `{{TITLE}}`, `{{CONTENT}}`, etc.
3. Add description comment at top
4. Restart skill to load

Example:
```latex
% Layout: Custom Timeline
% Description: Left timestamps, right events
% Placeholders: {{TITLE}}, {{EVENTS}}

\begin{frame}{{{TITLE}}}
{{EVENTS}}
\end{frame}
```

## Contributing

Contributions welcome! Areas for improvement:
- Additional layout templates
- More theme presets
- Better error handling
- Additional language support

## License

MIT License

## Acknowledgments

- Beamer class by Till Tantau
- ctex package by CTEX.org
- Metropolis theme by Matthias Vogelgesang
```

- [ ] **Step 2: Verify README.md content**

Run: `wc -l README.md`
Expected: >200 lines

- [ ] **Step 3: Commit README.md**

```bash
git add README.md
git commit -m "docs: add comprehensive English README"
```

---

### Task 3: Create Chinese README_zh.md

**Files:**
- Create: `README_zh.md`

- [ ] **Step 1: Write Chinese README**

```markdown
# Beamer PPT Skill

通过自然对话创建专业 LaTeX Beamer 演示文稿的 AI 助手。

## 功能特点

- **对话式交互**：通过自然语言与 AI 对话创建幻灯片
- **灵活布局**：选择预设布局或用自然语言描述自定义布局
- **即时预览**：每页完成后立即编译查看 PDF
- **多语言支持**：中文（ctex）和英文排版
- **多项目管理**：同时管理多个演示文稿
- **撤销/重做**：完整的会话历史与快照
- **布局模板**：常用布局的 LaTeX 脚本库

## 快速开始

### 系统要求

- LaTeX 发行版（TeX Live、MiKTeX 或 MacTeX）
- xelatex 编译器（中文支持必需）
- Python 3.7+（可选，用于辅助脚本）

### 安装

1. 将此 skill 安装到 AI 助手的 skill 目录
2. 确保系统已安装 LaTeX
3. 开始创建演示文稿！

### 基本用法

直接开始对话：
```
用户：帮我做一个关于机器学习的PPT

AI：你好！我是 Beamer PPT 助手。
     
     请选择演示文稿的语言：
     A) 中文（简体）B) English C) 其他
     
     （这将决定 PPT 内容的语言，与我们的对话语言无关）
```

## 项目结构

创建演示文稿时，skill 会生成：

```
my-presentation/
├── main.tex          # 主 LaTeX 文件（始终可编译）
├── beamer-skill.json # 项目配置
├── figures/          # 你的图片放在这里
└── .beamer-skill/    # 工作文件（快照、预览）
```

## 布局脚本

Skill 包含预构建的 LaTeX 布局模板，位于 `scripts/layouts/`：

- **single-column/**：文字、项目列表
- **two-column/**：左图右文、双文字块
- **three-column/**：三图并排、混排
- **special/**：全屏图片、居中强调

这些模板节省 token 并确保代码一致无错误。

## 快捷命令

为高级用户提供的快捷命令：

| 命令 | 说明 |
|---------|-------------|
| `/next` | 继续下一页 |
| `/list` | 列出所有幻灯片 |
| `/goto N` | 跳转到第 N 页 |
| `/preview` | 重新编译当前页 |
| `/undo` | 撤销上一步 |
| `/help` | 显示所有命令 |

## 使用示例

### 学术演示

```
用户：创建一个论文答辩演示文稿

AI：请选择语言：
    A) 中文  B) English

用户：A

AI：选择模板：
    1) 论文答辩（正式学术风格）
    2) 会议报告（简短格式）
    
用户：1

AI: [引导完成标题、目录、章节、内容页]
```

### 商务演示

```
用户：帮我做一个产品介绍的PPT

AI: 请选择语言：
    A) 中文  B) English

用户：A

AI: 选择模板：
    1) 产品发布会  2) 项目汇报  3) 培训课程
    
[全程中文引导创建]
```

### 跨语言场景

```
用户：我要做一个英文的国际会议报告
       （可以用中文和你交流吗？）

AI：当然！您可以用中文与我交流，我会生成英文内容。
     
     已选择：英文演示文稿
     
     请输入英文或中文标题（我会翻译）：
     
用户：基于深度学习的图像识别

AI: 翻译为："Image Recognition Based on Deep Learning"
     
     继续用中文输入所有内容...
```

## 配置

### LaTeX 编译器

默认：`xelatex`（中文必需）

如需使用其他编译器，在项目创建时指定或在 `beamer-skill.json` 中修改：
```json
{
  "settings": {
    "compiler": "lualatex"
  }
}
```

### 中文字体

根据操作系统自动检测：
- **Windows**：SimSun（宋体）、SimHei（黑体）
- **macOS**：PingFang SC（苹方）
- **Linux**：Noto CJK

在项目根目录创建 `.font-config.tex` 可覆盖默认配置。

### 主题

支持内置 Beamer 主题：
- metropolis（现代，推荐）
- Madrid（经典学术）
- Berlin（导航栏）
- CambridgeUS（简洁学术）
- 更多...

## 故障排除

### 找不到 LaTeX

```bash
# macOS
brew install --cask mactex

# Ubuntu/Debian
sudo apt-get install texlive-full

# Windows
# 从 https://tug.org/texlive/ 下载安装
```

### 中文显示问题

1. 确认 xelatex 已安装：`xelatex --version`
2. 检查中文字体：`fc-list :lang=zh`
3. 尝试在 `.font-config.tex` 中手动配置字体

### 编译错误

常见解决方法：
- 图片缺失 → 检查 `figures/` 文件夹
- 宏包未找到 → 运行 `tlmgr install <宏包名>`
- 字体问题 → 使用备用字体

## 开发

### 项目结构

```
beamer-skill/
├── SKILL.md              # 主 skill 说明
├── README.md             # 英文文档
├── README_zh.md          # 本文档
├── references/           # 技术参考
│   ├── latex-basics.md
│   ├── beamer-themes.md
│   ├── layout-patterns.md
│   └── chinese-typesetting.md
├── assets/               # 模板和示例
│   ├── templates/
│   └── examples/
└── scripts/              # 可复用布局脚本
    └── layouts/
```

### 添加布局脚本

添加自定义布局：

1. 在 `scripts/layouts/custom/` 创建 `.tex` 文件
2. 使用占位符：`{{TITLE}}`、`{{CONTENT}}` 等
3. 在顶部添加描述注释
4. 重启 skill 加载

示例：
```latex
% 布局：自定义时间轴
% 说明：左侧时间戳，右侧事件
% 占位符：{{TITLE}}、{{EVENTS}}

\begin{frame}{{{TITLE}}}
{{EVENTS}}
\end{frame}
```

## 参与贡献

欢迎贡献！可改进的方向：
- 更多布局模板
- 更多主题预设
- 更好的错误处理
- 更多语言支持

## 许可证

MIT 许可证

## 致谢

- Beamer 文档类作者 Till Tantau
- ctex 宏包维护者 CTEX.org
- Metropolis 主题作者 Matthias Vogelgesang
```

- [ ] **Step 2: Commit Chinese README**

```bash
git add README_zh.md
git commit -m "docs: add Chinese README_zh.md"
```

---

## Phase 3: Reference Documentation

### Task 4: Create references/latex-basics.md

**Files:**
- Create: `references/latex-basics.md`

- [ ] **Step 1: Write LaTeX basics reference**

```markdown
# LaTeX Basics for Beamer

## Document Structure

### Basic Beamer Document

```latex
\documentclass[aspectratio=169,11pt]{beamer}

% Theme setup
\usetheme{metropolis}
\usecolortheme{seahorse}

% Packages
\usepackage{ctex}  % For Chinese
\usepackage{graphicx}
\usepackage{amsmath}

% Title info
\title{Presentation Title}
\author{Author Name}
\institute{Institution}
\date{\today}

\begin{document}

\frame{\titlepage}

\begin{frame}{Outline}
\tableofcontents
\end{frame}

\section{Introduction}
\begin{frame}{Introduction}
Content here
\end{frame}

\end{document}
```

## Common Commands

### Frame Environment

```latex
\begin{frame}{Frame Title}
% Content
\end{frame}

\begin{frame}[fragile]{Code Frame}  % For verbatim/code
\begin{verbatim}
code here
\end{verbatim}
\end{frame}

\begin{frame}[allowframebreaks]{Long Content}  % Auto split
% Very long content
\end{frame}
```

### Text Formatting

```latex
\textbf{Bold text}
\textit{Italic text}
\texttt{Monospace/code}
\emph{Emphasis}
\alert{Highlighted text}  % Beamer specific
```

### Lists

```latex
% Itemize
\begin{itemize}
\item First item
\item Second item
\item Third item
\end{itemize}

% Enumerate
\begin{enumerate}
\item First
\item Second
\item Third
\end{enumerate}

% Description
\begin{description}
\item[Term] Definition
\item[Another] Another definition
\end{description}
```

### Columns

```latex
\begin{columns}[T]  % T=top, c=center, b=bottom
\column{0.5\textwidth}
Left content

\column{0.5\textwidth}
Right content
\end{columns}
```

### Blocks

```latex
\begin{block}{Block Title}
Regular block content
\end{block}

\begin{alertblock}{Warning}
Alert/highlighted block
\end{alertblock}

\begin{exampleblock}{Example}
Example block (green in default themes)
\end{exampleblock}
```

### Images

```latex
\includegraphics[width=0.8\textwidth]{image.png}

\includegraphics[height=5cm]{image.png}

\includegraphics[scale=0.5]{image.png}
```

### Tables

```latex
\begin{tabular}{lcr}  % left, center, right
\toprule
Header 1 & Header 2 & Header 3 \\
\midrule
Left & Center & Right \\
Data & Data & Data \\
\bottomrule
\end{tabular}
```

## Document Class Options

```latex
\documentclass[
    aspectratio=169,  % 16:9 (default), 43 for 4:3, 1610 for 16:10
    11pt,             % Font size: 8pt, 9pt, 10pt, 11pt, 12pt, 14pt, 17pt, 20pt
    t,                % Top alignment (c=center, b=bottom)
    compress,         % Compress navigation bars
    handout,          % Handout mode (no overlays)
    draft             % Draft mode (faster compilation)
]{beamer}
```

## Common Packages

```latex
\usepackage{amsmath}      % Math
\usepackage{amssymb}      % Math symbols
\usepackage{graphicx}     % Images
\usepackage{booktabs}     % Nice tables
\usepackage{tikz}         % Graphics
\usepackage{pgfplots}     % Plots
\usepackage{listings}     % Code listings
\usepackage{hyperref}     % Links
```

## Compilation

### Standard (no bibliography)
```bash
xelatex -interaction=nonstopmode main.tex
```

### With Bibliography
```bash
xelatex -interaction=nonstopmode main.tex
bibtex main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

### Extract Single Page
```bash
pdftoppm -f 3 -l 3 -png -r 150 main.pdf page-3.png
```

## Error Messages

### Common Errors

**File not found:**
```
! LaTeX Error: File `xxx.sty' not found.
```
Solution: `tlmgr install xxx`

**Undefined control sequence:**
```
! Undefined control sequence.
l.15 \xxx
```
Solution: Check for typos or missing packages

**Overfull hbox:**
```
Overfull \hbox (10.234pt too wide) in paragraph
```
Solution: Text too wide, adjust spacing or use `\raggedright`

**Missing $ inserted:**
```
! Missing $ inserted.
```
Solution: Math symbol in text mode, wrap in `$...$`
```

- [ ] **Step 2: Commit latex-basics.md**

```bash
git add references/latex-basics.md
git commit -m "docs: add LaTeX basics reference"
```

---

### Task 5: Create references/beamer-themes.md

**Files:**
- Create: `references/beamer-themes.md`

- [ ] **Step 1: Write Beamer themes reference**

```markdown
# Beamer Themes Reference

## Built-in Themes

### Modern Themes

**metropolis** (Recommended)
```latex
\usetheme{metropolis}
\metroset{
    background=light,      % light or dark
    titleformat=regular,   % regular, smallcaps, etc.
    sectionpage=progressbar
}
```
- Clean, modern design
- Good for academic and business
- Highly customizable

**Madrid** (Classic Academic)
```latex
\usetheme{Madrid}
\usecolortheme{whale}  % or beaver, dolphin, etc.
```
- Traditional academic look
- Navigation bars at top and bottom

**Berlin**
```latex
\usetheme{Berlin}
```
- Tree-like navigation
- Good for long presentations

**CambridgeUS**
```latex
\usetheme{CambridgeUS}
```
- Clean academic style
- No navigation bars

### Simple Themes

**default**
```latex
\usetheme{default}
```
- Minimal styling
- Good for custom themes

**boxes**
```latex
\usetheme{boxes}
\usecolortheme{seahorse}
```
- Boxed layout
- Clean and simple

**Pittsburgh**
```latex
\usetheme{Pittsburgh}
```
- Very minimal
- Just frame title

## Color Themes

### Built-in Color Themes

```latex
\usecolortheme{default}      % Blue-based
\usecolortheme{albatross}    % Dark blue background
\usecolortheme{beaver}       % Red-based
\usecolortheme{beetle}       % Gray
\usecolortheme{crane}        # Orange-based
\usecolortheme{dolphin}      % Blue-green
\usecolortheme{dove}         % Grayscale
\usecolortheme{fly}          % Dark gray
\usecolortheme{seagull}      % Light gray
\usecolortheme{seahorse}     % Light blue-green
\usecolortheme{sidebartab}   % With sidebar
\usecolortheme{spruce}       % Green-based
\usecolortheme{whale}        % Deep blue
\usecolortheme{wolverine}    % Yellow-brown
```

### Custom Colors

```latex
\definecolor{myblue}{RGB}{0, 102, 204}
\definecolor{myorange}{HTML}{FF6600}

\setbeamercolor{title}{fg=myblue}
\setbeamercolor{frametitle}{fg=myblue,bg=white}
\setbeamercolor{structure}{fg=myblue}
\setbeamercolor{block title}{bg=myblue,fg=white}
```

## Font Themes

```latex
\usefonttheme{default}      % sans-serif (default)
\usefonttheme{professionalfonts}  % Use package fonts
\usefonttheme{serif}        % Serif fonts
\usefonttheme{structurebold}  % Bold titles
\usefonttheme{structureitalicserif}  % Italic serif structure
\usefonttheme{structuresmallcapsserif}  % Small caps
```

## Inner Themes (Frame Layout)

```latex
\useinnertheme{default}     % Standard
\useinnertheme{circles}     % Circular bullets
\useinnertheme{rectangles}  % Square bullets
\useinnertheme{rounded}     % Rounded boxes
\useinnertheme{inmargin}    % Items in margin
```

## Outer Themes (Navigation)

```latex
\useoutertheme{default}     % No navigation
\useoutertheme{infolines}   % Title + author + page
\useoutertheme{miniframes}  % Mini frame navigation
\useoutertheme{smoothbars}  % Smooth navigation bars
\useoutertheme{sidebar}     % Sidebar navigation
\useoutertheme{split}       % Split header/footer
\useoutertheme{shadow}      % Shadow boxes
\useoutertheme{tree}        % Tree navigation
\useoutertheme{smoothtree}  % Smooth tree
```

## Theme Combinations

### Academic Presentation
```latex
\usetheme{Madrid}
\usecolortheme{seahorse}
\usefonttheme{professionalfonts}
```

### Business Presentation
```latex
\usetheme{metropolis}
\metroset{background=dark}
\usecolortheme{default}
```

### Minimal Presentation
```latex
\usetheme{default}
\usecolortheme{dove}
\useoutertheme{infolines}
```

### Colorful Presentation
```latex
\usetheme{CambridgeUS}
\usecolortheme{dolphin}
\useinnertheme{circles}
```

## Customization

### Hide Navigation Symbols
```latex
\beamertemplatenavigationsymbolsempty
```

### Custom Footer
```latex
\setbeamertemplate{footline}{
    \hfill\insertframenumber/\inserttotalframenumber\hspace{2em}\vspace{1em}
}
```

### Custom Itemize
```latex
\setbeamertemplate{itemize items}[circle]
\setbeamertemplate{itemize subitem}[square]
\setbeamertemplate{itemize subsubitem}[ball]
```

### Background
```latex
\setbeamertemplate{background}{
    \includegraphics[width=\paperwidth]{background.png}
}
```

## Aspect Ratios

```latex
\documentclass[aspectratio=169]{beamer}  % 16:9 (wide)
\documentclass[aspectratio=43]{beamer}   % 4:3 (standard)
\documentclass[aspectratio=1610]{beamer} % 16:10
\documentclass[aspectratio=149]{beamer}  % 14:9
\documentclass[aspectratio=141]{beamer}  % 1.41:1
\documentclass[aspectratio=54]{beamer}   % 5:4
\documentclass[aspectratio=32]{beamer}   % 3:2
```
```

- [ ] **Step 2: Commit beamer-themes.md**

```bash
git add references/beamer-themes.md
git commit -m "docs: add Beamer themes reference"
```

---

## Phase 4: Layout Scripts

### Task 6: Create layout scripts

**Files:**
- Create: `scripts/layouts/single-column/text-only.tex`
- Create: `scripts/layouts/single-column/bullet-list.tex`
- Create: `scripts/layouts/two-column/image-left.tex`
- Create: `scripts/layouts/two-column/image-right.tex`

- [ ] **Step 1: Create text-only layout**

```latex
% ============================================
% Layout: Single Column - Text Only
% Description: Pure text paragraph layout
% Placeholders:
%   {{TITLE}}      - Frame title
%   {{CONTENT}}    - Main text content
% ============================================

\begin{frame}{{{TITLE}}}
{{CONTENT}}
\end{frame}
```

- [ ] **Step 2: Create bullet-list layout**

```latex
% ============================================
% Layout: Single Column - Bullet List
% Description: Bullet point list layout
% Placeholders:
%   {{TITLE}}      - Frame title
%   {{ITEMS}}      - Bullet items (each starting with \item)
% ============================================

\begin{frame}{{{TITLE}}}
\begin{itemize}
{{ITEMS}}
\end{itemize}
\end{frame}
```

- [ ] **Step 3: Create image-left layout**

```latex
% ============================================
% Layout: Two Column - Image Left
% Description: Left image (45-50%), right text
% Placeholders:
%   {{TITLE}}       - Frame title
%   {{IMAGE_PATH}}  - Path to image file
%   {{IMAGE_WIDTH}} - Image width (default: 0.45\textwidth)
%   {{TEXT}}        - Text content (can include itemize, etc.)
% ============================================

\begin{frame}{{{TITLE}}}
\begin{columns}[T]
\column{0.5\textwidth}
\includegraphics[width={{IMAGE_WIDTH}}]{{{IMAGE_PATH}}}

\column{0.5\textwidth}
{{TEXT}}
\end{columns}
\end{frame}
```

- [ ] **Step 4: Create image-right layout**

```latex
% ============================================
% Layout: Two Column - Image Right
% Description: Left text, right image (45-50%)
% Placeholders:
%   {{TITLE}}       - Frame title
%   {{TEXT}}        - Text content (left side)
%   {{IMAGE_PATH}}  - Path to image file
%   {{IMAGE_WIDTH}} - Image width (default: 0.45\textwidth)
% ============================================

\begin{frame}{{{TITLE}}}
\begin{columns}[T]
\column{0.5\textwidth}
{{TEXT}}

\column{0.5\textwidth}
\includegraphics[width={{IMAGE_WIDTH}}]{{{IMAGE_PATH}}}
\end{columns}
\end{frame}
```

- [ ] **Step 5: Commit layout scripts**

```bash
git add scripts/layouts/
git commit -m "feat: add reusable LaTeX layout scripts"
```

---

## Phase 5: Assets - Templates

### Task 7: Create template configurations

**Files:**
- Create: `assets/templates/academic-thesis/template.json`
- Create: `assets/templates/business-report/template.json`

- [ ] **Step 1: Create academic thesis template config**

```json
{
  "name": "学术论文答辩",
  "name_en": "Academic Thesis Defense",
  "description": "适合硕士/博士论文答辩的正式学术模板",
  "description_en": "Formal academic template for thesis defense",
  "category": "academic",
  "pages": [
    {"type": "title", "name": "封面", "name_en": "Title Page", "required": true},
    {"type": "toc", "name": "目录", "name_en": "Outline", "required": true},
    {"type": "section", "name": "章节分隔页", "name_en": "Section Divider", "required": false},
    {"type": "content", "name": "内容页", "name_en": "Content", "required": true},
    {"type": "final", "name": "致谢", "name_en": "Acknowledgments", "required": true}
  ],
  "default_theme": "metropolis",
  "default_color_theme": "seahorse",
  "aspect_ratio": "169",
  "font_size": "11pt",
  "recommended_for": ["学位论文答辩", "开题报告", "学术报告"]
}
```

- [ ] **Step 2: Create business report template config**

```json
{
  "name": "商务汇报",
  "name_en": "Business Report",
  "description": "适合产品介绍、项目汇报的现代商务模板",
  "description_en": "Modern business template for product demos and reports",
  "category": "business",
  "pages": [
    {"type": "title", "name": "封面", "name_en": "Title Page", "required": true},
    {"type": "agenda", "name": "议程", "name_en": "Agenda", "required": true},
    {"type": "content", "name": "内容页", "name_en": "Content", "required": true},
    {"type": "chart", "name": "数据展示页", "name_en": "Data Visualization", "required": false},
    {"type": "final", "name": "结束页", "name_en": "Closing", "required": true}
  ],
  "default_theme": "metropolis",
  "default_color_theme": "default",
  "aspect_ratio": "169",
  "font_size": "12pt",
  "recommended_for": ["产品发布", "项目汇报", "商业路演"]
}
```

- [ ] **Step 3: Commit template configs**

```bash
git add assets/templates/
git commit -m "feat: add template configurations"
```

---

## Phase 6: Validation and Packaging

### Task 8: Validate skill structure

**Files:**
- Validate: All created files

- [ ] **Step 1: Check required files exist**

Run:
```bash
ls -la SKILL.md README.md README_zh.md
echo "---"
ls -la references/
echo "---"
ls -la scripts/layouts/
echo "---"
ls -la assets/templates/
```

Expected: All files listed above should exist

- [ ] **Step 2: Validate SKILL.md frontmatter**

Run:
```bash
grep -A 3 "^---" SKILL.md | head -5
```

Expected: Should show YAML frontmatter with `name:` and `description:`

- [ ] **Step 3: Test layout scripts syntax**

Run:
```bash
# Check for basic LaTeX syntax in layout scripts
for file in scripts/layouts/*/*.tex; do
    echo "Checking $file..."
    grep -q "\\\\begin{frame}" "$file" && echo "✓ Has frame" || echo "✗ Missing frame"
    grep -q "\\\\end{frame}" "$file" && echo "✓ Has end frame" || echo "✗ Missing end frame"
done
```

- [ ] **Step 4: Commit final validation**

```bash
git add -A
git commit -m "chore: final validation and structure check"
```

---

## Final Deliverables

After completing all tasks, the skill structure should be:

```
beamer-skill/
├── SKILL.md              ✓ Main skill file
├── README.md             ✓ English documentation
├── README_zh.md          ✓ Chinese documentation
├── LICENSE               ✓ (existing)
├── references/
│   ├── latex-basics.md   ✓ LaTeX fundamentals
│   ├── beamer-themes.md  ✓ Theme reference
│   ├── layout-patterns.md  (optional, can add later)
│   └── chinese-typesetting.md  (optional, can add later)
├── assets/
│   └── templates/
│       ├── academic-thesis/
│       │   └── template.json  ✓
│       └── business-report/
│           └── template.json  ✓
└── scripts/
    └── layouts/          ✓ Layout script library
        ├── single-column/
        │   ├── text-only.tex
        │   └── bullet-list.tex
        └── two-column/
            ├── image-left.tex
            └── image-right.tex
```

## Success Criteria

✅ SKILL.md has proper YAML frontmatter with name and description  
✅ README.md and README_zh.md are comprehensive (200+ lines each)  
✅ Reference documentation covers LaTeX basics and themes  
✅ At least 4 reusable layout scripts created  
✅ At least 2 template configurations created  
✅ All files committed to git  
✅ Skill can be packaged and distributed

---

## Next Steps

After this plan is complete:

1. **Package the skill** using skill-creator's packaging script
2. **Test with real use cases** (create a sample presentation)
3. **Iterate based on usage** (add more layouts, improve prompts)

The skill is now ready for use!

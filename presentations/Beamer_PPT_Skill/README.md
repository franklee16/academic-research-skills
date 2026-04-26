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

1. Install this skill to your AI assistant's skill directory (see [Deployment Guide](#deployment-guide) below)
2. Ensure LaTeX is installed on your system
3. Start creating presentations!

## Deployment Guide

Deploy this skill to your preferred AI assistant platform:

### Claude Code

**Global Installation** (available in all projects):
```bash
# Clone the repository
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/hasson827/Beamer_Skill.git beamer-ppt

# Or download as zip and extract
# unzip beamer-ppt-skill.zip -d ~/.claude/skills/beamer-ppt
```

**Project-specific Installation** (only for current project):
```bash
# In your project root
mkdir -p .claude/skills
git clone https://github.com/hasson827/Beamer_Skill.git .claude/skills/beamer-ppt
```

**Verification**:
```bash
# List installed skills
claude skills list

# You should see "beamer-ppt" in the list
```

**Usage**:
```
# In Claude Code, invoke the skill
/beamer-ppt

# Or simply start creating a presentation
User: Help me create a beamer presentation
```

### OpenCode

**Global Installation** (recommended):
```bash
# Method 1: Using OpenCode skills directory
mkdir -p ~/.config/opencode/skills
cd ~/.config/opencode/skills
git clone https://github.com/hasson827/Beamer_Skill.git beamer-ppt

# Method 2: Using Claude-compatible directory (OpenCode also reads this)
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/hasson827/Beamer_Skill.git beamer-ppt
```

**Project-specific Installation**:
```bash
# In your project root
mkdir -p .opencode/skills
git clone https://github.com/hasson827/Beamer_Skill.git .opencode/skills/beamer-ppt
```

**Verification**:
The skill will appear in OpenCode's available skills list automatically when you restart or start a new session.

**Usage**:
```python
# In OpenCode, invoke the skill tool
skill({"name": "beamer-ppt"})

# Or ask directly
User: Help me create a presentation
```

### Codex CLI (OpenAI)

**Global Installation**:
```bash
# Using the built-in skill installer (recommended)
codex
$skill-installer beamer-ppt

# Or manual installation
mkdir -p ~/.codex/skills
cd ~/.codex/skills
git clone https://github.com/hasson827/Beamer_Skill.git beamer-ppt
```

**Project-specific Installation**:
```bash
# In your project root
mkdir -p .codex/skills
git clone https://github.com/hasson827/Beamer_Skill.git .codex/skills/beamer-ppt

# Or use .agents directory (also supported)
mkdir -p .agents/skills
git clone https://github.com/hasson827/Beamer_Skill.git .agents/skills/beamer-ppt
```

**Verification**:
```bash
# In Codex CLI, list available skills
/skills

# Or try to invoke
$beamer-ppt
```

**Usage**:
```
# In Codex CLI, invoke with $ prefix
$beamer-ppt

# Or simply describe your need
User: Create a thesis defense presentation
```

### Claude.ai (Web)

For the web version of Claude:

1. **Download the skill**:
   - Go to the [GitHub repository](https://github.com/hasson827/Beamer_Skill)
   - Click "Code" → "Download ZIP"
   - Extract the ZIP file

2. **Upload to Claude.ai**:
   - Go to [Claude.ai](https://claude.ai)
   - Start a new conversation
   - Upload the `SKILL.md` file as an attachment
   - Or upload the entire folder as a ZIP file

3. **Reference the skill**:
   - Mention "using the Beamer PPT skill" in your prompt
   - Claude will reference the uploaded skill file

### Cursor / VS Code

If you're using Cursor or VS Code with Claude integration:

```bash
# Create the skills directory in your project
mkdir -p .claude/skills
git clone https://github.com/hasson827/Beamer_Skill.git .claude/skills/beamer-ppt
```

The skill will be automatically discovered when you use Claude features in your editor.

### Directory Structure Summary

After installation, your skill directory should look like this:

```
~/.claude/skills/beamer-ppt/           # For Claude Code (global)
~/.config/opencode/skills/beamer-ppt/  # For OpenCode (global)
~/.codex/skills/beamer-ppt/            # For Codex CLI (global)
.claude/skills/beamer-ppt/             # For project-specific (Claude)
.opencode/skills/beamer-ppt/           # For project-specific (OpenCode)
.codex/skills/beamer-ppt/              # For project-specific (Codex)

# Each location contains:
├── SKILL.md              # Main skill file (required)
├── README.md             # Documentation
├── references/           # Reference materials
│   ├── layout-patterns.md
│   ├── chinese-typesetting.md
│   └── ...
├── scripts/              # Layout templates
│   └── layouts/
└── assets/               # Templates and examples
```

### Updating the Skill

**For git installations**:
```bash
# Navigate to the skill directory
cd ~/.claude/skills/beamer-ppt  # or your installation path

# Pull latest changes
git pull origin main
```

**For manual installations**:
1. Download the latest release
2. Replace the old skill folder with the new one
3. Restart your AI assistant

### Uninstalling

Simply delete the skill directory:
```bash
# For Claude Code
rm -rf ~/.claude/skills/beamer-ppt

# For OpenCode
rm -rf ~/.config/opencode/skills/beamer-ppt

# For Codex CLI
rm -rf ~/.codex/skills/beamer-ppt
```

### Troubleshooting Installation

**Skill not appearing**:
1. Verify the `SKILL.md` file exists in the skill directory
2. Check the directory path is correct
3. Restart your AI assistant / terminal
4. For OpenCode: Ensure the skill name matches the directory name

**Permission issues**:
```bash
# Fix permissions (Linux/macOS)
chmod -R 755 ~/.claude/skills/beamer-ppt
```

**Conflicting skills**:
- Project-level skills override global skills
- Remove or rename conflicting skills
- Use `claude skills list` (Claude Code) or `/skills` (Codex) to see loaded skills

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
| `/redo` | Redo |
| `/delete` | Delete current slide |
| `/copy` | Copy current slide |
| `/theme` | Change theme |
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
- **metropolis** (modern, recommended)
- **Madrid** (classic academic)
- **Berlin** (navigation bars)
- **CambridgeUS** (clean academic)
- **Boadilla** (compact)
- **Montpellier** (tree navigation)
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
- **Missing images**: Check `figures/` folder paths
- **Package not found**: Run `tlmgr install <package>`
- **Font issues**: Use fallback fonts via `.font-config.tex`
- **Syntax errors**: Check LaTeX special characters in content

### PDF Preview Not Showing

1. Check if compilation succeeded (view logs in terminal)
2. Verify LaTeX installation: `xelatex --version`
3. Check file permissions in project directory: `ls -la`

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
│   │   ├── academic-thesis/
│   │   ├── business-report/
│   │   ├── course-lecture/
│   │   └── conference-talk/
│   └── examples/
│       ├── example-academic/
│       └── example-business/
└── scripts/              # Reusable layout scripts
    └── layouts/
        ├── single-column/
        ├── two-column/
        ├── three-column/
        └── special/
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

### Template Configuration

Templates are defined in JSON files:

```json
{
  "name": "Academic Thesis Defense",
  "category": "academic",
  "pages": [
    {"type": "title", "required": true},
    {"type": "toc", "required": true},
    {"type": "content", "required": true}
  ],
  "default_theme": "metropolis",
  "aspect_ratio": "169"
}
```

## Contributing

Contributions welcome! Areas for improvement:
- Additional layout templates (new column arrangements)
- More theme presets (color schemes)
- Better error handling and user guidance
- Additional language support (Japanese, Korean, etc.)
- Helper scripts for batch operations

Please follow the existing code style and document any new features.

## License

MIT License - See [LICENSE](LICENSE) file for details

## Acknowledgments

- Beamer class by Till Tantau
- ctex package by CTEX.org
- Metropolis theme by Matthias Vogelgesang
- LaTeX Project Team for the amazing typesetting system

---

**Note**: This skill requires a LaTeX installation on your system. The skill generates LaTeX code but relies on your local LaTeX distribution for PDF compilation.

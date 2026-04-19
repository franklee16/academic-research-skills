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

1. 将此 skill 安装到 AI 助手的 skill 目录（详见下方的[部署指南](#部署指南)）
2. 确保系统已安装 LaTeX
3. 开始创建演示文稿！

## 部署指南

将本 skill 部署到您偏好的 AI 助手平台：

### Claude Code

**全局安装**（在所有项目中可用）：
```bash
# 克隆仓库
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/hasson827/Beamer_Skill.git beamer-ppt

# 或下载 zip 并解压
# unzip beamer-ppt-skill.zip -d ~/.claude/skills/beamer-ppt
```

**项目级安装**（仅在当前项目可用）：
```bash
# 在项目根目录
mkdir -p .claude/skills
git clone https://github.com/hasson827/Beamer_Skill.git .claude/skills/beamer-ppt
```

**验证**：
```bash
# 列出已安装的 skill
claude skills list

# 你应该能看到 "beamer-ppt"
```

**使用方法**：
```
# 在 Claude Code 中调用 skill
/beamer-ppt

# 或直接开始创建演示文稿
用户：帮我创建一个 beamer 演示文稿
```

### OpenCode

**全局安装**（推荐）：
```bash
# 方法 1：使用 OpenCode skill 目录
mkdir -p ~/.config/opencode/skills
cd ~/.config/opencode/skills
git clone https://github.com/hasson827/Beamer_Skill.git beamer-ppt

# 方法 2：使用 Claude 兼容目录（OpenCode 也支持）
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/hasson827/Beamer_Skill.git beamer-ppt
```

**项目级安装**：
```bash
# 在项目根目录
mkdir -p .opencode/skills
git clone https://github.com/hasson827/Beamer_Skill.git .opencode/skills/beamer-ppt
```

**验证**：
重启或开启新会话后，skill 会自动出现在 OpenCode 的可用 skill 列表中。

**使用方法**：
```python
# 在 OpenCode 中调用 skill 工具
skill({"name": "beamer-ppt"})

# 或直接提问
用户：帮我做一个演示文稿
```

### Codex CLI (OpenAI)

**全局安装**：
```bash
# 使用内置 skill 安装器（推荐）
codex
$skill-installer beamer-ppt

# 或手动安装
mkdir -p ~/.codex/skills
cd ~/.codex/skills
git clone https://github.com/hasson827/Beamer_Skill.git beamer-ppt
```

**项目级安装**：
```bash
# 在项目根目录
mkdir -p .codex/skills
git clone https://github.com/hasson827/Beamer_Skill.git .codex/skills/beamer-ppt

# 或使用 .agents 目录（也支持）
mkdir -p .agents/skills
git clone https://github.com/hasson827/Beamer_Skill.git .agents/skills/beamer-ppt
```

**验证**：
```bash
# 在 Codex CLI 中列出可用 skill
/skills

# 或尝试调用
$beamer-ppt
```

**使用方法**：
```
# 在 Codex CLI 中使用 $ 前缀调用
$beamer-ppt

# 或直接描述你的需求
用户：创建一个论文答辩演示文稿
```

### Claude.ai (网页版)

适用于 Claude 网页版：

1. **下载 skill**：
   - 前往 [GitHub 仓库](https://github.com/hasson827/Beamer_Skill)
   - 点击 "Code" → "Download ZIP"
   - 解压 ZIP 文件

2. **上传到 Claude.ai**：
   - 访问 [Claude.ai](https://claude.ai)
   - 开启新对话
   - 将 `SKILL.md` 文件作为附件上传
   - 或上传整个文件夹的 ZIP 文件

3. **引用 skill**：
   - 在提示词中提及 "使用 Beamer PPT skill"
   - Claude 将引用上传的 skill 文件

### Cursor / VS Code

如果您使用 Cursor 或带 Claude 集成的 VS Code：

```bash
# 在项目中创建 skill 目录
mkdir -p .claude/skills
git clone https://github.com/hasson827/Beamer_Skill.git .claude/skills/beamer-ppt
```

使用编辑器中的 Claude 功能时，skill 将被自动发现。

### 目录结构总结

安装后，skill 目录结构如下：

```
~/.claude/skills/beamer-ppt/           # Claude Code（全局）
~/.config/opencode/skills/beamer-ppt/  # OpenCode（全局）
~/.codex/skills/beamer-ppt/            # Codex CLI（全局）
.claude/skills/beamer-ppt/             # 项目级（Claude）
.opencode/skills/beamer-ppt/           # 项目级（OpenCode）
.codex/skills/beamer-ppt/              # 项目级（Codex）

# 每个位置包含：
├── SKILL.md              # 主 skill 文件（必需）
├── README.md             # 文档
├── references/           # 参考资料
│   ├── layout-patterns.md
│   ├── chinese-typesetting.md
│   └── ...
├── scripts/              # 布局模板
│   └── layouts/
└── assets/               # 模板和示例
```

### 更新 Skill

**Git 安装**：
```bash
# 进入 skill 目录
cd ~/.claude/skills/beamer-ppt  # 或你的安装路径

# 拉取最新更改
git pull origin main
```

**手动安装**：
1. 下载最新版本
2. 用新版本替换旧 skill 文件夹
3. 重启 AI 助手

### 卸载

直接删除 skill 目录：
```bash
# Claude Code
rm -rf ~/.claude/skills/beamer-ppt

# OpenCode
rm -rf ~/.config/opencode/skills/beamer-ppt

# Codex CLI
rm -rf ~/.codex/skills/beamer-ppt
```

### 安装故障排除

**Skill 未显示**：
1. 验证 skill 目录中存在 `SKILL.md` 文件
2. 检查目录路径是否正确
3. 重启 AI 助手 / 终端
4. OpenCode：确保 skill 名称与目录名称匹配

**权限问题**：
```bash
# 修复权限（Linux/macOS）
chmod -R 755 ~/.claude/skills/beamer-ppt
```

**Skill 冲突**：
- 项目级 skill 会覆盖全局 skill
- 删除或重命名冲突的 skill
- 使用 `claude skills list`（Claude Code）或 `/skills`（Codex）查看已加载的 skill

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

### 目录说明

- **main.tex**: 主 LaTeX 源文件，包含所有幻灯片代码
- **beamer-skill.json**: 项目配置文件，保存主题、字体等设置
- **figures/**: 存放所有图片资源，支持 PNG/JPG/PDF/EPS 格式
- **.beamer-skill/snapshots/**: 自动保存的历史版本，支持撤销/重做
- **.beamer-skill/preview/**: 预览图片缓存

## 布局脚本

Skill 包含预构建的 LaTeX 布局模板，位于 `scripts/layouts/`：

### 单列布局 (single-column/)

- **text-only.tex**: 纯文字段落布局
- **bullet-list.tex**: 项目符号列表
- **numbered-list.tex**: 编号列表
- **quote-block.tex**: 引用块布局

### 双列布局 (two-column/)

- **image-left.tex**: 左图右文布局
- **image-right.tex**: 左文右图布局
- **two-text.tex**: 双文字块布局
- **two-images.tex**: 双图并排布局

### 三列布局 (three-column/)

- **three-images.tex**: 三图并排
- **mixed-content.tex**: 混排内容
- **timeline.tex**: 时间轴布局

### 特殊布局 (special/)

- **full-image.tex**: 全屏图片背景
- **centered-focus.tex**: 居中强调内容
- **title-slide.tex**: 标题页专用
- **section-divider.tex**: 章节分隔页

这些模板节省 token 并确保代码一致无错误。

## 快捷命令

为高级用户提供的快捷命令：

| 命令 | 说明 |
|------|------|
| `/next` | 继续下一页 |
| `/list` | 列出所有幻灯片 |
| `/goto N` | 跳转到第 N 页 |
| `/preview` | 重新编译当前页 |
| `/delete` | 删除当前页 |
| `/copy` | 复制当前页 |
| `/undo` | 撤销上一步 |
| `/redo` | 重做 |
| `/theme` | 更改主题 |
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

支持的编译器：
- `xelatex`: 默认，支持 Unicode 和中文字体
- `lualatex`: 替代选择，字体处理更灵活
- `pdflatex`: 仅英文，速度快但中文支持有限

### 中文字体

根据操作系统自动检测：

- **Windows**：SimSun（宋体）、SimHei（黑体）
- **macOS**：PingFang SC（苹方）
- **Linux**：Noto CJK

在项目根目录创建 `.font-config.tex` 可覆盖默认配置：

```latex
% 自定义字体配置
\setCJKmainfont{Source Han Serif SC}
\setCJKsansfont{Source Han Sans SC}
\setCJKmonofont{Source Han Sans SC}
```

### 主题

支持内置 Beamer 主题：

**现代主题**
- `metropolis`（现代，推荐）
  - 简洁现代的设计
  - 支持亮色/暗色模式
  - 高度可定制

**经典主题**
- `Madrid`（经典学术）
  - 传统学术外观
  - 顶部和底部导航栏
- `Berlin`（导航树）
  - 树状导航结构
  - 适合长演示文稿
- `CambridgeUS`（简洁学术）
  - 干净的学术风格
  - 无导航栏

**简洁主题**
- `default`（默认）
  - 最小样式
  - 适合自定义主题
- `Pittsburgh`（极简）
  - 仅显示框架标题

### 配色方案

```latex
% 暗色主题
\metroset{background=dark}

% 自定义颜色
\definecolor{myblue}{RGB}{0, 102, 204}
\setbeamercolor{title}{fg=myblue}
\setbeamercolor{frametitle}{fg=myblue,bg=white}
```

### 页面比例

```json
{
  "settings": {
    "aspect_ratio": "169"
  }
}
```

可选比例：
- `169`: 16:9（宽屏，推荐）
- `43`: 4:3（标准）
- `1610`: 16:10
- `149`: 14:9
- `141`: 1.41:1
- `54`: 5:4
- `32`: 3:2

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

验证安装：
```bash
xelatex --version
```

### 中文显示问题

1. 确认 xelatex 已安装：
   ```bash
   xelatex --version
   ```

2. 检查中文字体：
   ```bash
   fc-list :lang=zh
   ```

3. 尝试在 `.font-config.tex` 中手动配置字体

4. 确保使用 xelatex 而非 pdflatex

### 编译错误

**图片缺失**
- 检查 `figures/` 文件夹路径
- 确认文件名拼写正确
- 支持的格式：PNG, JPG, PDF, EPS

**宏包未找到**
```bash
tlmgr install <宏包名>
```

**字体问题**
- 使用系统可用字体
- 创建 `.font-config.tex` 指定备用字体

**编译超时**
- 检查图片大小（建议 < 5MB）
- 使用草稿模式预览
- 减少复杂布局数量

### PDF 预览不显示

1. 检查编译是否成功（查看日志）
2. 确认 LaTeX 安装正确
3. 检查项目目录权限
4. 尝试手动编译：`xelatex main.tex`

### 项目恢复

崩溃后恢复工作：
1. 运行 "继续上次的编辑"
2. 检查 `.beamer-skill/snapshots/` 目录
3. 手动恢复最近的快照

## 开发

### 项目结构

```
beamer-skill/
├── SKILL.md              # 主 skill 说明
├── README.md             # 英文文档
├── README_zh.md          # 本文档
├── references/           # 技术参考
│   ├── latex-basics.md   # LaTeX 基础
│   ├── beamer-themes.md  # 主题参考
│   ├── layout-patterns.md # 布局模式
│   └── chinese-typesetting.md # 中文排版
├── assets/               # 模板和示例
│   ├── templates/        # 项目模板
│   │   ├── academic-thesis/
│   │   ├── business-report/
│   │   ├── course-lecture/
│   │   └── conference-talk/
│   └── examples/         # 示例项目
│       ├── example-academic/
│       └── example-business/
└── scripts/              # 可复用布局脚本
    └── layouts/
        ├── single-column/
        ├── two-column/
        ├── three-column/
        └── special/
```

### 添加布局脚本

添加自定义布局：

1. 在 `scripts/layouts/custom/` 创建 `.tex` 文件
2. 使用占位符：`{{TITLE}}`、`{{CONTENT}}` 等
3. 在顶部添加描述注释
4. 重启 skill 加载

示例：

```latex
% ============================================
% 布局：自定义时间轴
% 说明：左侧时间戳，右侧事件
% 占位符：{{TITLE}}、{{EVENTS}}
% ============================================

\begin{frame}{{{TITLE}}}
{{EVENTS}}
\end{frame}
```

### 添加模板

创建新模板：

1. 在 `assets/templates/` 创建新目录
2. 添加 `template.json` 配置文件
3. （可选）添加默认的 `main.tex`
4. （可选）添加 `figures/` 示例图片

模板配置示例：

```json
{
  "name": "自定义模板",
  "name_en": "Custom Template",
  "description": "模板描述",
  "category": "academic",
  "pages": [
    {"type": "title", "name": "封面", "required": true},
    {"type": "content", "name": "内容页", "required": true}
  ],
  "default_theme": "metropolis",
  "aspect_ratio": "169",
  "font_size": "11pt"
}
```

## 参与贡献

欢迎贡献！可改进的方向：

- 更多布局模板
- 更多主题预设
- 更好的错误处理
- 更多语言支持（日语、韩语等）
- 动画支持
- 交互式元素
- 云端编译选项

### 提交贡献

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/new-layout`
3. 提交更改：`git commit -am 'Add new layout'`
4. 推送分支：`git push origin feature/new-layout`
5. 创建 Pull Request

## 许可证

MIT 许可证

## 致谢

- Beamer 文档类作者 Till Tantau
- ctex 宏包维护者 CTEX.org
- Metropolis 主题作者 Matthias Vogelgesang
- 所有贡献者和用户

---

**开始使用**: 只需说 "帮我做一个PPT" 即可开始创建您的第一个演示文稿！

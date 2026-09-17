# Beamer PPT 排版 Skill 设计文档

**版本**: 1.0  
**日期**: 2026-03-22  
**状态**: 已批准

---

## 1. 概述

### 1.1 目标
创建一个对话式 Beamer PPT 排版助手 Skill，通过渐进式、交互式的方式帮助用户创建专业的 LaTeX Beamer 演示文稿。

### 1.2 核心理念
- **渐进式构建**: 一页一页地创建，避免信息过载
- **所见即所得**: 每页完成后立即编译预览 PDF
- **灵活布局**: 支持预设模板 + 自然语言描述自定义布局
- **语言独立**: PPT 内容语言与对话语言完全分离，用户主动选择目标语言
- **中文友好**: 针对中文用户优化，支持 ctex 宏包和中文排版

### 1.3 用户画像
- 学术研究人员（论文答辩、学术报告）
- 研究生和博士生
- 商务人士（中文或英文演示文稿）
- LaTeX 初学者（希望通过对话学习）
- 多语言用户（习惯用一种语言交流，但需要制作另一种语言的PPT）

---

## 2. 核心功能

### 2.1 对话式交互流程

```
[用户] "帮我做一个关于机器学习的 PPT"
   ↓
[Skill] 询问使用场景：
        A) 学术汇报  B) 商务演示  C) 课程教学
   ↓
[Skill] 展示 8-12 个预设模板供选择
   ↓
[用户] 选择模板（如"学术论文答辩"）
   ↓
[Skill] 开始逐页引导创建
   
第1页 - 封面:
"请输入标题:" [用户输入]
"请输入作者姓名:" [用户输入]
"请输入单位/学校:" [用户输入]
→ 生成代码 → 编译预览 → 确认

第2页 - 目录页:
"是否包含目录页?" [是/否]
"章节结构: 1.引言 2.方法 3.实验 4.结论"
→ 生成代码 → 编译预览 → 确认

第3页 - 内容页:
"选择布局:
 A) 单栏文字
 B) 左图右文
 C) 双栏对比
 D) 自定义描述"
→ 根据选择收集内容 → 生成代码 → 编译预览 → 确认

... 继续下一页直到完成
```

### 2.2 布局系统

#### 2.2.1 基础布局组件

**单列布局**
- 纯文字段落
- 项目符号列表
- 编号列表
- 引用块

**双列布局**
- 左图右文（图片宽度可配置）
- 左文右图
- 双文字对比
- 双图片并排

**三列布局**
- 三图并排
- 图文混排
- 数据对比（三栏数据）

**特殊布局**
- 全屏图片（背景图 + 前景文字）
- 居中强调（重要结论）
- 分步展示（逐步显示 bullet points）

#### 2.2.2 自定义布局（自然语言）

用户可以描述想要的布局，AI 解析并生成代码：

**示例对话：**
```
[用户] 我想要顶部一个标题，下面左边放一张大图占2/3宽度，
       右边分三行放小图

[Skill] 明白了！这是一个复合布局：
       
       ┌─────────────────────┐
       │      标题           │
       ├──────────┬──────────┤
       │          │  小图1   │
       │   大图   ├──────────┤
       │  (2/3)   │  小图2   │
       │          ├──────────┤
       │          │  小图3   │
       └──────────┴──────────┘
       
       请提供：
       1. 标题文字
       2. 大图文件名
       3. 三张右侧小图的文件名
```

#### 2.2.3 布局微调选项

每页创建时提供三级调整：

**Level 1 - 框架调整**
- 修改整体布局类型（单列/双列/三列）
- 切换左右/上下分布
- 添加/删除列

**Level 2 - 内容调整**
- 图片位置：左/右/居中
- 图片宽度：30%/40%/50%/60%/70%
- 文字对齐：左对齐/居中/右对齐/两端对齐
- 文字字号：small/normal/large

**Level 3 - 间距调整**
- 垂直间距：紧凑/标准/宽松
- 列间距：窄/标准/宽
- 页边距：窄/标准/宽

---

## 3. 多项目管理

### 3.1 项目结构

每个 PPT 项目是一个独立的目录：

```
my-presentation/
├── main.tex              # 主文件（始终可编译）
├── beamer-skill.json     # 项目配置和元数据
├── figures/              # 图片资源目录
│   ├── results.png
│   └── diagram.pdf
└── .beamer-skill/        # Skill 工作目录
    ├── snapshots/        # 撤销/重做快照
    │   ├── snapshot-001.json
    │   ├── snapshot-002.json
    │   └── snapshot-003.json
    ├── preview/          # 预览文件
    │   └── page-03.png
    └── logs/             # 编译日志
        └── compile-20260322-143022.log
```

### 3.2 项目初始化

**新建项目：**
```
[用户] 新建一个PPT项目，叫"毕业论文答辩"

[Skill] 创建项目目录：./毕业论文答辩/
       初始化文件结构...
       请选择主题：
       A) 学术简约 (metropolis)
       B) 经典学术 (Madrid)
       C) 现代商务 (Berlin)
       D) 其他
```

**打开现有项目：**
```
[用户] 打开项目"毕业论文答辩"

[Skill] 检测到现有项目，包含 12 页：
       第1页: 封面 ✓
       第2页: 目录 ✓
       第3页: 研究背景 ✓
       ...
       第12页: 致谢 ✓
       
       您想：
       A) 继续编辑下一页
       B) 修改已有页面
       C) 插入新页面
       D) 查看完整PDF
```

### 3.3 多项目切换

支持在会话中切换不同项目：

```
[用户] 切换到项目"组会汇报"

[Skill] 当前项目"毕业论文答辩"已保存。
       切换到"组会汇报"...
       该包含 5 页，上次编辑到第3页。
       
       您想：
       A) 从第3页继续
       B) 查看完整结构
       C) 返回"毕业论文答辩"
```

### 3.4 项目配置 (beamer-skill.json)

```json
{
  "version": "1.0",
  "name": "毕业论文答辩",
  "created_at": "2026-03-22T14:30:00Z",
  "last_modified": "2026-03-22T16:45:00Z",
  "settings": {
    "theme": "metropolis",
    "color_theme": "seahorse",
    "aspect_ratio": "169",
    "font_size": "11pt",
    "language": "chinese",
    "compiler": "xelatex"
  },
  "slides": [
    {
      "id": 1,
      "type": "title",
      "status": "confirmed",
      "frame_comment": "Slide 1: Title Page"
    },
    {
      "id": 2,
      "type": "content",
      "status": "confirmed",
      "frame_comment": "Slide 2: Research Background"
    }
  ],
  "current_slide": 3,
  "snapshot_index": 5
}
```

---

## 4. 语言与排版支持

### 4.1 语言选择策略

**重要原则**：PPT 内容语言与对话语言完全独立。用户在项目开始时选择 PPT 的语言，后续无论使用什么语言与 AI 对话，PPT 内容都将使用选定的语言。

**选择时机**：
```
[Skill] 欢迎使用 Beamer PPT 助手！

请选择演示文稿的语言：
A) 中文（简体）- 启用 ctex 宏包，优化中文排版
B) 中文（繁体）- 启用 ctex 宏包，使用繁体字体
C) English - Standard English typesetting
D) 其他语言（请指定）

注意：这将决定 PPT 内容的语言，与我们的对话语言无关。
例如：您可以用中文与我交流，但生成英文 PPT。
```

**使用示例**：
```
[用户] 帮我做一个PPT

[Skill] 请选择演示文稿的语言：
       A) 中文  B) English  C) 其他

[用户] B

[Skill] 已选择：English
       现在开始创建英文演示文稿。
       （您可以用中文与我交流，我会生成英文内容）
       
       请输入标题：

[用户] 基于深度学习的研究

[Skill] 生成英文标题：
       "Research Based on Deep Learning"
       
       是否修改？
       A) 使用此标题
       B) 输入英文标题
       C) 翻译成其他表达
```

### 4.2 中文支持配置

当用户选择中文时，自动启用以下配置：

**LaTeX 导言区代码：**
```latex
\documentclass[aspectratio=169,11pt]{beamer}

% 中文支持
\usepackage{ctex}

% 根据操作系统自动选择字体
\IfFileExists{./.font-config.tex}{
  \input{./.font-config.tex}
}{
  % Windows
  \IfFontExistsTF{SimSun}{
    \setCJKmainfont{SimSun}
    \setCJKsansfont{SimHei}
  }{
    % macOS
    \IfFontExistsTF{PingFang SC}{
      \setCJKmainfont{PingFang SC}
      \setCJKsansfont{PingFang SC}
    }{
      % Linux - 使用 Fandol 或 Noto
      \setCJKmainfont{Noto Serif CJK SC}
      \setCJKsansfont{Noto Sans CJK SC}
    }
  }
}

% 中文排版优化
\xeCJKsetup{checksingle=true}  % 避免单字成行
\linespread{1.3}               % 行间距
```

### 4.3 字体回退策略

如果自动配置的字体不可用：

```
[Skill] ⚠️ 系统缺少推荐的中文字体。

可用选项：
A) 使用系统默认字体（可能显示效果不佳）
B) 安装推荐字体（提供各平台安装指南）
C) 自定义字体路径（指定字体文件位置）
D) 使用 Overleaf 兼容配置（Fandol 字体）
```

### 4.4 中文排版优化

- **标点挤压**: 自动处理中英文标点间距
- **段落缩进**: 符合中文习惯的段首缩进（2字符）
- **行首行尾**: 避免标点出现在行首
- **数字与单位**: 自动添加合适的间距（如"3 mm"）
- **中西文混排**: 自动在中西文之间添加小间距

### 4.5 多语言混合处理

即使选择单一语言，也支持有限的混合内容：

**中文 PPT 中的英文内容：**
- 自动使用西文字体（Latin Modern 或 Times）
- 保持合适的字距和间距

**英文 PPT 中的中文内容：**
- 如果检测到中文，提示是否切换语言设置
- 或按原样输出（依赖用户手动配置字体）

### 4.6 主题预设

**中文优化主题：**
- **学术简约**: 1.3倍行距，中文段落缩进，适合论文答辩
- **商务演示**: 醒目标题，适合屏幕阅读，列表样式优化

**英文标准主题：**
- **Academic Classic**: 标准学术风格
- **Business Modern**: 现代商务风格
- **Minimal Clean**: 极简风格

---

## 5. 撤销/重做机制

### 5.1 状态快照系统

**快照触发时机：**
- 每完成一页并确认后
- 每次重大修改前（批量修改、主题切换）
- 用户显式要求保存检查点

**快照内容：**
```json
{
  "timestamp": "2026-03-22T14:30:00Z",
  "description": "完成第3页创建",
  "main_tex_hash": "a1b2c3d4...",
  "main_tex_content": "...",
  "slides_state": [...],
  "figures_snapshot": {
    "results.png": "hash:abc123...",
    "diagram.pdf": "hash:def456..."
  }
}
```

### 5.2 撤销/重做操作

**对话式操作：**
```
[用户] 撤销上一步

[Skill] 撤销：第3页的创建
       恢复到：完成第2页后的状态
       
       当前状态：
       第1页: 封面 ✓
       第2页: 目录 ✓
       
       您想：
       A) 重新创建第3页
       B) 继续撤销（回到第1页）
       C) 查看历史记录
```

**历史记录查看：**
```
[用户] 查看历史记录

[Skill] 项目历史记录：
       
       [6] 16:45 完成第5页创建 ← 当前
       [5] 16:30 修改第4页布局
       [4] 16:15 完成第4页创建
       [3] 15:50 修改主题颜色
       [2] 15:30 完成第3页创建
       [1] 15:00 完成第2页创建
       [0] 14:30 创建项目
       
       输入编号回退到该状态，或输入"撤销"回退一步
```

### 5.3 快照管理

**自动清理策略：**
- 保留最近 20 个快照
- 保留每次"确认完成"的快照（长期保存）
- 超过 50 个快照时，删除最早的中间状态

**显式保存检查点：**
```
[用户] 保存检查点，命名为"最终版本提交前"

[Skill] 检查点已保存。
       您可以在任何时候说"恢复到检查点'最终版本提交前'"来回退
```

### 5.4 跨会话恢复

如果 AI 会话中断：

```
[用户] 继续上次的编辑

[Skill] 发现未完成的编辑会话（3小时前）
       项目：毕业论文答辩
       进度：已完成 5 页，正在编辑第 6 页
       
       A) 恢复到中断前的状态
       B) 从第5页确认后的快照恢复
       C) 放弃并重新开始
```

---

## 6. 异常处理

### 6.1 编译错误处理

#### 6.1.1 错误分类与处理

| 错误类型 | 检测方式 | 自动修复 | 用户提示 |
|---------|---------|---------|---------|
| 图片文件不存在 | 正则匹配 `File not found` | 尝试常见路径 | "找不到 figures/results.png，是否在其他位置？" |
| 编译超时 | 超时检测（60秒） | 分割长页面 | "此页内容过多，建议分页或简化" |
| 字体缺失 | 匹配 `font not found` | 自动回退 | "字体 xxx 缺失，已使用备用字体" |
| 宏包缺失 | 匹配 `File .* not found` | 无 | "缺少宏包 xxx，请运行: tlmgr install xxx" |
| 数学公式错误 | 匹配 `Missing $` 等 | 尝试包裹 `$` | "公式语法错误，已尝试修复" |
| 特殊字符未转义 | 匹配 `Undefined control sequence` | 转义特殊字符 | "文本中包含 LaTeX 特殊字符，已自动转义" |

#### 6.1.2 编译错误恢复流程

```
[编译失败]
   ↓
[解析错误日志] → 分类错误类型
   ↓
[尝试自动修复] → 成功？→ [重新编译]
   ↓ 失败
[向用户展示]
   
"编译出错：
 ❌ 错误1: 图片文件 'result.png' 不存在
    位置: 第3页，第15行
    建议: 请确认图片是否在 figures/ 目录中
 
 ❌ 错误2: 未定义的命令 '\beamerbutton'
    位置: 第5页，第22行
    建议: 缺少 hyperref 宏包，已自动添加
 
请修正后输入'重试'，或输入'跳过此页'继续"
```

### 6.2 文件系统错误

#### 6.2.1 磁盘空间不足

```
[Skill] ⚠️ 磁盘空间不足
       当前可用空间: 150MB
       预计需要: 300MB（包含编译临时文件）
       
       建议操作：
       A) 清理旧的编译临时文件（可回收 200MB）
       B) 使用外部存储（指定其他路径）
       C) 简化图片质量（降低预览图分辨率）
```

#### 6.2.2 文件权限问题

```
[Skill] ⚠️ 无法写入文件
       路径: ./毕业论文答辩/main.tex
       原因: 权限不足
       
       建议操作：
       A) 修改目录权限: chmod 755 ./毕业论文答辩
       B) 使用其他目录（如 ~/Documents/presentations/）
       C) 以管理员权限运行（不推荐）
```

#### 6.2.3 文件名特殊字符

```
[Skill] ⚠️ 文件名包含特殊字符
       问题文件: "result (1).png"
       
       LaTeX 对文件名有特殊要求，建议：
       A) 自动重命名为 "result_1.png"
       B) 手动重命名（仅使用字母、数字、下划线）
```

### 6.3 图片资源错误

#### 6.3.1 图片损坏

```
[Skill] ⚠️ 图片文件可能已损坏
       文件: figures/diagram.pdf
       错误: 无法读取 PDF 元数据
       
       建议操作：
       A) 尝试用其他工具重新导出图片
       B) 转换为 PNG 格式（可能损失矢量特性）
       C) 跳过此图片，先完成其他部分
```

#### 6.3.2 图片尺寸过大

```
[Skill] ⚠️ 图片文件过大
       文件: figures/photo.jpg (15.2MB)
       建议: 压缩至 2MB 以下以提高编译速度
       
       A) 自动压缩（可能降低质量）
       B) 手动压缩后替换
       C) 保持原样（编译可能较慢）
```

### 6.4 环境检测与提示

#### 6.4.1 LaTeX 环境检测

首次启动时检测：

```
[Skill] 正在检测 LaTeX 环境...
       
       ✓ xelatex 已安装 (版本: 2023)
       ✓ bibtex 已安装
       ✓ ctex 宏包已安装
       ⚠️ minted 宏包未安装（代码高亮功能受限）
       
       环境检测完成，可以开始使用！
       （可选）安装缺失宏包: tlmgr install minted
```

#### 6.4.2 编译器选择

如果 xelatex 不可用：

```
[Skill] ⚠️ xelatex 未检测到
       
       可用选项：
       A) 安装 TeX Live（推荐）- 提供安装指南
       B) 使用 lualatex（如果已安装）
       C) 使用 pdflatex（不支持中文，仅英文内容）
       D) 仅生成 .tex 文件，用户自行编译
```

### 6.5 网络与依赖

#### 6.5.1 宏包自动安装

```
[Skill] 检测到缺少宏包: "tikz"
       
       尝试自动安装...
       ❌ 自动安装失败（无网络连接）
       
       请手动安装：
       tlmgr install tikz
       
       或稍后处理（不使用 tikz 功能）
```

---

## 7. 用户操作灵活性

### 7.1 批量修改

支持一次性修改多个页面的属性：

```
[用户] 把所有页面的字体改成14号

[Skill] 批量修改：字体大小 → 14pt
       影响范围：第 2-12 页（共11页）
       第1页（封面）保持默认
       
       确认执行？
       A) 确认修改
       B) 预览效果（编译第3页作为示例）
       C) 选择特定页面
       D) 取消
```

**支持的批量操作：**
- 字体大小（全局或部分页面）
- 颜色主题（统一切换）
- 行间距
- 页边距
- 页脚显示/隐藏
- 页码显示/隐藏

### 7.2 页面重排序

```
[用户] 把第3页移到第5页后面

[Skill] 页面重排序：
       
       原顺序: 1  2  [3]  4  5  6  7
       新顺序: 1  2  4  5  [3]  6  7
       
       涉及页面：
       - 第3页: 研究方法
       - 第4页: 实验设计（前移1位）
       - 第5页: 结果分析（前移1位）
       
       确认重排序？
       A) 确认
       B) 查看调整后的完整结构
       C) 撤销
```

**其他重排序操作：**
- 移动到指定位置：`把第5页移到第2页之前`
- 交换两页：`交换第3页和第7页`
- 批量移动：`把第8-10页移到最前面`

### 7.3 复制页面

```
[用户] 复制第2页作为新页面

[Skill] 复制页面：
       源页面: 第2页 - 目录
       
       新页面插入位置：
       A) 作为第3页（当前第3页及之后后移）
       B) 作为最后一页
       C) 指定位置：第___页之后
       
       复制内容：
       ✓ 页面布局
       ✓ 文字内容
       ✓ 格式设置
       
       是否在新页面中修改内容？
       A) 先创建副本，稍后编辑
       B) 立即编辑新页面内容
```

**复制选项：**
- 完全复制（内容 + 布局）
- 仅复制布局（清空内容）
- 复制并递增编号（如从"实验1"到"实验2"）

### 7.4 页面模板保存

```
[用户] 把当前页面布局保存为模板

[Skill] 保存页面模板：
       
       模板名称: 三栏图文混排
       描述: 顶部标题 + 三栏并排（左图中文右图）
       
       适用场景：
       A) 仅当前项目使用
       B) 保存到全局模板库（所有项目可用）
       
       模板预览：
       ┌─────────────────────┐
       │      标题           │
       ├────────┬───┬────────┤
       │  图片  │文 │  图片  │
       │        │字 │        │
       └────────┴───┴────────┘
       
       保存成功！下次创建页面时可选择此模板。
```

### 7.5 快速操作命令

为熟练用户提供快捷命令：

```
[用户] /next
[Skill] 进入下一页创建流程...

[用户] /preview
[Skill] 重新编译并显示当前页预览

[用户] /list
[Skill] 显示所有页面列表：
       1. 封面 ✓
       2. 目录 ✓
       3. 研究背景 ✓
       4. 方法介绍 ← 当前编辑
       5. [空]
       ...

[用户] /goto 7
[Skill] 跳转到第7页

[用户] /delete
[Skill] 删除当前页面？
       A) 确认删除
       B) 删除并保存为模板
       C) 取消

[用户] /theme
[Skill] 切换主题：
       当前: metropolis
       可用: Madrid, Berlin, CambridgeUS, ...
```

### 7.6 内容导入

```
[用户] 从文件导入内容

[Skill] 导入内容：
       
       支持格式：
       A) Markdown 文件（自动转换）
       B) 纯文本文件
       C) 现有 .tex 文件（提取 frame）
       D) Word 文档（需安装 pandoc）
       
       请选择文件：
       [列出当前目录下的可用文件]
       
       或粘贴内容：
       [支持直接粘贴文本]
```

---

## 8. 技术实现细节

### 8.1 LaTeX 代码生成规范

**Frame 注释规范：**
```latex
% ============================================
% Slide 1: Title Page
% ============================================
\begin{frame}
\titlepage
\end{frame}

% ============================================
% Slide 2: Table of Contents
% ============================================
\begin{frame}{Outline}
\tableofcontents
\end{frame}

% ============================================
% Slide 3: Introduction
% ============================================
\begin{frame}{研究背景}
\begin{columns}
\column{0.5\textwidth}
\includegraphics[width=\textwidth]{./figures/background.png}

\column{0.5\textwidth}
\begin{itemize}
  \item 机器学习在医疗领域的应用
  \item 深度学习的发展
  \item 研究动机与目标
\end{itemize}
\end{columns}
\end{frame}
```

**代码组织原则：**
- 每页之间用空行和注释分隔
- 使用语义化的 frame 标题注释
- 缩进统一使用2个空格
- 图片路径使用相对路径 `./figures/`

### 8.2 编译流程

**标准编译链：**
```bash
# 标准编译（无参考文献）
xelatex -interaction=nonstopmode -file-line-error main.tex

# 带参考文献的编译
xelatex -interaction=nonstopmode -file-line-error main.tex
bibtex main
xelatex -interaction=nonstopmode -file-line-error main.tex
xelatex -interaction=nonstopmode -file-line-error main.tex
```

**预览提取：**
```bash
# 提取特定页为图片
pdftoppm -f <page> -l <page> -png -r 150 main.pdf preview-page-<page>.png

# 或使用 ImageMagick
convert -density 150 main.pdf[<page-1>] preview-page-<page>.png
```

### 8.3 状态持久化

**内存状态结构：**
```typescript
interface ProjectState {
  name: string;
  settings: {
    theme: string;
    colorTheme: string;
    aspectRatio: string;
    fontSize: string;
    language: 'chinese' | 'english';
    compiler: 'xelatex' | 'lualatex' | 'pdflatex';
  };
  slides: Slide[];
  currentSlideIndex: number;
  figures: Map<string, FigureInfo>;
}

interface Slide {
  id: number;
  type: 'title' | 'toc' | 'section' | 'content' | 'final';
  layout: LayoutConfig;
  content: ContentData;
  status: 'draft' | 'confirmed';
  frameComment: string;
}
```

---

## 9. 文件结构

### 9.1 Skill 目录结构

```
beamer-skill/
├── SKILL.md                     # 主技能文件
├── README.md                    # 英文说明
├── README_zh.md                 # 中文说明
├── references/                  # 参考资料
│   ├── latex-basics.md         # LaTeX 基础知识
│   ├── beamer-themes.md        # Beamer 主题参考
│   ├── layout-patterns.md      # 布局模式库
│   └── chinese-typesetting.md  # 中文排版指南
├── assets/                      # 模板资源
│   ├── templates/              # 预设模板
│   │   ├── academic-thesis/    # 学术论文答辩
│   │   ├── business-report/    # 商务汇报
│   │   ├── course-lecture/     # 课程讲义
│   │   └── conference-talk/    # 学术会议报告
│   └── examples/               # 示例项目
│       ├── example-academic/   # 学术示例
│       └── example-business/   # 商务示例
└── scripts/                    # 辅助脚本（可选）
    ├── check-environment.py    # 环境检测
    └── setup-fonts.py          # 字体配置
```

### 9.2 项目模板结构

**学术论文答辩模板：**
```
templates/academic-thesis/
├── template.json               # 模板配置
├── preview.png                 # 模板预览图
└── boilerplate.tex             # 模板代码
```

**template.json:**
```json
{
  "name": "学术论文答辩",
  "name_en": "Academic Thesis Defense",
  "description": "适合硕士/博士论文答辩的学术模板",
  "category": "academic",
  "pages": [
    {"type": "title", "name": "封面", "required": true},
    {"type": "toc", "name": "目录", "required": true},
    {"type": "section", "name": "章节分隔页", "required": false},
    {"type": "content", "name": "内容页", "required": true},
    {"type": "final", "name": "致谢/结束页", "required": true}
  ],
  "default_theme": "metropolis",
  "default_color": "seahorse",
  "aspect_ratio": "169"
}
```

### 9.3 布局脚本库 (scripts/layouts/)

为节省 token 并提高常用布局的生成效率，skill 内置经典布局脚本库。

#### 9.3.1 脚本库结构

```
scripts/
└── layouts/                    # 经典布局脚本
    ├── single-column/          # 单列布局
    │   ├── text-only.tex       # 纯文字
    │   ├── bullet-list.tex     # 项目列表
    │   └── numbered-list.tex   # 编号列表
    ├── two-column/             # 双列布局
    │   ├── image-left.tex      # 左图右文
    │   ├── image-right.tex     # 左文右图
    │   ├── two-text.tex        # 双文字对比
    │   └── two-images.tex      # 双图片并排
    ├── three-column/           # 三列布局
    │   ├── three-images.tex    # 三图并排
    │   └── mixed.tex           # 图文混排
    └── special/                # 特殊布局
        ├── full-image.tex      # 全屏图片
        ├── centered-focus.tex  # 居中强调
        └── step-by-step.tex    # 分步展示
```

#### 9.3.2 脚本文件格式

每个布局脚本包含占位符和说明：

**scripts/layouts/two-column/image-left.tex:**
```latex
% ============================================
% Layout: Two Column - Image Left
% Description: 左图右文布局，图片占50%宽度
% Placeholders:
%   {{TITLE}}      - 页面标题
%   {{IMAGE_PATH}} - 图片路径
%   {{IMAGE_SIZE}} - 图片宽度 (默认: 0.45\textwidth)
%   {{TEXT_CONTENT}} - 右侧文字内容
% ============================================

\begin{frame}{{{TITLE}}}
\begin{columns}[T]  % T = 顶部对齐
\column{0.5\textwidth}
\includegraphics[width={{IMAGE_SIZE}}]{{{IMAGE_PATH}}}

\column{0.5\textwidth}
{{TEXT_CONTENT}}
\end{columns}
\end{frame}
```

#### 9.3.3 使用流程

**首次使用时加载脚本：**
```
[Skill] 正在加载布局模板库...
       已加载 12 个经典布局模板
       - 单列布局: 3个
       - 双列布局: 4个
       - 三列布局: 2个
       - 特殊布局: 3个
       
       这些模板将用于快速生成常用布局。
```

**生成页面时调用：**
```
[用户] 选择布局 B) 左图右文

[Skill] 使用模板: two-column/image-left
       加载占位符并填充内容...
       
       请输入：
       1. 页面标题
       2. 图片文件名
       3. 右侧文字内容
```

#### 9.3.4 Token 节省策略

**不使用脚本库时：**
- 每个布局需要 AI 生成完整 LaTeX 代码
- 平均每个布局消耗 ~500-800 tokens
- 12个布局总计 ~6000-9600 tokens

**使用脚本库时：**
- 只需加载一次脚本库 (~2000 tokens)
- 每个布局只需填充占位符 (~100 tokens)
- 总计 ~3200 tokens (节省 50%+)

**智能缓存：**
- 脚本库在 skill 初始化时加载一次
- 在同一会话中复用，不重复消耗 token
- 支持增量加载（只加载用户选择的布局类型）

#### 9.3.5 扩展脚本库

用户可以添加自定义布局脚本：

```
[用户] 保存当前页面为布局模板

[Skill] 请输入模板名称：custom-timeline
       
       请输入描述：时间轴布局，左侧时间点，右侧事件描述
       
       保存到：scripts/layouts/custom/custom-timeline.tex
       模板将在下次启动时自动加载。
```

---

## 10. 工作流程详解

### 10.1 完整会话流程

```
用户: 帮我做一个PPT

Skill: 你好！我是 Beamer PPT 助手。
      我可以帮你创建专业的 LaTeX Beamer 演示文稿。
      
      我们可以：
      A) 新建一个项目
      B) 打开现有项目
      C) 查看示例

===================================================================
[用户选择 A]

Skill: 新建项目
      请输入项目名称（如：毕业论文答辩）

[用户输入: 机器学习研讨会]

Skill: 创建项目：机器学习研讨会
      
      请选择演示文稿的语言：
      A) 中文（简体）- 启用 ctex 宏包
      B) English - Standard English typesetting
      C) 其他语言
      
      注意：这将决定 PPT 内容的语言，与我们的对话语言无关。

[用户选择 B]

Skill: 已选择：English
      现在开始创建英文演示文稿。
      （您可以用中文与我交流，我会生成英文内容）
      
      请选择使用场景：
      A) 学术汇报（论文答辩、组会报告）
      B) 商务演示（产品介绍、项目汇报）
      C) 课程教学（课堂讲义、教程）
      D) 其他

[用户选择 A]

Skill: 学术汇报场景
      
      推荐模板：
      1) 学术论文答辩 - 适合学位论文答辩 [预览]
      2) 组会研究报告 - 适合实验室组会 [预览]
      3) 学术会议报告 - 适合会议口头报告 [预览]
      4) 文献综述汇报 - 适合文献阅读和综述 [预览]
      
      请选择模板（输入编号）

[用户选择 2]

Skill: 选择模板：组会研究报告
      
      该模板包含以下页面：
      ✓ 封面（标题、作者、日期）
      ✓ 目录（自动生成）
      ✓ 研究背景
      ✓ 方法介绍
      ✓ 实验设计
      ✓ 结果分析
      ✓ 讨论与展望
      ✓ 致谢
      
      现在开始创建，请跟随我的引导...
      
      ─────────────────────────────────────
      第1页：封面
      ─────────────────────────────────────
      
      请输入报告标题：

[用户输入: 基于深度学习的医学图像分割研究]

Skill: 请输入作者姓名：

[用户输入: 张三]

Skill: 请输入单位/实验室：

[用户输入: 计算机视觉实验室]

Skill: 生成第1页代码...
      编译预览中...
      
      第1页预览：
      [图片: preview-page-1.png]
      
      满意吗？
      A) 满意，继续下一页
      B) 修改布局
      C) 修改内容
      D) 查看完整PDF

[用户选择 A]

Skill: ─────────────────────────────────────
      第2页：目录
      ─────────────────────────────────────
      
      是否包含目录页？
      A) 是（自动生成）
      B) 否

... 继续创建后续页面 ...

===================================================================
[所有页面创建完成]

Skill: 恭喜！所有页面创建完成。
      
      项目摘要：
      名称：机器学习研讨会
      页数：12页
      主题：metropolis (seahorse)
      
      可用操作：
      A) 查看完整PDF
      B) 修改某页
      C) 调整整体样式
      D) 导出项目
      E) 完成并退出
```

### 10.2 修改现有页面流程

```
用户: 修改第3页

Skill: 第3页：研究背景
      当前布局：左图右文
      
      修改选项：
      A) 修改内容
      B) 修改布局
      C) 调整样式
      D) 删除此页
      E) 复制此页

[用户选择 B]

Skill: 布局修改
      
      当前布局：左图右文
      ┌────────┬────────┐
      │  图片  │  文字  │
      │ (50%)  │ (50%)  │
      └────────┴────────┘
      
      可用布局：
      A) 右图左文（交换位置）
      B) 上图文下（改为上下分布）
      C) 单栏文字（移除图片）
      D) 双图片对比（两图并排）
      E) 自定义布局（描述你想要的）

[用户选择 E]

Skill: 请描述你想要的布局：

[用户输入: 我想把图片放大到占2/3宽度，文字在右边窄一点]

Skill: 理解了！调整为：
      ┌──────────────┬────────┐
      │     图片     │  文字  │
      │    (66%)     │ (34%)  │
      └──────────────┴────────┘
      
      重新生成代码并编译预览...
      
      [预览图]
      
      满意吗？
      A) 满意
      B) 再调整
      C) 恢复原来的布局
```

### 10.3 多语言使用场景示例

**场景：中文对话，生成英文PPT**

```
用户: 帮我做一个PPT，用于下周的国际会议汇报

Skill: 你好！我是 Beamer PPT 助手。
      我可以帮你创建专业的 LaTeX Beamer 演示文稿。
      
      我们可以：
      A) 新建一个项目
      B) 打开现有项目
      C) 查看示例

[用户选择 A]

Skill: 新建项目
      请输入项目名称（如：Conference Presentation）

[用户输入: CVPR汇报

Skill: 创建项目：CVPR汇报
      
      请选择演示文稿的语言：
      A) 中文（简体）
      B) English
      C) 其他语言
      
      注意：这将决定 PPT 内容的语言，与我们的对话语言无关。

[用户选择 B]

Skill: 已选择：English
      现在开始创建英文演示文稿。
      
      请输入报告标题：

[用户输入: 基于注意力机制的医学图像分割新方法

Skill: 生成英文标题：
       "A Novel Attention-Based Approach for Medical Image Segmentation"
       
       请输入作者姓名（英文）：

[用户输入: 我叫李明，来自清华

Skill: 生成英文信息：
       Author: Li Ming
       Institution: Tsinghua University
       
       确认或修改？

[用户输入: 确认

Skill: 好的，继续创建...
      ─────────────────────────────────────
      第2页：Introduction
      ─────────────────────────────────────
      
      请输入研究背景介绍：

[用户输入: 医学图像分割很重要，但是传统方法有局限性

Skill: 生成英文内容：
       "Medical image segmentation plays a crucial role in clinical 
       diagnosis. However, traditional methods face significant 
       limitations in handling complex anatomical structures..."
       
       是否需要调整？

... 后续页面继续用中文交流，生成英文内容 ...
```

**关键特性：**
- AI 自动将中文概念翻译为恰当的英文学术表达
- 保持专业术语的准确性
- 支持作者/机构名称的英文格式化处理
- 即使用户输入混合中英文，AI也能智能提取关键信息

**适用场景：**
- 国际会议报告（CVPR, ICML, NeurIPS等）
- 海外学术交流
- 英文课程作业
- 外企工作汇报

---

## 11. 限制与未来扩展

### 11.1 当前版本限制

**不支持的特性：**
- 复杂动画（overlay 层级、动画序列）
- 演讲者备注（\note 命令）
- HTML/PowerPoint 导出
- 实时协作编辑
- 云端同步

**性能限制：**
- 建议最大页数：50页（超过后编译时间显著增加）
- 单张图片建议 < 5MB
- 撤销历史最大保留：20个中间状态 + 所有确认点

### 11.2 未来扩展方向

**功能扩展：**
- 动画支持（简单的 \pause、\item<+->）
- 演讲者模式（双屏显示支持）
- 版本控制集成（Git 自动提交）
- 协作功能（多人编辑）
- 模板市场（用户共享模板）

**技术优化：**
- 增量编译（只编译修改的部分）
- 智能缓存（复用未变更的编译结果）
- 云端编译选项（无需本地 LaTeX）
- 实时预览（保存时自动重新编译）

---

## 12. 附录

### 12.1 快捷键速查

| 命令 | 功能 |
|-----|------|
| `/next` | 进入下一页创建 |
| `/prev` | 返回上一页 |
| `/list` | 显示所有页面列表 |
| `/goto <n>` | 跳转到第 n 页 |
| `/preview` | 重新编译预览当前页 |
| `/delete` | 删除当前页 |
| `/copy` | 复制当前页 |
| `/undo` | 撤销 |
| `/redo` | 重做 |
| `/theme` | 切换主题 |
| `/help` | 显示帮助 |

### 12.2 常见问题

**Q: 编译速度很慢怎么办？**  
A: 检查图片大小，建议压缩至2MB以下。大图片会显著影响编译速度。

**Q: 中文显示乱码？**  
A: 确保使用 xelatex 编译器。如问题持续，检查系统是否安装中文字体。

**Q: 可以导入现有的 PPT 吗？**  
A: 目前支持从 .tex 文件导入。PowerPoint 导入需要先转换为 PDF 再手动提取内容。

**Q: 如何分享我的模板？**  
A: 将项目中的 `.beamer-skill/template-xxxx.json` 文件分享给他人即可。

### 12.3 相关资源

- Beamer 官方文档：https://ctan.org/pkg/beamer
- ctex 宏包文档：https://ctan.org/pkg/ctex
- LaTeX 项目：https://www.latex-project.org/
- TeX Live 下载：https://tug.org/texlive/

---

**文档结束**

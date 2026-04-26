# Beamer 布局模式参考

本参考文档提供 Beamer 演示文稿的常用布局模式，帮助快速选择合适的排版方案。

## 设计原则

### 1. 视觉层次
- **标题优先**：每页一个核心主题，标题清晰醒目
- **逻辑递进**：内容按照重要性递减排列
- **焦点集中**：避免多个竞争元素分散注意力

### 2. F 型阅读路径
读者的视线通常遵循 F 型路径：
1. 先看顶部（标题）
2. 横向扫视左上角
3. 向下垂直浏览

设计时应将重要内容放在左上区域。

### 3. 六点原则
每页内容建议不超过 6 个要点，保持简洁易读。每个要点可以是一段话或一个子主题。

### 4. 留白与呼吸空间
- 文字与边缘保持适当距离
- 元素之间要有足够的间距
- 不要让页面显得拥挤

## 布局模式目录

### 单栏布局 (Single Column)

#### 1. 纯文本 (text-only)
**适用场景**：定义、定理、引用、概念解释

**特点**：
- 内容居中或左对齐
- 适合大段文字
- 可以配合强调样式（加粗、斜体、颜色）

**LaTeX 结构**：
```latex
\begin{frame}{标题}
    \begin{center}
        % 居中内容
    \end{center}
    \begin{block}{块标题}
        % 块内容
    \end{block}
\end{frame}
```

#### 2. 要点列表 (bullet-list)
**适用场景**：列举、步骤说明、特性介绍

**特点**：
- 使用 itemize 或 enumerate 环境
- 可配合 \pause 实现逐步显示
- 建议每层缩进不超过 2 级

**变体**：
- 普通列表：使用 itemize
- 编号列表：使用 enumerate
- 描述列表：使用 description

#### 3. 聚焦中心 (centered-focus)
**适用场景**：核心概念、重要数据、引言

**特点**：
- 单一元素占据视觉中心
- 适合大图、大标题、关键数据
- 周围大量留白

### 双栏布局 (Two Column)

#### 1. 左图右文 (image-left)
**适用场景**：图解说明、产品展示

**比例建议**：
- 图片 40% - 文字 60%
- 或图片 50% - 文字 50%

**排版要点**：
- 图片放在左侧符合阅读习惯
- 文字说明简洁，配合图片
- 图片下方可加简短注释

#### 2. 右图左文 (image-right)
**适用场景**：强调文字内容，图片作为辅助

**比例建议**：
- 文字 60% - 图片 40%
- 或文字 50% - 图片 50%

**排版要点**：
- 文字先出现，图片随后展示
- 适合概念解释后给出示例图

#### 3. 左右文字对比 (two-text)
**适用场景**：对比分析、优劣比较、前后对比

**排版要点**：
- 左右两栏结构对称
- 可使用不同颜色区分
- 每栏使用小标题引导

**LaTeX 示例**：
```latex
\begin{columns}[T]  % T 表示顶部对齐
    \begin{column}{0.48\textwidth}
        \textbf{方案 A}
        \begin{itemize}
            \item 优点 1
            \item 优点 2
        \end{itemize}
    \end{column}
    \begin{column}{0.48\textwidth}
        \textbf{方案 B}
        \begin{itemize}
            \item 优点 1
            \item 优点 2
        \end{itemize}
    \end{column}
\end{columns}
```

#### 4. 代码与效果 (code-result)
**适用场景**：技术演示、编程教学

**排版要点**：
- 左侧放代码（使用 verbatim 或 listings）
- 右侧放编译/运行结果
- 代码字体使用等宽字体

### 三栏布局 (Three Column)

#### 1. 图-文-图 (image-text-image)
**适用场景**：对比两种方案，中间文字总结

**排版建议**：
- 左右两侧放对比图片
- 中间一栏放对比结论或文字说明
- 三栏比例：30%-40%-30%

#### 2. 三个文本块 (three-text)
**适用场景**：三个并列概念、步骤三阶段

**排版建议**：
- 三栏等宽或微调（33%-34%-33%）
- 每栏使用图标或小标题区分
- 可以使用编号（1, 2, 3）或箭头连接

**LaTeX 结构**：
```latex
\begin{columns}[T]
    \begin{column}{0.31\textwidth}
        \textbf{第一步}
        % 内容
    \end{column}
    \begin{column}{0.31\textwidth}
        \textbf{第二步}
        % 内容
    \end{column}
    \begin{column}{0.31\textwidth}
        \textbf{第三步}
        % 内容
    \end{column}
\end{columns}
```

#### 3. 图-文-文 (image-text-text)
**适用场景**：图片说明 + 两点文字补充

**排版建议**：
- 左栏放图（35%）
- 中间和右栏放文字（各占约 32%）
- 文字部分可以是"优点"和"缺点"，或"现状"和"未来"

#### 4. 文-文-图 (text-text-image)
**适用场景**：两点文字铺垫，最后图片总结

**排版建议**：
- 左侧两栏放文字说明（各占约 32%）
- 右侧放图（35%）
- 适合问题描述 → 解决方案 → 效果展示 的逻辑

#### 5. 文-图-文 (text-image-text)
**适用场景**：中间图片为核心，两侧文字解释

**排版建议**：
- 中间栏放图（40%）
- 左右两侧放说明文字（各占 30%）
- 适合"左文解释输入 → 中图展示过程 → 右文说明输出"的结构

### 特殊布局 (Special)

#### 1. 全屏图片 (full-image)
**适用场景**：震撼开场、过渡页、情感渲染

**实现方式**：
```latex
\begin{frame}[plain]  % plain 隐藏页眉页脚
    \begin{center}
        \includegraphics[width=\textwidth,height=0.9\paperheight,keepaspectratio]{图片路径}
    \end{center}
\end{frame}
```

**变体**：
- 全屏图片 + 底部标题栏
- 全屏图片 + 半透明覆盖层上的文字

#### 2. 时间轴 (timeline)
**适用场景**：历史发展、项目里程碑、流程步骤

**实现方式**：
- 横向时间轴：使用 \tikz 或 tabular 环境
- 纵向时间轴：使用 itemize 配合自定义标签

**LaTeX 示例（简化版）**：
```latex
\begin{frame}{项目里程碑}
    \begin{tikzpicture}
        \draw[thick,->] (0,0) -- (10,0);
        \foreach \x/\year in {1/2020, 3/2021, 5/2022, 7/2023, 9/2024}
            \draw (\x,0.2) -- (\x,-0.2) node[below] {\year};
    \end{tikzpicture}
\end{frame}
```

#### 3. 对比表格 (comparison-table)
**适用场景**：多方案对比、特性清单

**排版建议**：
- 使用 tabular 或 table 环境
- 表头加粗，关键差异使用颜色标记
- 保持简洁，不超过 4-5 行

#### 4. 逐步揭示 (step-by-step)
**适用场景**：流程演示、算法步骤、操作指南

**实现方式**：
- 使用 \pause 或 \uncover<2->
- 配合 \only<> 实现内容替换
- 使用 \alt<> 实现条件显示

**示例**：
```latex
\begin{frame}{算法步骤}
    \begin{enumerate}
        \item 初始化参数
        \pause
        \item 迭代计算
        \pause
        \item 判断收敛
        \pause
        \item 输出结果
    \end{enumerate}
\end{frame}
```

## 模式选择决策树

```
内容类型分析
    │
    ├── 纯文字内容？
    │       ├── 是 → 单栏布局
    │       │       ├── 要点列举 → bullet-list
    │       │       ├── 核心概念 → centered-focus
    │       │       └── 大段说明 → text-only
    │       └── 否 → 继续
    │
    ├── 包含图片？
    │       ├── 1 张图 → 双栏布局
    │       │       ├── 图解释文 → image-left
    │       │       └── 文配图 → image-right
    │       ├── 2 张图 → 三栏布局 (image-text-image)
    │       └── 3+ 张图 → 考虑 gallery 或分多页
    │
    ├── 需要对比？
    │       ├── 2 项对比 → two-text
    │       └── 3 项对比 → three-text
    │
    └── 特殊需求？
            ├── 全屏展示 → full-image
            ├── 时间序列 → timeline
            ├── 表格对比 → comparison-table
            └── 逐步演示 → step-by-step
```

## LaTeX 实现技巧

### columns 环境最佳实践

```latex
\begin{columns}[T]  % 选项：T(顶部对齐)、c(居中)、b(底部对齐)
    \begin{column}{0.48\textwidth}
        % 内容
    \end{column}
    \begin{column}{0.48\textwidth}
        % 内容
    \end{column}
\end{columns}
```

**注意事项**：
- 所有 column 宽度之和不要超过 1.0\textwidth（留一点间隙）
- 使用 [T] 顶部对齐，避免内容错位
- 栏间默认有间隙，不需要手动添加间距

### minipage 高级用法

当需要更复杂的布局控制时，使用 minipage：

```latex
\begin{frame}{复杂布局}
    \begin{minipage}[t]{0.45\textwidth}
        % 左侧内容
    \end{minipage}
    \hfill  % 自动填充间距
    \begin{minipage}[t]{0.45\textwidth}
        % 右侧内容
    \end{minipage}
\end{frame}
```

### 图片处理

**缩放与对齐**：
```latex
% 宽度自适应
\includegraphics[width=\textwidth]{图片}

% 高度限制
\includegraphics[height=0.6\textheight]{图片}

% 同时限制宽高，保持比例
\includegraphics[width=0.8\textwidth,height=0.6\textheight,keepaspectratio]{图片}
```

**图片与文字基线对齐**：
```latex
\begin{columns}[c]  % c 表示居中对齐
    \column{0.5\textwidth}
    文字内容
    \column{0.5\textwidth}
    \includegraphics[width=\textwidth]{图片}
\end{columns}
```

### 响应式字体大小

当内容过多时，使用缩放：

```latex
\begin{frame}{标题}
    \small  % 或 \footnotesize、\scriptsize
    % 内容
\end{frame}
```

常用字号（从小到大）：
- \tiny
- \scriptsize
- \footnotesize
- \small
- \normalsize（默认）
- \large
- \Large
- \LARGE
- \huge
- \Huge

### 颜色与强调

```latex
\usepackage{xcolor}

% 定义主题色
\definecolor{primary}{RGB}{0,102,204}
\definecolor{accent}{RGB}{255,102,0}

% 使用
\textcolor{primary}{重点文字}
\colorbox{accent}{\textcolor{white}{高亮块}}
```

## 中文排版特别注意事项

1. **避免英文标点**：中文内容使用中文标点
2. **数字与单位**：使用正确的数字格式（如 1024×768 而非 1024x768）
3. **代码块**：代码中的注释使用中文时，确保字体设置正确
4. **行距调整**：中文需要更大的行距，使用 \linespread{1.3}

## 布局检查清单

创建每页内容前检查：

- [ ] 标题是否清晰表达页面主题？
- [ ] 内容是否遵循六点原则？
- [ ] 视觉焦点是否明确？
- [ ] 留白是否充足？
- [ ] 图片分辨率是否足够？
- [ ] 文字大小是否便于阅读（建议不小于 18pt）？
- [ ] 颜色对比度是否合适？

## 推荐组合

### 学术汇报组合
1. 标题页（centered-focus）
2. 目录页（bullet-list）
3. 研究背景（image-left）
4. 方法对比（two-text）
5. 实验结果（image-right 或 three-text）
6. 结论总结（bullet-list）

### 产品展示组合
1. 产品全图（full-image）
2. 核心特性（three-text）
3. 竞品对比（comparison-table）
4. 使用场景（image-text-image）
5. 用户评价（text-only + 引用样式）
6. 购买信息（centered-focus）

### 教学课件组合
1. 课程标题（centered-focus）
2. 学习目标（bullet-list）
3. 概念讲解（text-only）
4. 示例演示（code-result 或 image-left）
5. 练习题目（two-text：题目 + 提示）
6. 课程总结（three-text）

---

**提示**：选择布局时，优先考虑内容的逻辑关系，其次是视觉美观。没有最好的布局，只有最合适的布局。

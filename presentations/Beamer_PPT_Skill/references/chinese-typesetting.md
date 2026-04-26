# 中文排版指南

本指南详细介绍在 Beamer 中使用中文排版的配置方法和最佳实践。

## 目录

1. [字体配置](#字体配置)
2. [ctex 包详解](#ctex-包详解)
3. [中英文混排](#中英文混排)
4. [标点符号](#标点符号)
5. [常见问题](#常见问题)
6. [最佳实践示例](#最佳实践示例)

## 字体配置

### 自动字体配置

ctex 宏包会根据操作系统自动选择合适的字体：

#### Windows
```latex
\usepackage[fontset=windows]{ctex}
% 默认使用：
% - 宋体 (SimSun) 作为正文字体
% - 黑体 (SimHei) 作为无衬线字体
% - 楷体 (KaiTi) 作为等宽字体
```

#### macOS
```latex
\usepackage[fontset=mac]{ctex}
% 默认使用：
% - 华文宋体 (STSong) 作为正文字体
% - 华文黑体 (STHeiti) 作为无衬线字体
% - 华文楷体 (STKaiti) 作为等宽字体
```

现代 macOS 更推荐使用：
```latex
\usepackage[fontset=macnew]{ctex}
% 使用苹方 (PingFang SC) 等现代字体
```

#### Linux
```latex
\usepackage[fontset=ubuntu]{ctex}  % Ubuntu
\usepackage[fontset=fandol]{ctex}  % 通用（可移植性好）
% 或使用：
\usepackage[fontset=noto]{ctex}    % Noto CJK 字体
```

### 自定义字体配置

当自动配置不满足需求时，可以手动指定字体：

```latex
\usepackage{ctex}

% 设置中文字体
\setCJKmainfont{Source Han Serif SC}      % 正文字体（宋体类）
\setCJKsansfont{Source Han Sans SC}        % 无衬线字体（黑体类）
\setCJKmonofont{Source Han Mono SC}        % 等宽字体

% 如果需要更多字体变体
\setCJKfamilyfont{zhsong}{Source Han Serif SC}
\setCJKfamilyfont{zhhei}{Source Han Sans SC}
\setCJKfamilyfont{zhkai}{AR PL UKai CN}
\setCJKfamilyfont{zhfs}{FangSong}

% 使用自定义字体族
\newcommand{\songti}{\CJKfamily{zhsong}}
\newcommand{\heiti}{\CJKfamily{zhhei}}
\newcommand{\kaishu}{\CJKfamily{zhkai}}
\newcommand{\fangsong}{\CJKfamily{zhfs}}
```

### 查看可用中文字体

在终端运行以下命令查看系统安装的中文字体：

```bash
# Linux/macOS
fc-list :lang=zh

# 查看特定字体
fc-list | grep -i "song"

# 查看字体文件路径
fc-list -v "Source Han Sans SC"
```

## ctex 包详解

### 基本用法

```latex
\documentclass{beamer}
\usepackage{ctex}  % 最简单的用法

\begin{document}
\begin{frame}{中文标题}
    这是一段中文内容。
\end{frame}
\end{document}
```

### 常用选项

#### 字体集选项 (fontset)

| 选项 | 说明 | 适用平台 |
|------|------|----------|
| `windows` | Windows 系统字体 | Windows |
| `mac` | macOS 旧版字体 | macOS (10.10 之前) |
| `macnew` | macOS 新版字体 | macOS (10.11+) |
| `ubuntu` | Ubuntu 系统字体 | Ubuntu |
| `fandol` | Fandol 开源字体 | 通用 |
| `noto` | Noto CJK 字体 | 通用 |
| `founder` | 方正字体 | Windows (需安装) |
| `adobe` | Adobe 字体 | 通用 (需安装) |

#### 排版方案选项 (scheme)

```latex
\usepackage[scheme=plain]{ctex}   % 仅中文支持，不改变默认样式
\usepackage[scheme=chinese]{ctex} % 完全中文化（默认）
```

`scheme=chinese` 会自动调整：
- 章节标题为中文（如"第1章"）
- 日期格式为中文
- 图表标题为中文（如"图 1"）
- 目录为中文（如"目录"、"参考文献"）

#### 空格处理选项 (space)

```latex
\usepackage[space=true]{ctex}   % 自动在中英文间加空格（推荐）
\usepackage[space=false]{ctex}  % 不自动加空格
```

#### 其他常用选项

```latex
\usepackage[
    fontset=macnew,      % 字体集
    scheme=chinese,      % 排版方案
    space=true,          % 中英文间空格
    heading=true,        % 启用章节标题样式修改
    punct=quanjiao       % 标点格式（全角）
]{ctex}
```

### 标题样式修改

```latex
\ctexset{
    section = {
        format = \Large\heiti\color{primary},
        beforeskip = 1em,
        afterskip = 0.5em
    },
    subsection = {
        format = \large\heiti\color{secondary},
        beforeskip = 0.5em,
        afterskip = 0.3em
    }
}
```

## 中英文混排

### 自动间距

启用 `space=true` 后，ctex 会自动在中英文、中文和数字之间添加适当间距：

```latex
\usepackage[space=true]{ctex}

% 输入
这是LaTeX排版系统，版本号为3.1415926。

% 实际显示（自动加空格）
这是 LaTeX 排版系统，版本号为 3.1415926。
```

### 手动调整间距

如果需要手动控制间距：

```latex
% 使用 xeCJK 的命令
\CJKsetecglue{\hspace{0.25em}}  % 设置中英文间隙

% 临时禁用自动空格
\mbox{LaTeX}  % 将内容视为一个整体

% 零宽度空格
\hspace{0pt}
\nobreak  % 禁止在此处断行
```

### 字体大小匹配

中文字号与英文 point 的对应关系：

| 中文字号 | 英文 point | LaTeX 命令 |
|---------|-----------|-----------|
| 初号 | 42pt | \Huge |
| 小初 | 36pt | \Huge |
| 一号 | 26pt | \LARGE |
| 小一 | 24pt | \LARGE |
| 二号 | 22pt | \Large |
| 小二 | 18pt | \large |
| 三号 | 16pt | \normalsize |
| 小三 | 15pt | \normalsize |
| 四号 | 14pt | \normalsize |
| 小四 | 12pt | \small |
| 五号 | 10.5pt | \footnotesize |
| 小五 | 9pt | \scriptsize |

```latex
% 自定义中文正文字号
\renewcommand{\normalsize}{\zihao{5}}  % 五号字

% 标题字号
\ctexset{
    section/format = \zihao{-3}\heiti  % 小三号黑体
}
```

## 标点符号

### 全角与半角标点

中文排版推荐使用全角标点：

```latex
\usepackage[punct=quanjiao]{ctex}  % 全角标点（默认）
\usepackage[punct=banjiao]{ctex}   % 半角标点
\usepackage[punct=kaiming]{ctex}   % 开明式标点（部分标点居左）
```

### 常用标点注意事项

| 标点 | 说明 | 示例 |
|------|------|------|
| ， | 逗号 | 这是第一句，这是第二句 |
| 。 | 句号 | 这是一个句子。 |
| 、 | 顿号 | 苹果、香蕉、橙子 |
| ； | 分号 | 第一；第二 |
| ： | 冒号 | 例如：这是一个例子 |
| ？ | 问号 | 这是什么？ |
| ！ | 感叹号 | 太好了！ |
| " " | 引号 | "这是引用" |
| ' ' | 单引号 | '这是单引号' |
| （） | 括号 | （补充说明） |
| 《》 | 书名号 | 《红楼梦》 |

### 标点压缩

行末标点自动压缩：

```latex
\ctexset{
    punct=quanjiao,           % 全角标点
    autoindent=true,          % 自动首行缩进
    linestretch=0.1           % 行末标点压缩比例
}
```

## 常见问题

### 1. 编译错误：字体未找到

**错误信息**：
```
! Package fontspec Error: The font "SimSun" cannot be found.
```

**解决方案**：

```latex
% 方案 1：使用可移植字体集
\usepackage[fontset=fandol]{ctex}

% 方案 2：使用系统已安装的字体
\usepackage{ctex}
\setCJKmainfont{Noto Serif CJK SC}  % 根据实际可用字体调整

% 方案 3：安装缺失字体或创建配置文件
% 创建 ~/.texliveYYYY/texmf-var/fonts/conf/fonts.conf
% 添加字体目录
```

### 2. 中文无法显示或显示为方框

**可能原因**：
- 编译器不对（应使用 xelatex 或 lualatex）
- 字体确实不存在
- 字体文件损坏

**解决方案**：

```bash
# 使用 xelatex 编译
xelatex main.tex

# 检查中文字体
fc-list :lang=zh | head -20

# 安装 Fandol 字体（通用）
# Ubuntu/Debian
sudo apt-get install fonts-fandol

# macOS (使用 Homebrew)
brew install --cask font-fandol
```

### 3. 粗体中文不显示或显示不正常

**原因**：某些中文字体没有粗体版本。

**解决方案**：

```latex
% 方案 1：使用有粗体的字体
\setCJKmainfont{Source Han Serif SC}  % 思源宋体有完整字重

% 方案 2：使用伪粗体（不推荐，效果差）
\setCJKmainfont{SimSun}[AutoFakeBold=true]

% 方案 3：切换到黑体表示强调
\newcommand{\zhbf}{\heiti}  % 使用黑体代替粗体
\zhbf{这是强调文字}
```

### 4. 中文行距过小

**解决方案**：

```latex
\usepackage{ctex}
\linespread{1.3}  % 调整行距为 1.3 倍

% 或在导言区添加
\setlength{\baselineskip}{1.5em}  % 设置基线间距
```

### 5. 中文标题与 Beamer 主题冲突

**问题**：使用 ctex 后，Beamer 的标题样式可能异常。

**解决方案**：

```latex
\documentclass{beamer}

% 先加载 Beamer 主题
\usetheme{metropolis}

% 后加载 ctex，使用 plain 方案避免样式冲突
\usepackage[scheme=plain]{ctex}

% 手动设置标题中文
\renewcommand{\contentsname}{目录}
\renewcommand{\figurename}{图}
\renewcommand{\tablename}{表}
```

### 6. 参考文献中的中文显示问题

```latex
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
% 或使用
\usepackage[backend=bibtex,style=numeric]{biblatex}

% 确保 bib 文件使用 UTF-8 编码
```

## 最佳实践示例

### 示例 1：学术论文演示

```latex
\documentclass[aspectratio=169]{beamer}
\usetheme{metropolis}
\usepackage[fontset=fandol,space=true]{ctex}

% 自定义颜色
\definecolor{primary}{RGB}{0,82,147}
\definecolor{accent}{RGB}{255,102,0}

\title{\textbf{基于深度学习的图像识别研究}}
\subtitle{硕士学位论文答辩}
\author{张三}
\institute{某某大学计算机学院}
\date{\today}

\begin{document}

\begin{frame}
    \titlepage
\end{frame}

\begin{frame}{目录}
    \tableofcontents
\end{frame}

\section{研究背景}
\begin{frame}{研究背景}
    \begin{itemize}
        \item 深度学习在计算机视觉领域的突破
        \item 图像识别技术的广泛应用
        \item 现有方法的局限性
    \end{itemize}
\end{frame}

\section{研究方法}
\begin{frame}{研究方法}
    \begin{columns}[T]
        \begin{column}{0.5\textwidth}
            \textbf{传统方法}
            \begin{itemize}
                \item 手工特征提取
                \item 浅层模型
                \item 泛化能力有限
            \end{itemize}
        \end{column}
        \begin{column}{0.5\textwidth}
            \textbf{深度学习方法}
            \begin{itemize}
                \item 自动特征学习
                \item 深层网络结构
                \item 端到端训练
            \end{itemize}
        \end{column}
    \end{columns}
\end{frame}

\section{实验结果}
\begin{frame}{实验结果}
    在 CIFAR-10 数据集上，我们的方法达到了 95.2\% 的准确率，
    比基线方法提升了 3.8 个百分点。
    
    \vspace{1em}
    \begin{table}
        \centering
        \begin{tabular}{lcc}
            \toprule
            \textbf{方法} & \textbf{准确率} & \textbf{参数量} \\
            \midrule
            ResNet-18 & 91.4\% & 11M \\
            VGG-16 & 89.2\% & 138M \\
            我们的方法 & \textbf{95.2\%} & 8M \\
            \bottomrule
        \end{tabular}
        \caption{实验结果对比}
    \end{table}
\end{frame}

\section{总结与展望}
\begin{frame}{总结与展望}
    \textbf{主要贡献：}
    \begin{enumerate}
        \item 提出了新的网络结构
        \item 设计了高效的训练策略
        \item 在多个数据集上验证有效性
    \end{enumerate}
    
    \vspace{1em}
    \textbf{未来工作：}
    \begin{itemize}
        \item 扩展到更大规模数据集
        \item 探索轻量化部署方案
        \item 应用到实际场景中
    \end{itemize}
\end{frame}

\begin{frame}
    \centering
    \Huge{\textbf{谢谢！}}
    
    \vspace{2em}
    \large{Q \& A}
\end{frame}

\end{document}
```

### 示例 2：商务演示

```latex
\documentclass[aspectratio=169]{beamer}
\usetheme{metropolis}
\usepackage[fontset=windows,space=true]{ctex}

% 商务主题色
\definecolor{primary}{RGB}{51,51,51}
\definecolor{accent}{RGB}{230,0,18}

\title{\textbf{2024 年度产品发布会}}
\subtitle{智能办公解决方案}
\author{产品团队}
\date{2024年3月}

\begin{document}

\begin{frame}
    \titlepage
\end{frame}

\begin{frame}{市场洞察}
    \begin{columns}[T]
        \begin{column}{0.6\textwidth}
            \textbf{当前痛点：}
            \begin{itemize}
                \item 工作效率低下
                \item 信息孤岛严重
                \item 协作成本高昂
            \end{itemize}
        \end{column}
        \begin{column}{0.35\textwidth}
            \includegraphics[width=\textwidth]{market-data.png}
        \end{column}
    \end{columns}
\end{frame}

\begin{frame}{解决方案}
    \begin{center}
        \textbf{\Large 一站式智能办公平台}
        
        \vspace{2em}
        \begin{tikzpicture}
            \node[draw,fill=primary!20,minimum width=3cm,minimum height=1cm] at (0,0) {文档协作};
            \node[draw,fill=primary!20,minimum width=3cm,minimum height=1cm] at (4,0) {项目管理};
            \node[draw,fill=primary!20,minimum width=3cm,minimum height=1cm] at (8,0) {即时通讯};
            \draw[->,thick] (1.5,0) -- (2.5,0);
            \draw[->,thick] (5.5,0) -- (6.5,0);
        \end{tikzpicture}
    \end{center}
\end{frame}

\end{document}
```

### 示例 3：教学课件

```latex
\documentclass[aspectratio=43]{beamer}
\usetheme{Madrid}
\usepackage[fontset=fandol]{ctex}

\title{Python 编程基础}
\subtitle{第 1 课：变量与数据类型}
\author{李老师}
\institute{计算机学院}

\begin{document}

\begin{frame}
    \titlepage
\end{frame}

\begin{frame}{学习目标}
    本节课我们将学习：
    \begin{enumerate}
        \item 什么是变量
        \item Python 的基本数据类型
        \item 变量的命名规则
        \item 简单的输入输出
    \end{enumerate}
\end{frame}

\begin{frame}{什么是变量}
    \begin{block}{定义}
        变量是用于存储数据的容器。可以将变量想象成一个贴有标签的盒子，
        盒子里装着数据，标签就是变量名。
    \end{block}
    
    \vspace{1em}
    \textbf{示例：}
    \begin{verbatim}
    name = "张三"    # 字符串
    age = 20        # 整数
    score = 95.5    # 浮点数
    \end{verbatim}
\end{frame}

\begin{frame}{练习时间}
    \begin{exampleblock}{课堂练习}
        请写出以下代码的输出结果：
        \begin{verbatim}
        x = 10
        y = 20
        print(x + y)
        \end{verbatim}
    \end{exampleblock}
    
    \pause
    \vspace{1em}
    \textbf{答案：}30
\end{frame}

\end{document}
```

### 示例 4：配置文件模板

创建 `chinese-config.tex`，在项目中引用：

```latex
% chinese-config.tex
% 中文排版配置文件

% 基础中文支持
\usepackage[fontset=fandol,space=true,scheme=plain]{ctex}

% 页面设置
\setlength{\parindent}{2em}      % 段落缩进 2 字符
\linespread{1.3}                  % 行距 1.3 倍

% 标题样式
\ctexset{
    section = {
        format = \Large\heiti\bfseries,
        beforeskip = 0.8em,
        afterskip = 0.4em
    }
}

% 中文字号命令（如果需要）
\newcommand{\erhao}{\fontsize{22pt}{26.4pt}\selectfont}
\newcommand{\xiaoer}{\fontsize{18pt}{21.6pt}\selectfont}
\newcommand{\sanhao}{\fontsize{16pt}{19.2pt}\selectfont}
\newcommand{\xiaosan}{\fontsize{15pt}{18pt}\selectfont}
\newcommand{\sihao}{\fontsize{14pt}{16.8pt}\selectfont}
\newcommand{\xiaosi}{\fontsize{12pt}{14.4pt}\selectfont}
\newcommand{\wuhao}{\fontsize{10.5pt}{12.6pt}\selectfont}
\newcommand{\xiaowu}{\fontsize{9pt}{10.8pt}\selectfont}
```

在主文件中引用：

```latex
\documentclass{beamer}
\usetheme{metropolis}
\input{chinese-config}

\begin{document}
% ...
\end{document}
```

## 性能优化建议

1. **字体缓存**：首次编译会生成字体缓存，后续编译会更快
2. **按需加载**：只使用需要的字体族，避免加载全部字体
3. **系统字体 vs 打包字体**：系统字体编译快，但可移植性差；Fandol 字体可移植性好

## 总结

- 使用 `\usepackage[fontset=xxx,space=true]{ctex}` 快速启用中文支持
- 选择合适的字体集：开发用 `fandol`，生产环境用系统优化字体
- 使用 `space=true` 自动处理中英文间距
- 遇到字体问题，优先尝试 `fontset=fandol`
- 中文行距建议设置为 1.3 倍

---

**参考文档**：
- ctex 宏包文档：`texdoc ctex`
- xeCJK 宏包文档：`texdoc xecjk`
- 字体排印学：《中文排版需求》W3C 标准

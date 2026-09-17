# 学术论文六支柱方法论提取规范 (Methodology Extraction Schema)

本规范用于从学术论文（PDF、LaTeX 源码或草稿）中，完整提取并结构化解构其方法论体系。严禁将方法简化为几句空洞的文字总结，必须按以下 6 大支柱进行形式化重构。

---

## 支柱一：数学形式化与问题空间 (Problem Formalization)

提取研究的问题定义、符号系统、状态空间与目标函数。

- **输入空间与定义域**：形式化定义输入变量集 $\mathcal{X}$、条件约束 $\mathcal{C}$ 与数据分布 $\mathcal{D}$；
- **输出空间与决策变量**：形式化定义预测目标、评分变量 $\mathcal{Y} \in \mathbb{R}^k$ 或生成的变体集合；
- **数学映射与变换算子**：
  $$\mathcal{T}: (\mathcal{X}, \theta_{\text{rewriter}}, d, \text{direction}) \mapsto \tilde{\mathcal{X}}$$
- **优化目标或判别准则**：显式列出损失函数、效用函数或评估准则，禁止仅用自然语言模糊带过。

---

## 支柱二：模块解耦与分层系统架构 (Modular System Architecture)

将方法划分为清晰解耦的逻辑阶段（Phases）或功能模块（Modules），并提供明确的数据流流向。

### 标准四层架构模板：
1. **数据准备与清洗层 (Ingestion & Normalization)**：
   - 原始语料/数据源接入；
   - 过滤与分层抽样规则（如分层等距抽样、相似度比对对齐）；
   - 实体脱敏与匿名化套件。
2. **干预与重构核心层 (Intervention & Transformation Engine)**：
   - 核心算法、调度引擎或变换模块；
   - 参数空间定义（如 6 个正交干预轴、正反向双向设计）。
3. **安全拦截与结构自愈层 (Integrity & Self-Healing Guardrails)**：
   - 语法树保护与结构锚点拦截器；
   - 编译/运行报错捕获与自动重试自愈流水线。
4. **评估与决策层 (Evaluation & Downstream Execution)**：
   - 评测接口、多模型裁判或下游任务环境；
   - 双盲判定机制与多协议评估规则。

---

## 支柱三：核心算法伪代码与执行流水线 (Algorithmic Workflow & Pipeline)

必须将方法的核心执行过程提炼为可复现的算法步骤或伪代码（LaTeX `algorithm` / Python 风格伪代码）。

```latex
\begin{algorithm}[H]
\caption{受控修辞干预与多模型双盲评审算法}
\label{alg:controlled_framework}
\begin{algorithmic}[1]
\REQUIRE 种子论文集 $\mathcal{D}_{\text{seed}}$, 修辞维度空间 $\mathcal{M} = \{d_1, \dots, d_6\}$, 重写模型集合 $\mathcal{R}$, 审稿模型集合 $\mathcal{V}$, 审稿协议 $\mathcal{P} = \{\text{Standard}, \text{Strict}\}$
\ENSURE 成对评分差异矩阵 $\mathbf{\Delta} \in \mathbb{R}^{|\mathcal{D}_{\text{seed}}| \times |\mathcal{M}| \times 2 \times |\mathcal{R}| \times |\mathcal{V}| \times |\mathcal{P}|}$
\FOR{每篇论文 $P_i \in \mathcal{D}_{\text{seed}}$}
    \STATE $P_i^{\text{clean}} \leftarrow \text{AnonymizeAndVerify}(P_i)$
    \FOR{每个审稿模型 $V \in \mathcal{V}$, 协议 $p \in \mathcal{P}$}
        \STATE $S_{\text{base}}(i, V, p) \leftarrow \text{Evaluate}(P_i^{\text{clean}}, V, p)$
    \ENDFOR
    \FOR{每个维度 $d \in \mathcal{M}$, 方向 $\text{dir} \in \{+, -\}$, 重写模型 $R \in \mathcal{R}$}
        \STATE $\tilde{P}_i \leftarrow \text{AgenticRewrite}(P_i^{\text{clean}}, d, \text{dir}, R)$
        \STATE $\tilde{P}_i^{\text{valid}} \leftarrow \text{SelfHealingCompile}(\tilde{P}_i)$
        \FOR{每个审稿模型 $V \in \mathcal{V}$, 协议 $p \in \mathcal{P}$}
            \STATE $S_{\text{var}}(i, d, \text{dir}, R, V, p) \leftarrow \text{Evaluate}(\tilde{P}_i^{\text{valid}}, V, p)$
            \STATE $\Delta(i, d, \text{dir}, R, V, p) \leftarrow S_{\text{var}} - S_{\text{base}}(i, V, p)$
        \ENDFOR
    \ENDFOR
\ENDFOR
\RETURN $\mathbf{\Delta}$
\end{algorithmic}
\end{algorithm}
```

---

## 支柱四：受控变量、不变性约束与安全边界 (Control Invariants & Guardrails)

学术方法必须明确其**控制条件**与**不变性红线 (Invariants)**：

1. **内容保真软约束 (Fidelity Invariants)**：
   - 严禁篡改底层技术逻辑、算法步骤与参数配置；
   - 严禁修改原始实验数据、对比排位与实测指标；
   - 严禁凭空伪造未经测试的结论与证据边界。
2. **底层结构硬拦截 (Structural Hard Anchors)**：
   - 保护参考文献引用键值（`\cite{...}`）；
   - 保护章节/图表标签（`\label{...}`, `\ref{...}`）；
   - 保护数学公式环境、算法块、图片超链接与 `.bib` 数据源。
3. **退避与熔断策略 (Fallback Policy)**：
   - 当遇到自愈失败或接口拦截时，显式记录缺失值而非随意插补。

---

## 支柱五：评测基准、基线对比与协议设计 (Experimental Protocols & Baselines)

提取方法时必须详述验证方法有效性的协议体系：

- **基准数据集配置**：样本规模、分层区间、涵盖领域与数据分布；
- **强对比基线 (Baselines)**：对比方法的名称、版本与官方默认超参；
- **评估协议分层**：
  - *标准协议 (Standard)*：常规操作条件；
  - *严格协议 (Strict)*：强约束、抗干扰或鲁棒性对抗条件；
- **核心产出指标**：主指标（如总体评分 OA）、细项指标（完备性、贡献度、表达）、决策阈值概率（如弱录取率）。

---

## 支柱六：成对统计检验与显著性验证 (Statistical Validation)

杜绝粗糙的绝对均值比较，必须提取严格的差分与统计检验方法：

- **成对差分公式**：
  $$\Delta \mathrm{Metric}_i = \mathrm{Metric}_{\text{Treatment}, i} - \mathrm{Metric}_{\text{Control}, i}$$
- **加权聚合规则**：在各分层区间内等权重聚合，防止特定子集主导全局结论；
- **鲁棒性重采样**：采用 5,000 次论文级 Bootstrap 检验，计算 95% 置信区间；
- **秩相关性分析**：采用 Spearman 秩相关检验度量相对排序一致性。

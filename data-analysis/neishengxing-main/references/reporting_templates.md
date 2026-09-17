# Reporting Templates

## Endogeneity Section Structure

Use this order when multiple methods are available:

1. State the endogeneity concern: omitted variables, reverse causality, self-selection, measurement error, or selection into observation.
2. Explain the primary identification strategy.
3. Report IV or IV-Tobit results and diagnostics.
4. Report omitted-variable sensitivity such as Oster (2019).
5. Report many-IV/WIT or TSCI only if the applicability gate is passed.
6. Put failed or exploratory methods in appendix or internal notes, not in the main text, unless reviewers explicitly ask.

## IV Paragraph Template

为缓解潜在内生性问题，本文进一步采用工具变量法进行识别。工具变量的构造基于【说明来源：外部制度/历史地理/同群体留一法/候选工具变量池】。其识别逻辑在于，【工具变量】能够通过【信息扩散、基础设施、政策触达、同伴环境、历史供给等渠道】影响【内生解释变量】，但在控制个体特征、家庭特征、地区固定效应及其他控制变量后，不应直接影响【被解释变量】。下文同时报告第一阶段结果、弱工具变量检验和必要的过度识别检验，以考察工具变量相关性和排除限制的合理性。

## Leave-One-Out IV Paragraph Template

本文进一步构造同群体留一法工具变量。具体而言，对每个样本个体，计算其所在【村/县/市/行业】中除本个体之外其他个体【数字经济参与/核心解释变量/子指数】的平均值。该变量反映个体所处局部数字环境和同伴学习机会，能够影响其自身数字经济参与概率；同时，由于剔除了本个体自身行为，可在一定程度上缓解机械相关问题。需要说明的是，同群体工具变量仍可能受到共同冲击和空间溢出的影响，因此本文进一步控制【地区固定效应/村级控制/家庭控制】，并报告弱工具变量稳健检验作为补充。

## Oster Paragraph Template

为检验遗漏变量是否可能驱动基准结论，本文参考 Oster（2019）的系数稳定性方法，比较未加入控制变量和加入完整控制变量后的核心系数及模型解释力变化，并在设定 `Rmax = 【数值或规则】`、`delta = 【数值】` 的基础上计算调整后系数或识别区间。若调整后系数仍保持同向且识别区间不包含 0，则说明不可观测因素需要具有较强选择性才可能推翻本文结论。

## Heckman Paragraph Template

若被解释变量仅在特定样本中可观测，本文采用 Heckman 两步法检验样本选择偏误。第一步估计样本进入方程，第二步在结果方程中加入逆米尔斯比率。若逆米尔斯比率不显著，则说明当前设定下没有发现显著样本选择偏误；若显著，则应报告修正后的核心系数，并解释选择方程的排除限制。若不存在清晰的选择过程，不应使用 Heckman。

## WIT Paragraph Template

考虑到单一工具变量可能存在弱相关或局部无效问题，本文进一步构造多候选工具变量池，并参考 WIT 思路对候选工具变量进行筛选。候选池包括【列出变量】。该方法的核心思想是，在多个候选工具变量中识别相对有效的工具变量组合，并剔除可能削弱识别强度或违反排除限制的候选变量。本文报告初始候选池、有效工具变量池、剔除变量及最终估计结果；同时结合第一阶段强度、弱工具变量检验和过度识别检验判断结果是否可作为识别补充。

## Table Checklist

IV table:

- Column labels: first stage, second stage, IV-Tobit or 2SLS.
- Main coefficient: endogenous regressor in second stage.
- Excluded IV coefficients in first stage.
- Controls, fixed effects, N.
- First-stage F and KP rk Wald F.
- AR / Stock-Wright / CLR p-values if available.
- Hansen J / Sargan p-value if overidentified.
- Endogeneity test p-value if available.

Oster table:

- Short coefficient and R-squared.
- Controlled coefficient and R-squared.
- `Rmax`.
- `delta`.
- Adjusted beta or identified set.
- Whether zero is excluded.

Heckman table:

- Selection equation.
- Outcome equation.
- Lambda / inverse Mills ratio.
- Wald test.
- N and selected sample size.

WIT/TSCI table:

- Candidate IV count.
- Candidate variables.
- Effective or selected IVs.
- Dropped IVs.
- Method-specific diagnostics.
- Final coefficient and standard error.
- Conventional diagnostic comparison when available.

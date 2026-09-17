# Evaluation Scenarios

Use these scenarios to regression-test `good-story` after edits.

## Scenario 1: Abstract Diagnosis

### Prompt

```text
用 $good-story 检查这个摘要的故事是否成立，并重写一版：

我们研究了城市绿地对居民心理健康的影响。通过问卷调查和空间分析，我们发现绿地可达性与心理健康评分显著相关。研究结果说明城市绿地能改善心理健康，应在城市规划中增加绿地。
```

### Must Pass

- It should identify the overclaim: correlation is written as causation.
- It should preserve the planning relevance without claiming proven intervention effect.
- It should produce a Chinese rewrite with natural Chinese headings.

### Should Not

- It should not say green space "improves" mental health as a causal fact.
- It should not invent longitudinal or experimental evidence.

## Scenario 2: Figure Order

### Prompt

```text
用 $good-story 重排这组图，让它们形成证据链：

Figure 1: 实验地点和采样设计
Figure 2: 所有土壤理化性质
Figure 3: 微生物量变化
Figure 4: 酶活性变化
Figure 5: 溶解性有机碳变化
Figure 6: 变量相关矩阵
```

### Must Pass

- It should move from puzzle to mechanism or constraint.
- It should explain the narrative job of each figure.
- It should not merely keep the original chronology.

## Scenario 3: Cross-Domain Calibration

### Prompt

```text
用 $good-story 先做领域校准，再判断这个 AI4Science 结果应该怎么讲：

我们训练了一个材料性质预测模型，在常用 benchmark 上比 baseline 低 8% MAE。模型还能提出 20 个高分候选材料，但还没有实验验证。
```

### Must Pass

- It should flag benchmark gain versus discovery.
- It should ask for leakage, out-of-distribution, physical constraint, and prospective validation checks.
- It should frame the strongest claim as prioritization or search-space reduction, not discovery.

## Scenario 4: Biomedical Overclaim

### Prompt

```text
用 $good-story 检查这段 discussion 是否说过头：

我们的生物标志物与治疗反应显著相关，并在细胞实验中影响相关通路。因此，该标志物可用于指导临床治疗选择。
```

### Must Pass

- It should distinguish association, mechanism, biomarker validation, and clinical decision-making.
- It should rewrite toward "candidate stratification signal" or equivalent.
- It should name prospective validation as missing proof.

## Scenario 5: Ecology Is Not The Boundary

### Prompt

```text
我做的是社会科学，不是生态学。$good-story 还能用吗？请用一个社会科学例子说明怎么用。
```

### Must Pass

- It should explicitly say ecology examples are calibration packs, not skill boundaries.
- It should give a social science example with construct, sampling, identification, and rival explanation.
- It should not default to biodiversity or ecosystem examples.

## Scenario 6: Chinese Terminology

### Prompt

```text
用中文回答。请用 $good-story 帮我把这个结果讲成故事，并说明薄弱点：

遥感产品在两个流域对湿地识别的 F1 分数提高了 0.04，但城市边缘湿地误分仍然严重，跨气候区还没有验证。
```

### Must Pass

- It should use natural Chinese labels, not `Best story`, `Story spine`, `Evidence map`, or `overclaim`.
- It should identify the strongest story as validated improvement for certain wetland settings, not global wetland monitoring.
- It should name mixed pixels and missing cross-climate validation as weak points.

## Scenario 7: Early Project Candidate Stories

### Prompt

```text
用 $good-story 把这些早期结果整理成 3 个候选论文故事，并排序：

1. 一个新催化剂在小规模实验中提高反应选择性。
2. 稳定性测试只做了 20 小时。
3. 机理表征显示中间体吸附发生变化。
4. 放大合成还没有做。
```

### Must Pass

- It should rank candidate stories.
- It should avoid deployable or industrial-scale claims.
- It should prefer a mechanism or structure-property story over a scale-up story.

## Scenario 8: Rebuttal Preparation

### Prompt

```text
用 $good-story 模拟审稿人会如何攻击这个故事，并给出修补路径：

我们的政策评估发现，补贴政策后小企业贷款申请增加，因此政策改善了小企业融资环境。
```

### Must Pass

- It should identify causal identification, confounding, and outcome relevance risks.
- It should distinguish loan applications from actual financing improvement.
- It should suggest repair paths such as comparison group, timing design, robustness, or alternative outcome measures.

## Scenario 9: Source Depth

### Prompt

```text
用 $good-story 分析这篇论文的最强故事，并直接给出故事卡：

题名：Papers and patents are becoming less disruptive over time
DOI: 10.1038/s41586-022-05543-x

我现在只给你题名和 DOI。
```

### Must Pass

- It should not produce a final story card from the title, DOI, abstract, or citation metadata alone.
- It should say that a specific-paper story diagnosis needs full text or sufficiently detailed materials, including methods, results, figures, limitations, and discussion.
- If browsing or full-text access is available, it should say it will read the full accessible source first.
- If browsing or full-text access is not available, it should ask for the paper, PDF, figures, or detailed notes and may give only a provisional reading plan.

### Should Not

- It should not invent methods, data, results, figures, or reviewer risks not present in the prompt.
- It should not treat the DOI landing page, title, or abstract as enough for release-quality story diagnosis.

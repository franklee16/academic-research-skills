# 引用格式规范

本文档汇总 SciPilot-cite 支持的 5 种引用格式的完整规范、模板和真实示例。

---

## 1. IEEE

**适用领域**：电气电子工程、计算机科学、通信。
**正文标记**：`[1]`、`[1, 2]`、`[1–3]`，连续编号上标或方括号。
**列表顺序**：按正文首次出现顺序。

### 1.1 期刊文章模板

```
[N] A. Author, B. Author, and C. Author, "Paper title," Journal Name,
    vol. X, no. Y, pp. 1–10, Month Year, doi: 10.xxxx/xxxxx.
```

### 1.2 会议论文模板

```
[N] A. Author and B. Author, "Paper title," in Proceedings of Conf., Year, pp. 1–10.
```

### 1.3 书籍模板

```
[N] A. Author, Book Title. Publisher, Year.
```

### 1.4 真实示例

```
[1] A. Vaswani, N. Shazeer, and N. Parmar, "Attention is all you need,"
    in Proc. NeurIPS, 2017, pp. 5998–6008.
[2] K. He, X. Zhang, and S. Ren, "Deep residual learning for image recognition,"
    in Proc. CVPR, 2016, pp. 770–778, doi: 10.1109/CVPR.2016.90.
[3] Y. LeCun, Y. Bengio, and G. Hinton, "Deep learning," Nature, vol. 521,
    no. 7553, pp. 436–444, 2015, doi: 10.1038/nature14539.
```

### 1.5 注意事项

- **作者名**：First Initial(s) + Last Name（"A. Vaswani"）
- **超过 6 个作者**：列前 1 + "et al."
- **期刊名斜体**，会议名斜体加 "in"
- **标题**：句首字母大写，专有名词大写；用英文引号
- **DOI 全部小写**

---

## 2. APA 7th Edition

**适用领域**：心理学、教育学、社会科学。
**正文标记**：(Author, Year) 或 Author (Year) 句中嵌入。
**列表顺序**：按第一作者姓字母序。

### 2.1 期刊文章模板

```
Author, A. A., Author, B. B., & Author, C. C. (Year). Title in sentence case.
    Journal Name, Volume(Issue), Pages. https://doi.org/10.xxxx/xxxxx
```

### 2.2 会议论文模板

```
Author, A. A. (Year, Month). Paper title [Conference presentation].
    Conference Name, City, Country.
```

### 2.3 真实示例

```
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N.,
    Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need.
    Advances in Neural Information Processing Systems, 30, 5998–6008.
He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for
    image recognition. Proceedings of the IEEE Conference on Computer Vision
    and Pattern Recognition, 770–778. https://doi.org/10.1109/CVPR.2016.90
```

### 2.4 注意事项

- **作者**：Last, F. M. 顺序；最多 20 个作者后 "..., Last Author"
- **使用 sentence case**（仅首字母和专有名词大写）
- **期刊名斜体**
- **DOI 是带 https 的完整 URL**
- **&** 用于最后一个作者之前

---

## 3. Nature

**适用领域**：自然科学顶刊。
**正文标记**：上标数字 `¹`、`¹⁻³`、`¹,²`。
**列表顺序**：按正文首次出现顺序。

### 3.1 期刊文章模板

```
N. Author, A. A., Author, B. B. & Author, C. C. Title in sentence case.
   Journal Name Volume, 1–10 (Year).
```

### 3.2 真实示例

```
1. Vaswani, A. et al. Attention is all you need. Adv. Neural Inf. Process. Syst.
   30, 5998–6008 (2017).
2. LeCun, Y., Bengio, Y. & Hinton, G. Deep learning. Nature 521, 436–444 (2015).
3. Senior, A. W. et al. Improved protein structure prediction using potentials
   from deep learning. Nature 577, 706–710 (2020).
```

### 3.3 注意事项

- **作者**：Last F.M. 顺序；超过 5 人用 "et al."
- **& 连接最后一个作者**（如 LeCun, Y., Bengio, Y. & Hinton, G.）
- **期刊用标准缩写**（如 Adv. Neural Inf. Process. Syst.），斜体
- **期号不写，仅卷号**
- **年份在括号内置于条目末尾**

---

## 4. Vancouver

**适用领域**：医学、生物医学。
**正文标记**：数字 `(1)`、`(1,2)`、`(1-3)` 或上标。
**列表顺序**：按正文首次出现顺序。

### 4.1 期刊文章模板

```
N. Author AA, Author BB, Author CC. Title. Journal Name. Year;Volume(Issue):Pages.
```

### 4.2 真实示例

```
1. Vaswani A, Shazeer N, Parmar N, Uszkoreit J, Jones L, Gomez AN, et al.
   Attention is all you need. Adv Neural Inf Process Syst. 2017;30:5998–6008.
2. He K, Zhang X, Ren S, Sun J. Deep residual learning for image recognition.
   In: Proc IEEE Conf Comput Vis Pattern Recognit. 2016. p. 770–8.
3. LeCun Y, Bengio Y, Hinton G. Deep learning. Nature. 2015;521(7553):436–44.
```

### 4.3 注意事项

- **作者**：Last F M 顺序，无逗号
- **超过 6 人**用 "et al"
- **期刊用 NLM 缩写**，无斜体（也可斜体）
- **年/卷(期):页码** 紧凑格式

---

## 5. GB/T 7714-2015（中文国标）

**适用领域**：中文期刊与硕博论文。
**正文标记**：`[1]`、`[1,2]`、`[1-3]`。
**列表顺序**：可按引用顺序或著者-出版年制，本 Skill 默认引用顺序制。

### 5.1 期刊文章模板

```
[N] 作者. 题名[J]. 刊名, 年, 卷(期): 起止页码. DOI: 10.xxxx/xxxxx.
```

### 5.2 会议论文模板

```
[N] 作者. 题名[C]//会议名. 会议地, 年: 起止页码.
```

### 5.3 学位论文模板

```
[N] 作者. 题名[D]. 学校所在地: 学校, 年.
```

### 5.4 真实示例

```
[1] 余凯, 贾磊, 陈雨强, 等. 深度学习的昨天、今天和明天[J].
    计算机研究与发展, 2013, 50(9): 1799-1804.
[2] Vaswani A, Shazeer N, Parmar N. Attention is all you need[C]//
    Advances in Neural Information Processing Systems. 2017: 5998-6008.
[3] LeCun Y, Bengio Y, Hinton G. Deep learning[J]. Nature, 2015, 521(7553): 436-444.
```

### 5.5 注意事项

- **文献类型标识**：[J] 期刊、[C] 会议、[D] 学位论文、[M] 专著、[N] 报纸
- **3 人以下全列**，4 人以上前 3 + "等"
- **页码用半角 -**
- **中英文混排**时英文按英文规则、中文用全角符号

---

## 6. 自定义格式

用户提供格式说明时，按以下结构提取关键参数：

```yaml
in_text_format: "[{number}]"
multiple_citations: "[{numbers_comma_separated}]"
consecutive_citations: "[{start}-{end}]"
reference_entry:
  journal: "{authors} \"{title}\" {venue}, {year}, doi: {doi}."
  conference: "..."
  book: "..."
author_format:
  max_display: 6
  et_al_threshold: 7
  separator: ", "
  last_separator: ", and "
  name_format: initials_first  # initials_first | last_initials
```

可保存为 `assets/format_templates/custom.json`，运行时通过 `--style custom` 调用。

---

## 7. 常见错误

| 错误 | 后果 | 解决 |
|---|---|---|
| 编号跳跃 | 列表/正文不一致 | `verify Stage 7` 自动检查 |
| 同一论文多种格式混用 | 评审低分 | 通过单一 `style` 参数保证一致 |
| 引用未出现在 References | 孤儿条目 | Stage 7 双向检查 |
| 编造作者或 DOI | 学术诚信问题 | **真实性铁律强制丢弃** |
| 预印本占比过高 | 评审质疑可靠性 | 默认 `include_preprint=False` |

<div align="center">

# 中文参考文献.skill

### Chinese Reference Formatter Skill

把“只有题名”的文献，整理成可核验的中文论文参考文献和 BibTeX。

<p>
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111827">
  <img alt="GB/T 7714 style" src="https://img.shields.io/badge/GB%2FT%207714-style-2f6f4e">
  <img alt="BibTeX output" src="https://img.shields.io/badge/output-BibTeX-8b5e34">
  <img alt="Python stdlib" src="https://img.shields.io/badge/Python-stdlib-3776ab">
</p>

<p>
  <a href="#效果示例">效果示例</a>
  ·
  <a href="#安装">安装</a>
  ·
  <a href="#它解决什么">它解决什么</a>
  ·
  <a href="#工作原理">工作原理</a>
  ·
  <a href="#开发">开发</a>
</p>

</div>

---

## 一句话

人工整理参考文献时，最烦的是格式；让 AI 代劳时，最怕的是信息不可靠。

这个 skill 同时解决这两个问题：先核验公开元数据，再输出通用中文论文参考文献条目和 BibTeX。找不到明确文献时，它会直接说找不到；来源冲突时，它会给出歧义说明。

> 少调格式，不编参考文献。

---

## 效果示例

### 你输入

```text
帮我把下面这些文献补全成中文论文参考文献格式，并输出 BibTeX：

1. Semi-supervised classification with graph convolutional networks
2. Focal loss for dense object detection
3. 理想的图书馆员和信息专家的素质与形象
```

### 它输出

````text
标准参考文献：[1] Kipf T N, Welling M. Semi-supervised Classification with Graph Convolutional Networks[J]. International Conference on Learning Representations, 2017. DOI:10.48550/arXiv.1609.02907.

BibTeX：
```bibtex
@article{kipf-2017-semi-supervised-classification-graph,
  author = {Kipf, Thomas N and Welling, Max},
  title = {Semi-supervised classification with graph convolutional networks},
  journal = {International Conference on Learning Representations},
  year = {2017},
  doi = {10.48550/arXiv.1609.02907}
}
```

核验来源：https://openreview.net/forum?id=SJU4ayYgl

标准参考文献：[2] Lin T Y, Goyal P, Girshick R, et al. Focal Loss for Dense Object Detection[C]. Proceedings of the IEEE International Conference on Computer Vision, 2017:2980-2988.

BibTeX：
```bibtex
@inproceedings{lin-2017-focal-loss-dense,
  author = {Lin, Tsung-Yi and Goyal, Priya and Girshick, Ross and He, Kaiming and Dollár, Piotr},
  title = {Focal loss for dense object detection},
  booktitle = {Proceedings of the IEEE International Conference on Computer Vision},
  year = {2017},
  pages = {2980-2988}
}
```

核验来源：https://openaccess.thecvf.com/content_ICCV_2017/html/Lin_Focal_Loss_for_ICCV_2017_paper.html

标准参考文献：[3] 李炳穆. 理想的图书馆员和信息专家的素质与形象[J]. 图书情报工作, 2000, 44(2):5-8,95.

BibTeX：
```bibtex
@article{ref-2000-b65e7d86,
  author = {李炳穆},
  title = {理想的图书馆员和信息专家的素质与形象},
  journal = {图书情报工作},
  year = {2000},
  volume = {44},
  number = {2},
  pages = {5-8,95}
}
```

核验来源：https://www.lis.ac.cn/CN/Y2000/V44/I2
````

如果没有可靠匹配：

```text
未找到与“definitely not a real paper title”明确对应的公开文献。
```

如果多个来源冲突：

```text
无法确定“...”的唯一对应文献：多个来源信息冲突，无法确定唯一对应文献。
```

---

## 安装

### Codex skills 目录

```bash
git clone https://github.com/Zechang-Xiong/chinese-reference-formatter-skill.git ~/.codex/skills/chinese-reference-formatter-skill
```

如果你设置了 `CODEX_HOME`：

```bash
git clone https://github.com/Zechang-Xiong/chinese-reference-formatter-skill.git "$CODEX_HOME/skills/chinese-reference-formatter-skill"
```

### skills CLI

如果你使用 open agent skills 生态的 CLI：

```bash
npx skills add Zechang-Xiong/chinese-reference-formatter-skill
```

### 调用

```text
Use $chinese-reference-formatter-skill to format these literature titles as Chinese academic references with BibTeX.
```

中文也可以：

```text
帮我把这些文献题名补全为中文参考文献格式，并给 BibTeX。
```

---

## 它解决什么

| 痛点 | 处理方式 |
| --- | --- |
| 只有论文题名，没有完整引用 | 搜索并比对公开元数据 |
| 中英文文献格式混在一起 | 统一输出中文论文参考文献格式 |
| BibTeX 和中文参考文献不一致 | 同一份标准化 JSON 同时渲染两种结果 |
| 聚合站、预印本、正式发表版本冲突 | 权威来源优先，无法判断就标记歧义 |
| 文献根本不存在或无法确认 | 明确返回未找到，不猜测 |

---

## 支持类型

| 类型 | 标识 | 典型字段 |
| --- | --- | --- |
| 期刊论文 | `J` | 作者、题名、期刊、年、卷、期、页码、DOI |
| 会议论文 | `C` | 作者、题名、会议/论文集、年、页码 |
| 图书/专著 | `M` | 作者、书名、版次、出版地、出版社、年份 |
| 析出章节 | `M` | 章节作者、章节题名、图书题名、出版社、页码 |
| 学位论文 | `D` | 作者、题名、保存地、保存单位、年份 |
| 报告 | `R` | 作者、题名、机构、年份 |
| 标准 | `S` | 标准编号、标准名称、发布机构、年份 |
| 专利 | `P` | 申请者、专利名、国别、专利号、发布日期 |
| 报纸 | `N` | 作者、题名、报纸名、日期、版次 |
| 在线资源 | `EB/OL` | 作者、题名、发布日期、引用日期、URL |

作者和语言规则：

- 3 名及以内作者全部列出。
- 超过 3 名作者，中文文献使用 `等`，英文文献使用 `et al`。
- 中文作者名按来源保留。
- 西文作者使用姓在前、名缩写在后，例如 `Einstein A`。
- 题名和作者名默认不翻译。

---

## 工作原理

输入题名后，skill 做四步：

| 步骤 | 做什么 | 目的 |
| --- | --- | --- |
| 1. 读取规则 | 读取 `references/chinese-reference-rules.md` | 确认通用中文参考文献格式 |
| 2. 核验来源 | 比对题名、作者、年份、载体、DOI/ISBN/URL | 避免把错文献格式化得很漂亮 |
| 3. 解决冲突 | DOI、出版社、官方页面、标准/专利机构优先 | 在正式版、预印本、聚合信息之间做取舍 |
| 4. 渲染输出 | 调用 `scripts/format_reference.py` | 同时生成中文参考文献和 BibTeX |

核心设计是把“核验”和“排版”拆开：

- 核验阶段负责判断文献是否可信。
- formatter 阶段只负责把可信元数据稳定渲染。

---

## 直接运行 formatter

`scripts/format_reference.py` 不联网检索，只格式化已经核验过的元数据。

```bash
python scripts/format_reference.py --start 1 < metadata.json
```

输入可以是单个对象、对象数组，或 `{ "items": [...] }`：

```json
{
  "type": "article",
  "title": "Semi-supervised classification with graph convolutional networks",
  "authors": ["Kipf, Thomas N", "Welling, Max"],
  "journal": "International Conference on Learning Representations",
  "year": 2017,
  "doi": "10.48550/arXiv.1609.02907",
  "sources": ["https://openreview.net/forum?id=SJU4ayYgl"]
}
```

常用字段：

| 字段 | 说明 |
| --- | --- |
| `type` | 文献类型，如 `article`、`inproceedings`、`book`、`thesis`、`standard`、`online` |
| `title` | 文献题名 |
| `authors` | 作者列表，支持字符串或 `{ "family": "...", "given": "..." }` |
| `journal` / `booktitle` | 期刊名或会议/论文集名 |
| `year` | 出版年份 |
| `volume` / `issue` / `pages` | 卷、期、页码 |
| `doi` / `url` | DOI 或 URL |
| `access_date` | 在线资源引用日期 |
| `sources` | 核验来源 URL 列表 |
| `status` | `not_found` 或 `ambiguous` 时输出对应提示 |

---

## 诚实边界

这个 skill 明确不做这些事：

- 不凭题名猜测文献信息。
- 不把聚合站结果自动当成权威来源。
- 不默认翻译题名或作者名。
- 不把学校、期刊或会议的特殊细则强加到所有用户身上。
- 不自动追加到项目 `.bib` 文件，除非你明确要求。

一个参考文献工具最重要的能力不是“看起来格式对”，而是知道什么时候不能确定。

---

## 仓库结构

```text
chinese-reference-formatter-skill/
├── README.md
├── SKILL.md                              # skill 入口
├── agents/
│   └── openai.yaml                       # Codex 展示信息
├── references/
│   └── chinese-reference-rules.md        # 中文参考文献规则
└── scripts/
    ├── format_reference.py               # JSON -> 参考文献 + BibTeX
    ├── test_format_reference.py          # formatter 行为测试
    └── test_skill_content.py             # skill 内容回归测试
```

---

## 开发

formatter 仅依赖 Python 标准库。测试使用 `pytest`：

```bash
python -m pytest scripts
```

当前测试覆盖：

- 英文期刊/会议条目。
- 三名以上作者规则。
- 中文期刊条目。
- 在线资源访问日期。
- 未匹配文献提示。
- skill 身份和通用性检查。

---

## English

Chinese Reference Formatter Skill turns verified bibliographic metadata into Chinese academic references and BibTeX.

It is built for common GB/T 7714-style Chinese bibliography workflows. It verifies public metadata first, formats confirmed records, and reports uncertainty instead of inventing missing references.

```bash
git clone https://github.com/Zechang-Xiong/chinese-reference-formatter-skill.git ~/.codex/skills/chinese-reference-formatter-skill
```

```text
Use $chinese-reference-formatter-skill to format these literature titles as Chinese academic references with BibTeX.
```

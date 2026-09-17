# 人文社科写作

`humanities-writing-zh` 是一个面向中文人文社会科学论文与学术专著的写作 Skill，尤其适配文学、历史学、文献学、古典学等以文本、史料和解释为核心的文史研究。

它只保留两个工作模式：

- **学术写作**：用于提纲推演、段落起草、内容续写、结构调整和局部修订。
- **成稿复核**：用于论文、专著章节或全稿的事实、证据、论证、结构、引文和表达复核。

核心边界是：不虚构事实、文献、引文或页码，不替代作者作出学术判断；材料不足时，明确区分“已证实”“可推断”和“待核实”。

## 当前版本

- Skill ID：`humanities-writing-zh`
- 版本：`v1.0.0`
- GitHub Release 与 RedSkill 上架包使用同一份 ZIP 文件
- ZIP SHA-256：`FAEE831444788C939C8FFBFC64C24D5D589259B32F93A1F9DCB3B3F02A6D16FA`

## 安装

从本仓库的 `v1.0.0` Release 下载 ZIP，将其解压到个人 Skill 目录中的 `humanities-writing-zh` 文件夹即可。

Codex 的 Windows 用户目录通常为：

```text
%USERPROFILE%\.codex\skills\humanities-writing-zh
```

安装后可显式调用：

```text
使用 $humanities-writing-zh，按“学术写作”模式处理这段论文内容。
```

或：

```text
使用 $humanities-writing-zh，按“成稿复核”模式检查这一章。
```

本 Skill 默认不隐式触发，建议在任务中明确写出 `$humanities-writing-zh`。

## 文件结构

```text
SKILL.md
agents/
  openai.yaml
references/
  academic-writing.md
  final-review.md
```

## 版本一致性

GitHub 源码目录中的四个 Skill 文件与 RedSkill `v1.0.0` 上架包逐字节一致。本仓库额外提供的 `README.md` 仅用于公开说明，不进入 RedSkill ZIP。

## 使用与权利说明

本仓库是该 Skill 的官方版本存档与发布源。允许下载后用于个人学习、研究与写作，并可为个人需要进行修改。

未经许可，不得将本 Skill 或其实质性衍生版本重新上架、冒充原创、商业售卖，或作为付费产品的一部分再次分发。除上述个人使用许可外，未授予其他开源许可，保留所有权利。

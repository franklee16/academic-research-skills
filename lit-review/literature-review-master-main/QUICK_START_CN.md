# Literature Review Master 中文快速使用指南

这个 skill 用于文献综述、research gap 搜索、idea validation、related work 写作支持、投稿前 citation verification、reviewer attack 模拟和 journal-specific literature positioning。

它现在已经重新包装为更通用的开源版本，不再只面向某一个研究者或某一个领域。它尤其适合 quantitative research、理论研究、模型研究、数值模拟、计算实验、统计建模、概率建模、Bayesian approaches、optimisation、machine learning、AI、管理学、经济金融、市场营销、运营管理、信息系统、工程、公共政策、医疗、教育和跨学科研究。

## 常用模式

Mode 0 用于科研前的战略判断，例如要不要进入一个方向、是否值得写 working paper、是否具备投某类期刊的基本条件。

Mode A 用于只有关键词或大方向，但还没有具体 idea 的探索阶段。

Mode B 用于已经有粗略 idea 时判断是否值得做。它会找 killer paper，判断 gap 是真实 gap 还是 cosmetic variation，并给出 Pursue、Pivot 或 Drop 的冷判断。

Mode C 用于课题已经确定后建立 literature tree、direct predecessor map、methodological foundation 和 critical discussion。

Mode D 用于写 introduction、related work、discussion、limitations 或 response letter 的文献材料。

Mode E 用于投稿前 citation and evidence verification。它不只查文献是否存在，还查 citation 是否真的支持正文 claim。

Mode F 用于一段时间后更新 literature，或 framing 改变后重新扫描。

Mode G 用于模拟 hostile reviewer 攻击文献遗漏、误读和定位问题。

Mode H 用于把同一篇文章改写成不同 journal family 的文献定位。

Mode I 用于 systematic review、scoping review、bibliometric review 或 survey paper。

Mode J 用于判断没有真实数据时，一个 gap 是否还能靠 theory、simulation、computation 或 formal modelling 成立。

## 调用示例

没有具体 idea 时可以这样说。

```text
请使用 Literature Review Master 的 Mode A。
我的大方向是 [topic / keywords]。
请帮我 map literature streams，找 research gaps，识别 killer-paper risk，并给出候选课题和 ROI 排名。
```

有粗略 idea 时可以这样说。

```text
请使用 Mode B 和 Mode J。
我的 idea 是……
我目前的 evidence 是 [真实数据 / 公开数据 / 理论模型 / 数值模拟 / 计算实验 / 暂无数据]。
请做 killer paper scan、framework-vs-cosmetic test、no-data viability check，并给出 Pursue、Pivot 或 Drop 的判断。
```

写 related work 时可以这样说。

```text
请使用 Mode C 和 Mode D。
目标 journal family 是……
请建立 literature tree、claim-citation map、closest-predecessor table，并给出 related work 写作计划。
```

投稿前核验引用时可以这样说。

```text
请使用 Mode E。
第一步只抽取所有需要 citation 或内部证据支持的 claims。
第二步再逐条核验 citation、metadata、版本风险、claim support、数字、表格、图和 appendix support。
最后给出 PASS、PASS WITH MINOR FIXES、MAJOR REPAIR REQUIRED 或 UNSAFE FOR SUBMISSION。
```

## ABS 数据库

skill 内置 AJG 2024 评级为 4*、4 和 3 的期刊数据库。期刊评级只作为搜索优先级和 coverage 工具，不代表某篇文献一定相关。

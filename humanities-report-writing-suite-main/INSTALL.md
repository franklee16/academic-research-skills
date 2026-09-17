# 给接收此压缩包的 AI

这是一个多 Skill 安装包，不是单个 Skill。安装前先检查全部文件。本包不含可执行脚本，不需要运行任何程序。

## 安装目标

把 `skills` 目录下的四个文件夹分别安装到当前平台的用户级 Skill 目录。安装完成后的结构应为：

```text
<用户级 Skill 目录>/
|-- humanizer/SKILL.md
|-- source-grounded-research/SKILL.md
|-- word-report-delivery/SKILL.md
`-- humanities-report-writer/SKILL.md
```

## 必须执行的安装顺序

1. 阅读 `MANIFEST.json`，确认四个 Skill 和依赖关系完整。有哈希工具时，核对完整 `humanizer` 的两个 SHA-256 值。
2. 检测当前 AI 平台支持的 Skill 安装方式和用户级 Skill 目录。优先使用平台自带的安装功能；可以访问文件系统时，再复制文件夹。
3. 按以下顺序安装：`humanizer`、`source-grounded-research`、`word-report-delivery`、`humanities-report-writer`。
4. 如果目标目录已经存在同名 Skill，不得直接覆盖。比较版本和内容，向用户报告冲突，得到明确指示后再处理。
5. 安装后重新加载 Skill。平台需要重启时，明确告诉用户。
6. 逐个检查文件夹名、`SKILL.md` 中的 `name`、清单中的名称是否一致。
7. 完成下面的只读测试，并报告安装路径、已加载的 Skill、冲突和未通过项目。

如果当前 AI 没有安装权限，不得声称已经安装。应说明受限原因，并给出平台实际可用的手动安装入口或目标目录。

## 安装后测试

先让系统回答以下三个问题，不生成正式报告：

1. 中文报告终稿由哪个 Skill 做最后一次自然化审校？正确答案应为 `humanizer`，并使用 embedded mode。
2. 用户要求联网学习优秀范例、核验最新政策或补参考文献时，应加载哪个 Skill？正确答案应为 `source-grounded-research`。
3. 用户要求最终交付 Word 时，应加载哪个 Skill？正确答案应为 `word-report-delivery`。

再用下面的测试请求检查主 Skill 能否正确路由：

```text
请使用 humanities-report-writer。我要把一个包含问卷、访谈和政策材料的文件夹写成正式中文调研报告，需要先联网学习范例，最终交付 Word。现在只说明你会加载哪些依赖 Skill，以及在材料不足时如何处理，不要开始写作。
```

正确结果应同时提到三个依赖 Skill，并明确不编造缺失事实。

## 日常调用

安装完成后，用户只需说：

```text
请使用 humanities-report-writer。材料在这里：[文件夹或附件]。用途是：[课程、评选、结项或其他]。请先读完材料，缺失问题一次问完，最后生成可以提交的 Word。
```

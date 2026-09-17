# 参与贡献

这个项目接受问题报告、文档修正、兼容性补充和 Skill 改进。提交内容应围绕人文社科报告的材料审读、事实控制、来源核验、中文写作和 Word 交付，不要把无关功能并入主流程。

## 提交 Issue

请先搜索现有 Issue，确认问题没有重复。错误报告应写明：

- 使用的 AI 或代理框架及版本
- 安装方式和操作系统
- 实际使用的 Skill
- 可以复现问题的最小材料或步骤
- 预期结果和实际结果

公开 Issue 不要上传真实姓名、联系方式、学号、未公开问卷、访谈原文或其他敏感材料。安全问题请使用 `SECURITY.md` 中的私密报告方式。

## 提交 Pull Request

1. 从 `main` 创建单独分支。
2. 只修改与本次问题有关的文件。
3. 说明修改原因、适用场景和验证方法。
4. 保持 Skill 文件夹名与 `SKILL.md` frontmatter 中的 `name` 一致。
5. 新增或修改中文说明时，不得加入无法核验的事实、来源或兼容性承诺。
6. 更新安装包内容时，同步检查 `MANIFEST.json`、`INSTALL.md` 和版本记录。

## 第三方 `humanizer`

`skills/humanizer` 来自 `blader/humanizer`。普通改进不要直接修改随包副本。升级该依赖时需要：

1. 记录新的上游提交和版本。
2. 保留上游 MIT 许可及版权声明。
3. 更新 `MANIFEST.json` 和 `NOTICE.md` 中的哈希。
4. 说明上游差异，并确认主 Skill 的 embedded mode 调用仍然有效。

## 本地检查

先运行：

```bash
python scripts/validate_bundle.py
```

再确认：

- 四个 Skill 都有有效的 `SKILL.md`。
- 主 Skill 提到的依赖名称真实存在。
- Word 模板是有效的 `.docx` 文件。
- 安装包不含构建脚本、临时文件、调试输出或个人材料。
- README、清单、安装说明和 Release 中的版本一致。

提交 Pull Request 即表示你有权提供相关内容，并同意按照本仓库的 MIT License 发布贡献。

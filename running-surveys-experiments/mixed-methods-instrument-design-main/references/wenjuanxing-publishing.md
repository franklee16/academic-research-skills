# 问卷星草稿推送与在线管理

## 适用边界

仅在用户明确要求“推送到问卷星”“创建在线问卷”“上线管理”时读取并执行本文件。默认交付仍是一份完整 Word；JSONL、manifest、命令和校验日志均为内部工作材料。

问卷表单可以推送到问卷星。人工主持的半结构化访谈提纲继续保留在 Word 中。若用户明确要求问卷星 AI 访谈，先说明该产品的网页端能力与普通问卷不同，并单独核查当时可用的官方接口，不得把普通问卷 API 当作 AI 访谈 API。

## 官方工具选择

优先使用问卷星官方 `wjx-cli`，底层为官方 `wjx-api-sdk`。官方 MCP 与 CLI 能力相近，但 MCP npm 包已退出主发版节奏；除非当前客户端已稳定配置最新版 MCP，否则使用 CLI。

权威来源：

- 官方开源仓库：https://github.com/wjxcom/wjx-ai-kit
- 官方 AIKit 帮助：https://www.wjx.cn/help/help.aspx?catid=136
- 官方 API 总览：https://www.wjx.cn/help/help.aspx?helpid=333
- 官方 AI 访谈说明：https://www.wjx.cn/help/help.aspx?catid=138

环境要求：Node.js 20+、`wjx-cli`、问卷星 API Key。密钥只能放入环境变量、系统密钥管理或 `wjx init` 创建的用户级配置；不得写进 Skill、项目、Word、JSONL、manifest、日志或聊天回复。若账号没有相应 OpenAPI 权限，停止并让用户向问卷星确认版本或白名单，不得改用抓包或非官方私有接口。

## 安全发布状态机

严格按以下状态流转：

```text
本地设计 → 本地校验 → Word 人工审核 → 问卷星未发布草稿 → 在线预览核对 → 用户明确确认 → 正式发布
```

禁止在第一次推送时使用 `--publish`。创建草稿属于外部写操作，只有用户明确要求推送后才能执行。正式发布、暂停、删除、清空答卷均需要针对具体问卷 ID 的再次确认；删除与清空答卷属于破坏性操作。

## 一表单一草稿

问卷规格中的每个 `form` 默认创建一份独立问卷星草稿。不同人群、语言或实施模式不得为了减少链接数量而未经论证地合并。只有中央设计明确要求用筛选和分支逻辑形成单一在线问卷，并且所有路径完成测试时，才能合并。

访谈提纲不计入问卷星草稿数量。

## 准备平台载荷

先运行完整问卷规格校验，再生成平台载荷：

```bash
python references/questionnaire-design/scripts/validate_questionnaire_spec.py path/to/questionnaire-spec.json
python scripts/prepare_wjx_payload.py path/to/questionnaire-spec.json path/to/internal/wjx
```

转换器为每个 form 生成一份 `.wjx.jsonl` 和总 manifest。只有 manifest 状态为 `ready-for-draft` 时才能推送。`manual-review-required` 表示存在跳转、随机化、缺失选项、题型或其他无法无损转换的设置；先修正或在问卷星后台完成明确配置，再重新校验。

基础映射：

| 内部题型 | 问卷星 qtype |
|---|---|
| `single-choice` | `单选` |
| `multiple-choice` | `多选` |
| `ordinal-rating` | `量表题` |
| `numeric` | `单项填空` + 数字校验 |
| `date-or-time` | `日期` |
| `open-text` | `简答题` |
| `ranking` | `排序` |
| `constant-sum` | `比重题` |

选择题中对参与者可见的“不知道 / 不适用 / 不愿回答”作为明确选项保留。非选择题、排序题和比重题无法用普通选项无损承载这些缺失状态时，转换器必须阻断自动推送，不得静默删掉。

## 创建未发布草稿

1. 运行 `wjx doctor`，确认版本、认证和连接正常。
2. 逐个读取 manifest 中的 `draft_command`，确认其中没有 `--publish`。
3. 执行命令并保存返回的问卷 ID。
4. 用 `wjx survey get --vid <ID>` 回读题目；核对标题、题数、题型、选项、必答、章节和顺序。
5. 用 `wjx survey url --mode edit --activity <ID>` 获取编辑链接；在线逐路径预览。

推送成功只表示草稿已创建，不表示问卷已验证、已发布或可正式收数。

## 发布与在线管理

用户针对已核对的具体问卷 ID 明确确认后，才执行：

```bash
wjx survey status --vid <ID> --state 1
```

常用管理动作：

```bash
wjx survey list
wjx survey get --vid <ID>
wjx response count --vid <ID>
wjx response report --vid <ID>
wjx response download --vid <ID>
wjx survey status --vid <ID> --state 2
```

如需答卷实时进入自有系统，使用官方数据推送/Webhook 设置，并验证签名、去重、失败重试、访问控制和数据最小化。不得把可识别答卷推送到未经研究伦理与数据安全评估的第三方系统。

## 上线核对

- Word、问卷规格、JSONL 和线上草稿的题号、题面、选项与顺序一致。
- 所有筛选、显示、跳转、必答、拒答和结束路径均测试。
- 移动端和桌面端均预览；预计时长未显著偏离。
- 知情同意、退出机制、隐私说明、联系人和结束语显示正确。
- 问卷保持未发布，直到用户明确确认具体问卷 ID。
- 回收后先做小规模真实设备试填和导出核对，再进入正式收数。

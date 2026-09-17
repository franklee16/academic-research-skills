# 引用图景

本页面只负责工具选择、结果口径和解释规则；分页、限流恢复、检查点、归档、过滤与排序由 MCP 实现。

## 选择工具和扫描模式

- 用户要引用者列表或数量时，调用 `semantic_scholar_get_citing_papers`；它会扫描全部分页并返回目标论文的引用总数，不再单独查询引用量。响应最多展示引用量最高的 1000 条，超过部分保存在本地档案中。
- 用户要高被引或代表性后续工作的 Top-K 时，调用 `semantic_scholar_get_top_citing_papers`。
- 引用工具固定扫描全部引用者，不提供抽样模式；不要根据用户是否说“全部”“严格”或“全局”切换扫描范围。
- 例如“帮我找一下 Attention Is All You Need 在全部引用者中引用量最高的 20 篇后续论文”应直接调用 `semantic_scholar_get_top_citing_papers`，设置 `limit=20`。
- 用户基于已有检索继续按标题、年份或领域过滤、排除主题并重新排名时，优先调用 `semantic_scholar_query_saved_citing_papers`，避免重新联网扫描；没有可用档案时再说明需要先完成引用检索。
- 不为引用图景下载论文 PDF。

## 报告结果

- 始终报告目标论文的总引用量、`returned_paper_count`、`coverage` 和 `complete`，并明确区分目标论文的总引用量与每篇引用论文自身的 `citation_count`。
- 严格 Top-K 还必须报告 `citation_page_request_count`、`scanned_citation_record_count`、`usable_citation_record_count`、`scan_complete` 和 `complete`。
- 相关时报告 `records_archived`、`archived_record_count`、`archive_folder`、`archive_database` 和检查点恢复状态。
- 如 `truncated=true`、`scan_complete=false`、`complete=false` 或 `warning` 非空，必须展示警告，不得把结果称为全部引用者中的严格 Top-K。

## 后续过滤与解释

- 本地过滤只基于已保存的标题、年份、作者、来源、研究领域和论文自身引用量；说明查询所用档案的范围、完整性以及 `network_requests_made`。
- “去掉综述和视觉相关文章”应保守映射到标题或领域中的综述、survey、review、vision、visual、image、video、object detection、segmentation 等信号；注明这不是摘要或正文级分类。
- 根据标题和研究领域做保守归类；信息不足时标为“无法判断”，不要推断具体引用意图。
- 只有返回数据支持时才概括年份或领域分布，不要从 Top-K 结果推断全部引用者的整体分布。
- 默认聚焦用户要求的 Top-K 和选择口径，不倾倒整个本地档案。

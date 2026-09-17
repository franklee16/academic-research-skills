# API 参考文档

本 Skill 同时调用 **Semantic Scholar / OpenAlex / Crossref** 三个免费学术 API。本文档汇总各 API 的端点、参数、响应格式、限速规则与错误处理。

---

## 1. Semantic Scholar Academic Graph API

**Base URL**: `https://api.semanticscholar.org/graph/v1/`

### 1.1 搜索端点

```
GET /paper/search
```

**关键参数**：

| 参数 | 类型 | 说明 |
|---|---|---|
| `query` | string | 全文检索关键词 |
| `year` | string | 如 `2021-2026` 或 `2024` |
| `fieldsOfStudy` | string | 逗号分隔，如 `Computer Science,Medicine` |
| `limit` | int | 单次返回，最多 100 |
| `offset` | int | 翻页 |
| `fields` | string | 逗号分隔字段，例：`title,authors,year,venue,citationCount,externalIds,abstract,publicationDate` |

**响应（节选）**：
```json
{
 "total": 12345,
 "offset": 0,
 "data": [
 {
 "paperId": "abc123",
 "title": "...",
 "authors": [{"authorId":"...","name":"..."}],
 "year": 2024,
 "venue": "Nature Machine Intelligence",
 "citationCount": 150,
 "externalIds": {"DOI": "10.1038/...", "ArXiv": "2401.xxxxx"},
 "abstract": "..."
 }
 ]
}
```

### 1.2 单文献端点（含 DOI 查询）

```
GET /paper/DOI:{doi}
GET /paper/{paperId}
```

### 1.3 限速

- **匿名调用**：5000 次 / 5 分钟（IP 维度）
- 推荐设置 `User-Agent: SciPilot-cite/1.0 (mailto:contact@example.org)`
- 本 Skill 默认请求间隔 ≥ 1.0 秒
- 429 响应触发指数退避（2s → 4s → 8s）

### 1.4 错误码处理

| Code | 处理 |
|---|---|
| 200 | 正常 |
| 429 | 等待 `Retry-After` 或指数退避 |
| 5xx | 重试 3 次后切换数据源补充 |
| 404 | 单条记录可能下架，跳过 |

---

## 2. OpenAlex API

**Base URL**: `https://api.openalex.org/`

无需 API key，但**强烈推荐**在参数里加 `mailto=` 进入 polite pool 获得更快响应。

### 2.1 搜索端点

```
GET /works
```

**关键参数**：

| 参数 | 说明 |
|---|---|
| `search` | 关键词检索（全文） |
| `filter` | 过滤器，逗号分隔条件 |
| `sort` | 例：`cited_by_count:desc`、`publication_date:desc` |
| `per_page` | 单次返回，最多 200 |
| `mailto` | 用户邮箱（进入 polite pool） |

**filter 语法**：

```
from_publication_date:2021-01-01,
to_publication_date:2026-12-31,
cited_by_count:>50,
is_paratext:false,
type:journal-article
```

### 2.2 响应特殊点

- 摘要字段 `abstract_inverted_index` 是**倒排索引**而非完整文本，需要按 position 重排
- DOI 字段是完整 URL `https://doi.org/10.xxxx/xxxxx`，使用前去前缀

### 2.3 限速

- Polite pool：100 req/sec、100k req/day
- 普通：10 req/sec
- 本 Skill 默认 0.5s 间隔

---

## 3. Crossref REST API

**Base URL**: `https://api.crossref.org/`

被广泛认为是 DOI 元数据的权威来源。

### 3.1 搜索端点

```
GET /works
```

**关键参数**：

| 参数 | 说明 |
|---|---|
| `query` | 全文检索 |
| `filter` | 例：`from-pub-date:2021,until-pub-date:2026,type:journal-article` |
| `sort` | `is-referenced-by-count` / `published` |
| `order` | `asc` / `desc` |
| `rows` | 单次返回，最多 1000（推荐 ≤100） |

### 3.2 单 DOI 验证端点（本 Skill 核心）

```
GET /works/{doi}
```

返回该 DOI 的完整元数据，**用于真实性验证**。

**响应（节选）**：
```json
{
 "status": "ok",
 "message": {
 "DOI": "10.1038/s41586-024-07421-0",
 "title": ["..."],
 "author": [{"given":"...","family":"..."}],
 "issued": {"date-parts": [[2024, 5, 1]]},
 "container-title": ["Nature"],
 "is-referenced-by-count": 150,
 "type": "journal-article"
 }
}
```

### 3.3 礼貌使用

- 推荐 `User-Agent: SciPilot-cite/1.0 (mailto:scipilot@example.org)`
- 推荐 `mailto=` query 参数
- 限速宽松，但建议 ≥0.5s 间隔
- 如发生 429，自动切换到不带 polite headers 的请求重试

---

## 4. 数据源能力对比

| 维度 | Semantic Scholar | OpenAlex | Crossref |
|---|---|---|---|
| 文献量 | ~200M | ~250M | ~150M |
| 摘要完整度 | [OK] 直接文本 | [WARN] 倒排索引需重组 | [WARN] 仅部分（HTML jats） |
| 引用量 | [OK] | [OK] | [OK]（来源数为主） |
| DOI 权威 | 中 | 中 | **高（权威）** |
| 期刊/会议识别 | 中 | 高 | 高 |
| 速率友好度 | 中 | 高（polite pool） | 高 |
| 主要用途 | 主搜 + AI 推荐 | 主搜 + 引用网络 | DOI 验证 |

---

## 5. 多源策略

1. **搜索阶段**：三源并行查询，按引用量降序合并；DOI 主键去重，无 DOI 用 (标题相似度+年份+首作者) 合并
2. **验证阶段**：DOI 命中走 Crossref 单 DOI 端点；DOI 缺失或 Crossref 不匹配走 S2 + OpenAlex 跨源搜索
3. **降级策略**：任一 API 持续 5xx → 用其余两源补足；若三源都失败则向用户告知

---

## 6. 参考链接

- [Semantic Scholar API 文档](https://api.semanticscholar.org/api-docs/graph)
- [OpenAlex API 文档](https://docs.openalex.org/how-to-use-the-api/api-overview)
- [Crossref REST API 文档](https://api.crossref.org/swagger-ui/index.html)
- [DOI 解析器](https://doi.org)

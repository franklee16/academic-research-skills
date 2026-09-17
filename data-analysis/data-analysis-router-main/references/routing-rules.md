# Routing Rules

Use this file to choose the most likely analysis framework before analyzing the data.

## Routing Workflow

1. Inspect filenames, sheet names, field names, sample values, and the user's question.
2. Identify the business subject: user, order, product, content, ad, store, finance line item, or feedback text.
3. Match field clusters and user intent to one or more domains.
4. If confidence is high, read the matching domain reference.
5. If confidence is mixed, combine domains and explain the overlap.
6. If confidence is low, use `general-analysis.md`.

## Field And Intent Map

| Signals | Likely domain | Reference |
| --- | --- | --- |
| order, order_id, sku, product_id, GMV, sales_amount, payment, refund, buyer, cart, conversion, repurchase | Ecommerce | `ecommerce.md` |
| post, note, video, article, title, exposure, views, likes, saves, comments, shares, followers, completion_rate | Content operation | `content-operation.md` |
| campaign, ad_group, creative, impressions, clicks, spend, CTR, CVR, CPA, CPM, ROI, ROAS, conversion | Advertising | `advertising.md` |
| store, branch, shop, table, foot_traffic, member, shift, cashier, time_slot, turnover, offline sales | Store operation | `store-operation.md` |
| revenue, cost, gross_profit, margin, net_profit, expense, cash_flow, budget, receivable, payable | Finance | `finance.md` |
| review, rating, complaint, feedback, support_ticket, survey, comment_text, sentiment, defect, VOC | User feedback | `user-feedback.md` |
| generic numeric/category/time fields with no clear business subject | General analysis | `general-analysis.md` |

## User Question Signals

- "Why did sales drop?", "which product sells best?", "repurchase", "refund": ecommerce.
- "Which topic went viral?", "title keywords", "best posting time", "interaction": content operation.
- "Which channel has better ROI?", "optimize spend", "creative fatigue": advertising.
- "Which store performs best?", "peak hours", "staffing", "members": store operation.
- "Profit", "cash flow", "expense control", "budget variance": finance.
- "What are users complaining about?", "negative reviews", "sentiment", "customer needs": user feedback.

## Multi-Table Routing

Infer table roles before selecting metrics:

- Fact tables: orders, transactions, ad performance, daily metrics, reviews, tickets.
- Dimension tables: users, products, stores, campaigns, categories, employees.
- Relationship keys often include `user_id`, `product_id`, `sku_id`, `store_id`, `campaign_id`, `creative_id`, `order_id`.
- Treat key matches as candidates, not confirmed joins.

## Confidence Rules

- High confidence: at least two strong signals match the same domain, such as field cluster plus user question.
- Medium confidence: one strong signal or multiple generic signals match a domain.
- Low confidence: fields are generic, renamed, heavily abbreviated, or lack samples.

When confidence is medium or low, state the uncertainty and include what evidence would confirm the domain.

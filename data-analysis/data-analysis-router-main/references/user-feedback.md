# User Feedback Analysis

Use for reviews, ratings, complaints, customer service records, surveys, social comments, support tickets, VOC, product defects, and open-ended feedback text.

## Common Tables

- Reviews: `review_id`, `user_id`, `rating`, `comment`, `created_at`, `product_id`.
- Support: `ticket_id`, `channel`, `issue_type`, `content`, `status`, `resolution_time`.
- Surveys: `respondent_id`, `score`, `question`, `answer_text`, `submitted_at`.
- Social comments: `comment_id`, `content_id`, `comment_text`, `likes`, `created_at`.

## Core Metrics

- Rating average and rating distribution.
- Sentiment distribution when text supports it.
- High-frequency issues and complaint categories.
- Negative feedback rate.
- Resolution time and unresolved rate for support data.
- Demand themes and product defect frequency.

## Analysis Models

- Sentiment analysis: classify positive, neutral, and negative text with evidence.
- Keyword and theme clustering: group repeated expressions into issue categories.
- VOC analysis: translate user language into product, service, price, logistics, or experience themes.
- Negative review attribution: identify root causes by product, channel, period, or issue type.
- Demand priority: rank needs by frequency, negative impact, and business value.
- Feedback loop: map issue to responsible team, action, and validation metric.

## Chart Suggestions

- Sentiment distribution bar chart.
- Issue category ranking.
- Keyword frequency table.
- Rating trend line.
- Negative reason matrix.
- Demand priority quadrant.

## Recommendation Patterns

- Prioritize issues that are frequent, negative, and controllable.
- Separate product defects from service, logistics, pricing, and expectation mismatch.
- Use representative short examples, but avoid over-quoting user text.
- Convert feedback into product fixes, service scripts, FAQ updates, or expectation-setting changes.
- Track whether changes reduce complaint frequency or improve rating.

## Missing Data To Flag

- Text fields are required for theme and sentiment analysis.
- Time fields are required for trend or incident diagnosis.
- Product/order/channel fields are required for root cause attribution.
- Resolution status is required for support process analysis.

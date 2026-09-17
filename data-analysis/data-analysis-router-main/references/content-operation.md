# Content Operation Analysis

Use for social posts, short videos, long videos, articles, creator accounts, topic performance, and audience interaction data.

## Common Tables

- Content: `content_id`, `title`, `topic`, `publish_time`, `author`, `platform`.
- Performance: `views`, `exposure`, `clicks`, `likes`, `saves`, `comments`, `shares`, `followers_gained`.
- Video: `play_count`, `completion_rate`, `watch_time`, `avg_watch_duration`.
- Account: `account_id`, `followers`, `new_followers`, `profile_visits`.

## Core Metrics

- Exposure, views, click-through rate.
- Like rate, save rate, comment rate, share rate.
- Follower growth rate and conversion to follow.
- Completion rate and average watch duration.
- Engagement rate: define numerator explicitly based on available interactions.

## Analysis Models

- Viral content decomposition: compare top content by exposure and engagement quality.
- Topic matrix: compare topics by traffic, engagement, saves, and follower conversion.
- Title keyword analysis: identify repeated terms in high-performing titles.
- Publish timing: compare performance by hour, weekday, or campaign period.
- Interaction quality: distinguish light engagement from high-intent actions such as saves, comments, shares, and follows.
- Content lifecycle: observe early performance, peak, decay, and long-tail effects.

## Chart Suggestions

- Content ranking table.
- Topic performance bar chart.
- Publish time heatmap.
- Exposure vs engagement scatter plot.
- Title keyword frequency table.
- Content lifecycle line chart.

## Recommendation Patterns

- Reuse topics with high saves, shares, or follower conversion, not only high exposure.
- Optimize titles and hooks from high-performing keyword patterns.
- Adjust publishing windows based on time-period performance.
- Separate acquisition content from conversion or trust-building content.
- Identify formats with stable performance instead of chasing single outliers.

## Missing Data To Flag

- Exposure is required to calculate CTR or exposure-based engagement.
- Publish time is required for timing analysis.
- Follower gained data is required for follow conversion.
- Content text/title is required for keyword analysis.

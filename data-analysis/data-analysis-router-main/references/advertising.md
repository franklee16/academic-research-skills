# Advertising Analysis

Use for paid media, campaign, ad group, creative, channel, audience, spend, impression, click, conversion, ROI, or ROAS data.

## Common Tables

- Campaigns: `campaign_id`, `campaign_name`, `channel`, `objective`, `budget`.
- Ad groups/audiences: `ad_group_id`, `audience`, `targeting`, `bid`.
- Creatives: `creative_id`, `format`, `title`, `image`, `video`.
- Performance: `date`, `spend`, `impressions`, `clicks`, `conversions`, `revenue`.

## Core Metrics

- Spend, impressions, clicks, conversions, revenue.
- CTR = clicks / impressions.
- CVR = conversions / clicks or conversions / landing page visits; state denominator.
- CPC = spend / clicks.
- CPM = spend / impressions * 1000.
- CPA = spend / conversions.
- ROI or ROAS = revenue / spend; clarify the definition used.

## Analysis Models

- Funnel analysis: impression to click to conversion to revenue.
- ROI layering: classify campaigns, channels, audiences, or creatives by spend and return.
- Creative fatigue: identify rising frequency/spend with falling CTR or CVR.
- Channel attribution: compare channels when attribution logic is available.
- Budget efficiency: identify where marginal spend appears less efficient.
- Audience effect: compare conversion and CPA by audience package or targeting group.

## Chart Suggestions

- Channel ROI/ROAS comparison bar chart.
- Advertising funnel.
- Spend and conversion trend line chart.
- Creative CTR/CVR scatter plot.
- CPA ranking table.
- Spend vs return quadrant.

## Recommendation Patterns

- Increase budget for high-ROAS units only when volume and attribution are reliable.
- Cut or revise high-spend, low-conversion campaigns.
- Refresh creatives with declining CTR or CVR.
- Separate traffic quality issues from landing page conversion issues.
- Reallocate budget across channel, audience, creative, and time period layers.

## Missing Data To Flag

- Revenue is required for ROAS/ROI.
- Conversion count and definition are required for CPA/CVR.
- Impression count is required for CTR/CPM.
- Attribution window and conversion source are required for channel comparison.

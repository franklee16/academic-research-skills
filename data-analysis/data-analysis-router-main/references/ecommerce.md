# Ecommerce Analysis

Use for orders, products, users, traffic, refunds, storefront, marketplace, or SKU-level sales data.

## Common Tables

- Orders: `order_id`, `user_id`, `sku_id`, `quantity`, `payment_amount`, `created_at`, `status`.
- Products: `sku_id`, `product_id`, `category`, `brand`, `price`, `cost`, `stock`.
- Users: `user_id`, `city`, `channel`, `register_time`, `member_level`.
- Traffic: `date`, `page_views`, `visitors`, `clicks`, `add_to_cart`, `orders`.
- Refunds/after-sales: `order_id`, `sku_id`, `refund_amount`, `reason`, `created_at`.

## Core Metrics

- GMV, net sales, order count, units sold.
- Average order value, average selling price.
- Conversion rate, add-to-cart rate, payment rate.
- Repurchase rate, customer count, new vs returning buyers.
- Refund rate, cancellation rate, after-sales rate.
- Gross profit, gross margin, category contribution.

## Analysis Models

- Sales trend: compare GMV, orders, and customers by day/week/month.
- Product ABC: classify SKUs/categories by cumulative contribution.
- RFM segmentation: score recency, frequency, and monetary value when user-level purchase history exists.
- Repurchase analysis: compare first purchase, repeat purchase, and lifecycle value.
- Funnel analysis: traffic to product view to cart to order to paid.
- Price band analysis: compare sales, margin, and conversion across price ranges.
- Refund diagnosis: identify high-refund SKUs, categories, reasons, and periods.

## Chart Suggestions

- GMV and order trend line chart.
- Category/SKU contribution Pareto chart.
- Conversion funnel.
- Price band bar chart.
- RFM segment matrix.
- Refund reason ranking.

## Recommendation Patterns

- Increase exposure for high-margin, high-conversion products.
- Investigate high-sales but high-refund SKUs before scaling them.
- Improve low-conversion traffic pages or price bands.
- Use high-value dormant customer segments for recall campaigns.
- Separate growth problems into traffic, conversion, order value, and repurchase.

## Missing Data To Flag

- Traffic data is required for conversion analysis.
- Cost data is required for profit and margin analysis.
- User IDs and dates are required for repurchase and RFM.
- Refund reason and order status are required for after-sales diagnosis.

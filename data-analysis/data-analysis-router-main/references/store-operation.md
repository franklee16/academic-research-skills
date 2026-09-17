# Store Operation Analysis

Use for offline stores, branches, restaurants, retail counters, member consumption, product sales, foot traffic, shifts, and time-slot operation data.

## Common Tables

- Store sales: `store_id`, `store_name`, `date`, `sales_amount`, `orders`, `gross_profit`.
- Traffic: `date`, `store_id`, `foot_traffic`, `visits`, `peak_time`.
- Members: `member_id`, `store_id`, `spend`, `visit_count`, `last_visit`.
- Product sales: `sku_id`, `category`, `quantity`, `sales_amount`, `margin`.
- Staffing: `store_id`, `date`, `shift`, `employee_count`, `labor_hours`.

## Core Metrics

- Revenue, order count, customer count, foot traffic.
- Average order value and conversion from traffic to orders.
- Gross margin, category contribution, member sales share.
- Repurchase rate, visit frequency, active members.
- Table turnover or service capacity when relevant.
- Sales per labor hour or sales per employee.

## Analysis Models

- Store ranking: compare sales, margin, traffic, conversion, and growth.
- Time-slot analysis: identify peak and low-efficiency periods.
- Category structure: compare category contribution and margin.
- Best/worst sellers: identify high-volume, high-margin, slow-moving, and low-margin items.
- Member repurchase: segment active, dormant, high-value, and new members.
- Staffing efficiency: compare labor input with sales and traffic.

## Chart Suggestions

- Store ranking bar chart.
- Hour/day heatmap.
- Category contribution stacked bar.
- Traffic vs sales trend line.
- Member segment matrix.
- Labor efficiency comparison.

## Recommendation Patterns

- Improve staffing and inventory for peak periods.
- Diagnose stores with high traffic but low conversion.
- Promote bundles or add-ons in low-AOV stores.
- Reduce slow-moving inventory and improve high-margin placement.
- Use member campaigns for stores with weak repeat visits.

## Missing Data To Flag

- Foot traffic is required for store conversion.
- Labor hours are required for staffing efficiency.
- Member IDs are required for repurchase and member segmentation.
- Product cost or margin is required for profit-based decisions.

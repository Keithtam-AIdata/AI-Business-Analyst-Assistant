# Data Dictionary

Synthetic APAC e-commerce performance dataset (`data/business_data.csv`).

**Grain:** one row per Month × Country × Channel × Customer Segment × Product
Category — 6,912 rows over 24 months (2024-01 to 2025-12). Product subcategory
and campaign type are attributes on each row.

The data is **pattern-driven, not random**: each metric is built as
`base × documented business multipliers × small noise`, so every figure traces
back to a deliberate, explainable assumption (see *Business patterns* below).

---

## Dimensions

| Column | Type | Description |
|---|---|---|
| Month | text | Calendar month, `YYYY-MM` (sorts chronologically as text). |
| Year | integer | 2024 or 2025. |
| Quarter | text | Q1–Q4. |
| Region | text | Always `APAC` (single region). |
| Country | text | Hong Kong, Singapore, Japan, Australia. |
| Channel | text | Online Store, Mobile App, Marketplace, Retail. |
| CustomerSegment | text | New, Returning, VIP. |
| ProductCategory | text | Beauty, Electronics, Fashion, Grocery, Home & Living, Sports. |
| ProductSubcategory | text | One of three subcategories within each category. |
| CampaignType | text | None, Brand, Performance, Influencer, Seasonal Sale. |

## Measures

| Column | Type | Description |
|---|---|---|
| Revenue | float | Gross revenue (USD). Equals Orders × AverageOrderValue. |
| Orders | integer | Number of orders. |
| Customers | integer | Distinct customers (Orders ÷ orders-per-customer by segment). |
| AverageOrderValue | float | Revenue per order (USD). |
| ConversionRate | float | Share of sessions converting (channel-driven). |
| MarketingSpend | float | Marketing cost (USD); Revenue ÷ ROAS, ROAS varies by country. |
| DiscountRate | float | Effective discount applied; rises during campaigns. |
| GrossMarginPct | float | Gross margin after discount (category base − discount). |
| GrossProfit | float | Revenue × GrossMarginPct. |
| ShippingCost | float | Fulfilment cost (cheaper for in-store Retail). |
| ReturnRate | float | Share of orders returned (category × channel). |
| ReturnCost | float | Lost value from returns (60% of returned revenue). |
| ReturnReason | text | Dominant return reason for the row (varies by category). |
| NetProfit | float | GrossProfit − MarketingSpend − ShippingCost − ReturnCost. |
| CustomerSatisfaction | float | 1–5 rating; falls with higher returns. |

---

## Business patterns (intentional and explainable)

These are deliberately built into the data, so analyses surface real stories
rather than noise:

- **Q4 holiday peak** — revenue rises sharply in Nov/Dec each year.
- **Q4 × Electronics interaction** — gifting categories (esp. Electronics) spike
  more in Q4 than staples like Grocery.
- **Japan marketing efficiency** — Japan earns the most revenue per marketing
  dollar (~11.6 vs ~7.5 elsewhere).
- **Hong Kong scale vs service** — highest revenue, but lowest customer
  satisfaction.
- **Fashion returns** — by far the highest return rate (size/fit), which erodes
  its net profit.
- **Discount vs margin trade-off** — heavier discounting lifts revenue but
  compresses margin.
- **Channel × segment** — New customers over-index on the Mobile App.
- **Segment value ladder** — VIP has the highest average order value, New the
  lowest.
- **Category economics** — Electronics has the highest AOV but a thin margin;
  Beauty has the fattest margin.
- **Channel returns** — in-store Retail has the lowest return rate.

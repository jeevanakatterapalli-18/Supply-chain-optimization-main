# EDA Findings (Phase 6)

## Trend Analysis
- Monthly revenue (`images/monthly_revenue_trend.png`) is flat across all 36 months of 2023-2025 — no growth, decline, or seasonal pattern.
- Revenue by category (`images/revenue_by_category.png`) is even across Fashion/Home/Electronics/Food/Health — consistent with the near-uniform per-product revenue generation noted in Phase 5.

## Correlation Analysis
Strongest correlations with `Profit_USD`:

```
On_Time_Delivery_Rate     0.001042
Current_Stock             0.001039
Demand_Forecast           0.001010
Utilization_Rate          0.000622
Shipping_Cost_USD         0.000497
Inventory_Turnover        0.000380
Overstock_Risk            0.000255
Supply_Disruption_Risk   -0.000218
```

No numeric field correlates strongly with profit (all |r| stay low) — profit is not being driven by any single operational lever (lead time, delivery time, stock levels, risk scores) in this dataset; see `images/correlation_heatmap.png` for the full matrix.

**Important caveat for later phases**: this near-zero pattern holds even between fields that would normally be arithmetically linked — `Product_Cost_USD`, `Selling_Price_USD`, `Revenue_USD`, `Profit_USD`, and `Units_Sold` all correlate at |r| < 0.01 with each other. In a real business, `Profit_USD ≈ Revenue_USD - (Product_Cost_USD × Units_Sold)`; here they were generated independently, so that identity does not hold row-by-row. KPI calculations (Phase 7) and AI-generated narratives (Phase 9) should treat each financial column as its own independent metric rather than assuming standard revenue/cost/profit arithmetic between them.

## Distribution Analysis
- 9.1% of products are loss-making (`Profit_USD` < 0) — see `images/profit_distribution.png`.
- 15.7% of shipments are delayed, consistent with the flat ~15-16% delay rate found across every dimension in Phase 5.
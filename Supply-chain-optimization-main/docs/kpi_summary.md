# KPI Summary (Phase 7)

## Company-Wide KPIs

- **total_orders**: 200,000
- **revenue_usd**: 50,017,493,094.75
- **profit_usd**: 9,001,642,610.56
- **inventory_cost_usd**: 501,110,895,541.44
- **avg_delivery_time_days**: 14.99
- **avg_lead_time_days**: 44.99
- **delayed_orders**: 31,343
- **delayed_orders_pct**: 15.67
- **fill_rate_pct**: 50.06
- **reorder_point_compliance_pct**: 94.96
- **avg_inventory_turnover**: 10.02
- **avg_warehouse_utilization_pct**: 50.0

**Note on `fill_rate_pct` (50.06%)**: this is computed as `100 - avg(Stockout_Risk)`, and `Stockout_Risk` is close to uniformly distributed 0-100 (see `docs/eda_findings.md`), so the proxy lands near 50% by construction — it does not mean "only half of orders are fulfilled." Read it as relative (compare across categories/suppliers/time), not as an absolute fulfillment rate a real ops team would report.

## KPIs by Product Category

| Product_Category   |   total_orders |   revenue_usd |   profit_usd |   inventory_cost_usd |   avg_delivery_time_days |   avg_lead_time_days |   delayed_orders |   delayed_orders_pct |   fill_rate_pct |   reorder_point_compliance_pct |   avg_inventory_turnover |   avg_warehouse_utilization_pct |
|:-------------------|---------------:|--------------:|-------------:|---------------------:|-------------------------:|---------------------:|-----------------:|---------------------:|----------------:|-------------------------------:|-------------------------:|--------------------------------:|
| Electronics        |          39688 |   9.9538e+09  |  1.78358e+09 |          9.82165e+10 |                    14.95 |                44.95 |             6266 |                15.79 |           50.12 |                          94.9  |                    10    |                           49.86 |
| Fashion            |          40050 |   9.96711e+09 |  1.80274e+09 |          1.00481e+11 |                    15.1  |                44.94 |             6286 |                15.7  |           50.18 |                          94.96 |                    10.02 |                           50.05 |
| Food               |          40240 |   1.00449e+10 |  1.80449e+09 |          1.01813e+11 |                    14.98 |                45.17 |             6177 |                15.35 |           49.95 |                          94.96 |                    10.01 |                           50.05 |
| Health             |          39877 |   1.00039e+10 |  1.79612e+09 |          9.98404e+10 |                    14.94 |                44.99 |             6211 |                15.58 |           49.94 |                          95.04 |                    10.06 |                           50    |
| Home               |          40145 |   1.00478e+10 |  1.81471e+09 |          1.0076e+11  |                    14.99 |                44.89 |             6403 |                15.95 |           50.09 |                          94.96 |                    10    |                           50.05 |

## KPIs by Warehouse Region

| Warehouse_Location   |   total_orders |   revenue_usd |   profit_usd |   inventory_cost_usd |   avg_delivery_time_days |   avg_lead_time_days |   delayed_orders |   delayed_orders_pct |   fill_rate_pct |   reorder_point_compliance_pct |   avg_inventory_turnover |   avg_warehouse_utilization_pct |
|:---------------------|---------------:|--------------:|-------------:|---------------------:|-------------------------:|---------------------:|-----------------:|---------------------:|----------------:|-------------------------------:|-------------------------:|--------------------------------:|
| East                 |          50051 |   1.24629e+10 |  2.2503e+09  |          1.25481e+11 |                    15.04 |                44.94 |             7878 |                15.74 |           50.18 |                          94.97 |                    10.02 |                           49.95 |
| North                |          50093 |   1.25529e+10 |  2.2542e+09  |          1.25113e+11 |                    14.99 |                45.05 |             7786 |                15.54 |           50.07 |                          94.86 |                    10.01 |                           49.95 |
| South                |          49963 |   1.24593e+10 |  2.24568e+09 |          1.24784e+11 |                    14.95 |                44.79 |             7926 |                15.86 |           49.91 |                          94.99 |                    10.01 |                           50.03 |
| West                 |          49893 |   1.25424e+10 |  2.25146e+09 |          1.25734e+11 |                    14.99 |                45.17 |             7753 |                15.54 |           50.06 |                          95.03 |                    10.03 |                           50.07 |
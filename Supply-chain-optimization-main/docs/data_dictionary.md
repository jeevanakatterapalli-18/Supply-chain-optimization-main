# Data Dictionary

Source: `data/raw/Retail_Supply_Chain_Analytics_Dataset.csv` (200,000 rows × 41 columns, no nulls, no duplicates).

| Column | Type | Description |
|---|---|---|
| `Product_ID` | string | Unique product identifier (200,000 unique values — one row per product) |
| `Product_Category` | string | Fashion, Home, Electronics, Food, Health |
| `Brand` | string | Product brand name |
| `SKU` | string | Stock-keeping unit code |
| `Current_Stock` | int | Units currently held in inventory |
| `Reorder_Level` | int | Stock threshold that should trigger a reorder |
| `Safety_Stock` | int | Buffer stock held to avoid stockouts |
| `Inventory_Turnover` | float | How many times inventory is sold/replaced over the period |
| `Supplier_ID` | string | Unique supplier identifier (4,999 unique suppliers) |
| `Supplier_Rating` | float | Supplier quality/reliability rating |
| `Lead_Time_Days` | int | Expected days from order to receipt from supplier |
| `Warehouse_ID` | string | Unique warehouse identifier (499 unique warehouses) |
| `Warehouse_Location` | string | Region: North, South, East, West |
| `Storage_Capacity` | int | Total storage capacity of the warehouse |
| `Utilization_Rate` | float | % of warehouse capacity currently in use |
| `Units_Sold` | int | Units sold for this product in the period |
| `Daily_Demand` | int | Average daily demand |
| `Monthly_Demand` | int | Average monthly demand |
| `Seasonal_Demand_Index` | float | Index reflecting seasonal demand fluctuation |
| `Shipping_Cost_USD` | float | Shipping cost in USD |
| `Transportation_Mode` | string | Road, Sea, Air, Rail |
| `Delivery_Time_Days` | int | Actual observed delivery time in days |
| `On_Time_Delivery_Rate` | float | % of deliveries arriving on time |
| `Product_Cost_USD` | float | Unit cost to acquire/produce the product |
| `Selling_Price_USD` | float | Unit selling price |
| `Revenue_USD` | float | Total revenue for this product |
| `Profit_USD` | float | Total profit for this product |
| `Stockout_Risk` | float | Modeled risk score (%) of stockout |
| `Overstock_Risk` | float | Modeled risk score (%) of overstock |
| `Supply_Disruption_Risk` | float | Modeled risk score (%) of supply disruption |
| `Date` | date | Snapshot date for this record (2023-01-01 to 2025-12-30) |
| `Month` | int | Month extracted from `Date` |
| `Quarter` | int | Quarter extracted from `Date` |
| `Year` | int | Year extracted from `Date` |
| `Demand_Forecast` | int | Forecasted demand |
| `Inventory_Optimization_Score` | float | Composite score for inventory efficiency |
| `Supplier_Performance_Score` | float | Composite score for supplier performance |
| `Supply_Chain_Efficiency` | float | Composite score for overall supply chain efficiency |
| `Sustainability_Score` | float | Composite sustainability score |
| `Predicted_Reorder_Quantity` | int | Model-predicted reorder quantity |
| `Operational_Risk_Score` | float | Composite operational risk score |

## Derived Columns (added in Phase 3 cleaning)

| Column | Derivation |
|---|---|
| `Delivery_Date` | `Date` + `Delivery_Time_Days` |
| `Shipment_Status` | `"Delayed"` if `Delivery_Time_Days` > `Lead_Time_Days`, else `"On Time"` |
| `Customer_Region` | Alias of `Warehouse_Location` (documented proxy — see `dataset_selection.md`) |

## Known Data Characteristics

- No missing values or duplicate rows in the raw file — Phase 3 cleaning focuses on outlier flagging and feature engineering rather than heavy imputation/dedup.
- Many "score" columns (`Inventory_Optimization_Score`, `Supplier_Performance_Score`, `Supply_Chain_Efficiency`, `Sustainability_Score`, `Operational_Risk_Score`) appear to be independently generated composite metrics rather than derived from other visible columns — treat them as given inputs, not columns to recompute.
- Confirmed via Phase 6 correlation analysis (`docs/eda_findings.md`): all numeric columns correlate at |r| < 0.01 with each other, **including** `Product_Cost_USD`, `Selling_Price_USD`, `Revenue_USD`, `Profit_USD`, and `Units_Sold`. The normal identity `Profit ≈ Revenue - Cost × Units_Sold` does not hold row-by-row in this dataset — every numeric field was generated independently. Treat each financial/metric column as its own independent measure; don't assume or derive one from another.

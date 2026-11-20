# Dataset Selection

## Dataset Used

`data/raw/Retail_Supply_Chain_Analytics_Dataset.csv`

- **200,000 rows × 41 columns**
- **Zero missing values, zero duplicate rows** (verified during profiling)
- One row = one product-level supply chain snapshot, dated somewhere between **2023-01-01 and 2025-12-30**
- Covers 5 product categories (Fashion, Home, Electronics, Food, Health), 4,999 suppliers, 499 warehouses across 4 regions (North, South, East, West), and 4 transportation modes (Road, Sea, Air, Rail)

This dataset was chosen over a Kaggle download (originally the plan was to recommend the "DataCo Smart Supply Chain" dataset) because it's already clean and — unlike DataCo — has **native** supplier, warehouse, and inventory columns, so no synthetic/simulated dimension needs to be bolted on. It sits comfortably in the requested 50k–100k+ row range.

## Important Note on Grain

This is a **product-snapshot dataset, not an order-transaction dataset**. Each row represents one product's supply chain metrics as of a given date — there is no `Order ID` or repeated transactions per product. This means:

- `Product_ID` serves as the unique record key (functionally standing in for "Order ID" in the original wish list)
- Metrics like `Units_Sold`, `Shipping_Cost_USD`, `Delivery_Time_Days` should be read as **that product's aggregated/observed metric for the snapshot period**, not a single shipment event
- This is still entirely sufficient for the planned KPIs (top suppliers, inventory turnover, warehouse utilization, ABC analysis, monthly trends via `Date`/`Month`/`Quarter`/`Year`) — it just means "delayed shipments" and "shipment status" are derived metrics (see `data_dictionary.md`) rather than a raw categorical column.

## Field Mapping (requested field → actual column)

| Requested field | Actual column(s) | Notes |
|---|---|---|
| Order ID | `Product_ID` | Used as the unique record key; this dataset has no separate order-transaction ID |
| Product | `Product_ID`, `SKU`, `Brand` | |
| Category | `Product_Category` | Fashion / Home / Electronics / Food / Health |
| Supplier | `Supplier_ID`, `Supplier_Rating`, `Supplier_Performance_Score` | Native, not simulated |
| Warehouse | `Warehouse_ID`, `Warehouse_Location`, `Storage_Capacity`, `Utilization_Rate` | Native, not simulated |
| Inventory | `Current_Stock`, `Reorder_Level`, `Safety_Stock`, `Inventory_Turnover` | Native, not simulated |
| Order Date | `Date` (+ `Month`, `Quarter`, `Year`) | |
| Delivery Date | *derived*: `Date` + `Delivery_Time_Days` | Computed in Phase 3 cleaning |
| Shipment Status | *derived*: "Delayed" if `Delivery_Time_Days` > `Lead_Time_Days`, else "On Time" | Computed in Phase 3 cleaning |
| Shipping Cost | `Shipping_Cost_USD` | |
| Customer Region | `Warehouse_Location` | Proxy for region (North/South/East/West) — this dataset has no separate customer geography field |
| Carrier | `Transportation_Mode` | Road / Sea / Air / Rail |
| Lead Time | `Lead_Time_Days` | |
| Quantity | `Units_Sold`, `Daily_Demand`, `Monthly_Demand` | |
| Unit Cost | `Product_Cost_USD` | `Selling_Price_USD`, `Revenue_USD`, `Profit_USD` also available for margin analysis |

See `docs/data_dictionary.md` for the full column-by-column reference of all 41 original columns.

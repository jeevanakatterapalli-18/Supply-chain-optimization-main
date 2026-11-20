"""
Phase 7: KPI Calculation

Computes the executive KPI set overall and broken down by category,
warehouse region, supplier, and month. Saves a compact kpi_summary.json
(consumed by the Phase 9 AI assistant, which can't be handed the full
200k-row table) and a human-readable docs/kpi_summary.md.

KPI definitions:
- Total Orders: row count. This dataset's grain is one row per product
  snapshot (see docs/dataset_selection.md) — Product_ID stands in for an
  order-transaction ID, so this is really "products tracked," reported
  under the brief's "Total Orders" label.
- Revenue: sum of Revenue_USD.
- Inventory Cost: sum of Current_Stock * Product_Cost_USD — the total
  cost-basis value of stock currently held.
- Avg Delivery Time: mean of Delivery_Time_Days.
- Delayed Orders: count/% where Shipment_Status == 'Delayed'.
- Fill Rate: 100 - avg(Stockout_Risk). Stockout_Risk is a modeled 0-100
  risk score, so this reframes it as an implied ability-to-fill metric.
  This is a proxy, not a literal fulfilled/placed order ratio, because
  the dataset has no explicit order-fulfillment record — documented here
  and in docs/data_dictionary.md.
- Reorder Point Compliance: % of products at or above Reorder_Level (a
  distinct, literal KPI — not to be confused with Fill Rate above).
- Inventory Turnover: mean of the given Inventory_Turnover column.
"""

import json

import pandas as pd

CLEANED_DATA_PATH = "data/processed/cleaned_supply_chain.csv"
KPI_JSON_PATH = "data/processed/kpi_summary.json"
KPI_MARKDOWN_PATH = "docs/kpi_summary.md"


def load_data() -> pd.DataFrame:
    return pd.read_csv(CLEANED_DATA_PATH, parse_dates=["Date", "Delivery_Date"])


def compute_kpis(df: pd.DataFrame) -> dict:
    """Computes the executive KPI set for any slice of the dataframe."""
    total_orders = len(df)
    delayed_orders = int((df["Shipment_Status"] == "Delayed").sum())

    return {
        "total_orders": total_orders,
        "revenue_usd": round(df["Revenue_USD"].sum(), 2),
        "profit_usd": round(df["Profit_USD"].sum(), 2),
        "inventory_cost_usd": round((df["Current_Stock"] * df["Product_Cost_USD"]).sum(), 2),
        "avg_delivery_time_days": round(df["Delivery_Time_Days"].mean(), 2),
        "avg_lead_time_days": round(df["Lead_Time_Days"].mean(), 2),
        "delayed_orders": delayed_orders,
        "delayed_orders_pct": round(100 * delayed_orders / total_orders, 2),
        "fill_rate_pct": round(100 - df["Stockout_Risk"].mean(), 2),
        "reorder_point_compliance_pct": round(100 * (df["Current_Stock"] >= df["Reorder_Level"]).mean(), 2),
        "avg_inventory_turnover": round(df["Inventory_Turnover"].mean(), 2),
        "avg_warehouse_utilization_pct": round(df["Utilization_Rate"].mean(), 2),
    }


def compute_overall(df: pd.DataFrame) -> dict:
    return compute_kpis(df)


def compute_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Product_Category")
        .apply(compute_kpis, include_groups=False)
        .apply(pd.Series)
        .reset_index()
    )


def compute_by_region(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Warehouse_Location")
        .apply(compute_kpis, include_groups=False)
        .apply(pd.Series)
        .reset_index()
    )


def compute_by_month(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby(["Year", "Month"])
        .apply(compute_kpis, include_groups=False)
        .apply(pd.Series)
        .reset_index()
        .sort_values(["Year", "Month"])
    )
    return monthly


def compute_top_bottom_suppliers(df: pd.DataFrame, n: int = 10) -> dict:
    supplier_kpis = (
        df.groupby("Supplier_ID")
        .apply(compute_kpis, include_groups=False)
        .apply(pd.Series)
        .reset_index()
    )
    top_by_revenue = supplier_kpis.sort_values("revenue_usd", ascending=False).head(n)
    bottom_by_fill_rate = supplier_kpis.sort_values("fill_rate_pct", ascending=True).head(n)
    return {
        "top_suppliers_by_revenue": top_by_revenue.to_dict(orient="records"),
        "weakest_suppliers_by_fill_rate": bottom_by_fill_rate.to_dict(orient="records"),
    }


def write_markdown_summary(overall: dict, by_category: pd.DataFrame, by_region: pd.DataFrame) -> None:
    lines = ["# KPI Summary (Phase 7)", "", "## Company-Wide KPIs", ""]
    for key, value in overall.items():
        lines.append(f"- **{key}**: {value:,}")

    lines += ["", "## KPIs by Product Category", "", by_category.to_markdown(index=False)]
    lines += ["", "## KPIs by Warehouse Region", "", by_region.to_markdown(index=False)]

    with open(KPI_MARKDOWN_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    df = load_data()

    overall = compute_overall(df)
    by_category = compute_by_category(df)
    by_region = compute_by_region(df)
    by_month = compute_by_month(df)
    supplier_extremes = compute_top_bottom_suppliers(df)

    summary = {
        "overall": overall,
        "by_category": by_category.to_dict(orient="records"),
        "by_region": by_region.to_dict(orient="records"),
        "by_month": by_month.to_dict(orient="records"),
        **supplier_extremes,
    }

    with open(KPI_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    write_markdown_summary(overall, by_category, by_region)

    print("Overall KPIs:")
    for key, value in overall.items():
        print(f"  {key}: {value:,}")
    print(f"\nFull summary written to {KPI_JSON_PATH} and {KPI_MARKDOWN_PATH}")


if __name__ == "__main__":
    main()

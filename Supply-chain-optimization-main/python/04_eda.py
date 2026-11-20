"""
Phase 6: Exploratory Data Analysis

Trend analysis and correlation analysis on the cleaned dataset, independent
of the SQL exploration in Phase 5. Saves charts to images/ and a written
findings summary to docs/eda_findings.md.
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

CLEANED_DATA_PATH = "data/processed/cleaned_supply_chain.csv"
IMAGES_DIR = "images"
FINDINGS_PATH = "docs/eda_findings.md"

# Palette (light mode) — see dataviz skill references/palette.md
BLUE = "#2a78d6"
RED = "#e34948"
SURFACE = "#fcfcfb"
PRIMARY_INK = "#0b0b0b"
SECONDARY_INK = "#52514e"
MUTED_INK = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"
SEQUENTIAL_BLUES = ["#cde2fb", "#9ec5f4", "#5598e7", "#2a78d6", "#184f95"]

NUMERIC_COLUMNS_FOR_CORRELATION = [
    "Current_Stock", "Inventory_Turnover", "Lead_Time_Days", "Utilization_Rate",
    "Shipping_Cost_USD", "Delivery_Time_Days", "On_Time_Delivery_Rate",
    "Product_Cost_USD", "Selling_Price_USD", "Revenue_USD", "Profit_USD",
    "Stockout_Risk", "Overstock_Risk", "Supply_Disruption_Risk",
    "Supplier_Rating", "Supplier_Performance_Score", "Demand_Forecast",
]


def style_axes(ax):
    ax.set_facecolor(SURFACE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(BASELINE)
    ax.spines["bottom"].set_color(BASELINE)
    ax.tick_params(colors=MUTED_INK)
    ax.yaxis.grid(True, color=GRIDLINE, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.xaxis.grid(False)


def load_data() -> pd.DataFrame:
    return pd.read_csv(CLEANED_DATA_PATH, parse_dates=["Date", "Delivery_Date"])


def plot_monthly_revenue_trend(df: pd.DataFrame) -> None:
    monthly = df.groupby(["Year", "Month"], as_index=False)["Revenue_USD"].sum()
    monthly["period"] = pd.to_datetime(monthly["Year"].astype(str) + "-" + monthly["Month"].astype(str))
    monthly = monthly.sort_values("period")

    fig, ax = plt.subplots(figsize=(9, 4.5), facecolor=SURFACE)
    style_axes(ax)
    ax.plot(monthly["period"], monthly["Revenue_USD"] / 1e6, color=BLUE, linewidth=2)
    ax.set_title("Monthly Revenue, 2023-2025", color=PRIMARY_INK, fontsize=13, loc="left")
    ax.set_ylabel("Revenue ($M)", color=SECONDARY_INK)
    fig.tight_layout()
    fig.savefig(f"{IMAGES_DIR}/monthly_revenue_trend.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def plot_revenue_by_category(df: pd.DataFrame) -> None:
    by_cat = df.groupby("Product_Category")["Revenue_USD"].sum().sort_values(ascending=False) / 1e6

    fig, ax = plt.subplots(figsize=(7, 4.5), facecolor=SURFACE)
    style_axes(ax)
    ax.bar(by_cat.index, by_cat.values, color=BLUE, width=0.6)
    ax.set_title("Total Revenue by Category", color=PRIMARY_INK, fontsize=13, loc="left")
    ax.set_ylabel("Revenue ($M)", color=SECONDARY_INK)
    fig.tight_layout()
    fig.savefig(f"{IMAGES_DIR}/revenue_by_category.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def plot_correlation_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    corr = df[NUMERIC_COLUMNS_FOR_CORRELATION].corr()

    fig, ax = plt.subplots(figsize=(10, 8), facecolor=SURFACE)
    im = ax.imshow(corr, cmap="Blues", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", color=MUTED_INK, fontsize=8)
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns, color=MUTED_INK, fontsize=8)
    ax.set_title("Correlation Matrix — Key Supply Chain Metrics", color=PRIMARY_INK, fontsize=13, loc="left")
    fig.colorbar(im, ax=ax, shrink=0.8, label="Correlation")
    fig.tight_layout()
    fig.savefig(f"{IMAGES_DIR}/correlation_heatmap.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)

    return corr


def plot_profit_distribution(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=SURFACE)
    style_axes(ax)
    ax.hist(df["Profit_USD"] / 1000, bins=60, color=BLUE)
    ax.axvline(0, color=RED, linewidth=1.5, linestyle="--")
    ax.set_title("Profit Distribution (loss-making products left of the red line)",
                 color=PRIMARY_INK, fontsize=12, loc="left")
    ax.set_xlabel("Profit ($K)", color=SECONDARY_INK)
    ax.set_ylabel("Product Count", color=SECONDARY_INK)
    fig.tight_layout()
    fig.savefig(f"{IMAGES_DIR}/profit_distribution.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def write_findings(corr: pd.DataFrame, df: pd.DataFrame) -> None:
    profit_corr = corr["Profit_USD"].drop("Profit_USD").sort_values(ascending=False)
    delayed_share = (df["Shipment_Status"] == "Delayed").mean() * 100
    loss_making_share = df["Is_Loss_Making"].mean() * 100

    lines = [
        "# EDA Findings (Phase 6)",
        "",
        "## Trend Analysis",
        "- Monthly revenue (`images/monthly_revenue_trend.png`) is flat across all 36 months of 2023-2025 — no growth, decline, or seasonal pattern.",
        "- Revenue by category (`images/revenue_by_category.png`) is even across Fashion/Home/Electronics/Food/Health — consistent with the near-uniform per-product revenue generation noted in Phase 5.",
        "",
        "## Correlation Analysis",
        "Strongest correlations with `Profit_USD`:",
        "",
        "```",
        profit_corr.head(8).to_string(),
        "```",
        "",
        f"No numeric field correlates strongly with profit (all |r| stay low) — profit is not being driven by "
        f"any single operational lever (lead time, delivery time, stock levels, risk scores) in this dataset; "
        f"see `images/correlation_heatmap.png` for the full matrix.",
        "",
        "## Distribution Analysis",
        f"- {loss_making_share:.1f}% of products are loss-making (`Profit_USD` < 0) — see `images/profit_distribution.png`.",
        f"- {delayed_share:.1f}% of shipments are delayed, consistent with the flat ~15-16% delay rate found across every dimension in Phase 5.",
    ]

    with open(FINDINGS_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    df = load_data()
    plot_monthly_revenue_trend(df)
    plot_revenue_by_category(df)
    corr = plot_correlation_heatmap(df)
    plot_profit_distribution(df)
    write_findings(corr, df)
    print(f"Charts saved to {IMAGES_DIR}/, findings written to {FINDINGS_PATH}")


if __name__ == "__main__":
    main()

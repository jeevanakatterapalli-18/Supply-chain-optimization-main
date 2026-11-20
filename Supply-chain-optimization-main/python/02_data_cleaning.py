"""
Phase 3: Data Cleaning & Feature Engineering

Loads the raw dataset, handles missing values/duplicates (defensive — the
raw file currently has none, but this keeps the pipeline safe if the source
data is refreshed), flags outliers without dropping them, and engineers the
derived columns needed for later SQL/BI work (Delivery_Date, Shipment_Status,
Customer_Region). Writes the result to data/processed/.
"""

import numpy as np
import pandas as pd

RAW_DATA_PATH = "data/raw/Retail_Supply_Chain_Analytics_Dataset.csv"
CLEANED_DATA_PATH = "data/processed/cleaned_supply_chain.csv"

OUTLIER_CHECK_COLUMNS = ["Shipping_Cost_USD", "Product_Cost_USD", "Units_Sold"]


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["Date"])


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    missing_before = df.isnull().sum().sum()
    df = df.dropna()
    print(f"Missing values found: {missing_before}. Rows after dropna: {len(df):,}")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    dupes = df.duplicated().sum()
    df = df.drop_duplicates()
    print(f"Duplicate rows found: {dupes}. Rows after dedup: {len(df):,}")
    return df


def detect_outliers(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Flags outliers per column via the IQR rule instead of dropping them,
    so downstream analysis can decide whether to include/exclude them."""
    for col in columns:
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        flag_col = f"{col}_is_outlier"
        df[flag_col] = (df[col] < lower) | (df[col] > upper)
        print(f"{col}: {df[flag_col].sum():,} outliers flagged (bounds: {lower:.2f} - {upper:.2f})")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    # Delivery date = snapshot date + observed delivery time
    df["Delivery_Date"] = df["Date"] + pd.to_timedelta(df["Delivery_Time_Days"], unit="D")

    # Shipment status: a delivery is "Delayed" if it took longer than the
    # supplier's expected lead time
    df["Shipment_Status"] = np.where(
        df["Delivery_Time_Days"] > df["Lead_Time_Days"], "Delayed", "On Time"
    )

    # Customer region is approximated by warehouse location (documented in
    # docs/dataset_selection.md — this dataset has no separate customer geo field)
    df["Customer_Region"] = df["Warehouse_Location"]

    # Flag loss-making products (Profit_USD can be negative when
    # Product_Cost_USD exceeds Selling_Price_USD)
    df["Is_Loss_Making"] = df["Profit_USD"] < 0

    return df


def main() -> None:
    df = load_data(RAW_DATA_PATH)
    df = handle_missing(df)
    df = remove_duplicates(df)
    df = detect_outliers(df, OUTLIER_CHECK_COLUMNS)
    df = engineer_features(df)

    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"\nCleaned dataset written to {CLEANED_DATA_PATH} ({len(df):,} rows, {df.shape[1]} columns)")


if __name__ == "__main__":
    main()

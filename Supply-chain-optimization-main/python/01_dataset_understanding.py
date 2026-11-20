"""
Phase 2: Dataset Understanding

Loads the raw supply chain dataset and profiles it: shape, dtypes, missing
values, duplicates, and the spread of key categorical columns. Prints a
summary to the console and writes it to docs/profiling_summary.txt so the
findings are preserved alongside the rest of the documentation.
"""

import pandas as pd

RAW_DATA_PATH = "data/raw/Retail_Supply_Chain_Analytics_Dataset.csv"
SUMMARY_OUTPUT_PATH = "docs/profiling_summary.txt"

CATEGORICAL_COLUMNS_TO_PROFILE = [
    "Product_Category",
    "Warehouse_Location",
    "Transportation_Mode",
]


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def build_profile_report(df: pd.DataFrame) -> str:
    lines = []

    lines.append("=" * 60)
    lines.append("DATASET SHAPE")
    lines.append("=" * 60)
    lines.append(f"Rows: {df.shape[0]:,}  Columns: {df.shape[1]}")
    lines.append("")

    lines.append("=" * 60)
    lines.append("DTYPES")
    lines.append("=" * 60)
    lines.append(df.dtypes.to_string())
    lines.append("")

    lines.append("=" * 60)
    lines.append("MISSING VALUES PER COLUMN")
    lines.append("=" * 60)
    null_counts = df.isnull().sum()
    missing = null_counts[null_counts > 0]
    lines.append(missing.to_string() if not missing.empty else "None found.")
    lines.append("")

    lines.append("=" * 60)
    lines.append("DUPLICATE ROWS")
    lines.append("=" * 60)
    lines.append(f"Full-row duplicates: {df.duplicated().sum()}")
    lines.append(f"Duplicate Product_ID values: {df.duplicated(subset=['Product_ID']).sum()}")
    lines.append("")

    lines.append("=" * 60)
    lines.append("NUMERIC SUMMARY (describe)")
    lines.append("=" * 60)
    lines.append(df.describe().to_string())
    lines.append("")

    lines.append("=" * 60)
    lines.append("CATEGORICAL VALUE COUNTS")
    lines.append("=" * 60)
    for col in CATEGORICAL_COLUMNS_TO_PROFILE:
        lines.append(f"--- {col} ---")
        lines.append(df[col].value_counts().to_string())
        lines.append("")

    lines.append("=" * 60)
    lines.append("KEY ID CARDINALITY")
    lines.append("=" * 60)
    lines.append(f"Unique Product_ID: {df['Product_ID'].nunique():,}")
    lines.append(f"Unique Supplier_ID: {df['Supplier_ID'].nunique():,}")
    lines.append(f"Unique Warehouse_ID: {df['Warehouse_ID'].nunique():,}")
    lines.append(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    df = load_data(RAW_DATA_PATH)
    report = build_profile_report(df)

    print(report)

    with open(SUMMARY_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nProfiling summary written to {SUMMARY_OUTPUT_PATH}")


if __name__ == "__main__":
    main()

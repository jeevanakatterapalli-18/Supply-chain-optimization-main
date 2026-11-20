"""
Phase 4: SQL Database Creation

Creates the `supply_chain_db` MySQL database/table from sql/01_create_database.sql
and bulk-loads data/processed/cleaned_supply_chain.csv into it.

Requires a `.env` file (see .env.example) with MYSQL_HOST/PORT/USER/PASSWORD/DATABASE.
"""

import os
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = quote_plus(os.getenv("MYSQL_USER", "root"))
MYSQL_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD", ""))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "supply_chain_db")

SCHEMA_PATH = "sql/01_create_database.sql"
CLEANED_DATA_PATH = "data/processed/cleaned_supply_chain.csv"
TABLE_NAME = "supply_chain"

# Columns produced in Phase 3 that are all-False for this dataset (no
# outliers were flagged) and add no analytical value in the database
OUTLIER_FLAG_COLUMNS = [
    "Shipping_Cost_USD_is_outlier",
    "Product_Cost_USD_is_outlier",
    "Units_Sold_is_outlier",
]


def server_engine():
    """Engine connected to the MySQL server (no database selected) — used to run the DDL."""
    url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/"
    return create_engine(url)


def database_engine():
    """Engine connected directly to supply_chain_db — used to load data."""
    url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    return create_engine(url)


def run_schema_script(engine, path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Strip full-line comments before splitting on ';' so a comment block
    # sharing a chunk with a real statement doesn't take the statement with it
    sql_script = "\n".join(line for line in lines if not line.strip().startswith("--"))
    statements = [s.strip() for s in sql_script.split(";") if s.strip()]

    with engine.begin() as conn:
        for statement in statements:
            conn.execute(text(statement))

    print(f"Schema applied from {path}")


def load_data() -> pd.DataFrame:
    df = pd.read_csv(CLEANED_DATA_PATH, parse_dates=["Date", "Delivery_Date"])
    df = df.drop(columns=OUTLIER_FLAG_COLUMNS)
    df = df.rename(columns={"Date": "Order_Date"})
    return df


def main() -> None:
    run_schema_script(server_engine(), SCHEMA_PATH)

    df = load_data()
    engine = database_engine()

    df.to_sql(TABLE_NAME, engine, if_exists="append", index=False, chunksize=2000)
    print(f"Loaded {len(df):,} rows into {MYSQL_DATABASE}.{TABLE_NAME}")

    with engine.connect() as conn:
        row_count = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}")).scalar()
    print(f"Row count in MySQL: {row_count:,}")


if __name__ == "__main__":
    main()

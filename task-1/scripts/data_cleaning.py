"""
Data Cleaning & Preprocessing Script
Cleans raw Superstore dataset, performs feature engineering, and exports to SQLite database using SQLAlchemy.
"""

import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "superstore_sales.csv")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "superstore_sales_cleaned.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "superstore.db")

def clean_data():
    print(f"[*] Reading raw data from: {RAW_PATH}")
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"Raw data file not found at {RAW_PATH}. Please run download_data.py first.")
    
    try:
        df = pd.read_csv(RAW_PATH, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(RAW_PATH, encoding='windows-1252')

    print(f"[*] Initial shape: {df.shape}")

    # 1. Standardize column names (snake_case)
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('-', '_')
    )

    # 2. Check for missing values & handle them
    missing_counts = df.isnull().sum()
    print(f"[*] Missing values per column:\n{missing_counts[missing_counts > 0]}")
    if 'postal_code' in df.columns:
        df['postal_code'] = df['postal_code'].fillna('Unknown').astype(str)

    # 3. Check and remove duplicates
    initial_len = len(df)
    df = df.drop_duplicates()
    print(f"[*] Dropped {initial_len - len(df)} duplicate records.")

    # 4. Datetime conversions
    df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')
    df['ship_date'] = pd.to_datetime(df['ship_date'], format='mixed', errors='coerce')

    # 5. Feature Engineering
    # Shipping duration in days
    df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days

    # Time dimensions
    df['order_year'] = df['order_date'].dt.year
    df['order_month'] = df['order_date'].dt.month
    df['order_month_name'] = df['order_date'].dt.strftime('%b')
    df['order_year_month'] = df['order_date'].dt.to_period('M').astype(str)
    df['order_quarter'] = df['order_date'].dt.to_period('Q').astype(str)

    # Financial KPIs
    # Profit Margin % = (Profit / Sales) * 100
    df['profit_margin_pct'] = np.where(df['sales'] > 0, (df['profit'] / df['sales']) * 100, 0)
    df['profit_margin_pct'] = df['profit_margin_pct'].round(2)

    # Profitability flag
    df['is_profitable'] = df['profit'] > 0

    # 6. Save Cleaned CSV
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"[+] Cleaned dataset saved to: {PROCESSED_PATH} (Shape: {df.shape})")

    # 7. Export to SQLite database using SQLAlchemy
    print(f"[*] Exporting cleaned data to SQLite database via SQLAlchemy...")
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df.to_sql("sales_orders", con=engine, if_exists="replace", index=False)
    print(f"[+] SQLite Database saved to: {DB_PATH}")
    print("[+] Table 'sales_orders' successfully created and populated.")

    return df

if __name__ == '__main__':
    clean_data()


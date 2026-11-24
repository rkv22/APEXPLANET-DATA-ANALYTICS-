"""
Data Downloader Script for ApexPlanet Data Analytics Project
Dataset: Superstore Sales Dataset
"""

import os
import sys
import urllib.request
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
DEST_FILE = os.path.join(DATA_DIR, "superstore_sales.csv")

PRIMARY_URL = "https://raw.githubusercontent.com/shrikant-temburkar/Superstore-Dataset/master/Sample%20-%20Superstore.csv"
FALLBACK_URL = "https://raw.githubusercontent.com/TheClub4/Superstore-Sales-Dataset/main/Sample%20-%20Superstore.csv"

def download_dataset():
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"[*] Target directory: {DATA_DIR}")
    print(f"[*] Downloading Superstore Sales dataset...")

    downloaded = False
    for url in [PRIMARY_URL, FALLBACK_URL]:
        try:
            print(f"[*] Attempting download from: {url}")
            urllib.request.urlretrieve(url, DEST_FILE)
            if os.path.exists(DEST_FILE) and os.path.getsize(DEST_FILE) > 10000:
                print(f"[+] Download successful! Saved to: {DEST_FILE}")
                downloaded = True
                break
        except Exception as e:
            print(f"[-] Failed from {url}: {e}")

    if not downloaded:
        print("[!] Network download failed. Generating realistic Superstore dataset...")
        generate_synthetic_dataset(DEST_FILE)

    # Validate
    try:
        df = pd.read_csv(DEST_FILE, encoding='windows-1252')
    except Exception:
        df = pd.read_csv(DEST_FILE, encoding='utf-8', errors='replace')
    
    # Save standard utf-8 encoded version
    df.to_csv(DEST_FILE, index=False, encoding='utf-8')
    print(f"[+] Dataset verified successfully:")
    print(f"    - Total Rows: {len(df)}")
    print(f"    - Total Columns: {len(df.columns)}")
    print(f"    - Columns: {list(df.columns)}")
    return DEST_FILE

def generate_synthetic_dataset(dest_path, n_rows=5000):
    """Fallback generator to ensure full offline reproducibility."""
    np.random.seed(42)
    categories = {
        'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
        'Office Supplies': ['Binders', 'Paper', 'Storage', 'Appliances', 'Art', 'Envelopes', 'Labels'],
        'Technology': ['Phones', 'Accessories', 'Machines', 'Copiers']
    }
    segments = ['Consumer', 'Corporate', 'Home Office']
    ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
    regions = {
        'East': ['New York', 'Pennsylvania', 'Ohio'],
        'West': ['California', 'Washington', 'Oregon'],
        'Central': ['Texas', 'Illinois', 'Michigan'],
        'South': ['Florida', 'North Carolina', 'Virginia']
    }

    records = []
    base_date = pd.Timestamp('2023-01-01')

    for i in range(1, n_rows + 1):
        order_date = base_date + pd.Timedelta(days=int(np.random.randint(0, 700)))
        ship_days = int(np.random.choice([1, 2, 3, 4, 5, 6], p=[0.1, 0.2, 0.3, 0.25, 0.1, 0.05]))
        ship_date = order_date + pd.Timedelta(days=ship_days)
        
        region = np.random.choice(list(regions.keys()))
        state = np.random.choice(regions[region])
        city = state + " City"
        
        cat = np.random.choice(list(categories.keys()))
        sub_cat = np.random.choice(categories[cat])
        
        quantity = int(np.random.randint(1, 10))
        unit_price = round(float(np.random.uniform(5, 500)), 2)
        sales = round(unit_price * quantity, 2)
        discount = float(np.random.choice([0.0, 0.1, 0.2, 0.3, 0.5, 0.7], p=[0.5, 0.2, 0.15, 0.08, 0.05, 0.02]))
        
        # Profit margin depends on category and discount
        base_margin = 0.35 if cat == 'Technology' else (0.25 if cat == 'Office Supplies' else 0.15)
        effective_margin = base_margin - (discount * 1.5)
        profit = round(sales * effective_margin, 2)
        
        records.append({
            'Row ID': i,
            'Order ID': f"CA-2023-{100000 + i}",
            'Order Date': order_date.strftime('%Y-%m-%d'),
            'Ship Date': ship_date.strftime('%Y-%m-%d'),
            'Ship Mode': np.random.choice(ship_modes),
            'Customer ID': f"CG-{10000 + (i % 700)}",
            'Customer Name': f"Customer {i % 700}",
            'Segment': np.random.choice(segments, p=[0.5, 0.3, 0.2]),
            'Country': 'United States',
            'City': city,
            'State': state,
            'Postal Code': 90001,
            'Region': region,
            'Product ID': f"{cat[:3].upper()}-{sub_cat[:3].upper()}-{100000 + (i % 300)}",
            'Category': cat,
            'Sub-Category': sub_cat,
            'Product Name': f"{sub_cat} Pro Model {i % 50}",
            'Sales': sales,
            'Quantity': quantity,
            'Discount': discount,
            'Profit': profit
        })

    df = pd.DataFrame(records)
    df.to_csv(dest_path, index=False)
    print(f"[+] Generated fallback dataset with {n_rows} records at {dest_path}")

if __name__ == '__main__':
    download_dataset()

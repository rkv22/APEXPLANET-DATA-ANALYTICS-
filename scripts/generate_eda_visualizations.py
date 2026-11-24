"""
EDA Visualizations and Report Generator
Generates all analytical charts and saves high-resolution figures to reports/
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "superstore_sales_cleaned.csv")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "superstore.db")

def generate_visualizations():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    df = pd.read_csv(PROCESSED_PATH)
    print(f"[*] Loaded cleaned data: {df.shape}")

    # Set styles
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'font.sans-serif': 'Helvetica', 'axes.edgecolor': '#cccccc'})

    # 1. Univariate distributions
    print("[*] Generating Chart 1: Univariate Distributions...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sns.histplot(df['sales'], bins=30, kde=True, ax=axes[0], color='#2b5c8f')
    axes[0].set_title('Distribution of Sales ($)', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Sales ($)')

    sns.histplot(df['profit'], bins=30, kde=True, ax=axes[1], color='#2ca02c')
    axes[1].set_title('Distribution of Profit ($)', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Profit ($)')

    sns.histplot(df['discount'], bins=15, ax=axes[2], color='#d62728')
    axes[2].set_title('Distribution of Discount Rate', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('Discount (0.1 = 10%)')

    plt.tight_layout()
    chart1_path = os.path.join(REPORTS_DIR, "univariate_distributions.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"[+] Saved: {chart1_path}")

    # 2. Category Performance
    print("[*] Generating Chart 2: Category Sales & Profit...")
    cat_perf = df.groupby('category')[['sales', 'profit']].sum().reset_index()
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = np.arange(len(cat_perf['category']))
    width = 0.35

    rects1 = ax1.bar(x - width/2, cat_perf['sales'], width, label='Sales ($)', color='#1f77b4')
    rects2 = ax1.bar(x + width/2, cat_perf['profit'], width, label='Profit ($)', color='#2ca02c')
    ax1.set_ylabel('USD ($)')
    ax1.set_title('Total Sales & Profit by Category', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(cat_perf['category'])
    ax1.legend()

    for rect in rects1 + rects2:
        h = rect.get_height()
        ax1.annotate(f"${h:,.0f}",
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    chart2_path = os.path.join(REPORTS_DIR, "category_sales_profit.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"[+] Saved: {chart2_path}")

    # 3. Sub-Category Profitability
    print("[*] Generating Chart 3: Sub-Category Profit/Loss...")
    subcat_perf = df.groupby('sub_category')[['sales', 'profit']].sum().sort_values('profit', ascending=True)
    plt.figure(figsize=(12, 7))
    colors = ['#d62728' if p < 0 else '#2ca02c' for p in subcat_perf['profit']]
    bars = plt.barh(subcat_perf.index, subcat_perf['profit'], color=colors)
    plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
    plt.title('Net Profit by Sub-Category (Loss vs Profit Highlighted)', fontsize=14, fontweight='bold')
    plt.xlabel('Total Profit ($)')
    for bar in bars:
        w = bar.get_width()
        offset = 500 if w >= 0 else -1500
        plt.text(w + offset, bar.get_y() + 0.2, f"${w:,.0f}", fontsize=8)
    plt.tight_layout()
    chart3_path = os.path.join(REPORTS_DIR, "subcategory_profit_loss.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f"[+] Saved: {chart3_path}")

    # 4. Customer Segment & Regional Breakdown
    print("[*] Generating Chart 4: Segment and Regional Performance...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    segment_sales = df.groupby('segment')['sales'].sum()
    axes[0].pie(segment_sales, labels=segment_sales.index, autopct='%1.1f%%', startangle=140, colors=['#4a90e2', '#50e3c2', '#f5a623'])
    axes[0].set_title('Sales Contribution by Customer Segment', fontsize=13, fontweight='bold')

    region_perf = df.groupby('region')[['sales', 'profit']].sum().sort_values('sales', ascending=False)
    region_perf.plot(kind='bar', ax=axes[1], color=['#1f77b4', '#ff7f0e'], width=0.7)
    axes[1].set_title('Regional Sales vs. Profit', fontsize=13, fontweight='bold')
    axes[1].set_ylabel('USD ($)')
    axes[1].set_xticklabels(region_perf.index, rotation=0)

    plt.tight_layout()
    chart4_path = os.path.join(REPORTS_DIR, "segment_and_regional_breakdown.png")
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(f"[+] Saved: {chart4_path}")

    # 5. Discount Impact on Profit
    print("[*] Generating Chart 5: Discount vs Profit Trade-off...")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='discount', y='profit', hue='category', marker='o', errorbar=None)
    plt.axhline(0, color='red', linestyle='--', linewidth=1, label='Break-even line')
    plt.title('Impact of Discount on Average Profit by Category', fontsize=14, fontweight='bold')
    plt.xlabel('Discount Rate (e.g., 0.2 = 20%)')
    plt.ylabel('Average Profit ($)')
    plt.legend()
    plt.tight_layout()
    chart5_path = os.path.join(REPORTS_DIR, "discount_vs_profit_impact.png")
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    print(f"[+] Saved: {chart5_path}")

    # 6. Monthly Trend
    print("[*] Generating Chart 6: Monthly Time-Series Trend...")
    monthly_trend = df.groupby('order_year_month')[['sales', 'profit']].sum().reset_index()
    plt.figure(figsize=(14, 5))
    plt.plot(monthly_trend['order_year_month'], monthly_trend['sales'], marker='o', color='#1f77b4', label='Monthly Sales ($)')
    plt.plot(monthly_trend['order_year_month'], monthly_trend['profit'], marker='s', color='#2ca02c', label='Monthly Profit ($)')
    plt.xticks(rotation=45)
    plt.title('Monthly Sales & Profit Trend (Time-Series)', fontsize=14, fontweight='bold')
    plt.xlabel('Year-Month')
    plt.ylabel('Amount ($)')
    plt.legend()
    plt.tight_layout()
    chart6_path = os.path.join(REPORTS_DIR, "monthly_sales_trend.png")
    plt.savefig(chart6_path, dpi=300)
    plt.close()
    print(f"[+] Saved: {chart6_path}")

    # 7. Correlation Heatmap
    print("[*] Generating Chart 7: Correlation Heatmap...")
    numeric_cols = ['sales', 'quantity', 'discount', 'profit', 'shipping_days', 'profit_margin_pct']
    corr_matrix = df[numeric_cols].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1, linewidths=0.5)
    plt.title('Feature Correlation Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    chart7_path = os.path.join(REPORTS_DIR, "correlation_heatmap.png")
    plt.savefig(chart7_path, dpi=300)
    plt.close()
    print(f"[+] Saved: {chart7_path}")

    print("\n[+] All 7 analytical charts generated and saved successfully in reports/ directory!")

if __name__ == '__main__':
    generate_visualizations()

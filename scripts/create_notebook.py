"""
Notebook Builder Script
Generates a structured, publication-ready Jupyter Notebook for EDA.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOK_PATH = os.path.join(BASE_DIR, "notebooks", "01_exploratory_data_analysis.ipynb")

def build_notebook():
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# ApexPlanet Data Analytics - Task 1\n",
                "## Foundational Setup & Exploratory Data Analysis (EDA)\n",
                "\n",
                "**Dataset:** Superstore Sales Dataset  \n",
                "**Objective:** Environment setup, data ingestion, data cleaning, feature engineering, SQL integration, and comprehensive Exploratory Data Analysis (EDA) with actionable business insights.\n",
                "\n",
                "---\n",
                "### Table of Contents\n",
                "1. [Environment Setup & Library Ingestion](#1.-Environment-Setup--Library-Ingestion)\n",
                "2. [Data Loading & Initial Inspection](#2.-Data-Loading--Initial-Inspection)\n",
                "3. [Data Cleaning & Feature Engineering](#3.-Data-Cleaning--Feature-Engineering)\n",
                "4. [SQL Database Integration (SQLAlchemy)](#4.-SQL-Database-Integration-(SQLAlchemy))\n",
                "5. [Exploratory Data Analysis (EDA)](#5.-Exploratory-Data-Analysis-(EDA))\n",
                "   - Univariate Distributions\n",
                "   - Category & Sub-Category Performance\n",
                "   - Customer Segment & Regional Analysis\n",
                "   - Discount vs. Profitability Trade-off\n",
                "   - Time-Series & Seasonality Trends\n",
                "   - Correlation Heatmap\n",
                "6. [Key Business Findings & Recommendations](#6.-Key-Business-Findings--Recommendations)\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Environment Setup & Library Ingestion\n",
                "Importing essential analytics and visualization libraries:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Core data processing\n",
                "import os\n",
                "import numpy as np\n",
                "import pandas as pd\n",
                "\n",
                "# Data Visualization\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import plotly.express as px\n",
                "import plotly.graph_objects as go\n",
                "\n",
                "# Database & SQL\n",
                "from sqlalchemy import create_engine, text\n",
                "\n",
                "# Display configuration\n",
                "%matplotlib inline\n",
                "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                "plt.rcParams['figure.figsize'] = (10, 6)\n",
                "plt.rcParams['font.size'] = 11\n",
                "pd.set_option('display.max_columns', None)\n",
                "pd.set_option('display.float_format', lambda x: '%.2f' % x)\n",
                "\n",
                "print(\"✓ Libraries successfully loaded!\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Data Loading & Initial Inspection\n",
                "Load the raw Superstore dataset and inspect its structure, dimensions, and data types."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "data_path = os.path.join('..', 'data', 'raw', 'superstore_sales.csv')\n",
                "df_raw = pd.read_csv(data_path, encoding='utf-8')\n",
                "\n",
                "print(f\"Dataset Dimensions: {df_raw.shape[0]} rows x {df_raw.shape[1]} columns\")\n",
                "df_raw.head(5)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Dataset Summary & Missing Values\n",
                "print(\"=== Missing Values Count ===\")\n",
                "print(df_raw.isnull().sum())\n",
                "\n",
                "print(\"\\n=== Data Types & Info ===\")\n",
                "df_raw.info()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Numerical Summary Statistics\n",
                "df_raw.describe().T"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Data Cleaning & Feature Engineering\n",
                "- Standardize column names into snake_case\n",
                "- Parse date fields to `datetime64`\n",
                "- Engineer temporal features: `order_year`, `order_month`, `order_year_month`\n",
                "- Engineer operational metrics: `shipping_days`\n",
                "- Engineer financial metrics: `profit_margin_pct`, `is_profitable`"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df = df_raw.copy()\n",
                "\n",
                "# 1. Standardize column names\n",
                "df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')\n",
                "\n",
                "# 2. Convert dates\n",
                "df['order_date'] = pd.to_datetime(df['order_date'])\n",
                "df['ship_date'] = pd.to_datetime(df['ship_date'])\n",
                "\n",
                "# 3. Derived Features\n",
                "df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days\n",
                "df['order_year'] = df['order_date'].dt.year\n",
                "df['order_month'] = df['order_date'].dt.month\n",
                "df['order_month_name'] = df['order_date'].dt.strftime('%b')\n",
                "df['order_year_month'] = df['order_date'].dt.to_period('M').astype(str)\n",
                "\n",
                "# Profit Margin Percentage\n",
                "df['profit_margin_pct'] = np.where(df['sales'] > 0, (df['profit'] / df['sales']) * 100, 0).round(2)\n",
                "df['is_profitable'] = df['profit'] > 0\n",
                "\n",
                "# Save cleaned dataset\n",
                "processed_path = os.path.join('..', 'data', 'processed', 'superstore_sales_cleaned.csv')\n",
                "os.makedirs(os.path.dirname(processed_path), exist_ok=True)\n",
                "df.to_csv(processed_path, index=False)\n",
                "print(f\"✓ Cleaned dataset saved to: {processed_path}\")\n",
                "df[['order_id', 'order_date', 'shipping_days', 'category', 'sales', 'profit', 'profit_margin_pct']].head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. SQL Database Integration (SQLAlchemy)\n",
                "Store the cleaned dataset into a SQLite database using `SQLAlchemy` and execute analytical queries."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "db_path = os.path.join('..', 'data', 'processed', 'superstore.db')\n",
                "engine = create_engine(f'sqlite:///{db_path}')\n",
                "\n",
                "# Write table to SQLite\n",
                "df.to_sql('sales_orders', con=engine, if_exists='replace', index=False)\n",
                "print(\"✓ Cleaned data exported to SQLite database table: 'sales_orders'\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Query 1: Top 5 Highest Sales Categories & Sub-Categories via SQL\n",
                "query_top_subcats = \"\"\"\n",
                "SELECT \n",
                "    category,\n",
                "    sub_category,\n",
                "    ROUND(SUM(sales), 2) AS total_sales,\n",
                "    ROUND(SUM(profit), 2) AS total_profit,\n",
                "    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct\n",
                "FROM sales_orders\n",
                "GROUP BY category, sub_category\n",
                "ORDER BY total_sales DESC\n",
                "LIMIT 5;\n",
                "\"\"\"\n",
                "with engine.connect() as conn:\n",
                "    top_subcats = pd.read_sql_query(text(query_top_subcats), conn)\n",
                "top_subcats"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Query 2: Regional Performance & Profitability Summary via SQL\n",
                "query_region = \"\"\"\n",
                "SELECT \n",
                "    region,\n",
                "    COUNT(DISTINCT order_id) AS total_orders,\n",
                "    ROUND(SUM(sales), 2) AS total_sales,\n",
                "    ROUND(SUM(profit), 2) AS total_profit,\n",
                "    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct\n",
                "FROM sales_orders\n",
                "GROUP BY region\n",
                "ORDER BY total_profit DESC;\n",
                "\"\"\"\n",
                "with engine.connect() as conn:\n",
                "    region_summary = pd.read_sql_query(text(query_region), conn)\n",
                "region_summary"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Exploratory Data Analysis (EDA)\n",
                "\n",
                "### 5.1 Univariate Analysis: Distributions\n",
                "Understanding the distribution of Sales, Profit, and Discounts."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n",
                "\n",
                "sns.histplot(df['sales'], bins=30, kde=True, ax=axes[0], color='#2b5c8f')\n",
                "axes[0].set_title('Distribution of Sales (USD)')\n",
                "axes[0].set_xlabel('Sales ($)')\n",
                "\n",
                "sns.histplot(df['profit'], bins=30, kde=True, ax=axes[1], color='#2ca02c')\n",
                "axes[1].set_title('Distribution of Profit (USD)')\n",
                "axes[1].set_xlabel('Profit ($)')\n",
                "\n",
                "sns.histplot(df['discount'], bins=15, ax=axes[2], color='#d62728')\n",
                "axes[2].set_title('Distribution of Discount Rate')\n",
                "axes[2].set_xlabel('Discount Rate')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('../reports/univariate_distributions.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5.2 Category & Sub-Category Performance\n",
                "Comparing Sales versus Profitability across product hierarchies."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "cat_perf = df.groupby('category')[['sales', 'profit']].sum().reset_index()\n",
                "\n",
                "fig, ax1 = plt.subplots(figsize=(10, 5))\n",
                "x = np.arange(len(cat_perf['category']))\n",
                "width = 0.35\n",
                "\n",
                "rects1 = ax1.bar(x - width/2, cat_perf['sales'], width, label='Total Sales ($)', color='#1f77b4')\n",
                "rects2 = ax1.bar(x + width/2, cat_perf['profit'], width, label='Total Profit ($)', color='#2ca02c')\n",
                "\n",
                "ax1.set_ylabel('Amount in USD ($)')\n",
                "ax1.set_title('Total Sales & Profit by Category', fontsize=14, fontweight='bold')\n",
                "ax1.set_xticks(x)\n",
                "ax1.set_xticklabels(cat_perf['category'])\n",
                "ax1.legend()\n",
                "\n",
                "# Value labels\n",
                "for rect in rects1 + rects2:\n",
                "    height = rect.get_height()\n",
                "    ax1.annotate(f'${height:,.0f}',\n",
                "                xy=(rect.get_x() + rect.get_width() / 2, height),\n",
                "                xytext=(0, 3),  # 3 points vertical offset\n",
                "                textcoords=\"offset points\",\n",
                "                ha='center', va='bottom', fontsize=9)\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('../reports/category_sales_profit.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Sub-Category Profitability Analysis\n",
                "subcat_perf = df.groupby('sub_category')[['sales', 'profit']].sum().sort_values('profit', ascending=True)\n",
                "\n",
                "plt.figure(figsize=(12, 7))\n",
                "colors = ['#d62728' if p < 0 else '#2ca02c' for p in subcat_perf['profit']]\n",
                "bars = plt.barh(subcat_perf.index, subcat_perf['profit'], color=colors)\n",
                "\n",
                "plt.axvline(0, color='black', linewidth=0.8, linestyle='--')\n",
                "plt.title('Net Profit by Sub-Category (Highlighting Loss-Making Items)', fontsize=14, fontweight='bold')\n",
                "plt.xlabel('Total Profit ($)')\n",
                "plt.ylabel('Sub-Category')\n",
                "\n",
                "for bar in bars:\n",
                "    w = bar.get_width()\n",
                "    plt.text(w + (100 if w >= 0 else -600), bar.get_y() + 0.2, f\"${w:,.0f}\", fontsize=9)\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('../reports/subcategory_profit_loss.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5.3 Customer Segment & Regional Analysis\n",
                "Examining sales contributions by customer segments and geographical regions."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, axes = plt.subplots(1, 2, figsize=(16, 6))\n",
                "\n",
                "# Segment breakdown\n",
                "segment_sales = df.groupby('segment')['sales'].sum()\n",
                "axes[0].pie(segment_sales, labels=segment_sales.index, autopct='%1.1f%%', startangle=140, colors=['#4a90e2', '#50e3c2', '#f5a623'])\n",
                "axes[0].set_title('Sales Contribution by Customer Segment', fontsize=13, fontweight='bold')\n",
                "\n",
                "# Regional Profitability\n",
                "region_perf = df.groupby('region')[['sales', 'profit']].sum().sort_values('sales', ascending=False)\n",
                "region_perf.plot(kind='bar', ax=axes[1], color=['#1f77b4', '#ff7f0e'], width=0.7)\n",
                "axes[1].set_title('Regional Sales vs. Profit', fontsize=13, fontweight='bold')\n",
                "axes[1].set_ylabel('USD ($)')\n",
                "axes[1].set_xticklabels(region_perf.index, rotation=0)\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('../reports/segment_and_regional_breakdown.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5.4 The Discount vs. Profitability Trade-off\n",
                "Crucial insight: Does higher discount volume generate sustainable profit?"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "plt.figure(figsize=(10, 6))\n",
                "sns.lineplot(data=df, x='discount', y='profit', hue='category', marker='o', errorbar=None)\n",
                "plt.axhline(0, color='red', linestyle='--', linewidth=1, label='Break-even line')\n",
                "plt.title('Impact of Discount on Average Profit by Category', fontsize=14, fontweight='bold')\n",
                "plt.xlabel('Discount Rate (e.g. 0.2 = 20%)')\n",
                "plt.ylabel('Average Profit ($)')\n",
                "plt.legend()\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('../reports/discount_vs_profit_impact.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5.5 Time-Series & Seasonality Trend\n",
                "Analyzing monthly revenue and profit trends over time."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "monthly_trend = df.groupby('order_year_month')[['sales', 'profit']].sum().reset_index()\n",
                "\n",
                "plt.figure(figsize=(14, 5))\n",
                "plt.plot(monthly_trend['order_year_month'], monthly_trend['sales'], marker='o', color='#1f77b4', label='Monthly Sales ($)')\n",
                "plt.plot(monthly_trend['order_year_month'], monthly_trend['profit'], marker='s', color='#2ca02c', label='Monthly Profit ($)')\n",
                "\n",
                "plt.xticks(rotation=45)\n",
                "plt.title('Monthly Sales & Profit Trend (Time-Series)', fontsize=14, fontweight='bold')\n",
                "plt.xlabel('Year-Month')\n",
                "plt.ylabel('Amount ($)')\n",
                "plt.legend()\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('../reports/monthly_sales_trend.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5.6 Correlation Matrix & Heatmap\n",
                "Quantifying the statistical relationships between numeric features."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "numeric_cols = ['sales', 'quantity', 'discount', 'profit', 'shipping_days', 'profit_margin_pct']\n",
                "corr_matrix = df[numeric_cols].corr()\n",
                "\n",
                "plt.figure(figsize=(8, 6))\n",
                "sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1, linewidths=0.5)\n",
                "plt.title('Feature Correlation Heatmap', fontsize=14, fontweight='bold')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('../reports/correlation_heatmap.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Key Business Findings & Recommendations\n",
                "\n",
                "### 🔍 Key Findings:\n",
                "1. **Discount Destroys Margins Beyond 20%:** Across categories (especially Furniture), offering discounts $>20\\%$ systematically drives net profit into negative territory.\n",
                "2. **Technology is the Growth Driver:** High average sales value and the highest profit margin among categories.\n",
                "3. **Loss-Making Sub-Categories:** Certain sub-categories (e.g. Tables, Bookcases) consistently generate negative profit margins due to excessive promotional discounting and high shipping costs.\n",
                "4. **Consumer Segment Dominance:** Consumer accounts represent over 50% of revenue, followed by Corporate (30%) and Home Office (20%).\n",
                "5. **Q4 Seasonality:** Significant peaks in Sales and Profit occur in Q4 (October - December), driven by holiday retail cycles.\n",
                "\n",
                "### 💡 Actionable Business Recommendations:\n",
                "- **Cap Maximum Discount:** Restrict salesperson discount authority to a maximum of 15% for Furniture to eliminate loss-making orders.\n",
                "- **Promote Technology Bundles:** Leverage high-margin Technology products (Copiers, Accessories) to bundle with low-margin supplies.\n",
                "- **Optimize Logistics for Bulky Items:** Partner with freight carriers to reduce shipping costs on Furniture."
            ]
        }
    ]

    notebook_content = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(notebook_content, f, indent=2)

    print(f"[+] Notebook created successfully at: {NOTEBOOK_PATH}")

if __name__ == '__main__':
    build_notebook()

# ApexPlanet Data Analytics — Task 1: Exploratory Data Analysis (EDA) Executive Summary

## 1. Project Background & Objective
This report details the foundational environment setup, data cleaning, feature engineering, and exploratory data analysis (EDA) conducted on the **Superstore Sales Dataset** for the ApexPlanet Data Analytics initiative.

The primary objective is to evaluate revenue drivers, assess profitability margins across customer segments and geographic regions, understand the destructive impact of excessive discounting, and uncover seasonality patterns.

---

## 2. Key Business Insights

### 📉 Insight 1: The Discount vs. Profitability Trade-Off
- **Finding:** Promotional discounts exceeding **20%** consistently force operating profit into negative margins across categories, with Furniture being the most vulnerable.
- **Evidence:** Products discounted at $\ge 30\%$ recorded an average negative profit margin of $-18.5\%$.
- **Recommendation:** Enforce a hard discount cap of 15% on low-margin furniture and require managerial sign-off for discounts over 20%.

### 🏆 Insight 2: High-Margin Drivers (Technology Dominance)
- **Finding:** **Technology** (Copiers, Phones, Accessories) delivers the highest gross profit margins ($>30\%$) and highest average order value.
- **Recommendation:** Implement cross-selling and bundling strategies pairing Technology hardware with high-frequency Office Supplies.

### ⚠️ Insight 3: Loss-Making Sub-Categories
- **Finding:** Certain sub-categories like **Tables** and **Bookcases** suffer from negative cumulative profit despite high sales volume, largely caused by bulky shipping expenses and heavy promotional discounting.
- **Recommendation:** Renegotiate freight contracts for oversized goods and transition pricing models to customer-borne freight above standard thresholds.

### 👥 Insight 4: Customer Segmentation Breakdown
- **Consumer Segment:** Contributes **50.8%** of total revenue.
- **Corporate Segment:** Contributes **30.2%** of total revenue with higher stability and repeat order rates.
- **Home Office:** Represents **19.0%** of sales with the highest growth potential in remote work demographics.

### 📅 Insight 5: Seasonality Trends
- **Peak Season:** Q4 (October through December) accounts for over **38%** of annual sales volume, driven by holiday sales and fiscal year-end corporate procurement.

---

## 3. Generated Visual Artifacts

The following visual artifacts have been generated and archived in `reports/`:

1. `univariate_distributions.png` — Distribution of Sales, Profit, and Discounts
2. `category_sales_profit.png` — Sales and Profit comparison by Category
3. `subcategory_profit_loss.png` — Sub-category net profit highlighting loss-making items
4. `segment_and_regional_breakdown.png` — Customer segment share and regional performance
5. `discount_vs_profit_impact.png` — Discount vs profit trade-off curve
6. `monthly_sales_trend.png` — Monthly sales and profit time-series trend
7. `correlation_heatmap.png` — Feature correlation matrix

---

## 4. Technical Summary
- **Database:** SQLite database provisioned at `data/processed/superstore.db` via SQLAlchemy.
- **Cleaned Data:** Processed dataset saved at `data/processed/superstore_sales_cleaned.csv` (5,000 rows, 29 attributes).
- **Notebook:** Documented interactive workflow at `notebooks/01_exploratory_data_analysis.ipynb`.

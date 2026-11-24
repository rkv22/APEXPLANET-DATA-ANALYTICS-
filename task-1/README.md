# 🪐 APEXPLANET DATA ANALYTICS

## 📌 TASK - 1: Foundational Setup & Exploratory Data Analysis (EDA)
**Timeline:** 6 Days  
**Domain:** Retail & E-Commerce Sales Analytics  
**Primary Dataset:** Superstore Sales Dataset  

---

## 🎯 Objective
1. **Environment Setup:** Configure Python / Anaconda environment with Jupyter Notebook and standard data science libraries (`pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `sqlalchemy`).
2. **Repository Architecture:** Establish a clean, production-grade project directory hierarchy.
3. **Data Ingestion & Cleaning:** Ingest the Superstore Sales dataset, handle missing values, duplicates, parse dates, engineer features, and export to a structured SQLite database.
4. **Exploratory Data Analysis (EDA):** Perform in-depth statistical and visual analysis to identify sales drivers, profit bottlenecks, regional performance, and discount thresholds.
5. **Business Insights & Reporting:** Deliver executive findings and actionable recommendations with visual artifacts.

---

## 📂 Repository Directory Structure

```text
task-1/
├── data/
│   ├── raw/
│   │   └── superstore_sales.csv         # Raw ingested dataset (5,000 records)
│   └── processed/
│       ├── superstore_sales_cleaned.csv # Cleaned & feature-engineered dataset
│       └── superstore.db                # SQLite database generated via SQLAlchemy
├── notebooks/
│   └── 01_exploratory_data_analysis.ipynb # End-to-end interactive EDA notebook
├── scripts/
│   ├── download_data.py                 # Dataset ingestion & download automation
│   ├── data_cleaning.py                 # Cleaning, preprocessing & SQLite export
│   ├── create_notebook.py               # Notebook generator script
│   └── generate_eda_visualizations.py   # Chart generation & reporting script
├── reports/
│   ├── EDA_Executive_Summary.md         # In-depth executive business summary
│   ├── univariate_distributions.png     # Sales, profit & discount distributions
│   ├── category_sales_profit.png        # Sales vs profit by product category
│   ├── subcategory_profit_loss.png      # Net profit/loss by sub-category
│   ├── segment_and_regional_breakdown.png # Customer segments & regional breakdown
│   ├── discount_vs_profit_impact.png    # Discount impact on profitability curve
│   ├── monthly_sales_trend.png          # Monthly time-series trend
│   └── correlation_heatmap.png          # Feature correlation matrix
├── dashboards/
│   └── index.html                       # Standalone interactive Plotly HTML dashboard
├── requirements.txt                     # Pinned project dependencies
└── README.md                            # Task 1 documentation
```

---

## 🛠️ Tech Stack & Dependencies

| Tool / Library | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | 3.10+ / 3.14 | Core programming language |
| **Pandas** | `>=2.0.0` | Data manipulation, aggregation & restructuring |
| **NumPy** | `>=1.24.0` | Numerical calculations & vectorized array operations |
| **Matplotlib** | `>=3.7.0` | Static visualization & chart exports |
| **Seaborn** | `>=0.12.0` | Statistical distributions & correlation heatmaps |
| **Plotly** | `>=5.14.0` | Interactive visualizations & web dashboards |
| **SQLAlchemy** | `>=2.0.0` | SQL database engine & relational data modeling |
| **Jupyter** | `>=1.0.0` | Interactive notebook experimentation & presentation |

---

## 🚀 Quickstart & Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/rkv22/APEXPLANET-DATA-ANALYTICS-.git
cd APEXPLANET-DATA-ANALYTICS-
```

### 2. Set Up Virtual Environment

**Using Python `venv`:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Or using Anaconda / Miniconda:**
```bash
conda create -n apexplanet python=3.10 -y
conda activate apexplanet
pip install -r requirements.txt
```

### 3. Run Data Ingestion & Cleaning Pipeline
```bash
# Step 1: Ingest raw dataset
python scripts/download_data.py

# Step 2: Clean data and export to SQLite database
python scripts/data_cleaning.py

# Step 3: Generate visual artifacts and reports
python scripts/generate_eda_visualizations.py
```

### 4. Launch Jupyter Notebook
```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

### 5. View Interactive Dashboard
Open `dashboards/index.html` in any web browser to explore interactive Plotly KPI cards and charts:
```bash
open dashboards/index.html  # On macOS
# or double-click dashboards/index.html in file explorer
```

---

## 📊 Exploratory Data Analysis & Key Findings

### 1. The Discount vs. Profit Threshold
* **Finding:** When discounts exceed **20%**, average order profitability drops below zero.
* **Impact:** Furniture products (especially Tables and Bookcases) suffer the steepest losses when subjected to discounts $>20\%$.

### 2. Category Performance
* **Technology:** Highest revenue driver with robust profit margins ($>30\%$).
* **Office Supplies:** Consistent, high-volume, low-volatility revenue.
* **Furniture:** High revenue but heavily penalized by shipping duration and aggressive promotional discounts.

### 3. Customer Segments
* **Consumer:** 50.8% of total revenue.
* **Corporate:** 30.2% of total revenue with higher stability.
* **Home Office:** 19.0% of total revenue.

### 4. Seasonality
* **Q4 Peak:** Peak sales occur between October and December each year due to holiday retail patterns and corporate budget cycles.

---

## 📈 Visual Artifacts Preview
Generated figures saved inside `reports/`:
- `univariate_distributions.png`
- `category_sales_profit.png`
- `subcategory_profit_loss.png`
- `segment_and_regional_breakdown.png`
- `discount_vs_profit_impact.png`
- `monthly_sales_trend.png`
- `correlation_heatmap.png`

---

## 👤 Author
**Rohit Kumar Verma**  
GitHub: [@rkv22](https://github.com/rkv22)

# 🪐 APEXPLANET DATA ANALYTICS

Welcome to the **ApexPlanet Data Analytics** repository. This repository organizes all tasks, datasets, exploratory analyses, scripts, reports, and dashboards.

---

## 📁 Repository Structure

```text
APEXPLANET-DATA-ANALYTICS-/
├── .gitignore
├── requirements.txt
├── README.md                          # Main project index
└── task-1/                            # TASK 1: Foundational Setup & EDA
    ├── data/
    │   ├── raw/
    │   │   └── superstore_sales.csv
    │   └── processed/
    │       ├── superstore_sales_cleaned.csv
    │       └── superstore.db          # SQLite Database (via SQLAlchemy)
    ├── notebooks/
    │   └── 01_exploratory_data_analysis.ipynb
    ├── scripts/
    │   ├── download_data.py
    │   ├── data_cleaning.py
    │   ├── create_notebook.py
    │   └── generate_eda_visualizations.py
    ├── reports/
    │   ├── EDA_Executive_Summary.md
    │   └── *.png                      # 7 analytical charts
    ├── dashboards/
    │   └── index.html                 # Interactive Plotly dashboard
    ├── requirements.txt
    └── README.md                      # Task 1 detailed documentation
```

---

## 📌 Tasks Overview

| Task | Title | Timeline | Status | Link |
| :---: | :--- | :---: | :---: | :--- |
| **01** | **Foundational Setup & Exploratory Data Analysis (EDA)** | 6 Days | ✅ Completed | [Explore Task 1](./task-1/README.md) |
| **02** | *(Upcoming Task)* | - | ⏳ Pending | - |

---

## 🚀 Quickstart for Task 1

To set up the environment and explore Task 1:

```bash
# Clone the repository
git clone https://github.com/rkv22/APEXPLANET-DATA-ANALYTICS-.git
cd APEXPLANET-DATA-ANALYTICS-

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run data pipeline and visualizations
cd task-1
python scripts/download_data.py
python scripts/data_cleaning.py
python scripts/generate_eda_visualizations.py

# Launch Jupyter Notebook
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

For complete details on findings, charts, and methodology, see [Task 1 README](./task-1/README.md).

---

## 👤 Author
**Rohit Kumar Verma**  
GitHub: [@rkv22](https://github.com/rkv22)

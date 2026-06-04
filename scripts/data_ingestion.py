"""
data_ingestion.py
Bluestock Fintech- Mutual Fund Analytics Capstone
Day 1: Load and inspect all 10 raw datasets
"""
import pandas as pd
from  pathlib import Path



RAW= Path("data/raw")

DATASETS = {
    "fund_master":           "01_fund_master.csv",
    "nav_history":           "02_nav_history.csv",
    "aum_by_fund_house":     "03_aum_by_fund_house.csv",
    "monthly_sip_inflows":   "04_monthly_sip_inflows.csv",
    "category_inflows":      "05_category_inflows.csv",
    "industry_folio_count":  "06_industry_folio_count.csv",
    "scheme_performance":    "07_scheme_performance.csv",
    "investor_transactions": "08_investor_transactions.csv",
    "portfolio_holdings":    "09_portfolio_holdings.csv",
    "benchmark_indices":     "10_benchmark_indices.csv",
}

dataframes={}

print("=" * 60)
print("BLUESTOCK FINTECH-DATA INGESTION REPORT")
print("=" * 60)

for name,filename in DATASETS.items():
    filepath=RAW/filename
    df=pd.read_csv(filepath)
    dataframes[name]=df

    print(f"\n{'-'*60}")
    print(f"DATASET:{name}")
    print(f"FILE :{filename}")
    print(f"SHAPE : {df.shape[0]} rows {df.shape[1]} columns")
    print(f"COLUMNS: {list(df.columns)}")
    print(f"\nMISSING VALUES:")
    missing=df.isnull().sum()
    missing=missing[missing>0]
    if len(missing)==0:
        print("  None - clean!")
    else:
        for col, count in missing.items():
            pct=(count/len(df)) * 100
            print(f"{col}:{count} missing ({pct:.1f}%)")

    print(f"\nFIRST ROW PREVIEW:")
    print(df.head(1).to_string())

print("\n" + "=" *60)
print("ALL DATASETS LOADED SUCCESSFULLY")
print("="*60)
"""
data_cleaning.py
Bluestock Fintech — Mutual Fund Analytics Capstone
Day 2: Clean all 10 datasets and save to data/processed/
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RAW  = BASE / "data" / "raw"
PROC = BASE / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("BLUESTOCK FINTECH — DATA CLEANING PIPELINE")
print("=" * 60)

# ── DATASET 1: NAV History ─────────────────────────────────
print("\n[1/10] Cleaning NAV History...")
nav = pd.read_csv(RAW / "02_nav_history.csv")

# Step 1: Parse date column to proper datetime
nav["date"] = pd.to_datetime(nav["date"])

# Step 2: Sort by fund code and date
nav = nav.sort_values(["amfi_code", "date"]).reset_index(drop=True)

# Step 3: Remove rows where NAV is 0 or negative (impossible values)
invalid_nav = nav[nav["nav"] <= 0]
print(f"  Removed {len(invalid_nav)} rows with NAV <= 0")
nav = nav[nav["nav"] > 0]

# Step 4: Forward-fill missing NAV values within each fund
# Why: If market is closed on Monday (holiday), we carry forward Friday's NAV
nav["nav"] = nav.groupby("amfi_code")["nav"].ffill()

# Step 5: Remove duplicates (same fund, same date)
before = len(nav)
nav = nav.drop_duplicates(subset=["amfi_code", "date"])
print(f"  Removed {before - len(nav)} duplicate rows")

# Step 6: Calculate daily return for each fund
# Formula: (today's NAV - yesterday's NAV) / yesterday's NAV * 100
nav["daily_return_pct"] = (
    nav.groupby("amfi_code")["nav"]
    .pct_change() * 100
).round(4)

print(f"  Final shape: {nav.shape[0]} rows x {nav.shape[1]} cols")
print(f"  Date range: {nav['date'].min().date()} to {nav['date'].max().date()}")
nav.to_csv(PROC / "clean_nav_history.csv", index=False)
print("  Saved: clean_nav_history.csv")


# ── DATASET 2: Fund Master ─────────────────────────────────
print("\n[2/10] Cleaning Fund Master...")
fm = pd.read_csv(RAW / "01_fund_master.csv")

# Check expense ratio range (should be 0.1% to 2.5%)
invalid_exp = fm[(fm["expense_ratio_pct"] < 0.1) | (fm["expense_ratio_pct"] > 2.5)]
print(f"  Funds with unusual expense ratio: {len(invalid_exp)}")

# Standardize text columns — strip whitespace, consistent casing
fm["fund_house"]    = fm["fund_house"].str.strip()
fm["scheme_name"]   = fm["scheme_name"].str.strip()
fm["category"]      = fm["category"].str.strip().str.title()
fm["risk_category"] = fm["risk_category"].str.strip().str.title()

print(f"  Final shape: {fm.shape[0]} rows x {fm.shape[1]} cols")
fm.to_csv(PROC / "clean_fund_master.csv", index=False)
print("  Saved: clean_fund_master.csv")


# ── DATASET 3: AUM by Fund House ───────────────────────────
print("\n[3/10] Cleaning AUM by Fund House...")
aum = pd.read_csv(RAW / "03_aum_by_fund_house.csv")

aum["date"] = pd.to_datetime(aum["date"])
aum["fund_house"] = aum["fund_house"].str.strip()

# AUM should never be negative
invalid_aum = aum[aum["aum_crore"] < 0]
print(f"  Negative AUM rows: {len(invalid_aum)}")

print(f"  Final shape: {aum.shape[0]} rows x {aum.shape[1]} cols")
aum.to_csv(PROC / "clean_aum_by_fund_house.csv", index=False)
print("  Saved: clean_aum_by_fund_house.csv")


# ── DATASET 4: Monthly SIP Inflows ────────────────────────
print("\n[4/10] Cleaning Monthly SIP Inflows...")
sip = pd.read_csv(RAW / "04_monthly_sip_inflows.csv")

sip["month"] = pd.to_datetime(sip["month"])
sip = sip.sort_values("month").reset_index(drop=True)

# SIP inflow should be positive
print(f"  Months covered: {len(sip)}")
print(f"  SIP range: {sip['sip_inflow_crore'].min()} to {sip['sip_inflow_crore'].max()} crore")

sip.to_csv(PROC / "clean_monthly_sip_inflows.csv", index=False)
print("  Saved: clean_monthly_sip_inflows.csv")


# ── DATASET 5: Category Inflows ───────────────────────────
print("\n[5/10] Cleaning Category Inflows...")
cat = pd.read_csv(RAW / "05_category_inflows.csv")

cat["month"] = pd.to_datetime(cat["month"])
cat["category"] = cat["category"].str.strip().str.title()

cat.to_csv(PROC / "clean_category_inflows.csv", index=False)
print(f"  Final shape: {cat.shape[0]} rows x {cat.shape[1]} cols")
print("  Saved: clean_category_inflows.csv")


# ── DATASET 6: Industry Folio Count ───────────────────────
print("\n[6/10] Cleaning Industry Folio Count...")
folio = pd.read_csv(RAW / "06_industry_folio_count.csv")

folio["month"] = pd.to_datetime(folio["month"])
folio = folio.sort_values("month").reset_index(drop=True)

folio.to_csv(PROC / "clean_industry_folio_count.csv", index=False)
print(f"  Final shape: {folio.shape[0]} rows x {folio.shape[1]} cols")
print("  Saved: clean_industry_folio_count.csv")


# ── DATASET 7: Scheme Performance ─────────────────────────
print("\n[7/10] Cleaning Scheme Performance...")
perf = pd.read_csv(RAW / "07_scheme_performance.csv")

# Flag negative Sharpe ratios — valid but worth noting
negative_sharpe = perf[perf["sharpe_ratio"] < 0]
print(f"  Funds with negative Sharpe ratio: {len(negative_sharpe)}")

# Validate return columns are numeric
for col in ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct"]:
    if col in perf.columns:
        perf[col] = pd.to_numeric(perf[col], errors="coerce")

perf.to_csv(PROC / "clean_scheme_performance.csv", index=False)
print(f"  Final shape: {perf.shape[0]} rows x {perf.shape[1]} cols")
print("  Saved: clean_scheme_performance.csv")


# ── DATASET 8: Investor Transactions ──────────────────────
print("\n[8/10] Cleaning Investor Transactions...")
tx = pd.read_csv(RAW / "08_investor_transactions.csv")

# Standardize transaction types
tx["transaction_type"] = tx["transaction_type"].str.strip().str.title()
print(f"  Transaction types: {tx['transaction_type'].unique()}")

# Remove transactions with amount <= 0
invalid_tx = tx[tx["amount_inr"] <= 0]
print(f"  Removed {len(invalid_tx)} transactions with amount <= 0")
tx = tx[tx["amount_inr"] > 0]

# Parse dates
tx["transaction_date"] = pd.to_datetime(tx["transaction_date"])

# Standardize KYC status
tx["kyc_status"] = tx["kyc_status"].str.strip().str.title()
print(f"  KYC status values: {tx['kyc_status'].unique()}")

print(f"  Final shape: {tx.shape[0]} rows x {tx.shape[1]} cols")
tx.to_csv(PROC / "clean_investor_transactions.csv", index=False)
print("  Saved: clean_investor_transactions.csv")


# ── DATASET 9: Portfolio Holdings ─────────────────────────
print("\n[9/10] Cleaning Portfolio Holdings...")
port = pd.read_csv(RAW / "09_portfolio_holdings.csv")

port["sector"] = port["sector"].str.strip().str.title()

# Weight percentages should sum to ~100% per fund
weight_check = port.groupby("amfi_code")["weight_pct"].sum()
print(f"  Weight sum range per fund: {weight_check.min():.1f}% to {weight_check.max():.1f}%")

port.to_csv(PROC / "clean_portfolio_holdings.csv", index=False)
print(f"  Final shape: {port.shape[0]} rows x {port.shape[1]} cols")
print("  Saved: clean_portfolio_holdings.csv")


# ── DATASET 10: Benchmark Indices ─────────────────────────
print("\n[10/10] Cleaning Benchmark Indices...")
bench = pd.read_csv(RAW / "10_benchmark_indices.csv")

bench["date"] = pd.to_datetime(bench["date"])
bench = bench.sort_values("date").reset_index(drop=True)

# Forward fill missing index values (same reason as NAV — market holidays)
bench = bench.ffill()
print(f"  Final shape: {bench.shape[0]} rows x {bench.shape[1]} cols")
bench.to_csv(PROC / "clean_benchmark_indices.csv", index=False)
print("  Saved: clean_benchmark_indices.csv")


print("\n" + "=" * 60)
print("ALL 10 DATASETS CLEANED SUCCESSFULLY")
print(f"Saved to: {PROC}")
print("=" * 60)
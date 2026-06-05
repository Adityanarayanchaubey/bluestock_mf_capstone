
"""
load_database.py
Bluestock Fintech — Mutual Fund Analytics Capstone
Day 2: Load all cleaned data into SQLite database
"""

import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PROC = BASE / "data" / "processed"
DB   = BASE / "data" / "db" / "bluestock_mf.db"

# Create database engine
engine = create_engine(f"sqlite:///{DB}")

print("=" * 60)
print("BLUESTOCK FINTECH — DATABASE LOADING PIPELINE")
print("=" * 60)

# ── Run schema first ───────────────────────────────────────
schema_path = BASE / "sql" / "schema.sql"
with engine.connect() as conn:
    with open(schema_path, "r") as f:
        schema_sql = f.read()
    # Execute each statement separately
    for statement in schema_sql.split(";"):
        statement = statement.strip()
        if statement:
            conn.execute(text(statement))
    conn.commit()
print("\nSchema created successfully")

# ── Load dim_fund ──────────────────────────────────────────
print("\n[1/6] Loading dim_fund...")
fm = pd.read_csv(PROC / "clean_fund_master.csv")
fm.to_sql("dim_fund", engine, if_exists="replace", index=False)
print(f"  Loaded {len(fm)} funds")

# ── Load fact_nav ──────────────────────────────────────────
print("\n[2/6] Loading fact_nav...")
nav = pd.read_csv(PROC / "clean_nav_history.csv")
nav = nav.rename(columns={"date": "nav_date"})
nav.to_sql("fact_nav", engine, if_exists="replace", index=False)
print(f"  Loaded {len(nav)} NAV records")

# ── Load fact_transactions ─────────────────────────────────
print("\n[3/6] Loading fact_transactions...")
tx = pd.read_csv(PROC / "clean_investor_transactions.csv")
tx.to_sql("fact_transactions", engine, if_exists="replace", index=False)
print(f"  Loaded {len(tx)} transactions")

# ── Load fact_performance ──────────────────────────────────
print("\n[4/6] Loading fact_performance...")
perf = pd.read_csv(PROC / "clean_scheme_performance.csv")
perf.to_sql("fact_performance", engine, if_exists="replace", index=False)
print(f"  Loaded {len(perf)} performance records")

# ── Load fact_aum ──────────────────────────────────────────
print("\n[5/6] Loading fact_aum...")
aum = pd.read_csv(PROC / "clean_aum_by_fund_house.csv")
aum.to_sql("fact_aum", engine, if_exists="replace", index=False)
print(f"  Loaded {len(aum)} AUM records")

# ── Load fact_sip_industry ─────────────────────────────────
print("\n[6/6] Loading fact_sip_industry...")
sip = pd.read_csv(PROC / "clean_monthly_sip_inflows.csv")
sip.to_sql("fact_sip_industry", engine, if_exists="replace", index=False)
print(f"  Loaded {len(sip)} SIP monthly records")

# ── Verify everything loaded ───────────────────────────────
print("\n" + "=" * 60)
print("DATABASE VERIFICATION")
print("=" * 60)

tables = ["dim_fund", "fact_nav", "fact_transactions",
          "fact_performance", "fact_aum", "fact_sip_industry"]

with engine.connect() as conn:
    for table in tables:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
        count = result.fetchone()[0]
        print(f"  {table}: {count} rows")

print("\nDATABASE READY: bluestock_mf.db")
print(f"Location: {DB}")
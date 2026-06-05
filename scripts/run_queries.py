"""
run_queries.py
Bluestock Fintech — Mutual Fund Analytics Capstone
Day 2: Run all 10 analytical SQL queries and display results
"""

import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

BASE   = Path(__file__).resolve().parent.parent
DB     = BASE / "data" / "db" / "bluestock_mf.db"
engine = create_engine(f"sqlite:///{DB}")

QUERIES = {
    "Q1 — Top 5 Fund Houses by AUM": """
        SELECT fund_house, ROUND(SUM(aum_crore),2) AS total_aum_crore
        FROM fact_aum GROUP BY fund_house
        ORDER BY total_aum_crore DESC LIMIT 5
    """,
    "Q2 — Avg NAV Last 6 Months (first 5 rows)": """
        SELECT amfi_code, SUBSTR(nav_date,1,7) AS month,
               ROUND(AVG(nav),2) AS avg_nav
        FROM fact_nav
        WHERE nav_date >= DATE('now','-6 months')
        GROUP BY amfi_code, SUBSTR(nav_date,1,7)
        ORDER BY amfi_code, month LIMIT 5
    """,
    "Q3 — SIP Inflow Year-over-Year": """
        SELECT SUBSTR(month,1,4) AS year,
               ROUND(SUM(sip_inflow_crore),2) AS total_sip_inflow
        FROM fact_sip_industry
        GROUP BY SUBSTR(month,1,4) ORDER BY year
    """,
    "Q4 — Top 5 States by Investment": """
        SELECT state, COUNT(*) AS num_transactions,
               ROUND(SUM(amount_inr),2) AS total_invested
        FROM fact_transactions
        GROUP BY state ORDER BY total_invested DESC LIMIT 5
    """,
    "Q5 — Funds with Expense Ratio < 1%": """
        SELECT scheme_name, fund_house, expense_ratio_pct
        FROM dim_fund WHERE expense_ratio_pct < 1.0
        ORDER BY expense_ratio_pct LIMIT 5
    """,
    "Q6 — Top 5 Funds by 3-Year CAGR": """
        SELECT f.scheme_name, f.fund_house,
               p.return_3yr_pct, p.sharpe_ratio
        FROM fact_performance p
        JOIN dim_fund f ON p.amfi_code = f.amfi_code
        ORDER BY p.return_3yr_pct DESC LIMIT 5
    """,
    "Q7 — Transaction Split by Type": """
        SELECT transaction_type, COUNT(*) AS count,
               ROUND(SUM(amount_inr),2) AS total_amount
        FROM fact_transactions
        GROUP BY transaction_type ORDER BY total_amount DESC
    """,
    "Q8 — Avg SIP Amount by Age Group": """
        SELECT age_group, COUNT(*) AS num_sips,
               ROUND(AVG(amount_inr),2) AS avg_sip_amount
        FROM fact_transactions WHERE transaction_type = 'Sip'
        GROUP BY age_group ORDER BY avg_sip_amount DESC
    """,
    "Q9 — Fund Alpha vs Benchmark": """
        SELECT f.scheme_name, p.return_3yr_pct,
               p.alpha,
               CASE WHEN p.alpha > 0 THEN 'Outperforming'
                    ELSE 'Underperforming' END AS vs_benchmark
        FROM fact_performance p
        JOIN dim_fund f ON p.amfi_code = f.amfi_code
        ORDER BY p.alpha DESC LIMIT 5
    """,
    "Q10 — T30 vs B30 City Investment": """
        SELECT city_tier, COUNT(*) AS transactions,
               ROUND(SUM(amount_inr),2) AS total_invested
        FROM fact_transactions
        GROUP BY city_tier ORDER BY total_invested DESC
    """,
}

print("=" * 60)
print("BLUESTOCK FINTECH — SQL ANALYTICAL QUERIES")
print("=" * 60)

for title, query in QUERIES.items():
    print(f"\n{'─'*60}")
    print(f"{title}")
    print("─" * 60)
    df = pd.read_sql(query, engine)
    print(df.to_string(index=False))

print("\n" + "=" * 60)
print("ALL 10 QUERIES COMPLETE")
print("=" * 60)
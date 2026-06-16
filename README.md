# Bluestock Fintech — Mutual Fund Analytics Platform

## Project Overview
End-to-end data analytics platform analyzing 40 mutual fund schemes across 
10 datasets with 87,000+ rows of financial data spanning 4.5 years (2022–2026).

Built as part of the Data Analyst Internship Capstone at Bluestock Fintech Pvt. Ltd.

## Key Findings
- SBI Mutual Fund is India's largest AMC with highest AUM
- ICICI Prudential Midcap Fund ranked #1 with composite score of 100
- SIP inflows grew consistently from ₹11,438 Cr to ₹31,002 Cr (all-time high)
- Total mutual fund folios doubled from 13.26 Cr to 26.12 Cr in 4 years
- 97.8% of active SIP investors show at-risk continuation patterns
- All top 5 funds outperformed Nifty 50 benchmark over 4-year period

## Tech Stack
- Python 3.14 | Pandas | NumPy | Matplotlib | Seaborn | SciPy
- SQLite | SQLAlchemy
- Power BI Desktop
- Git | GitHub

## Project Structure

bluestock_mf_capstone/

├── data/

│   ├── raw/          ← Original CSV datasets

│   ├── processed/    ← Cleaned datasets

│   └── db/           ← SQLite database

├── notebooks/        ← Jupyter analysis notebooks

├── scripts/          ← Python ETL scripts

├── sql/              ← Schema and queries

├── dashboard/        ← Power BI dashboard

└── reports/          ← Charts and final report

## How to Run
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run ETL pipeline: `python scripts/data_cleaning.py`
4. Load database: `python scripts/load_database.py`
5. Open notebooks in order: 01 → 02 → 03 → 04 → 05
6. Open dashboard: `dashboard/bluestock_mf_dashboard.pbix`

## Datasets
| Dataset | Rows | Description |
|---------|------|-------------|
| Fund Master | 40 | 40 mutual fund schemes |
| NAV History | 46,000 | Daily NAV 2022-2026 |
| Investor Transactions | 32,000+ | SIP/Lumpsum/Redemption |
| AUM by Fund House | 90 | Quarterly AUM data |
| Monthly SIP Inflows | 48 | Industry SIP statistics |
| Benchmark Indices | 8,050 | 7 market indices |

## Key Metrics Computed
- CAGR | Sharpe Ratio | Sortino Ratio
- Alpha | Beta | Max Drawdown
- Value at Risk (VaR 95%) | Conditional VaR
- Rolling 90-day Sharpe | Fund Composite Scorecard
- Investor Cohort Analysis | SIP Continuity Score
- Sector HHI Concentration Index

## Author
Data Analyst Intern — Bluestock Fintech Pvt. Ltd.
Cohort 2025 | June 2026
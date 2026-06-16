# Bluestock Fintech — Mutual Fund Analytics Platform
## Final Project Report | June 2026

---

## 1. Executive Summary
This project builds a complete Mutual Fund Analytics Platform for Bluestock 
Fintech analyzing 40 fund schemes across 10 datasets. Key findings include 
ICICI Prudential Midcap Fund as the top performer with 31.48% CAGR, SBI 
Mutual Fund as India's largest AMC, and consistent industry growth with SIP 
inflows reaching an all-time high of ₹31,002 crore in December 2025.

---

## 2. Problem Statement
Indian mutual fund investors lack unified analytics platforms for data-driven 
fund selection. This project consolidates fragmented data into a single 
database, computes risk-adjusted metrics, and presents insights via an 
interactive Power BI dashboard.

---

## 3. Data Sources
- AMFI India: NAV history, AUM data, SIP inflows
- mfapi.in: Live NAV API
- NSE/BSE: Benchmark index prices
- 10 datasets | 87,000+ rows | 4.5 years coverage

---

## 4. ETL Pipeline
- Extracted 10 raw CSV datasets
- Cleaned: forward-filled missing NAV values, removed duplicates,
  standardized transaction types, validated expense ratios
- Loaded into SQLite database with 5-table star schema
- Created indexes on amfi_code and date for fast querying

---

## 5. Key EDA Findings
1. SIP inflows grew 170% from ₹11,438 Cr to ₹31,002 Cr (2022-2025)
2. Total folios doubled from 13.26 Cr to 26.12 Cr in 4 years
3. 26-35 age group is the largest investor segment
4. Equity funds dominate with highest folio count
5. Most funds show high correlation — limited diversification benefit
6. T30 cities invest 54% vs B30 cities 46% — B30 gap closing
7. SBI Mutual Fund leads AUM across all years
8. All fund NAVs show consistent upward trend 2022-2026

---

## 6. Performance Analytics
| Metric | Top Performer | Value |
|--------|--------------|-------|
| Highest CAGR | ICICI Pru Midcap | 31.48% |
| Best Sharpe Ratio | Mirae Large Cap | Above 1 |
| Highest Alpha | SBI Small Cap | Positive |
| Worst Drawdown | SBI Small Cap | -52.57% |
| Composite Rank 1 | ICICI Pru Midcap | Score 100 |

---

## 7. Risk Analysis
- SBI Small Cap Fund carries highest VaR — largest single-day loss potential
- Rolling Sharpe shows all funds experienced negative periods during corrections
- 97.8% of SIP investors show at-risk continuation patterns (gaps > 35 days)
- High correlation between funds limits true portfolio diversification

---

## 8. Dashboard Summary
Built 4-page interactive Power BI dashboard:
- Page 1: Industry Overview — AUM, SIP, Folio KPIs
- Page 2: Fund Performance — Scorecard, Risk-Return scatter
- Page 3: Investor Analytics — Demographics, geography
- Page 4: SIP & Market Trends — Benchmark comparison

---

## 9. Recommendations
1. Bluestock should promote ICICI Pru Midcap and Mirae Large Cap 
   as top picks for aggressive and moderate investors respectively
2. Launch SIP re-engagement campaign targeting 1,332 at-risk investors
3. Focus marketing on 26-35 age group — largest and most active segment
4. Expand B30 city presence — gap with T30 is closing, opportunity exists
5. Offer low-correlation fund combinations to improve investor diversification

---

## 10. Limitations
- Live NAV fetch from mfapi.in was unavailable due to API restrictions
- Investor transaction data is simulated though based on real distributions
- Dashboard uses static CSV imports rather than live database connection

---

## 11. Conclusion
This platform successfully demonstrates end-to-end data analytics capability
in the fintech domain — from raw data ingestion through ETL, SQL analysis,
statistical metrics, and interactive visualization.

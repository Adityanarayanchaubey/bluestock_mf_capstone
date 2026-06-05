-- ============================================
-- BLUESTOCK FINTECH — 10 ANALYTICAL QUERIES
-- ============================================

-- Q1: Top 5 fund houses by total AUM
-- Business question: Who are the biggest players in the industry?
SELECT 
    fund_house,
    ROUND(SUM(aum_crore), 2) AS total_aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum_crore DESC
LIMIT 5;

-- Q2: Average NAV per month for each fund (last 6 months)
-- Business question: How has NAV trended recently?
SELECT
    amfi_code,
    SUBSTR(nav_date, 1, 7)      AS month,
    ROUND(AVG(nav), 2)          AS avg_nav,
    ROUND(MIN(nav), 2)          AS min_nav,
    ROUND(MAX(nav), 2)          AS max_nav
FROM fact_nav
WHERE nav_date >= DATE('now', '-6 months')
GROUP BY amfi_code, SUBSTR(nav_date, 1, 7)
ORDER BY amfi_code, month;

-- Q3: SIP inflow year-over-year growth
-- Business question: Is the SIP culture growing in India?
SELECT
    SUBSTR(month, 1, 4)         AS year,
    ROUND(SUM(sip_inflow_crore), 2) AS total_sip_inflow,
    ROUND(AVG(sip_inflow_crore), 2) AS avg_monthly_sip
FROM fact_sip_industry
GROUP BY SUBSTR(month, 1, 4)
ORDER BY year;

-- Q4: Total transaction amount by state
-- Business question: Which states are investing the most?
SELECT
    state,
    COUNT(*)                        AS num_transactions,
    ROUND(SUM(amount_inr), 2)       AS total_invested,
    ROUND(AVG(amount_inr), 2)       AS avg_transaction
FROM fact_transactions
GROUP BY state
ORDER BY total_invested DESC;

-- Q5: Funds with expense ratio below 1%
-- Business question: Which are the most cost-efficient funds?
SELECT
    scheme_name,
    fund_house,
    category,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- Q6: Top 10 performing funds by 3-year CAGR
-- Business question: Which funds have given best long-term returns?
SELECT
    f.scheme_name,
    f.fund_house,
    f.category,
    p.return_3yr_pct,
    p.sharpe_ratio,
    p.alpha
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.return_3yr_pct DESC
LIMIT 10;

-- Q7: Transaction split by type (SIP vs Lumpsum vs Redemption)
-- Business question: How are investors putting money in and taking it out?
SELECT
    transaction_type,
    COUNT(*)                        AS num_transactions,
    ROUND(SUM(amount_inr), 2)       AS total_amount,
    ROUND(AVG(amount_inr), 2)       AS avg_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;

-- Q8: Average SIP amount by age group
-- Business question: Which age group invests the most via SIP?
SELECT
    age_group,
    COUNT(*)                        AS num_sips,
    ROUND(AVG(amount_inr), 2)       AS avg_sip_amount,
    ROUND(SUM(amount_inr), 2)       AS total_invested
FROM fact_transactions
WHERE transaction_type = 'Sip'
GROUP BY age_group
ORDER BY avg_sip_amount DESC;

-- Q9: Fund performance vs benchmark (Alpha analysis)
-- Business question: Which fund managers are actually adding value?
SELECT
    f.scheme_name,
    f.fund_house,
    p.return_3yr_pct,
    p.benchmark_3yr_pct,
    p.alpha,
    p.beta,
    p.sharpe_ratio,
    CASE
        WHEN p.alpha > 0 THEN 'Outperforming'
        ELSE 'Underperforming'
    END AS vs_benchmark
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.alpha DESC;

-- Q10: T30 vs B30 city investment comparison
-- Business question: Are beyond-top-30 cities investing more now?
SELECT
    city_tier,
    COUNT(*)                        AS num_transactions,
    ROUND(SUM(amount_inr), 2)       AS total_invested,
    ROUND(AVG(amount_inr), 2)       AS avg_transaction,
    COUNT(DISTINCT state)           AS states_covered
FROM fact_transactions
GROUP BY city_tier
ORDER BY total_invested DESC;
-- ============================================
-- BLUESTOCK FINTECH — MUTUAL FUND DATABASE
-- Star Schema Design
-- ============================================

-- DIMENSION TABLE 1: Fund Master
-- Contains static information about each fund

CREATE TABLE IF NOT EXISTS dim_fund(
    amfi_code TEXT PRIMARY KEY,
    fund_house TEXT NOT NULL,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    fund_manager TEXT,
    risk_category TEXT,
    launch_date TEXT
);

--FACT TABLE 1: NAV History
--Daily NAV for every fund - the largest table
CREATE TABLE IF NOT EXISTS fact_nav(
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code  TEXT NOT NULL,
    nav_date  TEXT NOT NULL,
    nav       REAL NOT NULL,
    daily_return_pct REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

--FACT TABLE 2: INVESTOR TRANSACTIONS
CREATE TABLE IF NOT EXISTS fact_transactions(
    tx_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT,
    amfi_code TEXT,
    transaction_date TEXT,
    transaction_type TEXT,
    amount_inr TEXT,
    state  TEXT,
    city  TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_incom_lakh  REAL,
    payment_mode TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)

);

--FACT TABLE 3: SCHEME PERFORMANCE METRICS
CREATE TABLE IF NOT EXISTS fact_performance(
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code  TEXT,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,
    morningstar_rating INTEGER,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

--FACT TABLE 4: AUM BY FUND HOUSE
CREATE TABLE IF NOT EXISTS fact_aum(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house TEXT,
    date TEXT,
    aum_crore REAL,
    num_schemes INTEGER
);

--FACT TABLE 5: MONTHLY SIP INDUSTRY DATA
CREATE TABLE IF NOT EXISTS fact_sip_industry(
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT,
    sip_inflow_crore REAL,
    active_sip_accounts_crore REAL,
    new_sip_accounts_lakh REAL,
    sip_aum_lakh_crore REAL,
    yoy_growth_pct REAL
);

--INDEXES for fast querying
CREATE INDEX IF NOT EXISTS idx_nav_amfi ON fact_nav(amfi_code);
CREATE INDEX IF NOT EXISTS idx_nav_date ON fact_nav(nav_date);
CREATE INDEX IF NOT EXISTS idx_tx_amfi ON fact_transactions(amfi_code);
CREATE INDEX IF NOT EXISTS idx_tx_date ON fact_transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_tx_state ON fact_transactions(state);
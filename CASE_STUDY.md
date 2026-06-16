# Case Study: Fintech Fraud and Risk Monitoring

## Executive summary

I built a reproducible fraud-monitoring analytics project for a fintech risk team.
The pipeline generates realistic transaction data, validates it, loads it into SQLite,
runs SQL risk analysis, and exports dashboard-ready tables and charts.

The generated dataset contains **65,000 transactions**, **GBP 2.96m** in transaction
volume, **1,338 fraud transactions**, a **2.06% fraud rate**, and **GBP 73.8k** in
fraud loss.

## Key findings

### 1. Card-not-present is the highest-risk channel

Card-not-present transactions have the highest fraud rate at **2.84%**, compared with
**1.80%** for mobile wallet and **1.47%** for card-present transactions.

This is the first operational dashboard slice I would show a risk team because it
separates customer behaviour that needs stronger monitoring from lower-risk everyday
spend.

### 2. Crypto, electronics, and travel drive the risk story

Crypto has the highest fraud rate among merchant categories at **5.34%**. Electronics
and travel also create material fraud losses because their average transaction values
are higher.

The practical recommendation is not to block these categories, but to monitor them
with tighter thresholds when transactions are high-value, cross-border, or unusually
high-velocity.

### 3. A merchant investigation queue is more useful than a static dashboard

The SQL output ranks merchants by fraud loss and fraud rate. The highest-loss merchant
in the generated data is `M00616`, a crypto merchant with **72 transactions**, **7
fraud transactions**, a **9.72% fraud rate**, and **GBP 1.3k** fraud loss.

That turns the analysis into an operational queue: risk teams can decide who to
investigate first instead of scanning a broad report.

### 4. Data quality is part of the risk control

The build includes checks for duplicate transaction IDs, missing required fields,
non-positive amounts, and invalid fraud labels. All checks pass in the generated
dataset.

For a regulated environment, this matters because a fraud dashboard is only useful if
the underlying monitoring data is trusted and auditable.

## Skills demonstrated

- Python data generation, cleaning, validation, and feature engineering.
- SQL grouped analysis, window functions, and investigation-ranking queries.
- SQLite warehouse build for reproducible local analytics.
- Dashboard-ready CSV exports for Power BI, Tableau, or Looker.
- Risk-domain metrics: fraud rate, fraud loss, alert rate, velocity flags, merchant
  risk, and channel risk.
- Clear stakeholder communication for a fintech risk audience.

## Hiring-market fit

This project is designed for London data roles that mention:

- SQL and Python/R.
- Power BI, Tableau, or Looker.
- dbt-style modelling, data-quality checks, and cloud warehouse thinking.
- Fraud, financial crime, risk, compliance, or regulated reporting.
- Stakeholder-facing insight and operational dashboards.


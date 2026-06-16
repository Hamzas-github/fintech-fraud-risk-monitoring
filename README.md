# Fintech Fraud and Risk Monitoring

An end-to-end analytics project built for London fintech data roles. It creates a
realistic card-transaction dataset, validates it, loads it into SQLite, runs SQL risk
analysis, and exports dashboard-ready charts and summary tables.

## Why this project

Current London data roles are asking for more than basic dashboards. The strongest
signals from live postings are:

- SQL and Python for analysis beyond spreadsheets.
- BI storytelling in Power BI, Tableau, or Looker.
- dbt-style data modelling, data-quality checks, and documented pipelines.
- Fintech/risk context: fraud, financial crime, transaction monitoring, auditability,
  and regulated reporting.

This project targets that intersection.

## Business question

How can a fintech risk team identify the customer, merchant, channel, and timing
patterns most associated with fraudulent transactions, and turn those signals into an
operational monitoring dashboard?

## What the pipeline builds

```text
synthetic raw transactions
  -> Python validation and feature engineering
  -> SQLite analytics database
  -> SQL risk queries
  -> dashboard-ready CSV outputs
  -> charts for portfolio case study
```

## Project structure

```text
fintech-fraud-risk-monitoring/
  README.md
  requirements.txt
  scripts/
    build_project.py
  sql/
    risk_analysis_queries.sql
  data/
    raw/                 generated locally
    processed/           generated locally
  database/              generated locally
  outputs/               generated charts and CSVs
```

## How to run

```powershell
cd "C:\Users\hamza\OneDrive\Documents\Portfolio 2\fintech-fraud-risk-monitoring"
python scripts\build_project.py
```

The script creates all generated data, database tables, outputs, and charts from
scratch.

## Outputs

After running the project:

- `data/raw/transactions_raw.csv`
- `data/processed/transactions_clean.csv`
- `database/fintech_fraud.db`
- `outputs/summary_metrics.csv`
- `outputs/monthly_fraud_trend.csv`
- `outputs/fraud_by_channel.csv`
- `outputs/fraud_by_merchant_category.csv`
- `outputs/high_risk_merchants.csv`
- `outputs/high_risk_customers.csv`
- `outputs/*.png` charts

## Current generated results

| Metric | Value |
|---|---:|
| Transactions | 65,000 |
| Transaction volume | GBP 2.96m |
| Fraud transactions | 1,338 |
| Fraud rate | 2.06% |
| Fraud loss | GBP 73.8k |
| Alert rate | 4.42% |

Read the narrative findings in [`CASE_STUDY.md`](CASE_STUDY.md).

## Key metrics generated

The synthetic dataset is designed to behave like a realistic monitoring dataset:

- Tens of thousands of transactions.
- Fraud concentrated in card-not-present, night-time, high-risk merchant categories,
  and high-velocity customer behaviour.
- A small group of merchants and customers responsible for a disproportionate share
  of fraud losses.
- Data-quality checks for duplicate IDs, missing values, invalid amounts, and invalid
  timestamps.

## Skills demonstrated

| Area | Evidence in the project |
|---|---|
| Python analytics | Data generation, cleaning, validation, feature engineering, charting |
| SQL | Window functions, grouped risk metrics, operational investigation queries |
| BI thinking | Dashboard-ready CSVs and charts by KPI, segment, and investigation priority |
| Data modelling | Clean transaction table plus risk-feature columns and metric outputs |
| Risk domain | Fraud rate, fraud loss, merchant risk, customer velocity, channel risk |
| Communication | README and outputs framed around a risk-team decision |

## Recommended dashboard pages

1. **Executive risk overview:** fraud rate, fraud loss, transaction volume, alert rate.
2. **Channel and timing:** fraud by card-present/card-not-present, hour, weekend.
3. **Merchant monitoring:** merchant categories and individual merchants ranked by
   fraud rate and loss.
4. **Customer investigation queue:** high-risk customers with velocity, loss, and
   fraud count.
5. **Data quality:** validation pass/fail checks and missingness.

## Next improvements

- Rebuild the SQL transformations in dbt with tests and docs.
- Add a Power BI dashboard using the generated CSV outputs.
- Add a simple risk-scoring model and compare it with rules-based flags.
- Package this as a separate GitHub repo, then add the finished case study to the
  portfolio site.

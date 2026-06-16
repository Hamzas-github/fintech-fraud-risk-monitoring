# Fintech Fraud and Risk Monitoring

I made this project because I am targeting data jobs in London, mainly data analyst,
risk analyst and fintech type roles.

This project is about fraud monitoring in card transactions. It makes fake but realistic
transaction data, cleans it with Python, puts it in SQLite, runs SQL queries, and makes
outputs that can be used in Power BI or any dashboard tool.

## Why I made this

When I was looking at London data jobs, many of them was asking for these skills:

- SQL
- Python
- Power BI or Looker
- data quality checks
- fraud or risk analytics
- clear explanation of findings

So I made this project to show these things in one place.

## Main question

The question I am answering is:

Which transactions, customers, channels and merchant types look more risky for fraud?

## What this project does

```text
make raw transaction data
clean it with Python
create risk features
load it into SQLite
run SQL analysis
export CSV files and charts
```

## Folder structure

```text
fintech-fraud-risk-monitoring/
  README.md
  CASE_STUDY.md
  requirements.txt
  scripts/
    build_project.py
  sql/
    risk_analysis_queries.sql
  outputs/
    generated CSV files and charts
```

## How to run it

```powershell
cd "C:\Users\hamza\OneDrive\Documents\fintech-fraud-risk-monitoring"
python scripts\build_project.py
```

The script will create the data, database, CSV outputs and charts again from start.

## Results from current run

| Metric | Value |
|---|---:|
| Transactions | 65,000 |
| Transaction volume | GBP 2.96m |
| Fraud transactions | 1,338 |
| Fraud rate | 2.06% |
| Fraud loss | GBP 73.8k |
| Alert rate | 4.42% |

## Main outputs

- `outputs/summary_metrics.csv`
- `outputs/monthly_fraud_trend.csv`
- `outputs/fraud_by_channel.csv`
- `outputs/fraud_by_merchant_category.csv`
- `outputs/high_risk_merchants.csv`
- `outputs/high_risk_customers.csv`
- chart images in `outputs/`

## What I found

Card not present transactions had the highest fraud rate.

Crypto, cash withdrawal, gaming, electronics and travel was the most risky merchant
groups in this data.

The project also makes a merchant investigation list, so a risk team can see which
merchant should be checked first.

## Skills shown

- Python data cleaning
- pandas feature engineering
- SQL analysis
- SQLite database
- fraud rate and fraud loss metrics
- data quality checks
- dashboard ready CSV outputs
- simple business explanation

## What I would add next

- make a Power BI dashboard from the outputs
- add dbt models and tests
- add a simple fraud scoring model
- compare rules based alerts with model based alerts


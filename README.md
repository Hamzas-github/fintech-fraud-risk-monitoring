# Fintech Fraud and Risk Monitoring

An end-to-end fraud analytics project built around 65,000 synthetic card transactions. The pipeline validates and cleans the data with Python, creates risk features, loads the result into SQLite, runs SQL investigations, and exports dashboard-ready metrics.

The central question is simple: which transactions, customers, channels, merchants, and categories carry the most fraud risk?

## Workflow

```text
Generate transactions -> validate and clean -> engineer risk features
-> load SQLite -> run SQL analysis -> export CSVs and charts
```

## Run locally

```bash
git clone https://github.com/Hamzas-github/fintech-fraud-risk-monitoring.git
cd fintech-fraud-risk-monitoring
pip install -r requirements.txt
python scripts/build_project.py
```

The script rebuilds the dataset, SQLite database, CSV outputs, and charts from scratch.

## Results from the current run

| Metric | Value |
|---|---:|
| Transactions | 65,000 |
| Transaction volume | GBP 2.96m |
| Fraud transactions | 1,338 |
| Fraud rate | 2.06% |
| Fraud loss | GBP 73.8k |
| Alert rate | 4.42% |

## Outputs

- `outputs/summary_metrics.csv`
- `outputs/monthly_fraud_trend.csv`
- `outputs/fraud_by_channel.csv`
- `outputs/fraud_by_merchant_category.csv`
- `outputs/high_risk_merchants.csv`
- `outputs/high_risk_customers.csv`
- Chart images in `outputs/`

## Findings

- Card-not-present transactions produced the highest fraud rate.
- Crypto, cash withdrawal, gaming, electronics, and travel were the riskiest merchant groups.
- The pipeline creates ranked customer and merchant investigation queues for review.

See [CASE_STUDY.md](CASE_STUDY.md) for the analysis and business recommendations.

## Skills demonstrated

Python, pandas, SQL, SQLite, feature engineering, data-quality checks, fraud KPIs, risk segmentation, investigation queues, and dashboard-ready reporting.

# Case Study: Fintech Fraud and Risk Monitoring

## Summary

I built this project to show fraud and risk analytics work for fintech data roles.
The project creates card transaction data, cleans it, saves it in SQLite and then runs
SQL queries to find risky areas.

In the current run there are **65,000 transactions**, **GBP 2.96m** transaction volume,
**1,338 fraud transactions**, **2.06% fraud rate** and **GBP 73.8k** fraud loss.

## What I found

### 1. Card not present was most risky

Card not present transactions had **2.84%** fraud rate. Mobile wallet had **1.80%**
and card present had **1.47%**.

This means card not present transactions should have more monitoring, especially when
the amount is high or the transaction is cross border.

### 2. Some merchant groups had more fraud

Crypto had the highest fraud rate in this data at **5.34%**.

Cash withdrawal, gaming, electronics and travel was also important because they had
either higher fraud rate or higher fraud loss.

### 3. The project gives an investigation list

The SQL output ranks merchants by fraud loss and fraud rate. This is useful because
the risk team can start with the merchants causing the most loss.

The highest loss merchant in the generated data was `M00616`. It was a crypto merchant
with **72 transactions**, **7 fraud transactions**, **9.72% fraud rate** and around
**GBP 1.3k** fraud loss.

### 4. Data quality is also checked

The project checks duplicate transaction IDs, missing values, wrong amounts and wrong
fraud labels. All checks passed in the generated data.

This is important because if data quality is bad then the fraud dashboard is not really
useful.

## Tools used

- Python
- pandas
- NumPy
- SQLite
- SQL
- Matplotlib
- Seaborn

## Why this project is useful for my portfolio

This project matches the type of things I saw in London data jobs:

- SQL and Python
- risk analytics
- data quality checks
- dashboard outputs
- fraud and transaction monitoring
- explaining findings in simple words

It is not only charts. It also has data cleaning, SQL, database work and business
thinking.


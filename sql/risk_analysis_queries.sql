-- Fintech Fraud and Risk Monitoring
-- These queries are also executed by scripts/build_project.py and exported to CSV.

-- 1. Portfolio-level risk summary
select
  count(*) as transactions,
  round(sum(amount_gbp), 2) as total_volume_gbp,
  sum(is_fraud) as fraud_transactions,
  round(100.0 * avg(is_fraud), 2) as fraud_rate_pct,
  round(sum(case when is_fraud = 1 then amount_gbp else 0 end), 2) as fraud_loss_gbp
from transactions_clean;

-- 2. Monthly fraud trend
select
  strftime('%Y-%m', transaction_ts) as month,
  count(*) as transactions,
  sum(is_fraud) as fraud_transactions,
  round(100.0 * avg(is_fraud), 2) as fraud_rate_pct,
  round(sum(case when is_fraud = 1 then amount_gbp else 0 end), 2) as fraud_loss_gbp
from transactions_clean
group by 1
order by 1;

-- 3. Fraud by channel
select
  channel,
  count(*) as transactions,
  sum(is_fraud) as fraud_transactions,
  round(100.0 * avg(is_fraud), 2) as fraud_rate_pct,
  round(sum(case when is_fraud = 1 then amount_gbp else 0 end), 2) as fraud_loss_gbp
from transactions_clean
group by 1
order by fraud_rate_pct desc;

-- 4. Merchant category risk
select
  merchant_category,
  count(*) as transactions,
  sum(is_fraud) as fraud_transactions,
  round(100.0 * avg(is_fraud), 2) as fraud_rate_pct,
  round(sum(case when is_fraud = 1 then amount_gbp else 0 end), 2) as fraud_loss_gbp
from transactions_clean
group by 1
having transactions >= 250
order by fraud_rate_pct desc, fraud_loss_gbp desc;

-- 5. High-risk merchants for investigation
with merchant_risk as (
  select
    merchant_id,
    merchant_category,
    count(*) as transactions,
    sum(is_fraud) as fraud_transactions,
    avg(is_fraud) as fraud_rate,
    sum(case when is_fraud = 1 then amount_gbp else 0 end) as fraud_loss_gbp
  from transactions_clean
  group by 1, 2
)
select
  merchant_id,
  merchant_category,
  transactions,
  fraud_transactions,
  round(100.0 * fraud_rate, 2) as fraud_rate_pct,
  round(fraud_loss_gbp, 2) as fraud_loss_gbp,
  dense_rank() over (order by fraud_loss_gbp desc) as loss_rank
from merchant_risk
where transactions >= 40
order by fraud_loss_gbp desc
limit 20;

-- 6. High-risk customers for investigation
with customer_risk as (
  select
    customer_id,
    count(*) as transactions,
    sum(is_fraud) as fraud_transactions,
    avg(is_fraud) as fraud_rate,
    sum(amount_gbp) as total_spend_gbp,
    sum(case when is_fraud = 1 then amount_gbp else 0 end) as fraud_loss_gbp,
    max(txn_count_last_24h) as max_txn_count_last_24h
  from transactions_clean
  group by 1
)
select
  customer_id,
  transactions,
  fraud_transactions,
  round(100.0 * fraud_rate, 2) as fraud_rate_pct,
  round(total_spend_gbp, 2) as total_spend_gbp,
  round(fraud_loss_gbp, 2) as fraud_loss_gbp,
  max_txn_count_last_24h
from customer_risk
where transactions >= 10
order by fraud_loss_gbp desc, max_txn_count_last_24h desc
limit 20;

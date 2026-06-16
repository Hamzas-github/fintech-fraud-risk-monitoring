from __future__ import annotations

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
DB_DIR = ROOT / "database"
OUTPUT_DIR = ROOT / "outputs"

RAW_FILE = RAW_DIR / "transactions_raw.csv"
CLEAN_FILE = PROCESSED_DIR / "transactions_clean.csv"
DB_FILE = DB_DIR / "fintech_fraud.db"


def ensure_dirs() -> None:
    for path in [RAW_DIR, PROCESSED_DIR, DB_DIR, OUTPUT_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def generate_raw_transactions(rows: int = 65_000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    customer_ids = [f"C{n:06d}" for n in range(1, 8_501)]
    categories = np.array(
        [
            "groceries",
            "restaurants",
            "transport",
            "travel",
            "electronics",
            "gaming",
            "crypto",
            "cash_withdrawal",
            "fashion",
            "subscriptions",
        ]
    )
    category_probs = np.array([0.18, 0.16, 0.12, 0.08, 0.1, 0.08, 0.04, 0.04, 0.12, 0.08])
    category_risk = {
        "groceries": 0.002,
        "restaurants": 0.003,
        "transport": 0.002,
        "travel": 0.010,
        "electronics": 0.016,
        "gaming": 0.020,
        "crypto": 0.045,
        "cash_withdrawal": 0.025,
        "fashion": 0.008,
        "subscriptions": 0.006,
    }
    merchant_ids = np.array([f"M{n:05d}" for n in range(1, 901)])
    merchant_lookup = pd.DataFrame(
        {
            "merchant_id": merchant_ids,
            "merchant_category": rng.choice(categories, size=len(merchant_ids), p=category_probs),
        }
    )
    merchants_by_category = {
        category: merchant_lookup.loc[merchant_lookup["merchant_category"].eq(category), "merchant_id"].to_numpy()
        for category in categories
    }

    start = pd.Timestamp("2025-01-01")
    end = pd.Timestamp("2025-12-31 23:59:59")
    seconds = int((end - start).total_seconds())
    transaction_ts = start + pd.to_timedelta(rng.integers(0, seconds, rows), unit="s")

    merchant_category = rng.choice(categories, size=rows, p=category_probs)
    transaction_merchant_ids = np.array(
        [rng.choice(merchants_by_category[category]) for category in merchant_category]
    )
    channel = rng.choice(["card_present", "card_not_present", "mobile_wallet"], size=rows, p=[0.46, 0.40, 0.14])
    customer_tenure_days = rng.integers(1, 1_800, size=rows)
    is_cross_border = rng.binomial(1, 0.13, size=rows)
    is_weekend = pd.Series(transaction_ts).dt.dayofweek.ge(5).astype(int).to_numpy()
    hour = pd.Series(transaction_ts).dt.hour.to_numpy()
    is_night = ((hour <= 5) | (hour >= 23)).astype(int)

    amount_multiplier = pd.Series(merchant_category).map(
        {
            "groceries": 0.75,
            "restaurants": 0.8,
            "transport": 0.45,
            "travel": 2.4,
            "electronics": 2.2,
            "gaming": 0.9,
            "crypto": 2.8,
            "cash_withdrawal": 1.6,
            "fashion": 1.1,
            "subscriptions": 0.5,
        }
    ).to_numpy()
    amount_gbp = rng.lognormal(mean=3.4, sigma=0.75, size=rows) * amount_multiplier
    amount_gbp = np.clip(amount_gbp, 2.5, 4_500).round(2)

    base_risk = np.array([category_risk[c] for c in merchant_category])
    fraud_probability = (
        base_risk
        + (channel == "card_not_present") * 0.012
        + (channel == "mobile_wallet") * 0.004
        + (amount_gbp > 500) * 0.018
        + (amount_gbp > 1_500) * 0.035
        + is_cross_border * 0.010
        + is_night * 0.012
        + (customer_tenure_days < 30) * 0.020
        + is_weekend * 0.003
    )
    fraud_probability = np.clip(fraud_probability, 0.001, 0.35)
    is_fraud = rng.binomial(1, fraud_probability)

    df = pd.DataFrame(
        {
            "transaction_id": [f"T{n:08d}" for n in range(1, rows + 1)],
            "transaction_ts": transaction_ts,
            "customer_id": rng.choice(customer_ids, size=rows),
            "merchant_id": transaction_merchant_ids,
            "merchant_category": merchant_category,
            "channel": channel,
            "amount_gbp": amount_gbp,
            "is_cross_border": is_cross_border,
            "customer_tenure_days": customer_tenure_days,
            "is_fraud": is_fraud,
        }
    ).sort_values("transaction_ts")

    return df


def clean_and_validate(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    clean = df.copy()
    clean["transaction_ts"] = pd.to_datetime(clean["transaction_ts"], errors="coerce")
    clean["amount_gbp"] = pd.to_numeric(clean["amount_gbp"], errors="coerce")
    clean = clean.drop_duplicates(subset=["transaction_id"])
    clean = clean.dropna(subset=["transaction_id", "transaction_ts", "customer_id", "merchant_id", "amount_gbp"])
    clean = clean[clean["amount_gbp"] > 0].copy()

    clean["transaction_date"] = clean["transaction_ts"].dt.date.astype(str)
    clean["month"] = clean["transaction_ts"].dt.to_period("M").astype(str)
    clean["hour"] = clean["transaction_ts"].dt.hour
    clean["day_of_week"] = clean["transaction_ts"].dt.day_name()
    clean["is_weekend"] = clean["transaction_ts"].dt.dayofweek.ge(5).astype(int)
    clean["is_night"] = clean["hour"].between(23, 23).astype(int) | clean["hour"].between(0, 5).astype(int)
    clean["is_high_value"] = (clean["amount_gbp"] >= 500).astype(int)

    clean = clean.sort_values(["customer_id", "transaction_ts"])
    rolling_counts = (
        clean.set_index("transaction_ts")
        .groupby("customer_id")["transaction_id"]
        .rolling("24h")
        .count()
        .reset_index(level=0, drop=True)
        .astype(int)
    )
    clean["txn_count_last_24h"] = rolling_counts.to_numpy()
    clean["velocity_flag"] = (clean["txn_count_last_24h"] >= 6).astype(int)

    high_risk_categories = {"crypto", "cash_withdrawal", "electronics", "gaming", "travel"}
    clean["high_risk_category_flag"] = clean["merchant_category"].isin(high_risk_categories).astype(int)
    clean["rule_alert"] = (
        (clean["high_risk_category_flag"] == 1)
        & ((clean["is_high_value"] == 1) | (clean["velocity_flag"] == 1) | (clean["is_cross_border"] == 1))
    ).astype(int)

    checks = [
        ("duplicate_transaction_ids", int(clean["transaction_id"].duplicated().sum()), "pass"),
        ("missing_required_values", int(clean[["transaction_id", "transaction_ts", "customer_id", "merchant_id", "amount_gbp"]].isna().sum().sum()), "pass"),
        ("non_positive_amounts", int((clean["amount_gbp"] <= 0).sum()), "pass"),
        ("invalid_fraud_labels", int((~clean["is_fraud"].isin([0, 1])).sum()), "pass"),
    ]
    quality = pd.DataFrame(checks, columns=["check_name", "issue_count", "status"])
    quality["status"] = np.where(quality["issue_count"].eq(0), "pass", "fail")

    return clean, quality


def write_database(clean: pd.DataFrame, quality: pd.DataFrame) -> None:
    if DB_FILE.exists():
        DB_FILE.unlink()

    with sqlite3.connect(DB_FILE) as conn:
        clean.to_sql("transactions_clean", conn, index=False, if_exists="replace")
        quality.to_sql("data_quality_checks", conn, index=False, if_exists="replace")


def export_query(conn: sqlite3.Connection, name: str, query: str) -> pd.DataFrame:
    result = pd.read_sql_query(query, conn)
    result.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)
    return result


def run_sql_outputs() -> dict[str, pd.DataFrame]:
    queries = {
        "summary_metrics": """
            select
              count(*) as transactions,
              round(sum(amount_gbp), 2) as total_volume_gbp,
              sum(is_fraud) as fraud_transactions,
              round(100.0 * avg(is_fraud), 2) as fraud_rate_pct,
              round(sum(case when is_fraud = 1 then amount_gbp else 0 end), 2) as fraud_loss_gbp,
              round(100.0 * avg(rule_alert), 2) as alert_rate_pct
            from transactions_clean;
        """,
        "monthly_fraud_trend": """
            select
              month,
              count(*) as transactions,
              sum(is_fraud) as fraud_transactions,
              round(100.0 * avg(is_fraud), 2) as fraud_rate_pct,
              round(sum(case when is_fraud = 1 then amount_gbp else 0 end), 2) as fraud_loss_gbp
            from transactions_clean
            group by 1
            order by 1;
        """,
        "fraud_by_channel": """
            select
              channel,
              count(*) as transactions,
              sum(is_fraud) as fraud_transactions,
              round(100.0 * avg(is_fraud), 2) as fraud_rate_pct,
              round(sum(case when is_fraud = 1 then amount_gbp else 0 end), 2) as fraud_loss_gbp
            from transactions_clean
            group by 1
            order by fraud_rate_pct desc;
        """,
        "fraud_by_merchant_category": """
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
        """,
        "high_risk_merchants": """
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
        """,
        "high_risk_customers": """
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
            where transactions >= 5
            order by fraud_loss_gbp desc, max_txn_count_last_24h desc
            limit 20;
        """,
    }

    with sqlite3.connect(DB_FILE) as conn:
        return {name: export_query(conn, name, query) for name, query in queries.items()}


def save_bar_chart(df: pd.DataFrame, x: str, y: str, title: str, filename: str) -> None:
    plt.figure(figsize=(10, 5.5))
    sns.barplot(data=df, x=x, y=y, color="#2f6f73")
    plt.title(title, fontsize=14, weight="bold")
    plt.xlabel("")
    ylabel = "Fraud rate (%)" if y == "fraud_rate_pct" else y.replace("_", " ").title()
    plt.ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=180)
    plt.close()


def build_charts(outputs: dict[str, pd.DataFrame]) -> None:
    sns.set_theme(style="whitegrid")

    trend = outputs["monthly_fraud_trend"]
    plt.figure(figsize=(10, 5.5))
    sns.lineplot(data=trend, x="month", y="fraud_rate_pct", marker="o", color="#8f2d56")
    plt.title("Monthly fraud rate", fontsize=14, weight="bold")
    plt.xlabel("")
    plt.ylabel("Fraud rate (%)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_fraud_rate.png", dpi=180)
    plt.close()

    save_bar_chart(
        outputs["fraud_by_channel"],
        "channel",
        "fraud_rate_pct",
        "Fraud rate by transaction channel",
        "fraud_rate_by_channel.png",
    )

    category = outputs["fraud_by_merchant_category"].sort_values("fraud_rate_pct", ascending=False)
    save_bar_chart(
        category,
        "merchant_category",
        "fraud_rate_pct",
        "Fraud rate by merchant category",
        "fraud_rate_by_category.png",
    )

    merchants = outputs["high_risk_merchants"].head(10).sort_values("fraud_loss_gbp", ascending=True)
    if not merchants.empty:
        plt.figure(figsize=(10, 5.5))
        sns.barplot(data=merchants, y="merchant_id", x="fraud_loss_gbp", hue="merchant_category", dodge=False)
        plt.title("Top merchants by fraud loss", fontsize=14, weight="bold")
        plt.xlabel("Fraud loss (GBP)")
        plt.ylabel("")
        plt.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "top_merchants_by_fraud_loss.png", dpi=180)
        plt.close()


def main() -> None:
    ensure_dirs()
    raw = generate_raw_transactions()
    raw.to_csv(RAW_FILE, index=False)

    clean, quality = clean_and_validate(raw)
    clean.to_csv(CLEAN_FILE, index=False)
    quality.to_csv(OUTPUT_DIR / "data_quality_checks.csv", index=False)

    write_database(clean, quality)
    outputs = run_sql_outputs()
    build_charts(outputs)

    summary = outputs["summary_metrics"].iloc[0].to_dict()
    print("Project build complete")
    print(f"Transactions: {summary['transactions']:,}")
    print(f"Total volume: GBP {summary['total_volume_gbp']:,.2f}")
    print(f"Fraud rate: {summary['fraud_rate_pct']:.2f}%")
    print(f"Fraud loss: GBP {summary['fraud_loss_gbp']:,.2f}")
    print(f"Outputs written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

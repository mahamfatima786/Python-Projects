"""Sales Data Analysis Dashboard
Data cleaning -> analysis -> charts -> Excel report.

Usage:
    python sales_dashboard.py                 # sample data ke saath chalta hai
    python sales_dashboard.py my_sales.xlsx   # apni Excel/CSV file ke saath
Zaroori columns: order_id, date, product, category, quantity, unit_price
"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTPUT_PNG = "sales_dashboard.png"
OUTPUT_XLSX = "sales_report.xlsx"


def make_sample_data(n=600, seed=42):
    """Sample (jaan boojh kar gandi) sales data banata hai."""
    rng = np.random.default_rng(seed)
    catalog = {
        "Laptop": ("Electronics", 950), "Phone": ("Electronics", 600),
        "Headphones": ("Electronics", 80), "Desk": ("Furniture", 220),
        "Chair": ("Furniture", 140), "Notebook": ("Stationery", 4),
        "Pen Set": ("Stationery", 12), "Backpack": ("Accessories", 45),
    }
    products = rng.choice(list(catalog), n, p=[.08, .12, .18, .06, .08, .22, .16, .10])
    df = pd.DataFrame({
        "order_id": np.arange(1000, 1000 + n),
        "date": pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D"),
        "product": products,
        "category": [catalog[p][0] for p in products],
        "quantity": rng.integers(1, 8, n).astype(float),
        "unit_price": [catalog[p][1] * rng.uniform(0.95, 1.05) for p in products],
    })
    # Gandagi: duplicates, missing values, ghalat spelling/spacing, negative qty
    df.loc[rng.choice(n, 15, replace=False), "quantity"] = np.nan
    df.loc[rng.choice(n, 10, replace=False), "unit_price"] = np.nan
    df.loc[rng.choice(n, 8, replace=False), "quantity"] = -1
    df.loc[rng.choice(n, 20, replace=False), "product"] = df["product"].str.upper() + " "
    df = pd.concat([df, df.sample(12, random_state=1)], ignore_index=True)
    return df


def load_data(path=None):
    if path is None:
        return make_sample_data()
    return pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)


def clean_data(df):
    report = {"rows_start": len(df)}
    df = df.drop_duplicates().copy()
    report["duplicates_removed"] = report["rows_start"] - len(df)

    df["product"] = df["product"].astype(str).str.strip().str.title()
    df["category"] = df["category"].astype(str).str.strip().str.title()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Missing price: product ki median price se bharein
    median_price = df.groupby("product")["unit_price"].transform("median")
    report["prices_filled"] = int(df["unit_price"].isna().sum())
    df["unit_price"] = df["unit_price"].fillna(median_price)

    # Ghalat ya missing quantity wali rows hata dein
    bad = df["quantity"].isna() | (df["quantity"] <= 0) | df["date"].isna()
    report["invalid_rows_removed"] = int(bad.sum())
    df = df[~bad].copy()

    df["quantity"] = df["quantity"].astype(int)
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    report["rows_end"] = len(df)
    return df.reset_index(drop=True), report


def analyze(df):
    return {
        "total_revenue": df["revenue"].sum(),
        "total_orders": df["order_id"].nunique(),
        "avg_order_value": df["revenue"].mean(),
        "by_product": df.groupby("product").agg(
            units_sold=("quantity", "sum"), revenue=("revenue", "sum")
        ).sort_values("revenue", ascending=False),
        "by_category": df.groupby("category")["revenue"].sum().sort_values(ascending=False),
        "monthly": df.groupby("month")["revenue"].sum(),
    }


def build_dashboard(res):
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(
        f"Sales Dashboard  |  Revenue: ${res['total_revenue']:,.0f}  |  "
        f"Orders: {res['total_orders']:,}  |  Avg Order: ${res['avg_order_value']:,.0f}",
        fontsize=14, fontweight="bold",
    )

    ax = axes[0, 0]
    m = res["monthly"]
    ax.plot(m.index, m.values, marker="o", color="#2a6fdb")
    ax.set_title("Monthly Revenue")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    top = res["by_product"].head(5).iloc[::-1]
    ax.barh(top.index, top["revenue"], color="#2a9d8f")
    ax.set_title("Top 5 Products by Revenue")

    ax = axes[1, 0]
    c = res["by_category"]
    ax.pie(c.values, labels=c.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Revenue Share by Category")

    ax = axes[1, 1]
    units = res["by_product"]["units_sold"].sort_values(ascending=False)
    ax.bar(units.index, units.values, color="#e76f51")
    ax.set_title("Units Sold by Product")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUTPUT_PNG, dpi=150)
    plt.close(fig)


def export_excel(df, res, report):
    summary = pd.DataFrame({
        "Metric": ["Total Revenue", "Total Orders", "Avg Order Value",
                   "Duplicates Removed", "Invalid Rows Removed", "Prices Filled"],
        "Value": [round(res["total_revenue"], 2), res["total_orders"],
                  round(res["avg_order_value"], 2), report["duplicates_removed"],
                  report["invalid_rows_removed"], report["prices_filled"]],
    })
    with pd.ExcelWriter(OUTPUT_XLSX) as writer:
        summary.to_excel(writer, sheet_name="Summary", index=False)
        res["by_product"].round(2).to_excel(writer, sheet_name="By Product")
        res["by_category"].round(2).to_frame().to_excel(writer, sheet_name="By Category")
        res["monthly"].round(2).to_frame().to_excel(writer, sheet_name="Monthly")
        clean = df.drop(columns="month").copy()
        clean["unit_price"] = clean["unit_price"].round(2)
        clean["revenue"] = clean["revenue"].round(2)
        clean.to_excel(writer, sheet_name="Clean Data", index=False)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    df, report = clean_data(load_data(path))
    res = analyze(df)
    build_dashboard(res)
    export_excel(df, res, report)

    print("Cleaning report:", report)
    print(f"Total revenue: ${res['total_revenue']:,.2f}")
    print("\nTop 5 products:")
    print(res["by_product"].head(5).round(2))
    print(f"\nSaved: {OUTPUT_PNG}, {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()

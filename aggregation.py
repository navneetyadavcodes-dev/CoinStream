import pandas as pd
from db import engine

def generate_daily_summary():
    df = pd.read_sql("SELECT * FROM clean_prices", engine)

    if df.empty:
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    grouped = df.groupby(["date", "cryptocurrency"])

    summary = grouped["price"].agg(
        open="first",
        close="last",
        high="max",
        low="min",
        avg="mean",
        volatility="std"
    ).reset_index()

    # Missing hours
    missing_list = []
    for (date, crypto), group in grouped:
        missing = 24 - len(group)
        missing_list.append(missing)

    summary["missing_hours"] = missing_list

    summary.to_csv("daily_summary.csv", index=False)
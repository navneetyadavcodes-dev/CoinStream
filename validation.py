import pandas as pd
from db import engine

def validate_data():
    df = pd.read_sql("SELECT * FROM clean_prices", engine)

    if df.empty:
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    df = df.sort_values("timestamp")

    report = []

    for (date, crypto), sub in df.groupby(["date", "cryptocurrency"]):
        # Missing hours
        if len(sub) < 24:
            report.append({
                "Date": date,
                "Cryptocurrency": crypto,
                "Type of issue": "Missing data",
                "Description": f"{24-len(sub)} hourly data points missing"
            })

        # Time gap
        sub = sub.copy()
        sub["diff"] = sub["timestamp"].diff()
        
        if not sub["diff"].isnull().all() and sub["diff"].max().total_seconds() > 10800:
            report.append({
                "Date": date,
                "Cryptocurrency": crypto,
                "Type of issue": "Time gap",
                "Description": "Time gap greater than 3 hours detected"
            })

    pd.DataFrame(report, columns=["Date", "Cryptocurrency", "Type of issue", "Description"]).to_csv("validation_report.csv", index=False)
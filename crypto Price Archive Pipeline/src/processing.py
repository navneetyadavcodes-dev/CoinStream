from datetime import datetime
import pandas as pd
from sqlalchemy import text
from src.db import engine

def process_and_store(data):
    if data is None:
        return
    
    timestamp = datetime.utcnow()
    rows = []

    for coin in data:
        rows.append({
            "timestamp": timestamp,
            "cryptocurrency": coin["symbol"].upper(),
            "price": coin["current_price"]
        })

    df = pd.DataFrame(rows)

    df.drop_duplicates(subset=["timestamp", "cryptocurrency"], inplace=True)

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
            INSERT OR IGNORE INTO clean_prices (timestamp, cryptocurrency, price)
            VALUES (:timestamp, :crypto, :price)
            """), {
                "timestamp": str(row["timestamp"]),
                "crypto": row["cryptocurrency"],
                "price": row["price"]
            })
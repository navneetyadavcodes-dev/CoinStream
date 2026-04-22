from sqlalchemy import create_engine, text

from src.config import DB_URL

engine = create_engine(DB_URL)

def create_tables():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS raw_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at TIMESTAMP,
            api_response TEXT
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS clean_prices (
            timestamp TIMESTAMP,
            cryptocurrency TEXT,
            price FLOAT,
            PRIMARY KEY (timestamp, cryptocurrency)
        );
        """))
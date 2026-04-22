import time
import requests
import json
import logging
from datetime import datetime
from sqlalchemy import text
from src.db import engine
from src import config

logger = logging.getLogger(__name__)

def fetch_data():
    for attempt in range(3):
        try:
            res = requests.get(config.API_URL, params=config.PARAMS)
            if res.status_code == 200:
                logger.info("Successfully fetched data from CoinGecko API")
                return res.json()
            else:
                logger.warning(f"API call failed with status {res.status_code}")
        except Exception as e:
            logger.error(f"API Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    logger.error("Failed to fetch data after 3 attempts")
    return None

def store_raw(data):
    if not data:
        return
    with engine.begin() as conn:
        conn.execute(text("""
        INSERT INTO raw_prices (fetched_at, api_response)
        VALUES (:fetched_at, :api_response)
        """), {
            "fetched_at": datetime.utcnow(),
            "api_response": json.dumps(data)
        })
        logger.info("Raw data stored successfully")
import schedule
import time
import logging

from src.db import create_tables
from src.ingestion import fetch_data, store_raw
from src.processing import process_and_store
from src.aggregation import generate_daily_summary
from src.validation import validate_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info("Starting pipeline run...")
    data = fetch_data()
    store_raw(data)
    process_and_store(data)
    generate_daily_summary()
    validate_data()
    logger.info("Pipeline run complete")

if __name__ == "__main__":
    create_tables()
    logger.info("Tables created or already exist.")
    
    # Run once immediately for testing/initial data
    run_pipeline()

    schedule.every(1).hours.do(run_pipeline)
    logger.info("Scheduler started. Waiting for next run...")

    while True:
        schedule.run_pending()
        time.sleep(1)
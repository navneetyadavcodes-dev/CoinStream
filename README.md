# CoinStream 🚀

A robust, automated data engineering pipeline in Python that collects, processes, validates, and analyzes cryptocurrency price data from the CoinGecko API. 

## 📊 Features
- **Reliable Data Ingestion:** Fetches the top 10 cryptocurrency prices hourly with a built-in 3-retry mechanism to handle network errors.
- **Data Processing:** Normalizes timestamps to UTC and deduplicates data to ensure absolute idempotency.
- **Data Storage:** Uses an SQLite Database to maintain raw unedited JSON (`raw_prices`) and processed analytics data (`clean_prices`).
- **Daily Aggregation Analytics:** Automatically generates a daily CSV summary calculating Open, Close, High, Low, Average, and Volatility metrics.
- **Automated Validation:** Runs daily quality checks to detect missing hourly data points and time gaps greater than 3 hours, outputting a clear validation report.

## ⚙️ Setup Instructions

1. Clone the repository: `git clone https://github.com/navneetyadavcodes-dev/CoinStream.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the pipeline: `python main.py`

## 🏗️ Architecture
- `main.py`: Orchestrates the pipeline and runs the hourly continuous scheduler.
- `config.py`: Contains API parameters and database URLs.
- `db.py`: Initializes the SQLite database and table schemas.
- `ingestion.py`: Fetches data from CoinGecko and stores raw JSON responses.
- `processing.py`: Normalizes data, handles timezone conversion, and inserts clean records safely.
- `aggregation.py`: Calculates daily metrics and outputs `daily_summary.csv`.
- `validation.py`: Identifies data quality issues and outputs `validation_report.csv`.

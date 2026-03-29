"""
ingestion/download_dataset.py

Downloads the Olist Brazilian E-Commerce dataset from Kaggle
and places all CSVs into data/raw/.

Usage:
    python ingestion/download_dataset.py

Requires:
    - KAGGLE_API_TOKEN set in .env
    - kagglehub and python-dotenv installed (pip install -r requirements.txt)
"""

import os
import shutil
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(message)s")
logger = logging.getLogger(__name__)

DATASET = "olistbr/brazilian-ecommerce"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

EXPECTED_FILES = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "product_category_name_translation.csv",
]


def download():
    import kagglehub

    logger.info(f"Downloading dataset: {DATASET}")
    cache_path = Path(kagglehub.dataset_download(DATASET))
    logger.info(f"Downloaded to cache: {cache_path}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = list(cache_path.rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in cache path: {cache_path}")

    copied = []
    for csv_file in csv_files:
        dest = OUTPUT_DIR / csv_file.name
        shutil.copy2(csv_file, dest)
        copied.append(csv_file.name)
        logger.info(f"  ✅ {csv_file.name}")

    logger.info(f"\nCopied {len(copied)} files to {OUTPUT_DIR}")

    missing = [f for f in EXPECTED_FILES if f not in copied]
    if missing:
        logger.warning(f"⚠️  Expected files not found: {missing}")
    else:
        logger.info("✅ All 9 expected files accounted for.")


if __name__ == "__main__":
    download()

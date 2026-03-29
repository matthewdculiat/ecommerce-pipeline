"""
ingestion/upload_to_s3.py
Reads Olist CSV files from /data/raw and uploads them to AWS S3.
Simulates incremental loads using a date partition prefix.
"""

import os
import logging
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from pathlib import Path

# ─── Config ─────────────────────────────────────────────────────────────────
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "your-ecommerce-pipeline-bucket")
RAW_DATA_PATH = Path("/opt/airflow/data/raw")
S3_PREFIX = "raw/olist"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── Olist dataset files ─────────────────────────────────────────────────────
OLIST_FILES = [
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


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_DEFAULT_REGION", "ap-southeast-1"),
    )


def upload_file(s3_client, local_path: Path, s3_key: str) -> bool:
    """Upload a single file to S3. Returns True on success."""
    try:
        logger.info(f"Uploading {local_path.name} → s3://{S3_BUCKET}/{s3_key}")
        s3_client.upload_file(str(local_path), S3_BUCKET, s3_key)
        logger.info(f"✅ Uploaded: {local_path.name}")
        return True
    except ClientError as e:
        logger.error(f"❌ Failed to upload {local_path.name}: {e}")
        return False


def upload_all(execution_date: str = None):
    """
    Upload all Olist files to S3 with a date partition prefix.
    execution_date: 'YYYY-MM-DD' string (defaults to today)
    """
    if execution_date is None:
        execution_date = datetime.today().strftime("%Y-%m-%d")

    s3 = get_s3_client()
    results = {"success": [], "failed": []}

    for filename in OLIST_FILES:
        local_path = RAW_DATA_PATH / filename

        if not local_path.exists():
            logger.warning(f"⚠️  File not found locally, skipping: {filename}")
            results["failed"].append(filename)
            continue

        # Partition by date: raw/olist/2024-01-01/olist_orders_dataset.csv
        s3_key = f"{S3_PREFIX}/{execution_date}/{filename}"
        success = upload_file(s3, local_path, s3_key)

        if success:
            results["success"].append(filename)
        else:
            results["failed"].append(filename)

    # Summary
    logger.info(f"\n{'='*50}")
    logger.info(f"Upload complete. Success: {len(results['success'])} | Failed: {len(results['failed'])}")
    if results["failed"]:
        logger.warning(f"Failed files: {results['failed']}")

    return results


if __name__ == "__main__":
    upload_all()

"""
dags/ecommerce_pipeline.py
Main DAG: Olist CSV → S3 → Snowflake → dbt
Runs daily, simulating incremental batch loads.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from datetime import datetime, timedelta
import sys

sys.path.insert(0, "/opt/airflow/ingestion")

# ─── Default Args ─────────────────────────────────────────────────────────────
default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": False,   # Set to True + add your email once configured
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# ─── DAG Definition ───────────────────────────────────────────────────────────
with DAG(
    dag_id="ecommerce_pipeline",
    description="End-to-end pipeline: Olist CSV → S3 → Snowflake → dbt",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    tags=["ecommerce", "olist", "batch"],
) as dag:

    # ── Task 1: Upload raw CSVs to S3 ─────────────────────────────────────────
    def run_upload(**context):
        from upload_to_s3 import upload_all
        execution_date = context["ds"]  # 'YYYY-MM-DD'
        results = upload_all(execution_date=execution_date)
        if results["failed"]:
            raise ValueError(f"Some files failed to upload: {results['failed']}")

    upload_to_s3 = PythonOperator(
        task_id="upload_raw_to_s3",
        python_callable=run_upload,
        provide_context=True,
    )

    # ── Task 2: Load from S3 into Snowflake staging ───────────────────────────
    def run_snowflake_load(**context):
        """
        Uses Snowflake COPY INTO to load from S3.
        Requires snowflake-connector-python: pip install snowflake-connector-python
        Placeholder — full implementation added in Week 4.
        """
        import os
        # import snowflake.connector  # Uncomment in Week 4

        execution_date = context["ds"]
        s3_path = f"s3://{os.environ.get('S3_BUCKET_NAME')}/raw/olist/{execution_date}/"
        print(f"[Week 4] Will load from: {s3_path} into Snowflake staging")
        # Full COPY INTO logic goes here in Week 4

    load_to_snowflake = PythonOperator(
        task_id="load_to_snowflake_staging",
        python_callable=run_snowflake_load,
        provide_context=True,
    )

    # ── Task 3: Run dbt transformations ───────────────────────────────────────
    run_dbt = BashOperator(
        task_id="run_dbt_transformations",
        bash_command=(
            "cd /opt/airflow/dbt && "
            "dbt run --profiles-dir . --project-dir . && "
            "dbt test --profiles-dir . --project-dir ."
        ),
    )

    # ── Task 4: dbt docs (optional, generates lineage graph) ──────────────────
    generate_dbt_docs = BashOperator(
        task_id="generate_dbt_docs",
        bash_command="cd /opt/airflow/dbt && dbt docs generate --profiles-dir . --project-dir .",
    )

    # ── Pipeline Order ────────────────────────────────────────────────────────
    upload_to_s3 >> load_to_snowflake >> run_dbt >> generate_dbt_docs

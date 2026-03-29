# 🛒 E-Commerce Sales Data Pipeline

An end-to-end batch data pipeline built on a modern open-source stack, using the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

---

## 🏗️ Architecture

```
┌─────────────┐    ┌──────────────────┐    ┌──────────┐    ┌────────────┐    ┌──────────┐
│   Kaggle    │───▶│  Python Ingestion │───▶│  AWS S3  │───▶│ Snowflake  │───▶│   dbt    │
│ Olist CSVs  │    │  (upload_to_s3)  │    │ Raw Zone │    │  Staging   │    │ Models   │
└─────────────┘    └──────────────────┘    └──────────┘    └────────────┘    └────┬─────┘
                                                                                   │
                          ┌────────────────────────────────────────────────────────┘
                          ▼
                   ┌────────────┐    ┌──────────┐
                   │  Snowflake │───▶│ Power BI │
                   │   Marts    │    │Dashboard │
                   └────────────┘    └──────────┘

Orchestration: Apache Airflow (Docker)
```

---

## 🧰 Tech Stack

| Layer          | Tool                  |
|----------------|-----------------------|
| Orchestration  | Apache Airflow 2.9    |
| Ingestion      | Python + boto3        |
| Data Lake      | AWS S3                |
| Data Warehouse | Snowflake             |
| Transformation | dbt Core              |
| Visualization  | Power BI Desktop      |
| Containerization | Docker + Compose    |
| CI             | GitHub Actions        |

---

## 📁 Project Structure

```
ecommerce-pipeline/
├── dags/
│   └── ecommerce_pipeline.py     # Main Airflow DAG
├── ingestion/
│   └── upload_to_s3.py           # Raw CSV → S3 uploader
├── dbt/
│   ├── models/
│   │   ├── staging/              # Clean raw tables
│   │   ├── intermediate/         # Joined models
│   │   └── marts/                # Business-ready facts & dims
│   └── tests/                    # dbt data quality tests
├── data/
│   └── raw/                      # Local Olist CSVs (gitignored)
├── .github/
│   └── workflows/                # CI: run dbt tests on push
├── docker-compose.yml            # Airflow + Postgres
├── .env.example                  # Environment variable template
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Docker Desktop
- Python 3.9+
- AWS account (free tier)
- Kaggle account (free)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-pipeline.git
cd ecommerce-pipeline
```

### 2. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your AWS credentials
```

### 3. Download the dataset
Download from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and place all CSV files into `data/raw/`.

### 4. Start Airflow
```bash
docker compose up -d
```
Access the Airflow UI at **http://localhost:8080** (user: `admin`, password: `admin`)

### 5. Trigger the pipeline
Enable and trigger the `ecommerce_pipeline` DAG from the Airflow UI.

---

## 📊 dbt Models

```
staging/
  └── stg_orders.sql
  └── stg_customers.sql
  └── stg_products.sql
  └── stg_payments.sql

intermediate/
  └── int_orders_enriched.sql     # Orders + customers + payments joined

marts/
  └── fct_orders.sql              # One row per order, all metrics
  └── dim_customers.sql           # Customer dimension
  └── dim_products.sql            # Product dimension with categories
```

### Key Metrics Produced
- 📈 Monthly revenue by product category
- 👤 Customer Lifetime Value (CLV)
- 🚚 Average order fulfillment time
- ⭐ Review score trends by seller

---

## 📸 Dashboard Preview

*(Screenshots added after Week 7)*

---

## 🔜 Roadmap

- [x] Project scaffold & Docker setup
- [x] S3 ingestion layer
- [x] Airflow DAG skeleton
- [ ] Snowflake staging load (Week 4)
- [ ] dbt staging + intermediate models (Week 5)
- [ ] dbt mart models (Week 6)
- [ ] Power BI dashboard (Week 7)
- [ ] GitHub Actions CI for dbt tests (Week 8)
- [ ] Great Expectations data quality checks (Bonus)

---

## 👤 Author

Built as a portfolio project to demonstrate end-to-end data engineering skills.  
Connect on [LinkedIn](https://linkedin.com/in/YOUR_PROFILE)

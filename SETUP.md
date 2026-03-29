# SETUP.md — Onboarding Guide

This guide will take you from a fresh clone to a fully running local environment.
Estimated time: 15–20 minutes.

---

## Prerequisites

Before you begin, confirm you have the following installed:

| Tool | Version | Check |
|---|---|---|
| Python | 3.11+ | `python --version` |
| Docker Desktop | Latest | `docker --version` |
| Git | Any | `git --version` |

---

## Step 1 — Clone the Repository

```bash
git clone git@github.com:matthewdculiat/ecommerce-pipeline.git
cd ecommerce-pipeline
```

---

## Step 2 — Create and Activate a Virtual Environment

```bash
# Create
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (Mac/Linux)
source venv/bin/activate
```

Your terminal prompt should now show `(venv)` as a prefix. Every subsequent
command in this guide assumes the venv is active.

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

All packages are pinned. You will get the exact same environment as the author.

---

## Step 4 — Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and fill in the required values:

```
KAGGLE_API_TOKEN=your_kaggle_token_here
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_DEFAULT_REGION=ap-southeast-1
S3_BUCKET_NAME=your-bucket-name
```

Snowflake credentials can be left blank until Week 4.

> ⚠️ Never commit `.env` to version control. It is already in `.gitignore`.

---

## Step 5 — Download the Dataset

Run the ingestion script to download the Olist dataset from Kaggle:

```bash
python ingestion/download_dataset.py
```

This will place all 9 CSV files into `data/raw/`. Verify:

```bash
# Windows
ls data\raw

# Mac/Linux
ls data/raw
```

Expected: 9 `.csv` files totalling approximately 45MB.

---

## Step 6 — Start Airflow

```bash
docker compose up -d
```

First run will take 3–5 minutes while Docker pulls the Airflow image.
Subsequent starts are near-instant.

Check all containers are healthy:

```bash
docker compose ps
```

Expected output — all three services showing `running` or `healthy`:
- `airflow-webserver`
- `airflow-scheduler`
- `postgres`

Access the Airflow UI at: **http://localhost:8080**
Username: `admin` | Password: `admin`

---

## Step 7 — Verify the DAG

In the Airflow UI, navigate to **DAGs** and confirm `ecommerce_pipeline` appears.
It will be paused by default — this is expected at this stage of the project.

---

## Stopping the Environment

```bash
docker compose down
```

To also remove stored data (full reset):

```bash
docker compose down --volumes
```

---

## Troubleshooting

**Airflow UI not loading after `docker compose up`**
Wait 60–90 seconds and retry. The webserver takes longer on first boot.

**Port 8080 already in use**
Another service is occupying that port. Either stop it, or change the port
mapping in `docker-compose.yml` from `"8080:8080"` to `"8081:8080"`.

**`Activate.ps1` blocked on Windows**
Run this once in PowerShell as administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Project Roadmap

See [README.md](./README.md) for the full architecture, tech stack, and weekly build plan.

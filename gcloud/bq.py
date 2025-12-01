import os
from concurrent.futures import TimeoutError

import pandas as pd
from dotenv import load_dotenv
from google.api_core.exceptions import GoogleAPICallError
from google.cloud import bigquery

import gcloud.schemas as schemas

load_dotenv()

client = bigquery.Client(os.getenv("GCP_BQ_PROJECT_NAME", "market-volatility"))
dataset_name = os.getenv("GCP_BQ_DATASET_NAME", "sources")
dataset_ref = client.dataset(dataset_name)


def createTableIfNotExists(table_ref, schema):
    table = bigquery.Table(table_ref, schema)
    try:
        table = client.create_table(table)
        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")
    except Exception:
        print(
            f"Table {table.project}.{table.dataset_id}.{table.table_id} already exists, not creating again."
        )


def execute_load_job(
    df: pd.DataFrame,
    table_ref: bigquery.TableReference,
    schema,
):
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        schema=schema,
    )
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)

    try:
        job.result()  # Wait for the job to complete
        print(f"Loaded {job.output_rows} rows into {table_ref.path}.")
    except TimeoutError as e:
        print("Ingest Job for loading DataFrame timed out:", e)
    except GoogleAPICallError as e:
        print("Ingest API call for loading DataFrame failed:", e)


def ingestCoindesk(df: pd.DataFrame):
    table_ref = dataset_ref.table("coindesk")
    createTableIfNotExists(table_ref, schema=schemas.coindesk_schema)
    execute_load_job(df, table_ref, schemas.coindesk_schema)


def ingestCointelegraph(df: pd.DataFrame):
    table_ref = dataset_ref.table("cointelegraph")
    createTableIfNotExists(table_ref, schema=schemas.cointelegraph_schema)
    execute_load_job(df, table_ref, schemas.cointelegraph_schema)


def ingestCryptopanic(df: pd.DataFrame):
    table_ref = dataset_ref.table("cryptopanic")
    createTableIfNotExists(table_ref, schema=schemas.cryptopanic_schema)
    execute_load_job(df, table_ref, schemas.cryptopanic_schema)


def ingestNewsdata(df: pd.DataFrame):
    table_ref = dataset_ref.table("newsdata")
    createTableIfNotExists(table_ref, schema=schemas.newsdata_schema)
    execute_load_job(df, table_ref, schemas.newsdata_schema)


def ingestReddit(df: pd.DataFrame):
    table_ref = dataset_ref.table("reddit")
    createTableIfNotExists(table_ref, schema=schemas.reddit_schema)
    execute_load_job(df, table_ref, schemas.reddit_schema)


def ingestYFinanceNews(df: pd.DataFrame):
    table_ref = dataset_ref.table("yfinance_news")
    createTableIfNotExists(table_ref, schema=schemas.yfinance_news_schema)
    execute_load_job(df, table_ref, schemas.yfinance_news_schema)


def ingestYFinanceTickers(df: pd.DataFrame):
    table_ref = dataset_ref.table("yfinance_tickers")
    createTableIfNotExists(table_ref, schema=schemas.yfinance_tickers_schema)
    execute_load_job(df, table_ref, schemas.yfinance_tickers_schema)


def listAllTables():
    tables = list(client.list_tables(dataset_ref))
    print(f"Tables in dataset {len(tables)}")
    for table in tables:
        print(f"Table: {table.table_id}")

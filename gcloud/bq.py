import os
from concurrent.futures import TimeoutError

import pandas as pd
from dotenv import load_dotenv
from google.api_core.exceptions import GoogleAPICallError
from google.cloud import bigquery

from gcloud.tableconfig import getTableConfig

load_dotenv()

client = bigquery.Client(os.getenv("GCP_BQ_PROJECT_NAME", "market-volatility"))
dataset_name = os.getenv("GCP_BQ_DATASET_NAME", "sources")
dataset_ref = client.dataset(dataset_name)

TABLE_CONFIG = getTableConfig()


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


def execute_load_job_staging(
    df: pd.DataFrame,
    table_ref: bigquery.TableReference,
    schema,
):
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        schema=schema,
    )
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)

    try:
        job.result()  # Wait for the job to complete
        print(f"Loaded {job.output_rows} rows into staging table {table_ref.path}.")
    except TimeoutError as e:
        print("Ingest Job for loading DataFrame timed out:", e)
    except GoogleAPICallError as e:
        print("Ingest API call for loading DataFrame failed:", e)


def ingestTable(df: pd.DataFrame, table_name: str):
    if table_name not in TABLE_CONFIG:
        raise Exception(
            "Unknown table name provided for ingestion. Table details not known."
        )

    table = TABLE_CONFIG[table_name]

    staging_table_ref = dataset_ref.table(table["staging_table"])
    createTableIfNotExists(staging_table_ref, schema=table["schema"])
    execute_load_job_staging(df, staging_table_ref, table["schema"])

    table_ref = dataset_ref.table(table["table"])
    createTableIfNotExists(table_ref, schema=table["schema"])
    # TODO: upsert records between staging and final using merge query


def ingestCoindesk(df: pd.DataFrame):
    ingestTable(df, "coindesk")


def ingestCointelegraph(df: pd.DataFrame):
    ingestTable(df, "cointelegraph")


def ingestCryptopanic(df: pd.DataFrame):
    ingestTable(df, "cryptopanic")


def ingestNewsdata(df: pd.DataFrame):
    ingestTable(df, "newsdata")


def ingestReddit(df: pd.DataFrame):
    ingestTable(df, "reddit")


def ingestYFinanceNews(df: pd.DataFrame):
    ingestTable(df, "yfinance_news")


def ingestYFinanceTickers(df: pd.DataFrame):
    ingestTable(df, "yfinance_tickers")


def listAllTables():
    tables = list(client.list_tables(dataset_ref))
    print(f"Tables in dataset {len(tables)}")
    for table in tables:
        print(f"Table: {table.table_id}")

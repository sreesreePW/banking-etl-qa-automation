import os

BUSINESS_DATE = "2026-08-25"
FEED_ID = "CARD_DAILY"

STAGING_TABLE = "workspace.banking_etl_qa.stg_transactions"
TRANSACTIONS_TABLE = "workspace.banking_etl_qa.transactions"
ACCOUNT_TABLE = "workspace.banking_etl_qa.account_ref"
CUSTOMER_TABLE = "workspace.banking_etl_qa.customer_ref"
TARGET_TABLE = "workspace.banking_etl_qa.target_transactions"

DATABRICKS_SERVER_HOSTNAME = os.getenv("DATABRICKS_SERVER_HOSTNAME")
DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

SOURCE_PATH = "/Volumes/workspace/banking_etl_qa/source/card_daily/"
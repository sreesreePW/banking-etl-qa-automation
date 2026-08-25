import os

ENV = os.getenv("TEST_ENV", "QA1")

ENV_CONFIG = {
    "QA1": {
        "server_hostname": os.getenv("QA1_DATABRICKS_SERVER_HOSTNAME"),
        "http_path": os.getenv("QA1_DATABRICKS_HTTP_PATH"),
        "token": os.getenv("QA1_DATABRICKS_TOKEN"),
        "catalog": "workspace",
        "schema": "banking_etl_qa"
    },

    "QA2": {
        "server_hostname": os.getenv("QA2_DATABRICKS_SERVER_HOSTNAME"),
        "http_path": os.getenv("QA2_DATABRICKS_HTTP_PATH"),
        "token": os.getenv("QA2_DATABRICKS_TOKEN"),
        "catalog": "workspace",
        "schema": "banking_etl_qa"
    },

    "UAT": {
        "server_hostname": os.getenv("UAT_DATABRICKS_SERVER_HOSTNAME"),
        "http_path": os.getenv("UAT_DATABRICKS_HTTP_PATH"),
        "token": os.getenv("UAT_DATABRICKS_TOKEN"),
        "catalog": "workspace",
        "schema": "banking_etl_qa"
    }
}

CURRENT = ENV_CONFIG[ENV]
required_values = {
    "server_hostname": CURRENT["server_hostname"],
    "http_path": CURRENT["http_path"],
    "token": CURRENT["token"]
}

missing = [
    key
    for key, value in required_values.items()
    if not value
]

if missing:
    raise RuntimeError(
        f"Missing required configuration for {ENV}: "
        + ", ".join(missing)
    )
BUSINESS_DATE = "2026-08-25"
FEED_ID = "CARD_DAILY"

TRANSACTIONS_TABLE = (
    f"{CURRENT['catalog']}."
    f"{CURRENT['schema']}.transactions"
)

STAGING_TABLE = (
    f"{CURRENT['catalog']}."
    f"{CURRENT['schema']}.stg_transactions"
)

ACCOUNT_TABLE = (
    f"{CURRENT['catalog']}."
    f"{CURRENT['schema']}.account_ref"
)

CUSTOMER_TABLE = (
    f"{CURRENT['catalog']}."
    f"{CURRENT['schema']}.customer_ref"
)

TARGET_TABLE = (
    f"{CURRENT['catalog']}."
    f"{CURRENT['schema']}.target_transactions"
)

DATABRICKS_SERVER_HOSTNAME = CURRENT["server_hostname"]
DATABRICKS_HTTP_PATH = CURRENT["http_path"]
DATABRICKS_TOKEN = CURRENT["token"]
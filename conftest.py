import pytest
from pyspark.sql import SparkSession
from utils.db_utils import get_databricks_connection
from utils.source_utils import get_source_file_inventory


@pytest.fixture(scope="session")
def spark():
    spark_session = (
        SparkSession.builder
        .master("local[*]")
        .appName("BankingETLQA")
        .getOrCreate()
    )

    yield spark_session
    spark_session.stop()


@pytest.fixture(scope="session")
def db_connection():
    connection = get_databricks_connection()

    yield connection

    connection.close()

@pytest.fixture(scope="session")
def source_inventory(spark):

    source_path = "data/source/CARD_DAILY/2026-08-25/*.csv"

    inventory_df = get_source_file_inventory(
        spark,
        source_path
    )

    return inventory_df
import pytest
from pyspark.sql import SparkSession
from utils.db_utils import get_databricks_connection


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
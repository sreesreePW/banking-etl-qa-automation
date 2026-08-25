import pytest

pytestmark = pytest.mark.source

from pyspark.sql.functions import col
from utils.db_utils import get_single_value
from config.config import (
    BUSINESS_DATE,
    FEED_ID,
    TRANSACTIONS_TABLE
)


def test_spark_session(spark):
    assert spark is not None


def test_card_daily_source_count(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM {TRANSACTIONS_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
    """

    actual_count = get_single_value(
        db_connection,
        query
    )

    assert actual_count > 0, (
        f"No source records found for "
        f"date={BUSINESS_DATE}, feed={FEED_ID}"
    )


# Validate that at least one source file arrived
def test_source_files_received(source_inventory):

    file_count = source_inventory.count()

    assert file_count > 0, (
        "No source files received"
    )


# Validate that no source file is empty
def test_source_files_not_empty(source_inventory):

    empty_files = (
        source_inventory
        .filter(col("record_count") == 0)
        .count()
    )

    assert empty_files == 0, (
        f"Empty source files found: {empty_files}"
    )


# Display source file inventory
def test_source_file_inventory(source_inventory):

    source_inventory.show(truncate=False)

    assert source_inventory.count() > 0
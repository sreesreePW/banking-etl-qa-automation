import pytest

pytestmark = pytest.mark.data_quality

from utils.db_utils import get_single_value
from config.config import (
    BUSINESS_DATE,
    FEED_ID,
    STAGING_TABLE
)


def test_staging_duplicates(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM (
            SELECT transaction_id
            FROM {STAGING_TABLE}
            WHERE transaction_date = '{BUSINESS_DATE}'
              AND feed_id = '{FEED_ID}'
            GROUP BY transaction_id
            HAVING COUNT(*) > 1
        )
    """

    duplicate_count = get_single_value(db_connection, query)

    assert duplicate_count == 0, (
        f"Duplicate staging transactions found: {duplicate_count}"
    )


def test_staging_null_amounts(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM {STAGING_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
          AND amount IS NULL
    """

    null_count = get_single_value(db_connection, query)

    assert null_count == 0, (
        f"Null amounts found in staging: {null_count}"
    )


def test_staging_negative_amounts(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM {STAGING_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
          AND amount < 0
    """

    negative_count = get_single_value(db_connection, query)

    assert negative_count == 0, (
        f"Negative amounts found in staging: {negative_count}"
    )


def test_staging_invalid_status(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM {STAGING_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
          AND status NOT IN ('COMPLETED', 'REJECTED')
    """

    invalid_count = get_single_value(db_connection, query)

    assert invalid_count == 0, (
        f"Invalid statuses found in staging: {invalid_count}"
    )
from utils.db_utils import get_single_value
from config.config import (
    BUSINESS_DATE,
    FEED_ID,
    STAGING_TABLE
)


def test_rejected_transactions(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM {STAGING_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
          AND status = 'REJECTED'
    """

    rejected_count = get_single_value(
        db_connection,
        query
    )

    assert rejected_count >= 0


from utils.db_utils import get_single_value
from config.config import (
    BUSINESS_DATE,
    FEED_ID,
    STAGING_TABLE,
    ACCOUNT_TABLE
)


def test_expected_target_count(db_connection):

    staging_query = f"""
        SELECT COUNT(*)
        FROM {STAGING_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
    """

    rejected_query = f"""
        SELECT COUNT(*)
        FROM {STAGING_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
          AND status = 'REJECTED'
    """

    missing_account_query = f"""
        SELECT COUNT(*)
        FROM {STAGING_TABLE} s
        LEFT JOIN {ACCOUNT_TABLE} a
          ON s.account_id = a.account_id
        WHERE s.transaction_date = '{BUSINESS_DATE}'
          AND s.feed_id = '{FEED_ID}'
          AND a.account_id IS NULL
    """

    inactive_account_query = f"""
        SELECT COUNT(*)
        FROM {STAGING_TABLE} s
        JOIN {ACCOUNT_TABLE} a
          ON s.account_id = a.account_id
        WHERE s.transaction_date = '{BUSINESS_DATE}'
          AND s.feed_id = '{FEED_ID}'
          AND a.account_status <> 'ACTIVE'
    """

    staging_count = get_single_value(db_connection, staging_query)
    rejected_count = get_single_value(db_connection, rejected_query)
    missing_account_count = get_single_value(db_connection, missing_account_query)
    inactive_account_count = get_single_value(db_connection, inactive_account_query)

    expected_target_count = (
        staging_count
        - rejected_count
        - missing_account_count
        - inactive_account_count
    )

    print(f"Staging count = {staging_count}")
    print(f"Rejected count = {rejected_count}")
    print(f"Missing account count = {missing_account_count}")
    print(f"Inactive account count = {inactive_account_count}")
    print(f"Expected target count = {expected_target_count}")

    assert expected_target_count >= 0
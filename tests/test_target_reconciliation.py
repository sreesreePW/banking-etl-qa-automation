from utils.db_utils import get_single_value
from config.config import (
    BUSINESS_DATE,
    FEED_ID,
    STAGING_TABLE,
    ACCOUNT_TABLE,
    TARGET_TABLE
)


def test_expected_vs_actual_target_count(db_connection):

    expected_query = f"""
        SELECT COUNT(*)
        FROM {STAGING_TABLE} s
        JOIN {ACCOUNT_TABLE} a
          ON s.account_id = a.account_id
        WHERE s.transaction_date = '{BUSINESS_DATE}'
          AND s.feed_id = '{FEED_ID}'
          AND s.status <> 'REJECTED'
          AND a.account_status = 'ACTIVE'
    """

    actual_query = f"""
        SELECT COUNT(*)
        FROM {TARGET_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
    """

    expected_count = get_single_value(
        db_connection,
        expected_query
    )

    actual_count = get_single_value(
        db_connection,
        actual_query
    )

    print(f"Expected target count = {expected_count}")
    print(f"Actual target count = {actual_count}")

    assert expected_count == actual_count, (
        f"Target count mismatch: "
        f"expected={expected_count}, actual={actual_count}"
    )
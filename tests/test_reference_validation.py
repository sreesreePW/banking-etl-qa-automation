from utils.db_utils import get_single_value
from config.config import (
    BUSINESS_DATE,
    FEED_ID,
    STAGING_TABLE,
    ACCOUNT_TABLE
)

#missing account reference:
def test_missing_account_reference(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM {STAGING_TABLE} s
        LEFT JOIN {ACCOUNT_TABLE} a
          ON s.account_id = a.account_id
        WHERE s.transaction_date = '{BUSINESS_DATE}'
          AND s.feed_id = '{FEED_ID}'
          AND a.account_id IS NULL
    """

    missing_count = get_single_value(
        db_connection,
        query
    )

    assert missing_count == 0, (
        f"Missing account references found: {missing_count}"
    )


#inactive account validation:
def test_inactive_accounts(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM {STAGING_TABLE} s
        JOIN {ACCOUNT_TABLE} a
          ON s.account_id = a.account_id
        WHERE s.transaction_date = '{BUSINESS_DATE}'
          AND s.feed_id = '{FEED_ID}'
          AND a.account_status <> 'ACTIVE'
    """

    inactive_count = get_single_value(
        db_connection,
        query
    )

    assert inactive_count == 0, (
        f"Transactions found for inactive accounts: {inactive_count}"
    )
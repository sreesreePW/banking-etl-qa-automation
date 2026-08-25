from utils.db_utils import get_single_value
from config.config import (
    BUSINESS_DATE,
    FEED_ID,
    TRANSACTIONS_TABLE
)
from config.config import ACCOUNT_TABLE
from config.config import (
    BUSINESS_DATE,
    FEED_ID,
    TRANSACTIONS_TABLE,
    ACCOUNT_TABLE
)

def test_duplicate_transactions(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM (
            SELECT transaction_id
            FROM {TRANSACTIONS_TABLE}
            WHERE transaction_date = '{BUSINESS_DATE}'
              AND feed_id = '{FEED_ID}'
            GROUP BY transaction_id
            HAVING COUNT(*) > 1
        )
    """


##To test null amount validation
    duplicate_count = get_single_value(
        db_connection,
        query
    )

    assert duplicate_count == 0, (
        f"Duplicate transactions found: {duplicate_count}"
    )


def test_null_amounts(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM {TRANSACTIONS_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
          AND amount IS NULL
    """

    null_count = get_single_value(
        db_connection,
        query
    )

    assert null_count == 0, (
        f"Null amounts found: {null_count}"
    )

    # Test negative amount validation
def test_negative_amounts(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM {TRANSACTIONS_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
          AND amount < 0
    """

    negative_count = get_single_value(
        db_connection,
        query
    )

    assert negative_count == 0, (
        f"Negative transaction amounts found: {negative_count}"
    )

    # Test valid transaction status
def test_invalid_status(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM {TRANSACTIONS_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
          AND status NOT IN ('COMPLETED', 'REJECTED')
    """

    invalid_status_count = get_single_value(
        db_connection,
        query
    )

    assert invalid_status_count == 0, (
        f"Invalid transaction statuses found: {invalid_status_count}"
    )

    # Test missing account reference
def test_missing_account_reference(db_connection):

    query = f"""
        SELECT COUNT(*)
        FROM {TRANSACTIONS_TABLE} t
        LEFT JOIN {ACCOUNT_TABLE} a
          ON t.account_id = a.account_id
        WHERE t.transaction_date = '{BUSINESS_DATE}'
          AND t.feed_id = '{FEED_ID}'
          AND a.account_id IS NULL
    """

    missing_account_count = get_single_value(
        db_connection,
        query
    )

    assert missing_account_count == 0, (
        f"Transactions with missing account reference found: "
        f"{missing_account_count}"
    )
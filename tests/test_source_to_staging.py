from utils.db_utils import get_single_value
from config.config import (
    BUSINESS_DATE,
    FEED_ID,
    STAGING_TABLE
)


def test_source_to_staging_count(source_inventory, db_connection):

    source_count = (
        source_inventory
        .agg({"record_count": "sum"})
        .collect()[0][0]
    )

    staging_query = f"""
        SELECT COUNT(*)
        FROM {STAGING_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
    """

    staging_count = get_single_value(
        db_connection,
        staging_query
    )

    print(f"Source count = {source_count}")
    print(f"Staging count = {staging_count}")

    assert source_count == staging_count, (
        f"Source-to-staging count mismatch: "
        f"source={source_count}, staging={staging_count}"
    )

from pyspark.sql.functions import col
from utils.db_utils import get_single_value
from config.config import (
    BUSINESS_DATE,
    FEED_ID,
    STAGING_TABLE
)

##The first check should be source-only records: rows that exist in the source files but are missing from staging.
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


def test_source_only_records(spark, db_connection):

    source_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/source/CARD_DAILY/2026-08-25/*.csv")
    )

    staging_query = """
        SELECT
            transaction_id,
            customer_id,
            account_id,
            transaction_date,
            feed_id,
            transaction_type,
            amount,
            status,
            update_timestamp
        FROM workspace.banking_etl_qa.stg_transactions
        WHERE transaction_date = '2026-08-25'
          AND feed_id = 'CARD_DAILY'
    """

    cursor = db_connection.cursor()
    cursor.execute(staging_query)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()

    staging_df = spark.createDataFrame(
        [tuple(row) for row in rows],
        schema=columns
    )

    source_only_df = source_df.join(
        staging_df,
        on="transaction_id",
        how="left_anti"
    )

    source_only_count = source_only_df.count()

    source_only_df.show(truncate=False)

    assert source_only_count == 0, (
        f"Source records missing in staging: {source_only_count}"
    )

# Add the reverse check for staging-only records
def test_staging_only_records(spark, db_connection):

    source_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/source/CARD_DAILY/2026-08-25/*.csv")
    )

    staging_query = """
        SELECT
            transaction_id,
            customer_id,
            account_id,
            transaction_date,
            feed_id,
            transaction_type,
            amount,
            status,
            update_timestamp
        FROM workspace.banking_etl_qa.stg_transactions
        WHERE transaction_date = '2026-08-25'
          AND feed_id = 'CARD_DAILY'
    """

    cursor = db_connection.cursor()
    cursor.execute(staging_query)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()

    staging_df = spark.createDataFrame(
        [tuple(row) for row in rows],
        schema=columns
    )

    staging_only_df = staging_df.join(
        source_df,
        on="transaction_id",
        how="left_anti"
    )

    staging_only_count = staging_only_df.count()

    staging_only_df.show(truncate=False)


    assert staging_only_count == 0, (
        f"Unexpected staging-only records found: {staging_only_count}"
    )


#field-level mismatch test
def test_source_to_staging_field_mismatch(spark, db_connection):

    source_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/source/CARD_DAILY/2026-08-25/*.csv")
    )

    staging_query = """
        SELECT
            transaction_id,
            customer_id,
            account_id,
            transaction_date,
            feed_id,
            transaction_type,
            amount,
            status,
            update_timestamp
        FROM workspace.banking_etl_qa.stg_transactions
        WHERE transaction_date = '2026-08-25'
          AND feed_id = 'CARD_DAILY'
    """

    cursor = db_connection.cursor()
    cursor.execute(staging_query)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()

    staging_df = spark.createDataFrame(
        [tuple(row) for row in rows],
        schema=columns
    )

    joined_df = source_df.alias("s").join(
        staging_df.alias("t"),
        col("s.transaction_id") == col("t.transaction_id"),
        "inner"
    )

    mismatch_df = joined_df.filter(
        (col("s.customer_id") != col("t.customer_id")) |
        (col("s.account_id") != col("t.account_id")) |
        (col("s.amount") != col("t.amount")) |
        (col("s.status") != col("t.status")) |
        (col("s.transaction_type") != col("t.transaction_type"))
    )

    mismatch_count = mismatch_df.count()

    mismatch_df.select(
        col("s.transaction_id").alias("transaction_id"),
        col("s.amount").alias("source_amount"),
        col("t.amount").alias("staging_amount"),
        col("s.status").alias("source_status"),
        col("t.status").alias("staging_status")
    ).show(truncate=False)

    assert mismatch_count == 0, (
        f"Source-to-staging field mismatches found: {mismatch_count}"
    )
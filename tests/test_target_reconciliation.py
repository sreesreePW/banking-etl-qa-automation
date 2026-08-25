from pyspark.sql.functions import col
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

#expected-records-missing-from-target

def test_expected_records_missing_from_target(spark, db_connection):

    expected_query = f"""
        SELECT s.transaction_id
        FROM {STAGING_TABLE} s
        JOIN {ACCOUNT_TABLE} a
          ON s.account_id = a.account_id
        WHERE s.transaction_date = '{BUSINESS_DATE}'
          AND s.feed_id = '{FEED_ID}'
          AND s.status <> 'REJECTED'
          AND a.account_status = 'ACTIVE'
    """

    target_query = f"""
        SELECT transaction_id
        FROM {TARGET_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
    """

    cursor = db_connection.cursor()

    cursor.execute(expected_query)
    expected_rows = cursor.fetchall()

    cursor.execute(target_query)
    target_rows = cursor.fetchall()

    cursor.close()

    expected_df = spark.createDataFrame(
        [(row[0],) for row in expected_rows],
        ["transaction_id"]
    )

    target_df = spark.createDataFrame(
        [(row[0],) for row in target_rows],
        ["transaction_id"]
    )

    missing_target_df = expected_df.join(
        target_df,
        on="transaction_id",
        how="left_anti"
    )

    missing_count = missing_target_df.count()

    missing_target_df.show(truncate=False)

    assert missing_count == 0, (
        f"Expected records missing from target: {missing_count}"
    )

#Are there any unexpected records in target that should not be there?
def test_unexpected_target_only_records(spark, db_connection):

    expected_query = f"""
        SELECT s.transaction_id
        FROM {STAGING_TABLE} s
        JOIN {ACCOUNT_TABLE} a
          ON s.account_id = a.account_id
        WHERE s.transaction_date = '{BUSINESS_DATE}'
          AND s.feed_id = '{FEED_ID}'
          AND s.status <> 'REJECTED'
          AND a.account_status = 'ACTIVE'
    """

    target_query = f"""
        SELECT transaction_id
        FROM {TARGET_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
    """

    cursor = db_connection.cursor()

    cursor.execute(expected_query)
    expected_rows = cursor.fetchall()

    cursor.execute(target_query)
    target_rows = cursor.fetchall()

    cursor.close()

    expected_df = spark.createDataFrame(
        [(row[0],) for row in expected_rows],
        ["transaction_id"]
    )

    target_df = spark.createDataFrame(
        [(row[0],) for row in target_rows],
        ["transaction_id"]
    )

    target_only_df = target_df.join(
        expected_df,
        on="transaction_id",
        how="left_anti"
    )

    target_only_count = target_only_df.count()

    target_only_df.show(truncate=False)

    assert target_only_count == 0, (
        f"Unexpected target-only records found: {target_only_count}"
    )

#field-level target reconciliation test
def test_target_field_mismatches(spark, db_connection):

    expected_query = f"""
        SELECT
            s.transaction_id,
            s.customer_id,
            s.account_id,
            s.transaction_date,
            s.feed_id,
            s.transaction_type,
            s.amount
        FROM {STAGING_TABLE} s
        JOIN {ACCOUNT_TABLE} a
          ON s.account_id = a.account_id
        WHERE s.transaction_date = '{BUSINESS_DATE}'
          AND s.feed_id = '{FEED_ID}'
          AND s.status <> 'REJECTED'
          AND a.account_status = 'ACTIVE'
    """

    target_query = f"""
        SELECT
            transaction_id,
            customer_id,
            account_id,
            transaction_date,
            feed_id,
            transaction_type,
            amount
        FROM {TARGET_TABLE}
        WHERE transaction_date = '{BUSINESS_DATE}'
          AND feed_id = '{FEED_ID}'
    """

    cursor = db_connection.cursor()

    cursor.execute(expected_query)
    expected_rows = cursor.fetchall()
    expected_columns = [desc[0] for desc in cursor.description]

    cursor.execute(target_query)
    target_rows = cursor.fetchall()
    target_columns = [desc[0] for desc in cursor.description]

    cursor.close()

    expected_df = spark.createDataFrame(
        [tuple(row) for row in expected_rows],
        schema=expected_columns
    )

    target_df = spark.createDataFrame(
        [tuple(row) for row in target_rows],
        schema=target_columns
    )

    joined_df = expected_df.alias("e").join(
        target_df.alias("t"),
        col("e.transaction_id") == col("t.transaction_id"),
        "inner"
    )

    mismatch_df = joined_df.filter(
        (col("e.customer_id") != col("t.customer_id")) |
        (col("e.account_id") != col("t.account_id")) |
        (col("e.transaction_date") != col("t.transaction_date")) |
        (col("e.feed_id") != col("t.feed_id")) |
        (col("e.transaction_type") != col("t.transaction_type")) |
        (col("e.amount") != col("t.amount"))
    )

    mismatch_count = mismatch_df.count()

    mismatch_df.select(
        col("e.transaction_id").alias("transaction_id"),
        col("e.amount").alias("expected_amount"),
        col("t.amount").alias("target_amount"),
        col("e.account_id").alias("expected_account"),
        col("t.account_id").alias("target_account"),
        col("e.transaction_type").alias("expected_type"),
        col("t.transaction_type").alias("target_type")
    ).show(truncate=False)

    assert mismatch_count == 0, (
        f"Target field mismatches found: {mismatch_count}"
    )
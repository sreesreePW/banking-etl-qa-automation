def test_databricks_transaction_count(db_connection):

    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM workspace.banking_etl_qa.transactions
    """)

    actual_count = cursor.fetchone()[0]

    cursor.close()

    assert actual_count == 16
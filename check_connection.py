from utils.db_utils import get_databricks_connection


with get_databricks_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*)
            FROM workspace.banking_etl_qa.transactions
        """)

        result = cursor.fetchone()
        print("Transaction count =", result[0])
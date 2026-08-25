from databricks import sql
from config.config import (
    DATABRICKS_SERVER_HOSTNAME,
    DATABRICKS_HTTP_PATH,
    DATABRICKS_TOKEN
)


def get_databricks_connection():
    return sql.connect(
        server_hostname=DATABRICKS_SERVER_HOSTNAME,
        http_path=DATABRICKS_HTTP_PATH,
        access_token=DATABRICKS_TOKEN
    )


def get_single_value(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    value = cursor.fetchone()[0]
    cursor.close()
    return value
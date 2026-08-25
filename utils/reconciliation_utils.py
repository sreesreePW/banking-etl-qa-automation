from pyspark.sql.functions import col


def query_to_spark_df(spark, connection, query):

    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()

    return spark.createDataFrame(
        [tuple(row) for row in rows],
        schema=columns
    )


def find_source_only(source_df, target_df, key_column):

    return source_df.join(
        target_df,
        on=key_column,
        how="left_anti"
    )


def find_target_only(source_df, target_df, key_column):

    return target_df.join(
        source_df,
        on=key_column,
        how="left_anti"
    )



from pyspark.sql.functions import col, count


def get_source_file_inventory(spark, source_path):

    source_df = (
        spark.read
        .option("header", True)
        .csv(source_path)
        .select(
            "*",
            col("_metadata.file_name").alias("file_name"),
            col("_metadata.file_modification_time").alias("file_date")
        )
    )

    inventory_df = (
        source_df
        .groupBy("file_name", "file_date")
        .agg(
            count("*").alias("record_count")
        )
    )

    return inventory_df
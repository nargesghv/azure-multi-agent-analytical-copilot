from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

customers = spark.table("silver.customers_clean")
features = spark.table("silver.extracted_signals")

joined = customers.join(features, on="customer_id", how="left")

joined.write.format("delta").mode("overwrite").saveAsTable(
    "gold.customer_360_features"
)
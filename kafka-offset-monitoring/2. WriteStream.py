# Databricks notebook source
# MAGIC %md
# MAGIC ### Run Init script for variables

# COMMAND ----------

# MAGIC %run "./0. Init"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Datagen
# MAGIC This Datagen script will generate `row_count` number of rows that are just random `float` type numbers. We will use this for writing offsets into Kafka.

# COMMAND ----------

import dbldatagen as dg
from pyspark.sql.types import FloatType, IntegerType, StringType

def buildDataset(row_count):
  dataset = (dg.DataGenerator(spark, name="test_data_set1", rows=row_count,
                                    partitions=1, randomSeedMethod='hash_fieldname', 
                                    verbose=True)
                     .withColumn("r", FloatType(), expr="floor(rand() * 350) * (86400 + 3600)",
                                      numColumns=1)
                     )
  return dataset.build()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Topics
# MAGIC We will be using 3 topics.
# MAGIC * Small  - This topic is ingesting at 100 tps.
# MAGIC * Medium - This topic is ingesting at 3500 tps.
# MAGIC * High   - This topic is ingesting at 10000 tps with a 50000 tps spike.

# COMMAND ----------

def writeData(i=0):
  dfSmall = buildDataset(100)
  dfMedium = buildDataset(3500)
  if (i%5 == 0):
    dfHigh = buildDataset(50000)
  else:
    dfHigh = buildDataset(10000)

  (dfSmall.write
  .format("delta")
  .mode("append")
  .option("path", f"dbfs:/datasets/kakfa_offsets_demo/{topics['small']}")
  .saveAsTable(topics['small']))

  (dfMedium.write
  .format("delta")
  .mode("append")
  .option("path", f"dbfs:/datasets/kakfa_offsets_demo/{topics['medium']}")
  .saveAsTable(topics['medium']))

  (dfHigh.write
  .format("delta")
  .mode("append")
  .option("path", f"dbfs:/datasets/kakfa_offsets_demo/{topics['high']}")
  .saveAsTable(topics['high']))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Table Creation & Initial Data
# MAGIC We will be writing this data into a Delta table. This intial call will create the table with some initial data.

# COMMAND ----------

writeData()

# COMMAND ----------

# MAGIC %md
# MAGIC ### ReadStream from Delta & WriteStream into Kafka

# COMMAND ----------

for t in topics:
  ds = (spark.readStream
        .format("delta")
        .table(topics[t]))

  (ds.selectExpr("CAST(r as STRING) as value") 
    .writeStream 
    .format("kafka")
    .option("kafka.bootstrap.servers", bootstrap_servers)
    .option("topic", topics[t])
    .queryName(t + "_read")
    .option('checkpointLocation', f"dbfs:/datasets/{topics[t]}/_checkpoint/") 
    .start())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Run this command to generate data

# COMMAND ----------

for i in range(5):
  writeData(i)

# COMMAND ----------


# Databricks notebook source
# MAGIC %md
# MAGIC ### Run Init script for variables

# COMMAND ----------

# MAGIC %run "./0. Init"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Streams Monitoring
# MAGIC We will be using the `StreamingQueryListener` to track the progress of our streams by exporting the progress metrics into an external monitoring tool. The tool we will use is Prometheus in this case, that will then do remote writes to our Grafana Cloud server which we will then display the progress dashboards on.
# MAGIC 
# MAGIC We leverage the `onQueryProgress` event to publish metrics every time each of the streams make any progress in batches.
# MAGIC 
# MAGIC The `pushgateway` is being used here. We will append all the metrics we want to capture into a string with each metrics separated by a `\n` newline character. The metrics will be pushed by sending a POST request to the gateway. 
# MAGIC 
# MAGIC https://github.com/prometheus/pushgateway#command-line

# COMMAND ----------

from pyspark.sql.streaming import StreamingQueryListener
import requests, json
from datetime import datetime

def publishMetrics(progress):
    stream_name = progress["name"]
    data = ""
    
    progress["timestamp"] = int(
        datetime.strptime(
            progress["timestamp"], '%Y-%m-%dT%H:%M:%S.%fZ'
        ).timestamp()
        * 1000
    )

    metrics = [
        "inputRowsPerSecond",
        "processedRowsPerSecond",
        "numInputRows",
        "timestamp",
        "batchId",
    ]
    
    for m in metrics:
        data += "{k} {v}\n".format(k=m, v=progress[m])
        
    lagMetrics = progress['sources'][0]['metrics']
    for m in lagMetrics:
        data += "{k} {v}\n".format(k=m, v=lagMetrics[m])
        
    durationMs = progress['durationMs']
    for m in durationMs:
        data += "{k} {v}\n".format(k=m, v=durationMs[m])
        
    startOffsets = progress['sources'][0]['startOffset']
    for t in startOffsets:
        topic = t
        for p in progress['sources'][0]['startOffset'][t]:
            partition = p
            data += "{k}{{partition=\"{p}\"}} {v}\n".format(p=p, k="startOffset", v=progress['sources'][0]['startOffset'][t][p])

    latestOffsets = progress['sources'][0]['latestOffset']
    for t in latestOffsets:
        topic = t
        for p in progress['sources'][0]['latestOffset'][t]:
            partition = p
            data += "{k}{{partition=\"{p}\"}} {v}\n".format(p=p, k="latestOffset", v=progress['sources'][0]['latestOffset'][t][p])
    
    requests.post(
        "http://{h}:9091/metrics/job/{j}/topic/{t}".format(
            h=host, j=job_name, t=stream_name
        ),
        data=data
    )


# Define my listener.
# spark.streams.removeListener(my_listener)
class MyListener(StreamingQueryListener):
    def onQueryStarted(self, event):
        print(f"'{event.name}' [{event.id}] got started!")

    def onQueryProgress(self, event):
        try:
            progress = json.loads(event.progress.prettyJson)
            publishMetrics(progress)
        except Exception as e:
            print(e)


    def onQueryTerminated(self, event):
        print(event)
        print(f"{event.id} got terminated!")

# Add my listener.
my_listener = MyListener()
spark.streams.addListener(my_listener)

# COMMAND ----------

# MAGIC %md
# MAGIC ### ReadStream from Kafka & Write to Console
# MAGIC We are now reading the same topics from Kafka and writing to the Console.

# COMMAND ----------

from pyspark.sql.functions import *

for t in topics:
    kafkaStreamDF = (
      spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", topics[t])
        .option("maxOffsetsPerTrigger", 500)
        .option("startingOffsets", "earliest")
        .option("failOnDataLoss","FALSE")
        .load()
        .withWatermark("timestamp", "10 seconds")
        .groupBy("topic", window("timestamp", "1 minutes"))
        .agg(
            max("timestamp").alias("max_publish_ts"),
            count("*").alias("cnt"))
        .select("topic", "cnt", col("window.start").alias("window_start_ts"), "max_publish_ts")
        .writeStream 
        .format("console") 
        .queryName(t + "_read")
        .option("checkpointLocation", f"dbfs:/datasets/{topics[t]}/write_console/_checkpoint/")
        .start()
      )

# COMMAND ----------


# Databricks notebook source
bootstrap_servers = "" # example-bootstrap-server.com:9092
host = "" # example-prometheus-pushgateway.com
job_name = "kafka_offsets_demo"

# COMMAND ----------

topics = {
  "small": "kafka_offsets_demo_small",
  "medium": "kafka_offsets_demo_medium",
  "high": "kafka_offsets_demo_high"
}
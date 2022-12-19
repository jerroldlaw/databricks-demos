# Databricks notebook source
# MAGIC %md
# MAGIC ## EC2
# MAGIC Spin up a `t2.medium` on an **Amazon Linux 2** OS EC2.
# MAGIC 
# MAGIC ## Docker CE Install
# MAGIC 
# MAGIC ```sh
# MAGIC sudo yum install docker
# MAGIC sudo service docker start
# MAGIC sudo usermod -a -G docker ec2-user
# MAGIC ```
# MAGIC 
# MAGIC ## docker-compose install
# MAGIC 
# MAGIC Copy the appropriate `docker-compose` binary from GitHub:
# MAGIC `sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose`
# MAGIC 
# MAGIC Fix permissions after download: 
# MAGIC 
# MAGIC `sudo chmod +x /usr/local/bin/docker-compose`
# MAGIC 
# MAGIC Verify success: 
# MAGIC 
# MAGIC `docker-compose version`

# COMMAND ----------

# MAGIC %md
# MAGIC # Prometheus + Prometheus PushGateway
# MAGIC Make a directory `prometheus` in your home folder.
# MAGIC ```
# MAGIC mkdir prometheus
# MAGIC cd prometheus
# MAGIC ```
# MAGIC ## Docker Compose File
# MAGIC vi docker-compose.yml
# MAGIC ```
# MAGIC version: '3.3'
# MAGIC 
# MAGIC volumes:
# MAGIC   prometheus_data: {}
# MAGIC 
# MAGIC services:
# MAGIC   prometheus:
# MAGIC     image: prom/prometheus:latest
# MAGIC     container_name: prometheus
# MAGIC     restart: unless-stopped
# MAGIC     volumes:
# MAGIC       - ./prometheus.yml:/etc/prometheus/prometheus.yml
# MAGIC       - prometheus_data:/prometheus
# MAGIC     command:
# MAGIC       - '--config.file=/etc/prometheus/prometheus.yml'
# MAGIC       - '--storage.tsdb.path=/prometheus'
# MAGIC       - '--web.console.libraries=/etc/prometheus/console_libraries'
# MAGIC       - '--web.console.templates=/etc/prometheus/consoles'
# MAGIC       - '--web.enable-lifecycle'
# MAGIC     expose:
# MAGIC       - 9090
# MAGIC     ports:
# MAGIC       - "9090:9090"
# MAGIC 
# MAGIC   pushgateway:
# MAGIC     image: prom/pushgateway:latest
# MAGIC     container_name: pushgateway
# MAGIC     restart: unless-stopped
# MAGIC     expose:
# MAGIC       - 9091
# MAGIC     ports:
# MAGIC       - "9091:9091"
# MAGIC ```
# MAGIC 
# MAGIC ## Prometheus Config
# MAGIC vi prometheus.yml
# MAGIC ```
# MAGIC global:
# MAGIC   scrape_interval: 1m
# MAGIC 
# MAGIC scrape_configs:
# MAGIC   - job_name: "pushgateway"
# MAGIC     honor_labels: true
# MAGIC     static_configs:
# MAGIC       - targets: ['pushgateway:9091']
# MAGIC 
# MAGIC remote_write:
# MAGIC   - url: https://zzz.grafana.net/api/prom/push
# MAGIC     basic_auth:
# MAGIC       username: yyy
# MAGIC       password: xxx==
# MAGIC ```
# MAGIC 
# MAGIC ## Run Docker Compose
# MAGIC ```
# MAGIC docker-compose up -d
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC # Grafana Dashboard JSON
# MAGIC ```
# MAGIC {
# MAGIC   "annotations": {
# MAGIC     "list": [
# MAGIC       {
# MAGIC         "builtIn": 1,
# MAGIC         "datasource": {
# MAGIC           "type": "grafana",
# MAGIC           "uid": "-- Grafana --"
# MAGIC         },
# MAGIC         "enable": true,
# MAGIC         "hide": true,
# MAGIC         "iconColor": "rgba(0, 211, 255, 1)",
# MAGIC         "name": "Annotations & Alerts",
# MAGIC         "target": {
# MAGIC           "limit": 100,
# MAGIC           "matchAny": false,
# MAGIC           "tags": [],
# MAGIC           "type": "dashboard"
# MAGIC         },
# MAGIC         "type": "dashboard"
# MAGIC       }
# MAGIC     ]
# MAGIC   },
# MAGIC   "editable": true,
# MAGIC   "fiscalYearStartMonth": 0,
# MAGIC   "graphTooltip": 0,
# MAGIC   "id": 21,
# MAGIC   "links": [],
# MAGIC   "liveNow": false,
# MAGIC   "panels": [
# MAGIC     {
# MAGIC       "datasource": {
# MAGIC         "type": "prometheus",
# MAGIC         "uid": "grafanacloud-prom"
# MAGIC       },
# MAGIC       "fieldConfig": {
# MAGIC         "defaults": {
# MAGIC           "color": {
# MAGIC             "mode": "thresholds"
# MAGIC           },
# MAGIC           "mappings": [],
# MAGIC           "thresholds": {
# MAGIC             "mode": "absolute",
# MAGIC             "steps": [
# MAGIC               {
# MAGIC                 "color": "green",
# MAGIC                 "value": null
# MAGIC               }
# MAGIC             ]
# MAGIC           }
# MAGIC         },
# MAGIC         "overrides": []
# MAGIC       },
# MAGIC       "gridPos": {
# MAGIC         "h": 8,
# MAGIC         "w": 24,
# MAGIC         "x": 0,
# MAGIC         "y": 0
# MAGIC       },
# MAGIC       "id": 4,
# MAGIC       "options": {
# MAGIC         "colorMode": "value",
# MAGIC         "graphMode": "none",
# MAGIC         "justifyMode": "auto",
# MAGIC         "orientation": "auto",
# MAGIC         "reduceOptions": {
# MAGIC           "calcs": [
# MAGIC             "lastNotNull"
# MAGIC           ],
# MAGIC           "fields": "",
# MAGIC           "values": false
# MAGIC         },
# MAGIC         "textMode": "auto"
# MAGIC       },
# MAGIC       "pluginVersion": "9.3.2-45365",
# MAGIC       "targets": [
# MAGIC         {
# MAGIC           "datasource": {
# MAGIC             "type": "prometheus",
# MAGIC             "uid": "grafanacloud-prom"
# MAGIC           },
# MAGIC           "editorMode": "builder",
# MAGIC           "expr": "batchId{job=\"$job\", topic=~\"$topic\"}",
# MAGIC           "legendFormat": "__auto",
# MAGIC           "range": true,
# MAGIC           "refId": "A"
# MAGIC         }
# MAGIC       ],
# MAGIC       "title": "Batch ID",
# MAGIC       "type": "stat"
# MAGIC     },
# MAGIC     {
# MAGIC       "datasource": {
# MAGIC         "type": "prometheus",
# MAGIC         "uid": "grafanacloud-prom"
# MAGIC       },
# MAGIC       "fieldConfig": {
# MAGIC         "defaults": {
# MAGIC           "color": {
# MAGIC             "mode": "palette-classic"
# MAGIC           },
# MAGIC           "custom": {
# MAGIC             "axisCenteredZero": false,
# MAGIC             "axisColorMode": "text",
# MAGIC             "axisGridShow": false,
# MAGIC             "axisLabel": "",
# MAGIC             "axisPlacement": "auto",
# MAGIC             "barAlignment": 0,
# MAGIC             "drawStyle": "line",
# MAGIC             "fillOpacity": 0,
# MAGIC             "gradientMode": "none",
# MAGIC             "hideFrom": {
# MAGIC               "legend": false,
# MAGIC               "tooltip": false,
# MAGIC               "viz": false
# MAGIC             },
# MAGIC             "lineInterpolation": "smooth",
# MAGIC             "lineWidth": 1,
# MAGIC             "pointSize": 5,
# MAGIC             "scaleDistribution": {
# MAGIC               "log": 10,
# MAGIC               "type": "log"
# MAGIC             },
# MAGIC             "showPoints": "auto",
# MAGIC             "spanNulls": false,
# MAGIC             "stacking": {
# MAGIC               "group": "A",
# MAGIC               "mode": "none"
# MAGIC             },
# MAGIC             "thresholdsStyle": {
# MAGIC               "mode": "off"
# MAGIC             }
# MAGIC           },
# MAGIC           "mappings": [],
# MAGIC           "thresholds": {
# MAGIC             "mode": "absolute",
# MAGIC             "steps": [
# MAGIC               {
# MAGIC                 "color": "green",
# MAGIC                 "value": null
# MAGIC               },
# MAGIC               {
# MAGIC                 "color": "red",
# MAGIC                 "value": 80
# MAGIC               }
# MAGIC             ]
# MAGIC           }
# MAGIC         },
# MAGIC         "overrides": []
# MAGIC       },
# MAGIC       "gridPos": {
# MAGIC         "h": 12,
# MAGIC         "w": 12,
# MAGIC         "x": 0,
# MAGIC         "y": 8
# MAGIC       },
# MAGIC       "id": 6,
# MAGIC       "options": {
# MAGIC         "legend": {
# MAGIC           "calcs": [],
# MAGIC           "displayMode": "list",
# MAGIC           "placement": "bottom",
# MAGIC           "showLegend": true
# MAGIC         },
# MAGIC         "tooltip": {
# MAGIC           "mode": "single",
# MAGIC           "sort": "none"
# MAGIC         }
# MAGIC       },
# MAGIC       "targets": [
# MAGIC         {
# MAGIC           "datasource": {
# MAGIC             "type": "prometheus",
# MAGIC             "uid": "grafanacloud-prom"
# MAGIC           },
# MAGIC           "editorMode": "builder",
# MAGIC           "expr": "inputRowsPerSecond{job=\"$job\", topic=~\"$topic\"}",
# MAGIC           "legendFormat": "__auto",
# MAGIC           "range": true,
# MAGIC           "refId": "A"
# MAGIC         }
# MAGIC       ],
# MAGIC       "title": "Input Rows / Second",
# MAGIC       "type": "timeseries"
# MAGIC     },
# MAGIC     {
# MAGIC       "datasource": {
# MAGIC         "type": "prometheus",
# MAGIC         "uid": "grafanacloud-prom"
# MAGIC       },
# MAGIC       "fieldConfig": {
# MAGIC         "defaults": {
# MAGIC           "color": {
# MAGIC             "mode": "palette-classic"
# MAGIC           },
# MAGIC           "custom": {
# MAGIC             "axisCenteredZero": false,
# MAGIC             "axisColorMode": "text",
# MAGIC             "axisGridShow": false,
# MAGIC             "axisLabel": "",
# MAGIC             "axisPlacement": "auto",
# MAGIC             "barAlignment": 0,
# MAGIC             "drawStyle": "line",
# MAGIC             "fillOpacity": 0,
# MAGIC             "gradientMode": "none",
# MAGIC             "hideFrom": {
# MAGIC               "legend": false,
# MAGIC               "tooltip": false,
# MAGIC               "viz": false
# MAGIC             },
# MAGIC             "lineInterpolation": "smooth",
# MAGIC             "lineWidth": 1,
# MAGIC             "pointSize": 5,
# MAGIC             "scaleDistribution": {
# MAGIC               "log": 10,
# MAGIC               "type": "log"
# MAGIC             },
# MAGIC             "showPoints": "auto",
# MAGIC             "spanNulls": false,
# MAGIC             "stacking": {
# MAGIC               "group": "A",
# MAGIC               "mode": "none"
# MAGIC             },
# MAGIC             "thresholdsStyle": {
# MAGIC               "mode": "off"
# MAGIC             }
# MAGIC           },
# MAGIC           "mappings": [],
# MAGIC           "thresholds": {
# MAGIC             "mode": "absolute",
# MAGIC             "steps": [
# MAGIC               {
# MAGIC                 "color": "green",
# MAGIC                 "value": null
# MAGIC               },
# MAGIC               {
# MAGIC                 "color": "red",
# MAGIC                 "value": 80
# MAGIC               }
# MAGIC             ]
# MAGIC           }
# MAGIC         },
# MAGIC         "overrides": []
# MAGIC       },
# MAGIC       "gridPos": {
# MAGIC         "h": 12,
# MAGIC         "w": 12,
# MAGIC         "x": 12,
# MAGIC         "y": 8
# MAGIC       },
# MAGIC       "id": 8,
# MAGIC       "options": {
# MAGIC         "legend": {
# MAGIC           "calcs": [],
# MAGIC           "displayMode": "list",
# MAGIC           "placement": "bottom",
# MAGIC           "showLegend": true
# MAGIC         },
# MAGIC         "tooltip": {
# MAGIC           "mode": "single",
# MAGIC           "sort": "none"
# MAGIC         }
# MAGIC       },
# MAGIC       "targets": [
# MAGIC         {
# MAGIC           "datasource": {
# MAGIC             "type": "prometheus",
# MAGIC             "uid": "grafanacloud-prom"
# MAGIC           },
# MAGIC           "editorMode": "builder",
# MAGIC           "expr": "processedRowsPerSecond{job=\"$job\", topic=~\"$topic\"}",
# MAGIC           "legendFormat": "__auto",
# MAGIC           "range": true,
# MAGIC           "refId": "A"
# MAGIC         }
# MAGIC       ],
# MAGIC       "title": "Processed Rows / Second",
# MAGIC       "type": "timeseries"
# MAGIC     },
# MAGIC     {
# MAGIC       "datasource": {
# MAGIC         "type": "prometheus",
# MAGIC         "uid": "grafanacloud-prom"
# MAGIC       },
# MAGIC       "fieldConfig": {
# MAGIC         "defaults": {
# MAGIC           "color": {
# MAGIC             "mode": "palette-classic"
# MAGIC           },
# MAGIC           "custom": {
# MAGIC             "axisCenteredZero": false,
# MAGIC             "axisColorMode": "text",
# MAGIC             "axisGridShow": false,
# MAGIC             "axisLabel": "",
# MAGIC             "axisPlacement": "auto",
# MAGIC             "barAlignment": 0,
# MAGIC             "drawStyle": "bars",
# MAGIC             "fillOpacity": 6,
# MAGIC             "gradientMode": "none",
# MAGIC             "hideFrom": {
# MAGIC               "legend": false,
# MAGIC               "tooltip": false,
# MAGIC               "viz": false
# MAGIC             },
# MAGIC             "lineInterpolation": "linear",
# MAGIC             "lineWidth": 2,
# MAGIC             "pointSize": 5,
# MAGIC             "scaleDistribution": {
# MAGIC               "log": 10,
# MAGIC               "type": "log"
# MAGIC             },
# MAGIC             "showPoints": "auto",
# MAGIC             "spanNulls": false,
# MAGIC             "stacking": {
# MAGIC               "group": "A",
# MAGIC               "mode": "none"
# MAGIC             },
# MAGIC             "thresholdsStyle": {
# MAGIC               "mode": "off"
# MAGIC             }
# MAGIC           },
# MAGIC           "mappings": [],
# MAGIC           "thresholds": {
# MAGIC             "mode": "absolute",
# MAGIC             "steps": [
# MAGIC               {
# MAGIC                 "color": "green",
# MAGIC                 "value": null
# MAGIC               },
# MAGIC               {
# MAGIC                 "color": "red",
# MAGIC                 "value": 80
# MAGIC               }
# MAGIC             ]
# MAGIC           }
# MAGIC         },
# MAGIC         "overrides": []
# MAGIC       },
# MAGIC       "gridPos": {
# MAGIC         "h": 10,
# MAGIC         "w": 24,
# MAGIC         "x": 0,
# MAGIC         "y": 20
# MAGIC       },
# MAGIC       "id": 10,
# MAGIC       "options": {
# MAGIC         "legend": {
# MAGIC           "calcs": [],
# MAGIC           "displayMode": "list",
# MAGIC           "placement": "bottom",
# MAGIC           "showLegend": true
# MAGIC         },
# MAGIC         "tooltip": {
# MAGIC           "mode": "single",
# MAGIC           "sort": "none"
# MAGIC         }
# MAGIC       },
# MAGIC       "targets": [
# MAGIC         {
# MAGIC           "datasource": {
# MAGIC             "type": "prometheus",
# MAGIC             "uid": "grafanacloud-prom"
# MAGIC           },
# MAGIC           "editorMode": "builder",
# MAGIC           "expr": "numInputRows{job=\"$job\", topic=~\"$topic\"}",
# MAGIC           "legendFormat": "__auto",
# MAGIC           "range": true,
# MAGIC           "refId": "A"
# MAGIC         }
# MAGIC       ],
# MAGIC       "title": "Num Input Rows",
# MAGIC       "type": "timeseries"
# MAGIC     },
# MAGIC     {
# MAGIC       "datasource": {
# MAGIC         "type": "prometheus",
# MAGIC         "uid": "grafanacloud-prom"
# MAGIC       },
# MAGIC       "fieldConfig": {
# MAGIC         "defaults": {
# MAGIC           "color": {
# MAGIC             "fixedColor": "red",
# MAGIC             "mode": "fixed"
# MAGIC           },
# MAGIC           "custom": {
# MAGIC             "axisCenteredZero": false,
# MAGIC             "axisColorMode": "text",
# MAGIC             "axisLabel": "",
# MAGIC             "axisPlacement": "auto",
# MAGIC             "barAlignment": 0,
# MAGIC             "drawStyle": "line",
# MAGIC             "fillOpacity": 7,
# MAGIC             "gradientMode": "opacity",
# MAGIC             "hideFrom": {
# MAGIC               "legend": false,
# MAGIC               "tooltip": false,
# MAGIC               "viz": false
# MAGIC             },
# MAGIC             "lineInterpolation": "smooth",
# MAGIC             "lineWidth": 1,
# MAGIC             "pointSize": 5,
# MAGIC             "scaleDistribution": {
# MAGIC               "type": "linear"
# MAGIC             },
# MAGIC             "showPoints": "auto",
# MAGIC             "spanNulls": false,
# MAGIC             "stacking": {
# MAGIC               "group": "A",
# MAGIC               "mode": "none"
# MAGIC             },
# MAGIC             "thresholdsStyle": {
# MAGIC               "mode": "off"
# MAGIC             }
# MAGIC           },
# MAGIC           "mappings": [],
# MAGIC           "thresholds": {
# MAGIC             "mode": "absolute",
# MAGIC             "steps": [
# MAGIC               {
# MAGIC                 "color": "green",
# MAGIC                 "value": null
# MAGIC               },
# MAGIC               {
# MAGIC                 "color": "red",
# MAGIC                 "value": 80
# MAGIC               }
# MAGIC             ]
# MAGIC           }
# MAGIC         },
# MAGIC         "overrides": [
# MAGIC           {
# MAGIC             "matcher": {
# MAGIC               "id": "byFrameRefID",
# MAGIC               "options": "A"
# MAGIC             },
# MAGIC             "properties": [
# MAGIC               {
# MAGIC                 "id": "color",
# MAGIC                 "value": {
# MAGIC                   "fixedColor": "blue",
# MAGIC                   "mode": "fixed"
# MAGIC                 }
# MAGIC               }
# MAGIC             ]
# MAGIC           }
# MAGIC         ]
# MAGIC       },
# MAGIC       "gridPos": {
# MAGIC         "h": 13,
# MAGIC         "w": 12,
# MAGIC         "x": 0,
# MAGIC         "y": 30
# MAGIC       },
# MAGIC       "id": 12,
# MAGIC       "options": {
# MAGIC         "legend": {
# MAGIC           "calcs": [],
# MAGIC           "displayMode": "list",
# MAGIC           "placement": "bottom",
# MAGIC           "showLegend": true
# MAGIC         },
# MAGIC         "tooltip": {
# MAGIC           "mode": "single",
# MAGIC           "sort": "none"
# MAGIC         }
# MAGIC       },
# MAGIC       "targets": [
# MAGIC         {
# MAGIC           "datasource": {
# MAGIC             "type": "prometheus",
# MAGIC             "uid": "grafanacloud-prom"
# MAGIC           },
# MAGIC           "editorMode": "code",
# MAGIC           "expr": "sum(startOffset{job=\"$job\", topic=~\"$topic\", partition=~\"$partition\"})",
# MAGIC           "legendFormat": "__auto",
# MAGIC           "range": true,
# MAGIC           "refId": "A"
# MAGIC         },
# MAGIC         {
# MAGIC           "datasource": {
# MAGIC             "type": "prometheus",
# MAGIC             "uid": "grafanacloud-prom"
# MAGIC           },
# MAGIC           "editorMode": "code",
# MAGIC           "expr": "sum(latestOffset{job=\"$job\", topic=~\"$topic\", partition=~\"$partition\"})",
# MAGIC           "hide": false,
# MAGIC           "interval": "",
# MAGIC           "legendFormat": "__auto",
# MAGIC           "range": true,
# MAGIC           "refId": "B"
# MAGIC         }
# MAGIC       ],
# MAGIC       "title": "Start Offset vs Latest Offset",
# MAGIC       "type": "timeseries"
# MAGIC     },
# MAGIC     {
# MAGIC       "datasource": {
# MAGIC         "type": "prometheus",
# MAGIC         "uid": "grafanacloud-prom"
# MAGIC       },
# MAGIC       "fieldConfig": {
# MAGIC         "defaults": {
# MAGIC           "color": {
# MAGIC             "fixedColor": "dark-red",
# MAGIC             "mode": "fixed"
# MAGIC           },
# MAGIC           "custom": {
# MAGIC             "axisCenteredZero": false,
# MAGIC             "axisColorMode": "text",
# MAGIC             "axisLabel": "",
# MAGIC             "axisPlacement": "auto",
# MAGIC             "barAlignment": 0,
# MAGIC             "drawStyle": "line",
# MAGIC             "fillOpacity": 19,
# MAGIC             "gradientMode": "none",
# MAGIC             "hideFrom": {
# MAGIC               "legend": false,
# MAGIC               "tooltip": false,
# MAGIC               "viz": false
# MAGIC             },
# MAGIC             "lineInterpolation": "smooth",
# MAGIC             "lineStyle": {
# MAGIC               "dash": [
# MAGIC                 10,
# MAGIC                 10
# MAGIC               ],
# MAGIC               "fill": "dash"
# MAGIC             },
# MAGIC             "lineWidth": 1,
# MAGIC             "pointSize": 5,
# MAGIC             "scaleDistribution": {
# MAGIC               "type": "linear"
# MAGIC             },
# MAGIC             "showPoints": "auto",
# MAGIC             "spanNulls": false,
# MAGIC             "stacking": {
# MAGIC               "group": "A",
# MAGIC               "mode": "none"
# MAGIC             },
# MAGIC             "thresholdsStyle": {
# MAGIC               "mode": "off"
# MAGIC             }
# MAGIC           },
# MAGIC           "mappings": [],
# MAGIC           "thresholds": {
# MAGIC             "mode": "absolute",
# MAGIC             "steps": [
# MAGIC               {
# MAGIC                 "color": "red",
# MAGIC                 "value": null
# MAGIC               }
# MAGIC             ]
# MAGIC           }
# MAGIC         },
# MAGIC         "overrides": []
# MAGIC       },
# MAGIC       "gridPos": {
# MAGIC         "h": 13,
# MAGIC         "w": 12,
# MAGIC         "x": 12,
# MAGIC         "y": 30
# MAGIC       },
# MAGIC       "id": 2,
# MAGIC       "options": {
# MAGIC         "legend": {
# MAGIC           "calcs": [],
# MAGIC           "displayMode": "list",
# MAGIC           "placement": "bottom",
# MAGIC           "showLegend": true
# MAGIC         },
# MAGIC         "tooltip": {
# MAGIC           "mode": "single",
# MAGIC           "sort": "none"
# MAGIC         }
# MAGIC       },
# MAGIC       "targets": [
# MAGIC         {
# MAGIC           "datasource": {
# MAGIC             "type": "prometheus",
# MAGIC             "uid": "grafanacloud-prom"
# MAGIC           },
# MAGIC           "editorMode": "builder",
# MAGIC           "expr": "sum(maxOffsetsBehindLatest{job=\"$job\", topic=~\"$topic\"})",
# MAGIC           "legendFormat": "__auto",
# MAGIC           "range": true,
# MAGIC           "refId": "A"
# MAGIC         }
# MAGIC       ],
# MAGIC       "title": "Offset Lag",
# MAGIC       "type": "timeseries"
# MAGIC     },
# MAGIC     {
# MAGIC       "datasource": {
# MAGIC         "type": "prometheus",
# MAGIC         "uid": "grafanacloud-prom"
# MAGIC       },
# MAGIC       "fieldConfig": {
# MAGIC         "defaults": {
# MAGIC           "color": {
# MAGIC             "mode": "thresholds"
# MAGIC           },
# MAGIC           "custom": {
# MAGIC             "axisCenteredZero": false,
# MAGIC             "axisColorMode": "text",
# MAGIC             "axisLabel": "",
# MAGIC             "axisPlacement": "auto",
# MAGIC             "fillOpacity": 80,
# MAGIC             "gradientMode": "none",
# MAGIC             "hideFrom": {
# MAGIC               "legend": false,
# MAGIC               "tooltip": false,
# MAGIC               "viz": false
# MAGIC             },
# MAGIC             "lineWidth": 1,
# MAGIC             "scaleDistribution": {
# MAGIC               "type": "linear"
# MAGIC             },
# MAGIC             "thresholdsStyle": {
# MAGIC               "mode": "off"
# MAGIC             }
# MAGIC           },
# MAGIC           "mappings": [],
# MAGIC           "thresholds": {
# MAGIC             "mode": "absolute",
# MAGIC             "steps": [
# MAGIC               {
# MAGIC                 "color": "green",
# MAGIC                 "value": null
# MAGIC               },
# MAGIC               {
# MAGIC                 "color": "red",
# MAGIC                 "value": 80
# MAGIC               }
# MAGIC             ]
# MAGIC           }
# MAGIC         },
# MAGIC         "overrides": []
# MAGIC       },
# MAGIC       "gridPos": {
# MAGIC         "h": 11,
# MAGIC         "w": 24,
# MAGIC         "x": 0,
# MAGIC         "y": 43
# MAGIC       },
# MAGIC       "id": 14,
# MAGIC       "options": {
# MAGIC         "barRadius": 0,
# MAGIC         "barWidth": 0.97,
# MAGIC         "groupWidth": 0.7,
# MAGIC         "legend": {
# MAGIC           "calcs": [],
# MAGIC           "displayMode": "list",
# MAGIC           "placement": "bottom",
# MAGIC           "showLegend": true
# MAGIC         },
# MAGIC         "orientation": "auto",
# MAGIC         "showValue": "auto",
# MAGIC         "stacking": "none",
# MAGIC         "tooltip": {
# MAGIC           "mode": "single",
# MAGIC           "sort": "none"
# MAGIC         },
# MAGIC         "xTickLabelRotation": 0,
# MAGIC         "xTickLabelSpacing": 0
# MAGIC       },
# MAGIC       "targets": [
# MAGIC         {
# MAGIC           "datasource": {
# MAGIC             "type": "prometheus",
# MAGIC             "uid": "grafanacloud-prom"
# MAGIC           },
# MAGIC           "editorMode": "code",
# MAGIC           "expr": "(triggerExecution{job=\"$job\", topic=~\"$topic\"} + latestOffset{job=\"$job\", topic=~\"$topic\"}) / 1000",
# MAGIC           "legendFormat": "__auto",
# MAGIC           "range": true,
# MAGIC           "refId": "A"
# MAGIC         }
# MAGIC       ],
# MAGIC       "title": "Batch Duration",
# MAGIC       "type": "barchart"
# MAGIC     }
# MAGIC   ],
# MAGIC   "refresh": false,
# MAGIC   "schemaVersion": 37,
# MAGIC   "style": "dark",
# MAGIC   "tags": [],
# MAGIC   "templating": {
# MAGIC     "list": [
# MAGIC       {
# MAGIC         "current": {
# MAGIC           "selected": true,
# MAGIC           "text": "kafka_offsets_demo",
# MAGIC           "value": "kafka_offsets_demo"
# MAGIC         },
# MAGIC         "datasource": {
# MAGIC           "type": "prometheus",
# MAGIC           "uid": "grafanacloud-prom"
# MAGIC         },
# MAGIC         "definition": "label_values(job)",
# MAGIC         "hide": 0,
# MAGIC         "includeAll": false,
# MAGIC         "multi": false,
# MAGIC         "name": "job",
# MAGIC         "options": [],
# MAGIC         "query": {
# MAGIC           "query": "label_values(job)",
# MAGIC           "refId": "StandardVariableQuery"
# MAGIC         },
# MAGIC         "refresh": 1,
# MAGIC         "regex": "",
# MAGIC         "skipUrlSync": false,
# MAGIC         "sort": 0,
# MAGIC         "type": "query"
# MAGIC       },
# MAGIC       {
# MAGIC         "current": {
# MAGIC           "selected": true,
# MAGIC           "text": [
# MAGIC             "All"
# MAGIC           ],
# MAGIC           "value": [
# MAGIC             "$__all"
# MAGIC           ]
# MAGIC         },
# MAGIC         "datasource": {
# MAGIC           "type": "prometheus",
# MAGIC           "uid": "grafanacloud-prom"
# MAGIC         },
# MAGIC         "definition": "label_values({job=\"$job\", topic!=\"hello_test\"}, topic)",
# MAGIC         "hide": 0,
# MAGIC         "includeAll": true,
# MAGIC         "multi": true,
# MAGIC         "name": "topic",
# MAGIC         "options": [],
# MAGIC         "query": {
# MAGIC           "query": "label_values({job=\"$job\", topic!=\"hello_test\"}, topic)",
# MAGIC           "refId": "StandardVariableQuery"
# MAGIC         },
# MAGIC         "refresh": 1,
# MAGIC         "regex": "",
# MAGIC         "skipUrlSync": false,
# MAGIC         "sort": 0,
# MAGIC         "type": "query"
# MAGIC       },
# MAGIC       {
# MAGIC         "current": {
# MAGIC           "selected": false,
# MAGIC           "text": "All",
# MAGIC           "value": "$__all"
# MAGIC         },
# MAGIC         "datasource": {
# MAGIC           "type": "prometheus",
# MAGIC           "uid": "grafanacloud-prom"
# MAGIC         },
# MAGIC         "definition": "label_values({job=\"$job\", topic=~\"$topic\"}, partition)",
# MAGIC         "hide": 0,
# MAGIC         "includeAll": true,
# MAGIC         "multi": true,
# MAGIC         "name": "partition",
# MAGIC         "options": [],
# MAGIC         "query": {
# MAGIC           "query": "label_values({job=\"$job\", topic=~\"$topic\"}, partition)",
# MAGIC           "refId": "StandardVariableQuery"
# MAGIC         },
# MAGIC         "refresh": 1,
# MAGIC         "regex": "",
# MAGIC         "skipUrlSync": false,
# MAGIC         "sort": 0,
# MAGIC         "type": "query"
# MAGIC       }
# MAGIC     ]
# MAGIC   },
# MAGIC   "time": {
# MAGIC     "from": "now-5m",
# MAGIC     "to": "now"
# MAGIC   },
# MAGIC   "timepicker": {},
# MAGIC   "timezone": "",
# MAGIC   "title": "Structured Streaming Kafka Offsets Monitoring",
# MAGIC   "uid": "h_-29Sc4z",
# MAGIC   "version": 29,
# MAGIC   "weekStart": ""
# MAGIC }
# MAGIC ```

# COMMAND ----------


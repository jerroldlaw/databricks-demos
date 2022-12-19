# EC2
Spin up a `t2.medium` on an **Amazon Linux 2** OS EC2.

## Docker CE Install

```sh
sudo yum install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
```

## docker-compose install

Copy the appropriate `docker-compose` binary from GitHub:
`sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose`

Fix permissions after download:

`sudo chmod +x /usr/local/bin/docker-compose`

Verify success:

`docker-compose version`

# Prometheus + Prometheus PushGateway
Make a directory `prometheus` in your home folder.
```
mkdir prometheus
cd prometheus
```
## Docker Compose File
vi docker-compose.yml
```
version: '3.3'

volumes:
  prometheus_data: {}

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    expose:
      - 9090
    ports:
      - "9090:9090"

  pushgateway:
    image: prom/pushgateway:latest
    container_name: pushgateway
    restart: unless-stopped
    expose:
      - 9091
    ports:
      - "9091:9091"
```

## Prometheus Config
vi prometheus.yml
```
global:
  scrape_interval: 1m

scrape_configs:
  - job_name: "pushgateway"
    honor_labels: true
    static_configs:
      - targets: ['pushgateway:9091']

remote_write:
  - url: https://zzz.grafana.net/api/prom/push
    basic_auth:
      username: yyy
      password: xxx==
```

## Run Docker Compose
```
docker-compose up -d
```

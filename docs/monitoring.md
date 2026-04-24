# Monitoring Documentation

## Overview

Monitoring is implemented with Prometheus, Grafana and Node Exporter.

The monitoring stack runs on:

```text
monitoring-vm: 192.168.0.113
```

## Components

| Component | Purpose |
|---|---|
| Prometheus | Metrics collection |
| Grafana | Visualization and dashboards |
| Node Exporter | Linux host metrics |

## Prometheus

Prometheus is available at:

```text
http://192.168.0.113:9090
```

## Grafana

Grafana is available at:

```text
http://192.168.0.113:3000
```

Default login:

```text
admin / admin
```

The password should be changed after the first login.

## Prometheus Targets

| Target | Role |
|---|---|
| 192.168.0.110:9100 | app-vm |
| 192.168.0.111:9100 | proxy-vm |
| 192.168.0.112:9100 | db-vm |
| 192.168.0.113:9100 | monitoring-vm |

## Prometheus Configuration

Example `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "node-exporter"
    static_configs:
      - targets:
          - "192.168.0.110:9100"
          - "192.168.0.111:9100"
          - "192.168.0.112:9100"
          - "192.168.0.113:9100"
```

## Grafana Datasource

Grafana uses Prometheus as a datasource.

When Grafana and Prometheus run in the same Docker Compose network, the datasource URL is:

```text
http://prometheus:9090
```

## Verification

Open:

```text
http://192.168.0.113:9090/targets
```

All Node Exporter targets should be in the `UP` state.

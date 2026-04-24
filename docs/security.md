# Security Documentation

## Overview

The lab uses basic network segmentation and host-based firewall rules with UFW.

The goal is to expose only the services that are required for the application to work.

## Firewall Rules

### proxy-vm — 192.168.0.111

Allowed incoming traffic:

| Source | Port | Purpose |
|---|---:|---|
| 192.168.0.0/24 | 22 | SSH |
| 192.168.0.0/24 | 80 | HTTP access to Nginx |

### app-vm — 192.168.0.110

Allowed incoming traffic:

| Source | Port | Purpose |
|---|---:|---|
| 192.168.0.0/24 | 22 | SSH |
| 192.168.0.111 | 8080 | Application access from proxy-vm |

### db-vm — 192.168.0.112

Allowed incoming traffic:

| Source | Port | Purpose |
|---|---:|---|
| 192.168.0.0/24 | 22 | SSH |
| 192.168.0.110 | 5432 | PostgreSQL access from app-vm |

### monitoring-vm — 192.168.0.113

Allowed incoming traffic:

| Source | Port | Purpose |
|---|---:|---|
| 192.168.0.0/24 | 22 | SSH |
| 192.168.0.0/24 | 3000 | Grafana |
| 192.168.0.0/24 | 9090 | Prometheus |
| 192.168.0.0/24 | 9100 | Node Exporter metrics |

## PostgreSQL Access Control

PostgreSQL listens only on:

```text
192.168.0.112:5432
```

The `pg_hba.conf` file allows access only from:

```text
192.168.0.110/32
```

Example rule:

```text
host    cloudlab_app    cloudlab_user    192.168.0.110/32    scram-sha-256
```

## Application Access Control

The FastAPI application runs on:

```text
192.168.0.110:8080
```

It should be accessible only from the Nginx reverse proxy:

```text
192.168.0.111
```

## Secrets Management

Real credentials are stored in local `.env` files.

The repository contains only:

```text
.env.example
```

Real `.env` files are ignored by Git.

## Security Notes

This is a local training lab, not a production environment. However, the project follows several production-like principles:

- service separation
- least privilege network access
- private database access
- no secrets committed to Git
- firewall enabled on every VM
- reverse proxy in front of the application
- database isolated from direct user access

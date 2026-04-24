# Security Documentation

## Overview

The lab uses basic network segmentation and host-based firewall rules with UFW.

The goal is to expose only the services that are required for the application to work.

## Firewall Rules

### proxy-vm

Allowed incoming traffic:

| Source | Port | Purpose |
|---|---:|---|
| 10.10.10.0/24 | 22 | SSH |
| 10.10.10.0/24 | 80 | HTTP access to Nginx |

### app-vm

Allowed incoming traffic:

| Source | Port | Purpose |
|---|---:|---|
| 10.10.10.0/24 | 22 | SSH |
| 10.10.10.10 | 8080 | Application access from proxy-vm |

### db-vm

Allowed incoming traffic:

| Source | Port | Purpose |
|---|---:|---|
| 10.10.10.0/24 | 22 | SSH |
| 10.10.10.20 | 5432 | PostgreSQL access from app-vm |

### monitoring-vm

Allowed incoming traffic:

| Source | Port | Purpose |
|---|---:|---|
| 10.10.10.0/24 | 22 | SSH |
| 10.10.10.0/24 | 3000 | Grafana |
| 10.10.10.0/24 | 9090 | Prometheus |

## PostgreSQL Access Control

PostgreSQL listens only on:

```text
10.10.10.30:5432
```

The `pg_hba.conf` file allows access only from:

```text
10.10.10.20/32
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

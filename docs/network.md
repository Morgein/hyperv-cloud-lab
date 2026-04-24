# Network Documentation

## Overview

This lab uses a private Hyper-V NAT network. All virtual machines are connected to the same internal switch and use static IP addresses.

## Hyper-V Network

| Component | Value |
|---|---|
| Switch name | cloud-lab-switch |
| Network | 10.10.10.0/24 |
| Host gateway | 10.10.10.1 |
| Type | Internal switch with NAT |

## IP Addressing

| VM | IP Address | Gateway | Role |
|---|---:|---:|---|
| proxy-vm | 10.10.10.10/24 | 10.10.10.1 | Reverse proxy |
| app-vm | 10.10.10.20/24 | 10.10.10.1 | Application server |
| db-vm | 10.10.10.30/24 | 10.10.10.1 | Database server |
| monitoring-vm | 10.10.10.40/24 | 10.10.10.1 | Monitoring server |

## Traffic Flow

```text
Windows Host
   ↓
proxy-vm / Nginx
   ↓
app-vm / FastAPI
   ↓
db-vm / PostgreSQL
```

## Access Model

The Windows host accesses the application through `cloudlab.local`, which points to `10.10.10.10`.

The database server is not exposed directly to the application user. It accepts PostgreSQL connections only from `app-vm`.

## DNS / Hosts Entry

On the Windows host, the following entry is added to the hosts file:

```text
10.10.10.10 cloudlab.local
```

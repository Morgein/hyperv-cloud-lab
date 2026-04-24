# Network Documentation

## Overview

This lab uses a local Hyper-V-based virtual infrastructure. All virtual machines are connected to the `192.168.0.0/24` network and use static IP addresses.

## Network

| Component | Value |
|---|---|
| Network | 192.168.0.0/24 |
| Virtualization platform | Hyper-V |
| Addressing | Static IP addresses |
| Local application domain | cloudlab.local |

## IP Addressing

| VM | IP Address | Role |
|---|---:|---|
| app-vm | 192.168.0.110 | Docker + FastAPI application |
| proxy-vm | 192.168.0.111 | Nginx reverse proxy |
| db-vm | 192.168.0.112 | PostgreSQL database |
| monitoring-vm | 192.168.0.113 | Prometheus + Grafana |

## Traffic Flow

```text
Windows Host
   ↓
proxy-vm / Nginx
192.168.0.111
   ↓
app-vm / FastAPI
192.168.0.110
   ↓
db-vm / PostgreSQL
192.168.0.112
```

## Access Model

The Windows host accesses the application through:

```text
http://cloudlab.local
```

The local hostname points to the Nginx reverse proxy:

```text
192.168.0.111 cloudlab.local
```

The application server listens on:

```text
192.168.0.110:8080
```

The database server listens on:

```text
192.168.0.112:5432
```

The database server is not exposed directly to the application user. It accepts PostgreSQL connections only from:

```text
192.168.0.110
```

## Windows Hosts Entry

On the Windows host, the following entry is added to:

```text
C:\Windows\System32\drivers\etc\hosts
```

Entry:

```text
192.168.0.111 cloudlab.local
```

## Connectivity Tests

From Windows PowerShell:

```powershell
ping 192.168.0.110
ping 192.168.0.111
ping 192.168.0.112
ping 192.168.0.113
```

From proxy-vm:

```bash
curl http://192.168.0.110:8080/health
```

From app-vm:

```bash
curl http://localhost:8080/health
```

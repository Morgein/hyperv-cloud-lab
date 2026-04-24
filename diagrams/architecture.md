# Architecture Diagram

```mermaid
flowchart TD
    A[Windows 11 Host] --> B[Hyper-V Virtual Network<br/>192.168.0.0/24]

    B --> C[app-vm<br/>192.168.0.110<br/>Docker + FastAPI]
    B --> D[proxy-vm<br/>192.168.0.111<br/>Nginx Reverse Proxy]
    B --> E[db-vm<br/>192.168.0.112<br/>PostgreSQL]
    B --> F[monitoring-vm<br/>192.168.0.113<br/>Prometheus + Grafana]

    D --> C
    C --> E

    F --> C
    F --> D
    F --> E
```

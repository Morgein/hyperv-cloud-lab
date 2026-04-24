# Hyper-V Production-like Cloud Lab

## Goal

This project demonstrates a production-like local cloud infrastructure built with Hyper-V, Ubuntu Server, Nginx, Docker, PostgreSQL, Prometheus, Grafana, UFW firewall rules and backup automation.

The main goal is to practice core Cloud Engineering and DevOps skills without using paid cloud resources.

---

## Architecture

The lab runs on a Windows 11 Hyper-V host. Four Ubuntu Server virtual machines are connected through a private Hyper-V NAT network.

```text
Windows 11 / Hyper-V Host
        |
        | NAT Internal Switch: cloud-lab-switch
        | Network: 10.10.10.0/24
        | Host Gateway: 10.10.10.1
        |
-----------------------------------------------------
|              |              |                     |
proxy-vm       app-vm         db-vm                 monitoring-vm
10.10.10.10    10.10.10.20    10.10.10.30           10.10.10.40
Nginx          Docker App     PostgreSQL            Prometheus + Grafana
```

---

## Request Flow

```text
Windows browser / PowerShell
   ↓
http://cloudlab.local
   ↓
proxy-vm / Nginx reverse proxy
   ↓
app-vm / Dockerized FastAPI application
   ↓
db-vm / PostgreSQL database
```

---

## Network

| VM | IP Address | Role |
|---|---:|---|
| proxy-vm | 10.10.10.10 | Nginx reverse proxy |
| app-vm | 10.10.10.20 | Dockerized FastAPI application |
| db-vm | 10.10.10.30 | PostgreSQL database server |
| monitoring-vm | 10.10.10.40 | Prometheus and Grafana server |

---

## Technologies

- Hyper-V
- Ubuntu Server
- Netplan
- Nginx
- Docker
- Docker Compose
- FastAPI
- PostgreSQL
- UFW
- Fail2ban
- Prometheus
- Grafana
- Node Exporter
- systemd timers
- PowerShell
- SSH / SCP

---

## Repository Structure

```text
hyperv-cloud-lab/
├── README.md
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
├── nginx/
│   └── cloudlab.conf
├── monitoring/
│   ├── prometheus.yml
│   └── docker-compose.monitoring.yml
├── scripts/
│   ├── backup-postgres.sh
│   └── restore-postgres.sh
├── docs/
│   ├── network.md
│   ├── security.md
│   ├── monitoring.md
│   └── troubleshooting.md
└── diagrams/
    └── architecture.md
```

---

## Application

The application is a small FastAPI service connected to a PostgreSQL database.

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Basic API message |
| GET | `/health` | Health check |
| POST | `/notes` | Create a note |
| GET | `/notes` | List notes from PostgreSQL |

### Example Requests

Health check:

```powershell
curl.exe http://cloudlab.local/health
```

Create a note:

```powershell
curl.exe -X POST "http://cloudlab.local/notes" `
  -H "Content-Type: application/json" `
  -d '{"text":"Request through Nginx reverse proxy"}'
```

List notes:

```powershell
curl.exe http://cloudlab.local/notes
```

Expected request path:

```text
Windows Host → Nginx Reverse Proxy → FastAPI Container → PostgreSQL VM
```

---

## Security

The lab uses basic network segmentation with UFW firewall rules.

### proxy-vm

Allowed:

- SSH from lab network
- HTTP port 80 from lab network

### app-vm

Allowed:

- SSH from lab network
- Application port 8080 only from proxy-vm

### db-vm

Allowed:

- SSH from lab network
- PostgreSQL port 5432 only from app-vm

### monitoring-vm

Allowed:

- SSH from lab network
- Grafana port 3000 from lab network
- Prometheus port 9090 from lab network

### Secrets

Real credentials are stored in `.env` files and are not committed to Git.

The repository contains only:

```text
app/.env.example
```

Example:

```env
DATABASE_URL=postgresql://cloudlab_user:CHANGE_ME@10.10.10.30:5432/cloudlab_app
```

---

## PostgreSQL

PostgreSQL runs on a separate virtual machine:

```text
db-vm: 10.10.10.30
```

The database accepts connections only from:

```text
app-vm: 10.10.10.20
```

PostgreSQL access is controlled through:

```text
postgresql.conf
pg_hba.conf
UFW firewall rules
```

---

## Monitoring

Monitoring is implemented with Prometheus, Grafana and Node Exporter.

### Prometheus Targets

| Target | Role |
|---|---|
| 10.10.10.10:9100 | proxy-vm |
| 10.10.10.20:9100 | app-vm |
| 10.10.10.30:9100 | db-vm |
| 10.10.10.40:9100 | monitoring-vm |

Prometheus is available inside the lab network:

```text
http://10.10.10.40:9090
```

Grafana is available inside the lab network:

```text
http://10.10.10.40:3000
```

Grafana uses Prometheus as a datasource:

```text
http://prometheus:9090
```

---

## Backup and Restore

PostgreSQL backups are created using `pg_dump`.

Backup script:

```text
scripts/backup-postgres.sh
```

Restore test script:

```text
scripts/restore-postgres.sh
```

Backups are scheduled with a systemd timer:

```text
cloudlab-db-backup.timer
```

The backup process creates compressed PostgreSQL dump files and keeps only recent backups.

---

## Basic Verification Commands

### Check VM connectivity

```bash
ping 10.10.10.1
ping 1.1.1.1
ping google.com
```

### Check Nginx

```bash
sudo nginx -t
sudo systemctl status nginx
sudo journalctl -u nginx -xe
```

### Check Docker application

```bash
docker ps
docker logs cloudlab-api
curl http://localhost:8080/health
```

### Check PostgreSQL

```bash
sudo systemctl status postgresql
sudo ss -lntp | grep 5432
```

### Check firewall

```bash
sudo ufw status verbose
```

### Check Prometheus targets

Open:

```text
http://10.10.10.40:9090/targets
```

All targets should be in the `UP` state.

---

## Screenshots

Recommended screenshots for documentation:

```text
diagrams/hyper-v-vms.png
diagrams/api-health.png
diagrams/api-notes.png
diagrams/prometheus-targets.png
diagrams/grafana-dashboard.png
```

Suggested README section after adding screenshots:

```markdown
## Screenshots

### Hyper-V Virtual Machines

![Hyper-V VMs](diagrams/hyper-v-vms.png)

### API Health Check

![API Health](diagrams/api-health.png)

### Prometheus Targets

![Prometheus Targets](diagrams/prometheus-targets.png)

### Grafana Dashboard

![Grafana Dashboard](diagrams/grafana-dashboard.png)
```

---

## What I Learned

During this project, I practiced:

- Hyper-V virtual networking
- NAT-based private infrastructure
- Static IP configuration with Netplan
- Linux server administration
- Nginx reverse proxy configuration
- Dockerized application deployment
- PostgreSQL remote access configuration
- Firewall segmentation with UFW
- Monitoring with Prometheus and Grafana
- Database backup and restore automation
- Basic production-like infrastructure documentation

---

## Future Improvements

Possible next steps:

- Add Ansible provisioning
- Add GitLab CI/CD deployment
- Add HTTPS with a local certificate authority
- Add Alertmanager
- Add PostgreSQL exporter
- Add Docker container monitoring with cAdvisor
- Rebuild the same architecture in Microsoft Azure using Terraform
- Add infrastructure diagrams and screenshots

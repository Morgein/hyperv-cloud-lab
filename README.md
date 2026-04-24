# Hyper-V Production-like Cloud Lab

## Goal

This project demonstrates a production-like local cloud infrastructure built with Hyper-V, Ubuntu Server, Nginx, Docker, PostgreSQL, Prometheus, Grafana, UFW firewall rules and backup automation.

The main goal is to practice core Cloud Engineering and DevOps skills without using paid cloud resources.

---

## Architecture

The lab runs on a Windows 11 Hyper-V host. Several Ubuntu Server virtual machines are connected through the local lab network `192.168.0.0/24`.

```text
Windows 11 / Hyper-V Host
        |
        | Hyper-V Virtual Network
        | Network: 192.168.0.0/24
        |
-----------------------------------------------------
|              |              |                     |
app-vm         proxy-vm       db-vm                 monitoring-vm
192.168.0.110  192.168.0.111  192.168.0.112         192.168.0.113
Docker + API   Nginx Proxy    PostgreSQL            Prometheus + Grafana
```

---

## Request Flow

```text
Windows browser / PowerShell
   ↓
http://cloudlab.local
   ↓
proxy-vm / Nginx reverse proxy
192.168.0.111
   ↓
app-vm / Dockerized FastAPI application
192.168.0.110
   ↓
db-vm / PostgreSQL database
192.168.0.112
```

---

## Network

| VM | IP Address | Role |
|---|---:|---|
| app-vm | 192.168.0.110 | Dockerized FastAPI application |
| proxy-vm | 192.168.0.111 | Nginx reverse proxy |
| db-vm | 192.168.0.112 | PostgreSQL database server |
| monitoring-vm | 192.168.0.113 | Prometheus and Grafana server |

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

The API runs on:

```text
192.168.0.110:8080
```

The application is not accessed directly by the user. User requests go through the Nginx reverse proxy on:

```text
192.168.0.111
```

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
Windows Host
   ↓
Nginx Reverse Proxy / 192.168.0.111
   ↓
FastAPI Container / 192.168.0.110:8080
   ↓
PostgreSQL VM / 192.168.0.112:5432
```

---

## Nginx Reverse Proxy

Nginx runs on:

```text
proxy-vm: 192.168.0.111
```

It forwards HTTP requests to the API server:

```text
http://192.168.0.110:8080
```

The local domain `cloudlab.local` points to the proxy VM:

```text
192.168.0.111 cloudlab.local
```

---

## Security

The lab uses basic network segmentation with UFW firewall rules.

### proxy-vm

Allowed:

- SSH from the lab network
- HTTP port 80 from the lab network

### app-vm

Allowed:

- SSH from the lab network
- Application port 8080 only from proxy-vm `192.168.0.111`

### db-vm

Allowed:

- SSH from the lab network
- PostgreSQL port 5432 only from app-vm `192.168.0.110`

### monitoring-vm

Allowed:

- SSH from the lab network
- Grafana port 3000 from the lab network
- Prometheus port 9090 from the lab network

### Secrets

Real credentials are stored in `.env` files and are not committed to Git.

The repository contains only:

```text
app/.env.example
```

Example:

```env
DATABASE_URL=postgresql://cloudlab_user:CHANGE_ME@192.168.0.112:5432/cloudlab_app
```

---

## PostgreSQL

PostgreSQL runs on a separate virtual machine:

```text
db-vm: 192.168.0.112
```

The database accepts connections only from:

```text
app-vm: 192.168.0.110
```

PostgreSQL access is controlled through:

```text
postgresql.conf
pg_hba.conf
UFW firewall rules
```

Expected PostgreSQL listening address:

```text
192.168.0.112:5432
```

---

## Monitoring

Monitoring is implemented with Prometheus, Grafana and Node Exporter.

### Prometheus Targets

| Target | Role |
|---|---|
| 192.168.0.110:9100 | app-vm |
| 192.168.0.111:9100 | proxy-vm |
| 192.168.0.112:9100 | db-vm |
| 192.168.0.113:9100 | monitoring-vm |

Prometheus is available inside the lab network:

```text
http://192.168.0.113:9090
```

Grafana is available inside the lab network:

```text
http://192.168.0.113:3000
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
ping 192.168.0.110
ping 192.168.0.111
ping 192.168.0.112
ping 192.168.0.113
ping 1.1.1.1
ping google.com
```

### Check Nginx

```bash
sudo nginx -t
sudo systemctl status nginx
sudo journalctl -u nginx -xe
curl http://192.168.0.110:8080/health
```

### Check Docker application

```bash
docker ps
docker logs cloudlab-api
curl http://localhost:8080/health
curl http://192.168.0.110:8080/health
```

### Check PostgreSQL

```bash
sudo systemctl status postgresql
sudo ss -lntp | grep 5432
```

Expected result:

```text
192.168.0.112:5432
```

### Check firewall

```bash
sudo ufw status verbose
```

### Check Prometheus targets

Open:

```text
http://192.168.0.113:9090/targets
```

All targets should be in the `UP` state.

---

## Screenshots

### Hyper-V Virtual Machines

![Hyper-V VMs](diagrams/hyper-v-vms.png)

### API Health Check

![API Health](diagrams/api-health.png)

### API Notes Endpoint

![API Notes](diagrams/api-notes.png)

### Prometheus Targets

![Prometheus Targets](diagrams/prometheus-targets.png)

### Grafana Dashboard

![Grafana Dashboard](diagrams/grafana-dashboard.png)


---

## What I Learned

During this project, I practiced:

- Hyper-V virtual networking
- Local cloud-like infrastructure design
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

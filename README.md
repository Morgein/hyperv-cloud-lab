# Hyper-V Production-like Cloud Lab

## Goal

This project demonstrates a production-like local cloud infrastructure built with Hyper-V, Ubuntu Server, Nginx, Docker, FastAPI, PostgreSQL, Prometheus, Grafana, UFW firewall rules and Ansible automation.

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
- Ansible
- Ansible Vault
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
├── ansible/
│   ├── inventory.ini
│   ├── playbook.yml
│   ├── group_vars/
│   │   └── all/
│   │       ├── vars.yml
│   │       └── vault.example.yml
│   └── templates/
│       └── cloudlab.conf.j2
├── nginx/
│   └── cloudlab.conf
├── monitoring/
│   ├── prometheus.yml
│   └── docker-compose.yml
├── scripts/
│   ├── backup-postgres.sh
│   └── restore-postgres.sh
├── docs/
│   ├── network.md
│   ├── security.md
│   ├── monitoring.md
│   └── troubleshooting.md
└── diagrams/
    ├── architecture.md
    ├── hyper-v-vms.png
    ├── api-health.png
    ├── api-notes.png
    ├── prometheus-targets.png
    └── grafana-dashboard.png
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

## Ansible Automation

The infrastructure is automated with Ansible.

The playbook automates:

- common package installation
- Node Exporter installation
- UFW firewall rules
- Nginx reverse proxy configuration
- Docker installation
- FastAPI application deployment with Docker Compose
- PostgreSQL installation and configuration
- PostgreSQL user and database creation
- Prometheus and Grafana deployment
- cleanup of old containers and stale port conflicts

### Inventory

```ini
[api]
api-vm ansible_host=192.168.0.110

[proxy]
proxy-vm ansible_host=192.168.0.111

[database]
db-vm ansible_host=192.168.0.112

[monitoring]
monitoring-vm ansible_host=192.168.0.113
```

### Run the Playbook

From the `ansible/` directory:

```bash
ansible-playbook -i inventory.ini playbook.yml --ask-become-pass --ask-vault-pass
```

Run only one group:

```bash
ansible-playbook -i inventory.ini playbook.yml --limit api --ask-become-pass --ask-vault-pass
ansible-playbook -i inventory.ini playbook.yml --limit proxy --ask-become-pass --ask-vault-pass
ansible-playbook -i inventory.ini playbook.yml --limit database --ask-become-pass --ask-vault-pass
ansible-playbook -i inventory.ini playbook.yml --limit monitoring --ask-become-pass --ask-vault-pass
```

---

## Secrets Management

PostgreSQL credentials are managed with Ansible Vault.

The real vault file is not committed to Git.

Example file:

```text
ansible/group_vars/all/vault.example.yml
```

Expected variable:

```yaml
vault_postgres_password: "CHANGE"
```

Create a real vault file:

```bash
cp ansible/group_vars/all/vault.example.yml ansible/group_vars/all/vault.yml
ansible-vault encrypt ansible/group_vars/all/vault.yml
```

Edit it later:

```bash
ansible-vault edit ansible/group_vars/all/vault.yml
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
- Prometheus port 9090 from the lab network
- Grafana port 3000 from the lab network
- Node Exporter port 9100 from the lab network

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

PostgreSQL is configured by Ansible:

- PostgreSQL installation
- `listen_addresses`
- `pg_hba.conf`
- database creation
- user creation
- privileges
- firewall rule for port `5432`

Expected PostgreSQL listening address:

```text
192.168.0.112:5432
```

---

## Monitoring

Monitoring is implemented with Prometheus, Grafana and Node Exporter.

The monitoring stack is deployed by Ansible on:

```text
monitoring-vm: 192.168.0.113
```

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

---

## Basic Verification Commands

### Check VM connectivity

```bash
ping 192.168.0.110
ping 192.168.0.111
ping 192.168.0.112
ping 192.168.0.113
```

### Check Nginx

```bash
sudo nginx -t
sudo systemctl status nginx
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
- Linux server administration
- Nginx reverse proxy configuration
- Dockerized application deployment
- PostgreSQL remote access configuration
- firewall segmentation with UFW
- monitoring with Prometheus and Grafana
- infrastructure automation with Ansible
- secrets management with Ansible Vault
- troubleshooting Docker port conflicts and stale `docker-proxy` processes
- production-like infrastructure documentation

---

## Future Improvements

Possible next steps:

- Add GitLab CI/CD deployment
- Add HTTPS with a local certificate authority
- Add Alertmanager
- Add PostgreSQL exporter
- Add Docker container monitoring with cAdvisor
- Rebuild the same architecture in Microsoft Azure using Terraform
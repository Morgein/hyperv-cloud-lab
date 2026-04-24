# Troubleshooting

## Check VM Network Connectivity

```bash
ip a
ip route
ping 192.168.0.110
ping 192.168.0.111
ping 192.168.0.112
ping 192.168.0.113
ping 1.1.1.1
ping google.com
```

## Check SSH Access

From Windows PowerShell:

```powershell
ssh cloudadmin@192.168.0.110
ssh cloudadmin@192.168.0.111
ssh cloudadmin@192.168.0.112
ssh cloudadmin@192.168.0.113
```

## Check Nginx on proxy-vm

Run on proxy-vm:

```bash
sudo nginx -t
sudo systemctl status nginx
sudo journalctl -u nginx -xe
curl http://192.168.0.110:8080/health
```

Expected API response:

```json
{"status":"ok"}
```

## Check Docker Application on app-vm

Run on app-vm:

```bash
docker ps
docker logs cloudlab-api
curl http://localhost:8080/health
curl http://192.168.0.110:8080/health
```

Expected response:

```json
{"status":"ok"}
```

## Check PostgreSQL on db-vm

Run on db-vm:

```bash
sudo systemctl status postgresql
sudo ss -lntp | grep 5432
sudo -u postgres psql
```

Expected listening address:

```text
192.168.0.112:5432
```

## Check PostgreSQL Connection from app-vm

Run on app-vm:

```bash
docker logs cloudlab-api
curl http://localhost:8080/notes
```

If the API returns notes or an empty JSON list, the application can connect to PostgreSQL.

## Check Firewall Rules

Run on each VM:

```bash
sudo ufw status verbose
```

Expected key rules:

```text
app-vm:
8080 allowed only from 192.168.0.111

db-vm:
5432 allowed only from 192.168.0.110

monitoring-vm:
3000 and 9090 allowed from 192.168.0.0/24
```

## Check Prometheus Targets

Open in browser:

```text
http://192.168.0.113:9090/targets
```

All targets should be in the `UP` state.

## Check Grafana

Open in browser:

```text
http://192.168.0.113:3000
```

Default login:

```text
admin / admin
```

## Common Issues

### cloudlab.local does not open

Check the Windows hosts file:

```text
C:\Windows\System32\drivers\etc\hosts
```

Expected entry:

```text
192.168.0.111 cloudlab.local
```

Then test:

```powershell
curl.exe http://cloudlab.local/health
```

### Nginx cannot reach the API

Run on proxy-vm:

```bash
curl http://192.168.0.110:8080/health
```

If it fails, check:

- Docker container is running on app-vm
- FastAPI is listening on port 8080
- UFW on app-vm allows 8080 from 192.168.0.111

### FastAPI returns database connection error

Check:

- PostgreSQL is running on db-vm
- `listen_addresses` is set to `192.168.0.112`
- `pg_hba.conf` allows `192.168.0.110/32`
- UFW on db-vm allows port `5432` from app-vm
- `.env` contains the correct database URL

Expected `.env` format:

```env
DATABASE_URL=postgresql://cloudlab_user:YOUR_PASSWORD@192.168.0.112:5432/cloudlab_app
```

### Prometheus target is DOWN

Check:

- Node Exporter is running on the target VM
- port `9100` is allowed from monitoring-vm
- target IP is correct in `prometheus.yml`

Useful command:

```bash
sudo systemctl status prometheus-node-exporter
```

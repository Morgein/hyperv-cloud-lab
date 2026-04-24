# Troubleshooting

## Check VM Network Connectivity

```bash
ip a
ip route
ping 10.10.10.1
ping 1.1.1.1
ping google.com
```

## Check SSH Access

From Windows PowerShell:

```powershell
ssh cloudadmin@10.10.10.10
ssh cloudadmin@10.10.10.20
ssh cloudadmin@10.10.10.30
ssh cloudadmin@10.10.10.40
```

## Check Nginx on proxy-vm

```bash
sudo nginx -t
sudo systemctl status nginx
sudo journalctl -u nginx -xe
curl http://10.10.10.20:8080/health
```

## Check Docker Application on app-vm

```bash
docker ps
docker logs cloudlab-api
curl http://localhost:8080/health
```

## Check PostgreSQL on db-vm

```bash
sudo systemctl status postgresql
sudo ss -lntp | grep 5432
sudo -u postgres psql
```

## Check PostgreSQL Connection from app-vm

From app-vm:

```bash
docker logs cloudlab-api
curl http://localhost:8080/notes
```

## Check Firewall Rules

```bash
sudo ufw status verbose
```

## Check Prometheus Targets

Open in browser:

```text
http://10.10.10.40:9090/targets
```

All targets should be in the `UP` state.

## Check Grafana

Open in browser:

```text
http://10.10.10.40:3000
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
10.10.10.10 cloudlab.local
```

### FastAPI returns database connection error

Check:

- PostgreSQL is running on db-vm
- `listen_addresses` is set to `10.10.10.30`
- `pg_hba.conf` allows `10.10.10.20/32`
- UFW on db-vm allows port `5432` from app-vm

### Prometheus target is DOWN

Check:

- Node Exporter is running
- port `9100` is allowed from monitoring-vm
- target IP is correct in `prometheus.yml`

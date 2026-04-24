#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="/home/cloudadmin/backups/postgres"
TS=$(date +%F_%H-%M-%S)
BACKUP_FILE="$BACKUP_DIR/cloudlab_app_$TS.dump"

mkdir -p "$BACKUP_DIR"

sudo -u postgres pg_dump -Fc cloudlab_app > "$BACKUP_FILE"

find "$BACKUP_DIR" -type f -name "*.dump" -mtime +7 -delete

echo "Backup created: $BACKUP_FILE"

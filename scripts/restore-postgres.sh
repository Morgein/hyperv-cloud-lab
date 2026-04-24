#!/usr/bin/env bash
set -euo pipefail

BACKUP_FILE="${1:?Usage: $0 /path/to/backup.dump}"

sudo -u postgres dropdb --if-exists cloudlab_app_restore
sudo -u postgres createdb cloudlab_app_restore
sudo -u postgres pg_restore -d cloudlab_app_restore "$BACKUP_FILE"

echo "Restore test completed into database: cloudlab_app_restore"

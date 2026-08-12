#!/bin/sh
set -eu
mkdir -p /backups
while true; do
  stamp="$(date -u +%Y%m%dT%H%M%SZ)"
  target="/backups/metaphor_${stamp}.sql.gz"
  PGPASSWORD="$POSTGRES_PASSWORD" pg_dump \
    -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --no-privileges \
    | gzip -9 > "$target"
  find /backups -type f -name 'metaphor_*.sql.gz' -mtime "+${BACKUP_RETENTION_DAYS:-14}" -delete
  sleep 86400
done

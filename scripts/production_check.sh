#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "=== Docker services ==="
docker compose ps

echo "=== Internal health ==="
docker compose exec -T app curl -fsS http://localhost:8000/api/v1/health
echo

echo "=== Public health ==="
curl -fsS https://app.metaphor.uz/api/v1/health
echo

echo "=== Recent app/caddy/worker logs ==="
docker compose logs --tail=40 app caddy worker

echo "=== Backup files ==="
docker compose exec -T backup sh -lc 'ls -lh /backups | tail -n 10'

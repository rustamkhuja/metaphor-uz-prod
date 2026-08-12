#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
version="${1:-}"
if [[ -z "$version" ]]; then
  echo "Usage: bash scripts/promote_to_production.sh YYYY-MM-DD" >&2
  exit 1
fi
for file in app/static/privacy.html app/static/terms.html; do
  if grep -Eqi '\[УКАЗАТЬ|технический проект' "$file"; then
    echo "Legal page still contains a placeholder: $file" >&2
    exit 1
  fi
done
sed -i 's/^APP_ENV=.*/APP_ENV=production/' .env
sed -i "s/^PRIVACY_POLICY_VERSION=.*/PRIVACY_POLICY_VERSION=${version}/" .env
sed -i "s/^TERMS_VERSION=.*/TERMS_VERSION=${version}/" .env
sed -i 's/^LEGAL_LAUNCH_APPROVED=.*/LEGAL_LAUNCH_APPROVED=true/' .env
sed -i 's/^LLM_ENABLE_WEB_SEARCH=.*/LLM_ENABLE_WEB_SEARCH=true/' .env

docker compose config >/tmp/metaphor-compose-config.yml
docker compose up -d --build

echo "Production configuration applied. Current public health response:"
curl -fsS https://app.metaphor.uz/api/v1/health || true
echo

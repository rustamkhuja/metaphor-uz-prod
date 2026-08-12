#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

for command_name in openssl sed; do
  command -v "$command_name" >/dev/null 2>&1 || {
    echo "Required command is missing: $command_name" >&2
    exit 1
  }
done

read -r -s -p "Paste xAI API key (input is hidden): " XAI_KEY
echo
read -r -s -p "Paste Telegram bot token (input is hidden): " TELEGRAM_TOKEN
echo
read -r -p "Telegram bot username without @: " TELEGRAM_USERNAME
read -r -p "Public Telegram channel username with @: " TELEGRAM_CHANNEL
read -r -p "Operator Telegram chat ID (leave blank until it is discovered): " TELEGRAM_OPERATOR_ID

if [[ ! "$XAI_KEY" =~ ^xai- ]]; then
  echo "The xAI key does not start with xai-. Stop and verify that this is an API key from console.x.ai." >&2
  exit 1
fi
if [[ ! "$TELEGRAM_TOKEN" =~ ^[0-9]+: ]]; then
  echo "The Telegram token format is invalid. It should start with digits followed by a colon." >&2
  exit 1
fi
TELEGRAM_USERNAME="${TELEGRAM_USERNAME#@}"
if [[ "$TELEGRAM_CHANNEL" != @* ]]; then
  TELEGRAM_CHANNEL="@${TELEGRAM_CHANNEL}"
fi

ADMIN_API_KEY="$(openssl rand -hex 32)"
SESSION_SECRET="$(openssl rand -hex 48)"
PREMIUM_ACCESS_KEY="$(openssl rand -hex 32)"
TELEGRAM_WEBHOOK_SECRET="$(openssl rand -hex 32)"
POSTGRES_PASSWORD="$(openssl rand -hex 32)"

umask 077
mkdir -p runtime
cat > .env <<EOF_ENV
# Runtime
APP_ENV=development
APP_NAME="Metaphor AI OS"
PUBLIC_BASE_URL=https://app.metaphor.uz
DATABASE_URL=postgresql+psycopg://metaphor:${POSTGRES_PASSWORD}@db:5432/metaphor
TIMEZONE=Asia/Tashkent
LOG_LEVEL=INFO

# xAI
LLM_PRIMARY_PROVIDER=xai
LLM_PRIMARY_BASE_URL=https://api.x.ai/v1
LLM_PRIMARY_API_KEY=${XAI_KEY}
LLM_PRIMARY_MODEL=grok-4.3
LLM_PRIMARY_INPUT_USD_PER_M=1.25
LLM_PRIMARY_OUTPUT_USD_PER_M=2.50
LLM_REASONING_EFFORT=low
LLM_PROMPT_CACHE_KEY=metaphor-v1
LLM_JSON_MODE=true
LLM_TIMEOUT_SECONDS=90
LLM_MAX_OUTPUT_TOKENS=1200
LLM_ENABLE_WEB_SEARCH=false

# Optional failover provider
LLM_SECONDARY_PROVIDER=
LLM_SECONDARY_BASE_URL=
LLM_SECONDARY_API_KEY=
LLM_SECONDARY_MODEL=
LLM_SECONDARY_INPUT_USD_PER_M=0
LLM_SECONDARY_OUTPUT_USD_PER_M=0

# Cost and rate controls
FREE_DAILY_LIMIT=3
DAILY_AI_BUDGET_USD=3.00
MAX_INPUT_CHARACTERS=6000
PREMIUM_VARIANTS=3

# Privacy-by-default
STORE_RAW_INPUT=false
STORE_REDACTED_INPUT=false
STORE_GENERATED_OUTPUT=false
RAW_INPUT_RETENTION_HOURS=24
OUTPUT_RETENTION_HOURS=168
DATA_ENCRYPTION_KEY=
PRIVACY_POLICY_VERSION=2026-08-draft
TERMS_VERSION=2026-08-draft
LEGAL_LAUNCH_APPROVED=false

# Operator/admin
ADMIN_API_KEY=${ADMIN_API_KEY}
SESSION_SECRET=${SESSION_SECRET}
ENABLE_PREMIUM_PILOT=false
PREMIUM_ACCESS_KEY=${PREMIUM_ACCESS_KEY}
AUTO_APPROVE_LOW_RISK_CONTENT=false
AUTO_PUBLISH_TELEGRAM=false
DAILY_CONTENT_HOUR=9
WEEKLY_REVIEW_WEEKDAY=1

# Telegram
TELEGRAM_BOT_TOKEN=${TELEGRAM_TOKEN}
TELEGRAM_BOT_USERNAME=${TELEGRAM_USERNAME}
TELEGRAM_CHANNEL_ID=${TELEGRAM_CHANNEL}
TELEGRAM_OPERATOR_CHAT_ID=${TELEGRAM_OPERATOR_ID}
TELEGRAM_WEBHOOK_SECRET=${TELEGRAM_WEBHOOK_SECRET}

# Optional narration
XAI_TTS_ENABLED=false
XAI_TTS_BASE_URL=https://api.x.ai/v1
XAI_TTS_VOICE_ID=carina
XAI_TTS_USD_PER_M_CHARACTERS=15.0

# Deployment
DOMAIN=app.metaphor.uz
WIDGET_FRAME_ANCESTORS='self'
POSTGRES_DB=metaphor
POSTGRES_USER=metaphor
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
BACKUP_RETENTION_DAYS=14
EOF_ENV

cat > runtime/OWNER_SECRETS.txt <<EOF_SECRETS
Store these values in the owner's password manager, then delete this file.
ADMIN_API_KEY=${ADMIN_API_KEY}
PREMIUM_ACCESS_KEY=${PREMIUM_ACCESS_KEY}
TELEGRAM_WEBHOOK_SECRET=${TELEGRAM_WEBHOOK_SECRET}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
EOF_SECRETS
chmod 600 .env runtime/OWNER_SECRETS.txt
unset XAI_KEY TELEGRAM_TOKEN ADMIN_API_KEY SESSION_SECRET PREMIUM_ACCESS_KEY TELEGRAM_WEBHOOK_SECRET POSTGRES_PASSWORD

echo
echo "Created: $ROOT_DIR/.env"
echo "Created: $ROOT_DIR/runtime/OWNER_SECRETS.txt"
echo "APP_ENV remains development and Caddy must not be started until legal pages are finalized."
echo "Safe configuration summary:"
grep -E '^(APP_ENV|PUBLIC_BASE_URL|LLM_PRIMARY_PROVIDER|LLM_PRIMARY_MODEL|FREE_DAILY_LIMIT|DAILY_AI_BUDGET_USD|LEGAL_LAUNCH_APPROVED|DOMAIN|TELEGRAM_BOT_USERNAME|TELEGRAM_CHANNEL_ID)=' .env

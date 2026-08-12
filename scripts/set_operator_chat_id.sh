#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
command -v jq >/dev/null 2>&1 || { echo "jq is required" >&2; exit 1; }
set -a
# shellcheck disable=SC1091
source .env
set +a
if [[ -z "${TELEGRAM_BOT_TOKEN:-}" ]]; then
  echo "TELEGRAM_BOT_TOKEN is empty" >&2
  exit 1
fi
chat_id="$(curl -fsS "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates" \
  | jq -r '[.result[] | select(.message != null) | .message.chat.id] | last // empty')"
if [[ -z "$chat_id" ]]; then
  echo "No incoming Telegram message was found. Send /start to the bot and run this script again." >&2
  exit 1
fi
sed -i "s/^TELEGRAM_OPERATOR_CHAT_ID=.*/TELEGRAM_OPERATOR_CHAT_ID=${chat_id}/" .env
echo "TELEGRAM_OPERATOR_CHAT_ID was written to .env: ${chat_id}"

#!/usr/bin/env sh
set -eu
[ -f .env ] || cp .env.example .env
python scripts/generate_secrets.py > runtime/generated-secrets.env
python scripts/seed.py
pytest
python scripts/smoke_test.py
printf '\nGenerated secrets are in runtime/generated-secrets.env. Copy them into .env, add external credentials, then delete that file.\n'

# Metaphor AI OS v0.2.1 — Build Manifest

## Runtime

- Python 3.12 target
- FastAPI
- SQLAlchemy
- PostgreSQL 16
- Caddy 2
- Docker Compose
- Pillow + FFmpeg

## Services

- `app`: product/API/static/operator
- `worker`: scheduler/orchestrator
- `db`: PostgreSQL
- `backup`: daily compressed pg_dump
- `caddy`: HTTPS/reverse proxy/security headers

## Main entry points

- `/` — product
- `/widget` — B2B widget
- `/operator` — operator interface; production access must be protected
- `/api/v1/generate`
- `/api/v1/feedback`
- `/api/v1/telegram/webhook`
- `/api/v1/admin/*`
- `/api/v1/health`

## Guided deployment entry points

- `FULL_LAUNCH_GUIDE_RU.md` — complete beginner-safe production launch route;
- `scripts/configure_env.sh` — hidden entry of external secrets and generation of internal secrets;
- `scripts/set_operator_chat_id.sh` — discovery and recording of the operator Telegram chat ID;
- `scripts/promote_to_production.sh` — legal placeholder gate and production promotion;
- `scripts/production_check.sh` — final service, HTTPS, log and backup diagnostics.

## Validation commands

```bash
pytest -q
python scripts/smoke_test.py
python scripts/validate_package.py
python -m compileall -q app scripts
```

## Runtime artefacts excluded from release

- `.env`
- SQLite databases
- API keys and generated secrets
- caches/bytecode
- generated PNG/MP4
- backups
- benchmark outputs containing model responses

# Release v0.2.1 — 2026-08-12

## Product

- позиционирование изменено на помощника для важных разговоров;
- добавлены write/reply/improve/tone-check;
- реализована RU/UZ/EN локализация;
- добавлены editable result, refine, copy/share и feedback.

## AI and cost controls

- provider-independent Responses API router;
- xAI baseline `grok-4.3`;
- JSON mode, reasoning effort и prompt cache key;
- фактическая стоимость xAI через `cost_in_usd_ticks`;
- общий budget ledger для продукта, агентов и TTS;
- 45-case model benchmark.

## Privacy and security

- no-content-storage default;
- signed HttpOnly sessions;
- premium fail-closed;
- production refuses mock/SQLite/HTTP/default secrets;
- data retention cleanup;
- Telegram consent/delete;
- Caddy security headers;
- backup service.

## AI operations

- daily planner/trend/content/QA workflow;
- human approval gate;
- Telegram publisher;
- PNG/MP4 generation and optional TTS;
- growth analyst and operator dashboard;
- B2B widget.

## Validation

- 10 automated tests;
- isolated end-to-end smoke test;
- Python compile check;
- silent MP4 render check;
- package completeness validator;
- GitHub Actions CI and Dependabot configuration.

## Known external gaps

See `docs/20_PRODUCTION_GAP_REGISTER.md`.
## Deployment reliability patch

- added `.gitattributes` to preserve LF line endings when the package is committed from Windows;
- CI invokes release checks through `sh`;
- the backup container invokes the mounted script through `sh`, so deployment no longer depends on the executable bit preserved by the Windows client.
- the operator API key is stored only in browser `sessionStorage`, not persisted across browser restarts.
- generated `.env` is valid both for Docker Compose and the guarded shell helpers; release validation rejects strings resembling a real xAI key.


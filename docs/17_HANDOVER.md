# 17. Передача сильным специалистам и постоянному оператору

## Разовая команда сильных специалистов

### Backend/DevOps

- провести code review;
- создать production secrets;
- выполнить `docker compose config`;
- поднять PostgreSQL/app/worker/backup/Caddy;
- настроить DNS/HTTPS;
- установить Telegram webhook;
- проверить alert оператора;
- закрыть `/operator` identity proxy/VPN;
- dependency/container scan;
- reverse-proxy rate limiting;
- проверить backup и выполнить restore drill;
- оформить rollback.

### AI/Language

- прогнать `scripts/benchmark_models.py` по 45 кейсам;
- заполнить слепые оценки RU/UZ/EN;
- исправить JSON failures;
- подтвердить естественный узбекский;
- настроить fallback;
- провести prompt-injection и fabricated-quote тесты.

### Security/Privacy

- актуализировать data-flow map;
- проверить application/Caddy logs;
- проверить retention cleaner;
- проверить provider terms и фактическую географию;
- утвердить incident response;
- pentest публичных API;
- оформить юридический handoff.

### Product/UX

- мобильный тест на Android/iOS браузерах;
- проверка четырёх режимов;
- copy/share tracking;
- feedback reasons;
- Telegram flow;
- B2B widget flow;
- accessibility keyboard/focus/status test.

## Команды локальной приёмки

```bash
cp .env.example .env
pytest -q
python scripts/smoke_test.py
python scripts/validate_package.py
python -m compileall -q app scripts
```

## Команды production-приёмки

```bash
docker compose config
docker compose up -d --build
docker compose ps
curl -fsS https://app.metaphor.uz/api/v1/health
docker compose exec app python scripts/set_telegram_webhook.py
```

## Обязательная ручная проверка

- реальный xAI API call;
- фактическая стоимость в `/operator`;
- RU/UZ/EN генерация;
- Telegram `/start`, `/agree`, generation, `/delete`;
- daily content run;
- approve → publish;
- backup file;
- restore в отдельную БД;
- production startup fails on default secrets and draft legal pages;
- budget stop;
- no-content-storage проверка в БД и логах.

## Постоянный специалист

После подписания внутреннего acceptance checklist постоянный Product/Growth Operator ведёт проект по `docs/08_OPERATOR_RUNBOOK.md`.

## Ограничение текущей среды сборки

[ТРЕБУЕТ ПРОВЕРКИ] Docker Compose deployment не был фактически поднят в среде подготовки пакета, поскольку Docker daemon здесь недоступен. YAML, Python, API, smoke/media и unit tests проверены; контейнерную и сетевую приёмку обязан выполнить DevOps на целевом VPS.

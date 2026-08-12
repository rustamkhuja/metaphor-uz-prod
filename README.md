# Metaphor AI OS v0.2.1

Готовый стартовый пакет для превращения Metaphor из одностраничного генератора в AI-first сервис, который один product/growth operator ведёт через управляемые автоматизации.

## Что реализовано

- веб-приложение с четырьмя режимами: написать, ответить, улучшить, проверить тон;
- русский, узбекский и английский интерфейс и генерация;
- единый API для сайта, Telegram-бота и B2B-виджета;
- LLM-router: xAI/OpenAI-compatible Responses API, резервный провайдер и mock-режим;
- `store=false`, JSON-ответы, prompt cache key, reasoning control и фактический учёт стоимости xAI;
- privacy-by-default: содержание пользовательского текста и результата не хранится без отдельного включения;
- подписанная анонимная сессия, бесплатный лимит, общий дневной AI-бюджет и premium-gate;
- Telegram webhook, согласие на обработку, RU/UZ/EN, удаление данных и публикация в канал;
- ежедневный контентный цикл: календарь → тренды → RU/UZ генерация → QA → очередь одобрения → Telegram;
- автоматическое создание PNG 1080×1350 и вертикального MP4 1080×1920; xAI TTS включается отдельно;
- операторская панель `/operator`;
- продуктовая аналитика: генерации, пользователи, расходы по целям, copy/share, отзывы, источники и B2B-партнёры;
- B2B embed-widget для сайтов цветов, подарков и открыток;
- Docker Compose: приложение, worker, PostgreSQL, ежедневный backup и Caddy/HTTPS;
- 45-кейсный RU/UZ/EN benchmark и скрипт сравнения моделей;
- 90-дневная дорожная карта, регламент одного оператора, контент-календарь, B2B и legal/risk register;
- 10 автоматических тестов, изолированный smoke test, package validator и GitHub Actions CI с Docker build.

## Полный production-запуск для начинающего оператора

Откройте `FULL_LAUNCH_GUIDE_RU.md`. В нём зафиксирован один сквозной маршрут: резервная ветка GitHub → xAI → Telegram → Hetzner VPS → DNS → секреты → закрытый технический запуск → юридические страницы → HTTPS → webhook → операторская панель → backup/restore → закрытая бета.

Для безопасной настройки предусмотрены вспомогательные скрипты:

```bash
bash scripts/configure_env.sh
bash scripts/set_operator_chat_id.sh
bash scripts/promote_to_production.sh YYYY-MM-DD
bash scripts/production_check.sh
```

## Локальный запуск без внешнего AI

```bash
cp .env.example .env
make seed
make run
```

Открыть:

- продукт: `http://localhost:8000`;
- оператор: `http://localhost:8000/operator`;
- API docs в development: `http://localhost:8000/api/docs`.

В `.env.example` включён `LLM_PRIMARY_PROVIDER=mock`, поэтому локальный запуск не требует аккаунтов и платежей.

## Подключение xAI

В `.env`:

```env
LLM_PRIMARY_PROVIDER=xai
LLM_PRIMARY_BASE_URL=https://api.x.ai/v1
LLM_PRIMARY_API_KEY=<secret>
LLM_PRIMARY_MODEL=grok-4.3
LLM_PRIMARY_INPUT_USD_PER_M=1.25
LLM_PRIMARY_OUTPUT_USD_PER_M=2.50
LLM_REASONING_EFFORT=low
```

`grok-4.3` принят как дешёвая стартовая линия. До production необходимо прогнать `scripts/benchmark_models.py`; победитель определяется качеством RU/UZ и sendability, а не названием модели.

## Проверка

```bash
make test
make smoke
make validate
```

С реальным API:

```bash
python scripts/benchmark_models.py --models grok-4.3,grok-4.5
```

## Production

Выполнить внешние tickets из `docs/19_EXTERNAL_ACTION_TICKETS.md`, затем передать пакет техническому специалисту по `docs/17_HANDOVER.md`.

```bash
cp .env.example .env
python scripts/generate_secrets.py
# перенести значения в .env и заполнить внешние ключи
docker compose config
docker compose up -d --build
docker compose exec app python scripts/set_telegram_webhook.py
```

## Архитектурный принцип

Это не «рой из двадцати автономных ботов». AI создаёт и оценивает материалы; код управляет состояниями, лимитами, дедупликацией, публикацией и аудитом; человек принимает только рискованные, финансовые, юридические и внешние решения.

## Состояние релиза

- локальная функциональная приёмка: выполнена;
- production deployment: требует VPS, DNS, секретов и разрешения владельца;
- Telegram: код реализован, требуется токен/канал;
- Instagram/TikTok/YouTube: архитектура и порядок подключения описаны, публикационные адаптеры не активируются без developer apps, OAuth и platform review;
- платежи: намеренно не реализованы до продуктового gate и договора с провайдером;
- privacy/terms: технический проект, требующий реквизитов владельца и юридического заключения.

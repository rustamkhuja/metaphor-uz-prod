# 20. Реестр оставшихся production gaps

| ID | Статус | Gap | Почему не закрыт внутри пакета | Условие закрытия |
|---|---|---|---|---|
| G01 | OPEN/EXTERNAL | Реальный xAI call и benchmark | нужен API key и оплаченный аккаунт | EXT-01 + `scripts/benchmark_models.py` |
| G02 | OPEN/EXTERNAL | Контейнерная/сетевая приёмка | в среде сборки нет Docker daemon/VPS | EXT-03 + `docs/17_HANDOVER.md` |
| G03 | OPEN/EXTERNAL | Telegram production test | нужен bot token/channel/webhook domain | EXT-02/03 |
| G04 | OPEN/LEGAL | Финальный privacy/terms | неизвестны реквизиты и юридическое заключение | EXT-04 |
| G05 | OPEN/COMMERCIAL | Оплата | намеренно запрещена до product gate и договора | EXT-07 |
| G06 | OPEN/PLATFORM | Instagram/TikTok/YouTube adapters | нужны developer apps, OAuth, permissions/review | EXT-08 |
| G07 | OPEN/SECURITY | External pentest | требует целевого публичного окружения | после deploy, до масштабного продвижения |
| G08 | OPEN/OPS | Restore drill | нужен production PostgreSQL/backup | DevOps acceptance |
| G09 | OPEN/PRODUCT | Доказательство спроса | невозможно заменить реальными пользователями | 500 генераций + KPI gate |
| G10 | OPEN/BRAND | Проверка названия/товарного знака | требует внешней правовой проверки | EXT-04 |

## Закрыто внутри пакета

- модульная архитектура;
- public/admin/Telegram API;
- signed anonymous sessions;
- privacy-by-default storage;
- unified AI budget ledger;
- content/QA/approval/publish workflow;
- media generation;
- backup service definition;
- retention job;
- production configuration validation;
- operator dashboard;
- RU/UZ/EN test set;
- unit and smoke tests;
- handover and operator runbook.

# 10. KPI и автоматические ворота решений

## North Star

`Copy or Share Rate = unique generations with copy/share / completed generations`

## Метрики

| Метрика | Формула | Первичный порог |
|---|---|---:|
| Completion rate | completed / started | ≥60% |
| Copy/share rate | copied_or_shared / completed | ≥35% beta; stop-risk <20% |
| Positive feedback | positive / all explicit feedback | ≥70% |
| Critical language error | critical errors / reviewed outputs | <3% |
| 30-day return | returning users / cohort | ≥10% target |
| Paid conversion | payers / eligible users | ≥0.7% target |
| Refund rate | refunds / purchases | <5% |
| AI cost ratio | AI cost / revenue | <15% after monetization |
| Content-to-product | completed generations from content / landing visits | track by campaign |
| B2B activation | partner checkouts using widget | agreed pilot target |

## Решения

### Включить оплату

Только при 500 completed и достаточном copy/share.

### Включить Telegram auto-publish

Только после 50 подряд материалов, одобренных без существенной правки, и при отсутствии policy incidents.

### Подключить второй LLM

При любом из условий:

- доля технических ошибок >2%;
- качество одного языка статистически хуже;
- downtime основного провайдера;
- стоимость превышает утверждённый предел.

### Делать iOS/Android

Только при одновременном выполнении:

- 30-day return ≥15%;
- ≥1 000 MAU;
- ≥1.5% платной конверсии либо сильный B2B case;
- пользователи явно требуют функции ОС, недоступные Mini App/PWA.

### Закрыть или радикально изменить

После 2 000 completed, если copy/share <20%, возврат <5% и нет B2B-сигнала.

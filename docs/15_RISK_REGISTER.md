# 15. Реестр рисков

| ID | Риск | Вероятность | Влияние | Контроль | Владелец |
|---|---|---|---|---|---|
| R01 | Пользователь предпочитает общий ChatGPT | высокая | высокое | узкие режимы, Telegram, RU/UZ, sendability | Product |
| R02 | Низкая повторяемость | высокая | высокое | reply/improve/tone_check, reminders позже | Product |
| R03 | Неестественный узбекский | средняя | высокое | benchmark, носитель, модельная маршрутизация | Language QA |
| R04 | Утечка личного текста | средняя | критическое | no raw storage, encryption, retention, provider review | Owner/Security |
| R05 | AI создаёт манипулятивный/опасный текст | средняя | высокое | prompt rules, safety, QA, feedback | Product/Safety |
| R06 | Автоконтент становится спамом | высокая | среднее | 1 пост/язык/день, KPI по продукту, approval | Operator |
| R07 | Боты тратят бюджет циклически | средняя | высокое | dedup keys, daily budget, fixed schedule | Engineering |
| R08 | Зависимость от одного LLM | средняя | высокое | provider router, benchmark, failover | Engineering |
| R09 | Payment/legal несоответствие | средняя | критическое | не включать оплату до договора и review | Owner/Legal |
| R10 | Один оператор перегружен | средняя | среднее | регламент, escalation, запрет ручной рутины | Owner |
| R11 | Соцсеть блокирует автоматизацию | средняя | среднее | official API, scopes, audit, rate limits | Operator |
| R12 | Нет B2B-сделок | высокая | среднее | 5 лидов/неделю, 30-day pilot, stop-condition | Owner/Operator |
| R13 | Название конфликтует | низкая/средняя | высокое | trademark/domain review | Owner/Legal |
| R14 | Метрики оптимизируются неправильно | средняя | высокое | north star copy/share, one experiment/week | Product |
| R15 | Публичный кризис из-за неуместного текста | низкая/средняя | высокое | disclaimers, escalation, rapid disable | Owner |

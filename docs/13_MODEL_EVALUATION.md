# 13. Оценка LLM

## Решение

Не выбирать модель по общему рейтингу. `grok-4.3` является стартовой дешёвой линией; production-модель выбирается слепым RU/UZ/EN benchmark.

## Автоматизированный набор

Файл: `evaluation/test_cases.csv` — 45 сценариев:

- RU;
- UZ Latin;
- EN;
- write/reply/improve/tone_check;
- личные и деловые случаи;
- safety-блокировки;
- запрет вымышленных фактов и цитат.

Запуск:

```bash
python scripts/benchmark_models.py --models grok-4.3,grok-4.5
```

Результаты создаются в `evaluation/results/`. Поля human review заполняются вслепую редакторами, которые не видят model ID.

## Ручная оценка 1–5

- естественность;
- сохранение смысла;
- соответствие цели;
- культурная уместность;
- грамматика;
- отсутствие клише;
- готовность отправить;
- безопасность.

## Взвешенная метрика

`0.30 sendability + 0.20 meaning preservation + 0.15 language naturalness + 0.15 goal fit + 0.10 safety + 0.10 cost/latency`

## Production gate

- средняя sendability ≥4.0;
- критическая ошибка <3%;
- корректный JSON ≥95%;
- UZ не ниже RU более чем на 0.5 балла;
- p95 latency и стоимость укладываются в установленный бюджет;
- прямые self-harm/threat кейсы блокируются локально;
- 0 вымышленных цитат в тестовом наборе.

## Маршрутизация после benchmark

- free: самая дешёвая модель, прошедшая gate;
- premium: лидер sendability;
- UZ: лидер узбекской подвыборки;
- technical failure: secondary provider;
- crisis/high-risk: local safe response, не генерация обычного сообщения.

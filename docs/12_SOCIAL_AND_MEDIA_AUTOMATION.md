# 12. Социальные сети и медиа-автоматизация

## Реализовано и протестировано локально

- ежедневная генерация одного RU и одного UZ материала;
- evergreen-календарь и опциональный trend research;
- автоматический AI-QA;
- human approval queue;
- PNG-карточка 1080×1350;
- вертикальный MP4 1080×1920;
- опциональная xAI TTS-озвучка;
- Telegram Bot API;
- публикация approved media в Telegram-канал;
- метрики расходов и статусов внутри продукта.

## Не выдавать за реализованное

[ТРЕБУЕТ ПРОВЕРКИ] Автопубликация в Instagram, TikTok и YouTube не активирована и не протестирована: для каждой платформы нужны developer account/app, OAuth/scopes, фактические media URLs и, где предусмотрено, platform review. До их получения пакет создаёт готовые MP4/PNG и очередь одобрения; оператор публикует их вручную либо подключает официальный adapter после внешнего ticket.

## Instagram

[ПРОВЕРЕНО: Meta for Developers] Content Publishing API предназначен для профессиональных аккаунтов и позволяет программно публиковать media при наличии требуемых permissions.

Порядок подключения:

1. professional account;
2. Meta developer app;
3. publishing permissions и long-lived token;
4. публичный URL media;
5. отдельный журнал idempotency/publication;
6. ручное approval первые 30 дней;
7. только после 50 последовательных корректных публикаций — controlled auto-publish.

## TikTok

[ПРОВЕРЕНО: TikTok for Developers] Content Posting API требует developer app, scopes и review/audit для полноценной прямой публикации.

Порядок подключения:

1. developer app;
2. Content Posting scopes;
3. review/audit;
4. маркировка AI-generated content, когда применимо;
5. отдельная очередь видео;
6. запрет на скрытую массовую активность и обход ограничений.

## YouTube

Порядок подключения:

1. channel ownership;
2. Google Cloud project и OAuth credentials;
3. metadata templates;
4. disclosure synthetic/altered media, когда применимо;
5. публикация только approved media;
6. контроль quota и повторной загрузки.

## Формат контента первого этапа

Использовать шаблонные вертикальные ролики без цифрового аватара:

1. узнаваемая переписка;
2. неудачная формулировка;
3. улучшенный вариант;
4. короткое объяснение;
5. CTA на режим `reply`, `improve` или `tone_check`.

Говорящие AI-аватары не использовать как основу: для эмоционального бренда они создают дополнительный риск неискренности и однотипности.

## KPI

Не оптимизировать систему по числу публикаций. Рабочие KPI:

- переходы в продукт;
- завершённые генерации из конкретного content item;
- copy/share rate;
- повторное использование;
- стоимость активного пользователя;
- B2B lead rate;
- доход/маржа по каналу.

# Metaphor AI OS v0.2.1 — полная пошаговая инструкция запуска

## 0. Зафиксированный маршрут

Эта инструкция запускает новую систему **параллельно** действующему сайту:

- действующий сайт остаётся на `https://metaphor.uz`;
- новая версия запускается на `https://app.metaphor.uz`;
- рабочий код хранится в отдельной ветке GitHub `ai-os-v0.2.1`;
- первый публичный контур: веб-приложение, Telegram-бот, Telegram-канал, операторская панель, ежедневная генерация RU/UZ-контента, резервное копирование;
- оплата, Instagram/TikTok/YouTube auto-publish и нативные приложения не включаются до установленных продуктовых и платформенных gates.

[ПРОВЕРЕНО: GitHub-репозиторий `rustamkhuja/metaphor-uz-prod`, ветка `main`, 12.08.2026] Действующий маленький сайт использует **Groq API** и модель `llama-3.1-8b-instant`; новая версия использует **xAI API / Grok 4.3**. Это разные сервисы. Старый сайт и старый Groq-ключ не отключать, пока новая версия не прошла полную приёмку.

## 1. Обязательные правила безопасности

1. Никогда не отправляйте в чат, мессенджер или скриншот:
   - xAI API key;
   - Telegram bot token;
   - `ADMIN_API_KEY`;
   - пароль PostgreSQL;
   - SSH private key;
   - содержимое файла `.env`.
2. В скриншоте закрывайте секретные строки прямоугольником до отправки.
3. IP-адрес VPS, username бота, username канала, GitHub branch и диагностические логи без секретов отправлять можно.
4. Не изменяйте `main` и DNS-записи `@`/`www` действующего сайта.
5. Выполняйте по одной контрольной точке. Не переходите к следующей, пока я не проверю результат текущей.
6. Если название кнопки или экран отличается от инструкции, ничего не угадывайте: отправьте скриншот всего окна.

---

# ЭТАП A. Подготовка пакета и GitHub

[ПРОВЕРЕНО: официальная документация GitHub Desktop, 12.08.2026] Ветка изолирует новую работу от `main`; `Publish branch` публикует её в GitHub. Если интерфейс GitHub Desktop отличается, отправьте скриншот, не угадывая кнопку.

## Шаг A1. Скачать новый пакет

1. В чате скачайте файл `metaphor_ai_os_v0.2.1.zip`.
2. Сохраните его в папку `Загрузки`.
3. Откройте Проводник Windows.
4. В адресной строке Проводника введите:

```text
C:\
```

5. Создайте папку `Metaphor`.
6. Переместите скачанный ZIP в `C:\Metaphor`.

## Шаг A2. Проверить контрольную сумму

1. Нажмите кнопку **Пуск**.
2. Введите `PowerShell`.
3. Откройте **Windows PowerShell**.
4. Вставьте команду:

```powershell
Get-FileHash "C:\Metaphor\metaphor_ai_os_v0.2.1.zip" -Algorithm SHA256
```

5. Нажмите Enter.
6. В строке `Hash` должно быть значение, указанное рядом со ссылкой на пакет в чате.

Если значение отличается — файл не использовать.

## Шаг A3. Распаковать

1. Нажмите правой кнопкой мыши на ZIP.
2. Нажмите **Извлечь всё…**.
3. В поле пути вставьте:

```text
C:\Metaphor\release
```

4. Нажмите **Извлечь**.
5. Откройте получившуюся папку `metaphor_ai_os`.
6. Внутри на одном уровне должны быть видны:
   - папка `app`;
   - папка `docs`;
   - папка `scripts`;
   - файл `Dockerfile`;
   - файл `docker-compose.yml`;
   - файл `README.md`;
   - файл `.env.example`.

### КОНТРОЛЬНАЯ ТОЧКА A

Отправьте мне:

1. скриншот открытой папки `C:\Metaphor\release\metaphor_ai_os`;
2. текст SHA-256 из PowerShell.

Не отправляйте содержимое файлов.

---

## Шаг A4. Установить GitHub Desktop

1. Откройте браузер.
2. Перейдите на:

```text
https://desktop.github.com/
```

3. Нажмите **Download for Windows**.
4. Откройте скачанный установщик.
5. После установки откройте GitHub Desktop.
6. Нажмите **Sign in to GitHub.com**.
7. Браузер откроет GitHub. Подтвердите вход в аккаунт `rustamkhuja`.
8. Вернитесь в GitHub Desktop.

## Шаг A5. Клонировать существующий репозиторий

1. В верхнем меню GitHub Desktop нажмите **File**.
2. Нажмите **Clone repository…**.
3. Откройте вкладку **GitHub.com**.
4. В списке выберите:

```text
rustamkhuja/metaphor-uz-prod
```

5. В поле **Local path** вставьте:

```text
C:\Metaphor\repo
```

6. Нажмите **Clone**.

## Шаг A6. Создать резервную ветку действующего сайта

1. В верхней панели GitHub Desktop нажмите **Current Branch**.
2. Нажмите **New Branch**.
3. В поле имени вставьте:

```text
legacy-main-2026-08-12
```

4. Убедитесь, что ветка создаётся из `main`.
5. Нажмите **Create Branch**.
6. В верхней панели нажмите **Publish branch**.
7. После публикации снова нажмите **Current Branch**.
8. Выберите `main`.

## Шаг A7. Создать рабочую ветку новой версии

1. Нажмите **Current Branch**.
2. Нажмите **New Branch**.
3. Вставьте имя:

```text
ai-os-v0.2.1
```

4. Основа — `main`.
5. Нажмите **Create Branch**.

## Шаг A8. Заменить файлы только в новой ветке

1. В GitHub Desktop нажмите меню **Repository**.
2. Нажмите **Show in Explorer**.
3. Откроется папка `C:\Metaphor\repo`.
4. Удалите из неё текущие файлы сайта:
   - `index.html`;
   - `admin.html`;
   - `manifest.json`;
   - папку `api`.
5. Скрытую папку `.git` не удаляйте. Обычно Проводник её не показывает.
6. Откройте второе окно Проводника:

```text
C:\Metaphor\release\metaphor_ai_os
```

7. Нажмите `Ctrl+A` внутри этой папки.
8. Нажмите `Ctrl+C`.
9. Перейдите в `C:\Metaphor\repo`.
10. Нажмите `Ctrl+V`.
11. Проверьте: `Dockerfile`, `docker-compose.yml`, `app`, `docs`, `scripts` должны находиться прямо в `C:\Metaphor\repo`, а не внутри дополнительной вложенной папки.

## Шаг A9. Отправить код в GitHub

1. Вернитесь в GitHub Desktop.
2. Слева должен появиться длинный список изменений.
3. В нижнем левом поле **Summary** вставьте:

```text
Add Metaphor AI OS v0.2.1
```

4. Нажмите кнопку **Commit to ai-os-v0.2.1**.
5. После завершения нажмите **Publish branch** или **Push origin** в верхней панели.

## Шаг A10. Проверить GitHub Actions

1. В GitHub Desktop нажмите **Repository** → **View on GitHub**.
2. На странице GitHub сверху нажмите вкладку **Actions**.
3. Слева выберите workflow **Metaphor CI**.
4. Откройте самый верхний запуск.
5. Результат должен быть зелёным.
6. Если запуск красный, откройте красный job `test-and-build`, разверните упавший шаг и отправьте мне скриншот текста ошибки.

### КОНТРОЛЬНАЯ ТОЧКА B

Отправьте мне:

1. ссылку на ветку `ai-os-v0.2.1`;
2. скриншот корня репозитория на этой ветке;
3. скриншот зелёного workflow `Metaphor CI` либо полный текст ошибки.

---

# ЭТАП B. xAI API

[ПРОВЕРЕНО: официальная документация xAI, 12.08.2026] Billing и API usage относятся к выбранной team; prepaid credits позволяют ограничить расход, а полный API key отображается только при создании. Для baseline используется `grok-4.3`.

## Шаг B1. Создать отдельную команду

1. Откройте:

```text
https://console.x.ai/
```

2. Войдите в стабильный аккаунт владельца проекта.
3. В верхней части интерфейса найдите название текущей команды или `Personal Team`.
4. Нажмите на него.
5. Нажмите **+ Create Team**.
6. В поле имени вставьте:

```text
Metaphor Production
```

7. Завершите создание.
8. Убедитесь, что в верхней панели выбрана именно команда `Metaphor Production`.

## Шаг B2. Настроить оплату с жёстким пределом

1. В левом меню нажмите **Billing**.
2. Откройте **API spend management** или **API Credits**.
3. Нажмите **Purchase credits** / **Buy credits**.
4. Введите `25 USD`. Если интерфейс показывает другое обязательное минимальное значение, не оплачивайте сразу — отправьте мне скриншот.
5. Введите платёжные данные.
6. Проверьте billing name/address: эти данные попадут в инвойс.
7. Завершите покупку.
8. **Auto top-up** оставьте выключенным.
9. Не запрашивайте **Monthly invoiced billing**. Если интерфейс уже показывает поле **Invoiced spending limit**, установите `0`; если такого поля нет, ничего дополнительно не включайте.

Так расход ограничивается приобретёнными prepaid credits, пока отдельно не включён другой способ биллинга.

## Шаг B3. Создать API key

1. В левом меню нажмите **API Keys**.
2. Нажмите **Create API Key**.
3. Имя ключа:

```text
metaphor-prod-2026-08
```

4. Если откроется экран разрешений, оставьте только доступ к inference/model endpoints; management permissions не нужны. Если экран разрешений не показывается, продолжайте с настройками по умолчанию.
5. Нажмите **Create**.
6. Скопируйте ключ. Он начинается с `xai-`.
7. Сохраните его в password manager. В чат его не отправляйте.
8. Закройте окно только после сохранения: полный ключ второй раз может не показываться.

### КОНТРОЛЬНАЯ ТОЧКА C

Отправьте мне:

1. скриншот выбранной команды `Metaphor Production`;
2. скриншот баланса prepaid credits;
3. скриншот списка API keys, закрыв значение ключа;
4. текст: `xAI key сохранён, auto top-up выключен, invoiced limit = 0`.

---

# ЭТАП C. Telegram-бот и канал

[ПРОВЕРЕНО: официальная документация Telegram Mini Apps, 12.08.2026] Menu Button настраивается через `@BotFather` и открывает Mini App по HTTPS URL. Точные подписи пунктов могут отличаться в зависимости от языка Telegram.

## Шаг C1. Создать бота

1. Откройте Telegram.
2. В поиске введите:

```text
@BotFather
```

3. Откройте только подтверждённый аккаунт с синей галочкой.
4. Нажмите **Start**.
5. Отправьте команду:

```text
/newbot
```

6. Когда BotFather попросит имя, отправьте:

```text
Metaphor | Важные слова
```

7. Когда попросит username, сначала отправьте:

```text
metaphor_words_bot
```

8. Если username занят, последовательно попробуйте:

```text
metaphor_uz_bot
metaphor_words_uz_bot
metaphor_helper_uz_bot
```

9. После создания BotFather пришлёт token. Скопируйте token в password manager. Не отправляйте его мне.

## Шаг C2. Настроить описание

1. В BotFather отправьте:

```text
/setdescription
```

2. Выберите созданного бота.
3. Отправьте текст:

```text
Metaphor помогает подобрать слова для важного разговора: написать сообщение, ответить, улучшить свой текст или проверить его тон. Русский, o‘zbekcha, English.
```

4. Отправьте:

```text
/setabouttext
```

5. Выберите бота.
6. Отправьте:

```text
AI-помощник для важных разговоров на русском, узбекском и английском.
```

## Шаг C3. Настроить команды

1. Отправьте BotFather:

```text
/setcommands
```

2. Выберите бота.
3. Вставьте одним сообщением:

```text
start - начать
agree - подтвердить обработку текста
help - помощь
ru - русский язык
uz - o‘zbekcha
en - English
delete - удалить мои данные
```

## Шаг C4. Создать публичный канал

1. Вернитесь в список чатов Telegram.
2. Нажмите кнопку создания нового сообщения/чата.
3. Выберите **New Channel / Создать канал**.
4. Название:

```text
Metaphor — важные слова
```

5. Описание:

```text
Как подобрать слова для важного разговора: извиниться, поддержать, ответить спокойно и выразить мысль без шаблонов. Русский и o‘zbekcha.
```

6. Выберите **Public Channel / Публичный канал**.
7. Username сначала:

```text
metaphor_words
```

8. Если занят, используйте по порядку:

```text
metaphor_uz_words
metaphor_words_uz
metaphor_muhim_sozlar
```

## Шаг C5. Добавить бота администратором

1. Откройте созданный канал.
2. Нажмите название канала сверху.
3. Нажмите **Administrators / Администраторы**.
4. Нажмите **Add Administrator / Добавить администратора**.
5. Найдите созданного бота по username.
6. Включите право **Post Messages / Публиковать сообщения**.
7. Остальные опасные права, включая добавление администраторов, не включайте.
8. Сохраните.

## Шаг C6. Подготовить личный chat ID

1. Откройте созданного бота.
2. Нажмите **Start** или отправьте:

```text
/start
```

3. Бот пока может не ответить — сервер ещё не подключён. Сообщение нужно для определения вашего numeric chat ID позже.

### КОНТРОЛЬНАЯ ТОЧКА D

Отправьте мне:

1. username бота без token;
2. публичный username канала;
3. скриншот профиля бота;
4. скриншот страницы администраторов канала, где виден бот и право публикации.

---

# ЭТАП D. VPS в Hetzner Cloud

[ПРОВЕРЕНО: официальные материалы Hetzner, 12.08.2026] Текущий `CX23` имеет 2 vCPU, 4 GB RAM и 40 GB; Hetzner Docker CE App основан на Ubuntu 24.04 и содержит Docker Compose plugin. Новый аккаунт может потребовать подтверждение личности или предоплату.

## Шаг D1. Создать SSH-ключ на Windows

1. Нажмите **Пуск**.
2. Введите `PowerShell`.
3. Откройте Windows PowerShell.
4. Выполните:

```powershell
ssh-keygen -t ed25519 -C "metaphor-vps"
```

5. На вопрос о месте сохранения нажмите Enter — используется стандартный путь.
6. Введите отдельную сильную passphrase для SSH-ключа.
7. Повторите passphrase.
8. Скопируйте публичную часть ключа в буфер:

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | Set-Clipboard
```

Никому не отправляйте файл `id_ed25519`. Передавать можно только содержимое файла с окончанием `.pub`.

## Шаг D2. Создать аккаунт и проект Hetzner

1. Откройте:

```text
https://console.hetzner.cloud/
```

2. Создайте аккаунт на реальные данные владельца платёжной карты.
3. Подтвердите email.
4. Пройдите предложенную проверку личности/карты.
5. После входа нажмите **New Project**.
6. Название проекта:

```text
Metaphor Production
```

7. Откройте проект.

## Шаг D3. Добавить SSH key в Hetzner

1. В левом меню проекта откройте **Security**.
2. Откройте вкладку **SSH Keys**.
3. Нажмите **Add SSH Key**.
4. В большое поле вставьте публичный ключ из буфера `Ctrl+V`.
5. Имя:

```text
Metaphor owner laptop
```

6. Сохраните.

## Шаг D4. Создать firewall

1. В левом меню выберите **Firewalls**.
2. Нажмите **Create Firewall**.
3. Имя:

```text
metaphor-web-firewall
```

4. Добавьте входящие правила:

```text
TCP 22   Source: Any IPv4, Any IPv6
TCP 80   Source: Any IPv4, Any IPv6
TCP 443  Source: Any IPv4, Any IPv6
```

5. Outbound оставьте разрешённым.
6. Сохраните firewall.

SSH позже будет защищён ключом и запретом password login.

## Шаг D5. Создать сервер

1. В левом меню нажмите **Servers**.
2. Нажмите **Add Server**.
3. Location: выберите **Helsinki**. Если план недоступен — **Nuremberg**.
4. В блоке Image переключитесь с **OS Images** на **Apps**.
5. Выберите **Docker CE**. Он должен быть основан на Ubuntu 24.04 и включать Docker Compose plugin.
6. Type: **Shared vCPU**, архитектура **x86**.
7. Выберите `CX23` — 2 vCPU, 4 GB RAM, 40 GB. Если название тарифа отличается, выберите ближайший тариф не ниже 2 vCPU / 4 GB / 40 GB.
8. Networking: IPv4 включён; IPv6 можно оставить включённым.
9. SSH Key: отметьте `Metaphor owner laptop`.
10. Firewalls: выберите `metaphor-web-firewall`.
11. Backups: включите серверные backups.
12. Name:

```text
metaphor-prod-01
```

13. Нажмите **Create & Buy Now**.
14. После создания откройте сервер и скопируйте его IPv4.

### КОНТРОЛЬНАЯ ТОЧКА E

Отправьте мне:

1. скриншот Overview сервера;
2. IPv4 сервера;
3. скриншот firewall rules;
4. тариф и location текстом.

---

# ЭТАП E. Первичная настройка сервера

Во всех командах ниже вместо `SERVER_IP` вставляйте реальный IPv4.

## Шаг E1. Войти как root

1. Откройте PowerShell.
2. Выполните:

```powershell
ssh root@SERVER_IP
```

3. При первом входе появится вопрос о fingerprint. Введите:

```text
yes
```

4. Введите passphrase вашего SSH-ключа, если PowerShell запросит её.

## Шаг E2. Проверить Docker

В терминале сервера выполните по одной команде:

```bash
docker --version
docker compose version
uname -a
```

## Шаг E3. Создать постоянного пользователя

Выполните:

```bash
adduser metaphor
```

Система задаст вопросы:

1. `New password` — придумайте отдельный пароль пользователя сервера;
2. повторите пароль;
3. поля Full Name, Room Number, Work Phone и другие можно пропустить Enter;
4. на `Is the information correct?` введите `Y`.

Далее выполните:

```bash
usermod -aG sudo,docker metaphor
mkdir -p /home/metaphor/.ssh
cp /root/.ssh/authorized_keys /home/metaphor/.ssh/authorized_keys
chown -R metaphor:metaphor /home/metaphor/.ssh
chmod 700 /home/metaphor/.ssh
chmod 600 /home/metaphor/.ssh/authorized_keys
```

## Шаг E4. Проверить второй вход до отключения root

1. Не закрывайте текущую root-сессию.
2. Откройте второе окно PowerShell.
3. Выполните:

```powershell
ssh metaphor@SERVER_IP
```

4. Если вход успешен, выполните:

```bash
sudo whoami
```

5. Введите пароль пользователя `metaphor`.
6. Ответ должен быть:

```text
root
```

## Шаг E5. Отключить root/password SSH

Только после успешного входа `metaphor@SERVER_IP` выполните в сессии пользователя `metaphor`:

```bash
printf 'PermitRootLogin no\nPasswordAuthentication no\nKbdInteractiveAuthentication no\nPubkeyAuthentication yes\n' | sudo tee /etc/ssh/sshd_config.d/99-metaphor-hardening.conf
sudo sshd -t
sudo systemctl reload ssh
```

Команда `sudo sshd -t` не должна вывести ошибку.

## Шаг E6. Установить вспомогательные программы

```bash
sudo apt update
sudo apt install -y git curl jq nano unzip ca-certificates openssl unattended-upgrades
sudo systemctl enable --now unattended-upgrades
```

## Шаг E7. Подготовить папку и клонировать ветку

```bash
sudo mkdir -p /opt/metaphor
sudo chown metaphor:metaphor /opt/metaphor
git clone --branch ai-os-v0.2.1 --single-branch https://github.com/rustamkhuja/metaphor-uz-prod.git /opt/metaphor
cd /opt/metaphor
ls -la
```

В выводе должны быть `Dockerfile`, `docker-compose.yml`, `app`, `scripts`.

### КОНТРОЛЬНАЯ ТОЧКА F

Отправьте мне текстовый вывод команд:

```bash
docker --version
docker compose version
sudo sshd -t
cd /opt/metaphor && git branch --show-current && ls -1 | head -20
```

Секретов в этом выводе нет.

---

# ЭТАП F. DNS для app.metaphor.uz

Панель DNS зависит от регистратора. Здесь нельзя угадывать конкретную кнопку и рисковать действующим сайтом.

## Шаг F1. Открыть DNS-панель

1. Откройте сайт/аккаунт, где оплачивается домен `metaphor.uz` или управляются его DNS-записи.
2. Найдите домен `metaphor.uz`.
3. Откройте раздел с одним из названий:
   - DNS Management;
   - DNS Records;
   - Zone Editor;
   - Управление DNS;
   - DNS-зона.
4. Ничего не удаляйте.

### ПРОМЕЖУТОЧНАЯ КОНТРОЛЬНАЯ ТОЧКА G1

Отправьте мне скриншот всей таблицы DNS и название регистратора/сервиса. После этого я укажу точную кнопку именно в вашей панели.

## Шаг F2. Запись, которая должна быть создана

После моей проверки панели создаётся только одна запись:

```text
Type: A
Name/Host: app
Value/Points to: SERVER_IP
TTL: 300 или Auto
```

Если есть переключатель Proxy/Cloudflare, на этапе получения сертификата он должен быть **DNS only / серое облако**.

Не изменять:

```text
@
www
MX
TXT
NS
```

## Шаг F3. Проверить разрешение имени

На сервере выполните:

```bash
getent ahostsv4 app.metaphor.uz
```

В начале строки должен появиться IP вашего VPS.

### КОНТРОЛЬНАЯ ТОЧКА G2

Отправьте:

1. скриншот созданной A-записи;
2. вывод `getent ahostsv4 app.metaphor.uz`.

---

# ЭТАП G. Заполнить секреты без их показа

## Шаг G1. Запустить конфигуратор

На сервере:

```bash
cd /opt/metaphor
bash scripts/configure_env.sh
```

Скрипт последовательно спросит:

1. `Paste xAI API key` — вставьте сохранённый ключ `xai-...`; ввод не отображается;
2. `Paste Telegram bot token` — вставьте token BotFather; ввод не отображается;
3. `Telegram bot username without @` — username бота без `@`;
4. `Public Telegram channel username with @` — username канала с `@`;
5. `Operator Telegram chat ID` — пока нажмите Enter, если ID ещё не получен.

Скрипт создаст:

```text
/opt/metaphor/.env
/opt/metaphor/runtime/OWNER_SECRETS.txt
```

`OWNER_SECRETS.txt` содержит admin key и другие внутренние секреты. Его не отправлять.

## Шаг G2. Проверить только безопасные строки

```bash
cd /opt/metaphor
grep -E '^(APP_ENV|PUBLIC_BASE_URL|LLM_PRIMARY_PROVIDER|LLM_PRIMARY_MODEL|FREE_DAILY_LIMIT|DAILY_AI_BUDGET_USD|LEGAL_LAUNCH_APPROVED|DOMAIN|TELEGRAM_BOT_USERNAME|TELEGRAM_CHANNEL_ID)=' .env
```

Ожидается:

```text
APP_ENV=development
PUBLIC_BASE_URL=https://app.metaphor.uz
LLM_PRIMARY_PROVIDER=xai
LLM_PRIMARY_MODEL=grok-4.3
FREE_DAILY_LIMIT=3
DAILY_AI_BUDGET_USD=3.00
LEGAL_LAUNCH_APPROVED=false
DOMAIN=app.metaphor.uz
```

### КОНТРОЛЬНАЯ ТОЧКА H

Отправьте только вывод безопасной `grep`-команды. Не отправляйте `.env` и `OWNER_SECRETS.txt`.

---

# ЭТАП H. Закрытый технический запуск без публичного сайта

До финализации privacy/terms Caddy и публичный сайт не запускаются.

## Шаг H1. Проверить Compose

```bash
cd /opt/metaphor
docker compose config >/tmp/metaphor-compose.yml
```

Команда не должна вывести ошибку. Файл `/tmp/metaphor-compose.yml` не отправлять: в нём могут быть раскрыты секреты.

## Шаг H2. Запустить внутренние сервисы

```bash
docker compose up -d --build db app worker backup
docker compose ps
```

Ожидаемые сервисы:

```text
db       healthy
app      healthy
worker   running
backup   running
```

## Шаг H3. Проверить health внутри Docker

```bash
docker compose exec -T app curl -fsS http://localhost:8000/api/v1/health | jq
```

Ожидаются поля:

```json
{
  "status": "ok",
  "environment": "development",
  "provider": "xai",
  "model": "grok-4.3",
  "privacy_mode": "no-content-storage"
}
```

## Шаг H4. Сделать реальную тестовую генерацию

Скопируйте всю команду:

```bash
docker compose exec -T app curl -sS -X POST http://localhost:8000/api/v1/generate \
  -H 'Content-Type: application/json' \
  -d '{
    "mode":"write",
    "language":"ru",
    "relationship":"друг",
    "goal":"извиниться и предложить спокойный разговор",
    "tone":"спокойный, искренний, без пафоса",
    "output_format":"message",
    "length":"short",
    "context":"Мы резко поссорились. Я понимаю свою часть ответственности и хочу первым сделать шаг к примирению.",
    "source_text":"",
    "recipient_name":"",
    "address_form":"informal",
    "tier":"free",
    "source":"api",
    "accepted_terms":true
  }' | jq
```

В ответе должны быть:

```text
variants
provider: xai
model: grok-4.3
```

## Шаг H5. Проверить расходы в xAI

1. Откройте `https://console.x.ai/`.
2. Выберите `Metaphor Production`.
3. Слева откройте **Usage**.
4. Проверьте, что появился вызов API и небольшой расход.

### КОНТРОЛЬНАЯ ТОЧКА I

Отправьте:

1. вывод `docker compose ps`;
2. health JSON;
3. JSON тестовой генерации;
4. скриншот xAI Usage без ключей.

---

# ЭТАП I. Получить Telegram operator chat ID

## Шаг I1. Отправить сообщение боту

1. Откройте личный чат с ботом.
2. Ещё раз отправьте:

```text
/start
```

## Шаг I2. Записать ID автоматически

На сервере:

```bash
cd /opt/metaphor
bash scripts/set_operator_chat_id.sh
```

Скрипт должен вывести:

```text
TELEGRAM_OPERATOR_CHAT_ID was written to .env: ЧИСЛО
```

## Шаг I3. Перезапустить внутренние сервисы

```bash
docker compose up -d --force-recreate app worker
```

### КОНТРОЛЬНАЯ ТОЧКА J

Отправьте строку результата `set_operator_chat_id.sh`. Bot token не отправлять.

---

# ЭТАП J. Юридические страницы — обязательный внешний ввод

[ТРЕБУЕТ ПРОВЕРКИ] Юридическая допустимость трансграничной передачи текста, необходимость регистрации базы и содержание уведомлений пользователю зависят от фактического владельца, архитектуры и применимого законодательства. Production не запускается до письменного заключения профильного юриста.

Production намеренно не запустится с шаблонными страницами.

## Шаг J1. Отправить мне сведения для документов

Скопируйте блок ниже, заполните и отправьте мне:

```text
Юридический владелец сервиса:
Полное наименование / Ф.И.О.:
Организационно-правовая форма:
ИНН / ПИНФЛ:
Юридический/почтовый адрес:
Email поддержки:
Телефон поддержки:
Ответственный за персональные данные:
Email для запросов на доступ/удаление:
Предполагается ли хранить пользовательские тексты: нет
AI-провайдер: xAI
Основной домен: metaphor.uz
Приложение: app.metaphor.uz
Платные функции при первом запуске: нет
```

Также нужен письменный ответ юриста по двум вопросам:

1. требуется ли регистрация базы персональных данных при текущем режиме без хранения содержания текста;
2. какие условия нужны для передачи пользовательского текста иностранному AI-провайдеру.

## Шаг J2. После получения от меня двух финальных файлов

Я подготовлю:

```text
app/static/privacy.html
app/static/terms.html
```

Далее на Windows:

1. замените два файла в `C:\Metaphor\repo\app\static`;
2. откройте GitHub Desktop;
3. Summary:

```text
Finalize privacy and terms for production
```

4. нажмите **Commit to ai-os-v0.2.1**;
5. нажмите **Push origin**.

На сервере:

```bash
cd /opt/metaphor
git pull origin ai-os-v0.2.1
```

### КОНТРОЛЬНАЯ ТОЧКА K

Отправьте:

1. заполненный блок реквизитов;
2. заключение юриста или его краткий письменный вывод;
3. после замены — ссылку на commit с privacy/terms.

---

# ЭТАП K. Production deployment и HTTPS

Этот этап выполнять только после моей проверки юридических страниц.

## Шаг K1. Перевести конфигурацию в production

На сервере выполните, подставив фактическую дату утверждения документов:

```bash
cd /opt/metaphor
bash scripts/promote_to_production.sh "$(TZ=Asia/Tashkent date +%F)"
```

Скрипт:

- проверит отсутствие placeholders;
- установит `APP_ENV=production`;
- установит финальные версии privacy/terms;
- включит `LEGAL_LAUNCH_APPROVED=true`;
- включит web search для trend agent;
- соберёт и запустит `db`, `app`, `worker`, `backup`, `caddy`.

## Шаг K2. Проверить сервисы

```bash
cd /opt/metaphor
docker compose ps
```

Все пять сервисов должны быть `running`/`healthy`.

## Шаг K3. Проверить публичный HTTPS

```bash
curl -I https://app.metaphor.uz
curl -fsS https://app.metaphor.uz/api/v1/health | jq
```

Ожидается:

```text
HTTP/2 200
```

и health:

```json
{
  "status": "ok",
  "environment": "production",
  "provider": "xai",
  "model": "grok-4.3",
  "privacy_mode": "no-content-storage"
}
```

## Шаг K4. Проверить в браузере

Откройте по очереди:

```text
https://app.metaphor.uz
https://app.metaphor.uz/privacy
https://app.metaphor.uz/terms
https://app.metaphor.uz/operator
```

Проверьте:

1. браузер показывает значок замка;
2. нет предупреждения о сертификате;
3. privacy/terms не содержат `[УКАЗАТЬ]` или слов `технический проект`;
4. основная страница открывается на телефоне и компьютере.

### КОНТРОЛЬНАЯ ТОЧКА L

Отправьте:

1. вывод `docker compose ps`;
2. вывод двух `curl`-команд;
3. скриншот главной страницы с адресной строкой и замком;
4. скриншоты privacy и terms.

---

# ЭТАП L. Telegram webhook и Mini App

## Шаг L1. Установить webhook

На сервере:

```bash
cd /opt/metaphor
docker compose exec -T app python scripts/set_telegram_webhook.py
```

Ожидаемый ответ содержит:

```json
{"ok": true}
```

## Шаг L2. Проверить webhook без показа token

```bash
cd /opt/metaphor
set -a
source .env
set +a
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo" | jq
unset TELEGRAM_BOT_TOKEN
```

В поле `url` должно быть:

```text
https://app.metaphor.uz/api/v1/telegram/webhook
```

## Шаг L3. Настроить кнопку Mini App в BotFather

1. Откройте `@BotFather`.
2. Отправьте:

```text
/mybots
```

3. Выберите бота Metaphor.
4. Нажмите **Bot Settings**.
5. Нажмите **Menu Button**.
6. Нажмите **Configure menu button**.
7. Отправьте URL:

```text
https://app.metaphor.uz/
```

8. В качестве текста кнопки отправьте:

```text
Открыть Metaphor
```

9. Если доступен пункт **Configure Mini App**, откройте его, нажмите **Enable Mini App** и снова укажите:

```text
https://app.metaphor.uz/
```

## Шаг L4. Полный Telegram-тест

В личном чате с ботом:

1. отправьте `/start`;
2. проверьте, что пришло уведомление о передаче текста AI-провайдеру;
3. отправьте `/agree`;
4. отправьте:

```text
Поссорились с другом. Хочу извиниться спокойно и без лишнего пафоса.
```

5. должен прийти сгенерированный ответ;
6. отправьте `/uz`;
7. отправьте:

```text
Do‘stimni xafa qilib qo‘ydim. Samimiy, lekin ortiqcha balandparvoz bo‘lmagan uzr yozmoqchiman.
```

8. должен прийти естественный узбекский ответ;
9. отправьте `/delete`;
10. должно прийти подтверждение удаления.

### КОНТРОЛЬНАЯ ТОЧКА M

Отправьте:

1. вывод `getWebhookInfo`, скрыв ничего, кроме возможных чувствительных сообщений об ошибке;
2. скриншот кнопки `Открыть Metaphor`;
3. скриншоты RU и UZ ответов бота;
4. текст результата `/delete`.

---

# ЭТАП M. Операторская панель и контентный оркестр

## Шаг M1. Получить admin key локально

На сервере выполните:

```bash
cd /opt/metaphor
grep '^ADMIN_API_KEY=' runtime/OWNER_SECRETS.txt
```

Скопируйте значение после `=` в password manager. В чат не отправлять.

## Шаг M2. Открыть операторскую панель

1. На доверенном компьютере откройте:

```text
https://app.metaphor.uz/operator
```

2. В поле **Admin API key** вставьте сохранённый ключ.
3. Нажмите **Подключиться**.
4. Должны появиться блок **7 дней** и **Контентная очередь**.

## Шаг M3. Запустить контентный цикл вручную

1. Нажмите **Запустить контентный цикл** один раз.
2. После завершения в очереди должны появиться RU и UZ материалы.
3. Прочитайте каждый текст.
4. Если текст пригоден, нажмите **Одобрить**.
5. После одобрения нажмите **Опубликовать**.
6. Откройте Telegram-канал и проверьте публикацию карточки/ролика.

Первые 30 дней не включать:

```text
AUTO_APPROVE_LOW_RISK_CONTENT=true
AUTO_PUBLISH_TELEGRAM=true
```

## Шаг M4. Проверить worker

На сервере:

```bash
cd /opt/metaphor
docker compose logs --tail=100 worker
```

Не должно быть циклических ошибок.

### КОНТРОЛЬНАЯ ТОЧКА N

Отправьте:

1. скриншот операторской панели без admin key;
2. скриншот RU и UZ элементов очереди;
3. ссылку на первую публикацию Telegram-канала;
4. последние 100 строк worker log, если там есть ошибка; при чистом логе достаточно текста `worker без ошибок`.

---

# ЭТАП N. Резервное копирование и восстановление

## Шаг N1. Проверить наличие backup

```bash
cd /opt/metaphor
docker compose exec -T backup sh -lc 'ls -lh /backups'
```

Должен быть файл вида:

```text
metaphor_YYYYMMDDTHHMMSSZ.sql.gz
```

## Шаг N2. Выполнить restore drill в отдельную тестовую БД

Выполните весь блок:

```bash
cd /opt/metaphor
LATEST_BACKUP=$(docker compose exec -T backup sh -lc "ls -1t /backups/metaphor_*.sql.gz | head -1" | tr -d '\r')
echo "$LATEST_BACKUP"
docker compose exec -T db psql -U metaphor -d postgres -c "DROP DATABASE IF EXISTS metaphor_restore_test;"
docker compose exec -T db psql -U metaphor -d postgres -c "CREATE DATABASE metaphor_restore_test;"
docker compose exec -T backup sh -lc "gzip -dc '$LATEST_BACKUP'" | docker compose exec -T db psql -U metaphor -d metaphor_restore_test
docker compose exec -T db psql -U metaphor -d metaphor_restore_test -c "\dt"
docker compose exec -T db psql -U metaphor -d postgres -c "DROP DATABASE metaphor_restore_test;"
```

В выводе `\dt` должны быть таблицы `generations`, `ai_usage`, `content_items` и другие.

## Шаг N3. Проверить, что пользовательские тексты не хранятся

После нескольких тестов выполните:

```bash
cd /opt/metaphor
docker compose exec -T db psql -U metaphor -d metaphor -c "SELECT id, input_length, length(input_redacted) AS redacted_len, output_json FROM generations ORDER BY created_at DESC LIMIT 5;"
```

Ожидается:

```text
redacted_len = 0
output_json = {}
```

### КОНТРОЛЬНАЯ ТОЧКА O

Отправьте:

1. список backup-файлов;
2. вывод `\dt` тестового восстановления;
3. вывод privacy-проверки таблицы `generations`.

---

# ЭТАП O. Финальная security-проверка

## Шаг O1. Убедиться, что `.env` не попал в Git

```bash
cd /opt/metaphor
git status --ignored -s .env
```

Ожидается:

```text
!! .env
```

## Шаг O2. Проверить отсутствие xAI key в репозитории

```bash
cd /opt/metaphor
git grep -nE 'xai-[A-Za-z0-9_-]{20,}' || true
```

Вывод должен быть пустым.

## Шаг O3. Проверить открытые порты

```bash
sudo ss -lntp
```

Публично нужны только:

```text
22
80
443
```

PostgreSQL `5432` не должен слушать внешний интерфейс хоста.

## Шаг O4. Запустить итоговую диагностику

```bash
cd /opt/metaphor
bash scripts/production_check.sh
```

### КОНТРОЛЬНАЯ ТОЧКА P

Отправьте:

1. вывод `git status --ignored -s .env`;
2. подтверждение, что `git grep -nE 'xai-[A-Za-z0-9_-]{20,}'` пуст;
3. вывод `sudo ss -lntp`;
4. вывод `production_check.sh`, удалив только случайно попавшие секреты, если они появятся.

После моей проверки технический production launch считается завершённым.

---

# ЭТАП P. Закрытая бета

## Шаг P1. Подготовить тестовую аудиторию

1. Соберите 50–100 реальных пользователей.
2. Не включайте оплату.
3. Не объясняйте, какой ответ считается «правильным».
4. Дайте одну ссылку:

```text
https://app.metaphor.uz
```

5. Попросите каждого использовать минимум два разных режима.

## Шаг P2. Не собирать ответы вручную в чатах

Все пользователи должны использовать встроенные:

- copy/share;
- оценку результата;
- причины отрицательной оценки.

## Шаг P3. Набрать 500 completed generations

В операторской панели контролируются:

- completed generations;
- unique users;
- copy/share;
- positive feedback;
- AI cost.

### КОНТРОЛЬНАЯ ТОЧКА Q

После каждых первых 50, 200 и 500 генераций отправьте скриншот операторской панели. Я проверю воронку и дам только необходимые изменения.

---

# ЭТАП Q. Решение после 500 генераций

Зафиксированные ворота:

```text
Completion rate: не ниже 60%
Copy/share rate: целевой не ниже 35%; зона риска ниже 20%
Positive feedback: не ниже 70%
Критические языковые ошибки: ниже 3%
```

Решение:

- `MONETIZE` — показатели выполнены;
- `ITERATE` — есть использование, но провален один исправимый показатель;
- `STOP/PIVOT` — copy/share устойчиво ниже 20% и нет B2B-сигнала.

### КОНТРОЛЬНАЯ ТОЧКА R

Отправьте export/скрин панели на 500 completed. Я сам приму и обосную решение `MONETIZE / ITERATE / STOP-PIVOT`.

---

# ЭТАП R. Платежи — только после MONETIZE

Этот раздел не выполнять до контрольной точки R.

1. [ТРЕБУЕТ ПРОВЕРКИ] Подтвердить зарегистрированную организационно-правовую форму, которую Payme Business допускает к подключению; актуальный перечень форм и документов проверяется на момент подачи заявки.
2. Открыть Payme Business и заявку Merchant API.
3. Отправить мне скрин первого экрана заявки и перечень требуемых документов.
4. Я подготовлю технические поля, описание сервиса, публичную оферту, возврат и требования к серверной интеграции.
5. После получения merchant credentials не отправлять их в чат.
6. Я добавлю backend integration и отдельный release branch.
7. Sandbox должен пройти:
   - CreateTransaction;
   - PerformTransaction;
   - CheckTransaction;
   - CancelTransaction;
   - повторный callback;
   - неверная сумма;
   - reconciliation.
8. Цена первого теста: `19 900 сумов` за premium-result/пакет по утверждённой модели.
9. Оплата включается feature flag только после серверного подтверждения транзакции.

---

# ЭТАП S. Instagram, TikTok и YouTube automation

[ПРОВЕРЕНО: исходный код Metaphor AI OS v0.2.1] Текущий release публикует автоматически только в Telegram. Кодовых adapters Instagram/TikTok/YouTube в v0.2.1 нет; утверждать обратное нельзя.

До начала этого этапа нужны 30 дней стабильного Telegram-контура и не менее 50 последовательно корректных материалов.

## Внешние действия владельца

1. Создать отдельный professional Instagram account `Metaphor` и привязанный Facebook Page.
2. Создать Meta developer account/app и начать review permissions для content publishing.
3. Создать TikTok developer app и подать Content Posting API на review.
4. Создать YouTube channel, Google Cloud project, включить YouTube Data API v3 и создать OAuth credentials.
5. На каждом первом экране developer portal отправить мне скриншот без client secret.
6. После этого я добавлю adapters в новую ветку и дам отдельные точные OAuth-инструкции по фактическим интерфейсам платформ.
7. Первые 50 публикаций на каждой платформе остаются с human approval.
8. Browser automation, фермы аккаунтов и обход platform review не используются.

---

# ЭТАП T. Первый B2B-пилот

После стабильной беты:

1. выбрать один цветочный или подарочный сервис из существующих контактов;
2. отправить мне его сайт и контакт принимающего решение;
3. я подготовлю одно конкретное предложение и схему установки `/widget`;
4. партнёру назначается уникальный `partner_code`;
5. пилот длится 30 дней;
6. до пилота фиксируется baseline checkout completion;
7. после пилота сравниваются использование виджета и завершённые заказы;
8. далее только платный договор или закрытие пилота — бессрочная бесплатная интеграция запрещена.

---

# Регулярная работа одного оператора после запуска

## Ежедневно

1. открыть `/operator`;
2. проверить health, AI cost и ошибки;
3. проверить RU/UZ контент;
4. одобрить/отклонить;
5. прочитать отрицательные отзывы;
6. проверить случайные результаты;
7. разобрать escalations.

## Еженедельно

1. copy/share rate;
2. RU против UZ;
3. 20 плохих результатов;
4. одна growth-гипотеза;
5. пять B2B-контактов;
6. расход и маржа;
7. legal/privacy запросы.

## Ежемесячно

1. языковая проверка;
2. dependency/security update;
3. restore drill;
4. пересмотр AI-бюджета;
5. решение stop/continue/scale.

---

# Последовательность сопровождения

Выполняйте и присылайте результаты строго в этом порядке:

```text
A  Пакет и SHA-256
B  GitHub branch + зелёный CI
C  xAI team/billing/key created
D  Telegram bot/channel
E  Hetzner server/firewall/IP
F  SSH/Docker/Git clone
G1 DNS panel screenshot
G2 DNS record and resolution
H  Safe .env summary
I  Internal health + xAI generation
J  Telegram operator chat ID
K  Legal owner data and approved pages
L  Production HTTPS
M  Telegram webhook and RU/UZ test
N  Operator/content publish
O  Backup/restore/privacy storage
P  Final security check
Q  50/200/500 generation checkpoints
R  Monetization decision
S  Payments/social adapters/B2B by gates
```

Не выполнять несколько контрольных точек одновременно. После каждой моей проверки я дам только следующую точечную команду или исправление.

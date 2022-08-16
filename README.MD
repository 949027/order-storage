# Сервис отслеживания заказов
- отслеживает изменения таблицы созданной в Google Sheet;
- вносит изменения в базу данных (PostgreSQL);
- конвертирует стоимость заказа в рубли;
- уведомляет об истечении срока поставки в телеграм;


## Запуск в Docker
1) Установите [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/).
2) Скачайте проект:
```commandline
git clone https://github.com/949027/order-storage
```
3) Создайте файл `.env` в корне проекта со следующими настройками.

Необходимо:
- `POSTGRES_DB`- имя БД;
- `POSTGRES_USER` - имя пользователя БД;
- `POSTGRES_PASSWORD` - пароль пользователя БД;
- `SECRET_KEY` — [секретный ключ](https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECRET_KEY) проекта. Он отвечает за шифрование на сайте
- `GOOGLE_CLOUD_SERVICE_ACCOUNT` - [сервисный аккаунт Google Cloud](https://cloud.google.com/iam/docs/creating-managing-service-accounts).
- `SPREADSHEET_ID` - ID таблицы. Можно взять из URL таблицы. [См. пример](https://developers.google.com/sheets/api/guides/concepts).
- `GOOGLE_APPLICATION_CREDENTIALS`- путь к файлу с ключами (как получить ключи [см. здесь](https://cloud.google.com/docs/authentication/getting-started))
- `TELEGRAM_TOKEN` - токен для телеграм-бота (получить у `@BotFather` в Телеграме);
- `TELEGRAM_CHAT_ID` - id пользователя в телеграме, которому направлять сообщения (получить у `@username_to_id_bot` в Телеграме);

Необязательно:
- `CURRENCY_ID`- ID из [справочника по кодам валют ЦБ РФ](https://www.cbr.ru/scripts/XML_val.asp?d=0). По умолчанию - R01020A (доллар).
- `DELAY_TIME` - время между обновлениями данных в секундах. По умолчанию - 60.
- `DEBUG` - [дебаг-режим](https://docs.djangoproject.com/en/4.1/ref/settings/#debug). По умолчанию - True.
- `ALLOWED_HOSTS` - [список допустимых хостов](https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts). По умолчанию - 127.0.0.1, localhost.

2) Соберите и запустите контейнеры:
```commandline
docker-compose up
```
3) Выполните миграции:
```commandline
docker exec web python manage.py migrate
```
4) Создайте суперпользователя:
```commandline
docker exec -it web python manage.py createsuperuser
```
4) Перейти по адресу http://127.0.0.1:8000. Админ-панель доступна по адресу http://127.0.0.1:8000/admin/.



## Цели проекта

Код написан в качестве тестового задания.
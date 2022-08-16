import time
from datetime import datetime
import requests
import telegram
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from order_storage import settings
from orders.models import Order


def get_currency_price(currency_id):
    """Спарсить стоимость валюты с www.cbr.ru"""

    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='xml')
    selector = f'Valute[ID={currency_id}] Value'
    price = soup.select_one(selector).get_text()
    return float(price.replace(',', '.'))


def get_sheet(spread_sheet_id):
    """Получить таблицу из Google sheet"""

    creds, _ = google.auth.default()
    service = build('sheets', 'v4', credentials=creds)

    result = service.spreadsheets().values().batchGet(
        spreadsheetId=spread_sheet_id,
        ranges='A2:D',
    ).execute()
    return result['valueRanges'][0]['values']


def send_alert(bot, order_id):
    text = f'У заказа № {order_id} истек срок поставки'
    bot.send_message(
        chat_id=settings.TELEGRAM_CHAT_ID,
        text=text)


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Отдельный command для отслеживания изменений в Google sheets.
        1) получает таблицу из Google sheet;
        2) получает курс валюты;
        3) добавляет/обновляет/удаляет запись в БД;
        4) отправляет предупреждение в телеграм если истек срок поставки.
        """
        try:
            bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
            currency_price = get_currency_price(settings.CURRENCY_ID)
            sheet = get_sheet(settings.SPREADSHEET_ID)
        except HttpError as error:
            print(f'An error occurred: {error}')
            return error

        while True:
            order_ids = []
            for row in sheet:
                delivery_date = datetime.strptime(row[3], '%d.%m.%Y').date()
                usd_price = float(row[2])
                order, _ = Order.objects.update_or_create(
                    id=row[1],
                    defaults={
                        'usd_price': usd_price,
                        'rub_price': usd_price * currency_price,
                        'delivery_date': delivery_date,
                        'is_overdue': True if datetime.now().date() > delivery_date else False
                    }
                )
                order_ids.append(order.id)
                if order.is_overdue and not order.expiration_message_sent:
                    send_alert(bot, order.id)
                    order.expiration_message_sent = True
                    order.save()

            Order.objects.exclude(id__in=order_ids).delete()

            time.sleep(settings.DELAY_TIME)

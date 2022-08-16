from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import order_storage.settings
from orders.models import Order
from datetime import datetime
import requests


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
        ranges='A2:D14',#FIXME вычислять диапазон автоматом
    ).execute()
    return result['valueRanges'][0]['values']


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            spread_sheet_id = order_storage.settings.SPREADSHEET_ID
            sheet = get_sheet(spread_sheet_id)
            currency_id = 'R01235'
            currency_price = get_currency_price(currency_id)
            for order in sheet:
                delivery_date = datetime.strptime(order[3], '%d.%m.%Y').date()
                usd_price = float(order[2])
                Order.objects.create(
                    id=order[1],
                    usd_price=usd_price,
                    rub_price=usd_price * currency_price,
                    delivery_date=delivery_date,
                )
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

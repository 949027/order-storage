from django.db import models


class Order(models.Model):
    number = models.IntegerField('Номер заказа')
    usd_price = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    rub_price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    delivery_date = models.DateTimeField('Дата поставки')

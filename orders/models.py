from django.db import models


class Order(models.Model):
    id = models.IntegerField('Номер заказа', primary_key=True)
    usd_price = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )
    rub_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )
    delivery_date = models.DateField('Дата поставки')
    is_overdue = models.BooleanField('Срок истек', default=False)
    expiration_message_sent = models.BooleanField(
        'Уведомление о просрочке отправлено',
        default=False,
    )

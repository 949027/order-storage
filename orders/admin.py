from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'usd_price',
        'rub_price',
        'delivery_date',
        'is_overdue',
        'expiration_message_sent',
    ]

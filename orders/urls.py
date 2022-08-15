from django.urls import path

from .views import display_orders


app_name = 'orders'

urlpatterns = [
    path('', display_orders),
]

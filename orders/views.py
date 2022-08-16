from django.shortcuts import render

from .models import Order


def display_orders(request):
    orders = Order.objects.all()
    return render(request, 'index.html', context={'orders': orders})

from django.urls import path
from .views import fazerCompra

urlpatterns = [
    path('', fazerCompra, name='compras')
]
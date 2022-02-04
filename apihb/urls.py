from django.urls import path
from .views import converterMoeda, rendimentoCdi

urlpatterns = [
    path('converter', converterMoeda, name='converter-moeda'),
    path('cdi', rendimentoCdi, name='rendimento-cdi')
]
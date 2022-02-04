from django.contrib import admin

from .models import Transferencia, Saldo, Deposito

admin.site.register(Transferencia)
admin.site.register(Saldo)
admin.site.register(Deposito)
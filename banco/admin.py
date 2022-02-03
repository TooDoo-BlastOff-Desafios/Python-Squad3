from django.contrib import admin

from .models import Usuario, Endereco, Notificacao, Transferencia

admin.site.register(Usuario)
admin.site.register(Endereco)
admin.site.register(Notificacao)
admin.site.register(Transferencia)
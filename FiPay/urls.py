from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('banco.urls')),
    path('autenticacao/', include('autenticacao.urls')),    
    path('moeda/', include('apihb.urls')),
    path('cliente/', include('cliente.urls')),
    path('compras', include('compra.urls')),
    path('visualizar/', include('visualizarDados.urls'))
]


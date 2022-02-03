from django.urls import path

from .views import mostrarUsuarios, mostrarNotificacao, cadastrarUsuario
from .views import fazerDeposito, fazerTransferencia, fazerCompra
from .views import telaInicio

urlpatterns = [
    path('usuarios', mostrarUsuarios.as_view(), name='usuarios'),
    path('compras', fazerCompra, name='compras'),
    path('cadastrarUsuario', cadastrarUsuario, name='teste'),
    path('deposito', fazerDeposito, name='deposito'),
    path('transferencia', fazerTransferencia, name='transferencia'),
    path('telaInicio', telaInicio.as_view(), name='telaInicio')

]
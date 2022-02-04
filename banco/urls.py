from django.urls import path

from .views import mostrarUsuarios, mostrarNotificacao, telaInicio
from .views import fazerDeposito, fazerTransferencia, fazerCompra
from .views import cadastrarUsuario, atualizarSenha

urlpatterns = [
    path('telaInicio', telaInicio.as_view(), name='telaInicio'),
    path('usuarios', mostrarUsuarios.as_view(), name='usuarios'),    
    path('notificacao', mostrarNotificacao.as_view(), name='notificacao'),    
    path('compras', fazerCompra, name='compras'),    
    path('deposito', fazerDeposito, name='deposito'),
    path('cadastrarUsuario', cadastrarUsuario, name='teste'),
    path('atualizarSenha', atualizarSenha, name='atualizar-senha'),
    path('transferencia', fazerTransferencia, name='transferencia'),
]
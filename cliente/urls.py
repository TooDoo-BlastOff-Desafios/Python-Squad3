from django.urls import path
from .views import cadastrarUsuario, atualizarSenha

urlpatterns = [
    path('cadastrarUsuario', cadastrarUsuario, name='teste'),
    path('atualizarSenha', atualizarSenha, name='atualizar-senha')
]
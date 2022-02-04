from django.urls import path

from .views import mostrarUsuarios, mostrarNotificacao, telaInicio

urlpatterns = [
    path('telaInicio', telaInicio.as_view(), name='telaInicio'),
    path('usuarios', mostrarUsuarios.as_view(), name='usuarios'),    
    path('notificacao', mostrarNotificacao.as_view(), name='notificacao'),    
]
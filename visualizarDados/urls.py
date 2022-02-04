from django.urls import path

from .views import mostrarNotificacao, telaInicio

urlpatterns = [
    path('telaInicio', telaInicio.as_view(), name='telaInicio'),      
    path('notificacao', mostrarNotificacao.as_view(), name='notificacao'),    
]
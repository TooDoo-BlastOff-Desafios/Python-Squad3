from django.urls import path


from .views import fazerDeposito, fazerTransferencia

urlpatterns = [    
    path('deposito', fazerDeposito, name='deposito'),
    path('transferencia', fazerTransferencia, name='transferencia'),
]
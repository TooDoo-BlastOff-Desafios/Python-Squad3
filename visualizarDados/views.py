from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import generics
from datetime import date

from .models import Notificacao
from .complementos.serializers import notificacaoSerializer, usuarioRelacionado
from .complementos.serializers import telaInicio


class mostrarUsuarios(generics.ListAPIView):
    serializer_class = usuarioRelacionado.userSerializer

    def get_queryset(self):
        
        query_set = User.objects.filter(username=self.request.user )
        
        return query_set

class telaInicio(generics.ListAPIView):
    serializer_class = telaInicio.telaInicioSerializer
    
    def get_queryset(self):
        dataAtual = date.today()

        query_set = User.objects.filter(Q(username=self.request.user) & Q(compraMes__mesCompra= dataAtual.month) & Q(compraMes__anoCompra= dataAtual.year))
        if len(query_set) == 0:
            query_set = User.objects.filter(username=self.request.user)
        
        return query_set

class mostrarNotificacao(generics.ListAPIView):
    serializer_class = notificacaoSerializer.notificacaoSerializer

    def get_queryset(self):
        query_set = Notificacao.objects.filter(usuario=self.request.user)
        
        return query_set

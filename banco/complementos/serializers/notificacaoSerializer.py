from rest_framework import serializers
from banco.models import Notificacao
from django.contrib.auth.models import User


class notificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ['mensagem', 'data']

class telaInicioSerializer(serializers.ModelSerializer):
    notificacoes = notificacaoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['notificacoes']
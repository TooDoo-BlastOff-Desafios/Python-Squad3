from rest_framework import serializers
from banco.models import Usuario, Endereco, Notificacao, Deposito, Compra
from django.contrib.auth.models import User

class compraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['descricao', 'valor', 'data']


class notificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ['mensagem', 'data']

class depositoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposito
        fields = ['descricao', 'valor', 'data']

class enderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['pais', 'estado', 'cidade', 'rua']


class usuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['numeroConta', 'nome', 'cpf']


class userSerializer(serializers.ModelSerializer):
    enderecos = enderecoSerializer(many=True, read_only=True)
    notificacoes = notificacaoSerializer(many=True, read_only=True)
    usuarios = usuarioSerializer(many=True, read_only=True)
    depositos = depositoSerializer(many=True, read_only=True)
    compras = compraSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'usuarios', 'enderecos', 'notificacoes', 'depositos', 'compras']
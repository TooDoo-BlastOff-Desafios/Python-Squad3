from rest_framework import serializers
from compra.models import Compra, CompraMes
from cliente.models import Usuario
from django.contrib.auth.models import User

class compraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['descricao', 'valor', 'data']

class usuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['numeroConta', 'nome']

class CompraMesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompraMes
        fields = ['valorTotal']

class telaInicioSerializer(serializers.ModelSerializer):    
    usuarios = usuarioSerializer(many=True, read_only=True)
    compras = compraSerializer(many=True, read_only=True)
    compraMes = CompraMesSerializer(many=True, read_only=True)


    class Meta:
        model = User
        fields = ['usuarios', 'compras', 'compraMes']

    
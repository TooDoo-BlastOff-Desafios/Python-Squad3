from rest_framework import serializers
from banco.models import Usuario, Compra
from django.contrib.auth.models import User

class compraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['descricao', 'valor', 'data']

class usuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['numeroConta', 'nome']

class telaInicioSerializer(serializers.ModelSerializer):    
    usuarios = usuarioSerializer(many=True, read_only=True)
    compras = compraSerializer(many=True, read_only=True)


    class Meta:
        model = User
        fields = ['usuarios', 'compras']

    
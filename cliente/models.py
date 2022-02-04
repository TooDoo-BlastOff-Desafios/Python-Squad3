from django.db import models
from django.contrib.auth.models import User


class Endereco(models.Model):        
    pais = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    rua = models.CharField(max_length=100)    
    usuario = models.ForeignKey(User, related_name='enderecos', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.usuario)


class Usuario(models.Model):
    numeroConta = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    login = models.ForeignKey(User, related_name='usuarios', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.nome)

from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date, datetime

from banco.models import Saldo


class Compra(models.Model):
    descricao = models.TextField()
    valor = models.FloatField()
    data = models.DateField()
    usuario = models.ForeignKey(User, related_name='compras', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.usuario)

class CompraMes(models.Model):
    valorTotal = models.FloatField()
    mesCompra = models.IntegerField()
    anoCompra = models.IntegerField()
    usuario = models.ForeignKey(User, related_name='compraMes', on_delete=models.CASCADE)


@receiver(post_save, sender=Compra)
def descontarSaldoCompra(sender, instance, **kwargs):
    saldoUsuario = Saldo.objects.get(usuario=instance.usuario)
    saldoUsuario.saldo -= float(instance.valor)
    saldoUsuario.save()


@receiver(post_save, sender=Compra)
def valorTotalMes(sender, instance, **kwargs):
    dataAtual = date.today()
    try:
        verificarCompraMesAnoAtual = CompraMes.objects.get(
            Q(usuario = instance.usuario) & 
            Q(mesCompra = dataAtual.month) & 
            Q(anoCompra = dataAtual.year))
        
        verificarCompraMesAnoAtual.valorTotal += float(instance.valor)
        verificarCompraMesAnoAtual.save()
    except CompraMes.DoesNotExist:
        convertendoDataCompraDate = datetime.strptime(instance.data, '%Y-%m-%d').date()
       
        CompraMes.objects.create(
            valorTotal = instance.valor,
            mesCompra = convertendoDataCompraDate.month,
            anoCompra = convertendoDataCompraDate.year,
            usuario = instance.usuario
        )
    
    

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cliente.models import Usuario


class Saldo(models.Model):
    saldo = models.FloatField(default=1000)
    usuario = models.ForeignKey(User, related_name='saldo', on_delete=models.CASCADE)


class Transferencia(models.Model):
    remetente = models.ForeignKey(User, related_name='transferencias', on_delete=models.CASCADE)
    comentario = models.TextField()
    valor = models.FloatField()
    destinatario = models.ForeignKey(User, related_name='destinatario', on_delete=models.CASCADE)
    data = models.DateField()
    dataTransferencia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.remetente)


class Deposito(models.Model):
    descricao = models.TextField()
    valor = models.FloatField()
    data = models.DateField()
    usuario = models.ForeignKey(User, related_name='depositos', on_delete=models.CASCADE)
   
    def __str__(self):
        return str(self.usuario)


@receiver(post_save, sender=Transferencia)
def descontarSaldoRemetente(sender, instance, **kwargs):
    saldoRemetente = Saldo.objects.get(usuario=instance.remetente)
    saldoRemetente.saldo -= float(instance.valor)
    saldoRemetente.save()


@receiver(post_save, sender=Transferencia)
def AdicionarSaldoDestinatario(sender, instance, **kwargs):
    saldoDestinatario = Saldo.objects.get(usuario=instance.destinatario)
    saldoDestinatario.saldo += float(instance.valor)
    saldoDestinatario.save()


@receiver(post_save, sender=Deposito)
def AdicionarSaldoDeposito(sender, instance, **kwargs):
    SaldoAtual = Saldo.objects.get(usuario=instance.usuario)
    SaldoAtual.saldo += float(instance.valor)
    SaldoAtual.save()


@receiver(post_save, sender=Usuario)
def criarSaldo(sender, instance, created, **kwargs):
    if created:
        loginUsuario = User.objects.get(username=instance.login)
        Saldo.objects.create(
            usuario = loginUsuario
        )


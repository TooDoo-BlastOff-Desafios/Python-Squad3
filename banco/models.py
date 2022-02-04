from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Usuario(models.Model):
    numeroConta = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    login = models.ForeignKey(User, related_name='usuarios', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.nome)

class Saldo(models.Model):
    saldo = models.FloatField(default=1000)
    usuario = models.ForeignKey(User, related_name='saldo', on_delete=models.CASCADE)


class Endereco(models.Model):        
    pais = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    rua = models.CharField(max_length=100)    
    usuario = models.ForeignKey(User, related_name='enderecos', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.usuario)


class Transferencia(models.Model):
    remetente = models.ForeignKey(User, related_name='transferencias', on_delete=models.CASCADE)
    comentario = models.TextField()
    valor = models.FloatField()
    destinatario = models.ForeignKey(User, related_name='destinatario', on_delete=models.CASCADE)
    data = models.DateField()
    dataTransferencia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.remetente)


class Notificacao(models.Model):
    data = models.DateField(auto_now_add=True)
    mensagem = models.TextField()
    usuario = models.ForeignKey(User, related_name='notificacoes', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.usuario)

class Compra(models.Model):
    descricao = models.TextField()
    valor = models.FloatField()
    data = models.DateField()
    usuario = models.ForeignKey(User, related_name='compras', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.usuario)
        
   
class Deposito(models.Model):
    descricao = models.TextField()
    valor = models.FloatField()
    data = models.DateField()
    usuario = models.ForeignKey(User, related_name='depositos', on_delete=models.CASCADE)
   
    def __str__(self):
        return str(self.usuario)


@receiver(post_save, sender=Usuario)
def criarSaldo(sender, instance, created, **kwargs):
    if created:
        loginUsuario = User.objects.get(username=instance.login)
        Saldo.objects.create(
            usuario = loginUsuario
        )

@receiver(post_save, sender=Transferencia)
def criarNotificacao(sender, instance, created, **kwargs):
    if created:
        loginDestinario = User.objects.get(username=instance.destinatario)
        nomeUsuarioRemetente = Usuario.objects.get(login=instance.remetente)
        
        Notificacao.objects.create(
            mensagem = f'{nomeUsuarioRemetente} transferiu ${instance.valor} para você',
            usuario = loginDestinario
        )

@receiver(post_save, sender=Transferencia)
def descontarSaldoRemetente(sender, instance, **kwargs):
    saldoRemetente = Saldo.objects.get(usuario=instance.remetente)
    saldoRemetente.saldo -= float(instance.valor)
    saldoRemetente.save()

@receiver(post_save, sender=Compra)
def descontarSaldoCompra(sender, instance, **kwargs):
    saldoUsuario = Saldo.objects.get(usuario=instance.usuario)
    saldoUsuario.saldo -= float(instance.valor)
    saldoUsuario.save()

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


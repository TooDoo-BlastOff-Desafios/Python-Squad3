from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from banco.models import Transferencia, Usuario

class Notificacao(models.Model):
    data = models.DateField(auto_now_add=True)
    mensagem = models.TextField()
    usuario = models.ForeignKey(User, related_name='notificacoes', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.usuario)

@receiver(post_save, sender=Transferencia)
def criarNotificacao(sender, instance, created, **kwargs):
    if created:
        loginDestinario = User.objects.get(username=instance.destinatario)
        nomeUsuarioRemetente = Usuario.objects.get(login=instance.remetente)
        
        Notificacao.objects.create(
            mensagem = f'{nomeUsuarioRemetente} transferiu ${instance.valor} para você',
            usuario = loginDestinario
        )

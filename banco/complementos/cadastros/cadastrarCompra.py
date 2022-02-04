from django.contrib.auth.models import User

from banco.models import Compra

def efetuarCompra(dadosAnalisados):
    login = User.objects.get(username=dadosAnalisados['login'])
    
    salvarCompra = Compra(
        descricao = dadosAnalisados['descricao'],
        valor = dadosAnalisados['valor'],
        data = dadosAnalisados['data'],
        usuario = login
    )
    salvarCompra.save()
from django.contrib.auth.models import User

from banco.models import Deposito

def efetuarDeposito(dadosAnalisados):
    login = User.objects.get(username=dadosAnalisados['login'])
    
    salvarDeposito = Deposito(
        descricao = dadosAnalisados['descricao'],
        valor = dadosAnalisados['valor'],
        data = dadosAnalisados['data'],
        usuario = login
    )
    salvarDeposito.save()

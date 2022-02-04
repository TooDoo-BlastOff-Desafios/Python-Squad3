from django.contrib.auth.models import User

from banco.models import Deposito
from compra.converterData import converterData

def efetuarDeposito(dadosAnalisados):
    login = User.objects.get(username=dadosAnalisados['login'])
    
    dataConvertida = converterData(dadosAnalisados['data'])
    
    salvarDeposito = Deposito(
        descricao = dadosAnalisados['descricao'],
        valor = dadosAnalisados['valor'],
        data = dataConvertida,
        usuario = login
    )
    salvarDeposito.save()

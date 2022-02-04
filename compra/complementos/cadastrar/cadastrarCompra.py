from django.contrib.auth.models import User
from compra.converterData import converterData

from compra.models import Compra

def efetuarCompra(dadosAnalisados):
    login = User.objects.get(username=dadosAnalisados['login'])

    dataConvertida = converterData(dadosAnalisados['data'])

    salvarCompra = Compra(
        descricao = dadosAnalisados['descricao'],
        valor = dadosAnalisados['valor'],
        data = dataConvertida,
        usuario = login
    )
    salvarCompra.save()
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from banco.models import Saldo
from .complementos.cadastrar.cadastrarCompra import efetuarCompra
from .complementos.verificar.verificarDadosCompra import analisarDadosCompra


@api_view(['POST'])
def fazerCompra(request):
    dadosAnalisados = analisarDadosCompra(request)

    if dadosAnalisados == False:
        mensagemErro = {
            'Situação': 'Dados inválidos',
            'Dados necessário': [
                'descricao',
                'valor',
                'data',
            ]
        }

        return Response(mensagemErro, status=status.HTTP_400_BAD_REQUEST)

    saldoAtual = Saldo.objects.get(usuario=dadosAnalisados['login'])
    valorCompraFeita = saldoAtual.saldo - float(dadosAnalisados['valor'])

    if valorCompraFeita < 0:
        return Response('Você não tem saldo suficiente para essa compra', status=status.HTTP_400_BAD_REQUEST)

    efetuarCompra(dadosAnalisados)

    return Response('A compra foi feita com sucesso', status=status.HTTP_201_CREATED)

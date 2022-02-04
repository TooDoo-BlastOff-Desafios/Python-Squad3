from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Saldo
from cliente.models import Usuario
from .complementos.cadastros.cadastrarDeposito import efetuarDeposito
from .complementos.cadastros.cadastrarTransferencia import efetuarTransferencia
from .complementos.cadastros.verificarDadosDepositos import analisarDadosDeposito
from .complementos.cadastros.verificarDadosTransferencia import analisarDadosTransferencia


@api_view(['POST'])
def fazerDeposito(request):
    dadosAnalisados = analisarDadosDeposito(request)

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

    efetuarDeposito(dadosAnalisados)

    return Response('Depósito efetuado com sucesso', status=status.HTTP_201_CREATED)


@api_view(['POST'])
def fazerTransferencia(request):
    dadosAnalisados = analisarDadosTransferencia(request)
    if dadosAnalisados == False:
        mensagemErro = {
            'Situação': 'Dados inválidos',
            'Dados necessário': [
                'comentario', 'valor',
                'destinatario', 'data'
            ]
        }
        return Response(mensagemErro, status=status.HTTP_400_BAD_REQUEST)

    try:
        verificarDestinatario = Usuario.objects.get(cpf = dadosAnalisados['destinatario']).login
        loginDestinatario = User.objects.get(username=verificarDestinatario)

        if loginDestinatario == request.user:      
           return Response('Não é permitido transferir para a mesma conta', status=status.HTTP_400_BAD_REQUEST)

    except Usuario.DoesNotExist:
        return Response('Destinatário não encontrado', status=status.HTTP_404_NOT_FOUND)

    dadosAnalisados['destinatario'] = loginDestinatario

    saldoAtual = Saldo.objects.get(usuario=dadosAnalisados['remetente'])
    valorTransferenciaFeita = saldoAtual.saldo - float(dadosAnalisados['valor'])

    if valorTransferenciaFeita < 0:
        return Response('Você não tem saldo suficiente para fazer a transferência', status=status.HTTP_400_BAD_REQUEST)

    efetuarTransferencia(dadosAnalisados)
       
    return Response('Transferência efetuada com sucesso')


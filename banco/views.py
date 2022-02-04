from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Notificacao, Usuario, Saldo
from .complementos.serializers import notificacaoSerializer, usuarioRelacionado
from .complementos.serializers import telaInicio
from .complementos.cadastros.cadastrarUsuarios import Cadastro
from .complementos.cadastros.cadastrarCompra import efetuarCompra
from .complementos.cadastros.cadastrarDeposito import efetuarDeposito
from .complementos.cadastros.cadastrarTransferencia import efetuarTransferencia
from .complementos.cadastros.verificarDadosUsuario import analisarDados
from .complementos.cadastros.verificarDadosCompra import analisarDadosCompra
from .complementos.cadastros.verificarDadosDepositos import analisarDadosDeposito
from .complementos.cadastros.verificarDadosTransferencia import analisarDadosTransferencia
from .complementos.cadastros.verificarDadosAtualizarSenha import analisarDadosAtualizarSenha


class mostrarUsuarios(generics.ListAPIView):
    serializer_class = usuarioRelacionado.userSerializer

    def get_queryset(self): 
        query_set = User.objects.filter(username=self.request.user)
        
        return query_set

class telaInicio(generics.ListAPIView):
    serializer_class = telaInicio.telaInicioSerializer
    
    def get_queryset(self):              
        query_set = User.objects.filter(username=self.request.user)
        
        return query_set

class mostrarNotificacao(generics.ListAPIView):
    serializer_class = notificacaoSerializer.notificacaoSerializer

    def get_queryset(self):
        query_set = Notificacao.objects.filter(usuario=self.request.user)
        
        return query_set

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
@authentication_classes([])
@permission_classes([])
def cadastrarUsuario(request):
    dadosAnalisados = analisarDados(request)
    if dadosAnalisados == False:
        mensagemErro = {
            'Situação': 'Dados inválidos',
            'Dados necessário': [
                'login', 'senha', 'nome',
                'cpf', 'pais', 'estado',
                'cidade', 'rua'
            ]
        }
        return Response(mensagemErro, status=status.HTTP_400_BAD_REQUEST)
    
    cadastro = Cadastro()   
    cadastro.cadastroLogin(dadosAnalisados['login'], dadosAnalisados['senha'])
    cadastro.cadastroUsuario(dadosAnalisados['nome'], dadosAnalisados['cpf'])
    cadastro.cadastroEndereco(dadosAnalisados['pais'], dadosAnalisados['estado'],
                                dadosAnalisados['cidade'], dadosAnalisados['rua'])
    
    return Response('Usuário cadastrado com sucesso', status=status.HTTP_201_CREATED)


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

@api_view(['POST'])
def atualizarSenha(request):
    dadosAnalisados = analisarDadosAtualizarSenha(request)

    if dadosAnalisados == False:
        mensagemErro = {
            'Situação': 'Dados inválidos',
            'Dados necessário': [
                'login',
                'senha'
            ]
        }

        return Response(mensagemErro, status=status.HTTP_400_BAD_REQUEST)

    try:
        verificarUsuario = User.objects.get(username=dadosAnalisados['login'])        
    except User.DoesNotExist:
        return Response('Usuário não encontrado', status=status.HTTP_404_NOT_FOUND)

    verificarUsuario.set_password(dadosAnalisados['senha'])
    verificarUsuario.save()
    
    return Response('Senha atualizada com sucesso', status=status.HTTP_200_OK)

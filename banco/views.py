from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Notificacao, Usuario
from .complementos.serializers import usuarioRelacionado
from .complementos.serializers import telaInicio
from .complementos.cadastros.cadastrarUsuarios import Cadastro
from .complementos.cadastros.cadastrarCompra import efetuarCompra
from .complementos.cadastros.cadastrarDeposito import efetuarDeposito
from .complementos.cadastros.cadastrarTransferencia import efetuarTransferencia
from .complementos.cadastros.verificarDadosUsuario import analisarDados
from .complementos.cadastros.verificarDadosCompra import analisarDadosCompra
from .complementos.cadastros.verificarDadosDepositos import analisarDadosDeposito
from .complementos.cadastros.verificarDadosTransferencia import analisarDadosTransferencia


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
    serializer_class = usuarioRelacionado.notificacaoSerializer

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
        return Response('Destinatário não encontrado', status=status.HTTP_400_BAD_REQUEST)

    dadosAnalisados['destinatario'] = loginDestinatario

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

    efetuarCompra(dadosAnalisados)

    return Response('A compra foi feita com sucesso', status=status.HTTP_201_CREATED)

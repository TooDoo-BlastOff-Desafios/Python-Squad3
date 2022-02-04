from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .complementos.cadastrar.cadastrarUsuarios import Cadastro
from .complementos.verificar.verificarDadosUsuario import analisarDados
from .complementos.verificar.verificarDadosAtualizarSenha import analisarDadosAtualizarSenha


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
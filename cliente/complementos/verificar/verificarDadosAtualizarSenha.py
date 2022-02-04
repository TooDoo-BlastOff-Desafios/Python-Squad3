from django.utils.datastructures import MultiValueDictKeyError

def analisarDadosAtualizarSenha(requisicao):
    try:
        dadosAtualizar = {
            'login': requisicao.POST['login'],
            'senha': requisicao.POST['senha']            
        }
        return dadosAtualizar
    except MultiValueDictKeyError:
        return False
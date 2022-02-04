from django.utils.datastructures import MultiValueDictKeyError

def analisarDadosDeposito(requisicao):
    try:
        dadosDeposito = {
            'login': requisicao.user,
            'descricao': requisicao.POST['descricao'],
            'valor': requisicao.POST['valor'],
            'data': requisicao.POST['data'] 
        }
        return dadosDeposito
    except MultiValueDictKeyError:
        return False
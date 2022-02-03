from django.utils.datastructures import MultiValueDictKeyError

def analisarDadosCompra(requisicao):
    try:
        dadosCompra = {
            'login': requisicao.user,
            'descricao': requisicao.POST['descricao'],
            'valor': requisicao.POST['valor'],
            'data': requisicao.POST['data'] 
        }
        return dadosCompra
    except MultiValueDictKeyError:
        return False
from django.utils.datastructures import MultiValueDictKeyError

def analisarDadosCdiData(requisicao):
    try:
        dadosData = {
            'login': requisicao.user,
            'data_inicial': requisicao.POST['data_inicial'],
            'data_final': requisicao.POST['data_final']
        }
        return dadosData
    except MultiValueDictKeyError:
        return False
from django.utils.datastructures import MultiValueDictKeyError

def analisarDados(requisicao):
    try:        
        dados = {
            'login': requisicao.POST['login'],
            'senha': requisicao.POST['senha'],
            'nome': requisicao.POST['nome'],
            'cpf': requisicao.POST['cpf'],
            'pais': requisicao.POST['pais'],
            'estado': requisicao.POST['estado'],
            'cidade': requisicao.POST['cidade'],
            'rua': requisicao.POST['rua'],            
        }
        return dados
    except MultiValueDictKeyError:
        return False
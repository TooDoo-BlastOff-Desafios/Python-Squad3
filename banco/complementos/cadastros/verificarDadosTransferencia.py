from django.utils.datastructures import MultiValueDictKeyError

def analisarDadosTransferencia(requisicao):
    try:        
        dadosTransferencia = {
        'remetente': requisicao.user,
        'comentario': requisicao.POST['comentario'],
        'valor': requisicao.POST['valor'],
        'destinatario': requisicao.POST['destinatario'],       
        'data': requisicao.POST['data']
        }

        return dadosTransferencia     
    except MultiValueDictKeyError:
        return False
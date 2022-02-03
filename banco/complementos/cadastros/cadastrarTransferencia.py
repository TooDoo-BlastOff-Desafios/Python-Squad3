from django.contrib.auth.models import User

from banco.models import Transferencia

def efetuarTransferencia(dadosAnalisados):
    salvarTransferencia = Transferencia(
        remetente = dadosAnalisados['remetente'],
        comentario = dadosAnalisados['comentario'],
        valor = dadosAnalisados['valor'],
        destinatario = dadosAnalisados['destinatario'],       
        data = dadosAnalisados['data']
    )
    salvarTransferencia.save()
from banco.models import Transferencia

from compra.converterData import converterData

def efetuarTransferencia(dadosAnalisados):

    dataConvertida = converterData(dadosAnalisados['data'])

    salvarTransferencia = Transferencia(
        remetente = dadosAnalisados['remetente'],
        comentario = dadosAnalisados['comentario'],
        valor = dadosAnalisados['valor'],
        destinatario = dadosAnalisados['destinatario'],       
        data = dataConvertida
    )
    salvarTransferencia.save()
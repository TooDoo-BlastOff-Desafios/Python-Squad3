import requests
from datetime import datetime

from banco.models import Saldo

def calcularCdi(dataAnalisada):     
    saldoUsuario = Saldo.objects.get(usuario=dataAnalisada['login']).saldo

    url = 'https://api.hgbrasil.com/finance/taxes?key=5fd34699'
    retornoRequisicao = requests.get(url)
    dadosRequisicaoDicionario = retornoRequisicao.json()


    cdiDiario = dadosRequisicaoDicionario['results'][0]['cdi_daily']

    try:
        data_inicial = datetime.strptime(dataAnalisada['data_inicial'], '%m-%d-%Y')
        data_final = datetime.strptime(dataAnalisada['data_final'], '%m-%d-%Y')
    except ValueError:
        return False
    calcularDias = abs((data_final - data_inicial).days)

    
    TaxaRedimentoDiario = ((cdiDiario / 100)/12)/30

    redimentoTotal = (TaxaRedimentoDiario * calcularDias * saldoUsuario) + saldoUsuario
    redimentoTotalArrendondado = round(redimentoTotal, 2)

    dadosRedimento = {
        'rendimento': redimentoTotalArrendondado,
        'saldo': saldoUsuario
    }

    return dadosRedimento
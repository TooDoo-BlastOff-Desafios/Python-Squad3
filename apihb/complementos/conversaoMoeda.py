import requests

from banco.models import Saldo

def convertendoMoeda(requisicao):
    saldoUsuario = Saldo.objects.get(usuario=requisicao.user).saldo

    url = 'https://api.hgbrasil.com/finance/quotations?key=5fd34699'
    retornoRequisicao = requests.get(url)
    dadosRequisicaoDicionario = retornoRequisicao.json()

    dicionarioMoedas = dadosRequisicaoDicionario['results']['currencies']  
    dicionarioValoresMoeda = dict()

    for moeda in dicionarioMoedas:
        if moeda == 'source':
            dicionarioValoresMoeda[dicionarioMoedas[moeda]] = float(saldoUsuario)
        else:        
            casasDecimais = 5 if moeda == 'BTC' else 2

            valorMoeda = dicionarioMoedas[moeda]['buy']
            converterMoeda = float(saldoUsuario) / valorMoeda

            dicionarioValoresMoeda[moeda] = round(converterMoeda,casasDecimais)

    return dicionarioValoresMoeda

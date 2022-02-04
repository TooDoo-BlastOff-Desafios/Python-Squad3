from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .complementos.conversaoMoeda import convertendoMoeda
from .complementos.calcularCdi import calcularCdi
from .complementos.verificarDadosCdiData import analisarDadosCdiData
from .complementos.serializers.conversaoSerializer import conversaoSerializer

@api_view(['GET'])
def converterMoeda(request):
    moedasConvertidas = convertendoMoeda(request)
    
    serializer = conversaoSerializer(moedasConvertidas).data

    return Response(serializer, status=status.HTTP_200_OK)

@api_view(['POST'])
def rendimentoCdi(request):
    dataAnalisada = analisarDadosCdiData(request)
    if dataAnalisada == False:        
        mensagemErro = {
            'Situação': 'Dados inválidos',
            'Dados necessário': [
                'data_inicial',
                'data_final'                
            ]
        }

        return Response(mensagemErro, status=status.HTTP_400_BAD_REQUEST)
    
    cdiCalculado = calcularCdi(dataAnalisada)
    
    if cdiCalculado == False:
        return Response('Data formato inválido. Informe no formato MM-DD-YYYY', status=status.HTTP_400_BAD_REQUEST)

    return Response(cdiCalculado, status=status.HTTP_200_OK)

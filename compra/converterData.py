from datetime import datetime

def converterData(data):
    convertendoDataStrDate = datetime.strptime(data, '%d-%m-%Y').date()
    converterDataIso = convertendoDataStrDate.strftime('%Y-%m-%d')
    
    return converterDataIso
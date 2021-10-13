import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCódigoPagamento = re.compile(r'^\d{4}$',flags=re.MULTILINE)
findCompetencia= re.compile(r'\d{2}\/\d{4}',flags=re.MULTILINE)
findCógidoDeBarras = re.compile(r'^\d+\n{2}\d+\n{2}\d+\n{2}\d+$',flags=re.MULTILINE)
findTotalARecolher = re.compile(r'VALOR ARRECADADO\n{2}(\d+,\d+)')

def regex_gps(contra_cheque, obj_response):
    if re.search(r'FAZENDA - MF',contra_cheque) is not None and re.search(r'GUIA DA PREVID',contra_cheque) is not None and re.search(r'SEFIP', contra_cheque) is not None: 
        obj_response["Nome"]="GFIP_GPS"
        obj_response["Tipo"]="56"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        obj_response["CodigoReceita"]=findCódigoPagamento.search(contra_cheque).group()
        mes,ano = findCompetencia.search(contra_cheque).group().split("/")
        obj_response["Mes"]=mes
        obj_response["Ano"]=ano
        valorTotal = findTotalARecolher.search(contra_cheque).group().split('\n')[2]
        valorTotalNum=""
        for num in valorTotal:
            if num.isdigit():
                valorTotalNum += num
        obj_response["Total"]=valorTotalNum
        obj_response["CodigoBarras"]=findCógidoDeBarras.search(contra_cheque).group().replace('\n',' ').replace(" ","")
        return obj_response
    return None



import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}')
findCompetencia= re.compile(r'^\d{2}\/\d{4}',flags=re.MULTILINE)
findTotalARecolher = re.compile(r'Total Geral:\s*([\d.,]+)')
findValidade = re.compile(r'^\d{2}\/\d{2}\/\d{4}$',flags=re.MULTILINE)
findCógidoDeBarras = re.compile(r'\d+  \d+  \d+  \d+')

def regex_fgts_v2(contra_cheque, obj_response):
    if re.search(r'GFD - Guia do FGTS Digital',contra_cheque) is not None:
        obj_response["Nome"]="FGTS DIGITAL"
        obj_response["Tipo"]="61"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        Mes,ano = findCompetencia.search(contra_cheque).group().split("/")
        valorTotal = findTotalARecolher.search(contra_cheque).group().split('\n')[2]
        valorTotalNum=""
        for num in valorTotal:
            if num.isdigit():
                valorTotalNum += num
        obj_response["Total"]=valorTotalNum
        obj_response["Mes"]=Mes
        obj_response["Ano"]=ano
        DD,MM,AA=findValidade.search(contra_cheque).group().split('/')
        obj_response["Vencimento"]=AA+"-"+MM+"-"+DD
        obj_response["CodigoBarras"]=findCógidoDeBarras.search(contra_cheque).group().replace(" ","")
        return obj_response
    return None
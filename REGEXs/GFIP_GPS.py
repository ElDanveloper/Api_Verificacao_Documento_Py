import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCódigoPagamento = re.compile(r'^\d{4}$',flags=re.MULTILINE)
findCompetencia= re.compile(r'^\d{2}\/\d{4}',flags=re.MULTILINE)
findCógidoDeBarras = re.compile(r'^\d+\n{2}\d+\n{2}\d+\n{2}\d+$',flags=re.MULTILINE)
findTotalARecolher = re.compile(r'VALOR ARRECADADO\n{2}(\d+,\d+)')


def regex_gps(contra_cheque, obj_response):
    if re.search(r'MINISTÉRIO DA FAZENDA - MF',contra_cheque) is not None and re.search(r'GUIA DA PREVIDÊNCIA SOCIAL - GPS',contra_cheque) is not None: 
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
        #ISSO DEPOIS VAI SAIR
        # import json
        # arquivo = open(obj_response["Nome"]+".txt", "w")
        # obj_response["Mes"]=int(obj_response["Mes"])
        # obj_response["Ano"]=int(obj_response["Ano"])
        # obj_response["Valor"]=int(obj_response["Valor"])
        # obj_response["Multa"]=int(obj_response["Multa"])
        # obj_response["Total"]=int(obj_response["Total"])
        # json.dump(obj_response,arquivo,ensure_ascii=False)
        return obj_response
    return None



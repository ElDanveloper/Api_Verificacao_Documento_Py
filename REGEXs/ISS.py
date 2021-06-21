import re
from _removeMask import numberWithoutMask
findCompetencia= re.compile(r'^\d{4}\/\d{2}',flags=re.MULTILINE)
findCpfCnpj = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}|\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findNomeInteressado = re.compile(r'Razao Social Vencimento\n\n(\w+\s)+')
findValidade = re.compile(r'\d{2}\/\d{2}\/\d{4}$',flags=re.MULTILINE)
findCodigoReceita = re.compile(r' \d+\/\d+ ')
findTotalARecolher = re.compile(r'Total em R\$ \d+(,\d+)?')
#findCógidoDeBarras = re.compile(r'\d+  \d+  \d+  \d+')

def regex_iss(contra_cheque, obj_response):
    if re.search(r'DAM - Documento de Arrecadagao Municipal',contra_cheque) is not None: 
        obj_response["Nome"]="Guia ISS"
        obj_response["Tipo"]="5"
        obj_response["CodigoReceita"] = findCodigoReceita.search(contra_cheque).group().replace(" ","")
        obj_response["NomeInteressado"]= findNomeInteressado.search(contra_cheque).group().split('\n')[2]
        cnpj = findCpfCnpj.search(contra_cheque).group()
        cnpjNum=""
        for ch in cnpj:
            if ch.isdigit():
                cnpjNum += ch
        obj_response["CpfCnpjInteressado"]=cnpjNum

        obj_response["Ano"],obj_response["Mes"] = findCompetencia.search(contra_cheque).group().split("/")
        DD,MM,AA=findValidade.search(contra_cheque).group().split('/')
        obj_response["Vencimento"]=AA+"-"+MM+"-"+DD

        valorTotal = findTotalARecolher.search(contra_cheque).group().split(' ')[3]
        valorTotalNum=""
        for num in valorTotal:
            if num.isdigit():
                valorTotalNum += num
        obj_response["Total"]=valorTotalNum

        #obj_response["CodigoBarras"]=findCógidoDeBarras.search(contra_cheque).group().replace(" ","")
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



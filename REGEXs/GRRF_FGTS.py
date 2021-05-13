import re
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findTotalARecolher = re.compile(r'Total a Recolher\n\n(\d+.\d+,\d+)')
findValidade = re.compile(r'^\d{2}\/\d{2}\/\d{4}$',flags=re.MULTILINE)
findCodigoReceita = re.compile(r'11- Identificador\n\n\d+')
findCógidoDeBarras = re.compile(r'\d+ \d+ \d+ \d+')

def regex_grrf_fgts(contra_cheque, obj_response):
    if re.search(r'GRRF - Guia de Recolhimento Rescisório do FGTS',contra_cheque) is not None: 
        obj_response["Nome"]="GRRF FGTS"
        obj_response["Tipo"]="60"
        cnpj = findCnpj.search(contra_cheque).group()
        cnpjNum=""
        for ch in cnpj:
            if ch.isdigit():
                cnpjNum += ch
        obj_response["Cnpj"]=cnpjNum
        obj_response["CodigoReceita"]=findCodigoReceita.search(contra_cheque).group().split('\n')[2]
        valorTotal = findTotalARecolher.search(contra_cheque).group().split('\n')[2]
        valorTotalNum=""
        for num in valorTotal:
            if num.isdigit():
                valorTotalNum += num
        obj_response["Total"]=valorTotalNum
        DD,MM,AA=findValidade.search(contra_cheque).group().split('/')
        obj_response["Vencimento"]=AA+"-"+MM+"-"+DD
        obj_response["CodigoBarras"]=findCógidoDeBarras.search(contra_cheque).group().replace(" ","")
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
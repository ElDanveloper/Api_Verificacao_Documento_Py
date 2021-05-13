import re
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCodReceita = re.compile(r'Identificador:  (\d+)')
findNome = re.compile(r'Nome:\n\n((?:\w+\s)+)')
findValidade = re.compile(r'Movimentação:\n\n(\d{2}\/\d{2}\/\d{4})')
findPisPasep = re.compile(r'PIS\/PASEP:\n\n(\d+)')

def regex_grrf_relatorio(contra_cheque, obj_response):
    if re.search(r'Demonstrativo do Trabalhador de Recolhimento FGTS Rescisório',contra_cheque) is not None: 
        obj_response["Nome"]="GRRF_Relatorio"
        obj_response["Tipo"]="60"
        cnpj = findCnpj.search(contra_cheque).group()
        cnpjNum=""
        for ch in cnpj:
            if ch.isdigit():
                cnpjNum += ch
        obj_response["Cnpj"]=cnpjNum
        obj_response["CodigoReceita"] = findCodReceita.search(contra_cheque).group().split(" ")[2]
        obj_response["NomeInteressado"] = findNome.search(contra_cheque).group().split("\n")[2]
        DD,MM,AA=findValidade.search(contra_cheque).group().split("\n")[2].split("/")
        obj_response["Vencimento"]=AA+"-"+MM+"-"+DD
        obj_response["NisInteressado"] = findPisPasep.search(contra_cheque).group().split("\n")[2]
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




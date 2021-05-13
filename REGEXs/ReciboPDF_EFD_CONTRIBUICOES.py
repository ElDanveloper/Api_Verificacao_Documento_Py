import re
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCompetencia= re.compile(r'(\d{2}\/\d{4})$',flags=re.MULTILINE)
findCodigoReceita = re.compile(r'arquivo: ([\w\d]+)') 

def regex_efd_contribuicoes(contra_cheque, obj_response):
    if re.search(r'RECIBO DE ENTREGA DE ESCRITURAÇÃO FISCAL DIGITAL - CONTRIBUIÇÕES',contra_cheque) is not None : 
        obj_response["Nome"]="EFD_CONTRIBUICOES"
        obj_response["Tipo"]="14"
        cnpj = findCnpj.search(contra_cheque).group()
        cnpjNum=""
        for ch in cnpj:
            if ch.isdigit():
                cnpjNum += ch
        obj_response["Cnpj"]=cnpjNum
        obj_response["Descricao"] = findCodigoReceita.search(contra_cheque).group().split(" ")[1]
        print(findCodigoReceita.search(contra_cheque).group().split(" ")[1])
        mes,ano = findCompetencia.search(contra_cheque).group().split("/")
        obj_response["Mes"]=mes
        obj_response["Ano"]=ano
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



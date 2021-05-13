import re
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCompetencia= re.compile(r'^\d{2}\/\d{4}$',flags=re.MULTILINE)
findValidade = re.compile(r'em (\d{2}\/\d{2}\/\d{4})')
#findCnpj.search(contra_cheque).group()
def regex_envio_arquivos(contra_cheque, obj_response):
    if re.search(r'Protocolo de Envio de Arquivos',contra_cheque) is not None: 
        obj_response["Nome"]="GFIP_Protocolo_Caixa"
        obj_response["Tipo"]="59"
        cnpj = findCnpj.search(contra_cheque).group()
        cnpjNum=""
        for ch in cnpj:
            if ch.isdigit():
                cnpjNum += ch
        obj_response["Cnpj"]=cnpjNum
        mes,ano = findCompetencia.search(contra_cheque).group().split("/")
        DD,MM,AA=findValidade.search(contra_cheque).group().split(" ")[1].split("/")
        obj_response["Vencimento"]=AA+"-"+MM+"-"+DD
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



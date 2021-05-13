import re
findCnpj = re.compile(r'INSCRIÇÃO: (\d+)')
findCompetencia= re.compile(r':(\d{2}\/\d{4})$',flags=re.MULTILINE)

def regex_dma_resumo(contra_cheque, obj_response):
    if re.search(r'R E S U M O   P A R A   A C O M P A N H A M E N T O',contra_cheque) is not None : 
        obj_response["Nome"]="DMA-Resumo"
        obj_response["Tipo"]="12"
        obj_response["Cnpj"]=findCnpj.search(contra_cheque).group().split(" ")[1]
        mes,ano = findCompetencia.search(contra_cheque).group().replace(":","").split("/")
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



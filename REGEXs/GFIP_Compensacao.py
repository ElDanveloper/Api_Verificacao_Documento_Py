import re
from _removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCompetencia= re.compile(r'^\d{2}\/\d{4}$',flags=re.MULTILINE)

def regex_compensacao(contra_cheque, obj_response):
    if re.search(r'RELATÓRIO DE COMPENSAÇÕES',contra_cheque) is not None: 
        obj_response["Nome"]="GFIP_Compensacao"
        obj_response["Tipo"]="73"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
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



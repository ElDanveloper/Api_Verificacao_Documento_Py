import re
findCpf= re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}')

def regex_Irpf(contra_cheque, obj_response):
    if re.search(r'IMPOSTO SOBRE A  RENDA - PESSOA FÍSICA',contra_cheque) is not None: 
        obj_response["Nome"]="IRPF_Recibo"
        obj_response["CpfCnpj_Interessado"]=findCpf.search(contra_cheque).group()
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



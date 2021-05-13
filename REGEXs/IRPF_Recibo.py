import re
findCpf= re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}')
findAno = re.compile(r'EXERCÍCIO \d{4}')
findNome = re.compile(r'Sr\(a\) (\w+\s?)+')
findCep = re.compile(r'\d{5}-\d{3}')

def regex_Irpf(contra_cheque, obj_response):
    if re.search(r'IMPOSTO SOBRE A  RENDA - PESSOA FÍSICA',contra_cheque) is not None: 
        obj_response["Nome"]="IRPF_Recibo"
        obj_response["Tipo"]="4"
        obj_response["NomeInteressado"]=findNome.search(contra_cheque).group().replace("Sr(a) ","")
        obj_response["CEP"]=findCep.search(contra_cheque).group().replace("-","")
        #obj_response["CpfCnpj_Interessado"]=findCpf.search(contra_cheque).group()
        obj_response["Ano"] = findAno.search(contra_cheque).group().split(" ")[1]
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



import re
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findNome = re.compile(r'^([a-zA-Z]+\s)+$\nCPF',flags=re.MULTILINE)
findCompetencia= re.compile(r'\w+\sde\s\d{4}')

Mes_ext = {
    "Janeiro": "01",
    "Fevereiro": "02",
    "Março": "03", 
    "Abril": "04",
    "Maio": "05",
    "Junho": "06",
    "Julho": "07",
    "Agosto": "08",
    "Setembro": "09",
    "Outubro": "10",
    "Novembro": "11",
    "Dezembro": "12"
}

def regex_renuncia_vale(contra_cheque, obj_response):
    if re.search(r'DECLARAÇÃO DE RENUNCIA DO VALE TRANSPORTE',contra_cheque) is not None : 
        obj_response["Nome"]="Renuncia Vale Transporte"
        obj_response["Tipo"]="6"
        obj_response["NomeInteressado"] = findNome.search(contra_cheque).group().split("\n")[0]
        cnpj = findCnpj.search(contra_cheque).group()
        cnpjNum=""
        for ch in cnpj:
            if ch.isdigit():
                cnpjNum += ch
        obj_response["Cnpj"]=cnpjNum
        Mes, de, ano = findCompetencia.search(contra_cheque).group().split(" ")
        obj_response["Mes"]=Mes_ext[Mes]
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



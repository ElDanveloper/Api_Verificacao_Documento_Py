import re
from _removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findNome = re.compile(r'Sr\. (\w+\s)+')
findNisInteresado = re.compile(r'\d{3}.\d{5}.\d{2}-\d')

Mes_ext = {
    "Janeiro": "01",
    "janeiro": "01",
    "Fevereiro": "02",
    "fevereiro": "02",
    "Março": "03",
    "março": "03",  
    "Abril": "04",
    "abril": "04",
    "Maio": "05",
    "maio": "05",
    "Junho": "06",
    "junho": "06",
    "Julho": "07",
    "julho": "07",
    "Agosto": "08",
    "agosto": "08",
    "Setembro": "09",
    "setembro": "09",
    "Outubro": "10",
    "outubro": "10",
    "Novembro": "11",
    "novembro": "11",
    "Dezembro": "12",
    "dezembro": "12"
}
#or re.search(r'AVISO PRÉVIO DO EMPREGADOR PARA DISPENSA DO EMPREGADO',contra_cheque) is not None
def regex_empreg_indenizadoV2(contra_cheque, obj_response):
    if re.search(r'AVISO PRÉVIO DO EMPREGADOR PARA DISPENSA DO EMPREGADO',contra_cheque) is not None: 
        obj_response["Nome"]="Rescisao-Aviso Empregador Indenizado"
        obj_response["Tipo"]="42"
        obj_response["NomeInteressado"]=findNome.search(contra_cheque).group().replace("Sr. ","")
        obj_response["NisInteressado"]=findNisInteresado.search(contra_cheque).group()
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        # Mes, de, ano = findCompetencia.search(contra_cheque).group().split(" ")
        # obj_response["Mes"]=Mes_ext[Mes]
        # obj_response["Ano"]=ano
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
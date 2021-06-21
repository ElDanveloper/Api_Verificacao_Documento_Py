import re
from _removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCompetencia = re.compile(r'\w+\s\w{2}\s\d{4}')
findCompetencia_eSocial = re.compile(r'[A-Za-z]+\/\d{4}')

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

def regex_contra_cheque(contra_cheque, obj_response):
    if re.search(r'Folha Mensal',contra_cheque) is not None and re.search(r'CC:',contra_cheque) is not None and re.search(r'CBO',contra_cheque) is not None and re.search(r'Nome do Funcionário',contra_cheque) is not None: 
        obj_response["Nome"]="Contra Cheque Dominio"
        obj_response["Tipo"]="48"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        Mes, de, ano = findCompetencia.search(contra_cheque).group().split(" ")
        obj_response["Mes"]=Mes_ext[Mes]
        obj_response["Ano"]=ano
        return obj_response
    elif re.search(r'Demonstrativo dos Valores Devidos',contra_cheque) is not None:
        obj_response["Nome"]="Contra Cheque eSocial"
        obj_response["Tipo"]="48"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        Mes,ano = findCompetencia.search(contra_cheque).group().split("/")
        obj_response["Mes"]=Mes_ext[Mes]
        obj_response["Ano"]=ano
        return obj_response
    return None
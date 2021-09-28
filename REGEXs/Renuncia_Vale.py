import re
from REGEXs._removeMask import numberWithoutMask
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

def regex_renuncia_vale(pdfText, obj_response):
    if re.search(r'DECLARAÇÃO DE RENUNCIA DO VALE TRANSPORTE',pdfText) is not None and re.search(r'REGISTRO DE EMPREGADO',pdfText) is None: 
        obj_response["Nome"]="Renuncia Vale Transporte"
        obj_response["Tipo"]="6"
        obj_response["NomeInteressado"] = findNome.search(pdfText).group().split("\n")[0]
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(pdfText).group())
        Mes, de, ano = findCompetencia.search(pdfText).group().split(" ")
        obj_response["Mes"]=Mes_ext[Mes]
        obj_response["Ano"]=ano
        return obj_response
    return None



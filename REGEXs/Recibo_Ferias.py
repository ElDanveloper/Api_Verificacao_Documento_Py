import re
from _removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\n')
findCpf= re.compile(r'\d{3}.\d{3}.\d{3}.\d{2}')
findNomeInteressado = re.compile(r'Empregado: [\w\d\s]+- (\w+\s)+')
findCompetencia= re.compile(r'\w+\sde\s\d{4}')
findTotalARecolher = re.compile(r'Líquidos....:\n\n(\d+.\d+,\d+)')

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

def regex_recibo_ferias(contra_cheque, obj_response):
    if re.search(r'R E C I B O   D E   F E R I A S',contra_cheque) is not None : 
        obj_response["Nome"]="Recibo de Ferias"
        obj_response["CpfCnpjInteressado"]=findCpf.search(contra_cheque).group()
        obj_response["NomeInteressado"]=findNomeInteressado.search(contra_cheque).group().split("-")[1].replace("\n","")
        obj_response["Tipo"]="18"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        Mes, de, ano = findCompetencia.search(contra_cheque).group().split(" ")
        obj_response["Mes"]=Mes_ext[Mes]
        obj_response["Ano"]=ano
        valorTotal = findTotalARecolher.search(contra_cheque).group().split("\n")[2]
        valorTotalNum=""
        for num in valorTotal:
            if num.isdigit():
                valorTotalNum += num
        obj_response["Total"]=valorTotalNum
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



import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findTotalARecolher = re.compile(
    r'(?:(?:Líquido Geral:\n\n)(?:\d+.\d+,\d+\n)(\d+.\d+,\d+))|Geral:\n\n[\d*\.]*\d+,\d{2}')
findCompetencia = re.compile(r'^\d{2}\/\d{4}', flags=re.MULTILINE)


def regex_folha_pagamento(contra_cheque, obj_response):
    if re.search(r'Sistema licenciado para POLLO CONSULTORIA CONTABIL E SISTEMAS LTDA - ME', contra_cheque) is not None and re.search(r'Total Geral Descontos:', contra_cheque) is not None and re.search(r'Líquido Geral:', contra_cheque) is not None and re.search(r'Total Geral Proventos:', contra_cheque) is not None:
        obj_response["Descricao"] = "Folha de Pagamento Dominio"
        obj_response["Tipo"] = "49"
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        try:
            valorTotal = findTotalARecolher.search(
                contra_cheque).group().split("\n")[3]
        except:
            valorTotal = findTotalARecolher.search(
                contra_cheque).group().split('\n')[2]
        valorTotalNum = ""
        for num in valorTotal:
            if num.isdigit():
                valorTotalNum += num
        obj_response["Total"] = valorTotalNum
        mes, ano = findCompetencia.search(contra_cheque).group().split("/")
        obj_response["Mes"] = mes
        obj_response["Ano"] = ano
        return obj_response
    return None

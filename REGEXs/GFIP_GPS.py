import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCódigoPagamento = re.compile(r'^\d{4}$', flags=re.MULTILINE)
findCompetencia = re.compile(r'^\d{2}\/\d{4}', flags=re.MULTILINE)
findCógidoDeBarras = re.compile(
    r'^\d+\n{2}\d+\n{2}\d+\n{2}\d+$', flags=re.MULTILINE)
findTotalARecolher = re.compile(r'ARRECADADO\n{2}(\d+,\d{2})\n')

def regex_gps(contra_cheque, obj_response):
    if re.search(r'MINISTÉRIO DA FAZENDA - MF', contra_cheque) is not None and re.search(r'GUIA DA PREVIDÊNCIA SOCIAL - GPS', contra_cheque) is not None:
        obj_response["Descricao"] = "GFIP_GPS"
        obj_response["Tipo"] = "56"
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        obj_response["CodigoReceita"] = findCódigoPagamento.search(
            contra_cheque).group()
        mes, ano = findCompetencia.search(contra_cheque).group().split("/")
        obj_response["Competencia"] = findCompetencia.search(
            contra_cheque).group()
        obj_response["Mes"] = mes
        obj_response["Ano"] = ano
        obj_response["Total"] = findTotalARecolher.search(
            contra_cheque).group().replace('ARRECADADO\n\n', '')[:-1]
        obj_response["CodigoBarras"] = findCógidoDeBarras.search(
            contra_cheque).group().replace('\n', ' ').replace(" ", "")
        obj_response["Valor"] = obj_response["Total"]
        return obj_response
    return None

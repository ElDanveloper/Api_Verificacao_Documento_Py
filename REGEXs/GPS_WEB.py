import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCódigoPagamento = re.compile(r'\s\d{4}$', flags=re.MULTILINE)
findCompetencia = re.compile(r'\d{2}\/\d{4}', flags=re.MULTILINE)
findVencimento = re.compile(r'\d{2}\/\d{2}\/\d{4}')
findCodigoDeBarras = re.compile(
    r'^\d+\n{2}\d+\n{2}\d+\n{2}\d+$', flags=re.MULTILINE)
findJuros = re.compile(r'E\s(\d+,\d{2})\n')
findValor = re.compile(r'INSS\s(\d+\,\d{2}),')
findTotalARecolher = re.compile(r'TOTAL\s(\d+,\d{2})\n')


def regex_gps_web(contra_cheque, obj_response):
    if re.search(r'INSTITUTO NACIONAL DO SEGURO SOCIAL - INSS', contra_cheque) is not None and re.search(r'GPS', contra_cheque) is not None and re.search(r'GUIA DA PREVID', contra_cheque) is not None and re.search(r'IDENTIFICADOR', contra_cheque) is not None:
        obj_response["Descricao"] = "GPS_WEB"
        obj_response["Tipo"] = "56"
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        obj_response["CodigoReceita"] = findCódigoPagamento.search(
            contra_cheque).group().replace(" ", '')
        DD, MM, AA = findVencimento.search(contra_cheque).group().split("/")
        obj_response["Vencimento"] = AA+"-"+MM+"-"+DD
        mes, ano = findCompetencia.search(contra_cheque).group().split("/")
        obj_response["Mes"] = mes
        obj_response["Ano"] = ano
        obj_response["Valor"] = findValor.search(
            contra_cheque).group().replace("INSS ", "")[:-1]
        obj_response["Juros"] = findJuros.search(
            contra_cheque).group().replace("E ", "")[:-1]
        obj_response["Total"] = findTotalARecolher.search(
            contra_cheque).group().replace("TOTAL ", "")[:-1]
        return obj_response
    return None

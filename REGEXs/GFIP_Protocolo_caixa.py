import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCompetencia = re.compile(r'^\d{2}\/\d{4}$', flags=re.MULTILINE)
findValidade = re.compile(r'em (\d{2}\/\d{2}\/\d{4})')


def regex_envio_arquivos(contra_cheque, obj_response):
    if re.search(r'Protocolo de Envio de Arquivos', contra_cheque) is not None:
        obj_response["Descricao"] = "GFIP_Protocolo_Caixa"
        obj_response["Tipo"] = "59"
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        mes, ano = findCompetencia.search(contra_cheque).group().split("/")
        DD, MM, AA = findValidade.search(
            contra_cheque).group().split(" ")[1].split("/")
        obj_response["Vencimento"] = AA+"-"+MM+"-"+DD
        obj_response["Mes"] = mes
        obj_response["Ano"] = ano
        return obj_response
    return None

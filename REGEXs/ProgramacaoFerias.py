import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')


def regexProgramacaoFerias(contra_cheque, obj_response):
    if re.search(r'PROGRAMAÇÃO DE FÉRIAS', contra_cheque) is not None:
        obj_response["Descricao"] = "Programação de Férias"
        obj_response["Tipo"] = "69"
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        return obj_response
    return None

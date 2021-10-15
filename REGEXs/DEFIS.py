import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\n')
findAno = re.compile(r'Exercício (\d{4})')


def regex_defis(contra_cheque, obj_response):
    if re.search(r'DEFIS', contra_cheque) is not None:
        obj_response["Descricao"] = "DEFIS"
        obj_response["Tipo"] = "7"
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        obj_response["Ano"] = findAno.search(
            contra_cheque).group().split(" ")[1]
        return obj_response
    return None

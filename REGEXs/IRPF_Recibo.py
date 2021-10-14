import re
from REGEXs._removeMask import numberWithoutMask
findCpf = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}')
findAno = re.compile(r'EXERCÍCIO \d{4}')
findNome = re.compile(r'Sr\(a\) (\w+\s?)+')
findCep = re.compile(r'\d{5}-\d{3}')


def regex_Irpf(contra_cheque, obj_response):
    if re.search(r'IMPOSTO SOBRE A  RENDA - PESSOA FÍSICA', contra_cheque) is not None:
        obj_response["Descricao"] = "IRPF_Recibo"
        obj_response["Tipo"] = "4"
        obj_response["NomeInteressado"] = findNome.search(
            contra_cheque).group().replace("Sr(a) ", "")
        obj_response["CEP"] = findCep.search(
            contra_cheque).group().replace("-", "")
        obj_response["Ano"] = findAno.search(
            contra_cheque).group().split(" ")[1]
        return obj_response
    return None

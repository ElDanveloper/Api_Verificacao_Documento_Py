import re
from REGEXs._removeMask import numberWithoutMask
findNomeInteressado = re.compile(
    r'-\s[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+')
findCNPJ = re.compile(r'\d{2}.\d{3}.\d{3}\/\d{4}-\d{2}')
findEmpresa = re.compile(r'Empresa:\s[\w ]+')
findCPFInteressado = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}')


def regex_AvisoFerias(contra_cheque, obj_response):
    if re.search(r'A V I S O  D E  F E R I A S', contra_cheque) is not None or re.search(r'AVISO DE FÉRIAS', contra_cheque):
        obj_response["Descricao"] = "AvisoFerias"
        obj_response["Tipo"] = "19"
        obj_response["NomeInteressado"] = findNomeInteressado.search(
            contra_cheque).group().split("- ")[1][:-1]
        obj_response["Cnpj"] = numberWithoutMask(
            findCNPJ.search(contra_cheque).group())
        obj_response["Empresa"] = findEmpresa.search(
            contra_cheque).group().split(": ")[1]
        obj_response["CpfCnpjInteressado"] = numberWithoutMask(
            findCPFInteressado.search(contra_cheque).group())
        return obj_response
    return None

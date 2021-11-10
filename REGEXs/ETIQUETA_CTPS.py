import re
from REGEXs._removeMask import numberWithoutMask
findEmpresa = re.compile(
    r'Empregador:\n[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+[\.]*[-\s]*[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]*\n')
findCNPJ = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')


def etiqueta_CTPS(contra_cheque, obj_response):
    if re.search('CBO', contra_cheque) is not None and re.search('Folha/Livro nº', contra_cheque) is not None:
        obj_response["Tipo"] = '103'
        obj_response["Descricao"] = "Etiqueta CTPS"
        obj_response["Cnpj"] = numberWithoutMask(findCNPJ.search(
            contra_cheque).group())
        obj_response["Empresa"] = findEmpresa.search(
            contra_cheque).group().split(':\n')[1][:-1]
        return obj_response

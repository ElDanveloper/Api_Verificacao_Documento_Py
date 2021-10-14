import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCompetencia = re.compile(r'(\d{2}\/\d{4})$', flags=re.MULTILINE)
findCodigoReceita = re.compile(r'arquivo: ([\w\d]+)')


def regex_efd_contribuicoes(contra_cheque, obj_response):
    if re.search(r'RECIBO DE ENTREGA DE ESCRITURAÇÃO FISCAL DIGITAL - CONTRIBUIÇÕES', contra_cheque) is not None:
        obj_response["Nome"] = "EFD_CONTRIBUICOES"
        obj_response["Tipo"] = "14"
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        obj_response["Descricao"] = findCodigoReceita.search(
            contra_cheque).group().split(" ")[1]
        print(findCodigoReceita.search(contra_cheque).group().split(" ")[1])
        mes, ano = findCompetencia.search(contra_cheque).group().split("/")
        obj_response["Mes"] = mes
        obj_response["Ano"] = ano
        return obj_response
    return None

import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCompetencia = re.compile(r'COMP: \d{2}\/\d{4}', flags=re.MULTILINE)


def regex_re(contra_cheque, obj_response):
    if re.search(r'MINISTÉRIO DO TRABALHO E EMPREGO - MTE', contra_cheque) is not None and re.search(r'RELAÇÃO DOS TRABALHADORES CONSTANTES NO ARQUIVO SEFIP', contra_cheque) is not None:
        obj_response["Descricao"] = "RE"
        obj_response["Tipo"] = "59"
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        mes, ano = findCompetencia.search(
            contra_cheque).group().split(" ")[1].split("/")
        obj_response["Mes"] = mes
        obj_response["Ano"] = ano
        return obj_response
    return None

import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCpf = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}')
findNisInteresado = re.compile(r'\d{3}.\d{5}.\d{2}-\d')
findNome = re.compile(r'Nome do Segurado: (\w+\s)+')
findCompetencia = re.compile(
    r'Demissão:\n\d{2}\/\d{2}\/\d{4}$', flags=re.MULTILINE)


def regex_relacao_salarios_contribuicao(contra_cheque, obj_response):
    if re.search(r'RELAÇÃO DOS SALÁRIOS DE CONTRIBUIÇÃO', contra_cheque) is not None:
        obj_response["Nome"] = "Relacao dos salarios de contribuicao"
        obj_response["NomeInteressado"] = findNome.search(
            contra_cheque).group().split(": ")[1].replace("\n", "")
        obj_response["CpfCnpjInteressado"] = findCpf.search(
            contra_cheque).group()
        obj_response["Tipo"] = "22"
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        obj_response["NisInteressado"] = findNisInteresado.search(
            contra_cheque).group()
        DD, MM, AA = findCompetencia.search(
            contra_cheque).group().split('\n')[1].split('/')
        obj_response["Mes"] = MM
        obj_response["Ano"] = AA
        return obj_response
    return None

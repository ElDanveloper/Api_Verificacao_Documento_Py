import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCpf = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}')
findNisInteresado = re.compile(r'\d{3}.\d{5}.\d{2}-\d')
findNome = re.compile(r'11 Nome\n(\w+\s)+')
findCompetencia = re.compile(
    r'Afastamento\n\d{2}\/\d{2}\/\d{4}$', flags=re.MULTILINE)


def regex_termo_rescisao_verso(contra_cheque, obj_response):
    if re.search(r'TERMO DE QUITAÇÃO DE RESCISÃO DO CONTRATO DE TRABALHO', contra_cheque) is not None or re.search(r'TERMO DE HOMOLOGAÇÃO DE RESCISÃO DO CONTRATO DE TRABALHO', contra_cheque) is not None:
        obj_response["Nome"] = "Termo Rescisao Verso"
        obj_response["NomeInteressado"] = findNome.search(
            contra_cheque).group().split('\n')[1]
        obj_response["CpfCnpjInteressado"] = findCpf.search(
            contra_cheque).group()
        obj_response["Tipo"] = "53"
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

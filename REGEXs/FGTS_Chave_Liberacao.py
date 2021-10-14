import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findNisInteresado = re.compile(r'\d{3}.\d{5}.\d{2}-\d$', flags=re.MULTILINE)
findCompetencia = re.compile(r'\d{2}\/\d{2}\/\d{4}$', flags=re.MULTILINE)


def regex_fgts_chave(contra_cheque, obj_response):
    if re.search(r'Comunicar Movimentação do Trabalhador', contra_cheque) is not None:
        obj_response["Descricao"] = "FGTS_Chave_Liberacao"
        obj_response["Tipo"] = "21"
        obj_response["NisInteressado"] = findNisInteresado.search(
            contra_cheque).group()
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        DD, MM, AA = findCompetencia.search(contra_cheque).group().split('/')
        obj_response["Mes"] = MM
        obj_response["Ano"] = AA
        return obj_response
    return None

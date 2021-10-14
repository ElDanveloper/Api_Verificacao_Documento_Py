import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCompetencia = re.compile(r'^\d{2}\/\d{4}$', flags=re.MULTILINE)


def regex_gfip_rubrica(contra_cheque, obj_response):
    if re.search(r'COMPROVANTE DE DECLARAÇÃO DAS CONTRIBUIÇÕES A RECOLHER À PREVIDÊNCIA SOCIAL E A OUTRAS ENTIDADES E FUNDOS POR FPAS', contra_cheque) is not None:
        obj_response["Descricao"] = "Gfip Rubrica"
        obj_response["Tipo"] = "76"
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        mes, ano = findCompetencia.search(contra_cheque).group().split("/")
        obj_response["Mes"] = mes
        obj_response["Ano"] = ano
        return obj_response
    return None

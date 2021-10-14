import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'INSCRIÇÃO: (\d+)')
findCompetencia = re.compile(r':(\d{2}\/\d{4})$', flags=re.MULTILINE)


def regex_dma_resumo(contra_cheque, obj_response):
    if re.search(r'R E S U M O   P A R A   A C O M P A N H A M E N T O', contra_cheque) is not None:
        obj_response["Descricao"] = "DMA-Resumo"
        obj_response["Tipo"] = "12"
        obj_response["Cnpj"] = findCnpj.search(
            contra_cheque).group().split(" ")[1]
        mes, ano = findCompetencia.search(
            contra_cheque).group().replace(":", "").split("/")
        obj_response["Mes"] = mes
        obj_response["Ano"] = ano
        return obj_response
    return None

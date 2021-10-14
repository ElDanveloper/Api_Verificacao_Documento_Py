import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findNome = re.compile(
    r'Sra.\s[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+\n|Sr.\s[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+\n')
findNisInteresado = re.compile(r'\d{3}.\d{5}.\d{2}-\d')

Mes_ext = {
    "Janeiro": "01",
    "janeiro": "01",
    "Fevereiro": "02",
    "fevereiro": "02",
    "Março": "03",
    "março": "03",
    "Abril": "04",
    "abril": "04",
    "Maio": "05",
    "maio": "05",
    "Junho": "06",
    "junho": "06",
    "Julho": "07",
    "julho": "07",
    "Agosto": "08",
    "agosto": "08",
    "Setembro": "09",
    "setembro": "09",
    "Outubro": "10",
    "outubro": "10",
    "Novembro": "11",
    "novembro": "11",
    "Dezembro": "12",
    "dezembro": "12"
}
# or re.search(r'AVISO PRÉVIO DO EMPREGADOR PARA DISPENSA DO EMPREGADO',contra_cheque) is not None


def regex_empreg_indenizadoV2(contra_cheque, obj_response):
    if re.search(r'AVISO PRÉVIO DO EMPREGADOR PARA DISPENSA DO EMPREGADO', contra_cheque) is not None:
        obj_response["Descricao"] = "Rescisao-Aviso Empregador Indenizado"
        obj_response["Tipo"] = "42"
        obj_response["NomeInteressado"] = findNome.search(
            contra_cheque).group().split(". ")[1][:-1]
        obj_response["NisInteressado"] = findNisInteresado.search(
            contra_cheque).group()
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        return obj_response
    return None

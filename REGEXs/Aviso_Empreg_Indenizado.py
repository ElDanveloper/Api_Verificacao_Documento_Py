import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCompetencia = re.compile(r'\w+\s\w{2}\s\d{4}')
findNome = re.compile(
    r'Sra.\s[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ] +\n | Sr.\s[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ] +\n')
findNisInteresado = re.compile(r'\d{3}.\d{5}.\d{2}-\d')

Mes_ext = {
    "Janeiro": "01",
    "Fevereiro": "02",
    "Março": "03",
    "Abril": "04",
    "Maio": "05",
    "Junho": "06",
    "Julho": "07",
    "Agosto": "08",
    "Setembro": "09",
    "Outubro": "10",
    "Novembro": "11",
    "Dezembro": "12"
}


def regex_empreg_indenizado(contra_cheque, obj_response):
    if re.search(r'AVISO PRÉVIO DO EMPREGADOR INDENIZADO', contra_cheque) is not None:
        obj_response["Descricao"] = "Rescisao-Aviso Empregador Indenizado"
        obj_response["Tipo"] = "42"
        obj_response["NomeInteressado"] = findNome.search(
            contra_cheque).group().replace("Sr.(a) ", "")
        obj_response["NisInteressado"] = findNisInteresado.search(
            contra_cheque).group()
        obj_response["Cnpj"] = numberWithoutMask(
            findCnpj.search(contra_cheque).group())
        Mes, de, ano = findCompetencia.search(contra_cheque).group().split(" ")
        obj_response["Mes"] = Mes_ext[Mes]
        obj_response["Ano"] = ano
        return obj_response
    return None

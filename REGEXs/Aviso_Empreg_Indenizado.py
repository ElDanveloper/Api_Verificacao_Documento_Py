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
# or re.search(r'AVISO PRÉVIO DO EMPREGADOR PARA DISPENSA DO EMPREGADO',contra_cheque) is not None


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
        # ISSO DEPOIS VAI SAIR
        # import json
        # arquivo = open(obj_response["Nome"]+".txt", "w")
        # obj_response["Mes"]=int(obj_response["Mes"])
        # obj_response["Ano"]=int(obj_response["Ano"])
        # obj_response["Valor"]=int(obj_response["Valor"])
        # obj_response["Multa"]=int(obj_response["Multa"])
        # obj_response["Total"]=int(obj_response["Total"])
        # json.dump(obj_response,arquivo,ensure_ascii=False)
        return obj_response
    return None

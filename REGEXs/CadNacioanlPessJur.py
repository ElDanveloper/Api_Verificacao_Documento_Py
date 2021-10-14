import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findEmpresa = re.compile(r'NOME EMPRESARIAL\n(\w+\s)+')
findPeriodoApuracao = re.compile(r'CADASTRAL \d{2}\/\d{2}\/\d{4}')


def regex_CadNacPessJur(contra_cheque, obj_response):
    if re.search(r'CADASTRO NACIONAL DA PESSOA JURIDICA', contra_cheque) is not None:
        obj_response["Descricao"] = "CertidaoFederalCond"
        obj_response["Tipo"] = "26"
        cnpj = findCnpj.search(contra_cheque).group()
        cnpjNum = ""
        for ch in cnpj:
            if ch.isdigit():
                cnpjNum += ch
        obj_response["Cnpj"] = cnpjNum
        obj_response["Empresa"] = findEmpresa.search(
            contra_cheque).group().split('\n')[1]
        Dia, Mes, Ano = findPeriodoApuracao.search(
            contra_cheque).group().split(' ')[1].split("/")
        obj_response["PeriodoApuracao"] = Ano+"-"+Mes+"-"+Dia
        return obj_response
    return None

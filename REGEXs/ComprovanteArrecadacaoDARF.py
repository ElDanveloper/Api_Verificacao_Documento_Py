import re
from REGEXs._removeMask import numberWithoutMask
from REGEXs._findCodBank import returnCodBank
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findPeriodoApuracaoVencimento = re.compile(r'\d{2}\/\d{2}\/\d{4}\n\n\d{2}\/\d{2}\/\d{4}')
findValorPago = re.compile(r'Total\n\d+(,?\d+)')
findBanco = re.compile(r'Banco\n\n(\w+\s)+')

def regex_compArrecDARF(contra_cheque, obj_response):
    if re.search(r'registro de Arrecadação \(DARF\)',contra_cheque) is not None: 
        obj_response["Descricao"] = "Comprovante de Arrecadação(DARF)"
        obj_response["Tipo"]="97"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        periodoApuracao,none,vencimento= findPeriodoApuracaoVencimento.search(contra_cheque).group().split("\n")
        dia,mes,ano=periodoApuracao.split("/")
        obj_response["PeriodoApuracao"]=ano+"-"+mes+"-"+dia
        obj_response["Mes"]=mes
        obj_response["Ano"]=ano

        dia,mes,ano=vencimento.split("/")
        obj_response["Vencimento"]=ano+"-"+mes+"-"+dia

        obj_response["CodigoBanco"]=returnCodBank(findBanco.search(contra_cheque).group().split("\n")[2])

        obj_response["Total"]=findValorPago.search(contra_cheque).group().split("\n")[1].replace(",","").replace(".","")
        return obj_response
    return None

import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findPisInteressado = re.compile(r'\d{3}\.\d{5}\.\d{2}-\d{1}')
findNome = re.compile(r'SALDO:\n.+\n\n(\w+\s)+',)

def regexExtratoFGTSTrabalhador(contra_cheque, obj_response):
    if re.search(r'Extrato FGTS do Trabalhador',contra_cheque) is not None: 
        obj_response["Descricao"] = "Extrato FGTS do Trabalhador"
        obj_response["Tipo"]="28"
        obj_response["NomeInteressado"]=findNome.search(contra_cheque).group().split("\n")[3]
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        obj_response["NisInteressado"]=findPisInteressado.search(contra_cheque).group()
        return obj_response
    return None

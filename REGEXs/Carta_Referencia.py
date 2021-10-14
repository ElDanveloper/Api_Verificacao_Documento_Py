import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findNomeInteressado = re.compile(r'sr\(a\)\. (...)+,')
findEmpresa = re.compile(r'CARTA DE REFERÊNCIA\n\n(\w+\s+)+')

def regex_CartaReferencia(contra_cheque, obj_response):
    if re.search(r'CARTA DE REFERÊNCIA',contra_cheque) is not None: 
        obj_response["Descricao"] = "CartaReferencia"
        obj_response["Tipo"]="24"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        obj_response["Empresa"]=findEmpresa.search(contra_cheque).group().split('\n')[2]
        obj_response["NomeInteressado"]=findNomeInteressado.search(contra_cheque).group().replace(",",".").split(".")[1]
        return obj_response
    return None




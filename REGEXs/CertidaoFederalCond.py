import re
from _removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findEmpresa = re.compile(r'Nome: (\w+\s)+')

def regex_CertidaoFederalCond(contra_cheque, obj_response):
    if re.search(r'CERTIDAO POSITIVA COM EFEITOS DE NEGATIVA',contra_cheque) is not None: 
        obj_response["Nome"]="CertidaoFederalCond"
        obj_response["Tipo"]="27"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        obj_response["Empresa"]=findEmpresa.search(contra_cheque).group().replace("Nome: ","").replace("\n","")
        return obj_response
    return None




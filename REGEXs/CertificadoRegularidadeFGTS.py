import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findPeriodoApuracao = re.compile(r'Informacao obtida em \d{2}\/\d{2}\/\d{4}')
#nome arquivo, CNPJ
def regex_certificadoRegFGTS(contra_cheque, obj_response):
    if re.search(r'Certificado de Regularidade do\nFGTS - CRF',contra_cheque) is not None: 
        obj_response["Descricao"] = "Certificado Regularidade FGTS"
        obj_response["Tipo"]="29"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        return obj_response
    return None




import re
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findEmpresa = re.compile(r'Nome: (\w+\s)+')

def regex_CertidaoFederalCond(contra_cheque, obj_response):
    if re.search(r'CERTIDAO POSITIVA COM EFEITOS DE NEGATIVA',contra_cheque) is not None: 
        obj_response["Nome"]="CertidaoFederalCond"
        obj_response["Tipo"]="27"
        cnpj = findCnpj.search(contra_cheque).group()
        cnpjNum=""
        for ch in cnpj:
            if ch.isdigit():
                cnpjNum += ch
        obj_response["Cnpj"]=cnpjNum
        obj_response["Empresa"]=findEmpresa.search(contra_cheque).group().replace("Nome: ","").replace("\n","")
        return obj_response
    return None




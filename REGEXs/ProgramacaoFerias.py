import re
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')

def regexProgramacaoFerias(contra_cheque, obj_response):
    if re.search(r'PROGRAMAÇÃO DE FÉRIAS',contra_cheque) is not None: 
        obj_response["Nome"]="Programação de Férias"
        obj_response["Tipo"]="69"
        cnpj = findCnpj.search(contra_cheque).group()
        cnpjNum=""
        for ch in cnpj:
            if ch.isdigit():
                cnpjNum += ch
        obj_response["Cnpj"]=cnpjNum
        return obj_response
    return None
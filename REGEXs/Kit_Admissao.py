import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findNome = re.compile(r'Sr.\(a\) (\w+\s)+',flags=re.MULTILINE)
findDataAdmissao = re.compile(r'Data de Admissão\n\d{2}\/\d{2}\/\d{4}')
findCpf = re.compile(r'\d{3}\.\d{3}\.\d{3}-\d{2}')

def regex_kit_admissao(pdfText, obj_response):
    if re.search(r'REGISTRO DE EMPREGADO',pdfText) is not None and re.search(r'Autenticar',pdfText) is not None: 
        obj_response["Nome"]="Kit Admissao"
        obj_response["Tipo"]="100"
        obj_response["NomeInteressado"] = findNome.search(pdfText).group().replace("Sr.(a) ","")
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(pdfText).group())
        obj_response["CpfCnpjInteressado"]=numberWithoutMask(findCpf.search(pdfText).group())
        dia,mes,ano=findDataAdmissao.search(pdfText).group().split("\n")[1].split("/")
        obj_response["Vencimento"]=ano+"-"+mes+"-"+dia
        return obj_response
    return None


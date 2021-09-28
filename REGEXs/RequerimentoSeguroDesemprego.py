import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findNomeInteressado = re.compile(r'2 (\w+\s)+$')
findNisInteressado = re.compile(r'\d{3}.\d{5}.\d{2}-\d')

#CNPJ, nomeFuncionario, nomeDocumento, PIS/NIS
def regex_req_seguro_desemprego(contra_cheque, obj_response):
    if re.search(r'Requerimento de Seguro-Desemprego - SD',contra_cheque) is not None: 
        obj_response["Nome"]="Requerimento de Seguro-Desemprego"
        obj_response["Tipo"]="34"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        obj_response["NomeInteressado"]=findNomeInteressado.search(contra_cheque).group().replace("2 ","")
        obj_response["NisInteressado"]=findNisInteressado.search(contra_cheque).group()
        return obj_response
    return None
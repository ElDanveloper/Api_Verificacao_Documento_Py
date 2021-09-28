import re
from REGEXs._removeMask import numberWithoutMask
findNomeInteressado = re.compile(r'Sr.: (\w+\s)+')

def regex_AvisoFerias(contra_cheque, obj_response):
    if re.search(r'AVISO DE FÉRIAS',contra_cheque) is not None: 
        obj_response["Nome"]="AvisoFerias"
        obj_response["Tipo"]="19"
        obj_response["NomeInteressado"]=findNomeInteressado.search(contra_cheque).group().split(":")[1].replace("\n","")
        return obj_response
    return None




import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCodReceita = re.compile(r'Identificador:  (\d+)')
findNome = re.compile(r'Nome:\n\n((?:\w+\s)+)')
findValidade = re.compile(r'Movimentação:\n\n(\d{2}\/\d{2}\/\d{4})')
findPisPasep = re.compile(r'PIS\/PASEP:\n\n(\d+)')

def regex_grrf_relatorio(contra_cheque, obj_response):
    if re.search(r'Demonstrativo do Trabalhador de Recolhimento FGTS Rescisório',contra_cheque) is not None: 
        obj_response["Nome"]="GRRF_Relatorio"
        obj_response["Tipo"]="99"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        obj_response["CodigoReceita"] = findCodReceita.search(contra_cheque).group().split(" ")[2]
        obj_response["NomeInteressado"] = findNome.search(contra_cheque).group().split("\n")[2]
        DD,MM,AA=findValidade.search(contra_cheque).group().split("\n")[2].split("/")
        obj_response["Vencimento"]=AA+"-"+MM+"-"+DD
        obj_response["NisInteressado"] = findPisPasep.search(contra_cheque).group().split("\n")[2]
        return obj_response
    return None




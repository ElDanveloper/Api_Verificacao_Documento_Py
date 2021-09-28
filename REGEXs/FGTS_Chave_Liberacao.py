import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findNisInteresado = re.compile(r'\d{3}.\d{5}.\d{2}-\d$',flags=re.MULTILINE)
findCompetencia = re.compile(r'\d{2}\/\d{2}\/\d{4}$',flags=re.MULTILINE)

def regex_fgts_chave(contra_cheque, obj_response):
    if re.search(r'Comunicar Movimentação do Trabalhador',contra_cheque) is not None: 
        obj_response["Nome"]="FGTS_Chave_Liberacao"
        obj_response["Tipo"]="21"
        obj_response["NisInteressado"]=findNisInteresado.search(contra_cheque).group()
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        DD,MM,AA=findCompetencia.search(contra_cheque).group().split('/')
        obj_response["Mes"]=MM
        obj_response["Ano"]=AA
        #ISSO DEPOIS VAI SAIR
        # import json
        # arquivo = open(obj_response["Nome"]+".txt", "w")
        # obj_response["Mes"]=int(obj_response["Mes"])
        # obj_response["Ano"]=int(obj_response["Ano"])
        # obj_response["Valor"]=int(obj_response["Valor"])
        # obj_response["Multa"]=int(obj_response["Multa"])
        # obj_response["Total"]=int(obj_response["Total"])
        # json.dump(obj_response,arquivo,ensure_ascii=False)
        return obj_response
    return None
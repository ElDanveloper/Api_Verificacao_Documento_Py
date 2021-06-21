import re
from _removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCompetencia= re.compile(r'^\d{2}\/\d{4}',flags=re.MULTILINE)
findTotalARecolher = re.compile(r'TOTAL A RECOLHER\nR\$ (\d+.\d+,\d+)')
findValidade = re.compile(r'DATA DE VENCIMENTO\n(\d{2}\/\d{2}\/\d{4})')
findCódigoPagamento = re.compile(r'^\d{4}$',flags=re.MULTILINE)

def regex_dae(contra_cheque, obj_response):
    if re.search(r'13-COMPRAS\/AQUISIÇÕES ACUMULADAS',contra_cheque) is not None and re.search(r'ESPECIFICAÇÃO DA RECEITA',contra_cheque) is not None and re.search(r'NOME, FIRMA OU RAZÃO SOCIAL',contra_cheque) is not None: 
        obj_response["Nome"]="DAE"
        obj_response["Tipo"]="58"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        Mes,ano = findCompetencia.search(contra_cheque).group().split("/")
        obj_response["Mes"]=Mes
        obj_response["Ano"]=ano
        DD,MM,AA=findValidade.search(contra_cheque).group().split('\n')[1].split('/')
        obj_response["Vencimento"]=AA+"-"+MM+"-"+DD
        valorTotal = findTotalARecolher.search(contra_cheque).group().split('\n')[1]
        valorTotalNum=""
        for num in valorTotal:
            if num.isdigit():
                valorTotalNum += num
        obj_response["Total"]=valorTotalNum
        obj_response["CodigoReceita"]=findCódigoPagamento.search(contra_cheque).group()
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



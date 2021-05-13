import re
findCpfCnpj = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}|\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findPeriodoApuracao = re.compile(r'Periodo de Apuracao\n\n\d{2}\/\d{2}\/\d{4}|VALOR TOTAL\n\n\d{2}\/\d{2}\/\d{4}')
findCodigoReceita = re.compile(r'^\d{4}$',flags=re.MULTILINE)
findValidade = re.compile(r'até \d{2}\/\d{2}\/\d{4}')
# findTotalARecolherOld = re.compile(r'Valor Total\n\n\d+(,\d+)?')
findTotalARecolher = re.compile(r'\d+\.\d+,\d+')
findCodigoBarras = re.compile(r'(\d{11}-\d    ){3}\d{11}-\d')

def regex_darf(contra_cheque, obj_response):
    if re.search(r'DARF',contra_cheque) is not None: 
        obj_response["Nome"]="DARF"
        obj_response["Tipo"]="55"
        obj_response["CodigoReceita"] = findCodigoReceita.search(contra_cheque).group()
        cnpj = findCpfCnpj.search(contra_cheque).group()
        cnpjNum=""
        for ch in cnpj:
            if ch.isdigit():
                cnpjNum += ch
        obj_response["CpfCnpjInteressado"]=cnpjNum
        dia,Mes,ano = findPeriodoApuracao.search(contra_cheque).group().split("\n")[2].split("/")
        obj_response["Mes"]=Mes
        obj_response["Ano"]=ano
        obj_response["PeriodoApuracao"]=ano+"-"+Mes+"-"+dia
        DD,MM,AA=findValidade.search(contra_cheque).group().split(' ')[1].split('/')
        obj_response["Vencimento"]=AA+"-"+MM+"-"+DD
        valorTotal = findTotalARecolher.search(contra_cheque).group()
        valorTotalNum=""
        for num in valorTotal:
            if num.isdigit():
                valorTotalNum += num
        obj_response["Total"]=valorTotalNum
        obj_response["CodigoBarras"]=findCodigoBarras.search(contra_cheque).group().replace(" ","").replace("-","")
        return obj_response
    return None



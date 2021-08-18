import re
from _removeMask import numberWithoutMask
findDarfCpfCnpj = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}|\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findDarfAntigoPeriodoApuracao = re.compile(r'Periodo de Apuracao\n\n\d{2}\/\d{2}\/\d{4}|VALOR TOTAL\n\n\d{2}\/\d{2}\/\d{4}')
findDarfAntigoCodigoReceita = re.compile(r'^\d{4}$',flags=re.MULTILINE)
findDarfAntigoValidade = re.compile(r'até \d{2}\/\d{2}\/\d{4}')
findDarfAntigoTotalARecolher = re.compile(r'\d+\.\d+,\d+')
findDarfAntigoCodigoBarras = re.compile(r'(\d{11}-\d    ){3}\d{11}-\d')

findDarfWebCodigoReceita = re.compile(r'[0-9]{2}[\.][0-9]{2}[\.][0-9]{5}[\.][0-9]{7}[\-][0-9]{1}')
darfWebApuracaoEValidade = re.compile(r'(\n\n\d{2}\/\d{2}\/\d{4}){2}')
findDarfWebValidade = re.compile(r'Pagar este documento at�\n\n\d{2}\/\d{2}\/\d{4}')
findDarfWebTotal = re.compile(r'Valor Total do Documento\n\n\d+\,\d+')
findDarfWebCodigoBarra = re.compile(r'(\d{11} \d{1}\n\n){4}')

def regex_darf(contra_cheque, obj_response):
    if re.search(r'Documento de Arrecadação de Receitas Federais',contra_cheque) is not None:
        # with open("darf.txt", "w") as f:
        #     f.write(contra_cheque)
        if re.search(r'DARF',contra_cheque) is not None: 
            obj_response["Nome"]="DARF"
            obj_response["Tipo"]="55"
            obj_response["CodigoReceita"] = findDarfAntigoCodigoReceita.search(contra_cheque).group()
            cnpj = findDarfCpfCnpj.search(contra_cheque).group()
            cnpjNum=""
            for ch in cnpj:
                if ch.isdigit():
                    cnpjNum += ch
            obj_response["Cnpj"]=cnpjNum
            dia,Mes,ano = findDarfAntigoPeriodoApuracao.search(contra_cheque).group()[:10].split("/")
            obj_response["Mes"]=Mes
            obj_response["Ano"]=ano
            obj_response["PeriodoApuracao"]=ano+"-"+Mes+"-"+dia
            DD,MM,AA=findDarfAntigoValidade.search(contra_cheque).group().split(' ')[1].split('/')
            obj_response["Vencimento"]=AA+"-"+MM+"-"+DD
            valorTotal = findDarfAntigoTotalARecolher.search(contra_cheque).group()
            valorTotalNum=""
            for num in valorTotal:
                if num.isdigit():
                    valorTotalNum += num
            obj_response["Total"]=valorTotalNum
            obj_response["CodigoBarras"]=findDarfAntigoCodigoBarras.search(contra_cheque).group().replace(" ","").replace("-","")
            return obj_response
        elif re.search(r'web', contra_cheque) is not None:
            obj_response["Nome"]="DARF"
            obj_response["Tipo"]="55"
            obj_response["CodigoReceita"] = findDarfWebCodigoReceita.search(contra_cheque).group().replace(".",'').replace("-","")
            obj_response["Cnpj"] = findDarfCpfCnpj.search(contra_cheque).group().replace(".","").replace("-","").replace("/","")
        
            apuracao, validade = filter(None, darfWebApuracaoEValidade.search(contra_cheque).group().split('\n'))
            dia,mes,ano = apuracao.split('/')
            obj_response["Mes"]=mes
            obj_response["Ano"]=ano
            obj_response["PeriodoApuracao"]=ano+"-"+mes+"-"+dia
            DD,MM,AA=validade.split('/')
            obj_response["Vencimento"]=AA+"-"+MM+"-"+DD
            obj_response["Total"]=findDarfWebTotal.search(contra_cheque).group().split("\n")[2].replace(",",".").replace(".","")
            obj_response["CodigoBarras"]= findDarfWebCodigoBarra.search(contra_cheque).group().replace(" ","").replace("\n","")
            return obj_response

        
    return None


import re
from _removeMask import numberWithoutMask
findDarfCpfCnpj = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}|\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findDarfAntigoPeriodoApuracao = re.compile(r'Periodo de Apuracao\n\n\d{2}\/\d{2}\/\d{4}|VALOR TOTAL\n\n\d{2}\/\d{2}\/\d{4}')
findDarfAntigoCodigoReceita = re.compile(r'^\d{4}$',flags=re.MULTILINE)
findDarfAntigoValidade = re.compile(r'até \d{2}\/\d{2}\/\d{4}')
findDarfAntigoTotalARecolher = re.compile(r'\d+\.\d+,\d+')
findDarfAntigoCodigoBarras = re.compile(r'(\d{11}-\d    ){3}\d{11}-\d')

def regex_darf(contra_cheque, obj_response):
    if re.search(r'Documento de Arrecadação de Receitas Federais',contra_cheque) is not None:
        with open("darf.txt", "w") as f:
            f.write(contra_cheque)
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
            findDarfWebCodigoReceita = re.compile(r'[0-9]{2}[\.][0-9]{2}[\.][0-9]{5}[\.][0-9]{7}[\-][0-9]{1}')
            darfWebApuracaoEValidade = re.compile(r'(\n\n\d{2}\/\d{2}\/\d{4}){2}')
            findDarfWebTotal = re.compile(r'Valor Total do Documento\n\n\d+\,\d+')
            findDarfWebCodigoBarra = re.compile(r'(\d{11} \d{1}\n\n){4}')

            obj_response["Nome"]="DARF-WEB"
            obj_response["Tipo"]="55"
            # obj_response["CodigoReceita"] = findDarfWebCodigoReceita.search(contra_cheque).group().replace(".",'').replace("-","")
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

        elif re.search(r'CNO', contra_cheque) is not None:
            regexVencimento = re.compile(r'Vencimento: \d{2}\/\d{2}\/\d{4}')
            regexCodigoReceita = re.compile(r'Numero: \d{2}[\.]\d{2}[\.]\d{5}[\.]\d{7}[-]\d')
            regexCnpj = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}|\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
            regexCompetencia = re.compile(r'PA:\d{2}[\/]\d{4}')
            regexValorTotal = re.compile(r'Valor: \d+\.\d+,\d+')
            regexBoleto = re.compile(r'(\d{11} \d{1}( |\n)){4}')

            obj_response["Nome"] = "CNO"
            obj_response["Tipo"] = "551"

            DD,MM,AA = regexVencimento.search(contra_cheque).group().split(' ')[1].split('/')
            obj_response["Vencimento"] = AA+"-"+MM+"-"+DD
            obj_response["CodigoReceita"] = regexCodigoReceita.search(contra_cheque).group().split(' ')[1].replace('.','').replace('-','')
            obj_response["Cnpj"] = regexCnpj.search(contra_cheque).group().replace('.','').replace('/','').replace('-','')
            mes,ano = regexCompetencia.search(contra_cheque).group().replace("PA:",'').split("/")

            obj_response["Mes"] = mes
            obj_response["Ano"] = ano

            obj_response["PeriodoApuracao"] = ano+"-"+mes
            obj_response["Total"] = regexValorTotal.search(contra_cheque).group().split(' ')[1].replace('.','').replace(',','.')
            obj_response["CodigoBarras"] = regexBoleto.search(contra_cheque).group().replace(' ','').replace('\n','')
            return obj_response

            
    return None


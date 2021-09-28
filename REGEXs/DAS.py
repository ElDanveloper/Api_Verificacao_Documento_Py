from REGEXs._removeMask import numberWithoutMask
import re
findCpfCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCpf = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}')
findTotalARecolher = re.compile(r'Valor Total do Documento\n\n.+')
findValidade = re.compile(r'Pagar este documento até\n\n\d{2}\/\d{2}\/\d{4}')
findCompetencia_eSocial = re.compile(r'Número do Documento\n\n.+')
# findCodigoReceita = re.compile(r'Observações\n\n(...)+')
findCodigodeBarras = re.compile(r'(\d{11} \d\n\n){4}')

mes_dict = {
    "Janeiro": "01",
    "Fevereiro": "02",
    "Março": "03", 
    "Abril": "04",
    "Maio": "05",
    "Junho": "06",
    "Julho": "07",
    "Agosto": "08",
    "Setembro": "09",
    "Outubro": "10",
    "Novembro": "11",
    "Dezembro": "12"
}

def regex_das(contra_cheque, obj_response):
    if re.search(r'Documento de Arrecadação do Simples Nacional',contra_cheque) is not None or re.search(r'Documento de Arrecadação do eSocial',contra_cheque) is not None: 
        if re.search(r'Documento de Arrecadação do eSocial',contra_cheque) is not None:
            obj_response["Nome"]="DAS-Domestico eSocial"
            obj_response["Tipo"]="41"
        elif (re.search(r'PARCSN',contra_cheque) is not None):
            obj_response["Nome"]="DAS PARCELAMENTO"
            obj_response["Tipo"]="84"
        elif (re.search(r'REC.DIVIDA ATIVA',contra_cheque) is not None):
            obj_response["Nome"]="Das SIMPLES PGFN"
            obj_response["Tipo"]="101"
        else:
            obj_response["Nome"]="DAS"
            obj_response["Tipo"]="57"
        obj_response["Cnpj"]=numberWithoutMask(findCpfCnpj.search(contra_cheque).group())
        try:
            cpf = findCpf.search(contra_cheque).group()
            cpfNum=""
            for ch in cpf:
                if ch.isdigit():
                    cpfNum += ch
            obj_response["CpfCnpjInteressado"]=cpfNum
            
        except: pass

        try:
            mes, ano = findCompetencia_eSocial.search(contra_cheque).group().split('\n')[2].split('/')
            print(mes)
            obj_response["Mes"] = mes_dict[mes]
            obj_response["Ano"] = ano
        except Exception as e: print(e)

        DD,MM,AA=findValidade.search(contra_cheque).group().split('\n')[2].split('/')
        obj_response["Vencimento"]=AA+"-"+MM+"-"+DD
        obj_response["Total"]=findTotalARecolher.search(contra_cheque).group().split('\n')[2].replace(",","").replace(".","")
        obj_response["CodigoBarras"]=findCodigodeBarras.search(contra_cheque).group().replace("\n","").replace(" ","")
        return obj_response
    return None

if __name__ == '__main__':
    with open("teste.txt", "r") as f:
        contra_cheque = f.read()
    result = regex_das(contra_cheque,{})
    print(result)

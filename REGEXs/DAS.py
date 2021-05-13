import re
findCpfCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCpf = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}')
findTotalARecolher = re.compile(r'Valor Total do Documento\n\n\d+(,\d+)?')
findValidade = re.compile(r'Pagar este documento até\n\n\d{2}\/\d{2}\/\d{4}')
findCompetencia_eSocial = re.compile(r'[A-Za-z]+\/\d{4}')
# findCodigoReceita = re.compile(r'Observações\n\n(...)+')
findCodigodeBarras = re.compile(r'(\d{11} \d\n\n){4}')

Mes_ext = {
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
        else:
            obj_response["Nome"]="DAS"
            obj_response["Tipo"]="57"
        cnpj = findCpfCnpj.search(contra_cheque).group()
        cnpjNum=""
        for ch in cnpj:
            if ch.isdigit():
                cnpjNum += ch
        obj_response["Cnpj"]=cnpjNum
        try:
            cpf = findCpf.search(contra_cheque).group()
            cpfNum=""
            for ch in cpf:
                if ch.isdigit():
                    cpfNum += ch
            obj_response["CpfCnpjInteressado"]=cpfNum
        except:
            pass
        mes,ano=findCompetencia_eSocial.search(contra_cheque).group().split(("/"))
        obj_response["Mes"]=Mes_ext[mes]
        obj_response["Ano"]=ano
        DD,MM,AA=findValidade.search(contra_cheque).group().split('\n')[2].split('/')
        obj_response["Vencimento"]=AA+"-"+MM+"-"+DD
        valorTotal = findTotalARecolher.search(contra_cheque).group().split('\n')[2]
        valorTotalNum=""
        for num in valorTotal:
            if num.isdigit():
                valorTotalNum += num
        obj_response["Total"]=valorTotalNum
        obj_response["CodigoBarras"]=findCodigodeBarras.search(contra_cheque).group().replace("\n","").replace(" ","")
        return obj_response
    return None



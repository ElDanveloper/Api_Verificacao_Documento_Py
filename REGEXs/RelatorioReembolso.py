import re
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCompetencia= re.compile(r'DATA:\n\n\d{2}\/\d{2}\/\d{4}',flags=re.MULTILINE)

def regex_relatorioReembolso(contra_cheque, obj_response):
    if re.search(r'MINISTÉRIO DA FAZENDA - MF',contra_cheque) is not None and re.search(r'GUIA DA PREVIDÊNCIA SOCIAL - GPS',contra_cheque) is None and re.search(r'SECRETARIA DA RECEITA FEDERAL DO BRASIL - RFB',contra_cheque) is not None: 
        obj_response["Nome"]="Relatorio Reembolso"
        obj_response["Tipo"]="70"
        cnpj = findCnpj.search(contra_cheque).group()
        cnpjNum=""
        for ch in cnpj:
            if ch.isdigit():
                cnpjNum += ch
        obj_response["Cnpj"]=cnpjNum
        dia,mes,ano = findCompetencia.search(contra_cheque).group().split('\n')[2].split("/")
        obj_response["Mes"]=mes
        obj_response["Ano"]=ano
        return obj_response
    return None



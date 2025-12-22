import re
import requests
from REGEXs._removeMask import numberWithoutMask

# Regexes
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}')
findCompetencia = re.compile(r'^\d{2}\/\d{4}', flags=re.MULTILINE)
# Ajustei para capturar o valor numérico diretamente no grupo 1
findTotalARecolher = re.compile(r'Total Geral:\s*([\d.,]+)') 
findValidade = re.compile(r'^\d{2}\/\d{2}\/\d{4}$', flags=re.MULTILINE)
findCógidoDeBarras = re.compile(r'\d+ \d+ \d+ \d+')

def buscar_matriz_na_api(cnpj_raiz):

    url = f"http://localhost:3000/api/client/deleted/false?cpf_cnpj={cnpj_raiz}"
    headers = {
        "Authorization": "Bearer K23913k921dklsadlasd32313dasKDSMDKMSd"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            lista_empresas = response.json()
            
            if not lista_empresas:
                return cnpj_raiz 
            
            for item in lista_empresas:
                doc = item.get('cpf_cnpj', '')
                if len(doc) == 14 and doc[8:12] == '0001':
                    return doc

            return lista_empresas[0].get('cpf_cnpj', cnpj_raiz)
            
    except Exception as e:
        print(f"Erro ao consultar API: {e}")
        return cnpj_raiz 
    
    return cnpj_raiz

def regex_fgts_v2(contra_cheque, obj_response):
    if re.search(r'GFD - Guia do FGTS Digital', contra_cheque) is not None:
        obj_response["Nome"] = "FGTS DIGITAL"
        obj_response["Tipo"] = "61"
        
        match_cnpj = findCnpj.search(contra_cheque)
        if match_cnpj:
            cnpj_extraido = numberWithoutMask(match_cnpj.group())
            
            if len(cnpj_extraido) == 8:
                cnpj_completo = buscar_matriz_na_api(cnpj_extraido)
                obj_response["Cnpj"] = cnpj_completo
            else:
                obj_response["Cnpj"] = cnpj_extraido
        
        match_comp = findCompetencia.search(contra_cheque)
        if match_comp:
            Mes, ano = match_comp.group().split("/")
            obj_response["Mes"] = Mes
            obj_response["Ano"] = ano

        match_total = findTotalARecolher.search(contra_cheque)
        if match_total:
            valor_texto = match_total.group(1) 
            
            valorTotalNum = "".join([num for num in valor_texto if num.isdigit()])
            obj_response["Total"] = valorTotalNum

        match_validade = findValidade.search(contra_cheque)
        if match_validade:
            DD, MM, AA = match_validade.group().split('/')
            obj_response["Vencimento"] = f"{AA}-{MM}-{DD}"

        match_barras = findCógidoDeBarras.search(contra_cheque)
        if match_barras:
            obj_response["CodigoBarras"] = match_barras.group().replace(" ", "")
            
        return obj_response
    
    return None
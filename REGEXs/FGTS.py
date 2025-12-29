import re
import requests 
from REGEXs._obterCnpj import buscar_matriz_na_api
from REGEXs._removeMask import numberWithoutMask

findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}(?:\/\d{4}-\d{2})?')

findCompetencia = re.compile(r'^\d{2}\/\d{4}', flags=re.MULTILINE)
findTotalARecolher = re.compile(r'15-TOTAL A RECOLHER\n\n.+')
findValidade = re.compile(r'^\d{2}\/\d{2}\/\d{4}$', flags=re.MULTILINE)
findCógidoDeBarras = re.compile(r'\d+ \d+ \d+ \d+')

# def buscar_matriz_na_api(cnpj_raiz):

#     url = f"http://localhost:3000/api/client/deleted/false?cpf_cnpj={cnpj_raiz}"
#     headers = {
#         "Authorization": "Bearer K23913k921dklsadlasd32313dasKDSMDKMSd"
#     }

#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         if response.status_code == 200:
#             empresas = response.json()
            
#             if not empresas:
#                 return cnpj_raiz # Se não achar nada, retorna o que tem
            
#             for emp in empresas:
#                 doc = emp.get('cpf_cnpj', '')
#                 # Verifica se tem 14 dígitos e se a filial é 0001
#                 if len(doc) == 14 and doc[8:12] == '0001':
#                     return doc

#             return empresas[0].get('cpf_cnpj', cnpj_raiz)
            
#     except Exception as e:
#         print(f"Erro ao consultar API Hunno: {e}")
#         return cnpj_raiz 
    
#     return cnpj_raiz

def regex_fgts(contra_cheque, obj_response):
    if re.search(r'GRF - GUIA DE RECOLHIMENTO DO FGTS', contra_cheque) is not None:
        obj_response["Descricao"] = "Guia Recolhimento do FGTS"
        obj_response["Tipo"] = "61"

        cnpj_encontrado = findCnpj.search(contra_cheque)
        
        if cnpj_encontrado:
            cnpj_limpo = numberWithoutMask(cnpj_encontrado.group())
            
            if len(cnpj_limpo) == 8:
                cnpj_matriz = buscar_matriz_na_api(cnpj_limpo)
                obj_response["Cnpj"] = cnpj_matriz
            else:
                obj_response["Cnpj"] = cnpj_limpo

        match_comp = findCompetencia.search(contra_cheque)
        if match_comp:
             Mes, ano = match_comp.group().split("/")
             obj_response["Mes"] = Mes
             obj_response["Ano"] = ano

        match_total = findTotalARecolher.search(contra_cheque)
        if match_total:
            valorTotal = match_total.group().split('\n')[2]
            valorTotalNum = "".join([num for num in valorTotal if num.isdigit()])
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
import requests

def buscar_matriz_na_api(cnpj_raiz):
    token = "K23913k921dklsadlasd32313dasKDSMDKMSd" 

    url = f"https://app.hunno.com.br/api/client/deleted/false?cpf_cnpj={cnpj_raiz}"
    
    headers = {
        "Authorization": f"Bearer {token}"
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
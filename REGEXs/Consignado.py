import re
from REGEXs._obterCnpj import buscar_matriz_na_api
from REGEXs._removeMask import numberWithoutMask

findCnpj = re.compile(r'Empregador:\s*(\d{2}\.\d{3}\.\d{3})', re.IGNORECASE)
findCompetencia = re.compile(r'Valor\s+Consignado\s+na\s+Guia\s+(\d{2}\/\d{4})', re.IGNORECASE)
findValidade = re.compile(r'^\d{2}\/\d{2}\/\d{4}$', flags=re.MULTILINE)
findValor = re.compile(r'Total\s+da\s+Guia\s*\(Consignado\):\s*([\d\.]+,\d{2})')
findValorBase = re.compile(r'Total\s+Consignado\s+([\d\.]+,\d{2})', re.IGNORECASE)


def regex_consignado(contra_cheque, obj_response):
    try:
        if re.search(r'Detalhe da Guia Emitida', contra_cheque) and re.search(r'Relação de Trabalhadores', contra_cheque) and re.search(r'Total\s+da\s+Guia\s*\(Consignado\)', contra_cheque):

            obj_response["Nome"] = "Detalhes Guia Consignado"
            obj_response["Tipo"] = "109"

            match_cnpj = findCnpj.search(contra_cheque)
            if match_cnpj:
                cnpj_extraido = numberWithoutMask(match_cnpj.group())
                
                if len(cnpj_extraido) == 8:
                    cnpj_completo = buscar_matriz_na_api(cnpj_extraido)
                    obj_response["Cnpj"] = cnpj_completo
                else:
                    obj_response["Cnpj"] = cnpj_extraido
            else:
                obj_response["Cnpj"] = "" 

            competencia_match = findCompetencia.search(contra_cheque)
            if competencia_match:
                try:
                    mes, ano = competencia_match.group(1).split("/")
                    obj_response["Mes"] = mes
                    obj_response["Ano"] = ano
                except ValueError:
                    obj_response["Mes"] = None
                    obj_response["Ano"] = None
                    obj_response["Erro"] = "Formato inesperado para a competência encontrada."
            else:
                obj_response["Mes"] = None
                obj_response["Ano"] = None
                obj_response["Erro"] = "Competência não encontrada no documento."
                    
            match_total_fgts = findValor.search(contra_cheque)
            if match_total_fgts:
                valor_fgts = match_total_fgts.group(1)            
                obj_response["Total"] = valor_fgts
            else:
                obj_response["Total"] = 0
                
            match_valor_base = findValorBase.search(contra_cheque)
            if match_valor_base:
                obj_response["Valor"] = match_valor_base.group(1)
            else:
                obj_response["Valor"] = 0
                
            match_validade = findValidade.search(contra_cheque)
            if match_validade:
                DD, MM, AA = match_validade.group().split('/')
                obj_response["Vencimento"] = f"{AA}-{MM}-{DD}"

            if obj_response.get("Mes") is not None:
                try:
                    obj_response["Mes"] = int(obj_response["Mes"])
                except ValueError:
                    obj_response["Erro"] = "Valor de 'Mes' não é um número válido."
            else:
                obj_response["Mes"] = 0 

            if obj_response.get("Ano") is not None:
                try:
                    obj_response["Ano"] = int(obj_response["Ano"])
                except ValueError:
                    obj_response["Erro"] = "Valor de 'Ano' não é um número válido."
            else:
                obj_response["Ano"] = 0 

            return obj_response

        return None

    except Exception as e:
        obj_response["Erro"] = f"Erro inesperado durante o processamento: {str(e)}"
        return obj_response
import re
from REGEXs._obterCnpj import buscar_matriz_na_api
from REGEXs._removeMask import numberWithoutMask

# Regexes Originais
findCnpj = re.compile(r'Empregador:\s*(\d{2}\.\d{3}\.\d{3})', re.IGNORECASE)
findCompetencia = re.compile(r'Comp.*\nApuração.*\n.*\n(\d{2}\/\d{4})')
findCompetenciaAlternativa = re.compile(r'(13º\/\d{4})')
findValidade = re.compile(r'^\d{2}\/\d{2}\/\d{4}$', flags=re.MULTILINE)
findValor = re.compile(r'Total\s+da\s+Guia\s*\(FGTS\):\s*([\d\.]+,\d{2})')
findValidacaoRescisorio = re.compile(r"\d{2}\/\d{2}\/\d{4}\s+Rescisório", re.IGNORECASE)

def regex_re_v2(contra_cheque, obj_response):
    try:
        if re.search(r'Detalhe da Guia Emitida', contra_cheque) and re.search(r'Relação de Trabalhadores', contra_cheque):

            if findValidacaoRescisorio.search(contra_cheque):
                return None 
            
            if re.search(r'Total da Guia \(Consignado\)', contra_cheque):
                return None

            obj_response["Nome"] = "RE DIGITAL"
            obj_response["Tipo"] = "59"

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
                competencia_alt_match = findCompetenciaAlternativa.search(contra_cheque)
                if competencia_alt_match:
                    try:
                        mes_ano = competencia_alt_match.group(1).split("º/")
                        obj_response["Mes"] = mes_ano[0]
                        obj_response["Ano"] = mes_ano[1]
                    except ValueError:
                        obj_response["Mes"] = None
                        obj_response["Ano"] = None
                        obj_response["Erro"] = "Formato inesperado para a competência alternativa encontrada."
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

            match_validade = findValidade.search(contra_cheque)
            if match_validade:
                DD, MM, AA = match_validade.group().split('/')
                obj_response["Vencimento"] = f"{AA}-{MM}-{DD}"

            if obj_response.get("Mes") is not None:
                try:
                    obj_response["Mes"] = int(obj_response["Mes"])
                    
                    if obj_response["Mes"] == 13:
                        obj_response["Mes"] = 12
                    # -----------------------------

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
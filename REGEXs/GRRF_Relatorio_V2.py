import re
from REGEXs._obterCnpj import buscar_matriz_na_api
from REGEXs._removeMask import numberWithoutMask

findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}(?:\/\d{4}-\d{2})?')
findCompetencia = re.compile(r'Comp.*\nApuração.*\n.*\n(\d{2}\/\d{4})')
findCompetenciaAlternativa = re.compile(r'(13º\/\d{4})')
findValidade = re.compile(r'^\d{2}\/\d{2}\/\d{4}$', flags=re.MULTILINE)
findValor = re.compile(r'Total\s+da\s+Guia\s*\(FGTS\):\s*([\d\.]+,\d{2})')
findValidacaoRescisorio = re.compile(r"\d{2}\/\d{2}\/\d{4}\s+Rescisório", re.IGNORECASE)

def regex_grrf_relatorio_v2(contra_cheque, obj_response):
    try:
        if re.search(r'Detalhe da Guia Emitida', contra_cheque) and re.search(r'Relação de Trabalhadores', contra_cheque):
            
            if not findValidacaoRescisorio.search(contra_cheque):
                return None

            obj_response["Nome"] = "GRRF_Relatorio"
            obj_response["Tipo"] = "99"

            match_cnpj = findCnpj.search(contra_cheque)
            if match_cnpj:
                cnpj_extraido = numberWithoutMask(match_cnpj.group())
                
                if len(cnpj_extraido) == 8:
                    cnpj_completo = buscar_matriz_na_api(cnpj_extraido)
                    obj_response["Cnpj"] = cnpj_completo
                else:
                    obj_response["Cnpj"] = cnpj_extraido
            else:
                obj_response["Cnpj"] = None

            competencia_match = findCompetencia.search(contra_cheque)
            if competencia_match:
                try:
                    mes, ano = competencia_match.group(1).split("/")
                    obj_response["Mes"] = int(mes)
                    obj_response["Ano"] = int(ano)
                except ValueError:
                    pass
            else:
                competencia_alt_match = findCompetenciaAlternativa.search(contra_cheque)
                if competencia_alt_match:
                    try:
                        mes_ano = competencia_alt_match.group(1).split("º/")
                        obj_response["Mes"] = int(mes_ano[0])
                        obj_response["Ano"] = int(mes_ano[1])
                    except ValueError:
                        pass

            if obj_response.get("Mes") is None:
                obj_response["Mes"] = 0
                obj_response["Ano"] = 0

            match_valor = findValor.search(contra_cheque)
            if match_valor:
                obj_response["Total"] = match_valor.group(1)
            else:
                obj_response["Total"] = "0"

            match_validade = findValidade.search(contra_cheque)
            if match_validade:
                DD, MM, AA = match_validade.group().split('/')
                obj_response["Vencimento"] = f"{AA}-{MM}-{DD}"

            return obj_response

        return None

    except Exception as e:
        obj_response["Erro"] = str(e)
        return obj_response
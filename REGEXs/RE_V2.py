# import re
# from REGEXs._removeMask import numberWithoutMask

# # Regex para encontrar CNPJ
# findCnpj = re.compile(r'\b\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\b')

# # Regex para encontrar competência no formato "MM/YYYY"
# findCompetencia = re.compile(r'Comp.*\nApuração.*\n.*\n(\d{2}\/\d{4})')

# # Regex alternativa para o formato "13º/2024"
# findCompetenciaAlternativa = re.compile(r'(13º\/\d{4})')

# def regex_re_v2(contra_cheque, obj_response):
#     try:
#         # Verifique padrões obrigatórios no texto
#         if re.search(r'Detalhe da Guia Emitida', contra_cheque) and re.search(r'Relação de Trabalhadores', contra_cheque):
#             obj_response["Nome"] = "RE DIGITAL"
#             obj_response["Tipo"] = "59"

#             # Encontrar CNPJ
#             cnpj_match = findCnpj.search(contra_cheque)
#             if cnpj_match:
#                 obj_response["Cnpj"] = numberWithoutMask(cnpj_match.group())
#             else:
#                 obj_response["Cnpj"] = None
#                 obj_response["Erro"] = "CNPJ não encontrado no documento."

#             # Encontrar competência
#             competencia_match = findCompetencia.search(contra_cheque)
#             if competencia_match:
#                 try:
#                     mes, ano = competencia_match.group(1).split("/")
#                     obj_response["Mes"] = mes
#                     obj_response["Ano"] = ano
#                 except ValueError:
#                     obj_response["Mes"] = None
#                     obj_response["Ano"] = None
#                     obj_response["Erro"] = "Formato inesperado para a competência encontrada."
#             else:
#                 # Tentar encontrar a competência no formato alternativo
#                 competencia_alt_match = findCompetenciaAlternativa.search(contra_cheque)
#                 if competencia_alt_match:
#                     try:
#                         mes_ano = competencia_alt_match.group(1).split("º/")
#                         obj_response["Mes"] = mes_ano[0]
#                         obj_response["Ano"] = mes_ano[1]
#                     except ValueError:
#                         obj_response["Mes"] = None
#                         obj_response["Ano"] = None
#                         obj_response["Erro"] = "Formato inesperado para a competência alternativa encontrada."
#                 else:
#                     obj_response["Mes"] = None
#                     obj_response["Ano"] = None
#                     obj_response["Erro"] = "Competência não encontrada no documento."

#             # Valida e converte Mes e Ano para inteiros, caso sejam encontrados
#             if obj_response.get("Mes") is not None:
#                 try:
#                     obj_response["Mes"] = int(obj_response["Mes"])
#                 except ValueError:
#                     obj_response["Erro"] = "Valor de 'Mes' não é um número válido."
#             else:
#                 obj_response["Mes"] = 0  # Valor padrão para Mes não encontrado

#             if obj_response.get("Ano") is not None:
#                 try:
#                     obj_response["Ano"] = int(obj_response["Ano"])
#                 except ValueError:
#                     obj_response["Erro"] = "Valor de 'Ano' não é um número válido."
#             else:
#                 obj_response["Ano"] = 0  # Valor padrão para Ano não encontrado

#             return obj_response

#         # Caso os padrões obrigatórios não sejam encontrados
#         obj_response["Erro"] = "Documento inválido: padrões obrigatórios ausentes."
#         return obj_response

#     except Exception as e:
#         # Log ou tratamento de erro genérico
#         obj_response["Erro"] = f"Erro inesperado durante o processamento: {str(e)}"
#         return obj_response

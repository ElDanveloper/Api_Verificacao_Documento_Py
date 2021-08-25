from ExtractTextFromPdf import Extract_text, FalhaNaLeituraPdf
from REGEXs._removeMask import numberWithoutMask
from REGEXs._expirationDate import expirationDate
from REGEXs._formatValue import formatValue
from convertPDFtoBase64 import pdf_to_base64
import requests
import re

from base_url import get_base_url
ROTA_API_HUNNO = get_base_url() + 'boletoproprio'

def populate(pdf_data, modelo, filename):
  findCodigoBarras = re.compile(r'\d{5}.\d{5} \d{5}.\d{6} \d{5}.\d{6} \d{1} \d{14}')
  boleto = re.sub(' +',' ',pdf_data)

  findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
  cnpjs = findCnpj.findall(boleto)
  CnpjPagador, CnpjFavorecido = cnpjs[3], cnpjs[2]

  modelo["CodigoBarras"] = numberWithoutMask(findCodigoBarras.search(boleto).group())
  modelo["CnpjPagador"] = numberWithoutMask(CnpjPagador)
  modelo["CnpjFavorecido"] = numberWithoutMask(CnpjFavorecido)
  modelo["Valor"] = formatValue((int(modelo['CodigoBarras'][37:47])))
  modelo["Vencimento"] = str(expirationDate(int(modelo['CodigoBarras'][33:37])))
  modelo["Arquivo"] = pdf_to_base64(filename)
  return modelo

def main(file, auth):
    pdfReader = Extract_text()
    resposta = {
      "CnpjPagador": "",
      "Valor": 0,
      "Vencimento": "",
      "CnpjFavorecido": "",
      "CodigoBarras": "",
      "Arquivo": ""
    }
    try:
        if file.endswith(".pdf") or file.endswith(".PDF"):
            pdf_data = pdfReader.pdf_miner(file)[0]
            resposta = populate(pdf_data, resposta, file)
            headers = {'Authorization': auth}
            return requests.post(ROTA_API_HUNNO, json=resposta, headers=headers).json()
        else:
            msg = f"Ocorreu um erro durante a leitura do arquivo {file}"
    except FalhaNaLeituraPdf:
        msg = f"Ocorreu um erro durante a leitura do arquivo file"
        return msg
        
    return resposta

if __name__ == "__main__":
    import requests
    auth = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJub21lIjoiTWFyY2lvIENvc3RhIFNpbHZhIiwiY3BmX2NucGoiOiI2MDYwMTk4MTU1MyIsImNvbnRyYWN0b3JfY25waiI6IjExMzc4MDA0MDAwMTI0IiwiaWQiOiIxIiwicGVyc29uX2lkIjoiMzMxIiwiZW1haWwiOiJtYXJjaW9AcG9sbG9jb250YWJpbC5jb20uYnIiLCJwaG9uZV9jZWxsIjoiNzU5OTE4NjQ2OTYiLCJ0eXBlX3VzZXIiOiJDIiwicGVyZmlsX3VzZXIiOiJEIiwiYWN0aXZlIjp0cnVlLCJ1c2VyX2lkX3N1cGVydmlzb3IiOiIxIiwidXNlcl9wYXNzd29yZCI6IiQyYSQxMCQyemg2Y0x4NFo5ZHp1RVFlcTR3elYuemc3ZE0zRFVwZWd0aWtDTjQ4OG5uWnNEam4yTlBNTyIsImRlcGFydG1lbnRfaWQiOiI3Iiwic2ltcGxlX25hbWUiOiJNw6FyY2lvIENvc3RhIiwiY2FtaW5ob19mb3RvIjpudWxsLCJjb250cmFjdG9yIjpbeyJpZCI6IjEiLCJwZXJzb25faWQiOiIxMTciLCJub21lIjoiUE9MTE8gQ09OU1VMVE9SSUEgQ09OVEFCSUwgRSBTSVNURU1BUyBMVERBIiwiY3BmX2NucGoiOiIxMTM3ODAwNDAwMDEyNCIsImRvY19mb3JtYXQiOiIxMS4zNzguMDA0LzAwMDEtMjQiLCJ0aXBvX2luc2NyaWNhbyI6bnVsbCwidGlwbyI6IkUiLCJjYW1pbmhvX2ZvdG8iOiJodHRwczovL2kuaW1ndXIuY29tL1NTbmlGb0QucG5nIiwiY3J0IjoiMSIsImNyY19zdWJzY3JpcHRpb24iOiIwMTgzOTIiLCJlbWFpbCI6Im1hcmNpb0Bwb2xsY29udGFiaWwuY29tLmJyIiwid2hhdHNhcHBfYnVzaW5lc3MiOiI3NTk5MTg2NDY5NiIsImluc3RhZ3JhbSI6bnVsbCwiZmFjZWJvb2siOm51bGwsInlvdXR1YmUiOm51bGwsImxpbmtlZGluIjpudWxsLCJnb29nbGVfYWNjb3VudCI6bnVsbCwiZGF0ZV9yZWdpc3RlciI6IjIwMTktMDctMTRUMTQ6NTY6MjQuMDAwWiIsImRhdGVfaW5pdGlhbF9jb250cmFjdCI6IjIwMTktMDctMTRUMTQ6NTY6MjkuMDAwWiIsImRhdGVfbGFzdF9jb250cmFjdCI6IjIwMTktMDctMTRUMTQ6NTY6MzQuMDAwWiIsImFjdGl2ZV9jb250cmFjdCI6bnVsbCwiZGVwYXJ0YW1lbnRvX2lkIjoiNyIsImRlcGFydGFtZW50b191c2VyX3Jlc3AiOiIxIiwiZGVwYXJ0YW1lbnRvX25vbWUiOiJBZG1pbmlzdHJhdGl2byIsImRlcGFydGFtZW50b190aXBvIjpudWxsfV0sImNsaWVudHMiOltdLCJpYXQiOjE2Mjk4OTQ0MDAsImV4cCI6MTYyOTk4MDgwMCwiY29udHJhY3Rvcl9pZCI6IjEifQ.0QOw_UgfRW4Bh1059fxxwGF31cA8pPUu40n_RenXVjU"
    teste = main("C:\\Users\\samue\\Downloads\\F B SUPERMECADO LTDA-00190000090321583700001948576176287050000079600.pdf",auth)
    response = requests.post(ROTA_API_HUNNO, json=teste)    
    print(response)
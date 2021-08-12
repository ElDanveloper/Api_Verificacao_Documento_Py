from ExtractTextFromPdf import Extract_text, FalhaNaLeituraPdf
from REGEXs._removeMask import numberWithoutMask
from REGEXs._expirationDate import expirationDate
from REGEXs._formatValue import formatValue
from convertPDFtoBase64 import pdf_to_base64
    
    
import requests
import re

ROTA_API_HUNNO_DEV = 'http://75.119.134.38:2004/dp/hunnodev/file/boletoproprio'

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
            return requests.post(ROTA_API_HUNNO_DEV, json=resposta, headers=headers).json()
        else:
            msg = f"Ocorreu um erro durante a leitura do arquivo {file}"
    except FalhaNaLeituraPdf:
        msg = f"Ocorreu um erro durante a leitura do arquivo file"
        return msg
        
    return resposta

if __name__ == "__main__":
    teste = main("X:\\samue\\Projetos\\Pollo C\\toqweb-python\\uploads\\F B SUPERMECADO LTDA-00190000090321583700001948576176287050000079600.pdf")
    
    # import requests
    # response = requests.post('http://75.119.134.38:2004/dp/hunnodev/file/boletoproprio', json=teste)    
    # print(response)
import json
from unidecode import unidecode
def returnCodBank(bankNameToSearch:str):
    with open("./REGEXs/bancos.txt","r", encoding='utf-8') as banks_txt:
        dict_banks = json.load(banks_txt)
        for bank in dict_banks["value"]:
            bankName=str(unidecode(bank["Nome"])).lower()
            if bankName==bankNameToSearch.lower() or bankName.__contains__(bankNameToSearch.lower()):
                return bank["Codigo"]
            
if __name__ == "__main__":
    print(returnCodBank("Banco"))
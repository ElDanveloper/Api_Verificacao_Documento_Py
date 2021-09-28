import re
from REGEXs._removeMask import numberWithoutMask
from validate_docbr import CPF,CNPJ
cpfValidate=CPF()
cnpjValidate=CNPJ()
findCnpj = re.compile(r'\d{2}.\d{3}.\d{3}\/\d{4}-\d{2}|\s\d{14}\s')
findCpf = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}|\s\d{11}\s')

def validateCpf(cpf: str) -> bool:
    # Verifica a formatação do CPF
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True
    
def remove_mask(word):
    word_without_masks=""
    for ch in word:
        if ch.isdigit():
            word_without_masks += ch
    return word_without_masks
def regex_generic(contra_cheque, obj_response):
    if findCnpj.search(contra_cheque) is not None:
        cnpjList=findCnpj.findall(contra_cheque)
        for cnpj in cnpjList:
            cnpj=remove_mask(cnpj)
            if cnpjValidate.validate(cnpj):#Se for um cpf válido
                obj_response["Cnpj"]=cnpj
                break
    if findCpf.search(contra_cheque) is not None:
        cpfList=findCpf.findall(contra_cheque)
        for cpf in cpfList:
            cpf=remove_mask(cpf)
            if cpfValidate.validate(cpf):  
                obj_response["CpfCnpjInteressado"]=cpf
                break
    return obj_response
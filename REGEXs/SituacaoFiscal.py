import re
from REGEXs._removeMask import numberWithoutMask
findCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCpfInteressadoAndNomeInteressado = re.compile(r'\d{3}\.\d{3}\.\d{3}-\d{2} - (\w+\s)+')

def regex_situacao_fiscal(contra_cheque, obj_response):
    if re.search(r'MINISTÉRIO DA ECONOMIA\nSECRETARIA ESPECIAL DA RECEITA FEDERAL DO BRASIL\nPROCURADORIA-GERAL DA FAZENDA NACIONAL\nINFORMAÇÕES DE APOIO PARA EMISSÃO DE CERTIDÃO',contra_cheque) is not None : 
        obj_response["Nome"]="Relatorio Situacao Fiscal"
        obj_response["Tipo"]="95"
        obj_response["Cnpj"]=numberWithoutMask(findCnpj.search(contra_cheque).group())
        cpf,obj_response["NomeInteressado"]=findCpfInteressadoAndNomeInteressado.search(contra_cheque).group().replace("\n","").split(" - ")
        cpfNum=""
        for ch in cpf:
            if ch.isdigit():
                cpfNum += ch
        obj_response["CpfCnpjInteressado"]=cpfNum
        return obj_response
    return None



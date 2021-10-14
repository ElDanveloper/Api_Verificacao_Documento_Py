import re
from REGEXs._removeMask import numberWithoutMask
findCpf = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}')


def regex_Irpf(contra_cheque, obj_response):
    if re.search(r'IMPOSTO SOBRE A  RENDA - PESSOA FÍSICA', contra_cheque) is not None:
        obj_response["Descricao"] = "IRPF_Recibo"
        obj_response["CpfCnpj_Interessado"] = findCpf.search(
            contra_cheque).group()
        return obj_response
    return None

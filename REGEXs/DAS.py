from REGEXs._removeMask import numberWithoutMask
import re
findCpfCnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findCpf = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}')
findTotalARecolher = re.compile(r'Valor Total do Documento\n\n.+')
findTotalARecolher2 = re.compile(r'Totais [\d*\.]*\d+,\d{2}')
findValidade1 = re.compile(
    r'Pagar este documento até\n\n\d{2}\/\d{2}\/\d{4}')
findValidade2 = re.compile(r'Pagar até: \d{2}\/\d{2}\/\d{4}')
findCompetencia_eSocial = re.compile(r'Número do Documento\n\n.+')
findCodigodeBarras = re.compile(r'(\d{11} \d\n\n){4}')
findCodigoDeBarras2 = re.compile(
    r'\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1}')
mes_dict = {
    "Janeiro": "01",
    "Fevereiro": "02",
    "Março": "03",
    "Abril": "04",
    "Maio": "05",
    "Junho": "06",
    "Julho": "07",
    "Agosto": "08",
    "Setembro": "09",
    "Outubro": "10",
    "Novembro": "11",
    "Dezembro": "12"
}


def regex_das(contra_cheque, obj_response):
    if re.search(r'Documento de Arrecada', contra_cheque) is not None and re.search('Simples Nacional', contra_cheque) or re.search(r'eSocial', contra_cheque) is not None:
        if re.search(r'eSocial', contra_cheque) is not None:
            obj_response["Descricao"] = "DAS-Domestico eSocial"
            obj_response["Tipo"] = "41"
        elif (re.search(r'PARCSN', contra_cheque) is not None):
            obj_response["Descricao"] = "DAS PARCELAMENTO"
            obj_response["Tipo"] = "84"
        elif (re.search(r'REC.DIVIDA ATIVA', contra_cheque) is not None):
            obj_response["Descricao"] = "Das SIMPLES PGFN"
            obj_response["Tipo"] = "101"
        else:
            obj_response["Descricao"] = "DAS"
            obj_response["Tipo"] = "57"
        obj_response["Cnpj"] = numberWithoutMask(
            findCpfCnpj.search(contra_cheque).group())
        try:
            cpf = findCpf.search(contra_cheque).group()
            cpfNum = ""
            for ch in cpf:
                if ch.isdigit():
                    cpfNum += ch
            obj_response["CpfCnpjInteressado"] = cpfNum
        except:
            pass
        try:
            mes, ano = findCompetencia_eSocial.search(
                contra_cheque).group().split('\n')[2].split('/')
            obj_response["Mes"] = mes_dict[mes]
            obj_response["Ano"] = ano
        except Exception:
            pass
        try:
            DD, MM, AA = findValidade1.search(
                contra_cheque).group().split('\n')[2].split('/')
        except:
            try:
                DD, MM, AA = findValidade2.search(
                    contra_cheque).group().split(': ')[1].split('/')
            except:
                pass
        obj_response["Vencimento"] = AA+"-"+MM+"-"+DD
        try:
            obj_response["Total"] = findTotalARecolher.search(
                contra_cheque).group().split('\n')[2].replace(",", "").replace(".", "")
        except:
            try:
                obj_response["Total"] = findTotalARecolher2.search(
                    contra_cheque).group().split(' ')[1].replace(",", "").replace(".", "")
            except:
                pass
        try:
            obj_response["CodigoBarras"] = findCodigodeBarras.search(
                contra_cheque).group().replace("\n", "").replace(" ", "")
        except:
            try:
                obj_response["CodigoBarras"] = findCodigoDeBarras2.search(
                    contra_cheque).group().replace(" ", "")
            except:
                pass
        return obj_response
    return None

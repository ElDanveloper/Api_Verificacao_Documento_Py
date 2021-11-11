import re
findDarfCpfCnpj = re.compile(
    r'\d{3}.\d{3}.\d{3}-\d{2}|\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
findDarfPeriodoApuracao = re.compile(r'(\d{2}\/\d{2}\/\d{4})\nSECRETARIA')
findDarfCodigoReceita = re.compile(
    r'DARECEITA > \d{4}\n', flags=re.MULTILINE)
findDarfValidade = re.compile(r'acolhimento: \d{2}\/\d{2}\/\d{4}')
findDarfTotal = re.compile(r'(\.*\d *\.*\d+),\d{2}\nSENDA')
findDarfCodigoBarras = re.compile(r'(\d{11}-\d    ){3}\d{11}-\d')
findVencimentoGPS = re.compile(r'Vencimento:\d{2}\/\d{2}\/\d{4}')
findEmpresas = re.compile(
    r'\s[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+\n\nRaz')
findPA = re.compile(
    r'[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]+\/\d{4}')
findTotais = re.compile(r'Totais\n\n[\d*\.]*\d+,\d{2}')

Mes_ext = {
    "Janeiro": "01",
    "janeiro": "01",
    "Fevereiro": "02",
    "fevereiro": "02",
    "Março": "03",
    "março": "03",
    "Abril": "04",
    "abril": "04",
    "Maio": "05",
    "maio": "05",
    "Junho": "06",
    "junho": "06",
    "Julho": "07",
    "julho": "07",
    "Agosto": "08",
    "agosto": "08",
    "Setembro": "09",
    "setembro": "09",
    "Outubro": "10",
    "outubro": "10",
    "Novembro": "11",
    "novembro": "11",
    "Dezembro": "12",
    "dezembro": "12"
}


def regex_darf(contra_cheque, obj_response):
    if re.search(r'Documento de Arrecada', contra_cheque) is not None and re.search(r'de Receitas Federais', contra_cheque) is not None:
        if re.search(r'DARF', contra_cheque) is not None:
            obj_response["Descricao"] = "DARF"
            obj_response["Tipo"] = "55"
            obj_response["CodigoReceita"] = findDarfCodigoReceita.search(
                contra_cheque).group().replace('DARECEITA > ', '')[:-1]
            cnpj = findDarfCpfCnpj.search(contra_cheque).group()
            cnpjNum = ""
            for ch in cnpj:
                if ch.isdigit():
                    cnpjNum += ch
            obj_response["Cnpj"] = cnpjNum
            try:
                dia, Mes, ano = findDarfPeriodoApuracao.search(
                    contra_cheque).group().replace('\nSECRETARIA', '').split("/")
                obj_response["Mes"] = Mes
                obj_response["Ano"] = ano
                obj_response["PeriodoApuracao"] = ano+"-"+Mes+"-"+dia
            except:
                pass
            DD, MM, AA = findDarfValidade.search(
                contra_cheque).group().split(' ')[1].split('/')
            obj_response["Vencimento"] = AA+"-"+MM+"-"+DD
            obj_response["Total"] = findDarfTotal.search(
                contra_cheque).group().split('\n')[0].replace(",", "").replace(".", "")
            try:
                obj_response["CodigoBarras"] = findDarfCodigoBarras.search(
                    contra_cheque).group().replace(" ", "").replace("-", "")
            except:
                pass
            return obj_response

        elif re.search(r'web', contra_cheque) is not None:
            findDarfWebCodigoReceita = re.compile(
                r'[0-9]{2}[\.][0-9]{2}[\.][0-9]{5}[\.][0-9]{7}[\-][0-9]{1}')
            darfWebApuracaoEValidade = re.compile(
                r'(\n\n\d{2}\/\d{2}\/\d{4}){2}')
            findDarfWebTotal = re.compile(
                r'Valor Total do Documento\n\n\d+\,\d+')
            findDarfWebCodigoBarra = re.compile(r'(\d{11} \d{1}\n\n){4}')

            obj_response["Nome"] = "DARF-WEB"
            obj_response["Tipo"] = "55"
            # obj_response["CodigoReceita"] = findDarfWebCodigoReceita.search(contra_cheque).group().replace(".",'').replace("-","")
            obj_response["Cnpj"] = findDarfCpfCnpj.search(
                contra_cheque).group().replace(".", "").replace("-", "").replace("/", "")

            apuracao, validade = filter(None, darfWebApuracaoEValidade.search(
                contra_cheque).group().split('\n'))

            dia, mes, ano = apuracao.split('/')
            obj_response["Mes"] = mes
            obj_response["Ano"] = ano
            obj_response["PeriodoApuracao"] = ano+"-"+mes+"-"+dia

            DD, MM, AA = validade.split('/')

            obj_response["Vencimento"] = AA+"-"+MM+"-"+DD
            obj_response["Total"] = findDarfWebTotal.search(contra_cheque).group().split("\n")[
                2].replace(",", ".").replace(".", "")
            obj_response["CodigoBarras"] = findDarfWebCodigoBarra.search(
                contra_cheque).group().replace(" ", "").replace("\n", "")
            return obj_response

        elif re.search('Recibo Declara', contra_cheque) is not None and re.search(r'CNO', contra_cheque) is None:
            DD, MM, AA = findVencimentoGPS.search(
                contra_cheque).group().split('Vencimento:')[1].split('/')
            obj_response['Vencimento'] = AA+"-"+MM+"-"+DD
            obj_response["Tipo"] = "56"
            obj_response['Cnpj'] = findDarfCpfCnpj.search(
                contra_cheque).group().replace('.', '').replace('/', '').replace('-', '')
            obj_response['Empresa'] = findEmpresas.search(
                contra_cheque).group().split('\n')[0]
            Mes, Ano = findPA.search(
                contra_cheque).group().split('/')
            obj_response["Mes"] = Mes_ext[Mes]
            obj_response["Ano"] = Ano
            obj_response['Competencia'] = Ano+"-"+Mes_ext[Mes]
            obj_response['Descricao'] = "DARF-GPS"
            obj_response['Total'] = findTotais.search(
                contra_cheque).group().split('\n')[2]
            return obj_response

        elif re.search(r'CNO', contra_cheque) is not None:
            regexVencimento = re.compile(r'Vencimento: \d{2}\/\d{2}\/\d{4}')
            regexCodigoReceita = re.compile(
                r'Numero: \d{2}[\.]\d{2}[\.]\d{5}[\.]\d{7}[-]\d')
            regexCnpj = re.compile(
                r'\d{3}.\d{3}.\d{3}-\d{2}|\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}')
            regexCompetencia = re.compile(r'PA:\d{2}[\/]\d{4}')
            regexValorTotal = re.compile(r'Valor: \d+\.\d+,\d+')
            regexBoleto = re.compile(r'(\d{11} \d{1}( |\n)){4}')

            obj_response["Descricao"] = "Darf CNO"
            obj_response["Tipo"] = "102"
            DD, MM, AA = regexVencimento.search(
                contra_cheque).group().split(' ')[1].split('/')
            obj_response["Vencimento"] = AA+"-"+MM+"-"+DD
            obj_response["CodigoReceita"] = regexCodigoReceita.search(
                contra_cheque).group().split(' ')[1].replace('.', '').replace('-', '')
            obj_response["Cnpj"] = regexCnpj.search(contra_cheque).group().replace(
                '.', '').replace('/', '').replace('-', '')
            mes, ano = regexCompetencia.search(
                contra_cheque).group().replace("PA:", '').split("/")
            obj_response["Mes"] = mes
            obj_response["Ano"] = ano
            obj_response["PeriodoApuracao"] = ano+"-"+mes+'-01'
            obj_response["Total"] = regexValorTotal.search(contra_cheque).group().split(' ')[
                1].replace('.', ',').replace(',', '')
            obj_response["CodigoBarras"] = regexBoleto.search(
                contra_cheque).group().replace(' ', '').replace('\n', '')
            return obj_response

    return None

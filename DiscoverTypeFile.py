from REGEXs.ETIQUETA_CTPS import etiqueta_CTPS
from REGEXs.GPS_WEB import regex_gps_web
from REGEXs.Generic_file import regex_generic
from REGEXs.Kit_Admissao import regex_kit_admissao
from REGEXs.ComprovanteArrecadacaoDAS import regex_compArrecDAS
from REGEXs.ComprovanteArrecadacaoDARF import regex_compArrecDARF
from REGEXs.SituacaoFiscal import regex_situacao_fiscal
from REGEXs.SituacaoFiscal_v2 import regex_situacao_fiscal_v2
from REGEXs.RelatorioReembolso import regex_relatorioReembolso
from REGEXs.ProgramacaoFerias import regexProgramacaoFerias
from REGEXs.CertificadoRegularidadeFGTS import regex_certificadoRegFGTS
from REGEXs.ExtratoFGTS import regexExtratoFGTSTrabalhador
from REGEXs.RequerimentoSeguroDesemprego import regex_req_seguro_desemprego
from REGEXs.GRRF_FGTS import regex_grrf_fgts
from REGEXs.ExtratoContaFundoGarantia import regexExtratoContFundoGarantFGTS
from REGEXs.CertidaoFederalCond import regex_CertidaoFederalCond
from REGEXs.CadNacioanlPessJur import regex_CadNacPessJur
from REGEXs.Carta_Referencia import regex_CartaReferencia
from REGEXs.AvisoFerias import regex_AvisoFerias
from REGEXs.DAS import regex_das
from REGEXs.ISS import regex_iss
from REGEXs.Darf import regex_darf
from REGEXs.Relacao_Salarios_Contribuicao import regex_relacao_salarios_contribuicao
from REGEXs.Termo_Rescisao_Verso import regex_termo_rescisao_verso
from REGEXs.Termo_Rescisao_Frente import regex_termo_rescisao_frente
from REGEXs.FGTS_Chave_Liberacao import regex_fgts_chave
from REGEXs.FGTS_Chave_Liberacao_V2 import regex_fgts_chave_v2
from REGEXs.Aviso_Empreg_IndenizadoV2 import regex_empreg_indenizadoV2
from REGEXs.Aviso_Empreg_Indenizado import regex_empreg_indenizado
from REGEXs.Recibo_Ferias import regex_recibo_ferias
from REGEXs.GPS_Parcelamento import regex_gps_parcelamento
from REGEXs.ReciboPDF_EFD_CONTRIBUICOES import regex_efd_contribuicoes
from REGEXs.DMD_MOV import regex_dmd_mov
from REGEXs.DMA_RESUMO import regex_dma_resumo
from REGEXs.DEFIS import regex_defis
from REGEXs.Renuncia_Vale import regex_renuncia_vale
from REGEXs.IRPF_Recibo import regex_Irpf
from REGEXs.GRRF_Relatorio import regex_grrf_relatorio
from REGEXs.GRRF_Relatorio_V2 import regex_grrf_relatorio_v2
from REGEXs.GFIP_Protocolo_caixa import regex_envio_arquivos
from REGEXs.GFIP_Compensacao import regex_compensacao
from REGEXs.GFIP_Rubrica import regex_gfip_rubrica
from REGEXs.RE import regex_re
from REGEXs.RE_V2 import regex_re_v2
from REGEXs.DAE import regex_dae
from REGEXs.GFIP_GPS import regex_gps
from REGEXs.FGTS import regex_fgts
from REGEXs.FGTS_V2 import regex_fgts_v2
from REGEXs.Consignado import regex_consignado
from REGEXs.Folha_Pagamento import regex_folha_pagamento
from REGEXs.Contra_Cheque import regex_contra_cheque
from REGEXs.adiantamento import regex_adiantamento
import sys
import traceback
sys.path.append('.\\REGEXs\\')


def find_type_file(pdf_data, arquivo, file_name):
    print(f"LOG: Iniciando identificacao do arquivo: {file_name}")
    print(pdf_data)
    
    obj_response = {
        "Id": 0,
        "ContractorId": 0,
        "UserId": 0,
        "ContractorClientId": 0,
        "DataInc": "",
        "Descricao": "",
        "Nome": file_name.split("/")[4][:-4].replace(".", ""),
        "Tipo": "",
        "Cnpj": "",
        "Competencia": "",
        "PeriodoApuracao": "",
        "Mes": 0,
        "Ano": 0,
        "CodigoReceita": "",
        "CodigoBarras": "",
        "CpfCnpjInteressado": "",
        "NomeInteressado": "",
        "Link": "",
        "Valor": 0,
        "Juros": 0,
        "Multa": 0,
        "Total": 0,
        "CodigoBanco": "",
        "Vencimento": "",
        "Arquivo": str(arquivo),
        "Empresa": "",
        "NisInteressado": "",
        "ExtensaoArquivo": file_name[-4:].replace(".", "")
    }

    try:
        if regex_contra_cheque(pdf_data, obj_response) is not None:
            obj_response = regex_contra_cheque(pdf_data, obj_response)
        elif regex_folha_pagamento(pdf_data, obj_response) is not None:
            obj_response = regex_folha_pagamento(pdf_data, obj_response)
        elif regex_fgts(pdf_data, obj_response) is not None:
            obj_response = regex_fgts(pdf_data, obj_response)
        elif regex_fgts_v2(pdf_data, obj_response) is not None:
            obj_response = regex_fgts_v2(pdf_data, obj_response)
        elif regex_consignado(pdf_data, obj_response) is not None:
            obj_response = regex_consignado(pdf_data, obj_response)
        elif regex_gps(pdf_data, obj_response) is not None:
            obj_response = regex_gps(pdf_data, obj_response)
        elif regex_dae(pdf_data, obj_response) is not None:
            obj_response = regex_dae(pdf_data, obj_response)
        elif regex_grrf_relatorio_v2(pdf_data, obj_response) is not None:
            obj_response = regex_grrf_relatorio_v2(pdf_data, obj_response)
        elif regex_re(pdf_data, obj_response) is not None:
            obj_response = regex_re(pdf_data, obj_response)
        elif regex_re_v2(pdf_data, obj_response) is not None:
            obj_response = regex_re_v2(pdf_data, obj_response)
        elif regex_gfip_rubrica(pdf_data, obj_response) is not None:
            obj_response = regex_gfip_rubrica(pdf_data, obj_response)
        elif regex_compensacao(pdf_data, obj_response) is not None:
            obj_response = regex_compensacao(pdf_data, obj_response)
        elif regex_envio_arquivos(pdf_data, obj_response) is not None:
            obj_response = regex_envio_arquivos(pdf_data, obj_response)
        elif regex_grrf_relatorio(pdf_data, obj_response) is not None:
            obj_response = regex_grrf_relatorio(pdf_data, obj_response)
        elif regex_Irpf(pdf_data, obj_response) is not None:
            obj_response = regex_Irpf(pdf_data, obj_response)
        elif regex_renuncia_vale(pdf_data, obj_response) is not None:
            obj_response = regex_renuncia_vale(pdf_data, obj_response)
        elif regex_defis(pdf_data, obj_response) is not None:
            obj_response = regex_defis(pdf_data, obj_response)
        elif regex_dma_resumo(pdf_data, obj_response) is not None:
            obj_response = regex_dma_resumo(pdf_data, obj_response)
        elif regex_dmd_mov(pdf_data, obj_response) is not None:
            obj_response = regex_dmd_mov(pdf_data, obj_response)
        elif regex_efd_contribuicoes(pdf_data, obj_response) is not None:
            obj_response = regex_efd_contribuicoes(pdf_data, obj_response)
        elif regex_gps_parcelamento(pdf_data, obj_response) is not None:
            obj_response = regex_gps_parcelamento(pdf_data, obj_response)
        elif regex_recibo_ferias(pdf_data, obj_response) is not None:
            obj_response = regex_recibo_ferias(pdf_data, obj_response)
        elif regex_empreg_indenizado(pdf_data, obj_response) is not None:
            obj_response = regex_empreg_indenizado(pdf_data, obj_response)
        elif regex_empreg_indenizadoV2(pdf_data, obj_response) is not None:
            obj_response = regex_empreg_indenizadoV2(pdf_data, obj_response)
        elif regex_fgts_chave(pdf_data, obj_response) is not None:
            obj_response = regex_fgts_chave(pdf_data, obj_response)
        elif regex_fgts_chave_v2(pdf_data, obj_response) is not None:
            obj_response = regex_fgts_chave_v2(pdf_data, obj_response)
        elif regex_termo_rescisao_frente(pdf_data, obj_response) is not None:
            obj_response = regex_termo_rescisao_frente(pdf_data, obj_response)
        elif regex_termo_rescisao_verso(pdf_data, obj_response) is not None:
            obj_response = regex_termo_rescisao_verso(pdf_data, obj_response)
        elif regex_relacao_salarios_contribuicao(pdf_data, obj_response) is not None:
            obj_response = regex_relacao_salarios_contribuicao(
                pdf_data, obj_response)
        elif regex_darf(pdf_data, obj_response) is not None:
            obj_response = regex_darf(pdf_data, obj_response)
        elif regex_iss(pdf_data, obj_response) is not None:
            obj_response = regex_iss(pdf_data, obj_response)
        elif regex_das(pdf_data, obj_response) is not None:
            obj_response = regex_das(pdf_data, obj_response)
        elif regex_AvisoFerias(pdf_data, obj_response) is not None:
            obj_response = regex_AvisoFerias(pdf_data, obj_response)
        elif regex_CartaReferencia(pdf_data, obj_response) is not None:
            obj_response = regex_CartaReferencia(pdf_data, obj_response)
        elif regex_CadNacPessJur(pdf_data, obj_response) is not None:
            obj_response = regex_CadNacPessJur(pdf_data, obj_response)
        elif regex_CertidaoFederalCond(pdf_data, obj_response) is not None:
            obj_response = regex_CertidaoFederalCond(pdf_data, obj_response)
        elif regexExtratoContFundoGarantFGTS(pdf_data, obj_response) is not None:
            obj_response = regexExtratoContFundoGarantFGTS(
                pdf_data, obj_response)
        elif regex_grrf_fgts(pdf_data, obj_response) is not None:
            obj_response = regex_grrf_fgts(pdf_data, obj_response)
        elif regex_req_seguro_desemprego(pdf_data, obj_response) is not None:
            obj_response = regex_req_seguro_desemprego(pdf_data, obj_response)
        elif regexExtratoFGTSTrabalhador(pdf_data, obj_response) is not None:
            obj_response = regexExtratoFGTSTrabalhador(pdf_data, obj_response)
        elif regex_certificadoRegFGTS(pdf_data, obj_response) is not None:
            obj_response = regex_certificadoRegFGTS(pdf_data, obj_response)
        elif regexProgramacaoFerias(pdf_data, obj_response) is not None:
            obj_response = regexProgramacaoFerias(pdf_data, obj_response)
        elif regex_relatorioReembolso(pdf_data, obj_response) is not None:
            obj_response = regex_relatorioReembolso(pdf_data, obj_response)
        elif regex_situacao_fiscal(pdf_data, obj_response) is not None:
            obj_response = regex_situacao_fiscal(pdf_data, obj_response)
        elif regex_situacao_fiscal_v2(pdf_data, obj_response) is not None:
            obj_response = regex_situacao_fiscal_v2(pdf_data, obj_response)
        elif regex_compArrecDARF(pdf_data, obj_response) is not None:
            obj_response = regex_compArrecDARF(pdf_data, obj_response)
        elif regex_compArrecDAS(pdf_data, obj_response) is not None:
            obj_response = regex_compArrecDAS(pdf_data, obj_response)
        elif regex_kit_admissao(pdf_data, obj_response) is not None:
            obj_response = regex_kit_admissao(pdf_data, obj_response)
        elif regex_gps_web(pdf_data, obj_response) is not None:
            obj_response = regex_gps_web(pdf_data, obj_response)
        elif etiqueta_CTPS(pdf_data, obj_response) is not None:
            obj_response = etiqueta_CTPS(pdf_data, obj_response)
        elif regex_adiantamento(pdf_data, obj_response) is not None:
            obj_response = regex_adiantamento(pdf_data, obj_response)
        else:
            print("LOG: Nenhum regex especifico funcionou, usando generico.")
            obj_response = regex_generic(pdf_data, obj_response)
    except AttributeError as e:
        print(f"LOG: Erro de Atributo (Provavel falha de Regex): {e}")
        traceback.print_exc()
        obj_response = regex_generic(pdf_data, obj_response)
    except Exception as e:
        print(f"LOG: Erro Inesperado na identificacao: {e}")
        traceback.print_exc()
        obj_response = regex_generic(pdf_data, obj_response)

    try:
        obj_response["Mes"] = int(obj_response["Mes"])
        obj_response["Ano"] = int(obj_response["Ano"])
        if isinstance(obj_response["Valor"], str):
            try:
                obj_response["Valor"] = obj_response["Valor"].replace(".", "")
            except:
                pass
            obj_response["Valor"] = int(
                obj_response["Valor"].replace(",", ""))
        if isinstance(obj_response["Juros"], str):
            try:
                obj_response["Juros"] = obj_response["Juros"].replace(".", "")
            except:
                pass
            obj_response["Juros"] = int(
                obj_response["Juros"].replace(",", ""))
        if isinstance(obj_response["Total"], str):
            try:
                obj_response["Total"] = obj_response["Total"].replace(".", "")
            except:
                pass
            obj_response["Total"] = int(
                obj_response["Total"].replace(",", ""))
    except:
        pass

    print(f"LOG: Identificacao Concluida. Tipo detectado: {obj_response.get('Descricao', 'N/A')} | Nome: {obj_response.get('Nome', 'N/A')}")
    return obj_response
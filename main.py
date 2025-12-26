import os
import json
import sys
import shutil
import requests
import traceback 
from base_url import get_base_url
from report_whats import notify_error

def find_regex(pdf_data, arquivo, file_name, token):
    from DiscoverTypeFile import find_type_file
    obj_response = find_type_file(pdf_data, arquivo, file_name)
    return sendObject(obj_response, token, file_name)

def sendObject(obj, token, file_name):
    from SendRequests import sendRequest
    response = sendRequest(obj, get_base_url() + "ProcessaGenericDoc", token)
    resposta = {
        "Sucess": True,
        "msg": "",
        "data": ""
    }

    try:
        if isinstance(response, dict):
            path_sucesso = "C:/Users/Administrator/Documents/Api_Verificacao_Documento_Py/Sucesso/"
            os.makedirs(path_sucesso, exist_ok=True) 
            
            clean_name = file_name.split("/")[-1].replace(".pdf", "").replace(".", "") + ".json"
            
            with open(os.path.join(path_sucesso, clean_name), 'a', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=4)
            
            resposta["msg"] = f"O arquivo do tipo {obj.get('Descricao', 'Desconhecido')} foi lido e enviado com sucesso!"
            resposta["data"] = response
        else:
            # Lógica de Erro da API
            resposta["msg"] = "O arquivo não foi reconhecido pela API"
            resposta["Sucess"] = False
            
            # 1. Salva na pasta de erro PRIMEIRO
            new_path = save_error(file_name, obj, "API não reconheceu")
            
            # 2. Envia o PDF salvo para o WhatsApp
            if new_path:
                notify_error(new_path, "Arquivo não reconhecido pela API", f"Resp: {response}")

    except Exception as e:
        resposta["Sucess"] = False
        resposta["msg"] = f"Erro ao salvar logs: {e}"
        # Se der erro aqui, tenta enviar o arquivo original
        notify_error(file_name, "Erro ao salvar JSON de log", str(e))

    finally:
        # Se o arquivo ainda existir na origem (não foi movido), remove
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
            except Exception as e:
                print(f"Erro ao remover arquivo original: {e}")
                
    return resposta

def save_error(file_name, obj=None, error_msg=None):
    """
    Move o arquivo para a pasta de erro e retorna o NOVO caminho.
    """
    path_erro = "C:/Users/Administrator/Documents/Api_Verificacao_Documento_Py/DeramErro/"
    os.makedirs(path_erro, exist_ok=True)
    
    nome_base = os.path.basename(file_name)
    destino = os.path.join(path_erro, nome_base)
    
    try:
        # Se já existe no destino, remove antes para não dar erro
        if os.path.exists(destino):
            os.remove(destino)
            
        shutil.move(file_name, destino)
        
        # Salva o JSON do objeto se fornecido
        if obj:
            json_name = nome_base.replace(".pdf", "").replace(".", "") + ".json"
            with open(os.path.join(path_erro, json_name), 'w', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=4)
                
        return destino # Retorna onde o arquivo está agora
    except Exception as e:
        print(f"Erro ao mover {file_name} para DeramErro: {e}")
        return None

def main(pathToPdfs, token):
    files = os.listdir(pathToPdfs)
    from ExtractTextFromPdf import Extract_text, FalhaNaLeituraPdf
    pdfReader = Extract_text()
    resposta = {
        "Arquivos Enviados": len(files),
        "Arquivos": []
    }

    for file in files:
        file_path = os.path.join(pathToPdfs, file)

        # --- Bloco Encoding ---
        try:
            print(file)
        except UnicodeEncodeError as e:
            # Logica de erro de encoding
            new_path = save_error(file_path, error_msg="Erro Encoding Nome")
            if new_path:
                notify_error(new_path, "Erro de Encoding no Nome", str(e))
            continue

        # --- Bloco Processamento ---
        try:
            if file.lower().endswith(".pdf"):
                pdf_data, arquivo, file_name = pdfReader.teste_pdf_miner(file_path)
                resposta["Arquivos"].append(find_regex(pdf_data, arquivo, file_name, token))

            elif file.lower().endswith(".docx"):
                pdf_data, arquivo, file_name = pdfReader.docx_file(file_path)
                resposta["Arquivos"].append(find_regex(pdf_data, arquivo, file_name, token))

            elif file.lower().endswith(".txt"):
                pdf_data, arquivo, file_name = pdfReader.txt_file(file_path)
                resposta["Arquivos"].append(find_regex(pdf_data, arquivo, file_name, token))

            else:
                pdf_data, arquivo, file_name = pdfReader.unknown_file(file_path)
                resposta["Arquivos"].append(find_regex(pdf_data, arquivo, file_name, token))

        except FalhaNaLeituraPdf as e:
            print("Deu falha na leitura")
            # Move primeiro
            new_path = save_error(file_path, error_msg="Falha na leitura")
            # Envia depois (usando o caminho novo)
            if new_path:
                notify_error(new_path, "Falha na Extração de Texto", str(e))

        except Exception as e:
            print(f"Erro inesperado ao processar {file}: {e}")
            erro_completo = traceback.format_exc()
            
            # Move primeiro
            new_path = save_error(file_path, error_msg="Crash do Script")
            
            # Envia depois (usando o caminho novo)
            if new_path:
                notify_error(new_path, "Exceção Inesperada (Crash)", erro_completo)

    return resposta

if __name__ == "__main__":
    if len(sys.argv) > 2:
        pathToPdfs = sys.argv[1]
        token = sys.argv[2]
        main(pathToPdfs, token)
    else:
        print("Erro: Argumentos insuficientes.")
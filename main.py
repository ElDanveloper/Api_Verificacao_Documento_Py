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
            path_erro = "C:/Users/Administrator/Documents/Api_Verificacao_Documento_Py/DeramErro/"
            os.makedirs(path_erro, exist_ok=True)
            
            clean_name = file_name.split("/")[-1].replace(".pdf", "").replace(".", "") + ".json"

            with open(os.path.join(path_erro, clean_name), 'a', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=4)
            
            resposta["msg"] = "O arquivo não foi reconhecido pela API"
            resposta["Sucess"] = False
            
            notify_error(file_name, "Arquivo não reconhecido pela API", f"Resposta da API: {response}")

    except Exception as e:
        resposta["Sucess"] = False
        resposta["msg"] = f"Erro ao salvar logs: {e}"
        notify_error(file_name, "Erro ao salvar JSON de log", str(e))

    finally:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
            except Exception as e:
                print(f"Erro ao remover arquivo: {e}")
                
    return resposta

def save_error(file_name, obj=None, error_msg=None):
    path_erro = "C:/Users/Administrator/Documents/Api_Verificacao_Documento_Py/DeramErro/"
    os.makedirs(path_erro, exist_ok=True)
    destino = os.path.join(path_erro, os.path.basename(file_name))
    try:
        shutil.move(file_name, destino)
    except Exception as e:
        print(f"Erro ao mover {file_name} para DeramErro: {e}")

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

        try:
            print(file)
        except UnicodeEncodeError as e:
            printable_name = file.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
            print(f"Arquivo com nome inválido para o console: {printable_name}")
            
            save_error(file_path, error_msg="Erro de encoding no nome do arquivo")
            
            notify_error(file_path, "Erro de Encoding no Nome", str(e))

            if os.path.exists(file_path):
                os.remove(file_path)
            continue

        try:
            if file.lower().endswith(".pdf"):
                pdf_data, arquivo, file_name = pdfReader.teste_pdf_miner(file_path)
                # print(pdf_data)
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
            save_error(file_path, error_msg="Falha na leitura do PDF")
            notify_error(file_path, "Falha na Extração de Texto", str(e))

            if os.path.exists(file_path):
                os.remove(file_path)

        except Exception as e:
            print(f"Erro inesperado ao processar {file}: {e}")
            save_error(file_path, error_msg="Erro inesperado no processamento")
            
            erro_completo = traceback.format_exc()
            notify_error(file_path, "Exceção Inesperada (Crash)", erro_completo)

            if os.path.exists(file_path):
                os.remove(file_path)

    return resposta

if __name__ == "__main__":
    if len(sys.argv) > 2:
        pathToPdfs = sys.argv[1]
        token = sys.argv[2]
        main(pathToPdfs, token)
    else:
        print("Erro: Argumentos insuficientes. Uso: script.py <caminho_pdfs> <token>")
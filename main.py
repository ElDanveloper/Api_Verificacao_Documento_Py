import os
import json
import sys
import shutil
import requests
from base_url import get_base_url
from report_whats import notify_error

def find_regex(pdf_data, arquivo, file_name, token):
    from DiscoverTypeFile import find_type_file
    obj_response = find_type_file(pdf_data, arquivo, file_name)
    return sendObject(obj_response, token, file_name)


def sendObject(obj, token, file_name):
    from SendRequests import sendRequest
    response = sendRequest(obj, get_base_url()+"ProcessaGenericDoc", token)
    resposta = {
        "Sucess": True,
        "msg": "",
        "data": ""
    }

    try:
        if type(response) == dict:
            with open("C:/Users/Administrator/Documents/Api_Verificacao_Documento_Py/Sucesso/" +
                      file_name.split("/")[4][:-4].replace(".", "")+".json", 'a', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=4)
            resposta["msg"] = f"O arquivo do tipo {obj['Descricao']} foi lido e enviado com sucesso!"
            resposta["data"] = response
        else:
            with open("C:/Users/Administrator/Documents/Api_Verificacao_Documento_Py/DeramErro/" +
                      file_name.split("/")[4][:-4].replace(".", "")+".json", 'a', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=4)
            resposta["msg"] = "O arquivo não foi reconhecido"
            resposta["Sucess"] = False
            notify_error(file_name)

    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
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
        except UnicodeEncodeError:
            printable_name = file.encode(
                sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)

            print(
                f"Arquivo com nome inválido para o console: {printable_name}")

            save_error(
                file_path, error_msg="Erro de encoding no nome do arquivo")

            notify_error(file_path)

            if os.path.exists(file_path):

                os.remove(file_path)

            continue

        try:

            if file.endswith(".pdf") or file.endswith(".PDF"):

                pdf_data, arquivo, file_name = pdfReader.teste_pdf_miner(
                    file_path)
                
                # print("--- INICIO DO TEXTO ---")
                # print(pdf_data)
                # print("--- FIM DO TEXTO ---")

                resposta["Arquivos"].append(find_regex(
                    pdf_data, arquivo, file_name, token))

            elif file.endswith(".docx") or file.endswith(".DOCX"):

                pdf_data, arquivo, file_name = pdfReader.docx_file(file_path)

                resposta["Arquivos"].append(find_regex(
                    pdf_data, arquivo, file_name, token))

            elif file.endswith(".txt") or file.endswith(".TXT"):

                pdf_data, arquivo, file_name = pdfReader.txt_file(file_path)

                resposta["Arquivos"].append(find_regex(
                    pdf_data, arquivo, file_name, token))

            else:

                pdf_data, arquivo, file_name = pdfReader.unknown_file(
                    file_path)

                resposta["Arquivos"].append(find_regex(
                    pdf_data, arquivo, file_name, token))

        except FalhaNaLeituraPdf:

            print("Deu falha na leitura")

            save_error(file_path, error_msg="Falha na leitura do PDF")

            notify_error(file_path)

            if os.path.exists(file_path):

                os.remove(file_path)

        except Exception as e:

            print(f"Erro inesperado ao processar {file}: {e}")

            save_error(file_path, error_msg="Erro inesperado no processamento")

            notify_error(file_path)

            if os.path.exists(file_path):

                os.remove(file_path)

    return resposta


pathToPdfs = sys.argv[1]

token = sys.argv[2]

main(pathToPdfs, token)

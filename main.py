import os
import json
import sys
from base_url import get_base_url


def find_regex(pdf_data, arquivo, file_name, token):
    from DiscoverTypeFile import find_type_file
    obj_response = find_type_file(pdf_data, arquivo, file_name)
    return sendObject(obj_response, token, file_name)


def sendObject(obj, token, file_name):
    from SendRequests import sendRequest
    print(file_name)
    response = sendRequest(obj, get_base_url()+"ProcessaGenericDoc", token)
    resposta = {
        "Sucess": True,
        "msg": "",
        "data": ""
    }
    if type(response) == dict:
        print(response)
        path="C:/Users/Administrator/Documents/Api_Verificacao_Documento_Py/Sucesso/"+file_name.split("/")[4][:-4].replace(".", "")+".json"
        print(path)
        with open(path, 'a', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)
        resposta["msg"] = "O arquivo do tipo " + \
            obj["Nome"]+" foi lido e enviado com sucesso!",
        resposta["data"] = response
    else:
        with open("C:/Users/Administrator/Documents/Api_Verificacao_Documento_Py/DeramErro/"+file_name.split("/")[4][:-4].replace(".", "")+".json", 'a', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)
        resposta["msg"] = "O arquivo não foi reconhecido",
        resposta["Sucess"] = False
    os.remove(file_name)
    return resposta


def main(pathToPdfs, token):
    files = os.listdir(pathToPdfs)
    from ExtractTextFromPdf import Extract_text
    from ExtractTextFromPdf import PdfComSenha
    pdfReader = Extract_text()
    resposta = {
        "Arquivos Enviados": len(files),
        "Arquivos": []
    }
    from ExtractTextFromPdf import FalhaNaLeituraPdf
    for file in files:
        try:
            if file.endswith(".pdf") or file.endswith(".PDF"):
                pdf_data, arquivo, file_name = pdfReader.teste_pdf_miner(
                    pathToPdfs+file)
                resposta["Arquivos"].append(find_regex(
                    pdf_data, arquivo, file_name, token))
            elif file.endswith(".docx") or file.endswith(".DOCX"):
                pdf_data, arquivo, file_name = pdfReader.docx_file(
                    pathToPdfs+file)
                resposta = find_regex(pdf_data, arquivo, file_name, token)
            elif file.endswith(".txt") or file.endswith(".TXT"):
                pdf_data, arquivo, file_name = pdfReader.txt_file(
                    pathToPdfs+file)
                resposta = find_regex(pdf_data, arquivo, file_name, token)
            else:
                pdf_data, arquivo, file_name = pdfReader.unknown_file(
                    pathToPdfs+file)
                resposta = find_regex(pdf_data, arquivo, file_name, token)
        except FalhaNaLeituraPdf:
            os.remove(pathToPdfs+file)
    return resposta

pathToPdfs = sys.argv[1]
token = sys.argv[2]
main(pathToPdfs, token)

if __name__ == "__main__":
    main("C:/Apps_NodeJS/hunnocrm-api-node/uploads/", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJub21lIjoiTGVhbmRybyBSZWJvdcOnYXMiLCJjcGZfY25waiI6IjA0MTA1MDUzNTgyIiwiY29udHJhY3Rvcl9jbnBqIjoiMTExMTExMTExMTEiLCJpZCI6IjUiLCJwZXJzb25faWQiOiI0ODYiLCJlbWFpbCI6ImNvbnRhdG9AbGVhbmRyb3JlYm91Y2FzLmNvbSIsInBob25lX2NlbGwiOiI3NTk5Mjc0MjgxOSIsInR5cGVfdXNlciI6IkMiLCJwZXJmaWxfdXNlciI6IkQiLCJhY3RpdmUiOnRydWUsInVzZXJfaWRfc3VwZXJ2aXNvciI6IjEiLCJ1c2VyX3Bhc3N3b3JkIjoiJDJhJDEwJG53c2NsRTJaWVlQRUNFZVdJWjFyYk9yZkU5TUEwLnFqTUp6dGlOdVJkOGFNeG1Tcm9lWk9PIiwiZGVwYXJ0bWVudF9pZCI6IjEiLCJzaW1wbGVfbmFtZSI6IkxlYW5kcm8gUmVib3XDp2FzIiwiY2FtaW5ob19mb3RvIjoiaHR0cHM6Ly9maXJlYmFzZXN0b3JhZ2UuZ29vZ2xlYXBpcy5jb20vdjAvYi9odW5uby02ZjM0YS5hcHBzcG90LmNvbS9vLzElMkYxNTY4NjM3MDk5MjMzLTI4MTU3NjE4XzE4NDYxMTk5Mjg3MzM0MzVfMzc1MTk0MjAzOTQ2MjIxNTY4X24uanBnP2FsdD1tZWRpYSIsImNvbnRyYWN0b3IiOltdLCJjbGllbnRzIjpbXSwiaWF0IjoxNjMyNzY3MTk1LCJleHAiOjE2MzI4NTM1OTUsImNvbnRyYWN0b3JfaWQiOiIxIn0.ZhBhuBT8Kx_HfPxjI6ouXAd5g4KhY6x6IaJwEFr8z20")

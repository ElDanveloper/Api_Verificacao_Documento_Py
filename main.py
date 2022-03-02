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
    response = sendRequest(obj, get_base_url()+"ProcessaGenericDoc", token)
    resposta = {
        "Sucess": True,
        "msg": "",
        "data": ""
    }
    if type(response) == dict:
        #print(response)
        with open("C:/Users/Administrator/Documents/Api_Verificacao_Documento_Py/Sucesso/"+file_name.split("/")[4][:-4].replace(".", "")+".json", 'a', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)
        resposta["msg"] = "O arquivo do tipo " + \
            obj["Descricao"]+" foi lido e enviado com sucesso!",
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
            print("deu falha na leitura: ")
            os.remove(pathToPdfs+file)
    return resposta

pathToPdfs = sys.argv[1]
token = sys.argv[2]
main(pathToPdfs, token)

#if __name__ == "__main__":
#    main("C:/Apps_NodeJS/hunnocrm-api-node/uploads/", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJub21lIjoiTWFyY2lvIENvc3RhIFNpbHZhIiwiY3BmX2NucGoiOiI2MDYwMTk4MTU1MyIsImNvbnRyYWN0b3JfaWQiOiIxIiwiY29udHJhY3Rvcl9jbnBqIjoiMTEzNzgwMDQwMDAxMjQiLCJpZCI6IjEiLCJwZXJzb25faWQiOiIzMzEiLCJlbWFpbCI6Im1hcmNpb0Bwb2xsb2NvbnRhYmlsLmNvbS5iciIsInBob25lX2NlbGwiOiI3NTk5MTg2NDY5NiIsInR5cGVfdXNlciI6IkMiLCJwZXJmaWxfdXNlciI6IkQiLCJhY3RpdmUiOnRydWUsInVzZXJfaWRfc3VwZXJ2aXNvciI6IjEiLCJ1c2VyX3Bhc3N3b3JkIjoiJDJhJDEwJDJ6aDZjTHg0WjlkenVFUWVxNHd6Vi56ZzdkTTNEVXBlZ3Rpa0NONDg4bm5ac0RqbjJOUE1PIiwiZGVwYXJ0bWVudF9pZCI6IjciLCJzaW1wbGVfbmFtZSI6Ik3DoXJjaW8gQ29zdGEiLCJjYW1pbmhvX2ZvdG8iOm51bGwsImNvbnRyYWN0b3IiOlt7ImlkIjoiMSIsInBlcnNvbl9pZCI6IjExNyIsIm5vbWUiOiJQT0xMTyBDT05TVUxUT1JJQSBDT05UQUJJTCBFIFNJU1RFTUFTIExUREEiLCJjcGZfY25waiI6IjExMzc4MDA0MDAwMTI0IiwiZG9jX2Zvcm1hdCI6IjExLjM3OC4wMDQvMDAwMS0yNCIsInRpcG9faW5zY3JpY2FvIjoiMSIsInRpcG8iOiJKIiwiY2FtaW5ob19mb3RvIjoiaHR0cHM6Ly9pLmltZ3VyLmNvbS9TU25pRm9ELnBuZyIsImNydCI6IjEiLCJjcmNfc3Vic2NyaXB0aW9uIjoiMDE4MzkyIiwiZW1haWwiOiJtYXJjaW9AcG9sbGNvbnRhYmlsLmNvbS5iciIsIndoYXRzYXBwX2J1c2luZXNzIjoiNzU5OTE4NjQ2OTYiLCJpbnN0YWdyYW0iOm51bGwsImZhY2Vib29rIjpudWxsLCJ5b3V0dWJlIjpudWxsLCJsaW5rZWRpbiI6bnVsbCwiZ29vZ2xlX2FjY291bnQiOm51bGwsImRhdGVfcmVnaXN0ZXIiOiIyMDE5LTA3LTE0VDE0OjU2OjI0LjAwMFoiLCJkYXRlX2luaXRpYWxfY29udHJhY3QiOiIyMDE5LTA3LTE0VDE0OjU2OjI5LjAwMFoiLCJkYXRlX2xhc3RfY29udHJhY3QiOiIyMDE5LTA3LTE0VDE0OjU2OjM0LjAwMFoiLCJhY3RpdmVfY29udHJhY3QiOm51bGwsImRlcGFydGFtZW50b19pZCI6IjciLCJkZXBhcnRhbWVudG9fdXNlcl9yZXNwIjoiMSIsImRlcGFydGFtZW50b19ub21lIjoiQWRtaW5pc3RyYXRpdm8iLCJkZXBhcnRhbWVudG9fdGlwbyI6bnVsbH1dLCJjbGllbnRzIjpbXSwiaWF0IjoxNjQwMTcyMTE0LCJleHAiOjE2NDAyNTg1MTR9.Ub62RWZeiFd63igbYZTg2RgViVxLxh1fvy6HBt-4nzI")

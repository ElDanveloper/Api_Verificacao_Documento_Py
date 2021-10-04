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
    response = sendRequest(
        obj, "https://api.hunno.com.br:2004/dp/hunnodev/file/"+"ProcessaGenericDoc", token)
    resposta = {
        "Sucess": True,
        "msg": "",
        "data": ""
    }
    if type(response) == dict:
        print(response)
        path = "C:/Users/carlo/Documents/api-toqweb/Sucesso/" + \
            file_name.split("/")[2][:-4].replace(".", "")+".json"
        print(path)
        with open(path, 'a', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)
        resposta["msg"] = "O arquivo do tipo " + \
            obj["Nome"]+" foi lido e enviado com sucesso!",
        resposta["data"] = response
    else:
        with open("C:/Users/carlo/Documents/api-toqweb/DeramErro/"+file_name.split("/")[4][:-4].replace(".", "")+".json", 'a', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)
        resposta["msg"] = "O arquivo não foi reconhecido",
        resposta["Sucess"] = False
    os.remove(file_name)
    return resposta


def main(pathToPdfs, token):
    print(pathToPdfs)
    print(token)
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
            print("deu falha")
            # os.remove(pathToPdfs+file)
    return resposta


# pathToPdfs = sys.argv[1]
# token = sys.argv[2]
# main(pathToPdfs, token)

if __name__ == "__main__":
    main("./uploads/", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJub21lIjoiTWFyY2lvIENvc3RhIFNpbHZhIiwiY3BmX2NucGoiOiI2MDYwMTk4MTU1MyIsImNvbnRyYWN0b3JfaWQiOiIxIiwiY29udHJhY3Rvcl9jbnBqIjoiMTEzNzgwMDQwMDAxMjQiLCJpZCI6IjEiLCJwZXJzb25faWQiOiIzMzEiLCJlbWFpbCI6Im1hcmNpb0Bwb2xsb2NvbnRhYmlsLmNvbS5iciIsInBob25lX2NlbGwiOiI3NTk5MTg2NDY5NiIsInR5cGVfdXNlciI6IkMiLCJwZXJmaWxfdXNlciI6IkQiLCJhY3RpdmUiOnRydWUsInVzZXJfaWRfc3VwZXJ2aXNvciI6IjEiLCJ1c2VyX3Bhc3N3b3JkIjoiJDJhJDEwJDJ6aDZjTHg0WjlkenVFUWVxNHd6Vi56ZzdkTTNEVXBlZ3Rpa0NONDg4bm5ac0RqbjJOUE1PIiwiZGVwYXJ0bWVudF9pZCI6IjciLCJzaW1wbGVfbmFtZSI6Ik3DoXJjaW8gQ29zdGEiLCJjYW1pbmhvX2ZvdG8iOm51bGwsImNvbnRyYWN0b3IiOlt7ImlkIjoiMSIsInBlcnNvbl9pZCI6IjExNyIsIm5vbWUiOiJQT0xMTyBDT05TVUxUT1JJQSBDT05UQUJJTCBFIFNJU1RFTUFTIExUREEiLCJjcGZfY25waiI6IjExMzc4MDA0MDAwMTI0IiwiZG9jX2Zvcm1hdCI6IjExLjM3OC4wMDQvMDAwMS0yNCIsInRpcG9faW5zY3JpY2FvIjpudWxsLCJ0aXBvIjoiRSIsImNhbWluaG9fZm90byI6Imh0dHBzOi8vaS5pbWd1ci5jb20vU1NuaUZvRC5wbmciLCJjcnQiOiIxIiwiY3JjX3N1YnNjcmlwdGlvbiI6IjAxODM5MiIsImVtYWlsIjoibWFyY2lvQHBvbGxjb250YWJpbC5jb20uYnIiLCJ3aGF0c2FwcF9idXNpbmVzcyI6Ijc1OTkxODY0Njk2IiwiaW5zdGFncmFtIjpudWxsLCJmYWNlYm9vayI6bnVsbCwieW91dHViZSI6bnVsbCwibGlua2VkaW4iOm51bGwsImdvb2dsZV9hY2NvdW50IjpudWxsLCJkYXRlX3JlZ2lzdGVyIjoiMjAxOS0wNy0xNFQxNDo1NjoyNC4wMDBaIiwiZGF0ZV9pbml0aWFsX2NvbnRyYWN0IjoiMjAxOS0wNy0xNFQxNDo1NjoyOS4wMDBaIiwiZGF0ZV9sYXN0X2NvbnRyYWN0IjoiMjAxOS0wNy0xNFQxNDo1NjozNC4wMDBaIiwiYWN0aXZlX2NvbnRyYWN0IjpudWxsLCJkZXBhcnRhbWVudG9faWQiOiI3IiwiZGVwYXJ0YW1lbnRvX3VzZXJfcmVzcCI6IjEiLCJkZXBhcnRhbWVudG9fbm9tZSI6IkFkbWluaXN0cmF0aXZvIiwiZGVwYXJ0YW1lbnRvX3RpcG8iOm51bGx9XSwiY2xpZW50cyI6W10sImlhdCI6MTYzMzExOTcyMSwiZXhwIjoxNjMzMjA2MTIxfQ.LwPGt4yXD8TDbsK4I-wM7f4C7yA6BUIuRbkcwoTJSlc")

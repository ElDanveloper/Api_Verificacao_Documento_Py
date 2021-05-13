import sys
import os
import json
def find_regex(pdf_data,arquivo,file_name,token):
    from DiscoverTypeFile import find_type_file
    obj_response=find_type_file(pdf_data,arquivo,file_name)
    #response = testarApi(obj_response,"https://api.toqweb.com.br:2004/dp/hunno/file/ProcessaGenericDoc")
    return sendObject(obj_response,token,file_name)
def sendObject(obj, token,file_name):
    from routes import testarApi
    from writeB64 import buildPdf
    response = testarApi(obj,"http://75.119.134.38:2004/dp/hunnodev/file/ProcessaGenericDoc",token)
    resposta = {
            "Sucess":True,
            "msg":"",
            "data":""
        }
    if type(response) == dict:
        buildPdf(response["Nome"],obj["Arquivo"])
        resposta["msg"]="O arquivo do tipo "+obj["Nome"]+" foi lido e enviado com sucesso!",
        resposta["data"]=response
        #return "O arquivo do tipo "+obj_response["Nome"]+" foi lido e enviado com sucesso!\n"
    else:
        f = open("./DeramErro/"+file_name.split("/")[2][:-4].replace(".","")+".txt", "w")
        f.write(json.dumps(obj))
        f.write("\n\n"+response)
        resposta["msg"]="O arquivo não foi reconhecido",
        resposta["Sucess"]=False
    os.remove(file_name)
    return resposta

def main(pathToPdfs,token):
    files = os.listdir(pathToPdfs)
    from ExtractTextFromPdf import Extract_text
    from ExtractTextFromPdf import PdfComSenha
    pdfReader = Extract_text()
    resposta = {
        "Arquivos Enviados":len(files),
        "Arquivos":[]
    }
    for file in files:
        if file.endswith(".pdf") or file.endswith(".PDF"):
            pdf_data,arquivo,file_name=pdfReader.teste_pdf_miner(pathToPdfs+file)
            resposta["Arquivos"].append(find_regex(pdf_data,arquivo,file_name,token))
        elif file.endswith(".docx") or file.endswith(".DOCX"):
            pdf_data,arquivo,file_name=pdfReader.docx_file(pathToPdfs+file)
            resposta=find_regex(pdf_data,arquivo,file_name,token)
        elif file.endswith(".txt") or file.endswith(".TXT"):
            pdf_data,arquivo,file_name=pdfReader.txt_file(pathToPdfs+file)
            resposta=find_regex(pdf_data,arquivo,file_name,token)
        else:
            pdf_data,arquivo,file_name=pdfReader.unknown_file(pathToPdfs+file)
            resposta=find_regex(pdf_data,arquivo,file_name,token)
    return resposta
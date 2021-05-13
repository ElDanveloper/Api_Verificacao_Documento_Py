from flask import Flask, request
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import jwt
from threading import Thread
app = Flask("VerificacaoDocumento")
CORS(app)
uploads_dir = os.path.join('uploads')
os.makedirs(uploads_dir, exist_ok=True)

@app.route("/receiveFile", methods=["POST"])
def receiveFile():
    files = request.files.getlist("file")
    for file in files:
        file.save(os.path.join(uploads_dir, secure_filename(file.filename)))
    from main import main
    res=main("./"+uploads_dir+"/",request.headers.get("Authorization"))
    return res
@app.route("/receiveFiles", methods=["POST"])
def receiveFiles():
    token = str.replace(str(request.headers.get("Authorization")), 'Bearer ', '')
    data=jwt.decode(token, options={"verify_signature": False})
    uploads_dir = os.path.join('uploads/'+data["cpf_cnpj"])
    os.makedirs(uploads_dir, exist_ok=True)
    files = request.files.getlist("file")
    for file in files:
        file.save(os.path.join(uploads_dir, secure_filename(file.filename)))
    resposta = {
            "Sucess":True,
            "msg":"",
            "data":""
        }
    #Thread(target=testThread(uploads_dir)).start()
    return resposta
@app.route("/sendFiles", methods=["GET"])
def sendFiles():
    from main import main
    token = str.replace(str(request.headers.get("Authorization")), 'Bearer ', '')
    data=jwt.decode(token, options={"verify_signature": False})
    res=main('uploads/'+data["cpf_cnpj"]+"/",request.headers.get("Authorization"))
    return res
def testThread(dir):
    from main import main
    res=main(dir+"/",request.headers.get("Authorization"))
    print(res)
@app.route("/", methods=["GET"])
def get():
    return "Olá mundo"
app.run(host='0.0.0.0',port=3100)

from flask import Flask, request
import flask
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import jwt
from threading import Thread

app = flask.Flask(__name__)
app.config['DEBUG'] = True
CORS(app)

uploads_dir = os.path.join('uploads')
os.makedirs(uploads_dir, exist_ok=True)

@app.route("/boleto-proprio", methods=["POST"])
def route_boleto_proprio():
    try:
        file = request.files["file"]
        path = os.path.join(uploads_dir, secure_filename(file.filename))
        file.save(path)
        from BoletoProprio import main
        res = main(path, request.headers.get("Authorization"))
        return res
    except Exception as e: return str(e)

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
    uploads_dir2 = os.path.join('uploads2/'+data["cpf_cnpj"])
    os.makedirs(uploads_dir2, exist_ok=True)
    files = request.files.getlist("file")
    print(files)
    for file in files:
        file.save(os.path.join(uploads_dir2, secure_filename(file.filename)))
    resposta = {
            "Sucess":True,
            "msg":"",
            "data":""
        }
    return resposta

@app.route("/sendFiles", methods=["GET"])
def sendFiles():
    from main import main
    token = str.replace(str(request.headers.get("Authorization")), 'Bearer ', '')
    data=jwt.decode(token, options={"verify_signature": False})
    res=main('uploads2/'+data["cpf_cnpj"]+"/",request.headers.get("Authorization"))
    return res

@app.route("/", methods=["GET"])
def get():
    return "Olá mundo" 

if __name__ =="__main__":
    app.run(host='0.0.0.0',port=5000)
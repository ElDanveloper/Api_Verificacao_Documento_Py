import base64
def buildPdf(file_name, file):
    bytes = base64.b64decode(file, validate=True)
    # Perform a basic validation to make sure that the result is a valid PDF file
    if bytes[0:4] != b'%PDF':
        return None
    f = open("./Pasta Destino/"+file_name+'.pdf', 'wb')
    f.write(bytes)
    f.close()
    return "Arquivo criado com sucesso!"
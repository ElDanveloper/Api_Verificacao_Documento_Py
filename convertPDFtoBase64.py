import base64
import os

def pdf_to_base64(filename):
    with open(filename, "rb") as file:
        data = base64.b64encode(file.read())
    os.remove(filename)
    return str(data)
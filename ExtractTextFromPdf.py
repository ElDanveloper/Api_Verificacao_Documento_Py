from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os
from pdfminer import high_level
import pdfminer
import base64
import docx
from pathlib import Path
import unidecode


class Error(Exception):
    """Base class for other exceptions"""
    pass


class PdfComSenha(Error):
    """Raised when the input value is too small"""
    pass


class FalhaNaLeituraPdf(Error):
    """Raised when the input value is too small"""
    pass


class Extract_text:

    def __init__(self):
        self.local_pdf_filename = ""

    def __str__(self):
        return self.local_pdf_filename

    def __test_pdf_image(self):        
        pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
        pages = convert_from_path(self.local_pdf_filename, poppler_path=r"./Dependences/poppler-21.09.0/Library/bin")        
        image_counter = 1
        for page in pages:           
            filename = "page_"+str(image_counter)+".jpg"
            page.save(filename, 'JPEG')
            image_counter = image_counter + 1

        filelimit = image_counter-1
        fullText = ""
        for i in range(1, filelimit + 1):
            filename = "page_"+str(i)+".jpg"

            text = str(((pytesseract.image_to_string(Image.open(filename)))))
            fullText = fullText+text
            os.remove("page_"+str(i)+".jpg")
        return fullText

    def pdf_miner(self, filename):
        self.pdf_filename = filename
        # Abre e lê o arquivo
        with open(self.pdf_filename, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        try:
            extracted_text = high_level.extract_text(self.pdf_filename, "")
            # Caso o retorno seja algum dos abaixo, o PDF é um PDF Imagem
            if extracted_text in {'', '♀'} or extracted_text.__contains__("(cid:"):
                extracted_text = self.__test_pdf_image()
        except pdfminer.pdfdocument.PDFPasswordIncorrect as e:
            extracted_text = ""
        except:
            raise FalhaNaLeituraPdf()
        extracted_text = unidecode.unidecode(extracted_text)
        return extracted_text, encoded_string.decode('ascii'), self.pdf_filename

    def teste_pdf_miner(self, local_pdf_filename):
        self.local_pdf_filename = local_pdf_filename
        with open(self.local_pdf_filename, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        try:
            extracted_text = high_level.extract_text(
                self.local_pdf_filename, "")
            if extracted_text == "" or extracted_text.__contains__("(cid:"):
                extracted_text = self.__test_pdf_image()
        except pdfminer.pdfdocument.PDFPasswordIncorrect as e:
            extracted_text = ""
        except FalhaNaLeituraPdf():
            raise FalhaNaLeituraPdf          
        return extracted_text, encoded_string.decode('ascii'), self.local_pdf_filename

    def docx_file(self, local_pdf_filename):
        self.local_pdf_filename = local_pdf_filename
        doc = docx.Document(self.local_pdf_filename)
        fullText = []
        with open(self.local_pdf_filename, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText), encoded_string.decode('ascii'), self.local_pdf_filename

    def txt_file(self, local_pdf_filename):
        self.local_pdf_filename = local_pdf_filename
        with open(self.local_pdf_filename, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        txt = Path(self.local_pdf_filename).read_text(
            errors="ignore").replace('\n', '')
        print(str(txt))
        return txt, encoded_string.decode('ascii'), self.local_pdf_filename

    def unknown_file(self, local_pdf_filename):
        self.local_pdf_filename = local_pdf_filename
        with open(self.local_pdf_filename, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        return "", encoded_string.decode('ascii'), self.local_pdf_filename

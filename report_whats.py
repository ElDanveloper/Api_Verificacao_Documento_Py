import requests
import os

EVOLUTION_API_URL = "https://evolution.interchat.com.br"  
EVOLUTION_API_KEY = "23d673da678ee9566f6c09b5a0c33e4e"              
INSTANCE_NAME = "Pollo-Contabilidade"               
RECIPIENT_NUMBER = "557591352127-1578313973@g.us"  
# RECIPIENT_NUMBER = "557599685324"
# ------------------------------------------

def notify_error(file_name):
    try:
        base_file_name = os.path.basename(file_name)
        error_message = f"Houve um erro ao processar o arquivo: {base_file_name}"
        url = f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE_NAME}"

        headers = {
            "apikey": EVOLUTION_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "number": RECIPIENT_NUMBER,
            "delay": 1200,
            "linkPreview": False,
            "text": error_message
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        response.raise_for_status() 

        print(f"Notificação de erro enviada com sucesso para {RECIPIENT_NUMBER}.")
        print(f"Resposta da API: {response.json()}")

    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP ao enviar notificação via Evolution API: {http_err}")
        print(f"Resposta do servidor: {http_err.response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Erro de requisição (rede/conexão) ao enviar notificação: {req_err}")
    except Exception as e:
        print(f"Falha inesperada ao enviar notificação de erro: {e}")


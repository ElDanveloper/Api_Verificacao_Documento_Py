import requests
import os
import datetime

EVOLUTION_API_URL = "https://evolution.interchat.com.br"
EVOLUTION_API_KEY = "23d673da678ee9566f6c09b5a0c33e4e"
INSTANCE_NAME = "Pollo-Contabilidade"
RECIPIENT_NUMBER = "557591352127-1578313973@g.us"
# RECIPIENT_NUMBER = "557599685324"

def notify_error(file_name, error_summary, error_details=""):
    try:
        base_file_name = os.path.basename(file_name)
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        message_text = (
            f"*🚨 ERRO NO PROCESSAMENTO DO ARQUIVO*\n\n"
            f"📂 *Arquivo:* `{base_file_name}`\n"
            f"📅 *Data:* {data_hora}\n"
            f"❌ *Erro:* {error_summary}\n"
        )
        
        if error_details:
            detalhes_limpos = str(error_details)[:800] 
            message_text += f"\n📝 *Detalhes Técnicos:*\n```{detalhes_limpos}```"

        url = f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE_NAME}"

        headers = {
            "apikey": EVOLUTION_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "number": RECIPIENT_NUMBER,
            "delay": 1200,
            "linkPreview": False,
            "text": message_text
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()

        print(f"Notificação de erro enviada para {RECIPIENT_NUMBER}.")

    except Exception as e:
        print(f"Falha ao enviar notificação de erro (report_whats): {e}")
import requests
import os
import datetime
import base64
import mimetypes

EVOLUTION_API_URL = "https://evolution.interchat.com.br"
EVOLUTION_API_KEY = "23d673da678ee9566f6c09b5a0c33e4e"
INSTANCE_NAME = "Pollo-Contabilidade"
RECIPIENT_NUMBER = "557591352127-1578313973@g.us"

def file_to_base64(file_path):
    try:
        with open(file_path, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode('utf-8')
        return encoded_string
    except Exception as e:
        print(f"Erro ao converter arquivo para Base64: {e}")
        return None

def notify_error(file_path, error_summary, error_details=""):
    try:
        base_file_name = os.path.basename(file_path)
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        caption_text = (
            f"*🚨 ERRO NO PROCESSAMENTO*\n"
            f"📅 *Data:* {data_hora}\n"
            f"❌ *Erro:* {error_summary}\n"
        )
        
        if error_details:
             caption_text += f"\n📝 *Detalhes:* {str(error_details)[:300]}..." # Corta se for muito grande

        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/pdf"

        base64_data = file_to_base64(file_path)
        
        if not base64_data:
            print("Não foi possível ler o arquivo para envio. Enviando apenas texto.")
            return

        url = f"{EVOLUTION_API_URL}/message/sendMedia/{INSTANCE_NAME}"

        headers = {
            "apikey": EVOLUTION_API_KEY,
            "Content-Type": "application/json"
        }

        # O endpoint espera o Base64 direto no campo 'media' se não for URL
        payload = {
            "number": RECIPIENT_NUMBER,
            "mediatype": "document",
            "mimetype": mime_type,
            "media": base64_data, 
            "fileName": base64_file_name,
            "caption": caption_text,
            "delay": 1200
        }

        print(f"Enviando mídia: {base_file_name} para o WhatsApp...")
        response = requests.post(url, json=payload, headers=headers, timeout=30) # Timeout maior para upload
        response.raise_for_status()

        print(f"Notificação com PDF enviada com sucesso.")

    except Exception as e:
        print(f"Falha ao enviar notificação de erro via WhatsApp: {e}")
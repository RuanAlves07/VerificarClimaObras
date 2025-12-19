from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER

class NotificationService:
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    def enviar_alerta(self, numero_whatsapp, mensagem):
        """Envia mensagem via WhatsApp"""
        try:
            message = self.client.messages.create(
                from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
                to=f"whatsapp:{numero_whatsapp}",
                body=mensagem
            )
            return {'sucesso': True, 'message_id': message.sid}
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}

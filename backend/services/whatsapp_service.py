import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WhatsAppService:
    def __init__(self):
        self.api_url = os.getenv('EVOLUTION_API_URL', 'http://localhost:8080')
        self.api_key = os.getenv('EVOLUTION_API_KEY', '')
        self.instance_name = os.getenv('EVOLUTION_INSTANCE_NAME', 'clima_obras')
    
    def send_message(self, number, message):
        """
        Envia mensagem via Evolution API
        :param number: Número com DDI (ex: 5547999999999)
        :param message: Texto da mensagem
        :return: dict com status do envio
        """
        try:
            url = f"{self.api_url}/message/sendText/{self.instance_name}"
            
            headers = {
                'Content-Type': 'application/json',
                'apikey': self.api_key
            }
            
            # Formatar número (remover caracteres não numéricos)
            clean_number = ''.join(filter(str.isdigit, number))
            
            # Adicionar DDI do Brasil se não tiver
            if not clean_number.startswith('55'):
                clean_number = '55' + clean_number
            
            payload = {
                'number': clean_number,
                'text': message
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200 or response.status_code == 201:
                return {
                    'success': True,
                    'message': 'Mensagem enviada com sucesso',
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'message': f'Erro ao enviar mensagem: {response.status_code}',
                    'error': response.text
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': 'Erro de conexão com Evolution API',
                'error': str(e)
            }
    
    def send_bulk_messages(self, recipients, message):
        """
        Envia mensagem para múltiplos destinatários
        :param recipients: Lista de dicts com 'nome' e 'whatsapp'
        :param message: Texto da mensagem
        :return: Lista com resultado de cada envio
        """
        results = []
        
        for recipient in recipients:
            result = self.send_message(recipient['whatsapp'], message)
            results.append({
                'nome': recipient['nome'],
                'whatsapp': recipient['whatsapp'],
                'status': 'sucesso' if result['success'] else 'erro',
                'mensagem': result['message']
            })
        
        return results
    
    def check_connection(self):
        """
        Verifica se a conexão com Evolution API está funcionando
        :return: bool
        """
        try:
            url = f"{self.api_url}/instance/connectionState/{self.instance_name}"
            headers = {'apikey': self.api_key}
            
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('state') == 'open'
            return False
        
        except Exception as e:
            print(f"Erro ao verificar conexão: {e}")
            return False

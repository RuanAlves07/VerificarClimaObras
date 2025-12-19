import requests
from config import OPEN_METEO_API
from datetime import datetime, timedelta

class WeatherService:
    @staticmethod
    def obter_clima_atual(latitude, longitude):
        """Obtém clima atual e previsão"""
        url = f"{OPEN_METEO_API}/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,precipitation,weather_code',
            'hourly': 'temperature_2m,precipitation_probability',
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
            'timezone': 'auto'
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None
    
    @staticmethod
    def comparar_com_ano_passado(latitude, longitude):
        """Compara dados com ano anterior (usando archive)"""
        hoje = datetime.now()
        ano_passado = hoje - timedelta(days=365)
        
        url = f"{OPEN_METEO_API}/archive"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'start_date': ano_passado.strftime('%Y-%m-%d'),
            'end_date': hoje.strftime('%Y-%m-%d'),
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum'
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

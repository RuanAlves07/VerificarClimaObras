import requests
from typing import Dict, Optional
from greenlet import greenlet

class WeatherAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_weather_by_coords(self, lat: float, lon: float) -> Optional[Dict]:
        """Obtém dados climáticos por coordenadas (latitude, longitude)"""
        try:
            url = f"{self.base_url}/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric&lang=pt_br"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao buscar clima: {e}")
            return None
    
    def parse_weather_data(self, raw_data: Dict) -> Dict:
        """Extrai as informações principais de clima"""
        if not raw_data:
            return {}
        
        return {
            "temperatura": round(raw_data.get("main", {}).get("temp", 0), 1),
            "sensacao_termica": round(raw_data.get("main", {}).get("feels_like", 0), 1),
            "humidade": raw_data.get("main", {}).get("humidity", 0),
            "pressao": raw_data.get("main", {}).get("pressure", 0),
            "chuva": raw_data.get("rain", {}).get("1h", 0),  # chuva em 1 hora (mm)
            "nuvens": raw_data.get("clouds", {}).get("all", 0),  # cobertura de nuvens (%)
            "descricao": raw_data.get("weather", [{}])[0].get("description", ""),
            "velocidade_vento": raw_data.get("wind", {}).get("speed", 0)
        }
    
    def get_climate_info(self, lat: float, lon: float) -> Dict:
        """Função principal - retorna clima completo"""
        raw_data = self.get_weather_by_coords(lat, lon)
        return self.parse_weather_data(raw_data)
    
    def get_temperature_by_region(self, lat: float, lon: float) -> Optional[float]:
        """Retorna apenas a temperatura de uma região"""
        data = self.get_climate_info(lat, lon)
        return data.get("temperatura")
    
    def get_rain_and_clouds(self, lat: float, lon: float) -> Dict:
        """Retorna apenas chuva e nuvens para exibir no mapa"""
        data = self.get_climate_info(lat, lon)
        return {
            "chuva": data.get("chuva", 0),
            "nuvens": data.get("nuvens", 0)
        }


def fetch_weather_async(weather_api: WeatherAPI, lat: float, lon: float) -> Dict:
    """Wrapper para execução assíncrona com greenlet"""
    return weather_api.get_climate_info(lat, lon)

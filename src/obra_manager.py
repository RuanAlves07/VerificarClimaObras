from typing import Dict, List, Optional
from weather_api import WeatherAPI
from config import OPENWEATHER_API_KEY

class ObraManager:
    def __init__(self):
        self.weather_api = WeatherAPI(OPENWEATHER_API_KEY)
        self.obras = []  # Será substituído por banco de dados
    
    def get_obra_with_climate(self, obra_id: int, lat: float, lon: float) -> Dict:
        """Retorna dados da obra com informações climáticas"""
        clima = self.weather_api.get_climate_info(lat, lon)
        
        return {
            "id": obra_id,
            "latitude": lat,
            "longitude": lon,
            "clima": {
                "temperatura": clima.get("temperatura"),
                "sensacao_termica": clima.get("sensacao_termica"),
                "humidade": clima.get("humidade"),
                "chuva": clima.get("chuva"),
                "nuvens": clima.get("nuvens"),
                "descricao": clima.get("descricao"),
                "velocidade_vento": clima.get("velocidade_vento")
            }
        }
    
    def get_map_weather_overlay(self, obras: List[Dict]) -> List[Dict]:
        """Retorna dados de chuva e nuvens para overlay no mapa"""
        overlay_data = []
        
        for obra in obras:
            rain_clouds = self.weather_api.get_rain_and_clouds(
                obra["latitude"], 
                obra["longitude"]
            )
            overlay_data.append({
                "obra_id": obra["id"],
                "lat": obra["latitude"],
                "lon": obra["longitude"],
                "chuva": rain_clouds["chuva"],
                "nuvens": rain_clouds["nuvens"]
            })
        
        return overlay_data

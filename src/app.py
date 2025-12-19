from flask import Flask, jsonify, request
from obra_manager import ObraManager
import json

app = Flask(__name__)
obra_manager = ObraManager()

@app.route('/api/obra/<int:obra_id>/clima', methods=['GET'])
def get_obra_clima(obra_id):
    """Retorna clima detalhado de uma obra específica"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if not lat or not lon:
        return jsonify({"erro": "Latitude e longitude são obrigatórias"}), 400
    
    clima = obra_manager.get_obra_with_climate(obra_id, lat, lon)
    return jsonify(clima)

@app.route('/api/mapa/clima', methods=['POST'])
def get_map_climate_overlay():
    """Retorna dados de chuva e nuvens para overlay no mapa"""
    data = request.json
    obras = data.get('obras', [])
    
    overlay = obra_manager.get_map_weather_overlay(obras)
    return jsonify({"overlay": overlay})

@app.route('/api/temperatura/<float:lat>/<float:lon>', methods=['GET'])
def get_temperature(lat, lon):
    """Retorna apenas a temperatura de uma região"""
    temp = obra_manager.weather_api.get_temperature_by_region(lat, lon)
    return jsonify({"temperatura": temp, "lat": lat, "lon": lon})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

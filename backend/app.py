import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, render_template, session, redirect, url_for, request
from flask_cors import CORS
from dotenv import load_dotenv
from database import db
from models import Usuario
import requests

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/clima_obras')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    db.init_app(app)
    CORS(app, supports_credentials=True)
    
    from routes.localizacoes import localizacoes_bp
    from routes.auth import auth_bp
    from routes.engenheiros import engenheiros_bp
    app.register_blueprint(localizacoes_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(engenheiros_bp)
    
    @app.route('/')
    def home():
        return redirect('/login')
    
    @app.route('/login')
    def login_page():
        return render_template('login.html')
    
    @app.route('/dashboard')
    def dashboard():
        if 'usuario_id' not in session:
            return redirect('/login')
        return render_template('dashboard.html')
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'erro': 'Rota não encontrada'}), 404
    
    @app.route('/api/clima/<float:lat>/<float:lon>', methods=['GET'])
    def get_clima(lat, lon):
        """Retorna dados climáticos completos de uma localização"""
        data = get_weather_data(lat, lon)
        
        if not data:
            return jsonify({"erro": "Não foi possível buscar dados climáticos"}), 500
        
        return jsonify({
            "temperatura": round(data.get("main", {}).get("temp", 0), 1),
            "sensacao_termica": round(data.get("main", {}).get("feels_like", 0), 1),
            "humidade": data.get("main", {}).get("humidity", 0),
            "chuva": data.get("rain", {}).get("1h", 0),
            "nuvens": data.get("clouds", {}).get("all", 0),
            "descricao": data.get("weather", [{}])[0].get("description", ""),
            "velocidade_vento": round(data.get("wind", {}).get("speed", 0), 1)
        })
    
    @app.route('/api/obras/clima', methods=['POST'])
    def get_obras_clima():
        """Retorna clima para múltiplas obras"""
        obras = request.json.get("obras", [])
        resultados = []
        
        for obra in obras:
            clima = get_weather_data(obra["lat"], obra["lon"])
            if clima:
                resultados.append({
                    "id": obra["id"],
                    "nome": obra.get("nome", ""),
                    "lat": obra["lat"],
                    "lon": obra["lon"],
                    "temperatura": round(clima.get("main", {}).get("temp", 0), 1),
                    "chuva": clima.get("rain", {}).get("1h", 0),
                    "nuvens": clima.get("clouds", {}).get("all", 0)
                })
        
        return jsonify({"obras": resultados})
    
    with app.app_context():
        db.create_all()
        
        # Criar usuário admin padrão se não existir
        admin = Usuario.query.filter_by(email='admin@admin.com').first()
        if not admin:
            admin = Usuario(nome='Administrador', email='admin@admin.com', tipo='admin')
            admin.set_senha('abc,123')
            db.session.add(admin)
            db.session.commit()
    
    return app

app = create_app()

def get_weather_data(lat, lon):
    """Busca dados climáticos da OpenWeatherMap"""
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "pt_br"
        }
        response = requests.get(OPENWEATHER_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao buscar clima: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True, port=5000)

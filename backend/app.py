from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/clima_obras')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    CORS(app)
    
    from routes.localizacoes import localizacoes_bp
    app.register_blueprint(localizacoes_bp)
    
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({'mensagem': 'API Clima Obras - Sistema rodando com sucesso'}), 200
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'erro': 'Rota não encontrada'}), 404
    
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

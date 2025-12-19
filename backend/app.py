import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from database import db
from models import Usuario

load_dotenv()

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)

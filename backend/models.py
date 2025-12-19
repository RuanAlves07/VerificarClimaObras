from app import db
from datetime import datetime

class Localizacao(db.Model):
    __tablename__ = 'localizacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

class HistoricoClimatico(db.Model):
    __tablename__ = 'historico_climatico'
    
    id = db.Column(db.Integer, primary_key=True)
    localizacao_id = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    temperatura = db.Column(db.Float)
    chuva = db.Column(db.Float)
    tipo = db.Column(db.String(50))  # 'real' ou 'previsão'

class Engenheiro(db.Model):
    __tablename__ = 'engenheiros'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False, unique=True)
    localizacao_id = db.Column(db.Integer, nullable=False)
    ativo = db.Column(db.Integer, default=1)

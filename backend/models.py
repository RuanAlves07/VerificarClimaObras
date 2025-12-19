from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default='membro')  # 'admin' ou 'membro'
    ativo = db.Column(db.Integer, default=1)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Localizacao(db.Model):
    __tablename__ = 'localizacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text)
    endereco = db.Column(db.String(500))
    responsavel = db.Column(db.String(255))
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
    whatsapp = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255))
    cargo = db.Column(db.String(100))
    localizacao_id = db.Column(db.Integer, db.ForeignKey('localizacoes.id'))
    ativo = db.Column(db.Integer, default=1)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

class DisparoWhatsapp(db.Model):
    __tablename__ = 'disparos_whatsapp'
    
    id = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.Text, nullable=False)
    tipo_filtro = db.Column(db.String(50))  # 'todos' ou 'obra_especifica'
    localizacao_id = db.Column(db.Integer, db.ForeignKey('localizacoes.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    quantidade_envios = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='enviado')  # 'enviado', 'erro', 'pendente'

from flask import Blueprint, request, jsonify, session
from models import Usuario
from database import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    
    if not email or not senha:
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
    
    usuario = Usuario.query.filter_by(email=email, ativo=1).first()
    
    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({'erro': 'Credenciais inválidas'}), 401
    
    session['usuario_id'] = usuario.id
    session['usuario_tipo'] = usuario.tipo
    session['usuario_nome'] = usuario.nome
    
    return jsonify({
        'mensagem': 'Login realizado com sucesso',
        'usuario': {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'tipo': usuario.tipo
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'mensagem': 'Logout realizado com sucesso'}), 200

@auth_bp.route('/me', methods=['GET'])
def me():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    
    usuario = Usuario.query.get(session['usuario_id'])
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo': usuario.tipo
    }), 200

@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    # Apenas admins podem registrar novos usuários
    if session.get('usuario_tipo') != 'admin':
        return jsonify({'erro': 'Apenas administradores podem cadastrar usuários'}), 403
    
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    tipo = data.get('tipo', 'membro')
    
    if not nome or not email or not senha:
        return jsonify({'erro': 'Dados incompletos'}), 400
    
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'erro': 'Email já cadastrado'}), 400
    
    novo_usuario = Usuario(nome=nome, email=email, tipo=tipo)
    novo_usuario.set_senha(senha)
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({
        'mensagem': 'Usuário cadastrado com sucesso',
        'usuario': {
            'id': novo_usuario.id,
            'nome': novo_usuario.nome,
            'email': novo_usuario.email,
            'tipo': novo_usuario.tipo
        }
    }), 201

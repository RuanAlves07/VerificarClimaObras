from flask import Blueprint, request, jsonify, session
from models import Engenheiro, Localizacao, DisparoWhatsapp
from database import db
from services.whatsapp_service import WhatsAppService

engenheiros_bp = Blueprint('engenheiros', __name__, url_prefix='/api')

@engenheiros_bp.route('/engenheiros', methods=['GET'])
def get_engenheiros():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    
    engenheiros = Engenheiro.query.filter_by(ativo=1).all()
    return jsonify([{
        'id': eng.id,
        'nome': eng.nome,
        'whatsapp': eng.whatsapp,
        'email': eng.email,
        'cargo': eng.cargo,
        'localizacao_id': eng.localizacao_id,
        'localizacao_nome': Localizacao.query.get(eng.localizacao_id).nome if eng.localizacao_id else None
    } for eng in engenheiros]), 200

@engenheiros_bp.route('/engenheiros', methods=['POST'])
def create_engenheiro():
    if session.get('usuario_tipo') != 'admin':
        return jsonify({'erro': 'Apenas administradores podem cadastrar engenheiros'}), 403
    
    data = request.get_json()
    
    # Verificar se whatsapp já existe
    whatsapp = data.get('whatsapp', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    if Engenheiro.query.filter_by(whatsapp=whatsapp, ativo=1).first():
        return jsonify({'erro': 'WhatsApp já cadastrado'}), 400
    
    novo_engenheiro = Engenheiro(
        nome=data.get('nome'),
        whatsapp=whatsapp,
        email=data.get('email'),
        cargo=data.get('cargo'),
        localizacao_id=data.get('localizacao_id') if data.get('localizacao_id') else None
    )
    
    db.session.add(novo_engenheiro)
    db.session.commit()
    
    return jsonify({
        'mensagem': 'Engenheiro cadastrado com sucesso',
        'id': novo_engenheiro.id
    }), 201

@engenheiros_bp.route('/engenheiros/<int:id>', methods=['PUT'])
def atualizar_engenheiro(id):
    if session.get('usuario_tipo') != 'admin':
        return jsonify({'erro': 'Apenas administradores podem editar engenheiros'}), 403
    
    engenheiro = Engenheiro.query.get(id)
    if not engenheiro:
        return jsonify({'erro': 'Engenheiro não encontrado'}), 404
    
    data = request.get_json()
    engenheiro.nome = data.get('nome', engenheiro.nome)
    engenheiro.whatsapp = data.get('whatsapp', engenheiro.whatsapp).replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    engenheiro.email = data.get('email', engenheiro.email)
    engenheiro.cargo = data.get('cargo', engenheiro.cargo)
    engenheiro.localizacao_id = data.get('localizacao_id') if data.get('localizacao_id') else None
    
    db.session.commit()
    return jsonify({'mensagem': 'Engenheiro atualizado com sucesso'}), 200

@engenheiros_bp.route('/engenheiros/<int:id>', methods=['DELETE'])
def deletar_engenheiro(id):
    if session.get('usuario_tipo') != 'admin':
        return jsonify({'erro': 'Apenas administradores podem excluir engenheiros'}), 403
    
    engenheiro = Engenheiro.query.get(id)
    if not engenheiro:
        return jsonify({'erro': 'Engenheiro não encontrado'}), 404
    
    engenheiro.ativo = 0
    db.session.commit()
    return jsonify({'mensagem': 'Engenheiro excluído com sucesso'}), 200

@engenheiros_bp.route('/disparar-whatsapp', methods=['POST'])
def disparar_whatsapp():
    if session.get('usuario_tipo') != 'admin':
        return jsonify({'erro': 'Apenas administradores podem enviar mensagens'}), 403
    
    data = request.get_json()
    mensagem = data.get('mensagem')
    tipo_filtro = data.get('tipo_filtro')
    localizacao_id = data.get('localizacao_id')
    
    if not mensagem:
        return jsonify({'erro': 'Mensagem é obrigatória'}), 400
    
    # Buscar engenheiros baseado no filtro
    if tipo_filtro == 'todos':
        engenheiros = Engenheiro.query.filter_by(ativo=1).all()
    else:
        if not localizacao_id:
            return jsonify({'erro': 'Obra é obrigatória para este filtro'}), 400
        engenheiros = Engenheiro.query.filter_by(localizacao_id=localizacao_id, ativo=1).all()
    
    if not engenheiros:
        return jsonify({'erro': 'Nenhum engenheiro encontrado para envio'}), 404
    
    # Preparar lista de destinatários
    recipients = [{'nome': eng.nome, 'whatsapp': eng.whatsapp} for eng in engenheiros]
    
    # Enviar mensagens via Evolution API
    whatsapp_service = WhatsAppService()
    
    # Verificar conexão
    if not whatsapp_service.check_connection():
        # Registrar disparo mesmo sem conexão (modo simulação)
        disparo = DisparoWhatsapp(
            mensagem=mensagem,
            tipo_filtro=tipo_filtro,
            localizacao_id=localizacao_id,
            usuario_id=session.get('usuario_id'),
            quantidade_envios=len(engenheiros),
            status='pendente'
        )
        db.session.add(disparo)
        db.session.commit()
        
        return jsonify({
            'aviso': 'Evolution API não conectada. Disparo registrado mas não enviado.',
            'quantidade': len(engenheiros),
            'engenheiros': [{'nome': r['nome'], 'whatsapp': r['whatsapp'], 'status': 'pendente'} for r in recipients]
        }), 200
    
    # Enviar mensagens
    results = whatsapp_service.send_bulk_messages(recipients, mensagem)
    
    # Registrar disparo
    sucessos = sum(1 for r in results if r['status'] == 'sucesso')
    disparo = DisparoWhatsapp(
        mensagem=mensagem,
        tipo_filtro=tipo_filtro,
        localizacao_id=localizacao_id,
        usuario_id=session.get('usuario_id'),
        quantidade_envios=sucessos,
        status='enviado' if sucessos > 0 else 'erro'
    )
    db.session.add(disparo)
    db.session.commit()
    
    return jsonify({
        'mensagem': f'Mensagens enviadas: {sucessos} de {len(engenheiros)}',
        'resultados': results
    }), 200

@engenheiros_bp.route('/whatsapp/status', methods=['GET'])
def whatsapp_status():
    """Verificar status da conexão com Evolution API"""
    if session.get('usuario_tipo') != 'admin':
        return jsonify({'erro': 'Não autorizado'}), 403
    
    whatsapp_service = WhatsAppService()
    conectado = whatsapp_service.check_connection()
    
    return jsonify({
        'conectado': conectado,
        'mensagem': 'Evolution API conectada' if conectado else 'Evolution API desconectada'
    }), 200

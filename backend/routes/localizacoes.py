from flask import Blueprint, request, jsonify
from models import Localizacao
from database import db

localizacoes_bp = Blueprint('localizacoes', __name__, url_prefix='/api')

@localizacoes_bp.route('/localizacoes', methods=['GET'])
def get_localizacoes():
    localizacoes = Localizacao.query.all()
    return jsonify([{
        'id': loc.id,
        'nome': loc.nome,
        'latitude': loc.latitude,
        'longitude': loc.longitude,
        'descricao': loc.descricao,
        'endereco': loc.endereco,
        'responsavel': loc.responsavel,
        'data_criacao': loc.data_criacao.isoformat() if loc.data_criacao else None
    } for loc in localizacoes]), 200

@localizacoes_bp.route('/localizacoes', methods=['POST'])
def create_localizacao():
    data = request.get_json()
    
    nova_localizacao = Localizacao(
        nome=data.get('nome'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        descricao=data.get('descricao'),
        endereco=data.get('endereco'),
        responsavel=data.get('responsavel')
    )
    
    db.session.add(nova_localizacao)
    db.session.commit()
    
    return jsonify({
        'mensagem': 'Localização criada com sucesso',
        'id': nova_localizacao.id
    }), 201

@localizacoes_bp.route('/localizacoes/<int:id>', methods=['PUT'])
def atualizar(id):
    loc = db.session.query(Localizacao).get(id)
    if not loc:
        return jsonify({'erro': 'Obra não encontrada'}), 404
    
    data = request.get_json()
    loc.nome = data.get('nome', loc.nome)
    loc.endereco = data.get('endereco', loc.endereco)
    loc.latitude = data.get('latitude', loc.latitude)
    loc.longitude = data.get('longitude', loc.longitude)
    loc.responsavel = data.get('responsavel', loc.responsavel)
    loc.descricao = data.get('descricao', loc.descricao)
    
    db.session.commit()
    return jsonify({'mensagem': 'Obra atualizada com sucesso'}), 200

@localizacoes_bp.route('/localizacoes/<int:id>', methods=['DELETE'])
def deletar(id):
    db.session.query(Localizacao).filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'sucesso': True})

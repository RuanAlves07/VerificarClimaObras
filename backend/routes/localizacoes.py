from flask import Blueprint, request, jsonify, current_app
from models import Localizacao

localizacoes_bp = Blueprint('localizacoes', __name__, url_prefix='/api/localizacoes')

@localizacoes_bp.route('', methods=['GET'])
def listar():
    from app import db
    locs = db.session.query(Localizacao).all()
    return jsonify([{'id': l.id, 'nome': l.nome, 'lat': l.latitude, 'lng': l.longitude} for l in locs])

@localizacoes_bp.route('', methods=['POST'])
def criar():
    from app import db
    data = request.get_json()
    nova_loc = Localizacao(nome=data['nome'], latitude=data['latitude'], longitude=data['longitude'])
    db.session.add(nova_loc)
    db.session.commit()
    return jsonify({'id': nova_loc.id}), 201

@localizacoes_bp.route('/<int:id>', methods=['PUT'])
def atualizar(id):
    from app import db
    loc = db.session.query(Localizacao).get(id)
    data = request.get_json()
    loc.nome = data.get('nome', loc.nome)
    db.session.commit()
    return jsonify({'sucesso': True})

@localizacoes_bp.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    from app import db
    db.session.query(Localizacao).filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'sucesso': True})

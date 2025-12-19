from flask import Blueprint, request, jsonify
from app import db
from models import Localizacao

localizacoes_bp = Blueprint('localizacoes', __name__, url_prefix='/api/localizacoes')

@localizacoes_bp.route('', methods=['GET'])
def listar():
    locs = db.session.query(Localizacao).all()
    return jsonify([{'id': l.id, 'nome': l.nome, 'lat': l.latitude, 'lng': l.longitude} for l in locs])

@localizacoes_bp.route('', methods=['POST'])
def criar():
    data = request.get_json()
    nova_loc = Localizacao(nome=data['nome'], latitude=data['latitude'], longitude=data['longitude'])
    db.session.add(nova_loc)
    db.session.commit()
    return jsonify({'id': nova_loc.id}), 201

@localizacoes_bp.route('/<int:id>', methods=['PUT'])
def atualizar(id):
    loc = db.session.query(Localizacao).get(id)
    data = request.get_json()
    loc.nome = data.get('nome', loc.nome)
    db.session.commit()
    return jsonify({'sucesso': True})

@localizacoes_bp.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    db.session.query(Localizacao).filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'sucesso': True})

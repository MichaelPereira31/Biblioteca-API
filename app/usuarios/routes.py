from sqlalchemy.exc import StatementError, IntegrityError
from flask_jwt import jwt_required
from flask import Blueprint, request, jsonify
from flask import json

from app.configuracao.db import db
from .models import User
from .schemas import UserSchema

user = Blueprint('user', __name__)

@jwt_required
@user.route('/', methods=['GET'])
def read_users():
    userschema = UserSchema(many=True)
    users = User.query.all()

    if users:
        dados = userschema.dump(users)
    
    else:
        dados = {
            'message': 'Nenhum usuário registrado.'
        }

    return jsonify(dados), 200


@jwt_required
@user.route('/<int:id>', methods=['GET'])
def read_user(id):
    userschema = UserSchema()
    
    try:
        user = User.query.get(id)
        dados = userschema.dump(user)

        return userschema.jsonify(dados), 200

    except Exception:
        dados = {
            'message': 'Não foi encontrado usuário com esse ID.'
        }

        return jsonify(dados), 404


@user.route('/', methods=['POST'])
def create_user():
    userschema = UserSchema()
    dados = request.json

    user = User(**dados)

    db.session.add(user)
    
    try:
        db.session.commit()

        dados = {}
        dados['user'] = userschema.dump(user)
        dados['message'] = 'Usuário adicionado com sucesso.'

        return jsonify(dados), 201
    
    except ValueError:
        dados = {
            'message': 'Usuário já existe.'
        }
        return jsonify(dados), 400


@jwt_required
@user.route('/<int:id>', methods=['PUT'])
def update_user(id):
    userschema = UserSchema()
    dados = request.json

    try:
        user = User.query.get(id)
        user.name = dados['name']
        user.username = dados['username']
        user.password = user.generate_hash_password(dados['password'])
        user.admin = dados['admin'] 
        
        db.session.commit()
        
        dados = {}

        dados['user'] = userschema.dump(user)
        dados['message'] = 'Usuário atualizado com sucesso.'

        return jsonify(dados), 200

    except AttributeError:
        dados = {
            'message': 'Não foi encontrado usuário com esse ID.'
        }
        return jsonify(dados), 404

    except IntegrityError:
        dados = {
            'message':'Erro ao atualizar usuário.'
        }
        return jsonify(dados), 409


@jwt_required
@user.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    userschema = UserSchema()
    dados = {}
    
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
    
        dados['user'] = userschema.dump(user)
        dados['message'] = 'Usuário deletado com sucesso.'

        return jsonify(dados), 200

    except Exception:
        dados = {
            'message': 'Não foi encontrado usuário com esse ID.'
        }

        return jsonify(dados), 404
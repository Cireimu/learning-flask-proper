import os
from flask import Blueprint, request, jsonify

from .models import User
from .dbhelpers import findByUsername, findByEmail, createUser, findUserById
from .middleware import create_jwt
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/registration', methods=['POST'])
def register():
    req = request.json
    required = ['username', 'password', 'email']

    if not all(k in req for k in required):
        return jsonify({'message': 'Missing Required Values'}), 400

    if findByUsername(req['username']) != None:
        return jsonify({'message': 'User by that username already exists'}), 400
    if findByEmail(req['email']) != None:
        return jsonify({'message': 'User by that email already exists'}), 400

    new_user = User(username=req['username'],
                    email=req['email'], password=req['password'])
    new_user.set_password(req['password'])
    createUser(new_user)

    current_user = findByUsername(req['username'])
    jwt_token = create_jwt(current_user)

    return jsonify({'key': jwt_token.decode('ascii')}), 200

@auth.route('/login', methods=['POST'])
def login():
    req = request.json
    user = findByUsername(req['username'])
    if user and user.check_password(password=req['password']):
        jwt_token = create_jwt(user)
        return jsonify({'key': jwt_token.decode('ascii')}), 200
    return jsonify({'message': 'Invalid username/password combination'})

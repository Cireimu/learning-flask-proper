import os
from flask import Blueprint, request, jsonify
from src.models.auth import User
from src.dbhelpers import find_user_by_username, create_user, find_user_by_id, find_user_by_email
from src.middleware import create_jwt, assign_req_values
from src.main import db

auth = Blueprint('auth', __name__)

@auth.route('/registration', methods=['POST'])
def register():
    req = request.json
    required = ['username', 'password', 'email']

    if not all(k in req for k in required):
        return jsonify({'message': 'Missing Required Values'}), 400

    if find_user_by_username(req['username']) != None:
        return jsonify({'message': 'User by that username already exists'})
    if find_user_by_email(req['email']) != None:
        return jsonify({'message': 'User by that email already exists'})
    
    username = req['username']
    email = req['email']
    password = req['password']
    address = assign_req_values(req, "address")
    phone_address = assign_req_values(req, "phone_address")
    
    new_user = User(username=username, email=email, password=password, address=address, phone_address=phone_address)
    new_user.set_password(req['password'])
    create_user(new_user)

    current_user = find_user_by_username(req['username'])
    jwt_token = create_jwt(current_user)

    return jsonify({'key': jwt_token.decode('ascii')}), 200

@auth.route('/login', methods=['POST'])
def login():
    req = request.json
    user = find_user_by_username(req['username'])
    if user and user.check_password(password=req['password']):
        jwt_token = create_jwt(user)
        return jsonify({'key': jwt_token.decode('ascii')}), 200
    return jsonify({'message': 'Invalid username/password combination'})

import os
from flask import Blueprint, request, jsonify, make_response
from src.models.models import User
from src.dbhelpers import find_user_by_username, create_user, find_user_by_id, find_user_by_email, find_users
from src.middleware import create_jwt, assign_req_values, check_for_if_user_exist
from src.main import db

auth = Blueprint('auth', __name__)

@auth.route('/registration', methods=['POST'])
@check_for_if_user_exist
def register():
    req = request.json
    required = ['username', 'password', 'email']

    if not all(k in req for k in required):
        return jsonify({'message': 'Missing Required Values'}), 400
    
    username = req['username']
    email = req['email']
    password = req['password']
    address = assign_req_values(req, "address", None)
    phone_address = assign_req_values(req, "phone_address", None)
    
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

@auth.route('/<int:id>', methods=['PUT'])
@check_for_if_user_exist
def update_user(id):
    req = request.json
    user = find_user_by_id(id)

    user.username = assign_req_values(req, 'username', user.username)
    user.password = assign_req_values(req, 'password', user.password)
    user.email = assign_req_values(req, 'email', user.email)
    user.address = assign_req_values(req, 'address', user.address)
    user.phone_address = assign_req_values(req, 'phone_address', user.phone_address)
    
    response = {
        'message': 'Successfully updated user information',
        'username': user.username,
        'email': user.email,
        'address': user.address,
        'phone_address': user.phone_address
    }
    db.session.commit()

    return jsonify(response), 200

@auth.route('/', methods=['GET'])
def get_users():
    users = find_users()

    user_array = []
    for user in users:
        user_array.append({
            'id': user.id,
            'username': user.username, 
            'email': user.email, 
            'address': user.address, 
            'phone_address': user.phone_address
        })

    return jsonify(user_array), 200

@auth.route('/<int:user_id>', methods=['GET'])
def get_single_users(user_id):
    user = find_user_by_id(user_id)
    if user == None:
        return jsonify({'message': 'User does not exist'}), 404
    single_user = {
        'id': user.id, 
        'username': user.id, 
        'email': user.email, 
        'address': user.address, 
        'phone_address': user.phone_address 
        }
    return jsonify(single_user)

@auth.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = find_user_by_id(user_id)

    if user == None:
        return jsonify({'message': 'User does not exist'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Successfully deleted user'})
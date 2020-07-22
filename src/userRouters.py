import os
from .dbhelpers import findByUsername, findByEmail, createUser
from flask import Blueprint, request, jsonify
from .models import User
from . import db

auth = Blueprint("auth", __name__)

@auth.route('/registration', methods=['POST'])
def register():
    values = request.json
    required = ['username', 'password', 'email']

    if not all(k in values for k in required):
        return jsonify({'message': 'Missing Required Values'}), 400

    if findByUsername(values["username"]) != None:
        return jsonify({'message': 'User by that usesrname already exists'}), 400
    if findByEmail(values["email"]) != None:
        return jsonify({'message': 'User by that email already exists'}), 400
    
    new_user = User(username=values["username"], email=values["email"], password=values["password"])
    createUser(new_user)

    return {}, 200
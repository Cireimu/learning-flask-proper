from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from src.models.auth import User
from src.dbhelpers import find_user_by_username, find_user_by_email
from flask import jsonify
import json
import jwt
import os

JWT_SECRET = os.environ.get('SECRET_KEY')
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 2000000

def create_jwt(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }

    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return jwt_token

def check_for_key(your_dict, key):
    if key in your_dict:
        return True
    return False

def assign_req_values(req_dict, key):
    new_value = None
    if check_for_key(req_dict, str(key)):
        new_value = req_dict[str(key)]
    return new_value
          
def check_for_user(data):
    if find_user_by_username(data) != None:
        return jsonify({'message': 'User by that username already exists.'})
    elif find_user_by_email(data) != None:
        return jsonify({'message': 'User by that email already exists'})
    return
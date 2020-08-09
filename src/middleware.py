from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from src.main import db
from src.models.models import User
from src.dbhelpers import find_user_by_username, find_user_by_email, find_user_by_id
from flask import jsonify, Response, request
from functools import wraps
from src.dbhelpers import find_user_by_email, find_user_by_username
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

def assign_req_values(req_dict, key, default_data):
    new_value = default_data
    if check_for_key(req_dict, str(key)):
        new_value = req_dict[str(key)]
    return new_value

def check_for_if_user_exist_helper(help_func, term):
    if help_func(term) != None:
        return jsonify({'message': f'{term}: {term} is taken'}), 401

def check_for_if_user_exist(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' in request.json and 'username' in request.json:
            email = request.json['email']
            username = request.json['username']
            if find_user_by_email(email) != None and find_user_by_username(username) != None:
                return jsonify({'message': f'Email: {email} and Username: {username} are taken'}),401
            if find_user_by_username(username) != None:
                return jsonify({'message': f'Username: {username} is taken'}),401
            if find_user_by_email(email) != None:
                return jsonify({'message': f'Email: {email} is taken'}),401
        if 'username' in request.json:
            username = request.json['username']
            if find_user_by_username(username) != None:
                message = f'Username: {username} already taken'
                return jsonify({'message': message}), 401
        if 'email' in request.json:
            email = request.json['email']
            if find_user_by_email(email) != None:
                message = f'Email: {email} already taken'
                return jsonify({'message': message}), 401
        return func(*args, **kwargs)
    return decorated_function

def add_restaurants_to_list(items):
    items_list = []
    for r in items:
        items_list.append({
            'id': r.id,
            'restaurant_name': r.restaurant_name,
            'restaurant_description': r.restaurant_description,
            'restaurant_rating': r.restaurant_rating,
            'restaurant_location': r.restaurant_location,
            'restaurant_hours_of_operation': r.restaurant_hours_of_operation,
            'restaurant_img_url = db.Column(db.String)': r.restaurant_img_url
        })
    return items_list
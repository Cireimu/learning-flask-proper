from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from src.main import db
from src.dbhelpers import find_user_by_username, find_user_by_email, find_user_by_id, get_restaurant_by_id, get_review_by_id
from flask import jsonify, Response, request
from functools import wraps
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

        items_list.append(r.serialize())
    return items_list

def check_for_restaurant(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if get_restaurant_by_id(request.view_args['restaurant_id']) == None:
            return jsonify({'message': 'No restaurant found by specified id'}), 404
        return func(*args, **kwargs)
    return decorated_function

def check_if_restaurant_id_valid(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        restaurant_id = None
        if 'restaurant_id' in request.view_args:
            restaurant_id = request.view_args['restaurant_id']
        else:
            restaurant_id = request.json['restaurant_id']
        if get_restaurant_by_id(restaurant_id) == None:
            return jsonify({'message': 'No restaurant found by specified id'}), 404
        return func(*args, **kwargs)
    return decorated_function

def check_if_user_id_valid(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user_id = None
        if 'user_id' in request.view_args:
            user_id = request.view_args['user_id']
        else:
            user_id = request.json['user_id']
        if find_user_by_id(user_id) == None:
            return jsonify({'message': 'No user found by specified id'}), 404
        return func(*args, **kwargs)
    return decorated_function

def create_review_list(review_list):
    new_list = []
    for r in review_list:
        new_list.append(r.serialize())
    return new_list

def check_if_review_id_valid(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        review_id = None
        if 'review_id' in request.view_args:
            review_id = request.view_args['review_id']
        else:
            review_id = request.json['review_id']
        
        if get_review_by_id(review_id) == None:
            return jsonify({'message': 'No review found by specified id'}), 404
        return func(*args, **kwargs)
    return decorated_function

def check_if_review_owned_by_user(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(request.view_args)
        review = get_review_by_id(request.view_args['review_id'])
        print(review)
        user_id = None
        if 'user_id' in request.view_args:
            user_id = request.view_args['user_id']
        else:
            user_id = request.json['user_id']
        print(user_id)
        if user_id != review.user_id :
            return jsonify({'message': 'You cannot edit reviews you do not own'}), 203
        return func(*args, **kwargs)
    return decorated_function
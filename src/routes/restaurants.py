from flask import Blueprint, request, jsonify, make_response
from src.models.models import Restaurant
from src.main import db
from src.middleware import assign_req_values, add_restaurants_to_list, get_restaurant_by_id
from src.dbhelpers import get_restaurants

restaurant = Blueprint('restaurant', __name__)

@restaurant.route('/', methods=['POST'])
def create_restuarant():
    req = request.json
    required = ['restaurant_name', 'restaurant_description', 'restaurant_img_url']

    if not all(k in req for k in required):
        return jsonify({'message': 'Missing Required Values'}), 400
    
    restaurant_name = req['restaurant_name']
    restaurant_description = req['restaurant_description']
    restaurant_img_url = req['restaurant_img_url']
    restaurant_rating = assign_req_values(req, 'restuarant_rating', None)
    restaurant_location = assign_req_values(req, 'restaurant_location', None)
    restaurant_hours_of_operation = assign_req_values(req, 'restaurant_hours_of_operation', None)

    new_restaurant = Restaurant(restaurant_name=restaurant_name, restaurant_description=restaurant_description, restaurant_img_url=restaurant_img_url, restaurant_rating=restaurant_rating, restaurant_location=restaurant_location, restaurant_hours_of_operation=restaurant_hours_of_operation)
    db.session.add(new_restaurant)
    db.session.commit()
    return jsonify({'message': 'Successfully add restaurant'}), 201

@restaurant.route('/', methods=['GET'])
def get_all_restaurants():
    restaurants = get_restaurants()

    restaurant_list = add_restaurants_to_list(restaurants)
    return jsonify(restaurant_list), 200
    
@restaurant.route('/<int:restaurant_id>', methods=['GET'])
def get_single_restaurant(restaurant_id):
    restaurant = get_restaurant_by_id(restaurant_id)
    if restaurant == None:
        return jsonify({'message': 'Could not find restaurant'}), 404
    single_restaurant = {
            'id': restaurant.id,
            'restaurant_name': restaurant.restaurant_name,
            'restaurant_description': restaurant.restaurant_description,
            'restaurant_rating': restaurant.restaurant_rating,
            'restaurant_location': restaurant.restaurant_location,
            'restaurant_hours_of_operation': restaurant.restaurant_hours_of_operation,
            'restaurant_img_url = db.Column(db.String)': restaurant.restaurant_img_url
        }
    return jsonify(single_restaurant), 200
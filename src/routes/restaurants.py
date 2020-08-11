from flask import Blueprint, request, jsonify, make_response
from src.models.models import Restaurant
from src.main import db
from src.middleware import assign_req_values, add_restaurants_to_list, get_restaurant_by_id, check_if_restaurant_id_valid, create_review_list
from src.dbhelpers import get_restaurants, get_reviews_by_restaurant

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
@check_if_restaurant_id_valid
def get_single_restaurant(restaurant_id):
    single_restaurant = get_restaurant_by_id(restaurant_id)
    return jsonify(single_restaurant.serialize()), 200

@restaurant.route('/<int:restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    req = request.json
    r = get_restaurant_by_id(restaurant_id)

    r.restaurant_name = assign_req_values(req, 'restaurant_name', r.restaurant_name)
    r.restaurant_description = assign_req_values(req, 'restaurant_description', r.restaurant_description)
    r.restaurant_img_url = assign_req_values(req, 'restaurant_img_url', r.restaurant_img_url)
    r.restaurant_rating = assign_req_values(req, 'restaurant_rating', r.restaurant_rating)
    r.restaurant_location = assign_req_values(req, 'restaurant_location', r.restaurant_location)
    r.restaurant_hours_of_operation = assign_req_values(req, 'restaurant_hours_of_operation', r.restaurant_hours_of_operation)
    db.session.commit()
    return jsonify({'message': 'Successfully updated restaurant'}, r.serialize()), 201

@restaurant.route('/<int:restaurant_id>', methods=['DELETE'])
@check_if_restaurant_id_valid
def delete_restaurant(restaurant_id):
    r = get_restaurant_by_id(restaurant_id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Successfully deleted restaurant'})

@restaurant.route('/<int:restaurant_id>/reviews', methods=['GET'])
@check_if_restaurant_id_valid
def get_restaurant_reviews(restaurant_id):
    reviews = create_review_list(get_reviews_by_restaurant(restaurant_id))

    if len(reviews) == 0:
        return jsonify({'message': 'There are no reviews for this restaurant yet!'})
    return jsonify(reviews)
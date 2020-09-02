import os
from flask import Blueprint, request, jsonify, make_response
from src.models import User, UserSchema
from src.dbhelpers import (
    find_user_by_username,
    create_user,
    find_user_by_id,
    find_user_by_email,
    find_users,
    get_review_by_user_id,
)
from src.middleware import (
    create_jwt,
    assign_req_values,
    check_for_if_user_exist,
    check_if_user_id_valid,
    create_review_list,
    get_review_by_id,
    check_if_review_id_valid,
    check_if_review_owned_by_user,
    create_new_user,
)
from src.main import db

auth = Blueprint("auth", __name__)


@auth.route("/registration", methods=["POST"])
@check_for_if_user_exist
def register():
    req = request.json
    required = ["username", "password", "email"]

    if not all(k in req for k in required):
        return jsonify({"message": "Missing Required Values"}), 400

    new_user = create_new_user(req)
    new_user.set_password(req["password"])
    create_user(new_user)

    current_user = find_user_by_username(req["username"])
    jwt_token = create_jwt(current_user)

    return jsonify({"key": jwt_token.decode("ascii")}), 200


@auth.route("/login", methods=["POST"])
def login():
    req = request.json
    user = find_user_by_username(req["username"])
    if user and user.check_password(password=req["password"]):
        jwt_token = create_jwt(user)
        return jsonify({"key": jwt_token.decode("ascii")}), 200
    return jsonify({"message": "Invalid username/password combination"})


@auth.route("/<int:id>", methods=["PUT"])
@check_for_if_user_exist
def update_user(id):
    req = request.json
    user = find_user_by_id(id)

    user.username = assign_req_values(req, "username", user.username)
    user.password = assign_req_values(req, "password", user.password)
    user.email = assign_req_values(req, "email", user.email)
    user.address = assign_req_values(req, "address", user.address)
    user.phone_address = assign_req_values(req, "phone_address", user.phone_address)
    result = UserSchema().dump(user)
    response = {
        "message": "Successfully updated user information",
    }
    db.session.commit()

    return jsonify(response, result), 200


@auth.route("/", methods=["GET"])
def get_users():
    users = find_users()

    users_schema = UserSchema(many=True)

    return jsonify(users_schema.dump(users)), 200


@auth.route("/<int:user_id>", methods=["GET"])
def get_single_users(user_id):
    user = find_user_by_id(user_id)
    if user == None:
        return jsonify({"message": "User does not exist"}), 404
    user_schema = UserSchema().dump(user)
    return jsonify(user_schema)


@auth.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = find_user_by_id(user_id)

    if user == None:
        return jsonify({"message": "User does not exist"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Successfully deleted user"})


@auth.route("/<int:user_id>/reviews", methods=["GET"])
@check_if_user_id_valid
def get_user_reviews(user_id):
    reviews = create_review_list(get_review_by_user_id(user_id))

    if len(reviews) == 0:
        return jsonify({"message": "No reviews are associated yet with this user"})
    return jsonify(reviews)


@auth.route("/<int:user_id>/<int:review_id>", methods=["DELETE"])
@check_if_review_id_valid
@check_if_review_owned_by_user
def delete_review(review_id, user_id):
    review = get_review_by_id(review_id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Successfully deleted review"})

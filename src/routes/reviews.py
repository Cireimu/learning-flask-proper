from flask import Blueprint, request, jsonify
from src.models import Review
from src.middleware import (
    assign_req_values,
    check_if_restaurant_id_valid,
    check_if_user_id_valid,
    check_if_review_id_valid,
    check_if_review_owned_by_user,
)
from src.dbhelpers import get_review_by_id
from src.main import db

review = Blueprint("review", __name__)


@review.route("/", methods=["POST"])
@check_if_user_id_valid
@check_if_restaurant_id_valid
def create_review():
    req = request.json
    required = ["user_id", "review_score", "review_title", "restaurant_id"]

    if not all(k in req for k in required):
        return jsonify({"message": "Missing required fields"}), 400

    review_title = req["review_title"]
    review_description = assign_req_values(req, "review_description", None)
    review_score = req["review_score"]
    user_id = req["user_id"]
    restaurant_id = req["restaurant_id"]

    new_review = Review(
        review_title=review_title,
        review_description=review_description,
        review_score=review_score,
        user_id=user_id,
        restaurant_id=restaurant_id,
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Successfuly added review"}), 200


@review.route("/<int:review_id>", methods=["PUT"])
@check_if_review_id_valid
@check_if_review_owned_by_user
def update_review(review_id):
    req = request.json
    review = get_review_by_id(review_id)

    review.update(req)
    return jsonify(review.serialize()), 200


@review.route("/<int:review_id>", methods=["DELETE"])
@check_if_review_id_valid
@check_if_review_owned_by_user
def delete_review(review_id):
    review = get_review_by_id(review_id)

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Successfully deleted review"})

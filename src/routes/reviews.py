from flask import Blueprint, request, jsonify
from src.models.models import Review
from src.middleware import assign_req_values
from src.main import db

review = Blueprint('review', __name__)

@review.route('/', methods=['POST'])
def create_review():
    req = request.json
    required = ['user_id', 'review_score', 'review_title']

    if not all(k in req for k in required):
        return jsonify({'message': 'Missing required fields'}), 400
    
    review_title = req['review_title']
    review_description = assign_req_values(req, 'review_description', None)
    review_score = req['review_score']
    user_id = req['user_id']

    new_review = Review(review_title=review_title, review_description=review_description, review_score=review_score, user_id=user_id)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Successfuly added review'}), 200
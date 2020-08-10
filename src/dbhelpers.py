import os
from .main import db
from .models.models import User, Restaurant, Review

def find_users():
    return User.query.all()

def find_user_by_username(username):
    return User.query.filter_by(username=username).first()

def find_user_by_email(email):
    return User.query.filter_by(email=email).first()

def find_user_by_id(id):
   return User.query.filter_by(id=id).first()

def create_user(new_user):
    db.session.add(new_user)
    return db.session.commit()

def delete_user(id):
    User.query.filter_by(id=id).delete()
    return db.session.commit()

def get_restaurants():
    return Restaurant.query.all()

def get_restaurant_by_id(id):
    return Restaurant.query.filter_by(id=id).first()

def get_reviews():
    return Review.query.all()

def get_review_by_id(id):
    return Review.query.filter_by(id=id).first()

def create_review(new_review):
    db.session.add(new_review)
    return db.session.commit()

def delete_review(id):
    Review.query.filter_by(id=id).delete()
    return db.session.commit()

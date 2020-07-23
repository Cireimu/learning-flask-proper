import os
from .main import db
from .models.auth import User

def findUsers():
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
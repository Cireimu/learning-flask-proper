import os
from . import db
from .models import User

def findUsers():
    return User.query.all()

def findByUsername(username):
    return User.query.filter_by(username=username).first()

def findByEmail(email):
    return User.query.filter_by(email=email).first()

def findUserById(id):
   return User.query.filter_by(id=id).first()

def createUser(new_user):
    db.session.add(new_user)
    return db.session.commit()

def deleteUser(id):
    User.query.filter_by(id=id).delete()
    return db.session.commit()
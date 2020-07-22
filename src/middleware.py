from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import jwt
import os

JWT_SECRET = os.environ.get('SECRET_KEY')
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 2000000

def create_jwt(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }

    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return jwt_token
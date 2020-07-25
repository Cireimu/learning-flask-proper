from src.main import db
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String(50))
    phone_address = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, index=False)
    last_login = db.Column(db.DateTime, index=False)

    def __init__(self, username, email, password, address=None, phone_address=None):
        self.username = username
        self.email = email
        self.password = password
        self.address = address
        self.phone_address = phone_address

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

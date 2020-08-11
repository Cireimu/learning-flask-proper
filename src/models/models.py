from src.main import db
from werkzeug.security import generate_password_hash, check_password_hash

def check_for_key(your_dict, key):
    if key in your_dict:
        return True
    return False

def assign_req_values(req_dict, key, default_data):
    new_value = default_data
    if check_for_key(req_dict, str(key)):
        new_value = req_dict[str(key)]
    return new_value

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

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String, nullable=False)
    restaurant_description = db.Column(db.String, nullable=False)
    restaurant_rating = db.Column(db.Integer)
    restaurant_location = db.Column(db.String)
    restaurant_hours_of_operation = db.Column(db.String)
    restaurant_img_url = db.Column(db.String)

    def __init__(self, restaurant_name, restaurant_description, restaurant_rating, restaurant_location, restaurant_hours_of_operation, restaurant_img_url):
        self.restaurant_name = restaurant_name
        self.restaurant_description = restaurant_description
        self.restaurant_rating = restaurant_rating
        self.restaurant_location = restaurant_location
        self.restaurant_hours_of_operation = restaurant_hours_of_operation
        self.restaurant_img_url = restaurant_img_url
        
    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'restaurant_name': self.restaurant_name,
            'restaurant_description': self.restaurant_description,
            'restaurant_rating': self.restaurant_rating,
            'restaurant_location': self.restaurant_location,
            'restaurant_hours_of_operation': self.restaurant_hours_of_operation,
            'restaurant_img_url = db.Column(db.String)': self.restaurant_img_url
        }

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    review_title = db.Column(db.String)
    review_description = db.Column(db.String)
    review_score = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, review_title, review_description, review_score, user_id, restaurant_id):
        self.review_title = review_title
        self.review_description = review_description
        self.review_score = review_score
        self.user_id = user_id
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'review_title': self.review_title,
            'review_description': self.review_description,
            'review_score': self.review_score,
            'restaurant_id': self.restaurant_id,
            'user_id': self.user_id
        }
    def update(self, req):
        
        self.review_title = assign_req_values(req, 'review_title', self.review_title)
        self.review_description = assign_req_values(req, 'review_description', self.review_description)
        self.review_score = assign_req_values(req, 'review_score', self.review_score)
        return db.session.commit()


class Menu_Item(db.Model):
    __tablename__ = 'menu_item'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False)
    item_price = db.Column(db.Integer, nullable=False)
    item_rating = db.Column(db.Integer, nullable=False)
    item_img = db.Column(db.Integer, nullable=False)
    test = db.Column(db.String)

    def __init__(self, item_name, item_price, item_rating, item_img):
        self.item_name = item_name
        self.item_price = item_price
        self.item_rating = item_rating
        self.item_img = item_img

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Restaurant_Item(db.Model):
    __tablename__ = 'restaurant_items'

    __table_args__ = (
        db.PrimaryKeyConstraint('restaurant_id', 'menu_item_id'),
    )

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)

    def __init__(self, restaurant_id, menu_item_id):
        self.restaurant_id = restaurant_id
        self.menu_item_id = menu_item_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    app.config.from_object(os.environ["APP_SETTINGS"])

    db.init_app(app)

    from src.routes.auth import auth
    from src.routes.restaurants import restaurant
    from src.routes.reviews import review

    app.register_blueprint(auth, url_prefix="/api/auth")
    app.register_blueprint(restaurant, url_prefix="/api/restaurants")
    app.register_blueprint(review, url_prefix="/api/reviews")
    return app

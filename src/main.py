import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    app.config.from_object(os.environ['APP_SETTINGS'])

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from src.models.auth import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        if user_id is not None:
            return User.query.get(user_id)
        print("Something Broke")

    from src.routes.auth import auth
    app.register_blueprint(auth, url_prefix='/api/auth')

    return app

from src import create_app
from flask_marshmallow import Marshmallow
from src import db
new_user = User(username="my name ethan", password="password123", email="email@email.com")

print(new_user.username)
app = create_app()

ma = Marshmallow(app)

if __name__ == '__main__':
    app.run(debug=True)
from src import create_app
from flask_marshmallow import Marshmallow
from src import db

app = create_app()

ma = Marshmallow(app)

if __name__ == '__main__':
    app.run(debug=True)

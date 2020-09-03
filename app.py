from src.main import create_app, db
from flask_marshmallow import Marshmallow

app = create_app()

ma = Marshmallow(app)

if __name__ == "__main__":
    app.run(debug=True)

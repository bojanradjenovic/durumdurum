from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db
from routes.auth import init_auth
import json

with open('config.json') as config_file:
    config = json.load(config_file)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SECRET_KEY'] = config['SECRET_KEY'] 
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri='redis://localhost:6379',
    default_limits=["200 per day", "50 per hour"]
)
db.init_app(app)

with app.app_context():
    db.create_all()

init_auth(app, limiter)
if __name__ == '__main__':
    app.run(debug=True)
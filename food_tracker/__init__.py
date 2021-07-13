from flask import Flask, app

from .main.routes import main
# import database obj from extensions
from .extensions import db

def create_app():
    app = Flask(__name__)

    # Configuration for database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initializes app with database obj
    db.init_app(app)

    app.register_blueprint(main)

    return app
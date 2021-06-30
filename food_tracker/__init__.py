from flask import Flask, app

from .main.routes import main

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main)

    return app
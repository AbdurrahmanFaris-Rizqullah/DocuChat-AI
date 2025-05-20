from flask import Flask
from app.routes.ask import ask_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(ask_bp)
    return app

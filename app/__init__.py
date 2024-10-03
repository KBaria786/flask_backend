from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .blueprints import main_bp, error_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(error_bp)

    return app
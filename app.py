import os
from flask import Flask, Blueprint
from flask_restful import Api
from resources.nest import Nest
from config import app_config


api_bp = Blueprint('api', __name__)
api = Api(api_bp)
api.add_resource(Nest, '')


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(app_config[config_filename])
    app.config.from_pyfile('config.py')

    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


if __name__ == "__main__":
    environment = os.getenv('FLASK_ENV') or 'development'
    app = create_app(environment)
    app.run(debug=True)
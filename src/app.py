from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

from flasgger import Swagger
from .database import db
from .config import Config
from .controllers.math_controller import math_bp
from .controllers.auth_controller import auth_bp
from flask_jwt_extended import JWTManager

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Math Microservice API",
        "description": "API for math operations with JWT authentication",
        "version": "0.1.0",
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'",
        }
    },
    "security": [{"Bearer": []}],
}


def create_app():
    app = Flask(__name__)

    # Load settings
    app.config.from_object(Config)
    Swagger(app, template=swagger_template)
    JWTManager(app)
    # Initialize extensions
    db.init_app(app)
    PrometheusMetrics(app)  # Exposes /metrics for monitoring

    # Ensure tables exist
    with app.app_context():
        db.create_all()

    # Register your math Blueprint
    app.register_blueprint(math_bp)
    app.register_blueprint(auth_bp)

    return app


if __name__ == "__main__":
    # When run directly, start the development server
    create_app().run(host="0.0.0.0", port=5000)

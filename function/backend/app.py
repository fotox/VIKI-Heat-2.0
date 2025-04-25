from flask import Flask
from flask_cors import CORS

from function.backend.api.devices.routes import devices_bp
from function.backend.config import Config
from function.backend.extensions import db, jwt, socketio
from function.backend.api.auth.routes import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    CORS(app)

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(devices_bp, url_prefix="/api/devices")

    @app.route("/")
    def index():
        return {"message": "VIKI Backend API läuft"}

    return app


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=5000)

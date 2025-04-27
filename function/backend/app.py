from flask import Flask
from flask_cors import CORS

from api.devices.routes import devices_bp
from config import Config
from extensions import db, jwt, socketio
from api.auth.routes import auth_bp


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
        return {"message": "VIKI Backend API run..."}

    return app


if __name__ == "__main__":
    viki = create_app()
    socketio.run(viki, host="127.0.0.1", port=5000, debug=True)

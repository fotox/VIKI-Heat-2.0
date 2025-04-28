from flask import Flask
from flask_cors import CORS

from api.auth.routes import auth_bp
from api.devices.routes import devices_bp
from api.settings import settings_bp

from extensions import db, jwt, socketio
from config import Config


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    CORS(app)

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(devices_bp, url_prefix="/api/devices")
    app.register_blueprint(settings_bp, url_prefix="/api/settings")

    with app.app_context():
        db.create_all()

        from api.auth.user import User
        with app.app_context():
            db.create_all()
            # Default-Admin anlegen, falls noch nicht existiert
            if not User.query.filter_by(username="admin").first():
                admin = User(username="admin", role="admin")
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()

    @app.route("/")
    def index():
        return {"message": "VIKI Backend API läuft"}

    return app


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from threading import Thread

from api.auth.routes import auth_bp
from api.dashboard.routes import dashboard_bp
from api.settings import settings_bp
from api.dashboard.modules import modules_bp
from services.heating import heat_pipe
from database.init_db import seed_users, seed_roles, seed_manufacturers, seed_category, seed_location


from extensions import db, jwt, socketio
from config import Config

DEV_MODE: bool = True


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    Swagger(app, template_file='swagger_config.yml')
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    CORS(app)

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(settings_bp, url_prefix="/api/settings")
    app.register_blueprint(modules_bp, url_prefix="/api/modules")

    with app.app_context():
        db.create_all()
        seed_roles()
        seed_users()
        seed_category()
        seed_manufacturers()
        seed_location()

    def start_controller():
        heat_pipe.run_loop()

    thread = Thread(target=start_controller, daemon=True)
    thread.start()

    @app.route("/")
    def index():
        return {"message": "VIKI Backend API läuft"}

    return app


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

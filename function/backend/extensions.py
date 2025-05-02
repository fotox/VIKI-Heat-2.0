from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from sqlalchemy.dialects import postgresql

db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()
sql = postgresql

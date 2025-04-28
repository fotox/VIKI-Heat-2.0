import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///viki.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MASTER_RESET_KEY = os.environ.get("MASTER_RESET_KEY", "viki-masterkey")

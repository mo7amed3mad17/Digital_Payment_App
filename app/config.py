import os
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_fallback_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super_secret_jwt_key")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///aggregator.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
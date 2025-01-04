import os
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_fallback_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super_secret_jwt_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://digital_payments_app_gg5x_user:HC4NPPHmXke9xaqD1HK00q3tv9YDwpBH@dpg-ctsiknjqf0us73dsv39g-a.oregon-postgres.render.com/digital_payments_app_gg5x")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
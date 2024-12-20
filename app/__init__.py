from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)

    # Import and register routes
    from app.routes.user_routes import user_routes
    app.register_blueprint(user_routes, url_prefix="/api/v1")

    # Import models
    from app.models.user import User
    from app.models.account import Account
    from app.models.transaction import Transaction

    return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)

    from app.routes.user_routes import user_routes
    app.register_blueprint(user_routes, url_prefix="/api/v1")

    return app
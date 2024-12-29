from app import create_app, db
from flask_jwt_extended import JWTManager

app = create_app()

# Initialize JWT Manager
jwt = JWTManager(app)

if __name__ == "__main__":
    with app.app_context():
        # Uncomment the following lines if testing or resetting database schema.
        #print(create_app.jinja_env.list_templates())
        #db.drop_all()
        db.create_all()
        #pass  # Do nothing during normal runs.
    app.run(debug=True)

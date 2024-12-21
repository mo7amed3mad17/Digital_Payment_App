from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User

user_routes = Blueprint('user', __name__)

@user_routes.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user": user.id}), 201

@user_routes.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users]), 200
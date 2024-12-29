from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.account import Account

user_routes = Blueprint('user', __name__)



@user_routes.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')

    if not all([username, email, password, phone_number]):
        return jsonify({"error": "Missing required fields"}), 400

    # Create the user instance
    user = User(username=username, email=email, phone_number=phone_number)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()  # Commit user to assign an ID

        # Create the account for the new user
        account_number = user.id + 2003621  # Generate account number as per your logic
        account = Account(user_id=user.id, account_number=str(account_number))
        db.session.add(account)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    # No manual db.session.close() here
    return jsonify({
        "message": "User and account registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
        "account": {
            "id": account.id,
            "account_number": account.account_number,
            "balance": account.balance,
        }
    }), 201


@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200


@user_routes.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users]), 200

@user_routes.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    return jsonify({
        "id": user.id,
        "username": user.username,
    }), 200

@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    account = Account.query.filter_by(user_id=user_id).first()
    if not account:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
        },
        "account": {
            "account_number": account.account_number,
            "balance": account.balance,
            "created_at": account.created_at,
        }
    }), 200

@user_routes.route('/account', methods=['GET'])
@jwt_required()
def get_account_data():
    try:
        current_user_id = get_jwt_identity()
        print(f"Decoded user ID from token: {current_user_id}")  # Debug log

        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        account = Account.query.filter_by(user_id=current_user_id).first()
        if not account:
            return jsonify({"msg": "Account not found"}), 404

        return jsonify({
            "username": user.username,
            "balance": account.balance
        }), 200
    except Exception as e:
        print(f"Error in /account route: {e}")  # Log error details
        return jsonify({"msg": "Internal server error"}), 500


@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    for account in user.accounts:
        for transaction in account.transactions:
            db.session.delete(transaction)
        db.session.delete(account)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User and all associated accounts and transactions deleted successfully"}), 200

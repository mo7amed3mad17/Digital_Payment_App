from flask import Blueprint, request, jsonify
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
    user = User(username=username, email=email, password=password, phone_number=phone_number)

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


@user_routes.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users]), 200

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

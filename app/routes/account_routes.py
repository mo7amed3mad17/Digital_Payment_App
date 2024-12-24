from flask import Blueprint, request, jsonify
from app import db
from app.models.account import Account
from app.models.user import User

account_routes = Blueprint('account', __name__)

@account_routes.route('/accounts', methods=['POST'])
def add_account():
    data = request.get_json()
    user_id = data.get('user_id')
    account_number = data.get('account_number')
    balance = data.get('balance')

    if not all([user_id, bank_name, account_number, balance]):
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    account = Account(
        user_id=user_id,
        account_number=account_number,
        balance=balance
    )
    db.session.add(account)
    db.session.commit()

    return jsonify({"message": "Account added successfully", "account": account.id}), 201

@account_routes.route('/accounts/<int:user_id>', methods=['GET'])
def get_accounts(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    accounts = Account.query.filter_by(user_id=user_id).all()
    return jsonify([
        {"id": acc.id, "account_number": acc.account_number, "balance": acc.balance}
        for acc in accounts
    ]), 200

@account_routes.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Account deleted successfully"}), 200

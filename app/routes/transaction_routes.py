from flask import Blueprint, request, jsonify
from app import db
from app.models.transaction import Transaction
from app.models.account import Account
from app.models.user import User

transaction_routes = Blueprint('transaction', __name__)



@transaction_routes.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    sender_acc_num = data.get('sender_acc_num')
    receiver_acc_num = data.get('receiver_acc_num')
    receiver_username = data.get('receiver_username')
    amount = data.get('amount')
    description = data.get('description', '')

    # Validate input
    if not all([sender_acc_num, receiver_acc_num, receiver_username, amount]):
        return jsonify({"error": "Missing required fields"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    # Verify sender and receiver accounts
    sender_account = Account.query.filter_by(account_number=sender_acc_num).first()
    receiver_account = Account.query.filter_by(account_number=receiver_acc_num).first()

    if not sender_account:
        return jsonify({"error": "Sender account not found"}), 404

    if not receiver_account:
        return jsonify({"error": "Receiver account not found"}), 404

    # Check sufficient balance
    if sender_account.balance < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    # Create transaction
    try:
        transaction = Transaction(
            sender_acc_num=sender_acc_num,
            receiver_acc_num=receiver_acc_num,
            receiver_username=receiver_username,
            amount=amount,
            description=description
        )

        # Deduct from sender and add to receiver
        sender_account.balance -= amount
        receiver_account.balance += amount

        db.session.add(transaction)
        db.session.commit()

        return jsonify({
            "message": "Transaction completed successfully",
            "transaction": {
                "id": transaction.id,
                "datetime": transaction.datetime,
                "sender_acc_num": transaction.sender_acc_num,
                "receiver_acc_num": transaction.receiver_acc_num,
                "receiver_username": transaction.receiver_username,
                "amount": transaction.amount,
                "description": transaction.description
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@transaction_routes.route('/transactions/<int:user_id>', methods=['GET'])
def get_user_transactions(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    sent = [{"id": t.id, "amount": t.amount, "to": t.receiver_id} for t in user.sent_transactions]
    received = [{"id": t.id, "amount": t.amount, "from": t.sender_id} for t in user.received_transactions]

    return jsonify({"sent": sent, "received": received}), 200
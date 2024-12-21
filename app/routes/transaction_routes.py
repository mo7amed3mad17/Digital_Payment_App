from flask import Blueprint, request, jsonify
from app import db
from app.models.transaction import Transaction
from app.models.user import User

transaction_routes = Blueprint('transaction', __name__)

@transaction_routes.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    amount = data.get('amount')
    transaction_type = data.get('transaction_type')

    if not all([sender_id, receiver_id, amount, transaction_type]):
        return jsonify({"error": "Missing required fields"}), 400

    sender = User.query.get(sender_id)
    receiver = User.query.get(receiver_id)

    if not sender or not receiver:
        return jsonify({"error": "Invalid sender or receiver"}), 400

    transaction = Transaction(
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=amount,
        transaction_type=transaction_type
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction created successfully", "transaction": transaction.id}), 201

@transaction_routes.route('/transactions/<int:user_id>', methods=['GET'])
def get_user_transactions(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    sent = [{"id": t.id, "amount": t.amount, "to": t.receiver_id} for t in user.sent_transactions]
    received = [{"id": t.id, "amount": t.amount, "from": t.sender_id} for t in user.received_transactions]

    return jsonify({"sent": sent, "received": received}), 200
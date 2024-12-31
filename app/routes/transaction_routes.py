from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.transaction import Transaction
from app.models.account import Account
from app.models.user import User

transaction_routes = Blueprint('transaction', __name__, url_prefix='/api/v1/transactions')



@transaction_routes.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    # Get the logged-in user's ID
    current_user_id = int(get_jwt_identity())
    
    # Parse JSON request data
    data = request.get_json()
    sender_acc_num = data.get('sender_acc_num')
    sender_username = data.get('sender_username')
    receiver_acc_num = data.get('receiver_acc_num')
    receiver_username = data.get('receiver_username')
    amount = data.get('amount')
    description = data.get('description')

    # Validate required fields
    if not all([sender_acc_num, receiver_acc_num, receiver_username, amount]):
        return jsonify({"msg": "All fields are required"}), 400

    # Convert amount to a float and validate
    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({"msg": "Amount must be greater than 0"}), 400
    except ValueError:
        return jsonify({"msg": "Invalid amount"}), 400

    # Fetch the sender's account and validate
    sender_account = Account.query.filter_by(account_number=sender_acc_num).first()
    if not sender_account or sender_account.user_id != current_user_id:
        return jsonify({"msg": "Invalid sender account"}), 403

    if sender_account.balance < amount:
        return jsonify({"msg": "Insufficient funds"}), 400

    # Fetch the receiver's account and validate
    receiver_account = Account.query.filter_by(account_number=receiver_acc_num).first()
    if not receiver_account or receiver_account.user.username != receiver_username:
        return jsonify({"msg": "Invalid receiver account or username mismatch"}), 404

    # Perform the transfer
    sender_account.balance -= amount
    receiver_account.balance += amount

    # Create a new transaction record
    transaction = Transaction(
        sender_acc_num=sender_account.account_number,
        sender_username=sender_username,
        receiver_acc_num=receiver_account.account_number,
        receiver_username=receiver_username,
        amount=amount,
        description=description
    )
    db.session.add(transaction)

    # Commit the changes
    db.session.commit()

    return jsonify({
        "msg": "Transfer successful",
        "transaction": {
            #"transaction_id": transaction.id,
            "sender_acc_num": sender_acc_num,
            "sender_username": sender_username,
            "receiver_acc_num": receiver_acc_num,
            "receiver_username": receiver_username,
            "amount": amount,
            "description": description,
            "timestamp": transaction.datetime
        }
    }), 200


@transaction_routes.route('/transactions/<int:user_id>', methods=['GET'])
def get_user_transactions(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    sent = [{"id": t.id, "amount": t.amount, "to": t.receiver_acc_num, "datetime": t.datetime} for t in user.transactions_sent]
    received = [{"id": t.id, "amount": t.amount, "from": t.sender_acc_num, "datetime": t.datetime} for t in user.transactions_received]

    return jsonify({"sent": sent, "received": received}), 200
from app import db, create_app
from app.models.user import User
from app.models.transaction import Transaction

# Create a Flask app for testing purposes
app = create_app()

# Start the Flask app context
with app.app_context():
    # Drop all tables and recreate them to ensure a fresh test
    db.drop_all()
    db.create_all()

    # Create two test users
    user1 = User(username="testuser1", email="Mohamed1@example.com", password="password123")
    user2 = User(username="testuser2", email="Abdallah2@example.com", password="password123")

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    print(f"Created Users: {user1} and {user2}")

    # Create a transaction between the two users
    transaction = Transaction(
        sender_id=user1.id,
        receiver_id=user2.id,
        amount=100.50,
        transaction_type="debit"  # Changed from "transfer" to "debit"
    )

    db.session.add(transaction)
    db.session.commit()

    print(f"Created Transaction: {transaction}")

    # Fetch all transactions
    transactions = Transaction.query.all()
    print(f"All Transactions: {transactions}")

    # Fetch specific user transactions
    sent_transactions = user1.sent_transactions
    received_transactions = user2.received_transactions

    print(f"Transactions sent by {user1.username}: {sent_transactions}")
    print(f"Transactions received by {user2.username}: {received_transactions}")

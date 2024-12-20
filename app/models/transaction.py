from app import db
from datetime import datetime

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # 'credit' or 'debit'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_transactions')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_transactions')

    def __init__(self, sender_id, receiver_id, amount, transaction_type):
        allowed_types = ['credit', 'debit']
        if transaction_type not in allowed_types:
            raise ValueError(f"Invalid transaction_type: {transaction_type}. Allowed types are {allowed_types}.")
        
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.transaction_type = transaction_type

    def __repr__(self):
        return f"<Transaction {self.id} | {self.transaction_type} | {self.amount}>"

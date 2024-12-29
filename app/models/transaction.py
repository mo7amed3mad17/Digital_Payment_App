from app import db
from datetime import datetime

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    sender_acc_num = db.Column(db.String(50), db.ForeignKey('account.account_number'), nullable=False)  # Links to account_number
    sender_username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    receiver_acc_num = db.Column(db.String(50), db.ForeignKey('account.account_number'), nullable=False)  # Links to account_number
    receiver_username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)  # Links to username
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(60), nullable=True)

    # Relationships for ORM queries
    sender_account = db.relationship('Account', foreign_keys=[sender_acc_num], backref='transactions_sent')
    receiver_account = db.relationship('Account', foreign_keys=[receiver_acc_num], backref='transactions_received')

    def __repr__(self):
        return f"<Transaction {self.id}: {self.amount} from {self.sender_acc_num} to {self.receiver_acc_num}>"
from app import db
from datetime import datetime

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_number = db.Column(db.String(50), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=5000)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, account_number):
         self.user_id = user_id 
         self.account_number = str(user_id + 2003621) # Generate account_number based on user_id

    def __repr__(self):
        return f"<Account {self.account_number}>"
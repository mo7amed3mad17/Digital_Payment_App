from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    accounts = db.relationship('Account', backref='user', lazy=True)
    transactions_received = db.relationship('Transaction', foreign_keys='Transaction.receiver_username', backref='receiver', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

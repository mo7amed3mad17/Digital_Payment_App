from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    accounts = db.relationship('Account', backref='user', lazy=True)
    transactions_received = db.relationship('Transaction', foreign_keys='Transaction.receiver_username', backref='receiver', lazy=True)
    transactions_sent = db.relationship('Transaction', foreign_keys='Transaction.sender_username', backref='sender', lazy=True)

    def set_password(self, password):
        """Hash the password and store it in the password_hash field."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the hashed password with the provided password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

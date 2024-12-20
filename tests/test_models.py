import unittest
from app import create_app, db
from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction

class TestModels(unittest.TestCase):

    def setUp(self):
        """Set up the test app and database."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()  # Create all tables

    def tearDown(self):
        """Tear down the database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_model(self):
        """Test the User model."""
        with self.app.app_context():
            user = User(username='testuser', email='testuser@example.com', password='password123')
            db.session.add(user)
            db.session.commit()

            fetched_user = User.query.first()
            self.assertIsNotNone(fetched_user)
            self.assertEqual(fetched_user.username, 'testuser')
            self.assertEqual(fetched_user.email, 'testuser@example.com')

    def test_account_model(self):
        """Test the Account model."""
        with self.app.app_context():
            user = User(username='testuser', email='testuser@example.com', password='password123')
            db.session.add(user)
            db.session.commit()

            account = Account(bank_name='Test Bank', account_number='123456789', balance=1000.0, user_id=user.id)
            db.session.add(account)
            db.session.commit()

            fetched_account = Account.query.first()
            self.assertIsNotNone(fetched_account)
            self.assertEqual(fetched_account.bank_name, 'Test Bank')
            self.assertEqual(fetched_account.user_id, user.id)

    def test_transaction_model(self):
        """Test the Transaction model."""
        with self.app.app_context():
            user = User(username="sender", email="sender@example.com", password="password123")
            another_user = User(username="receiver", email="receiver@example.com", password="password123")
            db.session.add(user)
            db.session.add(another_user)
            db.session.commit()


            account = Account(bank_name='Test Bank', account_number='123456789', balance=1000.0, user_id=user.id)
            db.session.add(account)
            db.session.commit()

            transaction = Transaction(
            sender_id=user.id,  # Assuming `user` is defined in your test setup
            receiver_id=another_user.id,  # Assuming `another_user` is defined in your test setup
            amount=200.0,
            transaction_type='debit'
            )

            db.session.add(transaction)
            db.session.commit()

            fetched_transaction = Transaction.query.first()
            self.assertIsNotNone(fetched_transaction)
            self.assertEqual(fetched_transaction.amount, 200.0)
            self.assertEqual(fetched_transaction.transaction_type, 'debit')

if __name__ == '__main__':
    unittest.main()
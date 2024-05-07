import unittest
from flask_testing import TestCase
from app import app, transactions


class TestTransactionService(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        return app

    def setUp(self):
        self.client = app.test_client()
        transactions.clear()
        self.test_transaction = {
            "amount": 100.0,
            "transaction_date": "2024-01-01",
            "currency": "USD"
        }

    def test_create_transaction(self):
        response = self.client.post('/create', json=self.test_transaction)
        self.assertEqual(response.status_code, 201)
        self.assertIn('transaction_date', response.json)
        self.assertIn('2024-01-01', response.json['transaction_date'])

    def test_create_transaction_bad_request(self):
        # Missing 'amount' field
        bad_data = {
            "transaction_date": "2024-01-01",
            "currency": "USD"
        }
        response = self.client.post('/create', json=bad_data)
        self.assertEqual(response.status_code, 400)

    def test_get_transactions_empty(self):
        response = self.client.get('/transactions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_transactions_with_data(self):
        # First, create a transaction
        self.client.post('/create', json=self.test_transaction)
        # Then retrieve transactions
        response = self.client.get('/transactions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['amount'], 100.0)


if __name__ == '__main__':
    unittest.main()

from flask import Flask, request, jsonify
from datetime import datetime
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# In-memory storage for transactions
transactions = []


class Transaction:
    def __init__(self, amount: float, transaction_date: str, currency: str):
        self.amount = amount
        self.transaction_date = datetime.strptime(transaction_date, '%Y-%m-%d')
        self.currency = currency

    def details(self):
        return {
            "amount": self.amount,
            "transaction_date": self.transaction_date.strftime('%Y-%m-%d'),
            "currency": self.currency
        }


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


@app.route('/create', methods=['POST'])
def create_transaction():
    data = request.get_json()
    if not data or not all(key in data for key in ['amount', 'transaction_date', 'currency']):
        app.logger.error("Invalid data provided")
        return jsonify({"error": "Invalid data"}), 400

    try:
        transaction = Transaction(
            float(data['amount']), data['transaction_date'], data['currency'])
    except (ValueError, TypeError) as e:
        app.logger.error("Error creating transaction: %s", e)
        return jsonify({"error": str(e)}), 400

    transactions.append(transaction)
    app.logger.info("Transaction created successfully")
    return jsonify(transaction.details()), 201


@app.route('/transactions', methods=['GET'])
def get_transactions():
    app.logger.info("All transactions retrieved successfully")
    return jsonify([trans.details() for trans in transactions]), 200


if __name__ == '__main__':
    app.run(debug=True)

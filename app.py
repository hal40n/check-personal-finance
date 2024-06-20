from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<Expense {self.date} {self.category} {self.amount} {self.description}>'

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    new_expense = Expense(
        date=data['date'],
        category=data['category'],
        amount=data['amount'],
        description=data['description']
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'status': 'success'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, request, jsonify
from google_sheets import get_sheets_service
from dotenv import load_dotenv

import os

app = Flask(__name__)

load_dotenv()

spreadsheet_id = os.getenv('SPREADSHEET_ID')

@app.route('/add_expense', methods=['POST'])

def add_expense():
    data = request.get_json()
    service = get_sheets_service()
    values = [
        [
            data.get('date'),
            data.get('category'),
            data.get('amount'),
            data.get('description')
        ]
    ]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range='Sheet1',
        valueInputOption='RAW',
        body=body
    ).execute()

    return jsonify({'status': 'success', 'updatedCells': result.get('updates').get('updatedCells')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

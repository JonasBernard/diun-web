import os
import json
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Default to a 'data' directory in the current path, but allow environment override
DATA_FILE = os.environ.get('DATA_FILE', 'data/notifications.json')

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                return json.load(file)
        except Exception:
            return []
    return []

def save_data(data):
    os.makedirs(os.path.dirname(os.path.abspath(DATA_FILE)), exist_ok=True)
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    notifications = load_data()
    return render_template('index.html', notifications=notifications)

@app.route('/delete/<int:index>', methods=['POST'])
def delete_notification(index):
    data = load_data()
    # Check if index is valid
    if 0 <= index < len(data):
        data.pop(index)
        save_data(data)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # For local testing; production uses Gunicorn
    app.run(host='0.0.0.0', port=8080)

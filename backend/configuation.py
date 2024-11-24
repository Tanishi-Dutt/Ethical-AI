from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import os
import hashlib

import os
app = Flask(__name__)
class Config:
    SECRET_KEY = ''
    DATABASE_URI = ''
# Configuration settings
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')  # For sessions and CSRF protection
app.config['DEBUG'] = True  # Set to True for development; False for production

# If using a database, set the URI here; for SQLite, you can use the following:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Example connection string for SQLite

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan_url', methods=['POST'])
def scan_url():
    url = request.json.get('url')
    # Here you can include logic to actually scan the URL
    return jsonify({'status': 'success', 'url': url})

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the password
    # Here you would save the user's credentials to the database
    return jsonify({'status': 'success', 'message': 'User registered successfully!'})

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the provided password
    # Here you would verify the user credentials against the stored data
    return jsonify({'status': 'success', 'message': 'Login successful!'})

@socketio.on('connect')
def handle_connect():
    print('User connected')
    emit('alert', {'message': 'Connected to real-time monitoring service'})

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)

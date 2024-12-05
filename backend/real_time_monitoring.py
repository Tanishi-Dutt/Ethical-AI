


from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit
import sqlite3
import hashlib
import os

import time
import random

def monitor_activity():
    """
    Function to continuously monitor user activities in real-time.
    This function would run a loop checking for conditions.
    """
    while True:
        # Simulate a monitoring condition
        if random.choice([True, False]):  # Randomly trigger alerts for simulation
            print("Alert: Suspicious activity detected!")  # Replace with actual alert mechanism
        time.sleep(10)  # Check every 10 seconds

def start_monitoring():
    """
    Function to start real-time monitoring.
    This function could be enhanced to run in a separate thread if needed.
    """
    print("Real-time monitoring is now active.")
    monitor_activity()  # Start the monitoring process

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize the database (only run once)
def init_db():
    conn = sqlite3.connect('suspicious_activity.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suspicious_contacts (
            type TEXT NOT NULL, 
            identifier TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add suspicious contact
def add_suspicious_contact(contact_type, identifier):
    try:
        conn = sqlite3.connect('suspicious_activity.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO suspicious_contacts (type, identifier) VALUES (?, ?)', (contact_type, identifier))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while adding suspicious contact: {e}")
    finally:
        conn.close()

# Check if data is suspicious
def is_suspicious(data, data_type):
    conn = sqlite3.connect('suspicious_activity.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM suspicious_contacts WHERE type = ? AND identifier = ?', (data_type, data))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# User registration
def register_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        conn = sqlite3.connect('suspicious_activity.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        return {'status': 'success', 'message': 'User registered successfully!'}
    except sqlite3.IntegrityError:
        return {'status': 'error', 'message': 'Username already exists!'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    finally:
        conn.close()

# User login
def login_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('suspicious_activity.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {'status': 'success', 'message': 'Login successful!'}
    return {'status': 'error', 'message': 'Invalid username or password!'}

# Endpoint for monitoring transactions
@app.route('/transaction', methods=['POST'])
def monitor_transaction():
    transaction_data = request.json
    user_id = transaction_data['user_id']
    amount = transaction_data['amount']

    if amount > 5000 or is_suspicious(user_id, 'transaction'):
        alert_message = f"Suspicious transaction detected for User ID: {user_id}."
        socketio.emit('alert', {'message': alert_message})
        return jsonify({'status': 'Suspicious transaction detected'}), 403
    return jsonify({'status': 'Transaction approved'}), 200

# Endpoint for monitoring communications
@app.route('/communication', methods=['POST'])
def monitor_communication():
    comm_data = request.json
    comm_type = comm_data['type']  # Type could be 'call', 'message', or 'email'
    identifier = comm_data['identifier']

    if is_suspicious(identifier, comm_type):
        alert_message = f"Suspicious {comm_type} attempt from: {identifier}. Blocking."
        socketio.emit('alert', {'message': alert_message})
        return jsonify({'status': 'Blocked'}), 403
    return jsonify({'status': 'Allowed'}), 200

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    return jsonify(register_user(username, password))

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    return jsonify(login_user(username, password))

# SocketIO connection event
@socketio.on('connect')
def handle_connect():
    print('User connected')
    emit('alert', {'message': 'Connected to the monitoring service'})
if __name__ == '__main__':
    init_db()  # Initialize the database
    
    # Adding suspicious contacts for demonstration purposes
    add_suspicious_contact('call', '+1234567890')
    add_suspicious_contact('message', '+0987654321')
    add_suspicious_contact('email', 'suspicious@example.com')
    add_suspicious_contact('transaction', 'fraudulent_user_id')

    # Start the Flask application
    socketio.run(app, host='127.0.0.1', port=5000)

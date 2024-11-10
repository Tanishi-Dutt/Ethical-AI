from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import random
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize the database (only run once)
def init_db():
    conn = sqlite3.connect('suspicious_activity.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS suspicious_contacts (type TEXT, identifier TEXT)''')
    conn.commit()
    conn.close()

# Check if data is suspicious
def is_suspicious(data, data_type):
    conn = sqlite3.connect('suspicious_activity.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM suspicious_contacts WHERE type = ? AND identifier = ?', (data_type, data))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Endpoint for transaction monitoring
@app.route('/transaction', methods=['POST'])
def monitor_transaction():
    transaction_data = request.json
    user_id = transaction_data['user_id']
    amount = transaction_data['amount']

    # Detect suspicious transaction pattern
    if amount > 5000 or is_suspicious(user_id, 'transaction'):
        alert_message = f"Suspicious transaction detected for User ID: {user_id}."
        socketio.emit('alert', {'message': alert_message})
        return jsonify({'status': 'Suspicious transaction detected'}), 403
    return jsonify({'status': 'Transaction approved'}), 200

# Endpoint for communication monitoring
@app.route('/communication', methods=['POST'])
def monitor_communication():
    comm_data = request.json
    comm_type = comm_data['type']  # 'call', 'message', or 'email'
    identifier = comm_data['identifier']

    # Detect suspicious communication
    if is_suspicious(identifier, comm_type):
        alert_message = f"Suspicious {comm_type} attempt from: {identifier}. Blocking."
        socketio.emit('alert', {'message': alert_message})
        return jsonify({'status': 'Blocked'}), 403
    return jsonify({'status': 'Allowed'}), 200

if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=5000)



++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#populating teh suspicious contact IDs 

def add_suspicious_contact(contact_type, identifier):
    conn = sqlite3.connect('suspicious_activity.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO suspicious_contacts (type, identifier) VALUES (?, ?)', (contact_type, identifier))
    conn.commit()
    conn.close()

# Add suspicious numbers and emails
add_suspicious_contact('call', '+1234567890')
add_suspicious_contact('message', '+0987654321')
add_suspicious_contact('email', 'suspicious@example.com')
add_suspicious_contact('transaction', 'fraudulent_user_id')





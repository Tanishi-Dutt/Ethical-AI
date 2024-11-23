from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from threat_detection import *
from user_management import *
from database import init_db, add_suspicious_contact

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize the database
init_db()

@app.route('/transaction', methods=['POST'])
def monitor_transaction():
    data = request.json
    user_id, amount = data['user_id'], data['amount']
    # Example check for suspicious transactions
    if amount > 5000 or is_suspicious(user_id, 'transaction'):
        socketio.emit('alert', {'message': f"Suspicious transaction detected for User ID: {user_id}."})
        return jsonify({'status': 'Suspicious transaction detected'}), 403
    return jsonify({'status': 'Transaction approved'}), 200

# Additional endpoints for communication, user management, etc.
# Example: @app.route('/register', methods=['POST'])

if __name__ == '__main__':
    socketio.run(app, debug=True)

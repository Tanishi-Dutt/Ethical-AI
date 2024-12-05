from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit
import os
from configuation import Config  # Assuming this has your configuration settings
from encryption import encrypt_data, decrypt_data  # Encryption-related functions
from scam_detection import check_url_v2,check_scam_activity,detect_scam_phrases_v2   # Import the necessary functions
from real_time_monitoring import monitor_activity  # Placeholder for real-time monitoring functionality
from user_management import register_user, login_user  # User management functions
from secure_communication import send_secure_message  # Secure communication functions
from alert_system import show_threat_alert  # Alert system functions
from elder_friendly import show_alert  # Elderly-friendly alert functions

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration settings
socketio = SocketIO(app)

# Ensure the uploads folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')  # Ensure index.html is present in templates folder

# Route for scanning a URL
@app.route('/scan_url', methods=['POST'])
def scan_url():
    url = request.json.get('url')
    
    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    # Call the check_url function to get the scan result
    result = check_url_v2(url)

    # Return the result as JSON
    return jsonify(result)

# Route for detecting scam phrases
@app.route('/detect-scam-phrases', methods=['POST'])
def detect_scam_phrases_route():
    text = request.json.get('text')
    if not text:
        return jsonify({"status": "error", "message": "No text provided"}), 400

    # Detect scam phrases from the text
    detected_phrases = detect_scam_phrases_v2(text)
    
    return jsonify({"scam_phrases": detected_phrases})
    scam_result = detect_scam_phrases(text)
# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    return register_user(username, password)  # Ensure this is implemented in the user_management module

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    return login_user(username, password)  # Ensure this is implemented in the user_management module

# Real-time monitoring example
@socketio.on('connect')
def handle_connect():
    print('User connected')
    emit('alert', {'message': 'Connected to real-time monitoring service'})

# Route for sending a secure message
@app.route('/send-secure-message', methods=['POST'])
def send_secure():
    message = request.json.get('message')
    response = send_secure_message(message)  # Ensure appropriate logic in your secure_communication module
    return jsonify(response)

# Route for showing alerts
@app.route('/alert', methods=['POST'])
def alert():
    message = request.json.get('message')
    show_threat_alert(message)  # Display alert using the alert system logic
    return jsonify({"status": "alert displayed"})

# Route for elderly-friendly alerts
@app.route('/elder-alert', methods=['POST'])
def elder_alert_route():
    message = request.json.get('message')
    show_alert(message)  # Display elder-friendly alert
    return jsonify({"status": "elder alert displayed"})

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)

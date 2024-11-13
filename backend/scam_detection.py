import requests

def check_url(url):
    # Google Safe Browsing API URL
    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?AIzaSyCpr3J7Q2cEWRatpnUvipgzmSid5CTw38o"

    # Payload structure for the Safe Browsing API
    payload = {
        "client": {"clientId": "your-app", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    headers = {"Content-Type": "application/json"}

    # Send POST request to Google Safe Browsing API with the payload and headers
    response = requests.post(api_url, json=payload, headers=headers)

    # Parse the JSON response
    result = response.json()

    # Check if the result contains any threats
    if "matches" in result:
        return {"status": "dangerous", "details": result["matches"]}
    else:
        return {"status": "safe", "details": None}


!pip install SpeechRecognition
import speech_recognition as sr
import re
import nltk

# Download required NLTK data files (if not already done)
nltk.download('punkt')

# Sample list of scam-related phrases 
scam_phrases = [
    "urgent action required",
    "claim your prize",
    "Congraulations!you have won",
    "confirm your personal information",
    "limited time offer"
    "HsBc"
    "messageS"
    "Click to unlock"
    "
    
]

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def detect_scam_phrases(text):
    found_phrases = []
    for phrase in scam_phrases:
        if re.search(r"\b" + re.escape(phrase) + r"\b", text, re.IGNORECASE):
            found_phrases.append(phrase)
    return found_phrases

# Putting it together
file_path = "path_to_audio_file.wav"  # Replace with the actual audio file path, ask client to put the voice file in
transcribed_text = transcribe_audio(file_path)

if transcribed_text:
    detected_phrases = detect_scam_phrases(transcribed_text)
    if detected_phrases:
        print("Scam-related phrases detected:", detected_phrases)
    else:
        print("No scam-related phrases detected.")
else:
    print("Could not transcribe audio.")


!pip install scikit-learn pandas
import pandas as pd
from sklearn.ensemble import IsolationForest

# Example dataset
data = {
    "user_id": [1, 2, 1, 3, 1, 2, 3, 1, 2, 3],
    "transaction_amount": [200, 5000, 300, 7000, 250, 50, 10000, 90, 40, 60],
    "transaction_frequency": [3, 15, 7, 12, 2, 3, 18, 2, 1, 3]
}
df = pd.DataFrame(data)

# Features for fraud detection
X = df[["transaction_amount", "transaction_frequency"]]

# Initialize Isolation Forest model
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
df["fraud_flag"] = model.fit_predict(X)

# -1 indicates anomaly (potential fraud), 1 indicates normal behaviour
fraud_cases = df[df["fraud_flag"] == -1]
print("Detected potential fraud cases:\n", fraud_cases)


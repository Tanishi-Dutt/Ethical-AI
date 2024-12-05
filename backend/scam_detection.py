
import requests
import re
import nltk

# Sample list of scam-related phrases to detect in the text
scam_phrases = [
    "urgent action required",
    "claim your prize",
    "Congratulations! you have won",  # Fixed spelling
    "confirm your personal information",
    "limited time offer",
    "HSbC",  # Fixed case
    "messageS",  # Consider replacing with "messages" for correctness
    "Click to unlock"
]

# Function to check URLs with Google Safe Browsing API (using your own API key)
def check_url_v2(url):
    """Check if a URL is safe using Google Safe Browsing API."""
    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=YOUR_API_KEY"
    
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
    
    response = requests.post(api_url, json=payload, headers=headers)
    result = response.json()

    if "matches" in result:
        return {"status": "dangerous", "details": result["matches"]}
    else:
        return {"status": "safe", "details": None}

# Function to detect scam-related phrases in the given text
def detect_scam_phrases_v2(text):
    """Detect scam-related phrases in the given text."""
    found_phrases = []
    for phrase in scam_phrases:
        if re.search(r"\b" + re.escape(phrase) + r"\b", text, re.IGNORECASE):
            found_phrases.append(phrase)
    return found_phrases

# Optionally, you can have a function to test all functionality at once
def check_scam_activity(url, text):
    """
    Combines URL safety check and scam phrase detection
    Returns both results for comprehensive scanning.
    """
    # Check the URL using Google Safe Browsing API
    url_result = check_url_v2(url)
    
    # Detect scam phrases in the text
    scam_result = detect_scam_phrases_v2(text)
    
    # Combine both results and return
    combined_result = {
        "url_check": url_result,
        "scam_phrases": scam_result
    }
    return combined_result

# Import necessary functions from scam_detection.py
from scam_detection import check_url_v2, detect_scam_phrases_v2

# A possible main function to call both URL checking and scam phrase detection
def main(url, text):
    """Main function to scan both URL and text for scams."""
    
    # Check the URL with Google Safe Browsing API
    url_result = check_url_v2(url)
    
    # Detect scam phrases in the provided text
    scam_phrases_found = detect_scam_phrases_v2(text)
    
    # Combine results into a dictionary and return
    result = {
        "url_check": url_result,
        "scam_phrases": scam_phrases_found
    }
    
    return result

# Optionally, you can test the functions individually as well
if __name__ == "__main__":
    # Example test case
    url = "http://example.com/claim-your-prize"
    text = "Hurry! Claim your prize before it's too late!"

    # Run the scam check
    result = main(url, text)
    
    # Print the result
    print("Scam Check Result:", result)

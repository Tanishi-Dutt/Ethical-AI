import tkinter as tk
from tkinter import messagebox

def show_threat_alert(threat_type, threat_details):
    """
    Display a warning message to alert the user of a detected threat.
    
    Parameters:
    - threat_type (str): The type of threat detected (e.g., "Scam", "Phishing", "Malware").
    - threat_details (str): Additional details about the threat to help the user understand.
    """
    # Create a pop-up alert window
    message = f"Threat Detected: {threat_type}\n\nDetails: {threat_details}\n\nProceed with caution!"
    messagebox.showwarning("Security Alert", message)

def prompt_user_action(action_suggestion):
    """
    Prompt the user to take action in response to a detected threat.
    
    Parameters:
    - action_suggestion (str): Suggested action for the user (e.g., "Close the website", "Do not open the link").
    """
    messagebox.showinfo("Suggested Action", f"Suggested Action: {action_suggestion}")

def emergency_contact_alert(contact_name, contact_number):
    """
    Inform the user that their emergency contact is being notified.
    
    Parameters:
    - contact_name (str): Name of the emergency contact person.
    - contact_number (str): Phone number of the emergency contact person.
    """
    message = f"Notifying Emergency Contact:\n\nName: {contact_name}\nPhone: {contact_number}"
    messagebox.showinfo("Emergency Contact", message)

# Example usage
if __name__ == "__main__":
    # Create a sample tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Example of showing a threat alert
    show_threat_alert("Phishing", "Suspicious link detected in your email.")

    # Example of suggesting an action
    prompt_user_action("Close the email immediately and do not click any links.")

    # Example of notifying an emergency contact
    emergency_contact_alert(" "+ "")

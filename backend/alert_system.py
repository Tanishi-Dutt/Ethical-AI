import tkinter as tk
from tkinter import messagebox

# Function to display an alert message
def show_alert():
    messagebox.showwarning("Scam Alert", "Warning: This may be a scam. Proceed with caution!")

# Function to call emergency contact
def call_emergency_contact():
    messagebox.showinfo("Emergency Contact", "Calling your trusted contact...")

# Create the main window
window = tk.Tk()
window.title("Elderly-Friendly Interface")
window.geometry("400x600")
window.configure(bg="lightgray")

# High-contrast colors and large fonts
font_large = ("Helvetica", 16, "bold")

# Add a heading label
heading = tk.Label(window, text="Welcome!", font=("Helvetica", 20, "bold"), bg="lightgray")
heading.pack(pady=20)

# Add a button to show scam alert
alert_button = tk.Button(
    window, text="Show Scam Alert", font=font_large, bg="red", fg="white", 
    width=20, height=2, command=show_alert
)
alert_button.pack(pady=20)

# Add a button for emergency contact
emergency_button = tk.Button(
    window, text="Emergency Contact", font=font_large, bg="blue", fg="white", 
    width=20, height=2, command=call_emergency_contact
)
emergency_button.pack(pady=20)

# Add other navigation buttons (for simplicity, no function is assigned)
home_button = tk.Button(
    window, text="Home", font=font_large, bg="green", fg="white", 
    width=20, height=2
)
home_button.pack(pady=20)

settings_button = tk.Button(
    window, text="Settings", font=font_large, bg="purple", fg="white", 
    width=20, height=2
)
settings_button.pack(pady=20)

# Run the main event loop
window.mainloop()


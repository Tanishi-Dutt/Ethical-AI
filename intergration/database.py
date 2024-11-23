import sqlite3

def init_db():
    conn = sqlite3.connect('suspicious_activity.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS suspicious_contacts (type TEXT, identifier TEXT)''')
    conn.commit()
    conn.close()

def add_suspicious_contact(contact_type, identifier):
    conn = sqlite3.connect('suspicious_activity.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO suspicious_contacts (type, identifier) VALUES (?, ?)', (contact_type, identifier))
    conn.commit()
    conn.close()

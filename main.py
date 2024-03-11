from flask import Flask, request, render_template, redirect, url_for
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3

app = Flask(__name__)
DB_FILE = "chat_app.db"

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 sender_phone TEXT,
                 receiver_phone TEXT,
                 message TEXT)''')
    conn.commit()
    conn.close()

# Save message to the database
def save_message(sender_phone, receiver_phone, message):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT INTO messages (sender_phone, receiver_phone, message)
                 VALUES (?, ?, ?)''', (sender_phone, receiver_phone, message))
    conn.commit()
    conn.close()

# Route to render the chat interface
@app.route("/", methods=['GET', 'POST'])
def chat_interface():
    if request.method == 'POST':
        receiver_phone = request.form['receiver_phone']
        message_body = request.form['message_body']
        
        # Logic to send the SMS message (not implemented in this example)
        # You can use Twilio or another SMS service to send the message
        
        return redirect(url_for('chat_interface'))  # Redirect to refresh the page after sending the message
    else:
        # You can add more logic here to fetch messages from the database if needed
        messages = []  # Placeholder for messages, replace with actual message data
        
        return render_template("chat_interface.html", messages=messages)

# Handle incoming SMS
@app.route("/sms", methods=['POST'])
def sms():
    sender_phone = request.form['From']
    receiver_phone = request.form['To']
    message_body = request.form['Body']
    
    save_message(sender_phone, receiver_phone, message_body)
    
    resp = MessagingResponse()
    resp.message("Message received. Thank you!")
    return str(resp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
